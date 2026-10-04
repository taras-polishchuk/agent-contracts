#!/usr/bin/env python3
"""Load a contract's YAML frontmatter and Markdown body, print a system
prompt ready to paste into an LLM tool.

Usage:
    python examples/example_load_contract.py <specialist-id>

- specialist-id is the `id` value from a contract's frontmatter.
- The script looks for `contracts/<id>.md` next to the repo root.
- Output: a header echoing the role metadata + the contract body.

No third-party dependencies.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = REPO_ROOT / "contracts"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_contract(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, markdown_body) for a contract file."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("no leading YAML frontmatter block found")
    # Minimal YAML subset. The frontmatter is intentionally simple so a
    # tiny hand-rolled parser is enough for this example. For arbitrary
    # YAML, use PyYAML.
    frontmatter = _tiny_yaml(match.group(1))
    body = match.group(2).strip()
    return frontmatter, body


def _tiny_yaml(block: str) -> dict:
    """Parse the small subset of YAML used by these contracts.

    Supports:
        key: value
        key:
          - item
          - item
    """
    out: dict = {}
    current_list_key: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError(f"list item outside a list: {line!r}")
            out[current_list_key].append(line[4:].strip())
            continue
        if line.endswith(":"):
            current_list_key = line[:-1].strip()
            out[current_list_key] = []
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current_list_key = None
            if value.lower() in {"true", "false"}:
                out[key] = value.lower() == "true"
            else:
                out[key] = value
            continue
        raise ValueError(f"unrecognised frontmatter line: {line!r}")
    return out


def build_system_prompt(meta: dict, body: str) -> str:
    """Echo role metadata, then the contract body."""
    header = (
        f"You are operating as the '{meta.get('id', 'unknown')}' specialist.\n"
        f"Type: {meta.get('type', 'unknown')}.\n"
    )
    if "domain" in meta:
        header += f"Domain: {meta['domain']}.\n"
    if meta.get("use_when"):
        header += "Use this role when:\n"
        for trigger in meta["use_when"]:
            header += f"  - {trigger}\n"
    if meta.get("success_signals"):
        header += "\nSuccess signals:\n"
        for signal in meta["success_signals"]:
            header += f"  - {signal}\n"
    return header.rstrip() + "\n\n" + body + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write(
            "usage: python example_load_contract.py <specialist-id>\n"
        )
        sys.stderr.write(
            "  example: python example_load_contract.py solution-architect\n"
        )
        return 2

    specialist_id = sys.argv[1]
    contract_path = CONTRACTS_DIR / f"{specialist_id}.md"
    if not contract_path.exists():
        available = sorted(p.stem for p in CONTRACTS_DIR.glob("*.md") if p.name != "README.md")
        sys.stderr.write(
            f"unknown specialist {specialist_id!r}. "
            f"Available: {available}\n"
        )
        return 2

    text = contract_path.read_text(encoding="utf-8")
    meta, body = parse_contract(text)
    prompt = build_system_prompt(meta, body)

    print(f"# System prompt for specialist: {specialist_id}\n")
    print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())