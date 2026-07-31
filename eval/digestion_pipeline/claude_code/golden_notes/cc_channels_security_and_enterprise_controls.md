---
tags:
  - resource
  - documentation
  - claude_code
  - channels
  - security
keywords:
  - channel sender allowlist
  - pairing bootstrap
  - channels opt-in gate
  - channelsenabled master switch
  - allowedchannelplugins restriction
  - managed settings
  - enterprise controls
  - deny by default channels
topics:
  - Claude Code
  - Channels
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/channels
access_control_group: ["general"]
---

# Channels — Security and Enterprise Controls

## Overview

A channel pushes external events (chat messages, webhooks, alerts) into a running Claude Code session, so the inbound side is an untrusted-text surface that must be gated. Security here is layered, deny-by-default: every approved channel plugin keeps a **sender allowlist** (only added IDs can push; everyone else is silently dropped), each session opts servers in with `--channels`, and an organization gates availability with two managed settings (`channelsEnabled`, `allowedChannelPlugins`). This note covers configuring those controls; the `--channels` opt-in and per-platform pairing are also touched in [`cc_channels_setup`](cc_channels_setup.md), and the build-your-own sender-gating code lives in [`cc_channel_permission_relay`](cc_channel_permission_relay.md).

## Who Can Push Messages — Sender Allowlist

Every approved channel plugin maintains a **sender allowlist**: only IDs you have added can push messages, and everyone else is silently dropped.

Telegram and Discord bootstrap the list by **pairing**:

1. Find your bot in Telegram or Discord and send it any message
2. The bot replies with a pairing code
3. In your Claude Code session, approve the code when prompted
4. Your sender ID is added to the allowlist

iMessage works differently: texting yourself bypasses the gate automatically, and you add other contacts by handle with `/imessage:access allow`.

## The `--channels` Opt-In Gate

On top of the sender allowlist, you control which servers are enabled each session with `--channels`, and your organization controls availability with `channelsEnabled` on claude.ai Team and Enterprise plans and on Console organizations that deploy managed settings.

Being in `.mcp.json` isn't enough to push messages: a server also has to be named in `--channels`. (The `.mcp.json` registration mechanics are owned by the MCP page — see https://code.claude.com/docs/en/mcp.)

The allowlist also gates [permission relay](https://code.claude.com/docs/en/channels-reference#relay-permission-prompts) if the channel declares it. Anyone who can reply through the channel can approve or deny tool use in your session, so only allowlist senders you trust with that authority (covered in [`cc_channel_permission_relay`](cc_channel_permission_relay.md)).

## Enterprise Controls

Admins control availability through two [managed settings](https://code.claude.com/docs/en/settings) that users cannot override. The default depends on how you authenticate:

* **claude.ai Team and Enterprise**: channels are blocked until an admin enables them.
* **Anthropic Console with API key authentication**: channels are permitted by default. You only need this setting if your organization deploys managed settings.

In all cases, no channel runs until a user opts it in for the session with `--channels`.

| Setting | Purpose | When not configured |
| :--- | :--- | :--- |
| `channelsEnabled` | Master switch. Must be `true` for any channel to deliver messages. Set via the claude.ai Admin console toggle or directly in managed settings. Blocks all channels including the development flag when off. | claude.ai Team and Enterprise: channels blocked. Console: channels allowed unless your organization deploys managed settings, in which case channels are blocked until this key is set |
| `allowedChannelPlugins` | Which plugins can register once channels are enabled. Replaces the Anthropic-maintained list when set. Only applies when `channelsEnabled` is `true`. | Anthropic default list applies |

Pro and Max users without an organization skip these checks entirely: channels are available and users opt in per session with `--channels`.

### Enable Channels for Your Organization

Admins can enable channels from **claude.ai → Admin settings → Claude Code → Channels**, or by setting `channelsEnabled` to `true` in managed settings.

Once enabled, users in your organization can use `--channels` to opt channel servers into individual sessions. If the setting is disabled or unset, the MCP server still connects and its tools work, but channel messages won't arrive. A startup warning tells the user to have an admin enable the setting.

### Restrict Which Channel Plugins Can Run

By default, any plugin on the Anthropic-maintained allowlist can register as a channel. Admins on Team and Enterprise plans can replace that allowlist with their own by setting `allowedChannelPlugins` in managed settings. Use this to restrict which official plugins are allowed, approve channels from your own internal marketplace, or both. Each entry names a plugin and the marketplace it comes from:

```json
{
  "channelsEnabled": true,
  "allowedChannelPlugins": [
    { "marketplace": "claude-plugins-official", "plugin": "telegram" },
    { "marketplace": "claude-plugins-official", "plugin": "discord" },
    { "marketplace": "acme-corp-plugins", "plugin": "internal-alerts" }
  ]
}
```

When `allowedChannelPlugins` is set, it replaces the Anthropic allowlist entirely: only the listed plugins can register. Leave it unset to fall back to the default Anthropic allowlist. An empty array blocks all channel plugins from the allowlist, but `--dangerously-load-development-channels` can still bypass it for local testing. To block channels entirely including the development flag, leave `channelsEnabled` unset instead.

This setting requires `channelsEnabled: true`. If a user passes a plugin to `--channels` that isn't on your list, Claude Code starts normally but the channel doesn't register, and the startup notice explains that the plugin isn't on the organization's approved list.

> The general managed-settings layering model (how these keys merge with user/project/enterprise settings) is owned by the Settings page (https://code.claude.com/docs/en/settings) and the managed-policy-settings reference. This note documents only the channel-specific keys.

**Source**: https://code.claude.com/docs/en/channels
**Last Updated**: 2026-06-13
**Status**: Active
