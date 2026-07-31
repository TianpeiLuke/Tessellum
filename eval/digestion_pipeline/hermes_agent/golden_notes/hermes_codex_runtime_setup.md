---
tags:
  - resource
  - documentation
  - hermes_agent
  - codex_runtime
  - operations
keywords:
  - codex app-server runtime
  - codex-runtime enabling
  - ~/.codex/config.toml managed block
  - codex permission profiles
  - mcp server migration
  - chatgpt subscription token cost
topics:
  - Hermes Agent
  - Codex App-Server Runtime
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime
access_control_group: ["general"]
---

# Codex App-Server Runtime — Enabling & Operating

## Overview

This is the operator's procedure for turning Hermes' **opt-in Codex app-server runtime** on, running it day-to-day, and turning it off again. The runtime hands `openai/*` and `openai-codex/*` turns to the [Codex CLI app-server](https://github.com/openai/codex) so terminal commands, file edits, sandboxing, and MCP tool calls execute inside Codex's own tool loop while Hermes stays the shell around it (sessions DB, slash commands, gateway, memory and skill review). The companion model note (`hermes_codex_runtime_tools`) catalogs *what tools the runtime has*; this note covers *how you switch onto it and operate it*: the `codex` CLI + `codex login` prerequisites, the one-line `/codex-runtime codex_app_server` enable command and what it migrates, the managed `# managed by hermes-agent` block it writes into `~/.codex/config.toml` (MCP servers + native plugins), Codex's three sandbox permission profiles, the Dangerous-Command approval prompt, the self-improvement loop that keeps firing (with the `codex_responses` review-fork downgrade), the ChatGPT-subscription token cost of auxiliary tasks, per-profile `CODEX_HOME` isolation, `HOME` passthrough, disabling, and the opt-in-beta limitations. It is **opt-in only** — default Hermes behavior is unchanged unless you flip the flag, and Hermes never auto-routes you onto this runtime.

## Prerequisites

1. **Codex CLI installed**, then **Codex OAuth login** (the codex subprocess reads `~/.codex/auth.json`):
   ```bash
   npm i -g @openai/codex
   codex --version              # 0.130.0 or newer
   codex login                  # writes OAuth tokens to ~/.codex/auth.json
   ```
   Hermes' own `hermes auth login codex` writes to `~/.hermes/auth.json` — that is a separate session. **Run `codex login` separately** if you have not. For the cleanest UX you want both.
3. **(Optional) Install the Codex plugins you want.** When you enable the runtime, Hermes auto-migrates whichever curated plugins you already installed via Codex CLI (`codex plugin marketplace add openai-curated`, then install Linear / GitHub / Gmail / etc. via Codex's TUI). Hermes discovers them and writes `[plugins."<name>@openai-curated"]` entries to `~/.codex/config.toml` automatically.

## Enabling

In a Hermes session, run:

```
/codex-runtime codex_app_server
```

That command:
- Verifies the `codex` CLI is installed (blocks with an install hint if not).
- Persists `model.openai_runtime: codex_app_server` to your `config.yaml`.
- Migrates user MCP servers from `~/.hermes/config.yaml` to `~/.codex/config.toml`.
- **Discovers and migrates installed native Codex plugins** by querying Codex's `plugin/list` RPC.
- **Registers Hermes' own tools as an MCP server** so the codex subprocess can call back for tools codex does not ship with.
- **Writes `default_permissions = ":workspace"`** so the sandbox allows workspace writes without prompting for every operation.
- Tells you what was migrated. Takes effect on the **next** session — the current cached agent keeps the prior runtime so prompt caches stay valid.

Synonyms: `/codex-runtime on`, `/codex-runtime off`, `/codex-runtime auto`. To check current state without changing anything, run bare `/codex-runtime`. You can also set it manually in `~/.hermes/config.yaml` under `model:` with `openai_runtime: codex_app_server` (the default is `"auto"`, which is the Hermes runtime).

## How Approvals Work

Codex requests approval before executing commands or applying patches. These are translated into Hermes' standard "Dangerous Command" prompt with three choices — **Allow once** (approve this single command), **Allow for this session** (Codex will not re-prompt for similar commands), and **Deny** (command is rejected; Codex continues in read-only mode). For `apply_patch` (file edit) approvals, Hermes shows a summary of what changed (`1 add, 1 update: /tmp/new.py, /tmp/old.py`) when codex provides the data via the corresponding `fileChange` item.

## Permission Profiles

Codex has three built-in permission profiles:
- `:read-only` — no writes; every shell command requires approval.
- `:workspace` — writes within the current workspace allowed without prompts (Hermes' default when you enable the runtime).
- `:danger-no-sandbox` — no sandbox at all (do not use this unless you understand it).

You can override the default **outside** Hermes' managed block in `~/.codex/config.toml` by setting `default_permissions = ":read-only"`. Hermes preserves your override on re-migration as long as it lives outside the `# managed by hermes-agent` markers.

## Self-Improvement Loop (Memory + Skill Nudges)

Hermes' background self-improvement fires on counter thresholds — every 10 user prompts a forked review agent decides whether anything should be saved to memory, and every 10 tool iterations within a turn the same idea applies for skills (`skill_manage` writes). **Both keep working on the codex runtime.** The codex path projects each completed `commandExecution` / `fileChange` / `mcpToolCall` / `dynamicToolCall` item into a synthetic `assistant tool_call` + `tool` result message, so by the time the review runs it sees the same shape it sees on the default runtime. The counter wiring stays equivalent: `_turns_since_memory` increments per user prompt before the early-return, `_iters_since_skill` increments by `turn.tool_iterations` after the codex turn returns, and `_spawn_background_review(...)` is called identically when either trigger fires.

One detail: the review fork itself needs Hermes' agent-loop tools (`memory`, `skill_manage`), which require Hermes' own dispatch. So when the parent agent is on `codex_app_server`, the review fork is **downgraded to `codex_responses`** — same OAuth credentials, same `openai-codex` provider, but it talks to OpenAI's Responses API directly so Hermes owns the loop and the agent-loop tools work. This is invisible to the user. Net effect: enable the codex runtime and your memory + skill nudges keep firing exactly as they would otherwise.

## Auxiliary Tasks and ChatGPT Subscription Token Cost

When this runtime is on with the `openai-codex` provider, **auxiliary tasks (title generation, context compression, vision auto-detect, the background self-improvement review fork) also flow through your ChatGPT subscription by default**, because Hermes' auxiliary client uses the main provider/model when no per-task override is set. This is not specific to `codex_app_server` (it is true for the `codex_responses` path too) but is more visible here because you are explicitly opting in for subscription billing.

To route specific aux tasks to a cheaper / different model, set explicit overrides in `~/.hermes/config.yaml`:

```yaml
auxiliary:
  title_generation:
    provider: openrouter
    model: google/gemini-3-flash-preview
  compression:
    provider: openrouter
    model: google/gemini-3-flash-preview
  vision:
    provider: openrouter
    model: google/gemini-3-flash-preview
  goal_judge:
    provider: openrouter
    model: google/gemini-3-flash-preview
```

The self-improvement review fork inherits the main runtime via `_current_main_runtime()` and Hermes downgrades it from `codex_app_server` to `codex_responses` automatically (so the fork can actually call `memory` and `skill_manage`). That fork still uses your subscription auth unless you have routed aux tasks elsewhere.

## Editing `~/.codex/config.toml` Safely

Hermes wraps everything it manages between two marker comments:

```toml
# managed by hermes-agent — `hermes codex-runtime migrate` regenerates this section
default_permissions = ":workspace"
[mcp_servers.filesystem]
...
[plugins."github@openai-curated"]
...
# end hermes-agent managed section
```

Anything **outside** that block is yours. Re-running migration (via `/codex-runtime codex_app_server` or whenever you toggle the runtime on) replaces the managed block in place but preserves user content above and below it verbatim. This means you can add your own MCP servers Hermes does not know about, override `default_permissions` to `:read-only`, configure codex-only options (model, providers, otel, etc.), and add user-defined permission profiles in `[permissions.<name>]` tables. Anything you add **inside** the managed block gets clobbered on the next migration; if you need a tweak that requires editing the managed block, file an issue and the maintainers will add the knob.

## MCP Server Migration

Hermes' `mcp_servers` config is auto-translated to the TOML format Codex expects. The migration runs every time you enable the runtime and is idempotent — re-runs replace the managed section but preserve user-edited Codex config. What translates:

| Hermes (`config.yaml`) | Codex (`config.toml`) |
|---|---|
| `command` + `args` + `env` | stdio transport |
| `url` + `headers` | streamable_http transport |
| `timeout` | `tool_timeout_sec` |
| `connect_timeout` | `startup_timeout_sec` |
| `enabled: false` | `enabled = false` |

Not migrated: Hermes-specific keys like `sampling` (Codex's MCP client has no equivalent — these are dropped with a per-server warning).

## Native Codex Plugin Migration

Plugins installed via `codex plugin` (Linear, GitHub, Gmail, Calendar, Canva, etc.) are discovered through Codex's `plugin/list` RPC. For each plugin where `installed: true`, Hermes writes a `[plugins."<name>@openai-curated"]` block enabling it in your Hermes session. So when a friend says "I have Calendar and GitHub set up in my Codex CLI" and they enable Hermes' codex runtime, Hermes activates those automatically — no re-configuration needed.

What is NOT migrated: plugins you have not installed yet (install them in Codex first); plugins where codex reports `availability != AVAILABLE` (broken install, expired OAuth, removed from marketplace — skipped to avoid writing config that would fail at activation time); ChatGPT app marketplace entries (`app/list`, already enabled inside codex via your account auth); and plugin OAuth (you authorize each plugin once in Codex itself — Hermes does not touch credentials).

## Multi-Profile / Multi-Tenant Setups and HOME Passthrough

By default, Hermes points the codex subprocess at `~/.codex/` regardless of which Hermes profile is active, so `hermes -p work` and `hermes -p personal` share the same Codex auth, plugins, and config. For per-profile Codex isolation, set `CODEX_HOME` explicitly per profile (cleanest pointed under your `HERMES_HOME`):

```bash
# Inside the work profile, you might wrap hermes:
CODEX_HOME=~/.hermes/profiles/work/codex hermes chat
```

You must re-run `codex login` once with that `CODEX_HOME` set so the OAuth tokens land in the profile-scoped location. Auto-scoping is deliberately avoided because moving an existing `~/.codex/` would silently invalidate Codex CLI auth.

Hermes does NOT rewrite `HOME` when spawning the codex app-server subprocess (it uses `os.environ.copy()` and only overlays `CODEX_HOME` and `RUST_LOG`). Commands codex runs via its `shell` tool see the real user `HOME` and find `~/.gitconfig`, `~/.gh/`, `~/.aws/`, `~/.npmrc`, etc., while Codex's internal state stays isolated through `CODEX_HOME` (defaulting to `~/.codex/`).

## Disabling

Switch back at any time:

```
/codex-runtime auto
```

Effective on the next session. The Codex managed block stays in `~/.codex/config.toml` so you can re-enable later without losing config — or remove it manually if you prefer.

## Limitations

This runtime is **opt-in beta** (working as of Hermes Agent 2026.5 + Codex CLI 0.130.0). Verified: multi-turn conversations, `commandExecution`/`fileChange` (apply_patch) approvals via Hermes UI, MCP tool calls, native Codex plugin migration, deny/cancel paths, toggle on/off cycle, memory and skill nudge counters, and Hermes `web_search` through codex. Known limitations:

- **Hermes auth and codex auth are separate sessions.** You need both `codex login` AND `hermes auth login codex` for the cleanest UX (a deliberate choice in `_import_codex_cli_tokens` to avoid clobbering token refresh).
- **`delegate_task`, `memory`, `session_search`, `todo` are unavailable on this runtime.** They need the running AIAgent context; use `/codex-runtime auto` when you need these.
- **No inline patch preview in approval prompts when codex does not track the changeset.** Hermes caches data from the `item/started` notification when possible, else falls back to whatever `reason` codex provides.
- **Sub-second cancellation is not guaranteed.** Mid-stream interrupts (Ctrl+C) are sent via `turn/interrupt`, but if codex already flushed the final message you get the response anyway.

If you find a bug, open an issue with `hermes logs --since 5m` output and mention `codex-runtime` in the title.

**Source**: `inbox/hermes_agent_docs/user-guide/features/codex-app-server-runtime.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime
**Last Updated**: 2026-06-19
**Status**: Active
