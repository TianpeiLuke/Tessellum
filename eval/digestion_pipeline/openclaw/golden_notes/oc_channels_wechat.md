---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - wechat
keywords:
  - openclaw wechat channel
  - openclaw-weixin plugin
  - tencent weixin openclaw plugin
  - wechat qr login channel
  - wechat pairing access control
  - openclaw external channel plugin
  - wechat plugin compatibility
  - sidecar stale gateway cleanup
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/wechat
access_control_group: ["general"]
---

# OpenClaw — Connecting WeChat via the External `openclaw-weixin` Plugin

## Overview

This note is the procedure for connecting OpenClaw to **WeChat / Weixin** through Tencent's external `@tencent-weixin/openclaw-weixin` channel plugin, mirroring the `channels/wechat` source page. It walks the plugin-vs-core contract, install, QR login (including multi-account isolation), the pairing/allowlist access-control flow, version compatibility lines, the sidecar-process cleanup behavior, and the troubleshooting playbook. WeChat is an **external plugin**: OpenClaw core stays channel-agnostic and provides the generic channel-plugin contract, while the external plugin owns the WeChat-specific runtime. Per source, direct chats and media are supported; group chats are not advertised by the current plugin capability metadata.

## Naming

WeChat is the user-facing name in these docs; **Weixin** is the name used by Tencent's package and by the plugin id. The OpenClaw channel id is `openclaw-weixin`, and the npm package is `@tencent-weixin/openclaw-weixin`. Use `openclaw-weixin` in CLI commands and config paths.

## How it works

The WeChat code does not live in the OpenClaw core repo. OpenClaw provides the generic channel-plugin contract, and the external plugin provides the WeChat-specific runtime. The flow, per source, is:

1. `openclaw plugins install` installs `@tencent-weixin/openclaw-weixin`.
2. The Gateway discovers the plugin manifest and loads the plugin entrypoint.
3. The plugin registers channel id `openclaw-weixin`.
4. `openclaw channels login --channel openclaw-weixin` starts QR login.
5. The plugin stores account credentials under the OpenClaw state directory.
6. When the Gateway starts, the plugin starts its Weixin monitor for each configured account.
7. Inbound WeChat messages are normalized through the channel contract, routed to the selected OpenClaw agent, and sent back through the plugin outbound path.

That separation matters: OpenClaw core should stay channel-agnostic. WeChat login, Tencent iLink API calls, media upload/download, context tokens, and account monitoring are owned by the external plugin.

## Install

The quick install runs the plugin publisher's CLI installer:

```bash
npx -y @tencent-weixin/openclaw-weixin-cli install
```

The manual install pulls the package, enables it, then restarts the Gateway to load it:

```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin"
openclaw config set plugins.entries.openclaw-weixin.enabled true
openclaw gateway restart
```

## Login

Run QR login on the same machine that runs the Gateway, then scan the QR code with WeChat on your phone and confirm the login. The plugin saves the account token locally after a successful scan. To add another WeChat account, run the same login command again. For multiple accounts, isolate direct-message sessions by account, channel, and sender via `session.dmScope`:

```bash
openclaw channels login --channel openclaw-weixin
openclaw config set session.dmScope per-account-channel-peer
```

## Access control

Direct messages use the normal OpenClaw **pairing and allowlist model** for channel plugins. Approve new senders by listing pending pairing codes for the channel, then approving the desired `<CODE>`:

```bash
openclaw pairing list openclaw-weixin
openclaw pairing approve openclaw-weixin <CODE>
```

For the full access-control model, see Pairing (`/channels/pairing`).

## Compatibility

The plugin checks the host OpenClaw version at startup. Plugin lines map to OpenClaw version ranges and npm dist-tags as follows:

| Plugin line | OpenClaw version        | npm tag  |
| ----------- | ----------------------- | -------- |
| `2.x`       | `>=2026.3.22`           | `latest` |
| `1.x`       | `>=2026.1.0 <2026.3.22` | `legacy` |

If the plugin reports that your OpenClaw version is too old, either update OpenClaw or install the legacy plugin line with the `@legacy` dist-tag:

```bash
openclaw plugins install @tencent-weixin/openclaw-weixin@legacy
```

## Sidecar process

The WeChat plugin can run helper work beside the Gateway while it monitors the Tencent iLink API. In issue **#68451**, that helper path exposed a bug in OpenClaw's generic stale-Gateway cleanup: a child process could try to clean up the parent Gateway process, causing restart loops under process managers such as systemd. Current OpenClaw startup cleanup excludes the current process and its ancestors, so a channel helper must not kill the Gateway that launched it. This fix is generic; it is not a WeChat-specific path in core.

## Troubleshooting

Check install and status with the plugin list, a channel status probe, and the OpenClaw version. If the channel shows as installed but does not connect, confirm the plugin is enabled and restart. If the Gateway restarts repeatedly after enabling WeChat, force-reinstall the latest plugin and restart. As a last resort temporarily disable the plugin (`plugins.entries.openclaw-weixin.enabled false`) and restart. If startup reports that the installed plugin package `requires compiled runtime output for TypeScript entry`, the npm package was published without the compiled JavaScript runtime files OpenClaw needs — update/reinstall after the plugin publisher ships a fixed package, or temporarily disable/uninstall the plugin. The consolidated diagnostic and recovery commands are:

```bash
openclaw plugins list
openclaw channels status --probe
openclaw --version
npm view @tencent-weixin/openclaw-weixin version
openclaw plugins install "@tencent-weixin/openclaw-weixin" --force
openclaw config set plugins.entries.openclaw-weixin.enabled false
openclaw gateway restart
```

**Source**: OpenClaw documentation — `channels/wechat` (mirror `inbox/openclaw_docs/channels/wechat.md`)
**Last Updated**: 2026-06-22
**Status**: Active
