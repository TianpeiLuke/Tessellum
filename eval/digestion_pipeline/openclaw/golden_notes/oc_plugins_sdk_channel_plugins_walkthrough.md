---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - channels
keywords:
  - openclaw channel plugin walkthrough
  - createChatChannelPlugin
  - defineChannelPluginEntry
  - defineSetupPluginEntry
  - channel plugin package manifest
  - registerHttpRoute inbound webhook
  - channel plugin file structure
  - openclaw channel authoring steps
topics:
  - OpenClaw
  - Channel Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-channel-plugins
access_control_group: ["general"]
---

# OpenClaw — Channel Plugin Authoring Walkthrough

## Overview

This note is the step-by-step procedure for building an OpenClaw messaging channel plugin, mirroring the **Walkthrough**, **File structure**, **Advanced topics**, and **Next steps** sections of the `plugins/sdk-channel-plugins` source page. It walks through six steps — package & manifest, building the channel plugin object with `createChatChannelPlugin`, wiring the entry point with `defineChannelPluginEntry`, adding a setup entry with `defineSetupPluginEntry`, handling inbound messages via an HTTP webhook route, and testing — using the page's running `acme-chat` example. By the end you have a working channel with DM security, pairing, reply threading, and outbound messaging. The conceptual model (how channel plugins work, approvals/capabilities, inbound mention policy) is documented separately in `oc_plugins_sdk_channel_plugins_concepts.md`; prerequisite package structure lives in the Getting Started page (`/plugins/building-plugins`), and this walkthrough realizes that concept.

## Walkthrough

The walkthrough is a six-step `<Steps>` sequence. Each step builds one file of the bundled `acme-chat` example plugin.

### Step 1 — Package and manifest

Create the standard plugin files. The `channel` field in `package.json` is what makes this a channel plugin. The two files are `package.json` (the `openclaw` package field with `extensions`, `setupEntry`, and the `channel` metadata block) and `openclaw.plugin.json` (the manifest carrying `configSchema` and `channelConfigs`). For the full package-metadata surface, the source links to Plugin Setup and Config (`/plugins/sdk-setup#openclaw-channel`).

```json package.json
{
  "name": "@myorg/openclaw-acme-chat",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "setupEntry": "./setup-entry.ts",
    "channel": {
      "id": "acme-chat",
      "label": "Acme Chat",
      "blurb": "Connect OpenClaw to Acme Chat."
    }
  }
}
```

```json openclaw.plugin.json
{
  "id": "acme-chat",
  "kind": "channel",
  "channels": ["acme-chat"],
  "name": "Acme Chat",
  "description": "Acme Chat channel plugin",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  },
  "channelConfigs": {
    "acme-chat": {
      "schema": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "token": { "type": "string" },
          "allowFrom": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "uiHints": {
        "token": {
          "label": "Bot token",
          "sensitive": true
        }
      }
    }
  }
}
```

Per the source, `configSchema` validates `plugins.entries.acme-chat.config` and is used for plugin-owned settings that are not the channel account config. `channelConfigs` validates `channels.acme-chat` and is the cold-path source used by config schema, setup, and UI surfaces before the plugin runtime loads.

### Step 2 — Build the channel plugin object

The `ChannelPlugin` interface has many optional adapter surfaces. The source instructs you to start with the minimum — `id` and `setup` — and add adapters as you need them. Create `src/channel.ts` and build the plugin with `createChatChannelPlugin` (from `openclaw/plugin-sdk/channel-core`), passing a `base` produced by `createChannelPluginBase` plus declarative `security`, `pairing`, `threading`, and `outbound` options. The example resolves the account from `cfg.channels["acme-chat"]`, throwing `"acme-chat: token is required"` when the token is missing.

