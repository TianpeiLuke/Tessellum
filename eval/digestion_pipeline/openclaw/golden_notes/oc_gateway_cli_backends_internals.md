---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - cli_backends
keywords:
  - openclaw cli backend internals
  - jsonl streaming loop
  - bundle mcp loopback bridge
  - claude-cli warm stdio session
  - fallback prelude claude transcript
  - ownsNativeCompaction
  - plugin-owned cli backend defaults
  - reseed history cap
topics:
  - OpenClaw
  - CLI Backends
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway/cli-backends
access_control_group: ["general"]
---

# OpenClaw — CLI Backend Internals (Execution Loop, Sessions, Compaction, Bundle MCP)

## Overview

This note explains how OpenClaw **CLI backends** work internally — the mechanics behind the user-facing setup documented in its sibling. It covers the five-step run loop (select → build prompt → execute → parse → persist), the `claude-cli` warm-stdio session model and stored-session-id reuse, the fallback prelude harvested from Claude Code's local JSONL transcript, plugin-owned backend defaults (`claude-cli` and `google-gemini-cli`), native-compaction ownership via `ownsNativeCompaction`, the loopback HTTP MCP bridge (`bundleMcp: true`), and the reseed history cap. It mirrors the `gateway/cli-backends` source page (internals sections only); the quick start, fallback config, image pass-through, I/O modes, limitations, and troubleshooting live in [oc_gateway_cli_backends](oc_gateway_cli_backends.md).

## How It Works (The Run Loop)

A CLI-backend run proceeds in five steps, all grounded in the source page:

1. **Selects a backend** based on the provider prefix (`claude-cli/...`).
2. **Builds a system prompt** using the same OpenClaw prompt + workspace context.
3. **Executes the CLI** with a session id (if supported) so history stays consistent. The bundled `claude-cli` backend keeps a Claude stdio process alive per OpenClaw session and sends follow-up turns over stream-json stdin.
4. **Parses output** (JSON or plain text) and returns the final text.
5. **Persists session ids** per backend, so follow-ups reuse the same CLI session.

The bundled Anthropic `claude-cli` backend is supported again: Anthropic staff told the OpenClaw team that OpenClaw-style Claude CLI usage is allowed again, so OpenClaw treats `claude -p` usage as sanctioned for this integration unless Anthropic publishes a new policy. The bundled `claude-cli` backend prefers Claude Code's native skill resolver for OpenClaw skills: when the current skills snapshot includes at least one selected skill with a materialized path, OpenClaw passes a temporary Claude Code plugin with `--plugin-dir` and omits the duplicate OpenClaw skills catalog from the appended system prompt; if the snapshot has no materialized plugin skill, OpenClaw keeps the prompt catalog as a fallback. Skill env/API key overrides are still applied by OpenClaw to the child process environment for the run.

Claude CLI also has its own noninteractive permission mode, which OpenClaw maps to the existing exec policy rather than adding Claude-specific policy config. For OpenClaw-managed Claude live sessions the effective OpenClaw exec policy is authoritative: YOLO (`tools.exec.security: "full"` and `tools.exec.ask: "off"`) launches Claude with `--permission-mode bypassPermissions`, while a restrictive effective exec policy launches Claude with `--permission-mode default`. Per-agent `agents.list[].tools.exec` settings override global `tools.exec` for that agent. Raw Claude backend args may still include `--permission-mode`, but live Claude launches normalize that flag to match the effective OpenClaw exec policy. The bundled backend also maps OpenClaw `/think` levels to Claude Code's native `--effort` flag for non-off levels: `minimal` and `low` map to `low`, `adaptive` and `medium` map to `medium`, and `high`, `xhigh`, and `max` map directly; other CLI backends need their owning plugin to declare an equivalent argv mapper before `/think` can affect the spawned CLI. Before OpenClaw can use the bundled `claude-cli` backend, Claude Code itself must already be logged in on the same host (`claude auth login`); use `agents.defaults.cliBackends.claude-cli.command` only when the `claude` binary is not already on `PATH`.

## Sessions (Reuse, Resume, and Continuity)

Session continuity is configured per backend. If the CLI supports sessions, set `sessionArg` (e.g. `--session-id`) or `sessionArgs` (placeholder `{sessionId}`) when the ID needs to be inserted into multiple flags. If the CLI uses a **resume subcommand** with different flags, set `resumeArgs` (replaces `args` when resuming) and optionally `resumeOutput` (for non-JSON resumes). The `sessionMode` field controls when an id is sent: `always` always sends a session id (a new UUID if none stored), `existing` only sends one if a session id was stored before, and `none` never sends a session id.

