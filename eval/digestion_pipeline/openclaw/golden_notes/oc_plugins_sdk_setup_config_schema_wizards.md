---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk
keywords:
  - openclaw plugin config schema
  - buildChannelConfigSchema
  - buildJsonChannelConfigSchema
  - channelConfigs manifest
  - ChannelSetupWizard
  - setup wizard openclaw onboard
  - openclaw plugins install
  - clawhub install plugin
  - plugin-sdk channel-config-schema
topics:
  - OpenClaw
  - Plugin SDK Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-setup
access_control_group: ["general"]
---

# OpenClaw — Plugin Config Schemas, Setup Wizards, and Publishing/Installing

## Overview

This procedure note covers the second half of the OpenClaw plugin setup page (`plugins/sdk-setup`): how a plugin defines its **config schema**, builds an interactive **setup wizard** for `openclaw onboard`, and is **published and installed**. It documents how user config reaches a plugin (`api.pluginConfig` vs the `channels.<id>` section), how to convert a Zod or TypeBox schema into the `ChannelConfigSchema` wrapper via `buildChannelConfigSchema` / `buildJsonChannelConfigSchema`, how to mirror the generated JSON Schema into the manifest for cold-path inspection, the shape of a `ChannelSetupWizard` object and its shared/optional/binary-backed builder helpers, and the publish-then-install CLI flow (npm, ClawHub, and in-repo bundled plugins). The packaging metadata (`package.json` `openclaw` field), the `openclaw.plugin.json` manifest schema itself, ClawHub publish commands, and the `setup-entry.ts` setup entry are owned by the sibling packaging note — this note links to them rather than redefining them.

## Config schema

Plugin config is validated against the JSON Schema declared in the plugin's manifest. Users configure a plugin under the `plugins.entries.<id>.config` section of OpenClaw config:

```json5
{
  plugins: {
    entries: {
      "my-plugin": {
        config: {
          webhookSecret: "abc123",
        },
      },
    },
  },
}
```

A plugin receives this config object as `api.pluginConfig` during registration. For channel-specific config, use the channel config section (`channels.<id>`) instead of `plugins.entries`:

```json5
{
  channels: {
    "my-channel": {
      token: "bot-token",
      allowFrom: ["user1", "user2"],
    },
  },
}
```

### Building channel config schemas

Use `buildChannelConfigSchema` (from `openclaw/plugin-sdk/channel-config-schema`) to convert a Zod schema into the `ChannelConfigSchema` wrapper used by plugin-owned config artifacts:

```typescript
import { z } from "zod";
import { buildChannelConfigSchema } from "openclaw/plugin-sdk/channel-config-schema";

const accountSchema = z.object({
  token: z.string().optional(),
  allowFrom: z.array(z.string()).optional(),
  accounts: z.object({}).catchall(z.any()).optional(),
  defaultAccount: z.string().optional(),
});

const configSchema = buildChannelConfigSchema(accountSchema);
```

If you already author the contract as JSON Schema or `TypeBox`, use the direct helper `buildJsonChannelConfigSchema` (same subpath) so OpenClaw can skip Zod-to-JSON-Schema conversion on metadata paths — it accepts a `TypeBox` schema (`Type.Object(...)`) directly. For third-party plugins the cold-path contract is still the plugin manifest: mirror the generated JSON Schema into `openclaw.plugin.json#channelConfigs` so config-schema, setup, and UI surfaces can inspect `channels.<id>` without loading runtime code.

## Setup wizards

Channel plugins can provide an interactive setup wizard for `openclaw onboard`. The wizard is a `ChannelSetupWizard` object (typed via `openclaw/plugin-sdk/channel-setup`) attached to the `ChannelPlugin`:

```typescript
import type { ChannelSetupWizard } from "openclaw/plugin-sdk/channel-setup";

const setupWizard: ChannelSetupWizard = {
  channel: "my-channel",
  status: {
    configuredLabel: "Connected",
    unconfiguredLabel: "Not configured",
    resolveConfigured: ({ cfg }) => Boolean((cfg.channels as any)?.["my-channel"]?.token),
  },
  credentials: [
    {
      inputKey: "token",
      providerHint: "my-channel",
      credentialLabel: "Bot token",
      preferredEnvVar: "MY_CHANNEL_BOT_TOKEN",
      envPrompt: "Use MY_CHANNEL_BOT_TOKEN from environment?",
      keepPrompt: "Keep current token?",
      inputPrompt: "Enter your bot token:",
      inspect: ({ cfg, accountId }) => {
        const token = (cfg.channels as any)?.["my-channel"]?.token;
        return {
          accountConfigured: Boolean(token),
          hasConfiguredValue: Boolean(token),
        };
      },
    },
  ],
};
```

