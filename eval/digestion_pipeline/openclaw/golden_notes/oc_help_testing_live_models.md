---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - testing
keywords:
  - openclaw live model tests
  - test:live model matrix
  - OPENCLAW_LIVE_MODELS allowlist
  - layer 1 direct model layer 2 gateway smoke
  - live cli backend smoke
  - acp bind smoke acpx
  - codex app-server harness smoke
  - OPENCLAW_LIVE_TEST recommended recipes
  - android node capability sweep
  - apns http2 proxy reachability
topics:
  - OpenClaw
  - Live Testing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/testing-live
access_control_group: ["general"]
---

# OpenClaw — Live Model, CLI, ACP & Codex Harness Smoke Tests

## Overview

This note is the operator procedure for OpenClaw's **live (network-touching) model and agent smokes** — suites that call real providers, CLIs, and agent backends. It mirrors the model/CLI/ACP/Codex half of the `help/testing-live` page: local smoke commands, the Android node capability sweep, the two-layer model smoke (Layer 1 direct vs Layer 2 gateway+agent), CLI-backend smoke, APNs HTTP/2 proxy reachability, ACP bind smoke, the Codex app-server harness smoke + recommended recipes, and the recommended model matrix. The sibling note `oc_help_testing_live_media_creds` owns the media-provider live suites and the `## Credentials (never commit)` rules; this note links to it.

## Live: local smoke commands

Export the needed provider key in the process environment before any ad hoc live check. A safe local-TTS media smoke and a voice-call readiness smoke (setup + dry-run) are below.

```bash
pnpm openclaw infer tts convert --local --json \
  --text "OpenClaw live smoke." \
  --output /tmp/openclaw-live-smoke.mp3

pnpm openclaw voicecall setup --json
pnpm openclaw voicecall smoke --to "+15555550123"
```

`voicecall smoke` is a dry run unless `--yes` is present (use `--yes` only to place a real notify call). For Twilio, Telnyx, and Plivo, a successful readiness check requires a public webhook URL — local-only loopback/private fallbacks are rejected by design.

## Live: Android node capability sweep

The Android node sweep runs `src/gateway/android-node.capabilities.live.test.ts` via `pnpm android:test:integration` to invoke **every command currently advertised** by a connected Android node and assert command-contract behavior (command-by-command gateway `node.invoke` validation; the suite does not install/run/pair the app). Required pre-setup: the Android app must already be connected + paired to the gateway, kept in the foreground, with permissions/capture consent granted for the capabilities you expect to pass. Optional overrides: `OPENCLAW_ANDROID_NODE_ID` or `OPENCLAW_ANDROID_NODE_NAME`, plus `OPENCLAW_ANDROID_GATEWAY_URL` / `OPENCLAW_ANDROID_GATEWAY_TOKEN` / `OPENCLAW_ANDROID_GATEWAY_PASSWORD`. Full setup is on `platforms/android`.

## Live: model smoke (profile keys)

Live model tests split into two layers so failures isolate: **"Direct model"** tells you the provider/model can answer with the given key; **"Gateway smoke"** tells you the full gateway+agent pipeline works (sessions, history, tools, sandbox).

### Layer 1: Direct model completion (no gateway)

Layer 1 runs `src/agents/models.profiles.live.test.ts`: it enumerates discovered models, uses `getApiKeyForModel` to select models you have creds for, and runs a small completion per model (plus targeted regressions). It skips by default to keep `pnpm test:live` focused on gateway smoke; set `OPENCLAW_LIVE_MODELS=modern`, `small`, or `all` (= modern) to run it.

Model selection: `OPENCLAW_LIVE_MODELS=modern` runs the modern allowlist (Opus/Sonnet 4.6+, GPT-5.2 + Codex, Gemini 3, DeepSeek V4, GLM 5.1, MiniMax M3, Grok 4.3); `=small` runs the small-model allowlist (Qwen 8B/9B local-compatible routes, Ollama Gemma, OpenRouter Qwen/GLM, Z.AI GLM); `all` aliases modern; or a comma allowlist `OPENCLAW_LIVE_MODELS="openai/gpt-5.5,anthropic/claude-opus-4-6,..."`. Local Ollama defaults to `http://127.0.0.1:11434` — set `OPENCLAW_LIVE_OLLAMA_BASE_URL` only for LAN/custom/Ollama Cloud. `OPENCLAW_LIVE_MAX_MODELS=0` runs an exhaustive selected-profile sweep; `OPENCLAW_LIVE_TEST_TIMEOUT_MS` sets the direct-model timeout (default 60 minutes); probes run 20-way parallel by default (`OPENCLAW_LIVE_MODEL_CONCURRENCY` overrides).

