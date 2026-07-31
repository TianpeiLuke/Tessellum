---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - nextcloud_talk
keywords:
  - openclaw nextcloud talk
  - nextcloud talk webhook bot
  - occ talk bot install
  - channels.nextcloud-talk config
  - nextcloud talk dmPolicy pairing
  - nextcloud talk rooms allowlist
  - botSecret apiUser apiPassword
  - webhookPublicUrl webhookPort
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/nextcloud-talk
access_control_group: ["general"]
---

# OpenClaw — Connecting Nextcloud Talk

## Overview

This procedure note covers connecting a self-hosted **Nextcloud Talk** instance to the OpenClaw gateway as a webhook bot, mirroring the `channels/nextcloud-talk` source page. Nextcloud Talk ships as a **bundled plugin (webhook bot)** and supports direct messages, rooms, reactions, and markdown messages. The note walks through the bundled-plugin install (and the manual `@openclaw/nextcloud-talk` install for older/custom builds), the beginner quick setup (server-side bot creation with `occ talk:bot:install` plus OpenClaw config or CLI), operational notes/limitations, DM access control, room (group) handling, the capability matrix, and the full `channels.nextcloud-talk.*` configuration reference.

## Bundled plugin

Nextcloud Talk ships as a bundled plugin in current OpenClaw releases, so normal packaged builds do not need a separate install. If you are on an older build or a custom install that excludes Nextcloud Talk, install the npm package directly via the CLI:

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

Use the bare package to follow the current official release tag; pin an exact version only when you need a reproducible install. When running from a git repo, a local checkout can be installed instead:

```bash
openclaw plugins install ./path/to/local/nextcloud-talk-plugin
```

## Quick setup (beginner)

1. **Ensure the Nextcloud Talk plugin is available.** Current packaged OpenClaw releases already bundle it; older/custom installs can add it manually with the commands above.
2. **On your Nextcloud server, create a bot** using the `occ` admin command with the webhook, response, and reaction features:

   ```bash
   ./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature webhook --feature response --feature reaction
   ```

3. **Enable the bot in the target room settings.**
4. **Configure OpenClaw** — either via config (`channels.nextcloud-talk.baseUrl` + `channels.nextcloud-talk.botSecret`) or via the env var `NEXTCLOUD_TALK_BOT_SECRET` (default account only). The CLI setup form is:

   ```bash
   openclaw channels add --channel nextcloud-talk \
     --url https://cloud.example.com \
     --token "<shared-secret>"
   ```

   The equivalent explicit-field form uses `--base-url` and `--secret`, and a file-backed secret uses `--secret-file /path/to/nextcloud-talk-secret` instead of `--secret`.
5. **Restart the gateway** (or finish setup).

The minimal config that results sets `enabled`, `baseUrl`, `botSecret`, and `dmPolicy`:

```json5
{
  channels: {
    "nextcloud-talk": {
      enabled: true,
      baseUrl: "https://cloud.example.com",
      botSecret: "shared-secret",
      dmPolicy: "pairing",
    },
  },
}
```

## Notes

- Bots cannot initiate DMs — the user must message the bot first.
- The webhook URL must be reachable by the Gateway; set `webhookPublicUrl` if behind a proxy.
- Media uploads are not supported by the bot API; media is sent as URLs.
- The webhook payload does not distinguish DMs vs rooms; set `apiUser` + `apiPassword` to enable room-type lookups (otherwise DMs are treated as rooms).

## Access control (DMs)

- **Default:** `channels.nextcloud-talk.dmPolicy = "pairing"` — unknown senders get a pairing code.
- Approve a pending sender via `openclaw pairing list nextcloud-talk` and `openclaw pairing approve nextcloud-talk <CODE>`.
- **Public DMs:** set `channels.nextcloud-talk.dmPolicy="open"` plus `channels.nextcloud-talk.allowFrom=["*"]`.
- `allowFrom` matches Nextcloud user IDs only; display names are ignored.

## Rooms (groups)

- **Default:** `channels.nextcloud-talk.groupPolicy = "allowlist"` (mention-gated).
- Allowlist rooms with `channels.nextcloud-talk.rooms` keyed by room token, each carrying per-room settings such as `requireMention`:

```json5
{
  channels: {
    "nextcloud-talk": {
      rooms: {
        "room-token": { requireMention: true },
      },
    },
  },
}
```

- To allow no rooms, keep the allowlist empty or set `channels.nextcloud-talk.groupPolicy="disabled"`.

## Capabilities

| Feature         | Status        |
| --------------- | ------------- |
| Direct messages | Supported     |
| Rooms           | Supported     |
| Threads         | Not supported |
| Media           | URL-only      |
| Reactions       | Supported     |
| Native commands | Not supported |

## Configuration reference (Nextcloud Talk)

Provider options under `channels.nextcloud-talk.*`:

- `enabled`: enable/disable channel startup.
- `baseUrl`: Nextcloud instance URL.
- `botSecret`: bot shared secret.
- `botSecretFile`: regular-file secret path. Symlinks are rejected.
- `apiUser`: API user for room lookups (DM detection).
- `apiPassword`: API/app password for room lookups.
- `apiPasswordFile`: API password file path.
- `webhookPort`: webhook listener port (default: 8788).
- `webhookHost`: webhook host (default: 0.0.0.0).
- `webhookPath`: webhook path (default: /nextcloud-talk-webhook).
- `webhookPublicUrl`: externally reachable webhook URL.
- `dmPolicy`: `pairing | allowlist | open | disabled`.
- `allowFrom`: DM allowlist (user IDs). `open` requires `"*"`.
- `groupPolicy`: `allowlist | open | disabled`.
- `groupAllowFrom`: group allowlist (user IDs).
- `rooms`: per-room settings and allowlist.
- Static sender access groups can be referenced from `allowFrom` and `groupAllowFrom` with `accessGroup:<name>`.
- `historyLimit`: group history limit (0 disables).
- `dmHistoryLimit`: DM history limit (0 disables).
- `dms`: per-DM overrides (historyLimit).
- `textChunkLimit`: outbound text chunk size (chars).
- `chunkMode`: `length` (default) or `newline` to split on blank lines (paragraph boundaries) before length chunking.
- `blockStreaming`: disable block streaming for this channel.
- `blockStreamingCoalesce`: block streaming coalesce tuning.
- `mediaMaxMb`: inbound media cap (MB).

**Source**: OpenClaw documentation — `channels/nextcloud-talk` (mirror `inbox/openclaw_docs/channels/nextcloud-talk.md`)
**Last Updated**: 2026-06-22
**Status**: Active
