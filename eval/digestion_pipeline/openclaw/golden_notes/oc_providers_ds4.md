---
tags:
  - resource
  - documentation
  - openclaw
  - providers
  - local_model
keywords:
  - openclaw ds4 provider
  - deepseek v4 flash local
  - openai-completions provider
  - models.providers.ds4 config
  - localService on-demand startup
  - ds4 ctx context window
  - ds4 think max reasoning_effort
  - ds4-server metal gguf
topics:
  - OpenClaw
  - Providers
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/providers/ds4
access_control_group: ["general"]
---

# OpenClaw — Run a Local ds4 (DeepSeek V4 Flash) Server

## Overview

This note is the procedure for running OpenClaw against [`ds4`](https://github.com/antirez/ds4), a local DeepSeek V4 Flash server that exposes an OpenAI-compatible `/v1` API from a macOS Metal backend. ds4 is NOT a bundled OpenClaw provider plugin; you wire it in through the generic `openai-completions` provider family by declaring `models.providers.ds4` and then selecting the model ref `ds4/deepseek-v4-flash`. It mirrors the `providers/ds4` source page: requirements and the central `--ctx` sizing warning, the three-step quickstart, the full `models.providers.ds4` config block, `localService` on-demand startup, the Think Max large-context contract, the curl + `openclaw infer`/`openclaw agent` smoke tests, and the four troubleshooting cases.

## Provider facts

The page fixes these provider identifiers (copy verbatim into config):

- Provider id: `ds4`
- Plugin: none (configured manually under `models.providers.ds4`)
- API: OpenAI-compatible Chat Completions (`openai-completions`)
- Suggested base URL: `http://127.0.0.1:18000/v1`
- Model id: `deepseek-v4-flash` (selected as the ref `ds4/deepseek-v4-flash`)
- Tool calls: supported through OpenAI-style `tools` and `tool_calls`
- Reasoning: DeepSeek-style `thinking` and `reasoning_effort`

## Requirements

- macOS with Metal support.
- A working ds4 checkout with `ds4-server` and the DeepSeek V4 Flash GGUF file.
- Enough memory for the context you choose. Larger `--ctx` values allocate more KV memory when the server starts.

**Context-sizing warning (load-bearing).** OpenClaw agent turns include tool schemas and workspace context, so the prompt is much larger than a bare chat message. A tiny context such as `--ctx 4096` can pass direct curl tests but fail full agent runs with `500 prompt exceeds context`. Use at least `--ctx 32768` for agent and tool smoke tests. Use `--ctx 393216` only when you have enough memory and want ds4 Think Max behavior.

## Quickstart

Three steps: start the server, verify the endpoint, then add the OpenClaw provider config and run a one-shot model check.

**1. Start `ds4-server`** — replace `<DS4_DIR>` with your ds4 checkout path:

```bash
<DS4_DIR>/ds4-server \
  --model <DS4_DIR>/ds4flash.gguf \
  --host 127.0.0.1 \
  --port 18000 \
  --ctx 32768 \
  --tokens 128
```

**2. Verify the OpenAI-compatible endpoint** with `curl http://127.0.0.1:18000/v1/models`; the response should include `deepseek-v4-flash`.

**3. Add the provider config** from [Full config](#full-config), then run a one-shot model check with `openclaw infer model run --local --model ds4/deepseek-v4-flash --thinking off --prompt "Reply with exactly: openclaw-ds4-ok" --json` (the same command is shown in full under [Test](#test)).

## Full config

Use this config when ds4 is already running on `127.0.0.1:18000`. It selects `ds4/deepseek-v4-flash` as the default model, gives it the alias `DS4 local`, and declares the `ds4` provider with `api: "openai-completions"`, the local `baseUrl`, a placeholder `apiKey: "ds4-local"` (the local server ignores the key), a 300-second `timeoutSeconds`, and one `models[]` entry carrying the reasoning/`compat` flags.

```json5
{
  agents: {
    defaults: {
      model: { primary: "ds4/deepseek-v4-flash" },
      models: {
        "ds4/deepseek-v4-flash": {
          alias: "DS4 local",
        },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      ds4: {
        baseUrl: "http://127.0.0.1:18000/v1",
        apiKey: "ds4-local",
        api: "openai-completions",
        timeoutSeconds: 300,
        models: [
          {
            id: "deepseek-v4-flash",
            name: "DeepSeek V4 Flash (ds4)",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 32768,
            maxTokens: 128,
            compat: {
              supportsUsageInStreaming: true,
              supportsReasoningEffort: true,
              maxTokensField: "max_tokens",
              supportsStrictMode: false,
              thinkingFormat: "deepseek",
              supportedReasoningEfforts: ["low", "medium", "high", "xhigh"],
            },
          },
        ],
      },
    },
  },
}
```

**Alignment rule.** Keep `contextWindow` aligned with the `ds4-server --ctx` value, and keep `maxTokens` aligned with `--tokens` unless you intentionally want OpenClaw to request less output than the server default. A `contextWindow` larger than the running `--ctx` is what produces the `500 prompt exceeds context` failure on full agent turns.

## On-demand startup (`localService`)

OpenClaw can start ds4 only when a `ds4/...` model is selected, instead of you launching `ds4-server` by hand. Add a `localService` block to the same provider entry; OpenClaw runs `command` with `args`, polls `healthUrl` until ready, and waits up to `readyTimeoutMs` for warmup. `command` must be an absolute executable path — shell lookup and `~` expansion are NOT used. See [Local model services](https://docs.openclaw.ai/gateway/local-model-services) for every `localService` field.

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
        models: [ /* same deepseek-v4-flash entry as Full config */ ],
      },
    },
  },
}
```

## Think Max

ds4 applies Think Max only when BOTH conditions are true: (1) `ds4-server` starts with `--ctx 393216` or higher, and (2) the request uses `reasoning_effort: "max"` or the equivalent ds4 effort field. Smaller contexts fall back to high reasoning. If you run that large context, update both the server flags and the OpenClaw model metadata — raise `contextWindow` to `393216`, raise `maxTokens` to `384000`, and add `"max"` to `supportedReasoningEfforts`:

```json5
{
  contextWindow: 393216,
  maxTokens: 384000,
  compat: {
    supportsUsageInStreaming: true,
    supportsReasoningEffort: true,
    maxTokensField: "max_tokens",
    supportsStrictMode: false,
    thinkingFormat: "deepseek",
    supportedReasoningEfforts: ["low", "medium", "high", "xhigh", "max"],
  },
}
```

## Test

Start with a direct HTTP check against the server, sending `thinking: {"type":"disabled"}` for a fast deterministic reply:

```bash
curl http://127.0.0.1:18000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Reply with exactly: ds4-ok"}],"max_tokens":16,"stream":false,"thinking":{"type":"disabled"}}'
```

Then test OpenClaw model routing with `openclaw infer model run --local --model ds4/deepseek-v4-flash --thinking off --prompt "Reply with exactly: openclaw-ds4-ok" --json`. Finally, for a full agent and tool-call smoke (use a context of at least 32768):

```bash
openclaw agent \
  --local \
  --session-id ds4-tool-smoke \
  --model ds4/deepseek-v4-flash \
  --thinking off \
  --message "Use the shell command pwd once, then reply exactly: tool-ok <output>" \
  --json \
  --timeout 240
```

Expected result: `executionTrace.winnerProvider` is `ds4`, `executionTrace.winnerModel` is `deepseek-v4-flash`, `toolSummary.calls` is at least `1`, and `finalAssistantVisibleText` starts with `tool-ok`.

## Troubleshooting

- **`curl /v1/models` cannot connect** — ds4 is not running or not bound to the host and port in `baseUrl`. Start `ds4-server`, then retry `curl http://127.0.0.1:18000/v1/models`.
- **`500 prompt exceeds context`** — the configured `--ctx` is too small for the OpenClaw turn. Raise `ds4-server --ctx`, then update `models.providers.ds4.models[].contextWindow` to match. Full agent turns with tools need substantially more context than a direct one-message curl request.
- **Think Max does not activate** — ds4 only uses Think Max when `--ctx` is at least `393216` and the request asks for `reasoning_effort: "max"`. Smaller contexts fall back to high reasoning.
- **The first request is slow** — ds4 has a cold Metal residency and model warmup phase. Use `localService.readyTimeoutMs: 300000` when OpenClaw starts the server on demand.

**Source**: OpenClaw documentation — `providers/ds4` (mirror `inbox/openclaw_docs/providers/ds4.md`)
**Last Updated**: 2026-06-22
**Status**: Active