Provider selection uses `OPENCLAW_LIVE_PROVIDERS="google,google-antigravity,google-gemini-cli"`. Keys come from the profile store and env fallbacks by default; `OPENCLAW_LIVE_REQUIRE_PROFILE_KEYS=1` enforces **profile store** only. This layer separates "provider API broken / key invalid" from "gateway pipeline broken" and contains small isolated regressions (e.g. OpenAI/Codex Responses reasoning replay + tool-call flows).


### Layer 2: Gateway + dev agent smoke (what "@openclaw" actually does)

Layer 2 runs `src/gateway/gateway-models.profiles.live.test.ts`: it spins up an in-process gateway, creates/patches a `agent:dev:*` session (model override per run), iterates models-with-keys, and asserts a "meaningful" response (no tools), a real tool invocation (read probe), optional exec+read probes, and that OpenAI regression paths (tool-call-only → follow-up) keep working. Enable: `pnpm test:live`.

Probe details: the `read` probe writes a nonce file and asks the agent to `read` it and echo it back; the `exec+read` probe asks the agent to `exec`-write a nonce into a temp file then `read` it back; the image probe attaches a generated PNG (cat + randomized code) and expects `cat <CODE>` back (implementation in `test/helpers/live-image-probe.ts`). Tool + image probes are always on — `read` + `exec+read` always run; the image probe runs when the model advertises image input support. The image flow sends the PNG via `agent` `attachments: [{ mimeType: "image/png", content: "<base64>" }]`, the gateway parses attachments into `images[]` (`src/gateway/server-methods/agent.ts` + `src/gateway/chat-attachments.ts`), the embedded agent forwards a multimodal message, and the reply must contain `cat` + the code (OCR allows minor mistakes).

Model selection: default is the modern allowlist (Opus/Sonnet 4.6+, GPT-5.2 + Codex, Gemini 3, DeepSeek V4, GLM 4.7, MiniMax M3, Grok 4.3); `OPENCLAW_LIVE_GATEWAY_MODELS=small` runs the small-model allowlist through the full pipeline; `all` aliases modern; `="provider/model"` (or comma list) narrows; `OPENCLAW_LIVE_GATEWAY_MAX_MODELS=0` runs an exhaustive selected sweep. To avoid "OpenRouter everything", select providers with `OPENCLAW_LIVE_GATEWAY_PROVIDERS="google,google-antigravity,google-gemini-cli,openai,anthropic,zai,minimax"`. Run `openclaw models list` (add `--json`) to see testable `provider/model` ids.

## Live: CLI backend smoke (Claude, Gemini, or other local CLIs)

The CLI-backend smoke runs `src/gateway/gateway-cli-backend.live.test.ts` to validate the Gateway + agent pipeline using a local CLI backend **without touching your default config**; backend-specific defaults live with the owning extension's `cli-backend.ts`. Enable with `pnpm test:live` plus `OPENCLAW_LIVE_CLI_BACKEND=1`. Default provider/model `claude-cli/claude-sonnet-4-6`; command/args/image behavior come from the owning CLI backend plugin metadata.

Optional overrides: `OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-sonnet-4-6"`, `OPENCLAW_LIVE_CLI_BACKEND_COMMAND="/full/path/to/claude"`, `OPENCLAW_LIVE_CLI_BACKEND_ARGS='["-p","--output-format","json"]'`, `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_PROBE=1` (real image via prompt injection; Docker off unless requested), `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_ARG="--image"` (image paths as CLI args), `OPENCLAW_LIVE_CLI_BACKEND_IMAGE_MODE="repeat"` (or `"list"`), `OPENCLAW_LIVE_CLI_BACKEND_RESUME_PROBE=1` (second-turn resume), `OPENCLAW_LIVE_CLI_BACKEND_MODEL_SWITCH_PROBE=1` (Sonnet→Opus same-session continuity; Docker off), `OPENCLAW_LIVE_CLI_BACKEND_MCP_PROBE=1` (MCP/tool loopback; Docker off unless requested).