The bundled `claude-cli` defaults to `liveSession: "claude-stdio"`, `output: "jsonl"`, and `input: "stdin"` so follow-up turns reuse the live Claude process while it is active — warm stdio is the default now, including for custom configs that omit transport fields. If the Gateway restarts or the idle process exits, OpenClaw resumes from the stored Claude session id. Stored session ids are verified against an existing readable project transcript before resume, so phantom bindings are cleared with `reason=transcript-missing` instead of silently starting a fresh Claude CLI session under `--resume`. Claude live sessions keep bounded JSONL output guards: defaults allow up to 8 MiB and 20,000 raw JSONL lines per turn, and tool-heavy turns can raise them per backend with `agents.defaults.cliBackends.claude-cli.reliability.outputLimits.maxTurnRawChars` and `maxTurnLines`, which OpenClaw clamps to 64 MiB and 100,000 lines.

Stored CLI sessions are provider-owned continuity: the implicit daily session reset does not cut them, but `/reset` and explicit `session.reset` policies still do. Fresh CLI sessions normally reseed only from OpenClaw's compaction summary plus post-compaction tail; to recover short sessions that are invalidated before compaction, a backend can opt in with `reseedFromRawTranscriptWhenUncompacted: true`, after which OpenClaw still keeps raw transcript reseed bounded and limits it to safe invalidations such as missing CLI transcripts, system-prompt/MCP changes, or session-expired retry — auth profile or credential-epoch changes never reseed raw transcript history. On serialization: `serialize: true` keeps same-lane runs ordered, and most CLIs serialize on one provider lane. OpenClaw drops stored CLI session reuse when the selected auth identity changes (a changed auth profile id, static API key, static token, or OAuth account identity when the CLI exposes one); OAuth access and refresh token rotation does not cut the stored CLI session, and if a CLI does not expose a stable OAuth account id, OpenClaw lets that CLI enforce resume permissions.

## Fallback Prelude from claude-cli Sessions

When a `claude-cli` attempt fails over to a non-CLI candidate in `agents.defaults.model.fallbacks`, OpenClaw seeds the next attempt with a context prelude harvested from Claude Code's local JSONL transcript at `~/.claude/projects/`. Without this seed, the fallback provider would start cold because OpenClaw's own session transcript is empty for `claude-cli` runs. The prelude prefers the latest `/compact` summary or `compact_boundary` marker, then appends the most recent post-boundary turns up to a char budget; pre-boundary turns are dropped because the summary already represents them. Tool blocks are coalesced to compact `(tool call: name)` and `(tool result: …)` hints to keep the prompt budget honest, and the summary is labeled `(truncated)` if it overflows. Same-provider `claude-cli` to `claude-cli` fallbacks rely on Claude's own `--resume` and skip the prelude, and the seed reuses the existing Claude session-file path validation so arbitrary paths cannot be read.

## Defaults (Plugin-Owned)

Bundled CLI backend defaults live with their owning plugin: Anthropic owns `claude-cli` and Google owns `google-gemini-cli`. OpenAI Codex agent runs use the Codex app-server harness through `openai/*`; OpenClaw no longer registers a bundled `codex-cli` backend.

The bundled Anthropic plugin registers a default for `claude-cli`:

- `command: "claude"`
- `args: ["-p","--output-format","stream-json","--include-partial-messages","--verbose", ...]`
- `output: "jsonl"`
- `input: "stdin"`
- `modelArg: "--model"`
- `sessionMode: "always"`

The bundled Google plugin registers a default for `google-gemini-cli`:

- `command: "gemini"`
- `args: ["--skip-trust", "--approval-mode", "auto_edit", "--output-format", "stream-json", "--prompt", "{prompt}"]`
- `resumeArgs: ["--skip-trust", "--approval-mode", "auto_edit", "--resume", "{sessionId}", "--output-format", "stream-json", "--prompt", "{prompt}"]`
- `output: "jsonl"`, `resumeOutput: "jsonl"`, `jsonlDialect: "gemini-stream-json"`
- `imageArg: "@"`, `imagePathScope: "workspace"`
- `modelArg: "--model"`, `sessionMode: "existing"`, `sessionIdFields: ["session_id", "sessionId"]`

The local Gemini CLI must be installed and available as `gemini` on `PATH` (`brew install gemini-cli` or `npm install -g @google/gemini-cli`). The default `stream-json` parser reads assistant `message` events, tool events, final `result` usage, and fatal Gemini error events. If you override Gemini args to `--output-format json`, OpenClaw normalizes that backend back to `output: "json"` and reads reply text from the JSON `response` field; usage falls back to `stats` when `usage` is absent or empty, `stats.cached` is normalized into OpenClaw `cacheRead`, and if `stats.input` is missing OpenClaw derives input tokens from `stats.input_tokens - stats.cached`. Override defaults only if needed (commonly an absolute `command` path).

