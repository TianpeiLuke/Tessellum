---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - nostr
keywords:
  - openclaw nostr channel
  - nostr dm bot
  - nip-04 encrypted dms
  - nostr private key nsec
  - nostr relays wss
  - nostr dm policy allowlist
  - strfry local relay testing
topics:
  - OpenClaw
  - Nostr Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/nostr
access_control_group: ["general"]
---

# OpenClaw — Connecting the Nostr DM Channel

## Overview

This note is the operator procedure for running OpenClaw as a **Nostr** bot — a decentralized social-networking protocol — so the gateway can receive and respond to encrypted direct messages (DMs) over NIP-04. It mirrors the `channels/nostr` source page end to end: installing the bundled plugin (and older/custom-install fallbacks), interactive vs non-interactive key setup, the configuration reference, NIP-01 profile metadata, DM-policy/allowlist access control, accepted key formats, relay configuration, supported NIPs, testing against a local `strfry` relay, troubleshooting, security guidance, and the MVP limitations. The channel is an **optional bundled plugin, disabled by default until configured**.

## Bundled plugin

Current OpenClaw releases ship Nostr as a bundled plugin, so normal packaged builds do not need a separate install.

### Older / custom installs

For older builds, onboarding (`openclaw onboard`) and `openclaw channels add` still surface Nostr from the shared channel catalog. If your build excludes bundled Nostr, install the npm package directly (use the bare package to follow the current official release tag; pin an exact version only when you need a reproducible install) or, for dev workflows, install from a local checkout:

```bash
openclaw plugins install @openclaw/nostr
openclaw plugins install --link <path-to-local-nostr-plugin>
```

**Restart the Gateway** after installing or enabling plugins.

## Quick setup

The interactive flow is four steps: (1) generate a Nostr keypair if needed (`nak key generate` using the `nak` tool); (2) add the channel to config (the json5 block below); (3) export the key; (4) restart the Gateway. The shell commands for steps 1 and 3, plus the **non-interactive** `openclaw channels add` alternative, are shown together below:

```bash
# 1. Generate a keypair (using nak)
nak key generate
# 3. Export the key, then restart the Gateway
export NOSTR_PRIVATE_KEY="nsec1..."
# Non-interactive setup (alternative to editing config; --use-env keeps the key in env, not config)
openclaw channels add --channel nostr --private-key "$NOSTR_PRIVATE_KEY"
openclaw channels add --channel nostr --private-key "$NOSTR_PRIVATE_KEY" --relay-urls "wss://relay.damus.io,wss://relay.primal.net"
```

```json5
// 2. Add to config
{
  channels: {
    nostr: {
      privateKey: "${NOSTR_PRIVATE_KEY}",
    },
  },
}
```

## Configuration reference

The `channels.nostr` config keys, types, and defaults are reproduced verbatim from source:

| Key          | Type     | Default                                     | Description                         |
| ------------ | -------- | ------------------------------------------- | ----------------------------------- |
| `privateKey` | string   | required                                    | Private key in `nsec` or hex format |
| `relays`     | string[] | `['wss://relay.damus.io', 'wss://nos.lol']` | Relay URLs (WebSocket)              |
| `dmPolicy`   | string   | `pairing`                                   | DM access policy                    |
| `allowFrom`  | string[] | `[]`                                        | Allowed sender pubkeys              |
| `enabled`    | boolean  | `true`                                      | Enable/disable channel              |
| `name`       | string   | -                                           | Display name                        |
| `profile`    | object   | -                                           | NIP-01 profile metadata             |

## Profile metadata

Profile data is published as a NIP-01 `kind:0` event. You can manage it from the Control UI (Channels -> Nostr -> Profile) or set it directly in the `profile` config object, which carries the standard Nostr profile fields (`name`, `displayName`, `about`, `picture`, `banner`, `website`, `nip05`, `lud16`).

