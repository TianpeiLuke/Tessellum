---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - troubleshooting
keywords:
  - openclaw no replies channel silent
  - channel connected messages not flowing
  - cron heartbeat delivery skip reasons
  - node paired tool fails system_run_denied
  - browser tool fails cdp existing-session
  - dm policy allowlist mention gating
  - missing_scope not_in_channel forbidden
topics:
  - OpenClaw
  - Gateway Troubleshooting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/troubleshooting
access_control_group: ["general"]
---

# OpenClaw — Gateway Message-Flow and Runtime Troubleshooting

## Overview

This procedure note covers the message-flow and runtime cluster of the OpenClaw Gateway troubleshooting runbook (`gateway/troubleshooting`): the symptoms an operator hits once the gateway process itself is healthy but messages, scheduled work, paired-node tools, or the browser tool still do not work. It mirrors five source sections — **No replies**, **Channel connected, messages not flowing**, **Cron and heartbeat delivery**, **Node paired, tool fails**, and **Browser tool fails** — plus the page's **Related** see-also block. Each section keeps the source's exact diagnostic commands, "Look for" signals, and verbatim log/error signatures so the symptom→command→fix path is preserved. Process/config and auth/connectivity clusters live in the sibling notes; confirm the gateway process is up (process_config) and auth/connectivity is clean before chasing message flow.

## No replies

If channels are up but nothing answers, check routing and policy before reconnecting anything. Run, in order:

```bash
openclaw status
openclaw channels status --probe
openclaw pairing list --channel <channel> [--account <id>]
openclaw config get channels
openclaw logs --follow
```

Look for: pairing pending for DM senders; group mention gating (`requireMention`, `mentionPatterns`); and channel/group allowlist mismatches.

Common signatures: `drop guild message (mention required` means a group message is ignored until a mention; `pairing request` means a sender needs approval; and `blocked` / `allowlist` means the sender or channel was filtered by policy. See also the source's Channel troubleshooting (`/channels/troubleshooting`), Groups (`/channels/groups`), and Pairing (`/channels/pairing`) pages.

## Channel connected, messages not flowing

If channel state is connected but message flow is dead, focus on policy, permissions, and channel-specific delivery rules. Run:

```bash
openclaw channels status --probe
openclaw pairing list --channel <channel> [--account <id>]
openclaw status --deep
openclaw logs --follow
openclaw config get channels
```

Look for: DM policy (`pairing`, `allowlist`, `open`, `disabled`); group allowlist and mention requirements; and missing channel API permissions/scopes.

Common signatures: `mention required` means the message is ignored by group mention policy; `pairing` / pending-approval traces mean the sender is not approved; and `missing_scope`, `not_in_channel`, `Forbidden`, `401/403` indicate a channel auth/permissions issue. Related source pages: Channel troubleshooting (`/channels/troubleshooting`), Discord (`/channels/discord`), Telegram (`/channels/telegram`), WhatsApp (`/channels/whatsapp`).

## Cron and heartbeat delivery

If cron or heartbeat did not run or did not deliver, verify scheduler state first, then the delivery target. Run:

```bash
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw system heartbeat last
openclaw logs --follow
```

Look for: cron enabled and next wake present; job run-history status (`ok`, `skipped`, `error`); and heartbeat skip reasons (`quiet-hours`, `requests-in-flight`, `cron-in-progress`, `lanes-busy`, `alerts-disabled`, `empty-heartbeat-file`, `no-tasks-due`).

Common signatures:

- `cron: scheduler disabled; jobs will not run automatically` → cron disabled.
- `cron: timer tick failed` → scheduler tick failed; check file/log/runtime errors.
- `heartbeat skipped` with `reason=quiet-hours` → outside the active-hours window.
- `heartbeat skipped` with `reason=empty-heartbeat-file` → `HEARTBEAT.md` exists but only contains blank, comment, header, fence, or empty-checklist scaffolding, so OpenClaw skips the model call.
- `heartbeat skipped` with `reason=no-tasks-due` → `HEARTBEAT.md` contains a `tasks:` block, but none of the tasks are due on this tick.
- `heartbeat: unknown accountId` → invalid account id for the heartbeat delivery target.
- `heartbeat skipped` with `reason=dm-blocked` → the heartbeat target resolved to a DM-style destination while `agents.defaults.heartbeat.directPolicy` (or a per-agent override) is set to `block`.

Related source pages: Heartbeat (`/gateway/heartbeat`), Scheduled tasks (`/automation/cron-jobs`), Scheduled tasks: troubleshooting (`/automation/cron-jobs#troubleshooting`).

## Node paired, tool fails

If a node is paired but its tools fail, isolate foreground, permission, and approval state. Run:

```bash
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
openclaw logs --follow
openclaw status
```