```bash
  OPENCLAW_LIVE_CLI_BACKEND=1 \
  OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-sonnet-4-6" \
  pnpm test:live src/gateway/gateway-cli-backend.live.test.ts
```

A cheap Gemini MCP config smoke is `OPENCLAW_LIVE_TEST=1 pnpm test:live src/agents/cli-runner/bundle-mcp.gemini.live.test.ts`: it does not generate a response but writes the system settings OpenClaw gives Gemini then runs `gemini --debug mcp list` to prove a saved `transport: "streamable-http"` server is normalized to Gemini's HTTP MCP shape and connects to a local streamable-HTTP MCP server. Docker recipes: `pnpm test:docker:live-cli-backend` (aggregate) and variants `:claude`, `:claude-subscription`, `:gemini`.

Docker notes: the runner `scripts/test-live-cli-backend-docker.sh` runs inside the repo Docker image as the non-root `node` user, resolves CLI smoke metadata from the owning extension, then installs the matching Linux CLI package (`@anthropic-ai/claude-code` or `@google/gemini-cli`) into a cached writable prefix `OPENCLAW_DOCKER_CLI_TOOLS_DIR` (default `~/.cache/openclaw/docker-cli-tools`). The `claude-subscription` lane requires portable Claude Code subscription OAuth via either `~/.claude/.credentials.json` with `claudeAiOauth.subscriptionType` or `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`; it proves direct `claude -p` in Docker, runs two Gateway turns without preserving Anthropic API-key env vars, and disables the Claude MCP/tool and image probes by default (Claude routes third-party usage through extra-usage billing). The smoke runs the same flow for Claude and Gemini (text turn, image classification turn, MCP `cron` tool call via the gateway CLI); Claude's default smoke also patches Sonnet→Opus and verifies the resumed session remembers an earlier note.

## Live: APNs HTTP/2 proxy reachability

The APNs reachability smoke runs `src/infra/push-apns-http2.live.test.ts` to tunnel through a local HTTP CONNECT proxy to Apple's sandbox APNs endpoint, send the APNs HTTP/2 validation request, and assert Apple's real `403 InvalidProviderToken` comes back through the proxy path. Enable with `OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_APNS_REACHABILITY=1 pnpm test:live src/infra/push-apns-http2.live.test.ts`, with optional `OPENCLAW_LIVE_APNS_TIMEOUT_MS=30000`.

## Live: ACP bind smoke (`/acp spawn ... --bind here`)

The ACP bind smoke runs `src/gateway/gateway-acp-bind.live.test.ts` to validate the real ACP conversation-bind flow with a live ACP agent: it sends `/acp spawn <agent> --bind here`, binds a synthetic message-channel conversation in place, sends a follow-up on that conversation, and verifies it lands in the bound ACP session transcript. Enable with `pnpm test:live src/gateway/gateway-acp-bind.live.test.ts` plus `OPENCLAW_LIVE_ACP_BIND=1`. Defaults: Docker ACP agents `claude,codex,gemini`; direct-run agent `claude`; synthetic Slack DM-style channel; ACP backend `acpx`.

Overrides include `OPENCLAW_LIVE_ACP_BIND_AGENT=claude|codex|droid|gemini|opencode`, `OPENCLAW_LIVE_ACP_BIND_AGENTS=claude,codex,gemini`, `OPENCLAW_LIVE_ACP_BIND_AGENT_COMMAND='npx -y @agentclientprotocol/claude-agent-acp@<version>'`, `OPENCLAW_LIVE_ACP_BIND_CODEX_MODEL=gpt-5.5`, `OPENCLAW_LIVE_ACP_BIND_OPENCODE_MODEL=opencode/kimi-k2.6`, `OPENCLAW_LIVE_ACP_BIND_REQUIRE_TRANSCRIPT=1`, `OPENCLAW_LIVE_ACP_BIND_REQUIRE_CRON=1`, and `OPENCLAW_LIVE_ACP_BIND_PARENT_MODEL=openai/gpt-5.5`. Notes: the lane uses the gateway `chat.send` surface with admin-only synthetic originating-route fields so tests attach message-channel context without delivering externally; with `OPENCLAW_LIVE_ACP_BIND_AGENT_COMMAND` unset the test uses the embedded `acpx` plugin's built-in agent registry; bound-session cron MCP creation is best-effort by default (external ACP harnesses can cancel MCP calls after the bind/image proof), so `OPENCLAW_LIVE_ACP_BIND_REQUIRE_CRON=1` makes it strict.

