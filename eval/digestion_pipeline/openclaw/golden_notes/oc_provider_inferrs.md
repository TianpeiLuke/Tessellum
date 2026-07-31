---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - local_model
keywords:
  - openclaw inferrs provider
  - self-hosted openai-compatible server
  - models.providers.inferrs custom entry
  - requiresstringcontent compat flag
  - supportstools compat flag
  - localservice on-demand startup
  - inferrs gemma local serving
  - proxy-style openai backend
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/inferrs
access_control_group: ["general"]
---

# OpenClaw — Configuring the Inferrs Local OpenAI-Compatible Provider

## Overview

This note is the procedure for running OpenClaw against a self-hosted **inferrs** server — a local backend that serves models behind an OpenAI-compatible `/v1` API. It mirrors the `providers/inferrs` source page: because inferrs is NOT a bundled OpenClaw provider plugin (`Plugin: none`), you configure it as a custom `models.providers.inferrs` entry on the generic `openai-completions` API path, optionally have OpenClaw start it on demand via `localService`, and tune the `requiresStringContent` / `supportsTools` compat flags so stricter local backends survive full agent-runtime turns. It covers the property table, getting started, the full config example, on-demand startup, the advanced (proxy-style) behavior, and troubleshooting.

## Provider Summary

inferrs (https://github.com/ericcurtin/inferrs) can serve local models behind an OpenAI-compatible `/v1` API; OpenClaw works with it through the generic `openai-completions` path. The source page documents these properties verbatim:

| Property | Value |
| --- | --- |
| Provider id | `inferrs` (custom; configure under `models.providers.inferrs`) |
| Plugin | none — `inferrs` is not a bundled OpenClaw provider plugin |
| Auth env var | Optional. Any value works if your inferrs server has no auth |
| API | OpenAI-compatible (`openai-completions`) |
| Suggested base URL | `http://127.0.0.1:8080/v1` (or wherever your inferrs server lives) |

The page's `Note` callout is load-bearing: inferrs is "currently best treated as a custom self-hosted OpenAI-compatible backend, not a dedicated OpenClaw provider plugin." You configure it through `models.providers.inferrs` rather than an onboarding choice flag. If you need a true bundled plugin with auto-discovery, the doc points instead to SGLang (`/providers/sglang`) or vLLM (`/providers/vllm`).

## Getting Started

The source `Getting started` Steps are a three-step procedure:

1. **Start inferrs with a model** — launch the server, pinning host, port, and device:

```bash
inferrs serve google/gemma-4-E2B-it \
  --host 127.0.0.1 \
  --port 8080 \
  --device metal
```

2. **Verify the server is reachable** — probe both the health endpoint and the OpenAI-compatible model list:

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/v1/models
```

3. **Add an OpenClaw provider entry** — add an explicit provider entry and point your default model at it (full config example below).

## Full Config Example

This example uses Gemma 4 on a local inferrs server. It sets the default `primary` model to the `inferrs/google/gemma-4-E2B-it` ref, gives it an `alias`, and defines the custom provider entry under `models.providers.inferrs` with `mode: "merge"`. Note the per-model fields: `reasoning: false`, `input: ["text"]`, zero `cost`, `contextWindow: 131072`, `maxTokens: 4096`, and the `compat.requiresStringContent: true` flag.

```json5
{
  agents: {
    defaults: {
      model: { primary: "inferrs/google/gemma-4-E2B-it" },
      models: {
        "inferrs/google/gemma-4-E2B-it": {
          alias: "Gemma 4 (inferrs)",
        },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      inferrs: {
        baseUrl: "http://127.0.0.1:8080/v1",
        apiKey: "inferrs-local",
        api: "openai-completions",
        models: [
          {
            id: "google/gemma-4-E2B-it",
            name: "Gemma 4 E2B (inferrs)",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 4096,
            compat: {
              requiresStringContent: true,
            },
          },
        ],
      },
    },
  },
}
```

The `apiKey` is `"inferrs-local"` here — per the property table, any value works if your inferrs server has no auth.

## On-Demand Startup (`localService`)

inferrs can also be started by OpenClaw only when an `inferrs/...` model is selected. Add a `localService` block to the same provider entry (alongside an explicit `timeoutSeconds: 300`). The `command` must be an absolute path: use `which inferrs` on the Gateway host and put that path in config. For the full field reference, the page defers to Local model services (`/gateway/local-model-services`).

```json5
{
  models: {
    providers: {
      inferrs: {
        baseUrl: "http://127.0.0.1:8080/v1",
        apiKey: "inferrs-local",
        api: "openai-completions",
        timeoutSeconds: 300,
        localService: {
          command: "/opt/homebrew/bin/inferrs",
          args: [
            "serve",
            "google/gemma-4-E2B-it",
            "--host",
            "127.0.0.1",
            "--port",
            "8080",
            "--device",
            "metal",
          ],
          healthUrl: "http://127.0.0.1:8080/v1/models",
          readyTimeoutMs: 180000,
          idleStopMs: 0,
        },
        models: [
          {
            id: "google/gemma-4-E2B-it",
            name: "Gemma 4 E2B (inferrs)",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 4096,
            compat: {
              requiresStringContent: true,
            },
          },
        ],
      },
    },
  },
}
```

The `localService` fields here are `command` (absolute path), `args` (the same `serve …` invocation as the manual start), `healthUrl: "http://127.0.0.1:8080/v1/models"`, `readyTimeoutMs: 180000`, and `idleStopMs: 0`.

## Advanced Configuration

The source `Advanced configuration` accordions document four behaviors:

**Why `requiresStringContent` matters.** Some inferrs Chat Completions routes accept only string `messages[].content`, not structured content-part arrays. If OpenClaw runs fail with an error like `messages[1].content: invalid type: sequence, expected a string`, set `compat.requiresStringContent: true` in your model entry. OpenClaw will then flatten pure text content parts into plain strings before sending the request.

**Gemma and tool-schema caveat.** Some current inferrs + Gemma combinations accept small direct `/v1/chat/completions` requests but still fail on full OpenClaw agent-runtime turns. If that happens, the doc says to try setting `compat: { requiresStringContent: true, supportsTools: false }` first. That disables OpenClaw's tool schema surface for the model and can reduce prompt pressure on stricter local backends. If tiny direct requests still work but normal OpenClaw agent turns continue to crash inside inferrs, the remaining issue is usually upstream model/server behavior rather than OpenClaw's transport layer.

**Manual smoke test.** Once configured, test both layers — first a raw `/v1/chat/completions` curl, then the same prompt through OpenClaw's `infer model run`. If the first command works but the second fails, check the troubleshooting section.

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"google/gemma-4-E2B-it","messages":[{"role":"user","content":"What is 2 + 2?"}],"stream":false}'

openclaw infer model run \
  --model inferrs/google/gemma-4-E2B-it \
  --prompt "What is 2 + 2? Reply with one short sentence." \
  --json
```

**Proxy-style behavior.** inferrs is treated as a proxy-style OpenAI-compatible `/v1` backend, not a native OpenAI endpoint. Consequently: native OpenAI-only request shaping does not apply; there is no `service_tier`, no Responses `store`, no prompt-cache hints, and no OpenAI reasoning-compat payload shaping; and hidden OpenClaw attribution headers (`originator`, `version`, `User-Agent`) are not injected on custom inferrs base URLs.

## Troubleshooting

The source `Troubleshooting` accordions map symptoms to fixes:

- **`curl /v1/models` fails** — inferrs is not running, not reachable, or not bound to the expected host/port. Make sure the server is started and listening on the address you configured.
- **`messages[].content` expected a string** — set `compat.requiresStringContent: true` in the model entry (see the `requiresStringContent` section above).
- **Direct `/v1/chat/completions` calls pass but `openclaw infer model run` fails** — try setting `compat.supportsTools: false` to disable the tool schema surface (see the Gemma tool-schema caveat above).
- **inferrs still crashes on larger agent turns** — if OpenClaw no longer gets schema errors but inferrs still crashes on larger agent turns, treat it as an upstream inferrs or model limitation; reduce prompt pressure or switch to a different local backend or model.

The page closes with a `Tip` pointing to general help: Troubleshooting (`/help/troubleshooting`) and FAQ (`/help/faq`).

**Source**: OpenClaw documentation — `providers/inferrs` (mirror `inbox/openclaw_docs/providers/inferrs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
