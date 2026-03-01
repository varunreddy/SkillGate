from __future__ import annotations

import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from skill_registry_rag.cli import main
from skill_registry_rag.roles import install_role_bundle, list_role_offers
from skill_registry_rag.registry import load_registry


def _catalog_path() -> Path:
    return Path(__file__).resolve().parents[1] / "examples" / "registry" / "tools.json"


def test_list_role_offers_includes_roles_and_dependency_counts():
    offers = list_role_offers(catalog_registry=str(_catalog_path()))
    by_id = {offer["id"]: offer for offer in offers}

    assert "role.data-engineer" in by_id
    assert by_id["role.data-engineer"]["dependency_count"] >= 8

    # This role has empty dependency list in tools.json and should fall back to role markdown.
    assert "role.devops-engineer" in by_id
    assert by_id["role.devops-engineer"]["dependency_count"] >= 8


def test_install_role_bundle_creates_registry_with_role_and_dependencies(tmp_path):
    target = tmp_path / "installed.registry.yaml"
    result = install_role_bundle(
        catalog_registry=str(_catalog_path()),
        target_registry=str(target),
        role_id="role.data-engineer",
    )

    assert target.exists()
    assert "role.data-engineer" in result["added_ids"]
    cards = load_registry(target)
    ids = {card.id for card in cards}
    assert "role.data-engineer" in ids
    assert "data.spark" in ids
    assert "cloud.terraform" in ids


def test_install_role_bundle_skips_existing_cards(tmp_path):
    catalog = json.loads(_catalog_path().read_text(encoding="utf-8"))
    tools = catalog["tools"]
    spark = [entry for entry in tools if entry.get("id") == "data.spark"][0]
    target = tmp_path / "existing.registry.json"
    target.write_text(json.dumps({"tools": [spark]}, indent=2), encoding="utf-8")

    result = install_role_bundle(
        catalog_registry=str(_catalog_path()),
        target_registry=str(target),
        role_id="role.data-engineer",
    )

    assert "data.spark" in result["already_present_ids"]
    reloaded = json.loads(target.read_text(encoding="utf-8"))
    ids = [entry["id"] for entry in reloaded["tools"]]
    assert ids.count("data.spark") == 1


def test_cli_roles_list_and_install_json(tmp_path):
    buf = StringIO()
    with redirect_stdout(buf):
        code = main(["roles", "list", "--catalog", str(_catalog_path()), "--json"])
    assert code == 0
    payload = json.loads(buf.getvalue())
    assert payload["roles"]

    target = tmp_path / "roles.registry.json"
    buf = StringIO()
    with redirect_stdout(buf):
        code = main(
            [
                "roles",
                "install",
                "--catalog",
                str(_catalog_path()),
                "--registry",
                str(target),
                "--role-id",
                "role.devops-engineer",
                "--json",
            ]
        )

    assert code == 0
    install_payload = json.loads(buf.getvalue())
    assert "role.devops-engineer" in install_payload["added_ids"]
    # Dependency parsing falls back to role markdown when dependencies are absent.
    assert "devops.nginx" in install_payload["added_ids"]
