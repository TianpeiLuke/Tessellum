---
tags:
  - resource
  - documentation
  - hermes_agent
  - delegation
  - multi_agent
keywords:
  - delegate_task patterns
  - parallel research subagents
  - fresh-context code review
  - compare alternatives
  - multi-file refactoring
  - gather then analyze
  - toolset scoping
  - delegation concurrency depth
topics:
  - Hermes Agent
  - Subagent Delegation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns
access_control_group: ["general"]
---

# Hermes Agent — Delegation Patterns

## Overview

Delegation Patterns is the applied how-to layer over Hermes's `delegate_task` tool: a catalog of when (and when not) to spawn isolated child agents and the concrete prompt shapes for the common cases — parallel research, fresh-context code review, compare-alternatives, multi-file refactoring, and the `execute_code`-gather → delegate-analyze combo. Hermes can spawn isolated child agents that work on tasks in parallel; **each subagent gets its own conversation, terminal session, and toolset, and only the final summary comes back — intermediate tool calls never enter the parent's context window.** That context-isolation property is the whole point: it both keeps the parent context clean and forces you to articulate the subtask precisely. This guide is the recipe layer; for the complete delegation reference (all parameters, ACP integration, advanced config) it links out to the Subagent Delegation feature page.

## When to Delegate

**Good candidates for delegation:**

- Reasoning-heavy subtasks (debugging, code review, research synthesis).
- Tasks that would flood the parent context with intermediate data.
- Parallel independent workstreams (research A and B simultaneously).
- Fresh-context tasks where the agent should approach without bias.

**Use something else instead:**

- A single tool call → just use the tool directly.
- Mechanical multi-step work with logic between steps → `execute_code`.
- Tasks needing user interaction → subagents cannot use `clarify`.
- Quick file edits → do them directly.
- Durable long-running work that must outlive the current turn → `cronjob` or `terminal(background=True, notify_on_complete=True)`. `delegate_task` is **synchronous**: if the parent turn is interrupted, active children are cancelled and their work is discarded.

## Pattern: Parallel Research

Research multiple topics simultaneously and get structured summaries back. A plain-language request ("Research these three topics in parallel … focus on recent developments and key players") drives the agent to issue one `delegate_task` call carrying a list of tasks:

```python
delegate_task(tasks=[
    {
        "goal": "Research WebAssembly outside the browser in 2025",
        "context": "Focus on: runtimes (Wasmtime, Wasmer), cloud/edge use cases, WASI progress",
        "toolsets": ["web"]
    },
    {
        "goal": "Research RISC-V server chip adoption",
        "context": "Focus on: server chips shipping, cloud providers adopting, software ecosystem",
        "toolsets": ["web"]
    },
    {
        "goal": "Research practical quantum computing applications",
        "context": "Focus on: error correction breakthroughs, real-world use cases, key companies",
        "toolsets": ["web"]
    }
])
```

All tasks run concurrently. Each subagent searches the web independently and returns a summary; the parent then synthesizes them into a coherent briefing.

## Pattern: Code Review

Delegate a review to a fresh-context subagent that approaches the code without preconceptions. The key is the `context` field — it must include **everything** the subagent needs, because the subagent knows nothing about the parent conversation:

```python
delegate_task(
    goal="Review src/auth/ for security issues and fix any found",
    context="""Project at /home/user/webapp. Python 3.11, Flask, PyJWT, bcrypt.
    Auth files: src/auth/login.py, src/auth/jwt.py, src/auth/middleware.py
    Test command: pytest tests/auth/ -v
    Focus on: SQL injection, JWT validation, password hashing, session management.
    Fix issues found and verify tests pass.""",
    toolsets=["terminal", "file"]
)
```

**The Context Problem (warning).** Subagents know *absolutely nothing* about the parent conversation — they start completely fresh. Delegating "fix the bug we were discussing" leaves the subagent with no idea what bug is meant. Always pass file paths, error messages, project structure, and constraints explicitly.

## Pattern: Compare Alternatives & Multi-File Refactoring

**Compare alternatives.** Evaluate multiple approaches to the same problem in parallel, then pick one — e.g. "add full-text search to our Django app; evaluate PostgreSQL tsvector, Elasticsearch, and Meilisearch in parallel — for each: setup complexity, query capabilities, resource requirements, maintenance overhead; compare and recommend." Each subagent researches one option in isolation, so there is no cross-contamination; the parent receives all summaries and makes the comparison.

**Multi-file refactoring.** Split a large refactor across parallel subagents, **one file (or file group) per subagent**, each with the old→new format, the relevant paths, the import to add, and the test command — handler files to one subagent, the client SDK to another, the docs to a third, e.g.:

