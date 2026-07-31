---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - imessage
keywords:
  - openclaw imessage setup
  - imsg json-rpc stdio
  - imsg private api sip
  - full disk access automation
  - imsg launch helper dylib
  - remote mac ssh cliPath
  - csrutil disable library validation
  - openclaw channels status probe
topics:
  - OpenClaw
  - iMessage Channel Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/imessage
access_control_group: ["general"]
---

# OpenClaw — Setting Up Native iMessage via `imsg`

## Overview

This note is the host-setup procedure for OpenClaw's native iMessage channel, mirroring the **Quick setup**, **Requirements and permissions (macOS)**, and **Enabling the imsg private API** sections of the `channels/imessage` source page. OpenClaw talks to iMessage through `imsg`, an external CLI: the Gateway spawns `imsg rpc` and communicates over **JSON-RPC on stdio** (no separate daemon or port). This note covers the two connection topologies (a local signed-in Mac vs a remote Mac reached over an SSH `cliPath` wrapper), the macOS permissions required (Full Disk Access, Automation, Messages signed in), and the optional Private API mode that requires disabling System Integrity Protection (SIP) to inject a helper dylib into `Messages.app`. Access control / routing / ACP bindings, delivery / private-API actions, coalescing, inbound recovery, and troubleshooting are documented in the sibling notes **oc_channels_imessage_access_acp** and **oc_channels_imessage_delivery_ops**.

> **Migration note:** BlueBubbles support was removed; OpenClaw supports iMessage through `imsg` only. Migrate `channels.bluebubbles` configs to `channels.imessage` — see the sibling **oc_channels_imessage_from_bluebubbles** note for the full migration path.

## Quick setup

Advanced actions require `imsg launch` and a successful private API probe; basic text/media send/receive does not. Pick the topology that matches where the Gateway runs.

### Local Mac (fast path)

Run these on the Mac signed into Messages: install and verify `imsg`, inject the helper, probe from OpenClaw, start the gateway, then approve the first DM pairing (iMessage DMs default to pairing mode via `dmPolicy`):

```bash
brew install steipete/tap/imsg
imsg rpc --help
imsg launch
openclaw channels status --probe
openclaw gateway
openclaw pairing list imessage
openclaw pairing approve imessage <CODE>
```

Pairing requests expire after 1 hour. Configure the channel, pointing `cliPath` at the `imsg` binary and `dbPath` at the local Messages database:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/usr/local/bin/imsg",
      dbPath: "/Users/user/Library/Messages/chat.db",
    },
  },
}
```

### Remote Mac over SSH

OpenClaw only requires a stdio-compatible `cliPath`, so when the Gateway runs on Linux or Windows you can point `cliPath` at a wrapper script that SSHes to a remote Mac and runs `imsg`:

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

Recommended config when attachments are enabled. `remoteHost` is used for SCP attachment fetches and must be `host` or `user@host` (no spaces or SSH options); if unset, OpenClaw attempts to auto-detect it by parsing the SSH wrapper script:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "user@gateway-host", // used for SCP attachment fetches
      includeAttachments: true,
      // Optional: override allowed attachment roots.
      // Defaults include /Users/*/Library/Messages/Attachments
      attachmentRoots: ["/Users/*/Library/Messages/Attachments"],
      remoteAttachmentRoots: ["/Users/*/Library/Messages/Attachments"],
    },
  },
}
```

OpenClaw uses strict host-key checking for SCP, so the relay host key must already exist in `~/.ssh/known_hosts`, and attachment paths are validated against the allowed roots (`attachmentRoots` / `remoteAttachmentRoots`).

