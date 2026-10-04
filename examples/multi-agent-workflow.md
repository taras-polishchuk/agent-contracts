# Multi-agent workflow — worked example

Scenario: the user wants to ship a small AI helper that summarizes new
RSS entries into Slack. They ask the workspace: "Plan, design, and write
the landing-page copy for this."

The orchestrator routes to three specialists. This file walks through the
routing, the per-specialist output, and the merge.

---

## 1. Orchestrator routing

The orchestrator's `## Decision Policy` is applied:

1. Single-owner or multi-agent? **Multi-agent** — the task spans planning,
   architecture, and market copy.
2. Primary owner: **`chief-of-staff`** for the plan.
3. Secondary contributors:
   - **`solution-architect`** for the system design.
   - **`personal-brand`** for the landing-page copy.
4. Chief of Staff is involved at least as a framing layer (rule 4).

`automation-engineer` is **not** invoked yet — there is no implementation
work in this round. The deliverable is a plan + design + copy, all of
which will become a handoff to `automation-engineer` next iteration.

## 2. Handoff shape — what the orchestrator sends each specialist

Each handoff carries: `Goal`, `Context`, `Done when`, `Do not do`.

### To chief-of-staff

- **Goal** — produce a 2-week execution plan for shipping the RSS → Slack
  summarizer, including a staging rollout.
- **Context** — repo is greenfield; user has 6 hours/week for this; user
  prefers n8n over custom code for the orchestration layer; existing
  `infrastructure/n8n/` is already wired.
- **Done when** — a numbered plan with explicit `Done when` per item, plus
  a now/next/later priority split.
- **Do not do** — do not propose a custom microservice stack; do not invent
  dependencies the repo does not have.

### To solution-architect

- **Goal** — produce the system design: data flow, components, failure
  modes, cost.
- **Context** — RSS polling every 5 min, ~50 sources; Slack channel is
  `#ai-product-team`; summarization must be cheap and idempotent; the
  user wants guardrails against hallucinated summaries.
- **Done when** — a one-page architecture with one recommended design and
  one fallback, plus a risks/trade-offs section.
- **Do not do** — do not design a Kubernetes stack; do not propose a
  long-running LLM deployment.

### To personal-brand

- **Goal** — write the landing-page copy for the public beta.
- **Context** — target audience: solo founders and small teams drowning in
  RSS; outcome metric is hours saved per week; the public artifact will
  live on the portfolio site.
- **Done when** — headline + 3-bullet value prop + 1 CTA, in the tone
  defined by `repackaging/positioning/`.
- **Do not do** — do not promise enterprise-grade reliability; do not
  invent case-study numbers.

## 3. Per-specialist output (truncated)

### chief-of-staff → `Output Contract`

1. **Current state** — greenfield repo, infra wired, no summarizer
   implementation.
2. **Priority order** — now (week 1): wire the 1-source prototype; next
   (week 2): fan out to 50 sources + Slack delivery; later: monitoring and
   cost guardrails.
3. **Execution plan** — six steps, each with `Done when`.
4. **Blockers** — none on the build side; one external decision: which LLM
   provider the user wants to commit to.
5. **Required handoffs** — once the design lands, dispatch
   `automation-engineer` to wire the prototype.

### solution-architect → `Output Contract`

1. **Problem framing** — turn a noisy RSS firehose into one summarized
   Slack post per source per day, with provenance and idempotency.
2. **Recommended architecture** — n8n polls RSS, dedupes, batches into a
   single LLM call per day per source, posts to Slack. Two-stage filter:
   cheap classifier first, expensive summarizer only for items passing
   the filter.
3. **Why this design** — cheap first, expensive second; provenance is
   preserved; idempotency lives in the dedup table.
4. **Risks and trade-offs** — LLM cost spikes if the cheap classifier is
   too generous; Slack rate limits if batching is too coarse.
5. **Implementation handoff** — six bullet points naming the n8n nodes and
   the dedup table.
6. **Open questions** — choice of LLM provider, choice of cheap classifier.

### personal-brand → `Output Contract`

1. **Target asset** — landing page for the public beta.
2. **Audience** — solo founders and small teams drowning in RSS.
3. **Core message** — turn 50 feeds into one daily Slack digest in five
   minutes a day, with provenance.
4. **Proof used** — six-week internal beta, 28 users, median 4.1 hours
   saved per week per user (placeholder — to be replaced with real data).
5. **Draft copy** — headline + 3-bullet value prop + 1 CTA.
6. **Proof gaps** — internal beta numbers not yet public; needs a publish
   gate before launch.

## 4. Orchestrator merge — single coherent reply

The orchestrator's `## Output Format` is applied:

1. **Primary agent** — chief-of-staff.
2. **Why this route** — the task is multi-zone; planning is the spine,
   architecture and copy are parallel contributors.
3. **Delegations** — solution-architect and personal-brand ran in
   parallel; their outputs are condensed below.
4. **Plan** — (chief-of-staff's execution plan, full).
5. **Deliverable** — the merged artifact: plan + architecture summary +
   landing-page copy, all in one reply.

The merge is not a literal concatenation. It is a re-write of the three
specialist outputs into one voice, with the orchestrator's framing on top.

---

## Why this works

- The orchestrator picks the smallest correct specialist set.
- Each specialist produces a structured `Output Contract`, not a free-form
  essay — so the merge is mechanical, not interpretive.
- Each handoff carries a `Do not do` field, which prevents specialists
  from drifting into each other's scope.
- The user sees one answer, not three. The three contracts are an
  implementation detail of the orchestrator.