```python
delegate_task(tasks=[
    {
        "goal": "Refactor all API endpoint handlers to use the new response format",
        "context": """Project at /home/user/api-server.
        Files: src/handlers/users.py, src/handlers/auth.py, src/handlers/billing.py
        Old format: return {"data": result, "status": "ok"}
        New format: return APIResponse(data=result, status=200).to_dict()
        Import: from src.responses import APIResponse
        Run tests after: pytest tests/handlers/ -v""",
        "toolsets": ["terminal", "file"]
    },
    # ... one task each for the client SDK and the API docs
])
```

Each subagent gets its own terminal session, so they can work in the same project directory without stepping on each other **as long as they edit different files**. If two subagents might touch the same file, handle that file yourself after the parallel work completes.

## Pattern: Gather Then Analyze

Use `execute_code` for mechanical data gathering, then delegate the reasoning-heavy analysis — often the most efficient pattern. `execute_code` handles the 10+ sequential tool calls cheaply, then a single subagent does the one expensive reasoning task with a clean context:

```python
# Step 1: Mechanical gathering (execute_code — no reasoning needed)
execute_code("""
from hermes_tools import web_search, web_extract
results = []
for query in ["AI funding Q1 2026", "AI startup acquisitions 2026", "AI IPOs 2026"]:
    r = web_search(query, limit=5)
    for item in r["data"]["web"]:
        results.append({"title": item["title"], "url": item["url"], "desc": item["description"]})
content = web_extract([r["url"] for r in results[:5]])
import json
with open("/tmp/ai-funding-data.json", "w") as f:
    json.dump({"search_results": results, "extracted": content["results"]}, f)
""")

# Step 2: Reasoning-heavy analysis (delegation is better here)
delegate_task(
    goal="Analyze AI funding data and write a market report",
    context="""Raw data at /tmp/ai-funding-data.json contains search results and
    extracted web pages about AI funding, acquisitions, and IPOs in Q1 2026.
    Write a structured market report: key deals, trends, notable players,
    and outlook. Focus on deals over $100M.""",
    toolsets=["terminal", "file"]
)
```

## Toolset Selection

Choose toolsets by what the subagent actually needs — restricting them keeps the subagent focused and prevents accidental side effects (e.g. a research subagent running shell commands):

| Task type | Toolsets | Why |
|-----------|----------|-----|
| Web research | `["web"]` | web_search + web_extract only |
| Code work | `["terminal", "file"]` | shell access + file operations |
| Full-stack | `["terminal", "file", "web"]` | everything except messaging |
| Read-only analysis | `["file"]` | can only read files, no shell |

## Constraints & Tuning

- **Default 3 parallel tasks** — batches default to 3 concurrent subagents (`delegation.max_concurrent_children` in `config.yaml`; floor 1, no hard ceiling).
- **Nested delegation is opt-in** — leaf subagents (default) cannot call `delegate_task`, `clarify`, `memory`, `send_message`, or `execute_code`. Orchestrator subagents (`role="orchestrator"`) retain `delegate_task`, but only when `delegation.max_spawn_depth` is raised above the default of 1 (floor 1, no ceiling); the other four stay blocked. Disable globally via `delegation.orchestrator_enabled: false`.
- **Separate terminals** — each subagent gets its own terminal session, working directory, and state.
- **No conversation history** — subagents see only the `goal` and `context` the parent passes.
- **Default 50 iterations** — set `max_iterations` lower for simple tasks to save cost.
- **Not durable** — `delegate_task` is synchronous and runs inside the parent turn; if the parent is interrupted (new message, `/stop`, `/new`), active children are cancelled (`status="interrupted"`) and discarded. For work that must outlive the turn, use `cronjob` or `terminal(background=True, notify_on_complete=True)`.

The two tuning knobs together — e.g. 30 parallel workers with nested subagents:

```yaml
delegation:
  max_concurrent_children: 30
  max_spawn_depth: 2
```

| Config | Default | Range | Effect |
|--------|---------|-------|--------|
| `max_concurrent_children` | 3 | >=1 | parallel batch size per `delegate_task` call |
| `max_spawn_depth` | 1 | >=1 | how many delegation levels can spawn further |

## Tips

- **Be specific in goals.** "Fix the bug" is too vague; "Fix the TypeError in api/handlers.py line 47 where process_request() receives None from parse_body()" gives the subagent enough to work with.
- **Include file paths.** Subagents don't know the project structure — always pass absolute paths, the project root, and the test command.
- **Use delegation for context isolation.** Delegating forces you to articulate the problem clearly, and the subagent approaches it without the assumptions that built up in the conversation.
- **Check results.** Subagent summaries are just summaries; if one says "fixed the bug and tests pass," verify by running the tests yourself or reading the diff.

**Source**: `inbox/hermes_agent_docs/guides/delegation-patterns.md` · https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns
**Last Updated**: 2026-06-19
**Status**: Active