```typescript src/channel.ts
import {
  createChatChannelPlugin,
  createChannelPluginBase,
} from "openclaw/plugin-sdk/channel-core";
import type { OpenClawConfig } from "openclaw/plugin-sdk/channel-core";
import { acmeChatApi } from "./client.js"; // your platform API client

export const acmeChatPlugin = createChatChannelPlugin<ResolvedAccount>({
  base: createChannelPluginBase({
    id: "acme-chat",
    setup: { resolveAccount, inspectAccount /* ... */ },
  }),

  // DM security: who can message the bot
  security: {
    dm: {
      channelKey: "acme-chat",
      resolvePolicy: (account) => account.dmPolicy,
      resolveAllowFrom: (account) => account.allowFrom,
      defaultPolicy: "allowlist",
    },
  },

  // Pairing: approval flow for new DM contacts
  pairing: {
    text: {
      idLabel: "Acme Chat username",
      message: "Send this code to verify your identity:",
      notify: async ({ target, code }) => {
        await acmeChatApi.sendDm(target, `Pairing code: ${code}`);
      },
    },
  },

  // Threading: how replies are delivered
  threading: { topLevelReplyToMode: "reply" },

  // Outbound: send messages to the platform
  outbound: {
    attachedResults: {
      sendText: async (params) => {
        const result = await acmeChatApi.sendMessage(params.to, params.text);
        return { messageId: result.id };
      },
    },
    base: {
      sendMedia: async (params) => {
        await acmeChatApi.sendFile(params.to, params.filePath);
      },
    },
  },
});
```

For channels that accept both canonical top-level DM keys and legacy nested keys, the source says to use the helpers from `plugin-sdk/channel-config-helpers` — `resolveChannelDmAccess`, `resolveChannelDmPolicy`, `resolveChannelDmAllowFrom`, and `normalizeChannelDmPolicy` keep account-local values ahead of inherited root values; pair the same resolver with doctor repair through `normalizeLegacyDmAliases` so runtime and migration read the same contract. The page's "What `createChatChannelPlugin` does for you" accordion explains that instead of implementing low-level adapter interfaces manually you pass declarative options and the builder composes them: `security.dm` → scoped DM security resolver from config fields; `pairing.text` → text-based DM pairing flow with code exchange; `threading` → reply-to-mode resolver (fixed, account-scoped, or custom); `outbound.attachedResults` → send functions that return result metadata (message IDs). You can also pass raw adapter objects instead of the declarative options for full control; raw outbound adapters may define a `chunker(text, limit, ctx)` function whose optional `ctx.formatting` carries delivery-time formatting decisions such as `maxLinesPerMessage` (apply before sending so chunk boundaries are resolved once by shared outbound delivery), and send contexts include `replyToIdSource` (`implicit` or `explicit`) when a native reply target was resolved.

### Step 3 — Wire the entry point

Create `index.ts` exporting a default `defineChannelPluginEntry` (from `openclaw/plugin-sdk/channel-core`). The entry carries `id`, `name`, `description`, the `plugin` object from Step 2, an optional `registerCliMetadata(api)`, and `registerFull(api)`.

```typescript index.ts
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/channel-core";
import { acmeChatPlugin } from "./src/channel.js";

export default defineChannelPluginEntry({
  id: "acme-chat",
  name: "Acme Chat",
  description: "Acme Chat channel plugin",
  plugin: acmeChatPlugin,
  registerCliMetadata(api) {
    api.registerCli(
      ({ program }) => {
        program.command("acme-chat").description("Acme Chat management");
      },
      {
        descriptors: [
          { name: "acme-chat", description: "Acme Chat management", hasSubcommands: false },
        ],
      },
    );
  },
  registerFull(api) {
    api.registerGatewayMethod(/* ... */);
  },
});
```

The source directs you to put channel-owned CLI descriptors in `registerCliMetadata(...)` so OpenClaw can show them in root help without activating the full channel runtime, while normal full loads still pick up the same descriptors for real command registration; keep `registerFull(...)` for runtime-only work. If `registerFull(...)` registers gateway RPC methods, use a plugin-specific prefix — the core admin namespaces `config.*`, `exec.approvals.*`, `wizard.*`, and `update.*` stay reserved and always resolve to `operator.admin`. `defineChannelPluginEntry` handles the registration-mode split automatically; the page links Entry Points (`/plugins/sdk-entrypoints#definechannelpluginentry`) for all options.

### Step 4 — Add a setup entry

Create `setup-entry.ts` for lightweight loading during onboarding. The whole file is one line — it imports `defineSetupPluginEntry` from `openclaw/plugin-sdk/channel-core` and the `acmeChatPlugin` from `./src/channel.js`, then `export default defineSetupPluginEntry(acmeChatPlugin);`. OpenClaw loads this instead of the full entry when the channel is disabled or unconfigured, avoiding pulling in heavy runtime code during setup flows. The page links Setup and Config (`/plugins/sdk-setup#setup-entry`) for details.

