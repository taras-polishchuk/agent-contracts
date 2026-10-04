# Contracts

Each file in this folder is a single **specialist contract**: one role, one
narrow responsibility, one clear handoff format.

## Common structure

Every contract has:

1. **YAML frontmatter** — machine-readable metadata:
   - `id` — unique slug for the role
   - `type` — `orchestrator` | `specialist`
   - `domain` (specialists only) — short noun phrase
   - `default_entry` (orchestrator only) — boolean, exactly one orchestrator sets this to `true`
   - `use_when[]` — non-empty list of routing triggers
   - `primary_sources[]` — generic categories this role reads first
   - `delegates_to[]` (orchestrator only) — the specialists it routes to
   - `collaborates_with[]` (specialists only) — peer specialists
   - `success_signals[]` — observable outcomes that mean the role did its job

2. **Markdown body** with these sections in order:
   - `# <Role Name>` — title
   - `## Mission` — what the role owns in one paragraph
   - `## Workspace Intent` *(optional)* — how this role sits in the wider workspace
   - `## Default Routing Rules` *(orchestrator only)* — when to delegate to each specialist
   - `## Owns` — bullet list of responsibilities
   - `## Read First` — ordered checklist of categories to consult
   - `## Working Method` — numbered steps
   - `## Output Contract` *(specialists)* / `## Output Format` *(orchestrator)* — required fields
   - `## Handoffs` *(specialists)* / `## Handoff Contract` *(orchestrator)* — destinations and contracts
   - `## Non-Goals` — explicit anti-scope

## Handoff shape

Every handoff between contracts uses four fields:

- **Goal** — what to achieve
- **Context** — files, decisions, constraints already known
- **Done when** — concrete completion criterion
- **Do not do** — anti-scope guard

The orchestrator never passes vague "figure it out" framing downstream.

## See also

- `../schema/contract.schema.json` — JSON Schema for frontmatter validation
- `../tools/validate-contracts.py` — CLI that walks this folder and validates
- `../docs/design-principles.md` — rationale behind the structure