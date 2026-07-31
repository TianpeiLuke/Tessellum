---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - whatsapp
keywords:
  - openclaw whatsapp setup
  - whatsapp baileys channel install
  - whatsapp dmpolicy grouppolicy
  - whatsapp pairing allowlist
  - whatsapp qr login channels login
  - whatsapp mention activation gating
  - whatsapp pluginhooks messagereceived privacy
  - whatsapp dedicated number self-chat
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/whatsapp
access_control_group: ["general"]
---

# OpenClaw — WhatsApp Channel Setup, Access Control, and Activation

## Overview

This note is the onboarding procedure for the OpenClaw **WhatsApp** channel (production-ready via WhatsApp Web / Baileys, with the Gateway owning the linked session). It covers the on-demand plugin install, the four-step QR quick setup, the dedicated- vs personal-number deployment patterns, the DM and group access policies plus mention/activation gating, the opt-in plugin-hook privacy gate, and the self-chat safeguards. It mirrors the **Install (on demand)**, **Quick setup**, **Deployment patterns**, **Access control and activation**, **Plugin hooks and privacy**, and **Personal-number and self-chat behavior** sections of the `channels/whatsapp` source page. The WhatsApp runtime/delivery behavior model lives in `oc_channels_whatsapp_runtime_delivery`, and ACP bindings, multi-account credentials, troubleshooting, and the config reference live in `oc_channels_whatsapp_operations`.

## Install (on demand)

The WhatsApp runtime is distributed outside the core OpenClaw npm package so WhatsApp-specific runtime dependencies stay with the external plugin, and it installs on demand the first time you select the channel. Onboarding (`openclaw onboard`) and `openclaw channels add --channel whatsapp` prompt to install the WhatsApp plugin the first time you select it; `openclaw channels login --channel whatsapp` also offers the install flow when the plugin is not present yet. On a dev channel + git checkout the install defaults to the local plugin path, while Stable/Beta installs the official `@openclaw/whatsapp` plugin from ClawHub first, with npm as the fallback.

Manual install stays available:

```bash
openclaw plugins install clawhub:@openclaw/whatsapp
```

Use the bare npm package (`@openclaw/whatsapp`) only when you need the registry fallback. Pin an exact version only when you need a reproducible install.

## Quick setup

The four-step quick setup is: (1) configure the WhatsApp access policy, (2) link WhatsApp via QR, (3) start the gateway, and (4) approve the first pairing request if using pairing mode.

