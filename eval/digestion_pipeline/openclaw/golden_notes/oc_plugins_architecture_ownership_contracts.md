---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - capability_ownership
keywords:
  - openclaw capability ownership
  - plugin ownership boundary
  - capability contract enforcement
  - capability layering core vendor channel
  - multi-capability company plugin
  - native plugin execution model not sandboxed
  - openclaw plugin export boundary
  - duplicate provider id enforcement
topics:
  - OpenClaw
  - Plugin Capability Ownership
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/architecture
access_control_group: ["general"]
---

# OpenClaw — Plugin Capability Ownership, Contracts, and Execution Model

## Overview

This note covers the governance half of the OpenClaw plugin `architecture` page: how capabilities are OWNED, CONTRACTED, EXECUTED, and EXPORTED — the rules that decide which plugin may own which surface and where plugin code is allowed to run. It mirrors `plugins/architecture.md` from the "Capability ownership model" section through "Internals and reference", picking up where the companion concept note (the public capability model and plugin shapes) leaves off. The central distinction it formalizes is **plugin = ownership boundary** versus **capability = core contract that multiple plugins can implement or consume** — and the practical consequences of that distinction for layering, enforcement, in-process trust, and the public SDK export surface.

## Capability Ownership Model

OpenClaw treats a native plugin as the ownership boundary for a **company** or a **feature**, not as a grab bag of unrelated integrations. The page states three ownership norms: a company plugin should usually own all of that company's OpenClaw-facing surfaces; a feature plugin should usually own the full feature surface it introduces; and channels should consume shared core capabilities instead of re-implementing provider behavior ad hoc. The page gives three worked ownership shapes: **vendor multi-capability** — `openai` owns text inference, speech, realtime voice, media understanding, and image generation, `google` owns text inference plus media understanding, image generation, and web search, and `qwen` owns text inference plus media understanding and video generation; **vendor single-capability** — `elevenlabs` and `microsoft` own speech, `firecrawl` owns web-fetch, and `minimax` / `mistral` / `moonshot` / `zai` own media-understanding backends; and **feature plugin** — `voice-call` owns call transport, tools, CLI, routes, and Twilio media-stream bridging, but consumes shared speech, realtime transcription, and realtime voice capabilities instead of importing vendor plugins directly.

The intended end state is that OpenAI lives in one plugin even if it spans text models, speech, images, and future video; another vendor can do the same for its own surface area; and channels do not care which vendor plugin owns the provider because they consume the shared capability contract exposed by core. The key distinction is stated explicitly: **plugin = ownership boundary** and **capability = core contract that multiple plugins can implement or consume**. So if OpenClaw adds a new domain such as video, the first question is not "which provider should hardcode video handling?" — it is "what is the core video capability contract?" Once that contract exists, vendor plugins can register against it and channel/feature plugins can consume it.

When the capability does not exist yet, the page prescribes a four-step sequence: (1) **Define the capability** in core; (2) **Expose it through the SDK** — the plugin API/runtime in a typed way; (3) **Wire consumers** — channels/features against that capability; (4) **Vendor implementations** — let vendor plugins register implementations. This keeps ownership explicit while avoiding core behavior that depends on a single vendor or a one-off plugin-specific code path.

### Capability Layering

The page gives a three-layer mental model for deciding where code belongs. The **Core capability layer** holds shared orchestration, policy, fallback, config merge rules, delivery semantics, and typed contracts. The **Vendor plugin layer** holds vendor-specific APIs, auth, model catalogs, speech synthesis, image generation, future video backends, and usage endpoints. The **Channel/feature plugin layer** holds Slack/Discord/voice-call/etc. integration that consumes core capabilities and presents them on a surface. TTS is given as the canonical example of this shape: core owns reply-time TTS policy, fallback order, prefs, and channel delivery; `openai`, `elevenlabs`, and `microsoft` own synthesis implementations; and `voice-call` consumes the telephony TTS runtime helper. The page states the same pattern should be preferred for future capabilities.

### Multi-Capability Company Plugin

A company plugin should feel cohesive from the outside. The page notes that if OpenClaw has shared contracts for models, speech, realtime transcription, realtime voice, media understanding, image generation, video generation, web fetch, and web search, a vendor can own all of its surfaces in one place. The illustrative `exampleai` plugin registers a text provider, a speech provider, a media-understanding provider (capabilities `["image", "audio", "video"]`), and a web-search provider in one `register(api)` body:

```ts
import type { OpenClawPluginDefinition } from "openclaw/plugin-sdk/plugin-entry";
import {
  describeImageWithModel,
  transcribeOpenAiCompatibleAudio,
} from "openclaw/plugin-sdk/media-understanding";

const plugin: OpenClawPluginDefinition = {
  id: "exampleai",
  name: "ExampleAI",
  register(api) {
    api.registerProvider({
      id: "exampleai",
      // auth/model catalog/runtime hooks
    });

    api.registerSpeechProvider({
      id: "exampleai",
      // vendor speech config — implement the SpeechProviderPlugin interface directly
    });

    api.registerMediaUnderstandingProvider({
      id: "exampleai",
      capabilities: ["image", "audio", "video"],
      async describeImage(req) {
        return describeImageWithModel({
          provider: "exampleai",
          model: req.model,
          input: req.input,
        });
      },
      async transcribeAudio(req) {
        return transcribeOpenAiCompatibleAudio({
          provider: "exampleai",
          model: req.model,
          input: req.input,
        });
      },
    });

    api.registerWebSearchProvider(
      createPluginBackedWebSearchProvider({
        id: "exampleai-search",
        // credential + fetch logic
      }),
    );
  },
};

export default plugin;
```

