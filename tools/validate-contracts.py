#!/usr/bin/env python3
"""Validate every contract's YAML frontmatter against the JSON Schema.

Walks ``contracts/*.md`` (excluding README.md), parses the leading
``---\n...\n---\n`` frontmatter with PyYAML, and validates it against
``schema/contract.schema.json`` via jsonschema.

Exits 0 on success, 1 on the first validation failure (with a clear
error message), 2 on usage / dependency problems.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:
    sys.stderr.write("jsonschema is required: pip install jsonschema\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = REPO_ROOT / "contracts"
SCHEMA_PATH = REPO_ROOT / "schema" / "contract.schema.json"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("no leading YAML frontmatter block found")
    loaded = yaml.safe_load(match.group(1))
    if not isinstance(loaded, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return loaded


def main() -> int:
    if not SCHEMA_PATH.exists():
        sys.stderr.write(f"schema missing: {SCHEMA_PATH}\n")
        return 2

    with SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = Draft202012Validator(schema)

    contract_files = sorted(
        p for p in CONTRACTS_DIR.glob("*.md") if p.name != "README.md"
    )
    if not contract_files:
        sys.stderr.write(f"no contracts found in {CONTRACTS_DIR}\n")
        return 2

    failures = 0
    for path in contract_files:
        text = path.read_text(encoding="utf-8")
        try:
            frontmatter = parse_frontmatter(text)
        except (ValueError, yaml.YAMLError) as exc:
            sys.stderr.write(f"{path.name}: frontmatter invalid — {exc}\n")
            failures += 1
            continue

        errors = sorted(validator.iter_errors(frontmatter), key=lambda e: e.path)
        if errors:
            for err in errors:
                loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
                sys.stderr.write(f"{path.name}: {loc}: {err.message}\n")
            failures += 1
            continue

        print(f"{path.name}: OK ({frontmatter.get('id')})")

    # Cross-contract: orchestrator's delegates_to must point to existing IDs.
    orchestrator_files = [p for p in contract_files if "type: orchestrator" in path.read_text(encoding="utf-8").split("---", 2)[1]]
    known_ids = set()
    for p in contract_files:
        try:
            known_ids.add(parse_frontmatter(p.read_text(encoding="utf-8"))["id"])
        except (ValueError, yaml.YAMLError):
            pass

    for path in orchestrator_files:
        try:
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        except (ValueError, yaml.YAMLError):
            continue
        for target in fm.get("delegates_to", []) or []:
            if target not in known_ids:
                sys.stderr.write(
                    f"{path.name}: delegates_to references unknown id: {target!r}\n"
                )
                failures += 1

    # Exactly one default_entry.
    defaults = [p for p in contract_files if _has_default_entry(p)]
    if len(defaults) != 1:
        names = ", ".join(p.name for p in defaults) or "<none>"
        sys.stderr.write(
            f"expected exactly one default_entry contract, found {len(defaults)}: {names}\n"
        )
        failures += 1

    if failures:
        sys.stderr.write(f"\n{failures} failure(s)\n")
        return 1
    print(f"\nAll {len(contract_files)} contracts validated.")
    return 0


def _has_default_entry(path: Path) -> bool:
    try:
        return bool(parse_frontmatter(path.read_text(encoding="utf-8")).get("default_entry"))
    except (ValueError, yaml.YAMLError):
        return False


if __name__ == "__main__":
    sys.exit(main())