The `ChannelSetupWizard` type supports `credentials`, `textInputs`, `dmPolicy`, `allowFrom`, `groupAccess`, `prepare`, `finalize`, and more. The source points to bundled plugin packages (for example the Discord plugin `src/channel.setup.ts`) for full examples.

### Shared, optional, and binary-backed wizard helpers

Rather than hand-rolling repetitive wizard glue, the page documents shared builders. For DM allowlist prompts that only need the standard `note -> prompt -> parse -> merge -> patch` flow, prefer the shared setup helpers from `openclaw/plugin-sdk/setup`: `createPromptParsedAllowFromForAccount(...)`, `createTopLevelChannelParsedAllowFromPrompt(...)`, and `createNestedChannelParsedAllowFromPrompt(...)`. For channel setup status blocks that only vary by labels, scores, and optional extra lines, prefer `createStandardChannelSetupStatus(...)` from `openclaw/plugin-sdk/setup` instead of hand-rolling the same `status` object in each plugin.

For optional setup surfaces that should only appear in certain contexts, use `createOptionalChannelSetupSurface` from `openclaw/plugin-sdk/channel-setup`:

```typescript
import { createOptionalChannelSetupSurface } from "openclaw/plugin-sdk/channel-setup";

const setupSurface = createOptionalChannelSetupSurface({
  channel: "my-channel",
  label: "My Channel",
  npmSpec: "@myorg/openclaw-my-channel",
  docsPath: "/channels/my-channel",
});
// Returns { setupAdapter, setupWizard }
```

`plugin-sdk/channel-setup` also exposes the lower-level `createOptionalChannelSetupAdapter(...)` and `createOptionalChannelSetupWizard(...)` builders when you only need one half of that optional-install surface. The generated optional adapter/wizard fail closed on real config writes: they reuse one install-required message across `validateInput`, `applyAccountConfig`, and `finalize`, and append a docs link when `docsPath` is set.

For binary-backed setup UIs, prefer the shared delegated helpers instead of copying binary/status glue into every channel: `createDetectedBinaryStatus(...)` for status blocks that vary only by labels, hints, scores, and binary detection; `createCliPathTextInput(...)` for path-backed text inputs; `createDelegatedSetupWizardStatusResolvers(...)`, `createDelegatedPrepare(...)`, `createDelegatedFinalize(...)`, and `createDelegatedResolveConfigured(...)` when `setupEntry` needs to forward to a heavier full wizard lazily; and `createDelegatedTextInputShouldPrompt(...)` when `setupEntry` only needs to delegate a `textInputs[*].shouldPrompt` decision.

## Publishing and installing

**External plugins:** publish to ClawHub (see the packaging/ClawHub publishing note), then install. The page documents three install spec forms via `openclaw plugins install` — a bare package spec (installs from npm during the launch cutover), an explicit `clawhub:` spec, and an explicit `npm:` spec used when a package has not moved to ClawHub yet or when a direct npm install path is needed during migration:

```bash
openclaw plugins install @myorg/openclaw-my-plugin
openclaw plugins install clawhub:@myorg/openclaw-my-plugin
openclaw plugins install npm:@myorg/openclaw-my-plugin
```

**In-repo plugins:** place the plugin under the bundled plugin workspace tree and it is automatically discovered during build. Users install any plugin with `openclaw plugins install <package-name>`.

For npm-sourced installs, `openclaw plugins install` installs the package into a per-plugin project under `~/.openclaw/npm/projects` with lifecycle scripts disabled — so plugin authors should keep plugin dependency trees pure JS/TS and avoid packages that require `postinstall` builds. Gateway startup does NOT install plugin dependencies: npm/git/ClawHub install flows own dependency convergence, and local plugins must already have their dependencies installed. Bundled package metadata is explicit (not inferred from built JavaScript at gateway startup); runtime dependencies belong in the plugin package that owns them, and packaged OpenClaw startup never repairs or mirrors plugin dependencies.

**Source**: OpenClaw documentation — `plugins/sdk-setup` (mirror `inbox/openclaw_docs/plugins/sdk-setup.md`), Config schema + Setup wizards + Publishing and installing sections
**Last Updated**: 2026-06-22
**Status**: Active
