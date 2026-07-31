---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - exec
keywords:
  - openclaw tools.exec config
  - exec timeoutSec strictInlineEval
  - exec pathPrepend PATH handling
  - tools.exec.security ask mode
  - safeBins safeBinTrustedDirs safeBinProfiles
  - apply_patch subtool workspaceOnly
  - env.PATH LD_ DYLD_ rejection
  - per-agent exec node binding
topics:
  - OpenClaw
  - Exec Tool Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/exec
access_control_group: ["general"]
---

# OpenClaw — Exec Tool Configuration (`tools.exec.*`, PATH handling, apply_patch)

## Overview

This note is the configuration half of OpenClaw's `exec` shell tool (mirroring the `Config`, `PATH handling`, `Allowlist + safe bins` pointer, and `apply_patch` sections of the `tools/exec` source page). It documents the `tools.exec.*` knobs that shape every exec call — timeout, exit-notify, default host, the `security`/`ask` policy dials, `strictInlineEval`, `commandHighlighting`, `pathPrepend`, and the three safe-bin keys — plus per-host PATH merging with `env.PATH`/loader-override rejection, and the OpenAI/Codex-only `apply_patch` subtool. The exec invocation surface (parameters, `host=auto` routing, `/exec` session overrides, the authorization model, and examples) lives in the split sibling [oc_tools_exec_usage](oc_tools_exec_usage.md); the safe-bin and allowlist policy detail lives in [oc_tools_exec_approvals_safe_bins](oc_tools_exec_approvals_safe_bins.md).

## `tools.exec.*` Config Knobs

Configure exec behavior under the `tools.exec` object. The knobs and their documented defaults:

