# Design principles

These contracts are not just a prompt dump. They encode a small set of
opinions about how specialist agents should be designed and wired together.

## 1. One primary owner per task

Even when several specialists contribute, exactly one of them owns the
deliverable. The orchestrator names the primary owner. The other
contributors are listed explicitly with the slice they own.

This prevents the common failure mode where multiple agents each produce
a partial answer and the user has to reconcile them.

## 2. Narrow handoffs

Every handoff carries four fields: **Goal**, **Context**, **Done when**,
**Do not do**. The `Do not do` field is the most important one — it stops
specialists from drifting into each other's scope.

Handoffs are mechanical, not interpretive. The receiving specialist
should be able to start work without asking back.

## 3. No invented progress

Specialists must not invent status, metrics, or evidence that the repo
does not contain. If a number is needed but not present, the specialist
names the gap and stops, instead of guessing.

This is encoded in the `## Non-Goals` section of each contract and is
the strongest shared invariant across the library.

## 4. Portable paths

Contracts reference generic categories — `docs/roadmap.md`,
`learning/<topic>/`, `portfolio/case-<slug>/`. They never bind to an
absolute path on a specific machine. This lets the same contracts drop
into different workspaces without rewriting.

## 5. Output Contract is structured, not free-form

Each specialist's reply has an explicit `Output Contract` section that
names the required fields. The orchestrator's merge is mechanical because
each input is structured. If a reply is missing a required field, the
orchestrator raises it as a handoff violation, not as a content critique.

## 6. Specialists collaborate, not compete

Specialists declare `collaborates_with`, not `competes_with`. The
contracts are written assuming the user benefits from explicit handoffs,
not from each specialist owning the whole problem.

## 7. Anti-scope is documented

Every contract ends with `## Non-Goals`. This is not bureaucratic — it
is the most useful section when a specialist is being asked to do work
that belongs to a peer. The `Do not do` field in a handoff and the
`Non-Goals` section in a contract serve the same purpose from two
directions.

## 8. Default entry is exactly one

Exactly one contract has `default_entry: true` — the orchestrator. This
gives the workspace a single starting point for routing.

## 9. Frontmatter is the contract

The YAML frontmatter is not metadata for humans — it is the machine-
readable contract. `use_when`, `primary_sources`, `collaborates_with`,
and `success_signals` are the routing signals that downstream tooling
consumes.

The Markdown body is the human-readable elaboration. Both layers are
required: tooling without a body is unverifiable; a body without
frontmatter is unroutable.

## 10. MIT, not Apache-2.0

Plain-text prompts and schemas do not need a patent grant. MIT maximizes
downstream use and matches the dominant license for prompt/spec
collections.