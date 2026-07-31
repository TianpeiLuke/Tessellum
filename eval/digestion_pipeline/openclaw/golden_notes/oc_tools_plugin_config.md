---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - plugins
keywords:
  - openclaw plugin policy
  - security.installPolicy
  - plugins.allow plugins.deny
  - plugins.slots plugins.entries
  - typed plugin hooks api.on
  - api.registerHook internal hooks
  - verify active gateway runtime
  - blocked plugin path ownership
  - slow plugin tool factory
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/plugin
access_control_group: ["general"]
---

# OpenClaw — Configuring and Operating Plugins

## Overview

This note is the configure-and-operate half of the OpenClaw `tools/plugin` page (its install/quick-start/formats half is the sibling [oc_tools_plugin_install](oc_tools_plugin_install.md)). It covers the operator install policy (`security.installPolicy`), the `plugins.{enabled,allow,deny,load,slots,entries}` policy shape and its precedence rules, the two plugin-hook APIs (typed `api.on(...)` vs internal `api.registerHook(...)`), verifying that an already-running Gateway actually imported the plugin code, and the troubleshooting matrix — including the two deep-dive subsections on blocked plugin path ownership and slow plugin tool setup. Every config key, CLI command, and diagnostic string is reproduced verbatim from the `tools/plugin` mirror.

## Operator install policy (`security.installPolicy`)

Configure `security.installPolicy` to run a trusted local policy command before plugin install or update proceeds. The policy receives metadata plus the staged source path and can allow or block the install. It covers both CLI and Gateway-backed plugin install/update paths. Plugin `before_install` hooks run later, and only in OpenClaw processes where plugin hooks are loaded, so use `security.installPolicy` for operator-owned install decisions rather than `before_install`. The deprecated `--dangerously-force-unsafe-install` flag is accepted for compatibility but does NOT bypass install policy or OpenClaw's built-in plugin dependency denylist. The same `security.installPolicy` exec schema is shared between skills and plugins — see the Skills config page's "operator install policy" section for that shared schema.

## Configure plugin policy

