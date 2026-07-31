---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - testing
keywords:
  - openclaw plugin testing
  - plugin-sdk test subpaths
  - createTestPluginApi
  - loader-backed smoke test
  - channel provider contract tests
  - describePluginRegistrationContract
  - mock plugin runtime store
  - pnpm test vitest coverage
  - lint enforcement plugin imports
topics:
  - OpenClaw
  - Plugin Testing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-testing
access_control_group: ["general"]
---

# OpenClaw — Testing Plugins (SDK Test Utilities, Patterns, and Lint Enforcement)

## Overview

This note is the procedure for testing OpenClaw plugins, mirroring the `plugins/sdk-testing` source page. It covers the repo-local `openclaw/plugin-sdk/*` test-helper subpaths and their exported helpers, how to resolve which test target you are exercising, the concrete testing patterns (registration smoke tests, runtime-config access, channel and provider unit tests, runtime mocking, per-instance stubs), the in-repo contract-test suites and how to scope them, the three lint rules enforced by `pnpm check`, and the Vitest test configuration. The how-to guides referenced from the source's Tip — Channel plugin tests and Provider plugin tests — carry the full worked test examples; this note documents the utilities and patterns that back them.

## Test utilities

The test-helper subpaths are **repo-local source entrypoints for OpenClaw's own bundled plugin tests**. They are NOT package exports for third-party plugins, and they may import Vitest or other repo-only test dependencies. The named imports are: `openclaw/plugin-sdk/plugin-test-api` (Plugin API mock), `openclaw/plugin-sdk/agent-runtime-test-contracts` (Agent runtime contract), `openclaw/plugin-sdk/channel-contract-testing` (Channel contract), `openclaw/plugin-sdk/channel-test-helpers` (Channel test helper), `openclaw/plugin-sdk/channel-target-testing` (Channel target test), `openclaw/plugin-sdk/plugin-test-contracts` (Plugin contract), `openclaw/plugin-sdk/plugin-test-runtime` (Plugin runtime test), `openclaw/plugin-sdk/provider-test-contracts` (Provider contract), `openclaw/plugin-sdk/provider-http-test-mocks` (Provider HTTP mock), `openclaw/plugin-sdk/test-env` (Environment/network test), `openclaw/plugin-sdk/test-fixtures` (Generic fixture), and `openclaw/plugin-sdk/test-node-mocks` (Node builtin mock).

Inside the OpenClaw repo, **prefer the focused subpaths** above for new bundled plugin tests. The broad `openclaw/plugin-sdk/testing` barrel is legacy compatibility only. Repo guardrails reject new real imports from `plugin-sdk/testing` and `plugin-sdk/test-utils`; those names remain only as deprecated compatibility surfaces for compatibility-record tests. A representative import block from the focused subpaths:

```typescript
import {
  shouldAckReaction,
  removeAckReactionAfterReply,
} from "openclaw/plugin-sdk/channel-feedback";
import { installCommonResolveTargetErrorCases } from "openclaw/plugin-sdk/channel-target-testing";
import { AUTH_PROFILE_RUNTIME_CONTRACT } from "openclaw/plugin-sdk/agent-runtime-test-contracts";
import { createTestPluginApi } from "openclaw/plugin-sdk/plugin-test-api";
import { expectChannelInboundContextContract } from "openclaw/plugin-sdk/channel-contract-testing";
import { createStartAccountContext } from "openclaw/plugin-sdk/channel-test-helpers";
import { describePluginRegistrationContract } from "openclaw/plugin-sdk/plugin-test-contracts";
import { registerSingleProviderPlugin } from "openclaw/plugin-sdk/plugin-test-runtime";
import { describeOpenAIProviderRuntimeContract } from "openclaw/plugin-sdk/provider-test-contracts";
import { getProviderHttpMocks } from "openclaw/plugin-sdk/provider-http-test-mocks";
import { withEnv, withFetchPreconnect, withServer } from "openclaw/plugin-sdk/test-env";
import {
  bundledPluginRoot,
  createCliRuntimeCapture,
  typedCases,
} from "openclaw/plugin-sdk/test-fixtures";
import { mockNodeBuiltinModule } from "openclaw/plugin-sdk/test-node-mocks";
```

