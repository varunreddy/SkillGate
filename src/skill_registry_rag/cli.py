from __future__ import annotations

import argparse
import json
import os
import sys

from ._resolve import resolve_registry_path
from .adapters import render_claude_context, render_codex_context
from .roles import RoleCatalogError, install_role_bundle, list_role_offers
from .registry import RegistryError, load_registry
from .retriever import SkillRetriever


def _default_catalog_path() -> str:
    env_catalog = os.getenv("SKILLMESH_CATALOG", "").strip()
    if env_catalog:
        return env_catalog
    return os.getenv("SKILLMESH_REGISTRY", "").strip()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skillmesh",
        description="Top-k SkillMesh tool/role card retrieval for Codex/Claude style runtimes.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # index command
    index_cmd = sub.add_parser("index", help="Index registry into ChromaDB for persistent retrieval")
    index_cmd.add_argument("--registry", default=None, help="Path to tools/roles YAML/JSON")
    index_cmd.add_argument("--collection", default="skillmesh_experts", help="ChromaDB collection name")
    index_cmd.add_argument("--data-dir", default=None, help="ChromaDB persistence directory")
    index_cmd.add_argument("--ephemeral", action="store_true", help="Use ephemeral (in-memory) ChromaDB for testing")

    retrieve = sub.add_parser("retrieve", help="Retrieve top-k cards for query")
    retrieve.add_argument("--registry", default=None, help="Path to tools/roles YAML/JSON")
    retrieve.add_argument("--query", required=True, help="User query")
    retrieve.add_argument("--top-k", type=int, default=3, help="Top-k hits")
    retrieve.add_argument("--dense", action="store_true", help="Enable optional dense scoring")
    retrieve.add_argument("--backend", choices=["auto", "memory", "chroma"], default="auto", help="Retrieval backend")

    emit = sub.add_parser("emit", help="Emit provider-specific context block")
    emit.add_argument("--provider", required=True, choices=["codex", "claude"], help="Target provider")
    emit.add_argument("--registry", default=None, help="Path to tools/roles YAML/JSON")
    emit.add_argument("--query", required=True, help="User query")
    emit.add_argument("--top-k", type=int, default=3, help="Top-k hits")
    emit.add_argument("--dense", action="store_true", help="Enable optional dense scoring")
    emit.add_argument("--backend", choices=["auto", "memory", "chroma"], default="auto", help="Retrieval backend")
    emit.add_argument(
        "--instruction-chars",
        type=int,
        default=700,
        help="Max instruction text per retrieved expert",
    )

    roles = sub.add_parser("roles", help="Role commands")
    roles_sub = roles.add_subparsers(dest="roles_command", required=True)

    roles_list = roles_sub.add_parser("list", help="List available role cards from catalog")
    roles_list.add_argument(
        "--catalog",
        default=_default_catalog_path(),
        help="Path to source tools/roles catalog YAML/JSON",
    )
    roles_list.add_argument(
        "--registry",
        default="",
        help="Optional installed registry path for showing installed/missing status",
    )
    roles_list.add_argument("--json", action="store_true", help="Emit JSON output")

    roles_install = roles_sub.add_parser(
        "install",
        help="Install selected role card and missing dependency cards into registry",
    )
    roles_install.add_argument(
        "--catalog",
        default=_default_catalog_path(),
        help="Path to source tools/roles catalog YAML/JSON",
    )
    roles_install.add_argument(
        "--registry",
        required=True,
        help="Target registry YAML/JSON to write role/dependency cards into",
    )
    roles_install.add_argument(
        "--role-id",
        required=True,
        help="Role card id to install (example: role.data-engineer)",
    )
    roles_install.add_argument("--dry-run", action="store_true", help="Show changes only")
    roles_install.add_argument("--json", action="store_true", help="Emit JSON output")

    return parser