## Plugin-Owned Defaults and Text Transforms

CLI backend defaults are part of the plugin surface: plugins register them with `api.registerCliBackend(...)`, the backend `id` becomes the provider prefix in model refs, user config in `agents.defaults.cliBackends.<id>` still overrides the plugin default, and backend-specific config cleanup stays plugin-owned through the optional `normalizeConfig` hook. Plugins that need tiny prompt/message compatibility shims can declare bidirectional text transforms without replacing a provider or CLI backend:

```typescript
api.registerTextTransforms({
  input: [
    { from: /red basket/g, to: "blue basket" },
    { from: /paper ticket/g, to: "digital ticket" },
    { from: /left shelf/g, to: "right shelf" },
  ],
  output: [
    { from: /blue basket/g, to: "red basket" },
    { from: /digital ticket/g, to: "paper ticket" },
    { from: /right shelf/g, to: "left shelf" },
  ],
});
```

`input` rewrites the system prompt and user prompt passed to the CLI; `output` rewrites streamed assistant deltas and parsed final text before OpenClaw handles its own control markers and channel delivery. For CLIs that emit provider-specific JSONL events, set `jsonlDialect` on that backend's config — supported dialects are `claude-stream-json` for Claude Code-compatible streams and `gemini-stream-json` for Gemini CLI `stream-json` events.

## Native Compaction Ownership

Some CLI backends run an agent that compacts its **own** transcript, so OpenClaw must not run its safeguard summarizer against them — doing so fights the backend's own compaction and can hard-fail the turn. `claude-cli` has no harness endpoint (Claude Code compacts internally), so it declares `ownsNativeCompaction: true`, and OpenClaw returns a no-op from the compaction path. Native-harness sessions such as Codex keep routing to their harness compaction endpoint instead. Because the backend owns compaction, the old stopgap of setting `contextTokens: 1_000_000` purely to keep OpenClaw's safeguard from firing on a `claude-cli` session is **no longer needed** — the opt-out replaces it.

```typescript
api.registerCliBackend({ id: "my-cli", ownsNativeCompaction: true /* ... */ });
```

Only declare `ownsNativeCompaction` for a backend that genuinely owns its compaction: it must reliably bound its own transcript as it nears its context window and persist a resumable session (e.g. `--resume` / `--session-id`); otherwise a deferred session can stay over budget. Matching `agentHarnessId` sessions still route to the harness endpoint.

## Bundle MCP Overlays (Loopback Bridge)

CLI backends do **not** receive OpenClaw tool calls directly, but a backend can opt into a generated MCP config overlay with `bundleMcp: true`. The current bundled behavior generates a strict MCP config file for `claude-cli` and a Gemini system settings file for `google-gemini-cli`. When bundle MCP is enabled, OpenClaw:

- spawns a loopback HTTP MCP server that exposes gateway tools to the CLI process
- authenticates the bridge with a per-session token (`OPENCLAW_MCP_TOKEN`)
- scopes tool access to the current session, account, and channel context
- loads enabled bundle-MCP servers for the current workspace
- merges them with any existing backend MCP config/settings shape
- rewrites the launch config using the backend-owned integration mode from the owning extension

If no MCP servers are enabled, OpenClaw still injects a strict config when a backend opts into bundle MCP so background runs stay isolated. Session-scoped bundled MCP runtimes are cached for reuse within a session, then reaped after `mcp.sessionIdleTtlMs` milliseconds of idle time (default 10 minutes; set `0` to disable). One-shot embedded runs such as auth probes, slug generation, and active-memory recall request cleanup at run end so stdio children and Streamable HTTP/SSE streams do not outlive the run.

## Reseed History Cap

When a fresh CLI session is seeded from a prior OpenClaw transcript (for example after a `session_expired` retry), the rendered `<conversation_history>` block is capped to keep reseed prompts from exploding. The default is `12288` characters (about 3000 tokens). Claude CLI backends automatically use a larger cap derived from the resolved Claude context tier: standard 200K-token Claude runs keep a larger transcript slice, and 1M-token Claude runs keep a larger slice again, while other CLI backends keep the conservative default. The cap only governs the reseed prompt's prior-history block — live-session output limits are tuned separately under `reliability.outputLimits` (see Sessions above).

**Source**: OpenClaw documentation — `gateway/cli-backends` (mirror `inbox/openclaw_docs/gateway/cli-backends.md`), internals sections
**Last Updated**: 2026-06-22
**Status**: Active
