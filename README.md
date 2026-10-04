# Agent Contracts

A small, opinionated library of **specialist agent contracts** for AI-assisted
engineering workspaces. Each contract is a plain-text Markdown file with YAML
frontmatter that defines a single role: when to use it, what it reads, what it
hands off, and what "done" looks like.

## Why contracts?

Most AI coding assistants run on a single system message. The result is the same
prompt trying to be a solution architect, a planner, an implementer, and a
copywriter — and failing at each one.

This package takes the opposite approach: **one specialist per role, narrow
handoffs, one merged result.** A top-level **orchestrator** routes tasks to
the right specialist (or set of specialists) and returns a single coherent
answer.

The contracts are designed to be loaded into Claude, Cursor, Copilot, Codex,
or any other LLM environment that accepts a system prompt. They are pure
Markdown with YAML frontmatter — no runtime, no SDK lock-in.

## What's included

| Contract | Role |
|----------|------|
| `orchestrator`        | Single entrypoint. Routes tasks, picks primary owner, coordinates multi-agent workflows. |
| `chief-of-staff`      | Planning, prioritization, weekly/daily execution, progress tracking. |
| `learning-coach`      | Explains concepts, builds study plans, designs exercises. |
| `solution-architect`  | System architecture, design review, trade-off analysis, ADR framing. |
| `automation-engineer` | Implementation: workflows, API integrations, scripts, working artifacts. |
| `personal-brand`      | Translates technical work into market-facing assets (GitHub, LinkedIn, resume, case studies). |

Each contract is one file under `contracts/`. See `contracts/README.md` for
the common structure.

## Quick start

### 1. Pick a contract

Open the file that matches the task:

```text
"I need to plan the next 2 weeks of work"
  → contracts/chief-of-staff.md

"I need to design the data flow for an agent system"
  → contracts/solution-architect.md

"I'm not sure who should own this"
  → contracts/orchestrator.md
```

### 2. Load it as a system prompt

Copy the contents of the contract file into your LLM tool's system-prompt
field. Every contract is self-contained — no additional context is required
to start.

### 3. Combine for multi-agent tasks

When the orchestrator routes to multiple specialists, load each contract in
sequence (or in parallel where the tool supports it), then merge results
following the contract's `Output Format` section.

For a runnable example, see `examples/example_load_contract.py`.

## Design principles

- **One primary owner per task.** Even when multiple agents contribute.
- **Narrow handoffs.** Every handoff has `Goal`, `Context`, `Done when`, `Do not do`.
- **No invented progress.** Agents do not fabricate evidence, metrics, or status.
- **Portable.** Contracts reference generic categories (`docs/roadmap.md`,
  `learning/<topic>/`, `portfolio/`) so they drop into any workspace.

See `docs/design-principles.md` for the full rationale.

## Adding a new specialist

1. Copy `contracts/<closest-existing>.md` as a starting point.
2. Fill in YAML frontmatter (`id`, `type`, `domain`, `use_when[]`,
   `primary_sources[]`, `collaborates_with[]`, `success_signals[]`).
3. Add `Handoff Contract` and `Output Contract` sections.
4. Add the new role to the orchestrator's `delegates_to` list.
5. Run `python tools/validate-contracts.py` — it checks frontmatter against
   `schema/contract.schema.json`.

## Repository layout

```
agent-contracts/
├── LICENSE                              # MIT
├── README.md                            # this file
├── .editorconfig
├── .gitignore
├── contracts/                           # the 6 specialist contracts
│   ├── README.md
│   ├── orchestrator.md
│   ├── chief-of-staff.md
│   ├── learning-coach.md
│   ├── solution-architect.md
│   ├── automation-engineer.md
│   └── personal-brand.md
├── schema/
│   └── contract.schema.json             # JSON Schema for validating frontmatter
├── tools/
│   └── validate-contracts.py            # CLI: validates every contract.md
├── examples/
│   ├── README.md
│   ├── example_load_contract.py         # runnable demo: load a contract
│   └── multi-agent-workflow.md          # worked multi-agent walkthrough
└── docs/
    └── design-principles.md             # why one-primary-owner, narrow handoffs, etc.
```

## License

MIT — see [LICENSE](./LICENSE). Use these contracts in commercial work,
derivative prompts, or internal tooling without attribution required (but
appreciated).