def _hits_payload(hits):
    payload = []
    for hit in hits:
        payload.append(
            {
                "id": hit.card.id,
                "title": hit.card.title,
                "domain": hit.card.domain,
                "description": hit.card.description,
                "tags": hit.card.tags,
                "tool_hints": hit.card.tool_hints,
                "aliases": hit.card.aliases,
                "dependencies": hit.card.dependencies,
                "input_contract": hit.card.input_contract,
                "output_artifacts": hit.card.output_artifacts,
                "quality_checks": hit.card.quality_checks,
                "constraints": hit.card.constraints,
                "risk_level": hit.card.risk_level,
                "maturity": hit.card.maturity,
                "metadata": hit.card.metadata,
                "score": hit.score,
                "sparse_score": hit.sparse_score,
                "dense_score": hit.dense_score,
            }
        )
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "roles":
        catalog = str(getattr(args, "catalog", "") or "").strip()
        if not catalog:
            print(
                "Error: missing --catalog. Provide a catalog path or set SKILLMESH_CATALOG.",
                file=sys.stderr,
            )
            return 2

        try:
            if args.roles_command == "list":
                offers = list_role_offers(
                    catalog_registry=catalog,
                    installed_registry=(args.registry or None),
                )
                if args.json:
                    print(json.dumps({"roles": offers}, indent=2))
                    return 0

                print(f"Catalog: {catalog}")
                if args.registry:
                    print(f"Installed registry: {args.registry}")
                print(f"Roles available: {len(offers)}")
                print("")
                print("ID | DEPENDENCIES | INSTALLED | TITLE")
                for offer in offers:
                    installed = "yes" if offer["installed"] else "no"
                    print(
                        f"{offer['id']} | {offer['dependency_count']} | "
                        f"{installed} | {offer['title']}"
                    )
                return 0

            result = install_role_bundle(
                catalog_registry=catalog,
                target_registry=args.registry,
                role_id=args.role_id,
                dry_run=bool(args.dry_run),
            )
            if args.json:
                print(json.dumps(result, indent=2))
                return 0

            action = "Dry run for" if args.dry_run else "Installed"
            print(f"{action} role bundle: {result['role_id']}")
            print(f"Catalog: {result['catalog_registry']}")
            print(f"Target registry: {result['target_registry']}")
            print(
                f"Added cards: {len(result['added_ids'])} "
                f"({', '.join(result['added_ids']) if result['added_ids'] else 'none'})"
            )
            print(
                f"Already present: {len(result['already_present_ids'])} "
                "("
                f"{', '.join(result['already_present_ids']) if result['already_present_ids'] else 'none'}"
                ")"
            )
            if result["copied_instruction_files"]:
                print(
                    f"Instruction files {'to copy' if args.dry_run else 'copied'}: "
                    f"{len(result['copied_instruction_files'])}"
                )
            if result["unresolved_dependencies"]:
                print(
                    "Unresolved dependencies: "
                    + ", ".join(result["unresolved_dependencies"])
                )
            return 0
        except RoleCatalogError as exc:
            print(f"RoleCatalogError: {exc}", file=sys.stderr)
            return 2

    try:
        registry_path = resolve_registry_path(args.registry)
        cards = load_registry(registry_path)
    except (RegistryError, ValueError) as exc:
        print(f"RegistryError: {exc}", file=sys.stderr)
        return 2

    if args.command == "index":
        from .backends.chroma import ChromaBackend

        backend = ChromaBackend(
            collection_name=args.collection,
            data_dir=args.data_dir,
            ephemeral=args.ephemeral,
        )
        backend.index(cards)
        print(f"Indexed {len(cards)} cards into collection '{args.collection}'")
        return 0

    backend_choice = getattr(args, "backend", "auto")
    retriever = SkillRetriever(
        cards,
        use_dense=bool(getattr(args, "dense", False)),
        backend=backend_choice,
    )
    hits = retriever.retrieve(args.query, top_k=args.top_k)

    if args.command == "retrieve":
        print(json.dumps({"query": args.query, "hits": _hits_payload(hits)}, indent=2))
        return 0

    if args.provider == "codex":
        out = render_codex_context(args.query, hits, instruction_chars=args.instruction_chars)
    else:
        out = render_claude_context(args.query, hits, instruction_chars=args.instruction_chars)

    print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