Step 1 — configure WhatsApp access policy (JSON5):

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      allowFrom: ["+15551234567"],
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
}
```

Step 2 — link WhatsApp (QR-based) and start the gateway:

```bash
openclaw channels login --channel whatsapp
openclaw channels login --channel whatsapp --account work
openclaw channels add --channel whatsapp --account work --auth-dir /path/to/wa-auth
openclaw gateway
```

Current login is QR-based. In remote or headless environments, ensure a reliable path to deliver the live QR code to the phone that will scan it before starting login; the second command logs in a specific account, and `channels add ... --auth-dir` attaches an existing/custom WhatsApp Web auth directory before login.

Step 4 — approve the first pairing request (pairing mode):

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

Pairing requests expire after 1 hour, and pending requests are capped at 3 per channel. OpenClaw recommends running WhatsApp on a separate number when possible (the channel metadata and setup flow are optimized for that, but personal-number setups are also supported). The current setup flow is QR-only: terminal-rendered QRs, screenshots, PDFs, or chat attachments can expire or become unreadable while being relayed from a remote machine, so for remote/headless hosts prefer a direct QR image handoff path over manual terminal capture.

## Deployment patterns

There are two operational deployment shapes plus a note on channel scope. The **dedicated number (recommended)** mode is the cleanest operationally — a separate WhatsApp identity for OpenClaw, clearer DM allowlists and routing boundaries, and a lower chance of self-chat confusion. Its minimal policy pattern uses `dmPolicy: "allowlist"` with `allowFrom`.

The **personal-number fallback** is supported: onboarding writes a self-chat-friendly baseline of `dmPolicy: "allowlist"`, an `allowFrom` that includes your personal number, and `selfChatMode: true`; at runtime, self-chat protections key off the linked self number and `allowFrom`. On **channel scope**, the messaging platform channel is WhatsApp Web-based (`Baileys`) in the current OpenClaw channel architecture, and there is no separate Twilio WhatsApp messaging channel in the built-in chat-channel registry.

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

## Access control and activation

Access control spans three configurable layers: DM policy, group policy + allowlists, and mention/activation gating.

**DM policy.** `channels.whatsapp.dmPolicy` controls direct chat access with four values: `pairing` (default), `allowlist`, `open` (requires `allowFrom` to include `"*"`), and `disabled`. `allowFrom` accepts E.164-style numbers (normalized internally) and is a DM sender access-control list — it does NOT gate explicit outbound sends to WhatsApp group JIDs or `@newsletter` channel JIDs. A multi-account override `channels.whatsapp.accounts.<id>.dmPolicy` (and `allowFrom`) takes precedence over channel-level defaults for that account. Runtime behavior: pairings are persisted in the channel allow-store and merged with configured `allowFrom`; scheduled automation and heartbeat recipient fallback use explicit delivery targets or configured `allowFrom` (DM pairing approvals are not implicit cron or heartbeat recipients); if no allowlist is configured, the linked self number is allowed by default; and OpenClaw never auto-pairs outbound `fromMe` DMs (messages you send to yourself from the linked device).

**Group policy + allowlists.** Group access has two layers. First is the **group membership allowlist** (`channels.whatsapp.groups`): if `groups` is omitted, all groups are eligible; if `groups` is present, it acts as a group allowlist (`"*"` allowed). Second is the **group sender policy** (`channels.whatsapp.groupPolicy` + `groupAllowFrom`): `open` bypasses the sender allowlist, `allowlist` requires the sender to match `groupAllowFrom` (or `*`), and `disabled` blocks all group inbound. For the sender allowlist fallback, if `groupAllowFrom` is unset, runtime falls back to `allowFrom` when available, and sender allowlists are evaluated before mention/reply activation. If no `channels.whatsapp` block exists at all, the runtime group-policy fallback is `allowlist` (with a warning log), even if `channels.defaults.groupPolicy` is set.

**Mentions + activation.** Group replies require a mention by default. Mention detection includes explicit WhatsApp mentions of the bot identity, configured mention regex patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`), inbound voice-note transcripts for authorized group messages, and implicit reply-to-bot detection (reply sender matches bot identity). As a security note, a quote/reply only satisfies mention gating — it does NOT grant sender authorization, so with `groupPolicy: "allowlist"` non-allowlisted senders are still blocked even if they reply to an allowlisted user's message. The session-level activation command `/activation mention` or `/activation always` updates session state (not global config) and is owner-gated.

## Plugin hooks and privacy

WhatsApp inbound messages can contain personal message content, phone numbers, group identifiers, sender names, and session correlation fields. For that reason, WhatsApp does NOT broadcast inbound `message_received` hook payloads to plugins unless you explicitly opt in — a data-minimization default for untrusted plugins.

```json5
{
  channels: {
    whatsapp: {
      pluginHooks: {
        messageReceived: true,
      },
    },
  },
}
```

You can scope the opt-in to one account by setting `pluginHooks.messageReceived: true` under `channels.whatsapp.accounts.<id>` instead of at the channel level. Only enable this for plugins you trust to receive inbound WhatsApp message content and identifiers.

## Personal-number and self-chat behavior

When the linked self number is also present in `allowFrom`, WhatsApp self-chat safeguards activate: read receipts are skipped for self-chat turns; the mention-JID auto-trigger behavior that would otherwise ping yourself is ignored; and if `messages.responsePrefix` is unset, self-chat replies default to `[{identity.name}]` or `[openclaw]`.

**Source**: OpenClaw documentation — `channels/whatsapp` (mirror `inbox/openclaw_docs/channels/whatsapp.md`)
**Last Updated**: 2026-06-22
**Status**: Active