**Stdio-transparency requirement (load-bearing):** any `cliPath` wrapper or SSH proxy in front of `imsg` MUST behave like a transparent stdio pipe for long-lived JSON-RPC, because OpenClaw exchanges small newline-framed JSON-RPC messages over the wrapper's stdin/stdout for the lifetime of the channel. Forward each stdin chunk/line **as soon as bytes are available** (don't wait for EOF), forward each stdout chunk/line promptly in reverse, preserve newlines, avoid fixed-size blocking reads (`read(4096)`, `cat | buffer`, default shell `read`) that can starve small frames, and keep stderr separate from the JSON-RPC stdout stream. A wrapper that buffers stdin until a large block fills produces symptoms that look like an iMessage outage — `imsg rpc timeout (chats.list)` or repeated channel restarts — even though `imsg rpc` itself is healthy. `ssh -T host imsg "$@"` is safe because it forwards OpenClaw's `cliPath` arguments such as `rpc` and `--db`; pipelines like `ssh host imsg | grep -v '^DEBUG'` are NOT (line-buffered tools can still hold frames — use `stdbuf -oL -eL` on every stage if you must filter).

## Requirements and permissions (macOS)

The `imsg` host has hard macOS prerequisites:

- Messages must be **signed in** on the Mac running `imsg`.
- **Full Disk Access** is required for the process context running OpenClaw / `imsg` (for Messages DB access).
- **Automation** permission is required to send messages through Messages.app.
- For advanced actions (react / edit / unsend / threaded reply / effects / group ops), **System Integrity Protection must be disabled** — see *Enabling the imsg private API* below. Basic text and media send/receive work without it.

Permissions are granted **per process context**. If the gateway runs headless (LaunchAgent / SSH), run a one-time interactive command in that same context to trigger the macOS permission prompts — for example `imsg chats --limit 1` or `imsg send <handle> "test"`.

**SSH-wrapper sends fail with AppleEvents `-1743`:** a remote-SSH setup can read chats, pass `channels status --probe`, and process inbound messages while outbound sends still fail with `Not authorized to send Apple events to Messages. (-1743)`. Check the signed-in Mac user's TCC database or System Settings > Privacy & Security > Automation. If the Automation entry is recorded for `/usr/libexec/sshd-keygen-wrapper` instead of the `imsg` or local shell process (e.g. `kTCCServiceAppleEvents | /usr/libexec/sshd-keygen-wrapper | auth_value=0 | com.apple.MobileSMS`), macOS may not expose a usable Messages toggle for that SSH server-side client, and repeating `tccutil reset AppleEvents` or rerunning `imsg send` through the same wrapper keeps failing because the process context needing Automation is the SSH wrapper, not an app the UI can grant. Fix it by using a supported `imsg` process context instead: run the Gateway (or at least the `imsg` bridge) in the logged-in Messages user's local session; start the Gateway with a LaunchAgent for that user after granting Full Disk Access and Automation from the same session; or, if you keep the two-user SSH topology, verify a real outbound `imsg send` succeeds through the exact wrapper before enabling the channel, and reconfigure to a single-user `imsg` setup if Automation cannot be granted.

## Enabling the imsg private API

`imsg` ships in two operational modes:

- **Basic mode** (default, no SIP changes needed): outbound text and media via `send`, inbound watch/history, and chat list. This is what a fresh `brew install steipete/tap/imsg` plus the standard macOS permissions above gives you.
- **Private API mode**: `imsg` injects a helper dylib into `Messages.app` to call internal `IMCore` functions, unlocking `react`, `edit`, `unsend`, `reply` (threaded), `sendWithEffect`, `renameGroup`, `setGroupIcon`, `addParticipant`, `removeParticipant`, `leaveGroup`, plus typing indicators and read receipts.

Per the `imsg` README, advanced features (`read`, `typing`, `launch`, bridge-backed rich send, message mutation, chat management) are opt-in: they require SIP to be disabled and a helper dylib injected into `Messages.app`, and `imsg launch` refuses to inject when SIP is enabled. The helper-injection technique uses `imsg`'s own dylib to reach Messages private APIs — there is no third-party server or BlueBubbles runtime in the OpenClaw iMessage path.

> **SIP is a real security tradeoff.** SIP is one of macOS's core protections against running modified system code; turning it off system-wide opens additional attack surface and side effects. Notably, **disabling SIP on Apple Silicon Macs also disables installing and running iOS apps on your Mac**. Treat this as a deliberate operational choice, not a default. If your threat model can't tolerate SIP being off, bundled iMessage is limited to basic mode — text and media send/receive only.

### Setup

