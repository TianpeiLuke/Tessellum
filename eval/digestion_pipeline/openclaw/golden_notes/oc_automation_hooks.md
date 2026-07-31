---
tags:
  - resource
  - documentation
  - openclaw
  - automation
  - hooks
keywords:
  - openclaw internal hooks
  - hook.md handler.ts
  - openclaw hooks cli
  - gateway lifecycle event hooks
  - bundled hooks session-memory
  - hook discovery precedence
  - hooks.internal.entries config
  - command lifecycle automation
topics:
  - OpenClaw
  - Automation Hooks
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/automation/hooks
access_control_group: ["general"]
---

# OpenClaw — Internal Hooks (Command and Lifecycle Automation)

## Overview

This note is the procedure for OpenClaw **internal hooks**: small scripts that run inside the Gateway when something happens, discoverable from directories and inspected with `openclaw hooks`. It mirrors the `automation/hooks` source page end to end — choosing hooks vs other extension surfaces, the Quick start, the event types, authoring a hook (`HOOK.md` + `handler.ts` + event context), hook discovery and hook packs, the bundled hooks (`session-memory`, `bootstrap-extra-files`, `command-logger`, `compaction-notifier`, `boot-md`), how plugin-managed internal hooks relate, configuration, the `openclaw hooks` CLI, best practices, and troubleshooting. OpenClaw has two kinds of hooks: **internal hooks** (this page) that run inside the Gateway when agent events fire (like `/new`, `/reset`, `/stop`, or lifecycle events), and **Webhooks** (external HTTP endpoints that let other systems trigger work — documented separately under cron-jobs). The Gateway loads internal hooks only after you enable hooks or configure at least one hook entry, hook pack, legacy handler, or extra hook directory; hooks can also be bundled inside plugins, and `openclaw hooks list` shows both standalone hooks and plugin-managed hooks.

## Choose the right surface

OpenClaw has several extension surfaces that look similar but solve different problems. Use **internal hooks** (`HOOK.md`, this page) when you want to save a snapshot on `/new`, log `/reset`, call an external API after `message:sent`, or add coarse operator automation — file-based hooks are meant for operator-managed side effects and command/lifecycle automation, behaving like a small installed integration. Use **typed plugin hooks** via `api.on(...)` when you want to rewrite prompts, block tools, cancel outbound messages, or add ordered middleware/policy — typed hooks have explicit contracts, priorities, merge rules, and block/cancel semantics, and are the choice when you need runtime lifecycle control. Use **diagnostic events** when you want telemetry-only export or observability, because observability is a separate event bus, not a policy hook surface.

## Quick start

```bash
# List available hooks
openclaw hooks list

# Enable a hook
openclaw hooks enable session-memory

# Check hook status
openclaw hooks check

# Get detailed information
openclaw hooks info session-memory
```

## Event types

Internal hooks listen for these Gateway events:

| Event | When it fires |
|---|---|
| `command:new` | `/new` command issued |
| `command:reset` | `/reset` command issued |
| `command:stop` | `/stop` command issued |
| `command` | Any command event (general listener) |
| `session:compact:before` | Before compaction summarizes history |
| `session:compact:after` | After compaction completes |
| `session:patch` | When session properties are modified |
| `agent:bootstrap` | Before workspace bootstrap files are injected |
| `gateway:startup` | After channels start and hooks are loaded |
| `gateway:shutdown` | When gateway shutdown begins |
| `gateway:pre-restart` | Before an expected gateway restart |
| `message:received` | Inbound message from any channel |
| `message:transcribed` | After audio transcription completes |
| `message:preprocessed` | After media and link preprocessing completes or is skipped |
| `message:sent` | Outbound message delivered |

## Writing hooks

### Hook structure

Each hook is a directory containing two files — `HOOK.md` (metadata + documentation) and `handler.ts` (handler implementation), e.g. `my-hook/HOOK.md` and `my-hook/handler.ts`.

### HOOK.md format

```markdown
---
name: my-hook
description: "Short description of what this hook does"
metadata:
  { "openclaw": { "emoji": "🔗", "events": ["command:new"], "requires": { "bins": ["node"] } } }
---

# My Hook

Detailed documentation goes here.
```

The `metadata.openclaw` fields are: `emoji` (display emoji for CLI); `events` (array of events to listen for); `export` (named export to use, defaults to `"default"`); `os` (required platforms, e.g. `["darwin", "linux"]`); `requires` (required `bins`, `anyBins`, `env`, or `config` paths); `always` (bypass eligibility checks, boolean); and `install` (installation methods).

