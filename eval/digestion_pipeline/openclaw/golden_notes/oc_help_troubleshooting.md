---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - troubleshooting
keywords:
  - openclaw troubleshooting triage
  - openclaw first 60 seconds
  - openclaw status doctor gateway probe
  - assistant feels limited missing tools
  - anthropic long context 429
  - local openai-compatible backend fails
  - install policy blocks plugin
  - suspicious ownership blocked plugin
  - symptom decision tree
  - no replies control ui gateway channel cron node exec browser
topics:
  - OpenClaw
  - Troubleshooting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/troubleshooting
access_control_group: ["general"]
---

# OpenClaw — General Troubleshooting (Symptom-First Triage Hub)

## Overview

This note is the operator triage procedure for "OpenClaw is not working" — the symptom-first front door from the `help/troubleshooting` source page, for the fastest fix before diving into deep runbooks. It covers the First-60-seconds command ladder, the tool-profile fix when the assistant feels limited, the Anthropic long-context 429 pointer, the local OpenAI-compatible backend `compat` fixes, plugin install-shape / install-policy / suspicious-ownership recovery, and the symptom-to-cause decision tree plus its eight accordion symptom blocks (no replies, Control UI, gateway, channel flow, cron/heartbeat, node tools, exec approval, browser) — each routing to a deeper runbook.

## First 60 seconds

Run this exact ladder in order:

```bash
openclaw status
openclaw status --all
openclaw gateway probe
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

Good output, one line each: `openclaw status` shows configured channels and no obvious auth errors; `status --all` produces a full, shareable report; `gateway probe` shows the expected target reachable (`Reachable: yes`), where `Capability: ...` reports the proven auth level and `Read probe: limited - missing scope: operator.read` is degraded diagnostics, not a connect failure; `gateway status` shows `Runtime: running`, `Connectivity probe: ok`, and a plausible `Capability: ...` line (add `--require-rpc` for read-scope RPC proof); `doctor` shows no blocking errors; `channels status --probe` returns live per-account transport plus probe/audit results such as `works` or `audit ok` when reachable (else config-only summaries); and `logs --follow` shows steady activity with no repeating fatal errors.

## Assistant feels limited or missing tools

If the assistant cannot inspect files, run commands, use browser automation, or see expected tools, check the effective tool profile first via `openclaw status`, `status --all`, and `doctor`. Common causes: `tools.profile: "messaging"` is intentionally narrow for chat-only agents; `tools.profile: "coding"` is the usual profile for repository, file, shell, and runtime workflows; `tools.profile: "full"` exposes the broadest tool set and should be limited to trusted operator-controlled agents; and per-agent `agents.list[].tools` overrides can narrow or expand the root profile for one agent. Change the root or per-agent profile, restart or reload the Gateway, and run `status --all` again. See the Tools page for the profile model and allow/deny overrides.

## Anthropic long context 429

If you see `HTTP 429: rate_limit_error: Extra usage is required for long context requests`, go to `gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context`.

## Local OpenAI-compatible backend works directly but fails in OpenClaw

If your local/self-hosted `/v1` backend answers small direct `/v1/chat/completions` probes but fails on `openclaw infer model run` or agent turns, apply these compat fixes in order. (1) If the error mentions `messages[].content` expecting a string, set `models.providers.<provider>.models[].compat.requiresStringContent: true`. (2) If it still fails only on agent turns, set `compat.supportsTools: false` and retry. (3) If tiny direct calls work but larger prompts crash the backend, treat it as an upstream model/server limitation and continue in the deep runbook at `gateway/troubleshooting#local-openai-compatible-backend-passes-direct-probes-but-agent-runs-fail`.

## Plugin install fails with missing openclaw extensions

If install fails with `package.json missing openclaw.extensions`, the package uses an old shape OpenClaw no longer accepts. Fix it in the plugin package: (1) add `openclaw.extensions` to `package.json`; (2) point entries at built runtime files (usually `./dist/index.js`); (3) republish and run `openclaw plugins install <package>` again. Example `package.json`:

```json
{
  "name": "@openclaw/my-plugin",
  "version": "1.2.3",
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

Reference: Plugin architecture (`plugins/architecture`).

## Install policy blocks plugin installs or updates

If an update finishes but plugins are stale, disabled, or show `blocked by install policy`, `install policy failed closed`, or `Disabled "<plugin>" after plugin update failure`, check `security.installPolicy`. Install policy runs on plugin installs and updates; OpenClaw-owned plugin versions move with the OpenClaw release, so an update can also need matching `@openclaw/*` plugin updates during post-update sync. Avoid these broad policy shapes unless you maintain the matching upgrade rule: freezing OpenClaw-owned plugins to one exact old version (e.g. only `@openclaw/*@2026.5.3`); blocking by source kind alone (every npm, network, or `request.mode: "update"` request); treating the policy command as optional (an enabled `security.installPolicy` with a missing/slow/unreadable/permission-blocked executable fails closed); and approving versions without weighing the request's `openclawVersion` and candidate metadata. Safer rules allow trusted OpenClaw-owned updates when the candidate is compatible with the current host instead of pinning a release forever; if you block npm by default, make a narrow exception for the trusted `@openclaw/*` packages or plugin ids you use, applying the same trust rule to `request.mode: "update"`.

Recovery:

```bash
openclaw doctor --deep
openclaw plugins update --all
openclaw status --all
```

If the policy is intentionally strict, relax it for the trusted upgrade window, rerun `openclaw plugins update --all`, then restore the stricter rule. If a plugin was disabled after update failure, inspect it (`openclaw plugins inspect <plugin-id> --runtime --json`) and re-enable it (`openclaw plugins enable <plugin-id>`) only after the update succeeds. Reference: `tools/skills-config#operator-install-policy-securityinstallpolicy`.

## Plugin present but blocked by suspicious ownership

If `openclaw doctor`, setup, or startup warnings show `blocked plugin candidate: suspicious ownership (... uid=1000, expected uid=0 or root)` and `plugin present but blocked`, the plugin files are owned by a different Unix user than the loading process. Do not remove the plugin config — fix the ownership or run OpenClaw as the user that owns the state directory. Docker installs normally run as `node` (uid `1000`); for the default setup, repair the host bind mounts:

```bash
sudo chown -R 1000:1000 /path/to/openclaw-config /path/to/openclaw-workspace
openclaw doctor --fix
```

If you intentionally run as root, repair the managed plugin root to root ownership instead: `sudo chown -R root:root /path/to/openclaw-config/npm` then `openclaw doctor --fix`. Deeper docs: Plugin path ownership (`tools/plugin#blocked-plugin-path-ownership`) and Docker permissions (`install/docker#permissions-and-eacces`).

## Decision tree and symptom blocks

The source page's decision tree (a Mermaid `flowchart`) branches from "OpenClaw is not working" on "What breaks first" into eight symptoms, each routing to an accordion block below: No replies, Control UI will not connect, Gateway will not start, Channel connects but messages do not flow, Cron/heartbeat did not fire, Node paired but tool fails, Exec suddenly asks for approval, and Browser tool fails. Each block has a CLI ladder, good-output markers, log signatures, and deep-page links; the No-replies ladder is reproduced as representative:

```bash
openclaw status
openclaw gateway status
openclaw channels status --probe
openclaw pairing list --channel <channel> [--account <id>]
openclaw logs --follow
```

### No replies

Good output: `Runtime: running`; `Connectivity probe: ok`; a `Capability:` line (`read-only`, `write-capable`, or `admin-capable`); channel transport connected with (where supported) `works` or `audit ok`; and the sender approved (or open/allowlist DM policy). Common log signatures: `drop guild message (mention required` (Discord mention gating blocked the message), `pairing request` (sender unapproved, awaiting DM pairing), and `blocked` / `allowlist` (sender, room, or group filtered). Deep pages: `gateway/troubleshooting#no-replies`, `channels/troubleshooting`, and `channels/pairing`.

### Dashboard or Control UI will not connect

Run the same `status` / `gateway status` / `logs --follow` / `doctor` / `channels status --probe` ladder. Good output: `Dashboard: http://...` in `gateway status`, `Connectivity probe: ok`, a `Capability: ...` line, and no auth loop. Common log signatures: `device identity required` (HTTP/non-secure context cannot complete device auth); `origin not allowed` (browser `Origin` not allowed for the Control UI target); `AUTH_TOKEN_MISMATCH` with `canRetryWithDeviceToken=true` (one trusted device-token retry may occur automatically, reusing the cached scope set of the paired device token — explicit `deviceToken`/`scopes` callers keep their requested scopes); on the async Tailscale Serve path, failed attempts for the same `{scope, ip}` are serialized before the limiter records the failure, so a second concurrent bad retry can already show `retry later`; `too many failed authentication attempts (retry later)` from a localhost origin (that `Origin` is temporarily locked out — another localhost origin uses a separate bucket); repeated `unauthorized` after retry (wrong token/password, auth-mode mismatch, or stale device token); and `gateway connect failed:` (UI targeting the wrong URL/port or an unreachable gateway). Deep pages: `gateway/troubleshooting#dashboard-control-ui-connectivity`, `web/control-ui`, and `gateway/authentication`.

### Gateway will not start or service installed but not running

Same five-command ladder. Good output: `Service: ... (loaded)`, `Runtime: running`, `Connectivity probe: ok`, and a `Capability: ...` line. Common log signatures: `Gateway start blocked: set gateway.mode=local` or `existing config is missing gateway.mode` (gateway mode is remote, or the config is missing the local-mode stamp and should be repaired); `refusing to bind gateway ... without auth` (non-loopback bind without a valid auth path — token/password, or configured trusted-proxy); and `another gateway instance is already listening` or `EADDRINUSE` (port taken). Deep pages: `gateway/troubleshooting#gateway-service-not-running`, `gateway/background-process`, and `gateway/configuration`.

### Channel connects but messages do not flow

Same five-command ladder. Good output: transport connected, pairing/allowlist checks pass, mentions detected where required. Common log signatures: `mention required` (group mention gating blocked processing), `pairing` / `pending` (DM sender not approved), and `not_in_channel`, `missing_scope`, `Forbidden`, `401/403` (channel permission token issue). Deep pages: `gateway/troubleshooting#channel-connected-messages-not-flowing` and `channels/troubleshooting`.

### Cron or heartbeat did not fire or did not deliver

Run `openclaw status`, `gateway status`, `cron status`, `cron list`, `cron runs --id <jobId> --limit 20`, `logs --follow`. Good output: `cron.status` enabled with a next wake, `cron runs` with recent `ok` entries, and heartbeat enabled within active hours. Common log signatures: `cron: scheduler disabled; jobs will not run automatically` (cron disabled); `heartbeat skipped` with `reason=quiet-hours` (outside active hours), `reason=empty-heartbeat-file` (`HEARTBEAT.md` has only blank/comment/header/fence/empty-checklist scaffolding), `reason=no-tasks-due` (task mode active but no intervals due), or `reason=alerts-disabled` (`showOk`, `showAlerts`, and `useIndicator` all off); `requests-in-flight` (main lane busy; wake deferred); and `unknown accountId` (delivery target account missing). Deep pages: `gateway/troubleshooting#cron-and-heartbeat-delivery`, `automation/cron-jobs#troubleshooting`, and `gateway/heartbeat`.

### Node is paired but tool fails (camera/canvas/screen/exec)

Run `openclaw status`, `gateway status`, `nodes status`, `nodes describe --node <idOrNameOrIp>`, `logs --follow`. Good output: node connected and paired for role `node`, capability exists for the invoked command, and permission state granted for the tool. Common log signatures: `NODE_BACKGROUND_UNAVAILABLE` (bring node app to foreground), `*_PERMISSION_REQUIRED` (OS permission denied/missing), `SYSTEM_RUN_DENIED: approval required` (exec approval pending), and `SYSTEM_RUN_DENIED: allowlist miss` (command not on exec allowlist). Deep pages: `gateway/troubleshooting#node-paired-tool-fails`, `nodes/troubleshooting`, and `tools/exec-approvals`.

### Exec suddenly asks for approval

Inspect with `openclaw config get tools.exec.host`, `tools.exec.security`, and `tools.exec.ask`, then `openclaw gateway restart`. What changed: unset `tools.exec.host` defaults to `auto`, resolving to `sandbox` when a sandbox runtime is active and `gateway` otherwise; `host=auto` is routing only — the no-prompt "YOLO" behavior comes from `security=full` plus `ask=off` (the unset gateway/node defaults), so seeing approvals means some host-local or per-session policy tightened exec. Restore the no-approval default with `openclaw config set tools.exec.host gateway`, `... tools.exec.security full`, `... tools.exec.ask off`, then restart. Safer alternatives: set only `tools.exec.host=gateway` for stable routing; use `security=allowlist` with `ask=on-miss` to review allowlist misses; or enable sandbox mode so `host=auto` resolves back to `sandbox`. Common log signatures: `Approval required.` (waiting on `/approve ...`), `SYSTEM_RUN_DENIED: approval required` (node-host approval pending), and `exec host=sandbox requires a sandbox runtime for this session` (sandbox selected but mode off). Deep pages: `tools/exec`, `tools/exec-approvals`, and `gateway/security#what-the-audit-checks-high-level`.

### Browser tool fails

Run `openclaw status`, `gateway status`, `browser status`, `logs --follow`, `doctor`. Good output: browser status shows `running: true` and a chosen browser/profile, and `openclaw` starts or `user` can see local Chrome tabs. Common log signatures: `unknown command "browser"` (`plugins.allow` set without `browser`); `Failed to start Chrome CDP on port` (local launch failed); `browser.executablePath not found` (wrong binary path); `browser.cdpUrl must be http(s) or ws(s)` (unsupported scheme) and `browser.cdpUrl has invalid port` (bad/out-of-range port); `No Chrome tabs found for profile="user"` (no open tabs); `Remote CDP for profile "<name>" is not reachable` and `Browser attachOnly is enabled ... not reachable` (attach-only/remote profile has no live CDP target); and stale viewport/dark-mode/locale/offline overrides on attach-only or remote CDP profiles (run `openclaw browser stop --browser-profile <name>` to release emulation state without restarting the gateway). Deep pages: `gateway/troubleshooting#browser-tool-fails`, `tools/browser#missing-browser-command-or-tool`, `tools/browser-linux-troubleshooting`, and `tools/browser-wsl2-windows-remote-cdp-troubleshooting`.

**Source**: OpenClaw documentation — `help/troubleshooting` (mirror `inbox/openclaw_docs/help/troubleshooting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