The page stresses that the exact helper names do not matter — the shape matters: one plugin owns the vendor surface, core still owns the capability contracts, channels and feature plugins consume `api.runtime.*` helpers (not vendor code), and contract tests can assert that the plugin registered the capabilities it claims to own.

### Capability Example: Video Understanding

OpenClaw already treats image/audio/video understanding as one shared capability, and the same ownership model applies there in three steps: core defines the media-understanding contract; vendor plugins register `describeImage`, `transcribeAudio`, and `describeVideo` as applicable; and channels and feature plugins consume the shared core behavior instead of wiring directly to vendor code. The page notes this avoids baking one provider's video assumptions into core — the plugin owns the vendor surface; core owns the capability contract and fallback behavior. Video *generation* already uses that same sequence: core owns the typed capability contract and runtime helper, and vendor plugins register `api.registerVideoGenerationProvider(...)` implementations against it.

## Contracts and Enforcement

The plugin API surface is intentionally typed and centralized in `OpenClawPluginApi`. That contract defines the supported registration points and the runtime helpers a plugin may rely on. The page lists why this matters: plugin authors get one stable internal standard; core can reject duplicate ownership such as two plugins registering the same provider id; startup can surface actionable diagnostics for malformed registration; and contract tests can enforce bundled-plugin ownership and prevent silent drift.

There are two layers of enforcement. **Runtime registration enforcement** — the plugin registry validates registrations as plugins load, so duplicate provider ids, duplicate speech provider ids, and malformed registrations produce plugin diagnostics instead of undefined behavior. **Contract tests** — bundled plugins are captured in contract registries during test runs so OpenClaw can assert ownership explicitly; today this is used for model providers, speech providers, web search providers, and bundled registration ownership. The practical effect is that OpenClaw knows, up front, which plugin owns which surface, which lets core and channels compose seamlessly because ownership is declared, typed, and testable rather than implicit.

### What Belongs in a Contract

The page contrasts good and bad contracts. **Good contracts** are typed, small, capability-specific, owned by core, reusable by multiple plugins, and consumable by channels/features without vendor knowledge. **Bad contracts** are vendor-specific policy hidden in core, one-off plugin escape hatches that bypass the registry, channel code reaching straight into a vendor implementation, or ad hoc runtime objects that are not part of `OpenClawPluginApi` or `api.runtime`. The guiding rule: when in doubt, raise the abstraction level — define the capability first, then let plugins plug into it.

## Execution Model

Native OpenClaw plugins run **in-process** with the Gateway. They are **not sandboxed** — a loaded native plugin has the same process-level trust boundary as core code. The page spells out the implications: a plugin can register tools, network handlers, hooks, and services; a plugin bug can crash or destabilize the gateway; and a malicious native plugin is equivalent to arbitrary code execution inside the OpenClaw process. By contrast, compatible bundles are safer by default because OpenClaw currently treats them as metadata/content packs — in current releases that mostly means bundled skills.

The page recommends using allowlists and explicit install/load paths for non-bundled plugins, and treating workspace plugins as development-time code rather than production defaults. For bundled workspace package names, the plugin id should stay anchored in the npm name: `@openclaw/<id>` by default, or an approved typed suffix such as `-provider`, `-plugin`, `-speech`, `-sandbox`, or `-media-understanding` when the package intentionally exposes a narrower plugin role. A trust note clarifies that `plugins.allow` trusts **plugin ids**, not source provenance: a workspace plugin with the same id as a bundled plugin intentionally shadows the bundled copy when that workspace plugin is enabled/allowlisted (normal and useful for local development, patch testing, and hotfixes). Bundled-plugin trust is resolved from the source snapshot — the manifest and code on disk at load time — rather than from install metadata, so a corrupted or substituted install record cannot silently widen a bundled plugin's trust surface beyond what the actual source claims.

## Export Boundary

OpenClaw exports capabilities, not implementation convenience. The page directs authors to keep capability registration public while trimming non-contract helper exports: bundled-plugin-specific helper subpaths, runtime plumbing subpaths not intended as public API, vendor-specific convenience helpers, and setup/onboarding helpers that are implementation details. Reserved bundled-plugin helper subpaths have been retired from the generated SDK export map. The rule is to keep owner-specific helpers inside the owning plugin package and promote only reusable host behavior to generic SDK contracts such as `plugin-sdk/gateway-runtime`, `plugin-sdk/security-runtime`, and `plugin-sdk/plugin-config-runtime`.

## Internals and Reference

For the load pipeline, registry model, provider runtime hooks, Gateway HTTP routes, message tool schemas, channel target resolution, provider catalogs, context engine plugins, and the guide to adding a new capability, the page defers to *Plugin architecture internals* — the deeper reference digested in this series as the `oc_plugins_architecture_internals_*` notes (load/registry, runtime hooks, and gateway/SDK reference).

**Source**: OpenClaw documentation — `plugins/architecture` (mirror `inbox/openclaw_docs/plugins/architecture.md`, "Capability ownership model" → "Internals and reference")
**Last Updated**: 2026-06-22
**Status**: Active