Look for: the node online with expected capabilities; OS permission grants for camera/mic/location/screen; and exec approvals plus allowlist state.

Common signatures: `NODE_BACKGROUND_UNAVAILABLE` means the node app must be in the foreground; `*_PERMISSION_REQUIRED` / `LOCATION_PERMISSION_REQUIRED` means a missing OS permission; `SYSTEM_RUN_DENIED: approval required` means an exec approval is pending; and `SYSTEM_RUN_DENIED: allowlist miss` means the command is blocked by the allowlist. Related source pages: Exec approvals (`/tools/exec-approvals`), Node troubleshooting (`/nodes/troubleshooting`), Nodes (`/nodes/index`).

## Browser tool fails

Use this when browser tool actions fail even though the gateway itself is healthy. Run:

```bash
openclaw browser status
openclaw browser start --browser-profile openclaw
openclaw browser profiles
openclaw logs --follow
openclaw doctor
```

Look for: whether `plugins.allow` is set and includes `browser`; a valid browser executable path; CDP profile reachability; and local Chrome availability for `existing-session` / `user` profiles.

### Plugin / executable signatures

- `unknown command "browser"` or `unknown command 'browser'` → the bundled browser plugin is excluded by `plugins.allow`.
- browser tool missing / unavailable while `browser.enabled=true` → `plugins.allow` excludes `browser`, so the plugin never loaded.
- `Failed to start Chrome CDP on port` → the browser process failed to launch.
- `browser.executablePath not found` → the configured path is invalid.
- `browser.cdpUrl must be http(s) or ws(s)` → the configured CDP URL uses an unsupported scheme such as `file:` or `ftp:`.
- `browser.cdpUrl has invalid port` → the configured CDP URL has a bad or out-of-range port.
- `Playwright is not available in this gateway build; '<feature>' is unsupported.` → the current gateway install lacks the core browser runtime dependency; reinstall or update OpenClaw, then restart the gateway. ARIA snapshots and basic page screenshots can still work, but navigation, AI snapshots, CSS-selector element screenshots, and PDF export stay unavailable.

### Chrome MCP / existing-session signatures

- `Could not find DevToolsActivePort for chrome` → the Chrome MCP existing-session could not attach to the selected browser data dir yet. Open the browser inspect page, enable remote debugging, keep the browser open, approve the first attach prompt, then retry. If signed-in state is not required, prefer the managed `openclaw` profile.
- `No Chrome tabs found for profile="user"` → the Chrome MCP attach profile has no open local Chrome tabs.
- `Remote CDP for profile "<name>" is not reachable` → the configured remote CDP endpoint is not reachable from the gateway host.
- `Browser attachOnly is enabled ... not reachable` or `Browser attachOnly is enabled and CDP websocket ... is not reachable` → an attach-only profile has no reachable target, or the HTTP endpoint answered but the CDP WebSocket still could not be opened.

### Element / screenshot / upload signatures

- `fullPage is not supported for element screenshots` → the screenshot request mixed `--full-page` with `--ref` or `--element`.
- `element screenshots are not supported for existing-session profiles; use ref from snapshot.` → Chrome MCP / `existing-session` screenshot calls must use page capture or a snapshot `--ref`, not a CSS `--element`.
- `existing-session file uploads do not support element selectors; use ref/inputRef.` → Chrome MCP upload hooks need snapshot refs, not CSS selectors.
- `existing-session file uploads currently support one file at a time.` → send one upload per call on Chrome MCP profiles.
- `existing-session dialog handling does not support timeoutMs.` → dialog hooks on Chrome MCP profiles do not support timeout overrides.
- `existing-session type does not support timeoutMs overrides.` → omit `timeoutMs` for `act:type` on `profile="user"` / Chrome MCP existing-session profiles, or use a managed/CDP browser profile when a custom timeout is required.
- `existing-session evaluate does not support timeoutMs overrides.` → omit `timeoutMs` for `act:evaluate` on `profile="user"` / Chrome MCP existing-session profiles, or use a managed/CDP browser profile when a custom timeout is required.
- `response body is not supported for existing-session profiles yet.` → `responsebody` still requires a managed browser or raw CDP profile.
- stale viewport / dark-mode / locale / offline overrides on attach-only or remote CDP profiles → run `openclaw browser stop --browser-profile <name>` to close the active control session and release Playwright/CDP emulation state without restarting the whole gateway.

Related source pages: Browser, OpenClaw-managed (`/tools/browser`) and Browser troubleshooting (`/tools/browser-linux-troubleshooting`).

**Source**: OpenClaw documentation — `gateway/troubleshooting` (mirror `inbox/openclaw_docs/gateway/troubleshooting.md`); sections: No replies, Channel connected messages not flowing, Cron and heartbeat delivery, Node paired tool fails, Browser tool fails, Related
**Last Updated**: 2026-06-22
**Status**: Active
