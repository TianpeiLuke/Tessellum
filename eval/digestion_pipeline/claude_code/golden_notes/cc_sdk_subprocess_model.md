---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - hosting
keywords:
  - subprocess model
  - claude cli subprocess
  - stdio transport
  - jsonl session transcript
  - cwd per query
  - local disk state
  - session persistence
  - claude_config_dir
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/hosting
access_control_group: ["general"]
---

# Agent SDK — The Subprocess Model

## Overview

The Agent SDK does not run the agent in-process: when your code calls `query()`, the SDK spawns a separate `claude` CLI process and talks to it over **stdio**. That subprocess owns the shell, the working directory, and the JSONL session transcripts on local disk. Every hosting decision follows from this — hosting the SDK is not like hosting a stateless API wrapper, because every running agent is a long-lived process tied to local state.

One agent session maps to one subprocess. Three kinds of agent state live on the container filesystem by default, and none of them survive a container restart, a scale-down, or a move to a different node — so durable resumption requires an explicit persistence strategy. This note covers the process-to-session mapping and the local-disk state footprint; the lifecycle patterns built on top of it are in [The Session Patterns](cc_sdk_session_patterns.md).

## One session = one subprocess

When your code calls `query()`, the SDK spawns a separate `claude` CLI process and talks to it over stdio. That subprocess owns the shell, the working directory, and the JSONL session transcripts on local disk.

One agent session maps to one subprocess. Running N concurrent sessions means N subprocesses, each with its own process tree and transcript file. By default they all inherit your application's working directory, so pass `cwd` on each `query()` call when sessions need separate filesystems:

```typescript theme={null}
query({ prompt, options: { cwd: "/work/session-a" } })
```

(The Python equivalent is `query(prompt=prompt, options=ClaudeAgentOptions(cwd="/work/session-a"))`.)

The subprocess itself does not listen on the network: your application handles inbound client requests on a port it exposes and calls the SDK internally, while the subprocess reaches out over HTTPS to `api.anthropic.com` (or a provider endpoint).

## State that lives on local disk

Three kinds of agent state live on the container's filesystem by default. None of them survive a container restart, a scale-down, or a move to a different node:

| State | Default location |
| --- | --- |
| Session transcripts | `~/.claude/projects/`, or the `projects/` directory under `CLAUDE_CONFIG_DIR` if set |
| `CLAUDE.md` memory files | `~/.claude/CLAUDE.md` for the user tier and the session's working directory for the project tier |
| Working-directory artifacts | The session's working directory |

To persist transcripts across hosts, configure a `SessionStore` adapter (see [Session storage](https://code.claude.com/docs/en/agent-sdk/session-storage)). Memory files and other working-directory artifacts are **not** mirrored by `SessionStore` and need their own storage strategy, such as a mounted volume or an object-store sync.

For how sessions, resumption, and forking work at the API level, see [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions).

**Source**: https://code.claude.com/docs/en/agent-sdk/hosting
**Last Updated**: 2026-06-13
**Status**: Active
