# Examples

Runnable demonstrations of consuming a single contract.

## `example_load_contract.py`

Loads a contract file, splits YAML frontmatter from the Markdown body, and
prints a system prompt ready to be pasted into Claude, Cursor, Copilot, or
Codex.

```bash
python examples/example_load_contract.py solution-architect
```

The script has no third-party dependencies — it uses only the Python
standard library. It demonstrates the simplest possible integration: anyone can
read a contract and feed it into their LLM tool of choice.

## `multi-agent-workflow.md`

A worked walkthrough of a multi-agent task:

1. The user asks for a plan + design + landing-page copy.
2. The orchestrator routes to three specialists.
3. Each specialist produces its `Output Contract`.
4. The orchestrator merges the results into one coherent answer.

This is the reference scenario for non-trivial root tasks. Use it as a
template when designing your own multi-agent flows.