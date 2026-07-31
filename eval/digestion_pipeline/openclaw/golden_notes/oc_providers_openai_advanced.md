---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - openai
keywords:
  - openai advanced configuration
  - azure openai endpoints openclaw
  - websocket sse transport auto
  - fast mode service_tier priority
  - responses server-side compaction
  - strict-agentic gpt mode
  - native vs openai-compatible routes
  - azure deployment name api-version
topics:
  - OpenClaw
  - OpenAI Provider
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/openai
access_control_group: ["general"]
---

# OpenClaw — OpenAI Advanced Tuning (Azure, Transport, Compaction, Strict-Agentic)

## Overview

This note covers the advanced operational tuning of OpenClaw's bundled `openai` provider, mirroring the **Azure OpenAI endpoints** and **Advanced configuration** sections of the `providers/openai` source page. It documents how to route image generation through an Azure OpenAI resource (host detection, `api-version`, deployment-name rule, regions, parameter differences), and the six advanced accordions: WebSocket-vs-SSE transport, fast mode, `service_tier` priority processing, Responses server-side compaction, the strict-agentic GPT execution contract, and how OpenClaw shapes requests differently on native vs OpenAI-compatible proxy routes. Provider auth/runtime selection lives in `oc_providers_openai_auth` and media generation in `oc_providers_openai_media` (linked below); this note is the transport/compaction/Azure tuning slice.

## Azure OpenAI endpoints

The bundled `openai` provider can target an Azure OpenAI resource for **image generation** by overriding the base URL. On the image-generation path, OpenClaw detects Azure hostnames on `models.providers.openai.baseUrl` and switches to Azure's request shape automatically. Realtime voice uses a separate configuration path (`plugins.entries.voice-call.config.realtime.providers.openai.azureEndpoint`) and is NOT affected by `models.providers.openai.baseUrl` — that Azure surface is documented in the media note's Realtime voice section. Choose Azure OpenAI when you already have an Azure OpenAI subscription/quota/enterprise agreement, need regional data residency or compliance controls, or want to keep traffic inside an existing Azure tenancy.

### Configuration

For Azure image generation through the bundled `openai` provider, point `models.providers.openai.baseUrl` at your Azure resource and set `apiKey` to the Azure OpenAI key (NOT an OpenAI Platform key):

```json5
{
  models: {
    providers: {
      openai: {
        baseUrl: "https://<your-resource>.openai.azure.com",
        apiKey: "<azure-openai-api-key>",
      },
    },
  },
}
```

OpenClaw recognizes these Azure host suffixes for the Azure image-generation route: `*.openai.azure.com`, `*.services.ai.azure.com`, and `*.cognitiveservices.azure.com`. For image-generation requests on a recognized Azure host, OpenClaw sends the `api-key` header instead of `Authorization: Bearer`, uses deployment-scoped paths (`/openai/deployments/{deployment}/...`), appends `?api-version=...` to each request, and uses a 600s default request timeout for Azure image-generation calls (per-call `timeoutMs` values still override this default). Other base URLs (public OpenAI, OpenAI-compatible proxies) keep the standard OpenAI image request shape. Azure routing for the `openai` provider's image-generation path requires OpenClaw 2026.4.22 or later; earlier versions treat any custom `openai.baseUrl` like the public OpenAI endpoint and will fail against Azure image deployments.

### API version

Set `AZURE_OPENAI_API_VERSION` to pin a specific Azure preview or GA version for the Azure image-generation path. The default is `2024-12-01-preview` when the variable is unset:

```bash
export AZURE_OPENAI_API_VERSION="2024-12-01-preview"
```

### Model names are deployment names

Azure OpenAI binds models to deployments. For Azure image-generation requests routed through the bundled `openai` provider, the `model` field in OpenClaw must be the **Azure deployment name** you configured in the Azure portal, NOT the public OpenAI model id. If you create a deployment called `gpt-image-2-prod` that serves `gpt-image-2`, call the tool with the deployment name — e.g. `/tool image_generate model=openai/gpt-image-2-prod prompt="A clean poster" size=1024x1024 count=1`. The same deployment-name rule applies to image-generation calls routed through the bundled `openai` provider.

### Regional availability

Azure image generation is currently available only in a subset of regions (for example `eastus2`, `swedencentral`, `polandcentral`, `westus3`, `uaenorth`). Check Microsoft's current region list before creating a deployment, and confirm the specific model is offered in your region.

### Parameter differences

Azure OpenAI and public OpenAI do not always accept the same image parameters. Azure may reject options that public OpenAI allows (for example certain `background` values on `gpt-image-2`) or expose them only on specific model versions. These differences come from Azure and the underlying model, not OpenClaw. If an Azure request fails with a validation error, check the parameter set supported by your specific deployment and API version in the Azure portal. Azure OpenAI uses native transport and compat behavior but does NOT receive OpenClaw's hidden attribution headers (see Native vs OpenAI-compatible routes below). For chat or Responses traffic on Azure (beyond image generation), use the onboarding flow or a dedicated Azure provider config — `openai.baseUrl` alone does not pick up the Azure API/auth shape; a separate `azure-openai-responses/*` provider exists (see Server-side compaction below).

## Advanced configuration

### Transport (WebSocket vs SSE)

