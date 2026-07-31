---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - capabilities
keywords:
  - openclaw adding capabilities
  - capability vs plugin
  - typed core contract
  - registerImageGenerationProvider
  - runtime.imageGeneration.generate
  - embeddingProviders contract
  - provider and harness seams
  - capability file checklist
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/adding-capabilities
access_control_group: ["general"]
---

# OpenClaw — Adding a New Capability (Contributor Guide)

## Overview

This note is the OpenClaw **contributor procedure** for adding a brand-new shared capability — a domain such as embeddings, image generation, or video generation — across the provider and harness seams, mirroring the `plugins/adding-capabilities` source page. It is written for OpenClaw core developers (external-plugin authors use the building-plugins tutorial; the deep reference is the architecture page). The guiding rule is two-sided: a **plugin** is an ownership boundary, while a **capability** is a shared core contract — so you never wire a vendor directly into a channel or tool, you start by defining the capability. The note covers when to create a capability, the standard 7-step implementation sequence, what goes where (core vs vendor vs feature/channel), the provider/harness seam decision, the file checklist, the worked image-generation example, the embedding-providers contract, and the pre-ship review checklist.

## When to Create a Capability

Create a new capability when use it for a new shared domain that OpenClaw needs (such as embeddings, image generation, video generation, or some future vendor-backed feature area), and when **all** of these are true:

1. More than one vendor could plausibly implement it.
2. Channels, tools, or feature plugins should consume it without caring about the vendor.
3. Core needs to own fallback, policy, config, or delivery behavior.

If the work is vendor-only and no shared contract exists yet, stop and define the contract first. The rule stated up front: **plugin** = ownership boundary; **capability** = shared core contract. Do not start by wiring a vendor directly into a channel or a tool — start by defining the capability.

## The Standard Sequence

The standard sequence for adding a capability is seven ordered steps:

1. Define the typed core contract.
2. Add plugin registration for that contract.
3. Add a shared runtime helper.
4. Wire one real vendor plugin as proof.
5. Move feature/channel consumers onto the runtime helper.
6. Add contract tests.
7. Document the operator-facing config and ownership model.

## What Goes Where

Each layer owns a distinct slice of the implementation. **Core** owns: request/response types; the provider registry + resolution; fallback behavior; the config schema (with propagated `title` / `description` docs metadata on nested object, wildcard, array-item, and composition nodes); and the runtime helper surface. **Vendor plugin** owns: vendor API calls; vendor auth handling; vendor-specific request normalization; and registration of the capability implementation. **Feature/channel plugin** owns only the consumer side: it calls `api.runtime.*` or the matching `plugin-sdk/*-runtime` helper, and it **never** calls a vendor implementation directly.

## Provider and Harness Seams

Two extension seams exist, and the choice depends on where the behavior belongs. Use **provider hooks** when the behavior belongs to the model provider contract rather than the generic agent loop — examples include provider-specific request params after transport selection, auth-profile preference, prompt overlays, and follow-up fallback routing after model/profile failover. Use **agent harness hooks** when the behavior belongs to the runtime that is executing a turn — harnesses can classify explicit protocol outcomes such as empty output, reasoning without visible output, or a structured plan without a final answer, so the outer model fallback policy can make the retry decision.

Keep both seams narrow:

- Core owns the retry/fallback policy.
- Provider plugins own provider-specific request/auth/routing hints.
- Harness plugins own runtime-specific attempt classification.
- Third-party plugins return hints, not direct mutations of core state.

## File Checklist

For a new capability, expect to touch these areas:

```
src/<capability>/types.ts
src/<capability>/...registry/runtime.ts
src/plugins/types.ts
src/plugins/registry.ts
src/plugins/captured-registration.ts
src/plugins/contracts/registry.ts
src/plugins/runtime/types-core.ts
src/plugins/runtime/index.ts
src/plugin-sdk/<capability>.ts
src/plugin-sdk/<capability>-runtime.ts
```

Plus one or more bundled plugin packages, and the config, docs, and tests.

## Worked Example: Image Generation

Image generation follows the standard shape:

1. Core defines `ImageGenerationProvider`.
2. Core exposes `registerImageGenerationProvider(...)`.
3. Core exposes `runtime.imageGeneration.generate(...)`.
4. The `openai`, `google`, `fal`, and `minimax` plugins register vendor-backed implementations.
5. Future vendors register the same contract without changing channels/tools.

The config key is intentionally separate from vision-analysis routing: `agents.defaults.imageModel` analyzes images, while `agents.defaults.imageGenerationModel` generates images. Keep those separate so fallback and policy remain explicit.

## Embedding Providers

Use `embeddingProviders` for reusable vector embedding providers. This contract is intentionally broader than memory: tools, search, retrieval, importers, or future feature plugins can consume embeddings without depending on the memory engine. Memory search can consume generic `embeddingProviders`. The older `memoryEmbeddingProviders` contract is deprecated compatibility while existing memory-specific providers migrate; new reusable embedding providers should use `embeddingProviders`.

## Review Checklist

Before shipping a new capability, verify:

- No channel/tool imports vendor code directly.
- The runtime helper is the shared path.
- At least one contract test asserts bundled ownership.
- Config docs name the new model/config key.
- Plugin docs explain the ownership boundary.

If a PR skips the capability layer and hardcodes vendor behavior into a channel/tool, send it back and define the contract first.

**Source**: OpenClaw documentation — `plugins/adding-capabilities` (mirror `inbox/openclaw_docs/plugins/adding-capabilities.md`)
**Last Updated**: 2026-06-22
**Status**: Active