The common plugin config shape (json5) is:

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-plugin"] },
    slots: { memory: "memory-core" },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } },
    },
  },
}
```

Plugin-specific settings live under `plugins.entries.<id>.config` (the per-plugin config object passed to that plugin).

### Key policy rules

The precedence and behavior rules for the policy keys are exact:

- `plugins.enabled: false` disables all plugins and skips plugin discovery/load work. Stale plugin references are inert while this is active; re-enable plugins before running doctor cleanup when you want stale ids removed.
- `plugins.deny` wins over `allow` and over per-plugin enablement (it is the strongest signal).
- `plugins.allow` is an exclusive allowlist. Plugin-owned tools outside the allowlist stay unavailable, even when `tools.allow` includes `"*"`.
- `plugins.entries.<id>.enabled: false` disables one plugin while preserving its config.
- `plugins.load.paths` adds explicit local plugin files or directories. Managed `plugins install` local paths must be plugin directories or archives; use `plugins.load.paths` for standalone plugin files.
- Workspace-origin plugins are disabled by default; explicitly enable or allowlist them before using local workspace code.
- Bundled plugins follow their built-in default-on/default-off metadata unless config explicitly overrides them.
- `plugins.slots.<slot>` chooses one plugin for exclusive categories such as memory and context engines. Slot selection force-enables the selected plugin for that slot by counting as explicit activation; it can load even when it would otherwise be opt-in. `plugins.deny` and `plugins.entries.<id>.enabled: false` still block it.
- Bundled opt-in plugins can auto-activate when config names one of their owned surfaces, such as a provider/model ref, channel config, CLI backend, or agent harness runtime.
- OpenAI-family Codex routing keeps provider and runtime plugin boundaries separate: legacy Codex model refs are legacy config repaired by doctor, while the bundled `codex` plugin owns Codex app-server runtime for canonical `openai/*` agent refs, explicit `agentRuntime.id: "codex"`, and legacy `codex/*` refs.

Run `openclaw doctor` or `openclaw doctor --fix` when config validation reports stale plugin ids, allowlist/tool mismatches, or legacy bundled plugin paths.

## Plugin hooks

Plugins can register hooks at runtime, but there are two different APIs with different jobs:

- Use **typed hooks** via `api.on(...)` for runtime lifecycle hooks. This is the preferred surface for middleware, policy, message rewriting, prompt shaping, and tool control.
- Use `api.registerHook(...)` **only** when you want to participate in the internal hook system described in the Hooks automation page. This is mainly for coarse command/lifecycle side effects and compatibility with existing HOOK-style automation.

The quick rule for choosing between them: if the handler needs priority, merge semantics, or block/cancel behavior, use typed plugin hooks (`api.on`); if the handler just reacts to `command:new`, `command:reset`, `message:sent`, or similar coarse events, `api.registerHook(...)` is fine. Plugin-managed internal hooks show up in `openclaw hooks list` with a `plugin:<id>` prefix. You CANNOT enable or disable them through `openclaw hooks`; enable or disable the plugin instead.

## Verify the active Gateway

`openclaw plugins list` and plain `openclaw plugins inspect` read cold config, manifest, and registry state — they do NOT prove that an already-running Gateway has imported the same plugin code. When a plugin appears installed but live chat traffic does not use it, run the deep verification path:

```bash
openclaw gateway status --deep --require-rpc
openclaw plugins inspect <plugin-id> --runtime --json
openclaw gateway restart
```

Managed Gateways restart automatically after plugin install, update, and uninstall changes that alter plugin source. On VPS or container installs, make sure any manual restart targets the actual `openclaw gateway run` child that serves your channels, not only a wrapper or supervisor.

## Troubleshooting

The problem→check→fix matrix for plugin operation:

| Symptom | Check | Fix |
| --- | --- | --- |
| Plugin appears in `plugins list` but runtime hooks do not run | `openclaw plugins inspect <id> --runtime --json` and confirm the active Gateway with `gateway status --deep --require-rpc` | Restart the live Gateway after install, update, config, or source changes |
| Duplicate channel or tool ownership diagnostics appear | `openclaw plugins list --enabled --verbose`, inspect each suspect with `--runtime --json`, compare channel/tool ownership | Disable one owner, remove stale installs, or use manifest `preferOver` for intentional replacement |
| Config says a plugin is missing | Check the Plugin inventory for whether it is bundled, official external, or source-only | Install the external package, enable the bundled plugin, or remove stale config |
| Config is invalid during install | Read the validation message; run `openclaw doctor --fix` when it points to stale plugin state | Doctor can quarantine invalid plugin config by disabling the entry and removing the invalid payload |
| Plugin path is blocked for suspicious ownership or permissions | Inspect the diagnostic before the config error | Fix filesystem ownership/permissions, then run `openclaw plugins registry --refresh` |
| `OPENCLAW_NIX_MODE=1` blocks lifecycle commands | Confirm the install is managed by Nix | Change plugin selection in the Nix source instead of using plugin mutator commands |
| Dependency import fails at runtime | Check whether the plugin was installed through npm/git/ClawHub or from a local path | `openclaw plugins update <id>`, reinstall the source, or install local plugin dependencies yourself |

When stale plugin config still names a no-longer-discoverable channel plugin, Gateway startup skips that plugin-backed channel instead of blocking every other channel; run `openclaw doctor --fix` to remove stale plugin and channel entries. Unknown channel keys without stale-plugin evidence still fail validation so typos stay visible. For intentional channel replacement, the preferred plugin should declare `channelConfigs.<channel-id>.preferOver` with the legacy or lower-priority plugin id; if both plugins are explicitly enabled, OpenClaw keeps that request and reports duplicate channel/tool diagnostics instead of silently choosing one owner. If an installed package reports that it `requires compiled runtime output for TypeScript entry ...`, the package was published without the JavaScript files OpenClaw needs at runtime — update or reinstall after the publisher ships compiled JavaScript, or disable/uninstall the plugin until then.

### Blocked plugin path ownership

If plugin diagnostics say `blocked plugin candidate: suspicious ownership (... uid=1000, expected uid=0 or root)` and config validation follows with `plugin present but blocked`, OpenClaw found plugin files owned by a different Unix user than the process that is loading them. Keep the plugin config in place; fix the filesystem ownership, or run OpenClaw as the same user that owns the state directory. For Docker installs, the official image runs as `node` (uid `1000`), so host bind-mounted OpenClaw config and workspace directories should normally be owned by uid `1000`:

```bash
sudo chown -R 1000:1000 /path/to/openclaw-config /path/to/openclaw-workspace
```

If you intentionally run OpenClaw as root, repair the managed plugin root to root ownership instead:

```bash
sudo chown -R root:root /path/to/openclaw-config/npm
```

After fixing ownership, rerun `openclaw doctor --fix` or `openclaw plugins registry --refresh` so the persisted plugin registry matches the repaired files.

### Slow plugin tool setup

If agent turns appear to stall while preparing tools, enable trace logging and check for plugin tool factory timing lines:

```bash
openclaw config set logging.level trace
openclaw logs --follow
```

Look for a `[trace:plugin-tools] factory timings ...` line. The summary lists total factory time and the slowest plugin tool factories, including plugin id, declared tool names, result shape, and whether the tool is optional. Slow lines are promoted to warnings when a single factory takes at least 1s or total plugin tool factory prep takes at least 5s. OpenClaw caches successful plugin tool factory results for repeated resolutions with the same effective request context; the cache key includes the effective runtime config, workspace, agent/session ids, sandbox policy, browser settings, delivery context, requester identity, and ownership state, so factories that depend on those trusted fields are re-run when the context changes. If timings stay high, the plugin may be doing expensive work before returning its tool definitions. If one plugin dominates the timing, inspect its runtime registrations with `openclaw plugins inspect <plugin-id> --runtime --json`, then update, reinstall, or disable that plugin. Plugin authors should move expensive dependency loading behind the tool execution path instead of doing it inside the tool factory. For dependency roots, package metadata validation, registry records, startup reload behavior, and legacy cleanup, see the Plugin dependency resolution page.

**Source**: OpenClaw documentation — `tools/plugin` (mirror `inbox/openclaw_docs/tools/plugin.md`), config/policy/hooks/verify/troubleshooting half
**Last Updated**: 2026-06-22
**Status**: Active
