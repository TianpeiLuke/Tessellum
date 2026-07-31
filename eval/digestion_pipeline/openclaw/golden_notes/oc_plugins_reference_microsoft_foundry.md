---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - microsoft foundry plugin
  - "@openclaw/microsoft-foundry"
  - azure ai foundry provider
  - entra id az login auth
  - microsoft-foundry deployment model ref
  - openai-responses openai-completions
  - anthropic-messages canonicalModelId
  - mai image generation
  - mai-ds-r1 reasoning
  - imagegenerationproviders contract
topics:
  - OpenClaw
  - Plugins Reference
  - Microsoft Foundry Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/reference/microsoft-foundry
access_control_group: ["general"]
---

# OpenClaw — Configuring the Microsoft Foundry Provider Plugin

## Overview

This note is the configuration procedure for the OpenClaw **Microsoft Foundry** model-provider plugin (`@openclaw/microsoft-foundry`), mirroring the `plugins/reference/microsoft-foundry` reference card. It walks through the plugin's distribution and contract surface, the Azure/Foundry resource and authentication requirements (API-key or Entra ID via `az login`), how chat deployments are referenced and routed to the right OpenAI-compatible API shape, the special handling for Anthropic Claude deployments, MAI image generation (model refs, endpoints, constraints, and the json5 config block), and the troubleshooting cases. Every config key, env var, endpoint path, and model name below is copied verbatim from the source page.

## Distribution and Surface

The plugin is distributed as the package `@openclaw/microsoft-foundry` and its install route is **included in OpenClaw** (bundled, not a separate install). Its declared contract surface is `providers: microsoft-foundry; contracts: imageGenerationProviders`. Concretely it registers one image-generation provider — `microsoft-foundry` — alongside the chat-model provider, so the plugin contributes both a chat-model provider and an image-generation provider under the single `microsoft-foundry` provider id.

## Requirements

Before configuring the provider you need a **Microsoft Foundry or Azure AI Foundry resource with deployments**. Two authentication routes are supported:

- **API-key auth** — provide the key through the `AZURE_OPENAI_API_KEY` environment variable or a configured provider API key.
- **Entra ID auth** — install the Azure CLI and run `az login` before onboarding. OpenClaw refreshes Microsoft Foundry runtime tokens through `az account get-access-token`.

## Chat Models

Microsoft Foundry chat deployments are selected with the provider model ref `microsoft-foundry/<deployment-name>`. Onboarding discovers Foundry resources and deployments with the Azure CLI, then writes the selected deployment name to the model config. OpenClaw talks to the Foundry `/openai/v1` endpoint for supported OpenAI-compatible chat APIs, and chooses the API shape per model family:

- **`openai-responses` (default)** — the GPT, `o*`, `computer-use-preview`, and DeepSeek-V4 model families default to `openai-responses`.
- **`openai-completions`** — MAI-DS-R1 and other chat-completion deployments use `openai-completions` unless an explicit supported API is configured.
- **MAI-DS-R1 reasoning** — MAI-DS-R1 is recorded as reasoning-capable through reasoning content, **not** through `reasoning_effort`. Its context and output token metadata are 163,840 tokens.

### Anthropic Claude Deployments on Foundry

Anthropic Claude deployments in Microsoft Foundry use the **Anthropic Messages API shape**, not the OpenAI-compatible `/openai/v1` shape. Configure those as a custom `anthropic-messages` provider until the Microsoft Foundry plugin grows a native Anthropic runtime. When the Foundry deployment name differs from the Claude model ID, set `params.canonicalModelId` on the model entry so OpenClaw can apply model-specific wire contracts, map `/think off` correctly, and preserve signed thinking safely.

## MAI Image Generation

The plugin registers `microsoft-foundry` for `image_generate` with the current Microsoft AI image models: `MAI-Image-2.5-Flash`, `MAI-Image-2.5`, `MAI-Image-2e`, and `MAI-Image-2`. Use a deployed MAI image deployment name as the model ref. The provider does **not** declare a default image model because the MAI API requires your deployment name in the request `model` field. Configure the default image-generation model on `agents.defaults.imageGenerationModel`:

```json5
{
  agents: {
    defaults: {
      imageGenerationModel: {
        primary: "microsoft-foundry/<deployment-name>",
        timeoutMs: 600000,
      },
    },
  },
}
```

### Endpoints

Prompt-only generation calls Microsoft Foundry's MAI generations endpoint: `/mai/v1/images/generations`. Reference-image edits call `/mai/v1/images/edits` and are limited to `MAI-Image-2.5-Flash` and `MAI-Image-2.5` deployments. Prompt-only generation can use a custom deployment name with just the Foundry endpoint configured. For image edits with a custom deployment name, select the deployment through onboarding or include model metadata so OpenClaw can verify that the deployment is backed by `MAI-Image-2.5-Flash` or `MAI-Image-2.5`.

### MAI Image Constraints

- **Output:** one PNG image per request.
- **Size:** default `1024x1024`; both width and height must be at least 768 px.
- **Total pixels:** width × height must be at most 1,048,576.
- **Edits:** one PNG or JPEG input image.
- **Unsupported shared hints** such as `aspectRatio`, `resolution`, `quality`, `background`, and non-PNG `outputFormat` are not sent to Microsoft Foundry.

## Troubleshooting

- **`az: command not found`** — install the Azure CLI or use API-key auth.
- **`Microsoft Foundry endpoint missing for MAI image generation`** — select a Foundry deployment through onboarding or add `models.providers.microsoft-foundry.baseUrl`.
- **`supports MAI image deployments only`** — the selected image model points at a non-MAI deployment. Use a deployed MAI image model for `image_generate`.

**Source**: OpenClaw documentation — `plugins/reference/microsoft-foundry` (mirror `inbox/openclaw_docs/plugins/reference/microsoft-foundry.md`)
**Last Updated**: 2026-06-22
**Status**: Active
