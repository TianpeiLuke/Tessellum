---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - local_models
keywords:
  - openclaw local model services
  - models.providers localService
  - on-demand local model server
  - healthUrl readyTimeoutMs idleStopMs
  - command args cwd env
  - probe start wait lifecycle
  - inferrs ds4 local server
  - openai-completions local backend
topics:
  - OpenClaw
  - Gateway Local Model Services
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/local-model-services
access_control_group: ["general"]
---

# OpenClaw — Local Model Services (On-Demand Local Servers)

## Overview

This note is the procedure for **on-demand local model servers** in OpenClaw via the `models.providers.<id>.localService` config block, mirroring the `gateway/local-model-services` source page. `localService` is provider-level config that lets OpenClaw start a provider-owned local model server only when a model belonging to that provider is selected: OpenClaw probes the service, starts the process if the endpoint is down, waits for readiness, then sends the model request. It covers the probe-start-wait lifecycle, the full config shape and field reference (`command` / `args` / `cwd` / `env` / `healthUrl` / `readyTimeoutMs` / `idleStopMs`), the worked inferrs and ds4 examples, and the idle-shutdown / serialization operational notes. Use it for local servers that are expensive to keep running all day, or for manual setups where model selection alone should bring the backend up.

## How It Works (Probe-Start-Wait Lifecycle)

The lifecycle runs in the following ordered steps, exactly as the source enumerates them:

1. A model request resolves to a configured provider.
2. If that provider has `localService`, OpenClaw probes `healthUrl`.
3. If the probe succeeds, OpenClaw uses the existing server.
4. If the probe fails, OpenClaw starts `command` with `args`.
5. OpenClaw polls readiness until `readyTimeoutMs` expires.
6. The model request is sent through the normal provider transport.
7. If OpenClaw started the process and `idleStopMs` is positive, the process is stopped after the last in-flight request has been idle for that long.

OpenClaw does **not** install launchd, systemd, Docker, or a daemon for this. The server is a child process of the OpenClaw process that first needed it.

## Config Shape

`localService` is nested under a provider entry in `models.providers.<id>`, alongside the provider's `baseUrl`, `apiKey`, `api`, `timeoutSeconds`, and `models` list:

```json5
{
  models: {
    providers: {
      local: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "local-model",
        api: "openai-completions",
        timeoutSeconds: 300,
        localService: {
          command: "/absolute/path/to/server",
          args: ["--host", "127.0.0.1", "--port", "8000"],
          cwd: "/absolute/path/to/working-dir",
          env: { LOCAL_MODEL_CACHE: "/absolute/path/to/cache" },
          healthUrl: "http://127.0.0.1:8000/v1/models",
          readyTimeoutMs: 180000,
          idleStopMs: 0,
        },
        models: [
          {
            id: "my-local-model",
            name: "My Local Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Fields

The `localService` block accepts these fields (defaults verbatim from source):

- `command`: absolute executable path. Shell lookup is not used.
- `args`: process arguments. No shell expansion, pipes, globbing, or quoting rules are applied.
- `cwd`: optional working directory for the process.
- `env`: optional environment variables merged over the OpenClaw process environment.
- `healthUrl`: readiness URL. If omitted, OpenClaw appends `/models` to `baseUrl`, so `http://127.0.0.1:8000/v1` becomes `http://127.0.0.1:8000/v1/models`.
- `readyTimeoutMs`: startup readiness deadline. Default: `120000`.
- `idleStopMs`: idle shutdown delay for OpenClaw-started processes. `0` or omitted keeps the process alive until OpenClaw exits.

## Inferrs Example

Inferrs is a custom OpenAI-compatible `/v1` backend, so the same local service API works with the `inferrs` provider entry. This example pins the default agent model to `inferrs/google/gemma-4-E2B-it` and uses `models.mode: "merge"`:

```json5
{
  agents: {
    defaults: {
      model: { primary: "inferrs/google/gemma-4-E2B-it" },
    },
  },
  models: {
    mode: "merge",
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

Replace `command` with the result of `which inferrs` on the machine running OpenClaw.

## ds4 Example

For the full setup, context sizing guidance, and verification commands, the source defers to the [oc_providers_ds4](oc_providers_ds4.md) page. The ds4 provider entry serves a local DeepSeek V4 Flash GGUF model with an empty `models: []` list and a longer `readyTimeoutMs: 300000`:

```json5
{
  models: {
    providers: {
      ds4: {
        baseUrl: "http://127.0.0.1:18000/v1",
        apiKey: "ds4-local",
        api: "openai-completions",
        timeoutSeconds: 300,
        localService: {
          command: "<DS4_DIR>/ds4-server",
          args: [
            "--model",
            "<DS4_DIR>/ds4flash.gguf",
            "--host",
            "127.0.0.1",
            "--port",
            "18000",
            "--ctx",
            "32768",
            "--tokens",
            "128",
          ],
          cwd: "<DS4_DIR>",
          healthUrl: "http://127.0.0.1:18000/v1/models",
          readyTimeoutMs: 300000,
          idleStopMs: 0,
        },
        models: [],
      },
    },
  },
}
```

## Operational Notes

The source lists these operational behaviors verbatim:

- One OpenClaw process manages the child it started. Another OpenClaw process that sees the same health URL already live will reuse it without adopting it.
- Startup is serialized per provider command and argument set, so concurrent requests do not spawn duplicate servers for the same config.
- Active streaming responses hold a lease; idle shutdown waits until response body handling is complete.
- Use `timeoutSeconds` on slow local providers so cold starts and long generations do not hit the default model request timeout.
- Use an explicit `healthUrl` if your server exposes readiness somewhere other than `/v1/models`.

**Source**: OpenClaw documentation — `gateway/local-model-services` (mirror `inbox/openclaw_docs/gateway/local-model-services.md`)
**Last Updated**: 2026-06-22
**Status**: Active