**1. Install (or upgrade) `imsg`** on the Mac that runs Messages.app (`brew install steipete/tap/imsg`; check `imsg --version`). The `imsg status --json` output reports `bridge_version`, `rpc_methods`, and per-method `selectors`, so you can see what the current build supports before you start.

**2. Disable System Integrity Protection, and (on modern macOS) Library Validation.** Injecting a non-Apple helper dylib into the Apple-signed `Messages.app` needs SIP off **and** library validation relaxed. The Recovery-mode SIP step is macOS-version-specific:

- **macOS 10.13-10.15 (Sierra-Catalina):** disable Library Validation via Terminal, reboot to Recovery Mode, run `csrutil disable`, restart.
- **macOS 11+ (Big Sur and later), Intel:** Recovery Mode (or Internet Recovery), `csrutil disable`, restart.
- **macOS 11+, Apple Silicon:** power-button startup sequence to enter Recovery; on recent macOS versions hold the **Left Shift** key when you click Continue, then `csrutil disable`. Virtual-machine setups follow a separate flow, so take a VM snapshot first.

On macOS 11 and later, `csrutil disable` alone is usually not enough — Apple still enforces library validation against `Messages.app` as a platform binary, so an adhoc-signed helper is rejected (`Library Validation failed: ... platform binary, but mapped file is not`) even with SIP off. After disabling SIP, also disable library validation and reboot:

```bash
sudo defaults write /Library/Preferences/com.apple.security.libraryvalidation.plist DisableLibraryValidation -bool true
```

**macOS 26 (Tahoe), verified on 26.5.1:** SIP off **plus** the `DisableLibraryValidation` command above is sufficient to inject the helper across 26.0 through 26.5.x — **no boot-args required**. The plist is the decisive factor and the most common missing step: with the plist, `imsg launch` injects and `imsg status` reports `advanced_features: true`; without it (even with SIP off) `imsg launch` fails with `Failed to launch: Timeout waiting for Messages.app to initialize` because AMFI rejects the adhoc helper at load, so the bridge never becomes ready. If `imsg launch` injection or specific `selectors` start returning false after a macOS upgrade, this gate is the usual cause — check SIP and library-validation state before assuming the SIP step failed, and if settings are correct but the bridge still cannot inject, collect `imsg status --json` plus the `imsg launch` output and report it to the `imsg` project instead of weakening additional system-wide security controls.

**3. Inject the helper, then 4. verify the bridge from OpenClaw.** With SIP disabled and Messages.app signed in, `imsg launch` injects (it refuses when SIP is still enabled, so it also doubles as confirmation that step 2 took), then probe:

```bash
imsg launch
openclaw channels status --probe
```

The iMessage entry should report `works`, and `imsg status --json | jq '.selectors'` should show `retractMessagePart: true` plus whichever edit / typing / read selectors your macOS build exposes. The OpenClaw plugin's per-method gating in `actions.ts` only advertises actions whose underlying selector is `true`, so the action surface in the agent's tool list reflects what the bridge can actually do on this host. If the probe reports `works` but specific actions throw "iMessage `<action>` requires the imsg private API bridge" at dispatch time, run `imsg launch` again — the helper can fall out (Messages.app restart, OS update, etc.), and the cached `available: true` status keeps advertising actions until the next probe refreshes.

### When you can't disable SIP

If SIP-disabled isn't acceptable for your threat model:

- `imsg` falls back to basic mode — text + media + receive only.
- The OpenClaw plugin still advertises text/media send and inbound monitoring; it just hides `react`, `edit`, `unsend`, `reply`, `sendWithEffect`, and group ops from the action surface (per the per-method capability gate).
- You can run a separate non-Apple-Silicon Mac (or a dedicated bot Mac) with SIP off for the iMessage workload while keeping SIP enabled on your primary devices — the dedicated-bot deployment pattern is covered in the **oc_channels_imessage_access_acp** sibling note.

**Source**: OpenClaw documentation — `channels/imessage` (mirror `inbox/openclaw_docs/channels/imessage.md`) — Quick setup, Requirements and permissions (macOS), Enabling the imsg private API
**Last Updated**: 2026-06-22
**Status**: Active