- `tools.exec.notifyOnExit` (default: `true`): when true, backgrounded exec sessions enqueue a system event and request a heartbeat on exit.
- `tools.exec.approvalRunningNoticeMs` (default: `10000`): emit a single "running" notice when an approval-gated exec runs longer than this (`0` disables).
- `tools.exec.timeoutSec` (default: `1800`): default per-command exec timeout in seconds. A per-call `timeout` parameter overrides it; per-call `timeout: 0` disables the exec process timeout.
- `tools.exec.host` (default: `auto`): resolves to `sandbox` when a sandbox runtime is active, `gateway` otherwise.
- `tools.exec.security` (default: `deny` for sandbox, `full` for gateway + node when unset).
- `tools.exec.ask` (default: `off`).
- `tools.exec.node` (default: unset).
- `tools.exec.strictInlineEval` (default: `false`): see the dedicated section below.
- `tools.exec.commandHighlighting` (default: `false`): when true, approval prompts can highlight parser-derived command spans in the command text. Set to `true` globally or per agent to enable command-text highlighting without changing exec approval policy.
- `tools.exec.pathPrepend`: list of directories to prepend to `PATH` for exec runs (gateway + sandbox only).
- `tools.exec.safeBins`: stdin-only safe binaries that can run without explicit allowlist entries — for behavior details see [Safe bins (stdin-only)](https://docs.openclaw.ai/tools/exec-approvals-advanced#safe-bins-stdin-only) and the note below.
- `tools.exec.safeBinTrustedDirs`: additional explicit directories trusted for `safeBins` path checks. `PATH` entries are never auto-trusted. Built-in defaults are `/bin` and `/usr/bin`.
- `tools.exec.safeBinProfiles`: optional custom argv policy per safe bin (`minPositional`, `maxPositional`, `allowedValueFlags`, `deniedFlags`).

No-approval host exec is the default for gateway + node. To get approvals/allowlist behavior, tighten BOTH `tools.exec.*` AND the host approvals file (see [oc_tools_exec_approvals_policy](oc_tools_exec_approvals_policy.md)). "YOLO" comes from the host-policy defaults (`security=full`, `ask=off`), not from `host=auto`; to force gateway or node routing, set `tools.exec.host` or use `/exec host=...`. In `security=full` plus `ask=off` mode, host exec follows the configured policy directly — there is no extra heuristic command-obfuscation prefilter or script-preflight rejection layer.

A minimal `pathPrepend` config:

```json5
{
  tools: {
    exec: {
      pathPrepend: ["~/bin", "/opt/oss/bin"],
    },
  },
}
```

### `tools.exec.strictInlineEval`

When `true`, inline interpreter eval forms such as `python -c`, `node -e`, `ruby -e`, `perl -e`, `php -r`, `lua -e`, and `osascript -e` require reviewer or explicit approval. In `mode=auto`, the normal exec approval path may let the native auto reviewer allow a clearly low-risk one-off command; direct node-host `system.run` calls still require an explicit approval because they cannot hand the command to a human approval route. If the reviewer asks, the request goes to a human. `allow-always` can still persist benign interpreter/script invocations, but inline-eval forms do not become durable allow rules. If you explicitly allowlist interpreters, enable `strictInlineEval` so inline code-eval forms still require reviewer or explicit approval.

## PATH Handling (per host)

PATH resolution differs by execution host. `env.PATH` overrides are rejected for host execution (gateway/node) to prevent binary hijacking or injected code; loader overrides (`LD_*`/`DYLD_*`) are likewise rejected on host execution.

- `host=gateway`: merges your login-shell `PATH` into the exec environment. `env.PATH` overrides are rejected for host execution. The daemon itself still runs with a minimal `PATH`:
  - macOS: `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`
  - Linux: `/usr/local/bin`, `/usr/bin`, `/bin`
  - To prevent user shell configuration (like `~/.zshenv` or `/etc/zshenv`) from overriding priority paths during startup, `tools.exec.pathPrepend` entries are securely prepended to the final `PATH` inside the shell command right before execution.
- `host=sandbox`: runs `sh -lc` (login shell) inside the container, so `/etc/profile` may reset `PATH`. OpenClaw prepends `env.PATH` after profile sourcing via an internal env var (no shell interpolation); `tools.exec.pathPrepend` applies here too.
- `host=node`: only non-blocked env overrides you pass are sent to the node. `env.PATH` overrides are rejected for host execution and ignored by node hosts. To add PATH entries on a node, configure the node host service environment (systemd/launchd) or install tools in standard locations.

### Per-agent node binding

Bind a specific agent's exec calls to a node using the agent list index in config:

```bash
openclaw config get agents.list
openclaw config set 'agents.list[0].tools.exec.node' "node-id-or-name"
```

The Control UI's Nodes tab includes a small "Exec node binding" panel for the same settings.

## Allowlist + Safe Bins (config pointer)

The `exec` page documents two distinct controls and warns against conflating them; the full policy semantics are digested in [oc_tools_exec_approvals_safe_bins](oc_tools_exec_approvals_safe_bins.md). Use the controls for different jobs:

- `tools.exec.safeBins`: small, stdin-only stream filters.
- `tools.exec.safeBinTrustedDirs`: explicit extra trusted directories for safe-bin executable paths.
- `tools.exec.safeBinProfiles`: explicit argv policy for custom safe bins.
- allowlist: explicit trust for executable paths.

Do not treat `safeBins` as a generic allowlist, and do not add interpreter/runtime binaries (for example `python3`, `node`, `ruby`, `bash`); if you need those, use explicit allowlist entries and keep approval prompts enabled. `openclaw security audit` warns when interpreter/runtime `safeBins` entries are missing explicit profiles, and `openclaw doctor --fix` can scaffold missing custom `safeBinProfiles` entries. `openclaw security audit` and `openclaw doctor` also warn when you explicitly add broad-behavior bins such as `jq` back into `safeBins`. `autoAllowSkills` is a separate convenience path in exec approvals — not the same as manual path allowlist entries; for strict explicit trust, keep `autoAllowSkills` disabled.

## `apply_patch` Subtool

`apply_patch` is a subtool of `exec` for structured multi-file edits. It is enabled by default for OpenAI and OpenAI Codex models. Use config only when you want to disable it or restrict it to specific models:

```json5
{
  tools: {
    exec: {
      applyPatch: { workspaceOnly: true, allowModels: ["gpt-5.5"] },
    },
  },
}
```

Notes on `apply_patch`:

- Only available for OpenAI/OpenAI Codex models.
- Tool policy still applies; `allow: ["write"]` implicitly allows `apply_patch`.
- `deny: ["write"]` does NOT deny `apply_patch`; deny `apply_patch` explicitly or use `deny: ["group:fs"]` when patch writes should also be blocked.
- Config lives under `tools.exec.applyPatch`.
- `tools.exec.applyPatch.enabled` defaults to `true`; set it to `false` to disable the tool for OpenAI models.
- `tools.exec.applyPatch.workspaceOnly` defaults to `true` (workspace-contained). Set it to `false` only if you intentionally want `apply_patch` to write/delete outside the workspace directory.

**Source**: OpenClaw documentation — `tools/exec` (Config / PATH handling / Allowlist+safe-bins pointer / apply_patch sections; mirror `inbox/openclaw_docs/tools/exec.md`)
**Last Updated**: 2026-06-22
**Status**: Active