```bash
OPENCLAW_LIVE_ACP_BIND=1 \
  OPENCLAW_LIVE_ACP_BIND_AGENT=claude \
  pnpm test:live src/gateway/gateway-acp-bind.live.test.ts
```

Docker recipes are `pnpm test:docker:live-acp-bind` (aggregate) and single-agent variants `:claude`, `:codex`, `:droid`, `:gemini`, `:opencode`. The runner `scripts/test-live-acp-bind-docker.sh` by default runs the bind smoke against the live CLI agents in sequence (`claude`, `codex`, then `gemini`); `OPENCLAW_LIVE_ACP_BIND_AGENTS=...` narrows it. It stages the matching CLI auth material then installs the requested live CLI (`@anthropic-ai/claude-code`, `@openai/codex`, Factory Droid via `https://app.factory.ai/cli`, `@google/gemini-cli`, or `opencode-ai`) if missing — the ACP backend is the embedded `acpx/runtime` package from the official `acpx` plugin. The Droid variant stages `~/.factory`, requires `FACTORY_API_KEY` (local Factory auth is not container-portable), and uses ACPX's `droid exec --output-format acp` registry entry; the OpenCode variant is a strict single-agent lane writing a temporary `OPENCODE_CONFIG_CONTENT` default from `OPENCLAW_LIVE_ACP_BIND_OPENCODE_MODEL` (default `opencode/kimi-k2.6`) and requiring a bound transcript. Direct `acpx` CLI calls are only a manual path outside the Gateway; the Docker smoke exercises the embedded `acpx` runtime backend.

## Live: Codex app-server harness smoke

The Codex harness smoke validates the plugin-owned Codex harness through the normal gateway `agent` method: it loads the bundled `codex` plugin, selects `openai/gpt-5.5` (which routes OpenAI agent turns through Codex by default), sends a first then a second gateway agent turn to the same session to verify the app-server thread resumes, runs `/codex status` and `/codex models` through the gateway command path, and optionally runs two Guardian-reviewed escalated shell probes (one benign approved, one fake-secret upload denied). The test is `src/gateway/gateway-codex-harness.live.test.ts`, enabled with `OPENCLAW_LIVE_CODEX_HARNESS=1` and default model `openai/gpt-5.5`; optional probes `OPENCLAW_LIVE_CODEX_HARNESS_IMAGE_PROBE=1`, `_MCP_PROBE=1`, `_GUARDIAN_PROBE=1`. The smoke forces provider/model `agentRuntime.id: "codex"` so a broken harness cannot pass by silently falling back to OpenClaw; auth comes from the local Codex subscription login (Docker smokes can also provide `OPENAI_API_KEY` plus optional copied `~/.codex/auth.json` and `~/.codex/config.toml`).

```bash
OPENCLAW_LIVE_CODEX_HARNESS=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_IMAGE_PROBE=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_MCP_PROBE=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_GUARDIAN_PROBE=1 \
  OPENCLAW_LIVE_CODEX_HARNESS_MODEL=openai/gpt-5.5 \
  pnpm test:live -- src/gateway/gateway-codex-harness.live.test.ts
```

The Docker recipe is `pnpm test:docker:live-codex-harness`; its runner `scripts/test-live-codex-harness-docker.sh` passes `OPENAI_API_KEY`, copies Codex CLI auth files when present, installs `@openai/codex` into a writable mounted npm prefix, stages the source tree, then runs only the Codex-harness test. Docker enables the image, MCP/tool, and Guardian probes by default (set any of `_IMAGE_PROBE=0`, `_MCP_PROBE=0`, `_GUARDIAN_PROBE=0` to narrow) using the same explicit Codex runtime config so legacy aliases or OpenClaw fallback cannot hide a regression.

### Recommended live recipes