### Handler implementation

```typescript
const handler = async (event) => {
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log(`[my-hook] New command triggered`);
  // Your logic here

  // Optionally send a reply on replyable surfaces
  event.messages.push("Hook executed!");
};

export default handler;
```

Each event includes: `type`, `action`, `sessionKey`, `timestamp`, `messages` (push replies here on replyable surfaces only), and `context` (event-specific data). Agent and tool plugin hook contexts can also include `trace`, a read-only W3C-compatible diagnostic trace context that plugins may pass into structured logs for OTEL correlation. `event.messages` is only delivered automatically on replyable surfaces such as `command:*` and `message:received`; lifecycle-only events such as `agent:bootstrap`, `session:*`, `gateway:*`, or `message:sent` do not have a reply channel and ignore pushed messages.

### Event context highlights

**Command events** (`command:new`, `command:reset`) carry `context.sessionEntry`, `context.previousSessionEntry`, `context.commandSource`, `context.workspaceDir`, and `context.cfg`. **Message events** (`message:received`) carry `context.from`, `context.content`, `context.channelId`, and `context.metadata` (provider-specific data including `senderId`, `senderName`, `guildId`); `context.content` prefers a nonblank command body for command-like messages, then falls back to the raw inbound body and generic body, and does not include agent-only enrichment such as thread history or link summaries. **Message events** (`message:sent`) carry `context.to`, `context.content`, `context.success`, `context.channelId`; (`message:transcribed`) carry `context.transcript`, `context.from`, `context.channelId`, `context.mediaPath`; (`message:preprocessed`) carry `context.bodyForAgent` (final enriched body), `context.from`, `context.channelId`. **Bootstrap events** (`agent:bootstrap`) carry `context.bootstrapFiles` (mutable array) and `context.agentId`. **Session patch events** (`session:patch`) carry `context.sessionEntry`, `context.patch` (only changed fields), and `context.cfg` — only privileged clients can trigger patch events. **Compaction events**: `session:compact:before` includes `messageCount`, `tokenCount`; `session:compact:after` adds `compactedCount`, `summaryLength`, `tokensBefore`, `tokensAfter`. The `command:stop` event observes the user issuing `/stop` — it is cancellation/command lifecycle, not an agent-finalization gate; plugins that need to inspect a natural final answer and ask the agent for one more pass should use the typed plugin hook `before_agent_finalize` instead.

**Gateway lifecycle events**: `gateway:shutdown` includes `reason` and `restartExpectedMs` and fires when gateway shutdown begins; `gateway:pre-restart` includes the same context but only fires when shutdown is part of an expected restart and a finite `restartExpectedMs` value is supplied. During shutdown, each lifecycle hook wait is best-effort and bounded so shutdown continues if a handler stalls — the default wait budget is 5 seconds for `gateway:shutdown` and 10 seconds for `gateway:pre-restart`. Between the `gateway:shutdown` (or `gateway:pre-restart`) event and the rest of the shutdown sequence, the gateway also fires a typed `session_end` plugin hook for every session that was still active when the process stopped; the event's `reason` is `shutdown` for a plain SIGTERM/SIGINT stop and `restart` when the close was scheduled as part of an expected restart. This drain is bounded so a slow `session_end` handler cannot block process exit, and sessions already finalized through replace / reset / delete / compaction are skipped to avoid double-firing.

## Hook discovery

Hooks are discovered from these directories, in order of increasing override precedence: (1) **Bundled hooks** shipped with OpenClaw; (2) **Plugin hooks** bundled inside installed plugins; (3) **Managed hooks** at `~/.openclaw/hooks/` (user-installed, shared across workspaces — extra directories from `hooks.internal.load.extraDirs` share this precedence); (4) **Workspace hooks** at `<workspace>/hooks/` (per-agent, disabled by default until explicitly enabled). Workspace hooks can add new hook names but cannot override bundled, managed, or plugin-provided hooks with the same name. The Gateway skips internal hook discovery on startup until internal hooks are configured: enable a bundled or managed hook with `openclaw hooks enable <name>`, install a hook pack, or set `hooks.internal.enabled=true` to opt in. When you enable one named hook, the Gateway loads only that hook's handler; `hooks.internal.enabled=true`, extra hook directories, and legacy handlers opt into broad discovery.

### Hook packs

Hook packs are npm packages that export hooks via `openclaw.hooks` in `package.json`, installed with `openclaw plugins install <path-or-spec>`. Npm specs are registry-only (package name + optional exact version or dist-tag); Git/URL/file specs and semver ranges are rejected.

