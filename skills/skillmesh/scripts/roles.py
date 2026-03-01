#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


def _find_repo_root() -> Path | None:
    markers = ("src/skill_registry_rag/__main__.py", "examples/registry/tools.json")
    starts = [Path.cwd(), Path(__file__).resolve()]
    for start in starts:
        for candidate in [start, *start.parents]:
            if all((candidate / marker).exists() for marker in markers):
                return candidate
    return None


def _existing_path(value: str) -> str:
    p = Path(value).expanduser()
    return str(p.resolve()) if p.exists() else ""


def _default_catalog() -> str:
    env = os.getenv("SKILLMESH_CATALOG", "").strip()
    if env:
        return env

    env = os.getenv("SKILLMESH_REGISTRY", "").strip()
    if env:
        return env

    repo_root = _find_repo_root()
    if repo_root is not None:
        primary = repo_root / "examples" / "registry" / "tools.json"
        if primary.exists():
            return str(primary.resolve())

    cwd_candidate = _existing_path("examples/registry/tools.json")
    if cwd_candidate:
        return cwd_candidate
    return ""


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="skillmesh-roles",
        description="List and install SkillMesh role bundles.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    cmd_list = sub.add_parser("list", help="List available role bundles from catalog")
    cmd_list.add_argument("--catalog", default=_default_catalog())
    cmd_list.add_argument(
        "--registry",
        default="",
        help="Optional target registry to show installed status",
    )
    cmd_list.add_argument("--json", action="store_true")

    cmd_install = sub.add_parser(
        "install",
        help="Install role card and missing dependency cards into target registry",
    )
    cmd_install.add_argument("--catalog", default=_default_catalog())
    cmd_install.add_argument("--registry", required=True)
    cmd_install.add_argument("--role-id", required=True)
    cmd_install.add_argument("--dry-run", action="store_true")
    cmd_install.add_argument("--json", action="store_true")

    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    catalog = str(getattr(args, "catalog", "") or "").strip()
    if not catalog:
        print(
            "Error: Missing catalog path. Pass --catalog or set SKILLMESH_CATALOG.",
            file=sys.stderr,
        )
        return 2
    catalog_path = Path(catalog).expanduser()
    if not catalog_path.exists():
        print(f"Error: Catalog not found: {catalog_path}", file=sys.stderr)
        return 2

    cmd = ["skillmesh", "roles", args.command, "--catalog", str(catalog_path.resolve())]
    if args.command == "list":
        if args.registry:
            cmd.extend(["--registry", args.registry])
        if args.json:
            cmd.append("--json")
    else:
        cmd.extend(["--registry", args.registry, "--role-id", args.role_id])
        if args.dry_run:
            cmd.append("--dry-run")
        if args.json:
            cmd.append("--json")

    env = os.environ.copy()
    if shutil.which("skillmesh") is None:
        repo_root = _find_repo_root()
        if repo_root is not None:
            src_path = repo_root / "src"
            env["PYTHONPATH"] = str(src_path) + os.pathsep + env.get("PYTHONPATH", "")
        cmd = [sys.executable, "-m", "skill_registry_rag", *cmd[1:]]

    try:
        proc = subprocess.run(cmd, check=False, env=env)
        return int(proc.returncode)
    except FileNotFoundError:
        pretty = " ".join(shlex.quote(c) for c in cmd)
        print(
            "Error: SkillMesh CLI is not installed.\n"
            "Install with `pip install -e .` from the SkillMesh repo,\n"
            "or run from a checkout with:\n"
            f"  {pretty}",
            file=sys.stderr,
        )
        return 127


if __name__ == "__main__":
    raise SystemExit(main())