OpenClaw uses WebSocket-first with SSE fallback (`"auto"`) for `openai/*`. In `"auto"` mode, OpenClaw retries one early WebSocket failure before falling back to SSE; after a failure, marks WebSocket as degraded for ~60 seconds and uses SSE during cool-down; attaches stable session and turn identity headers for retries and reconnects; and normalizes usage counters (`input_tokens` / `prompt_tokens`) across transport variants. The supported `transport` values are `"auto"` (default — WebSocket first, SSE fallback), `"sse"` (force SSE only), and `"websocket"` (force WebSocket only). All three of the per-model tuning knobs in this and the next two sections (`transport`, `fastMode`, `serviceTier`) live under the same `params` object, shown combined here:

```json5
{
  agents: {
    defaults: {
      models: {
        "openai/gpt-5.5": {
          params: { transport: "auto", fastMode: true, serviceTier: "priority" },
        },
      },
    },
  },
}
```

### Fast mode

OpenClaw exposes a shared fast-mode toggle for `openai/*`, controllable via chat/UI (`/fast status|on|off`) or config (`agents.defaults.models["<provider>/<model>"].params.fastMode`). When enabled, OpenClaw maps fast mode to OpenAI priority processing (`service_tier = "priority"`). Existing `service_tier` values are preserved, and fast mode does not rewrite `reasoning` or `text.verbosity`. Session overrides win over config — clearing the session override in the Sessions UI returns the session to the configured default. The `params.fastMode` field is shown in the combined transport block above.

### Priority processing (service_tier)

OpenAI's API exposes priority processing via `service_tier`, settable per model in OpenClaw with `params.serviceTier` (shown in the combined transport block above). Supported values are `auto`, `default`, `flex`, and `priority`. Note that `serviceTier` is only forwarded to native OpenAI endpoints (`api.openai.com`) and native Codex endpoints (`chatgpt.com/backend-api`); if you route either provider through a proxy, OpenClaw leaves `service_tier` untouched.

### Server-side compaction (Responses API)

For direct OpenAI Responses models (`openai/*` on `api.openai.com`), the OpenAI plugin's OpenClaw stream wrapper auto-enables server-side compaction: it forces `store: true` (unless model compat sets `supportsStore: false`), injects `context_management: [{ type: "compaction", compact_threshold: ... }]`, and uses a default `compact_threshold` of 70% of `contextWindow` (or `80000` when unavailable). This applies to the built-in OpenClaw runtime path and to OpenAI provider hooks used by embedded runs; the native Codex app-server harness manages its own context through Codex and is configured by OpenAI's default agent route or provider/model runtime policy. The `responsesServerCompaction` flag can be explicitly enabled (useful for compatible endpoints like Azure OpenAI Responses), given a custom `responsesCompactThreshold`, or disabled — `responsesServerCompaction` only controls `context_management` injection, and direct OpenAI Responses models still force `store: true` unless compat sets `supportsStore: false`:

```json5
{
  agents: {
    defaults: {
      models: {
        "azure-openai-responses/gpt-5.5": {
          params: { responsesServerCompaction: true },
        },
        "openai/gpt-5.5": {
          params: {
            responsesServerCompaction: true,
            responsesCompactThreshold: 120000,
          },
        },
      },
    },
  },
}
```

### Strict-agentic GPT mode

For GPT-5-family runs on `openai/*`, OpenClaw can use a stricter embedded execution contract via `agents.defaults.embeddedAgent.executionContract: "strict-agentic"`. With `strict-agentic`, OpenClaw auto-enables `update_plan` for substantial work, retries structurally empty or reasoning-only turns with a visible-answer continuation, and uses explicit harness plan events when the selected harness provides them. OpenClaw does NOT classify assistant prose to decide whether a turn is a plan, progress update, or final answer. This mode is scoped to OpenAI and Codex GPT-5-family runs only; other providers and older model families keep default behavior:

```json5
{
  agents: {
    defaults: {
      embeddedAgent: { executionContract: "strict-agentic" },
    },
  },
}
```

### Native vs OpenAI-compatible routes

OpenClaw treats direct OpenAI, Codex, and Azure OpenAI endpoints differently from generic OpenAI-compatible `/v1` proxies. **Native routes** (`openai/*`, Azure OpenAI) keep `reasoning: { effort: "none" }` only for models that support the OpenAI `none` effort; omit disabled reasoning for models or proxies that reject `reasoning.effort: "none"`; default tool schemas to strict mode; attach hidden attribution headers on verified native hosts only; and keep OpenAI-only request shaping (`service_tier`, `store`, reasoning-compat, prompt-cache hints). **Proxy/compatible routes** use looser compat behavior; strip Completions `store` from non-native `openai-completions` payloads; accept advanced `params.extra_body`/`params.extraBody` pass-through JSON for OpenAI-compatible Completions proxies; accept `params.chat_template_kwargs` for OpenAI-compatible Completions proxies such as vLLM; and do not force strict tool schemas or native-only headers. Azure OpenAI uses native transport and compat behavior but does NOT receive the hidden attribution headers.

**Source**: OpenClaw documentation — `providers/openai` (Azure OpenAI endpoints + Advanced configuration sections; mirror `inbox/openclaw_docs/providers/openai.md`)
**Last Updated**: 2026-06-22
**Status**: Active