## Bundled hooks

OpenClaw ships these bundled hooks (enable any with `openclaw hooks enable <hook-name>`):

| Hook | Events | What it does |
|---|---|---|
| session-memory | `command:new`, `command:reset` | Saves session context to `<workspace>/memory/` |
| bootstrap-extra-files | `agent:bootstrap` | Injects additional bootstrap files from glob patterns |
| command-logger | `command` | Logs all commands to `~/.openclaw/logs/commands.log` |
| compaction-notifier | `session:compact:before`, `session:compact:after` | Sends visible chat notices when session compaction starts/ends |
| boot-md | `gateway:startup` | Runs `BOOT.md` when the gateway starts |

**session-memory** extracts the last 15 user/assistant messages and saves to `<workspace>/memory/YYYY-MM-DD-HHMM.md` using the host local date; memory capture runs in the background so `/new` and `/reset` acknowledgements are not delayed by transcript reads or optional slug generation. Set `hooks.internal.entries.session-memory.llmSlug: true` to generate descriptive filename slugs with the configured model; it requires `workspace.dir` to be configured. **bootstrap-extra-files** resolves paths relative to workspace and loads only recognized bootstrap basenames (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, `MEMORY.md`):

```json
{
  "hooks": {
    "internal": {
      "entries": {
        "bootstrap-extra-files": {
          "enabled": true,
          "paths": ["packages/*/AGENTS.md", "packages/*/TOOLS.md"]
        }
      }
    }
  }
}
```

**command-logger** logs every slash command to `~/.openclaw/logs/commands.log`. **compaction-notifier** sends short status messages into the current conversation when OpenClaw starts and finishes compacting the session transcript, making long turns less confusing on chat surfaces because the user can see that the assistant is summarizing context and will continue after compaction. **boot-md** runs `BOOT.md` from the active workspace when the gateway starts.

## Plugin hooks

Plugins can register typed hooks through the Plugin SDK for deeper integration — intercepting tool calls, modifying prompts, controlling message flow, and more; use plugin hooks when you need `before_tool_call`, `before_agent_reply`, `before_install`, or other in-process lifecycle hooks. Plugin-managed internal hooks are different: they participate in this page's coarse command/lifecycle event system and show up in `openclaw hooks list` as `plugin:<id>`; use those for side effects and compatibility with hook packs, not for ordered middleware or policy gates. For the complete plugin hook reference, see the Plugin hooks page.

## Configuration

Internal hooks are configured under `hooks.internal`, with `enabled` opting into broad discovery and `entries.<name>.enabled` toggling individual hooks:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": false }
      }
    }
  }
}
```

Per-hook environment variables go under `entries.<name>.env` (e.g. `"my-hook": { "enabled": true, "env": { "MY_CUSTOM_VAR": "value" } }`), and extra hook directories under `hooks.internal.load.extraDirs` (e.g. `"load": { "extraDirs": ["/path/to/more/hooks"] }`). The legacy `hooks.internal.handlers` array config format is still supported for backwards compatibility, but new hooks should use the discovery-based system.

## CLI reference

```bash
# List all hooks (add --eligible, --verbose, or --json)
openclaw hooks list

# Show detailed info about a hook
openclaw hooks info <hook-name>

# Show eligibility summary
openclaw hooks check

# Enable/disable
openclaw hooks enable <hook-name>
openclaw hooks disable <hook-name>
```

## Best practices

- **Keep handlers fast.** Hooks run during command processing. Fire-and-forget heavy work with `void processInBackground(event)`.
- **Handle errors gracefully.** Wrap risky operations in try/catch; do not throw so other handlers can run.
- **Filter events early.** Return immediately if the event type/action is not relevant.
- **Use specific event keys.** Prefer `"events": ["command:new"]` over `"events": ["command"]` to reduce overhead.

## Troubleshooting

**Hook not discovered** — verify the directory structure (`ls -la ~/.openclaw/hooks/my-hook/` should show `HOOK.md`, `handler.ts`) and list all discovered hooks with `openclaw hooks list`. **Hook not eligible** — run `openclaw hooks info my-hook` and check for missing binaries (PATH), environment variables, config values, or OS compatibility. **Hook not executing** — verify the hook is enabled (`openclaw hooks list`), restart your gateway process so hooks reload, and check gateway logs (`./scripts/clawlog.sh | grep hook`).

**Source**: OpenClaw documentation — `automation/hooks` (mirror `inbox/openclaw_docs/automation/hooks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
