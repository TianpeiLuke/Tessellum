---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - imessage
keywords:
  - openclaw bluebubbles removal
  - bluebubbles to imessage migration
  - imsg imessage plugin
  - channels.imessage config
  - imsg json-rpc stdin stdout
  - full disk access automation permissions
  - channels status --probe
  - acp channel bluebubbles imessage rename
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/announcements/bluebubbles-imessage
access_control_group: ["general"]
---

# OpenClaw — Migrating BlueBubbles to the `imsg` iMessage Path

## Overview

This note is the migration procedure for moving an OpenClaw deployment off the removed **BlueBubbles** channel onto the supported **iMessage** path, mirroring the `announcements/bluebubbles-imessage` source page. OpenClaw no longer ships the BlueBubbles channel; iMessage support now runs through the bundled `imessage` plugin, which starts [`imsg`](https://github.com/steipete/imsg) locally or through an SSH wrapper and talks JSON-RPC over stdin/stdout. If your config still contains `channels.bluebubbles`, migrate it to `channels.imessage`; the legacy `/channels/bluebubbles` docs URL redirects to "Coming from BlueBubbles" (`/channels/imessage-from-bluebubbles`), which holds the full config-translation table and cutover checklist. The procedure below covers what changed in the supported path, the five-step cutover (install/verify `imsg`, grant macOS permissions, translate the config, restart and probe, test before deleting the old server), and the migration caveats — link out to the channel docs for the exhaustive translation reference rather than reproducing it here.

## What Changed

The supported OpenClaw iMessage path differs from BlueBubbles in transport and capabilities:

- There is **no BlueBubbles HTTP server, webhook route, REST password, or BlueBubbles plugin runtime** in the supported OpenClaw iMessage path.
- OpenClaw reads and watches Messages through `imsg` on the Mac where **Messages.app is signed in**.
- Basic **send, receive, history, and media** use the normal `imsg` surfaces and macOS permissions.
- Advanced actions — **threaded replies, tapbacks, edit, unsend, effects, read receipts, typing indicators, and group management** — require `imsg launch` with the private API bridge available.
- **Linux and Windows gateways** can still use iMessage by setting `channels.imessage.cliPath` to an SSH wrapper that runs `imsg` on the signed-in Mac.

## Migration Steps

Perform the cutover in five ordered steps.

**1. Install and verify `imsg` on the Messages Mac.** Install via Homebrew and confirm the CLI and RPC surfaces respond:

```bash
brew install steipete/tap/imsg
imsg --version
imsg chats --limit 3
imsg rpc --help
```

**2. Grant macOS permissions.** Grant **Full Disk Access** and **Automation** permissions to the process context that runs `imsg` and OpenClaw.

**3. Translate the old config.** Replace `channels.bluebubbles` with a `channels.imessage` block. The translated configuration is:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/opt/homebrew/bin/imsg",
      dmPolicy: "pairing",
      allowFrom: ["+15555550123"],
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true },
      },
      includeAttachments: true,
    },
  },
}
```

**4. Restart the gateway and verify.** Restart the gateway, then probe channel status:

```bash
openclaw channels status --probe
```

**5. Test before deleting the old server.** Test DMs, groups, attachments, and any private API actions you depend on **before deleting your old BlueBubbles server**.

## Migration Caveats

When translating the configuration, apply these field-level rules from the source page:

- `channels.bluebubbles.serverUrl` and `channels.bluebubbles.password` have **no iMessage equivalent**.
- `channels.bluebubbles.allowFrom`, `groupAllowFrom`, `groups`, `includeAttachments`, attachment roots, media size limits, chunking, and action toggles **have iMessage equivalents**.
- `channels.imessage.includeAttachments` is **still off by default**. Set it explicitly if you expect inbound photos, voice memos, videos, or files to reach the agent.
- With `groupPolicy: "allowlist"`, copy the old `groups` block, including any `"*"` wildcard entry. **Group sender allowlists and the group registry are separate gates.**
- ACP bindings that matched `channel: "bluebubbles"` must be changed to `channel: "imessage"`.
- Old BlueBubbles **session keys do not become iMessage session keys**. Pairing approvals carry over by handle, but conversation history under BlueBubbles session keys does not.

**Source**: OpenClaw documentation — `announcements/bluebubbles-imessage` (mirror `inbox/openclaw_docs/announcements/bluebubbles-imessage.md`)
**Last Updated**: 2026-06-22
**Status**: Active