Narrow explicit allowlists are fastest and least flaky. Recipes: single-model direct `OPENCLAW_LIVE_MODELS="openai/gpt-5.5" pnpm test:live src/agents/models.profiles.live.test.ts`; small-model direct/gateway via `OPENCLAW_LIVE_MODELS=small` / `OPENCLAW_LIVE_GATEWAY_MODELS=small pnpm test:live src/gateway/gateway-models.profiles.live.test.ts`; single-model gateway `OPENCLAW_LIVE_GATEWAY_MODELS="openai/gpt-5.5" ...`; Z.AI Coding Plan GLM-5.2 direct `ZAI_CODING_LIVE_TEST=1 pnpm test:live src/agents/zai.live.test.ts`; and the Ollama Cloud smoke below.

```bash
OPENCLAW_LIVE_TEST=1 OPENCLAW_LIVE_OLLAMA=1 OPENCLAW_LIVE_OLLAMA_BASE_URL=https://ollama.com OPENCLAW_LIVE_OLLAMA_MODEL=glm-5.1:cloud OPENCLAW_LIVE_OLLAMA_WEB_SEARCH=0 pnpm test:live -- extensions/ollama/ollama.live.test.ts
```

Google focus splits into Gemini API key `OPENCLAW_LIVE_GATEWAY_MODELS="google/gemini-3-flash-preview" ...` and Antigravity OAuth `OPENCLAW_LIVE_GATEWAY_MODELS="google-antigravity/claude-opus-4-6-thinking,google-antigravity/gemini-3-pro-high" ...`; a Google adaptive-thinking smoke uses `pnpm openclaw qa manual --provider-mode live-frontier --model google/gemini-3.1-pro-preview --message '/think adaptive Reply exactly: GEMINI_ADAPTIVE_OK' --timeout-ms 180000`. The three Google route families differ by auth: `google/...` uses the Gemini API; `google-antigravity/...` uses the Antigravity OAuth bridge; `google-gemini-cli/...` shells out to a local `gemini` binary with its own auth and quirks.

## Live: model matrix (what we cover)

There is no fixed "CI model list" (live is opt-in), but these are **recommended** models to cover with keys. The **modern smoke set** (tool calling + image, the "common models" run) is: OpenAI non-Codex + ChatGPT/Codex OAuth `openai/gpt-5.5`; Anthropic `anthropic/claude-opus-4-6` (or `anthropic/claude-sonnet-4-6`); Google Gemini API `google/gemini-3.1-pro-preview` + `google/gemini-3-flash-preview` (avoid older Gemini 2.x); Google Antigravity `google-antigravity/claude-opus-4-6-thinking` + `google-antigravity/gemini-3-flash`; DeepSeek `deepseek/deepseek-v4-flash` + `deepseek/deepseek-v4-pro`; Z.AI `zai/glm-5.1` (general API) or `zai/glm-5.2` (Coding Plan); MiniMax `minimax/MiniMax-M3`. The **baseline tool-calling** set (Read + optional Exec, one per family) reuses those plus optional xAI `xai/grok-4.3`, Mistral, Cerebras, LM Studio; for **vision**, include an image-capable model in `OPENCLAW_LIVE_GATEWAY_MODELS`.

For **aggregators / alternate gateways** with keys: OpenRouter (`openrouter/...`, hundreds of models — `openclaw models scan` finds tool+image candidates) and OpenCode (`opencode/...` Zen, `opencode-go/...` Go; auth via `OPENCODE_API_KEY` / `OPENCODE_ZEN_API_KEY`). Built-in providers include `openai`, `anthropic`, `google`, `google-vertex`, `google-antigravity`, `google-gemini-cli`, `zai`, `openrouter`, `opencode`, `opencode-go`, `xai`, `groq`, `cerebras`, `mistral`, `github-copilot`, plus `models.providers` custom endpoints like `minimax` and any OpenAI/Anthropic-compatible proxy. The source warns: do not hardcode "all models" — the authoritative list is whatever `discoverModels(...)` returns plus available keys. Media-provider live suites and shared credential rules are in `oc_help_testing_live_media_creds`.

**Source**: OpenClaw documentation — `help/testing-live` (mirror `inbox/openclaw_docs/help/testing-live.md`), model/CLI/ACP/Codex sections
**Last Updated**: 2026-06-22
**Status**: Active
