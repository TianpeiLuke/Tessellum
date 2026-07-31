---
tags:
  - resource
  - documentation
  - openclaw
  - top_level
  - automation
keywords:
  - openprose openclaw
  - prose workflow format
  - prose slash command
  - open-prose plugin
  - multi-agent prose programs
  - sessions_spawn web_fetch prose
  - prose state backends
  - prose file locations
topics:
  - OpenClaw
  - OpenProse
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/prose
access_control_group: ["general"]
---

# OpenClaw — OpenProse Markdown Workflow Format

## Overview

This note is the procedure for running and writing **OpenProse** programs inside OpenClaw, mirroring the `prose` top-level docs page. OpenProse is a portable, markdown-first workflow format for orchestrating multi-agent AI sessions; in OpenClaw it ships as a plugin that installs an OpenProse skill pack and a `/prose` slash command. Programs live in `.prose` files and can spawn multiple sub-agents with explicit control flow. The note covers enabling the `open-prose` plugin, the `/prose` slash command surface, what OpenProse can do, a parallel-research example, how OpenProse concepts map to OpenClaw primitives, the `.prose/` file layout, the four state backends, and the security posture for treating `.prose` files as code.

## Install

Bundled plugins are disabled by default, so OpenProse must be enabled before use. The install procedure is three steps:

1. **Enable the plugin** — run `openclaw plugins enable open-prose`.
2. **Restart the Gateway** — run `openclaw gateway restart`.
3. **Verify** — run `openclaw plugins list | grep prose`; you should see `open-prose` as enabled, after which the `/prose` skill command is available in chat.

```bash
openclaw plugins enable open-prose
openclaw gateway restart
openclaw plugins list | grep prose
```

For a local checkout, install from a path instead: `openclaw plugins install ./path/to/local/open-prose-plugin`.

## Slash command

OpenProse registers `/prose` as a user-invocable skill command. The available subcommands are:

```text
/prose help
/prose run <file.prose>
/prose run <handle/slug>
/prose run <https://example.com/file.prose>
/prose compile <file.prose>
/prose examples
/prose update
```

`/prose run <handle/slug>` resolves to `https://p.prose.md/<handle>/<slug>`. Direct URLs are fetched as-is using the `web_fetch` tool.

## What it can do

OpenProse supports three documented use patterns:

- Multi-agent research and synthesis with explicit parallelism.
- Repeatable, approval-safe workflows (code review, incident triage, content pipelines).
- Reusable `.prose` programs you can run across supported agent runtimes.

## Example: parallel research and synthesis

A `.prose` program declares typed `input`, named `agent` blocks (each with a `model` and `prompt`), and control-flow blocks such as `parallel:` that fan out `session:` steps; results bind to names that a later `session` merges via `context`. The source example runs a `researcher` and a `writer` agent in parallel, then merges their `findings` and `draft`:

```prose
# Research + synthesis with two agents running in parallel.

input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

## OpenClaw runtime mapping

OpenProse programs map to OpenClaw primitives so that the markdown control flow drives the agent runtime's tools. The documented mapping is:

| OpenProse concept | OpenClaw tool |
| --- | --- |
| Spawn session / Task tool | `sessions_spawn` |
| File read / write | `read` / `write` |
| Web fetch | `web_fetch` |

If your tool allowlist blocks `sessions_spawn`, `read`, `write`, or `web_fetch`, OpenProse programs will fail; check your tools allowlist config (`/gateway/config-tools`).

## File locations

OpenProse keeps state under `.prose/` in your workspace. Each run lands in a timestamped, random-suffixed directory holding the program, its state, bindings, and per-run agents; workspace-level reusable agents live under `.prose/agents/`:

```text
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

User-level persistent agents live at `~/.prose/agents/`.

## State backends

OpenProse supports four state backends:

- **filesystem (default)** — state is written to `.prose/runs/...` in the workspace; no extra dependencies required.
- **in-context** — transient state kept in the context window; suitable for small, short-lived programs.
- **sqlite (experimental)** — requires the `sqlite3` binary on `PATH`.
- **postgres (experimental)** — requires `psql` and a connection string. Postgres credentials flow into sub-agent logs, so use a dedicated, least-privileged database.

## Security

Treat `.prose` files like code: review them before running. Use OpenClaw tool allowlists and approval gates to control side effects. For deterministic, approval-gated workflows, the source page suggests comparing with Lobster (`/tools/lobster`). The official OpenProse site is `https://www.prose.md`.

**Source**: OpenClaw documentation — `prose` (mirror `inbox/openclaw_docs/prose.md`)
**Last Updated**: 2026-06-22
**Status**: Active