```json5
{
  channels: {
    nostr: {
      privateKey: "${NOSTR_PRIVATE_KEY}",
      profile: {
        name: "openclaw",
        displayName: "OpenClaw",
        about: "Personal assistant DM bot",
        picture: "https://example.com/avatar.png",
        banner: "https://example.com/banner.png",
        website: "https://example.com",
        nip05: "openclaw@example.com",
        lud16: "openclaw@example.com",
      },
    },
  },
}
```

Notes: profile URLs must use `https://`; importing from relays merges fields and preserves local overrides.

## Access control

### DM policies

The `dmPolicy` key selects the inbound-DM access posture (default `pairing`):

- **pairing** (default): unknown senders get a pairing code.
- **allowlist**: only pubkeys listed in `allowFrom` can DM.
- **open**: public inbound DMs (requires `allowFrom: ["*"]`).
- **disabled**: ignore inbound DMs.

Enforcement order: inbound event signatures are verified **before** sender policy and NIP-04 decryption, so forged events are rejected early; pairing replies are sent without processing the original DM body; and inbound DMs are rate-limited while oversized payloads are dropped before decrypt.

### Allowlist example

```json5
{
  channels: {
    nostr: {
      privateKey: "${NOSTR_PRIVATE_KEY}",
      dmPolicy: "allowlist",
      allowFrom: ["npub1abc...", "npub1xyz..."],
    },
  },
}
```

## Key formats

Accepted formats are: **private key** as `nsec...` or 64-char hex; **pubkeys** (in `allowFrom`) as `npub...` or hex.

## Relays

The default relays are `relay.damus.io` and `nos.lol`. Relays are WebSocket (`wss://`) endpoints, configured via the `relays` array:

```json5
{
  channels: {
    nostr: {
      privateKey: "${NOSTR_PRIVATE_KEY}",
      relays: ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nostr.wine"],
    },
  },
}
```

Tips: use 2-3 relays for redundancy; avoid too many relays (latency, duplication); paid relays can improve reliability; local relays are fine for testing (`ws://localhost:7777`).

## Protocol support

The channel's supported and planned NIPs (verbatim from source):

| NIP    | Status    | Description                           |
| ------ | --------- | ------------------------------------- |
| NIP-01 | Supported | Basic event format + profile metadata |
| NIP-04 | Supported | Encrypted DMs (`kind:4`)              |
| NIP-17 | Planned   | Gift-wrapped DMs                      |
| NIP-44 | Planned   | Versioned encryption                  |

## Testing

### Local relay

Start a local `strfry` relay in Docker with `docker run -p 7777:7777 ghcr.io/hoytech/strfry`, then point the channel at it by setting `relays: ["ws://localhost:7777"]` in the `channels.nostr` config.

### Manual test

1. Note the bot pubkey (npub) from logs.
2. Open a Nostr client (Damus, Amethyst, etc.).
3. DM the bot pubkey.
4. Verify the response.

## Troubleshooting

**Not receiving messages:** verify the private key is valid; ensure relay URLs are reachable and use `wss://` (or `ws://` for local); confirm `enabled` is not `false`; check Gateway logs for relay connection errors.

**Not sending responses:** check that the relay accepts writes; verify outbound connectivity; watch for relay rate limits.

**Duplicate responses:** expected when using multiple relays — messages are deduplicated by event ID, and only the first delivery triggers a response.

## Security

Never commit private keys; use environment variables for keys; consider `allowlist` for production bots. Signatures are verified before sender policy, and sender policy is enforced before decrypt, so forged events are rejected early and unknown senders cannot force full crypto work.

## Limitations (MVP)

- Direct messages only (no group chats).
- No media attachments.
- NIP-04 only (NIP-17 gift-wrap planned).

**Source**: OpenClaw documentation — `channels/nostr` (mirror `inbox/openclaw_docs/channels/nostr.md`)
**Last Updated**: 2026-06-22
**Status**: Active