Per the source, bundled workspace channels that split setup-safe exports into sidecar modules can use `defineBundledChannelSetupEntry(...)` from `openclaw/plugin-sdk/channel-entry-contract` when they also need an explicit setup-time runtime setter.

### Step 5 — Handle inbound messages

Your plugin needs to receive messages from the platform and forward them to OpenClaw. The typical pattern is a webhook that verifies the request and dispatches it through your channel's inbound handler, registered from `registerFull(api)` via `api.registerHttpRoute`. The route uses `auth: "plugin"` (plugin-managed auth — verify signatures yourself).

```typescript
registerFull(api) {
  api.registerHttpRoute({
    path: "/acme-chat/webhook",
    auth: "plugin", // plugin-managed auth (verify signatures yourself)
    handler: async (req, res) => {
      const event = parseWebhookPayload(req);

      // Your inbound handler dispatches the message to OpenClaw.
      // The exact wiring depends on your platform SDK -
      // see a real example in the bundled Microsoft Teams or Google Chat plugin package.
      await handleAcmeChatInbound(api, event);

      res.statusCode = 200;
      res.end("ok");
      return true;
    },
  });
}
```

The source notes that inbound message handling is channel-specific — each channel plugin owns its own inbound pipeline — and points you to bundled channel plugins (for example the Microsoft Teams or Google Chat plugin package) for real patterns.

### Step 6 — Test

Write colocated tests in `src/channel.test.ts`. The page uses `vitest` and tests three behaviors against the `acme-chat` plugin: it resolves the account from config (asserting `account.token` is `"test-token"`), it inspects an account without materializing secrets (asserting `result.configured` is `true` and `result.tokenStatus` is `"available"`), and it reports missing config (asserting `result.configured` is `false` for empty `channels`). The example invokes `acmeChatPlugin.setup!.resolveAccount(cfg, undefined)` and `acmeChatPlugin.setup!.inspectAccount!(cfg, undefined)` directly. Run the tests with the bundled-plugin path:

```bash
pnpm test -- <bundled-plugin-root>/acme-chat/
```

For shared test helpers, the source links Testing (`/plugins/sdk-testing`).

## File structure

The walkthrough closes with the canonical channel-plugin layout under `<bundled-plugin-root>/acme-chat/`, where `package.json` holds the `openclaw.channel` metadata, `openclaw.plugin.json` holds the manifest with config schema, `index.ts` is the `defineChannelPluginEntry`, `setup-entry.ts` is the `defineSetupPluginEntry`, optional `api.ts`/`runtime-api.ts` hold public/internal exports, and `src/` holds `channel.ts` (the `ChannelPlugin` via `createChatChannelPlugin`), `channel.test.ts` (tests), `client.ts` (platform API client), and `runtime.ts` (runtime store, if needed).

## Advanced topics

The source surfaces a `<CardGroup>` of follow-on references beyond the basic walkthrough: **Threading options** (fixed, account-scoped, or custom reply modes — `/plugins/sdk-entrypoints#registration-mode`); **Message tool integration** (`describeMessageTool` and action discovery — `/plugins/architecture#channel-plugins-and-the-shared-message-tool`); **Target resolution** (`inferTargetChatType`, `looksLikeId`, `resolveTarget` — `/plugins/architecture-internals#channel-target-resolution`); **Runtime helpers** (TTS, STT, media, subagent via `api.runtime` — `/plugins/sdk-runtime`); and **Channel inbound API** (the shared inbound event lifecycle: ingest, resolve, record, dispatch, finalize — `/plugins/sdk-channel-inbound`). The page adds a note that some bundled helper seams still exist for bundled-plugin maintenance and compatibility but are not the recommended pattern for new channel plugins — prefer the generic channel/setup/reply/runtime subpaths from the common SDK surface unless you are maintaining that bundled plugin family directly.

## Next steps

The page's closing "Next steps" links are: Provider Plugins (`/plugins/sdk-provider-plugins`) — if your plugin also provides models; SDK Overview (`/plugins/sdk-overview`) — full subpath import reference; SDK Testing (`/plugins/sdk-testing`) — test utilities and contract tests; and Plugin Manifest (`/plugins/manifest`) — full manifest schema.

**Source**: OpenClaw documentation — `plugins/sdk-channel-plugins` (mirror `inbox/openclaw_docs/plugins/sdk-channel-plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