### Available exports

Key exports and the subpath each lives on (verbatim from the source's Available exports table): `createTestPluginApi` (`plugin-test-api`) builds a minimal plugin API mock for direct registration unit tests. `AUTH_PROFILE_RUNTIME_CONTRACT`, `DELIVERY_NO_REPLY_RUNTIME_CONTRACT`, `OUTCOME_FALLBACK_RUNTIME_CONTRACT`, and `createParameterFreeTool` (`agent-runtime-test-contracts`) are shared native-agent-runtime contract fixtures (auth-profile, delivery-suppression, fallback-classification, and dynamic-tool schema fixtures). `expectChannelInboundContextContract` and `installChannelOutboundPayloadContractSuite` (`channel-contract-testing`) assert channel inbound context shape and install outbound payload contract cases. From `channel-test-helpers`: `createStartAccountContext`, `installChannelActionsContractSuite`, `installChannelSetupContractSuite`, `installChannelStatusContractSuite`, `expectDirectoryIds`, `assertBundledChannelEntries`, `formatEnvelopeTimestamp`, and `expectPairingReplyText` build account lifecycle contexts and install generic channel message-action / setup / status contract cases.

For plugin and provider registration: `describePluginRegistrationContract` (`plugin-test-contracts`) installs plugin registration contract checks; from `plugin-test-runtime`, `registerSingleProviderPlugin` registers one provider plugin in loader smoke tests, `registerProviderPlugin` captures all provider kinds from one plugin, `registerProviderPlugins` captures registrations across multiple plugins, `requireRegisteredProvider` asserts a provider collection contains an id, `createRuntimeEnv` builds a mocked CLI/plugin runtime environment, and `createPluginSetupWizardStatus` builds setup status helpers. From `provider-test-contracts`: `describeOpenAIProviderRuntimeContract` installs provider-family runtime contract checks, `expectPassthroughReplayPolicy` asserts provider replay policies pass through provider-owned tools and metadata, `runRealtimeSttLiveTest` / `normalizeTranscriptForMatch` run a live realtime STT test with shared audio fixtures and normalize transcripts, and `expectExplicitVideoGenerationCapabilities` / `expectExplicitMusicGenerationCapabilities` / `mockSuccessfulDashscopeVideoTask` assert explicit media-generation capabilities. `getProviderHttpMocks` and `installProviderHttpMockCleanup` (`provider-http-test-mocks`) access and reset opt-in provider HTTP/auth Vitest mocks.

Environment/fixture helpers: from `test-env`, `withServer` runs tests against a disposable local HTTP server, `createMockIncomingRequest` / `createMockServerResponse` build minimal HTTP request/response objects, `withFetchPreconnect` installs preconnect hooks, `withEnv` / `withEnvAsync` temporarily patch environment variables, `createTempHomeEnv` / `withTempHome` / `withTempDir` create isolated filesystem fixtures, `createRequestCaptureJsonFetch` captures JSON fetch requests, and `useFrozenTime` / `useRealTime` freeze and restore timers. From `test-fixtures`: `createCliRuntimeCapture` captures CLI runtime output, `importFreshModule` imports an ESM module with a fresh query token to bypass the module cache, `bundledPluginRoot` / `bundledPluginFile` resolve bundled plugin source/dist fixture paths, and `typedCases` preserves literal types for table-driven tests (also `createSandboxTestContext`, `writeSkill`, `makeAgentAssistantMessage`, `peekSystemEvents` / `resetSystemEventsForTest`, `sanitizeTerminalText`, `countLines` / `hasBalancedFences`). `mockNodeBuiltinModule` (`test-node-mocks`) installs narrow Node builtin Vitest mocks. `createTestRegistry`, `createEmptyPluginRegistry`, and `setActivePluginRegistry` are importable from either `plugin-test-runtime` or `channel-test-helpers`. `installCommonResolveTargetErrorCases` is on `channel-target-testing`; `shouldAckReaction` / `removeAckReactionAfterReply` are on `channel-feedback`.

Bundled-plugin contract suites also use SDK testing subpaths for test-only registry, manifest, public-artifact, and runtime fixture helpers. **Core-only suites that depend on bundled OpenClaw inventory stay under `src/plugins/contracts`.** Keep new extension tests on a documented focused SDK subpath (e.g., `plugin-sdk/plugin-test-api`, `plugin-sdk/channel-contract-testing`, `plugin-sdk/agent-runtime-test-contracts`, `plugin-sdk/channel-test-helpers`, `plugin-sdk/plugin-test-contracts`, `plugin-sdk/plugin-test-runtime`, `plugin-sdk/provider-test-contracts`, `plugin-sdk/provider-http-test-mocks`, `plugin-sdk/test-env`, or `plugin-sdk/test-fixtures`) rather than importing the broad `plugin-sdk/testing` barrel, repo `src/**` files, or repo `test/helpers/*` bridges directly.

### Types

Focused testing subpaths also re-export TypeScript types useful in test files: `ChannelAccountSnapshot` and `ChannelGatewayContext` from `openclaw/plugin-sdk/channel-contract`, `OpenClawConfig` from `openclaw/plugin-sdk/config-contracts`, and `MockFn`, `PluginRuntime`, and `RuntimeEnv` from `openclaw/plugin-sdk/plugin-test-runtime` (all imported as `import type`).

## Testing target resolution

Use `installCommonResolveTargetErrorCases` from `openclaw/plugin-sdk/channel-target-testing` to add standard error cases for channel target resolution, then add your own channel-specific `it(...)` cases:

```typescript
import { describe } from "vitest";
import { installCommonResolveTargetErrorCases } from "openclaw/plugin-sdk/channel-target-testing";

describe("my-channel target resolution", () => {
  installCommonResolveTargetErrorCases({
    resolveTarget: ({ to, mode, allowFrom }) => {
      // Your channel's target resolution logic
      return myChannelResolveTarget({ to, mode, allowFrom });
    },
    implicitAllowFrom: ["user1", "user2"],
  });

  // Add channel-specific test cases
  it("should resolve @username targets", () => {
    // ...
  });
});
```

## Testing patterns

### Testing registration contracts

Unit tests that pass a hand-written `api` mock to `register(api)` do NOT exercise OpenClaw's loader acceptance gates. **Add at least one loader-backed smoke test for each registration surface your plugin depends on**, especially hooks and exclusive capabilities such as memory. The real loader fails plugin registration when required metadata is missing or a plugin calls a capability API it does not own — for example, `api.registerHook(...)` requires a hook name, and `api.registerMemoryCapability(...)` requires the plugin manifest or exported entry to declare `kind: "memory"`.

### Testing runtime config access

Prefer the shared plugin runtime mock from `openclaw/plugin-sdk/channel-test-helpers` when testing bundled channel plugins. Its deprecated `runtime.config.loadConfig()` and `runtime.config.writeConfigFile(...)` mocks **throw by default** so tests catch new usage of compatibility APIs; override those mocks only when the test is explicitly covering legacy compatibility behavior.

### Unit testing a channel plugin

Channel unit tests assert config-driven account resolution and that inspection does not materialize secrets (note `inspection` exposes `configured`/`tokenStatus` but no `token`):

```typescript
import { describe, it, expect, vi } from "vitest";

describe("my-channel plugin", () => {
  it("should resolve account from config", () => {
    const cfg = {
      channels: {
        "my-channel": {
          token: "test-token",
          allowFrom: ["user1"],
        },
      },
    };

    const account = myPlugin.setup.resolveAccount(cfg, undefined);
    expect(account.token).toBe("test-token");
  });

  it("should inspect account without materializing secrets", () => {
    const cfg = {
      channels: {
        "my-channel": { token: "test-token" },
      },
    };

    const inspection = myPlugin.setup.inspectAccount(cfg, undefined);
    expect(inspection.configured).toBe(true);
    expect(inspection.tokenStatus).toBe("available");
    // No token value exposed
    expect(inspection).not.toHaveProperty("token");
  });
});
```

### Unit testing a provider plugin

Provider unit tests assert dynamic model resolution and catalog behavior when an API key is available (the catalog `run` receives a `resolveProviderApiKey` injection):

```typescript
import { describe, it, expect } from "vitest";

describe("my-provider plugin", () => {
  it("should resolve dynamic models", () => {
    const model = myProvider.resolveDynamicModel({
      modelId: "custom-model-v2",
      // ... context
    });

    expect(model.id).toBe("custom-model-v2");
    expect(model.provider).toBe("my-provider");
    expect(model.api).toBe("openai-completions");
  });

  it("should return catalog when API key is available", async () => {
    const result = await myProvider.catalog.run({
      resolveProviderApiKey: () => ({ apiKey: "test-key" }),
      // ... context
    });

    expect(result?.provider?.models).toHaveLength(2);
  });
});
```

### Mocking the plugin runtime

For code that uses `createPluginRuntimeStore`, mock the runtime in tests: build the store with a `pluginId` and `errorMessage`, `store.setRuntime(mockRuntime)` in test setup with `vi.fn()` namespace mocks, and `store.clearRuntime()` after tests. The mocked runtime supplies `agent` (e.g. `resolveAgentDir`) and `config` (`current`, `mutateConfigFile`, `replaceConfigFile`) namespaces, cast `as unknown as PluginRuntime`. (Imports come from `openclaw/plugin-sdk/runtime-store`.) *(inferred from source code block — the store helper lives on the `runtime-store` subpath.)*

### Testing with per-instance stubs

**Prefer per-instance stubs over prototype mutation** — assign a `vi.fn()` to a method on a single client instance (`client.sendMessage = vi.fn().mockResolvedValue(...)`) rather than mutating `MyChannelClient.prototype.sendMessage`, so the stub does not leak across instances or tests.

## Contract tests (in-repo plugins)

Bundled plugins have contract tests that verify registration ownership; run the whole suite with `pnpm test -- src/plugins/contracts/`. These tests assert which plugins register which providers, which plugins register which speech providers, registration shape correctness, and runtime contract compliance.

### Running scoped tests

Scope by plugin with `pnpm test -- <bundled-plugin-root>/my-channel/`, or run specific contract files:

```bash
pnpm test -- src/plugins/contracts/shape.contract.test.ts
pnpm test -- src/plugins/contracts/auth-choice.contract.test.ts
pnpm test -- src/plugins/contracts/runtime-seams.contract.test.ts
```

## Lint enforcement (in-repo plugins)

Three rules are enforced by `pnpm check` for in-repo plugins: (1) **No monolithic root imports** — the `openclaw/plugin-sdk` root barrel is rejected; (2) **No direct `src/` imports** — plugins cannot import `../../src/` directly; (3) **No self-imports** — plugins cannot import their own `plugin-sdk/<name>` subpath. External plugins are not subject to these lint rules, but following the same patterns is recommended.

## Test configuration

OpenClaw uses Vitest with V8 coverage thresholds. Run all tests with `pnpm test`; scope to a file with `pnpm test -- <bundled-plugin-root>/my-channel/src/channel.test.ts`; filter by test name with `-t "resolves account"`; and run coverage with `pnpm test:coverage`. If local runs cause memory pressure, cap the worker count:

```bash
OPENCLAW_VITEST_MAX_WORKERS=1 pnpm test
```

**Source**: OpenClaw documentation — `plugins/sdk-testing` (mirror `inbox/openclaw_docs/plugins/sdk-testing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
