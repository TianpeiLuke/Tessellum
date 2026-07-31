---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - automation
keywords:
  - openclaw onboard non-interactive
  - openclaw cli automation
  - secret-input-mode plaintext ref
  - auth-choice provider flags
  - scripted openclaw agents add
  - ci onboarding openclaw
  - custom provider compatibility flags
  - gateway-port gateway-bind loopback
topics:
  - OpenClaw
  - CLI Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/wizard-cli-automation
access_control_group: ["general"]
---

# OpenClaw — Scripted (Non-Interactive) CLI Onboarding

## Overview

This note is the procedure for automating OpenClaw onboarding in scripts or CI, mirroring the `start/wizard-cli-automation` source page. It documents how `--non-interactive` drives `openclaw onboard` without prompts, the baseline command shape, the `--secret-input-mode plaintext` vs `ref` credential-storage choice, the per-provider non-interactive flag sets (Anthropic, Gemini, Z.AI, Vercel/Cloudflare AI Gateway, Moonshot, Mistral, Synthetic, OpenCode, Ollama, custom provider), and the scripted `openclaw agents add` command for provisioning a second agent. The interactive flow itself is covered by the onboarding hub; per-flag semantics are defined in the full reference (both linked under Related Notes).

## Enabling Non-Interactive Mode

Use `--non-interactive` to automate `openclaw onboard`. The source carries an explicit caution: `--json` does NOT imply non-interactive mode — use `--non-interactive` (and `--workspace`) for scripts. Add `--json` separately for a machine-readable summary.

Use `--skip-bootstrap` when your automation pre-seeds workspace files and does not want onboarding to create the default bootstrap files.

## Baseline Non-Interactive Example

The baseline scripted onboarding selects local mode, the API-key auth path, an Anthropic key pulled from the process environment, plaintext secret storage, the loopback-bound default gateway port, a Node daemon install, and skipping of both bootstrap files and skills:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --secret-input-mode plaintext \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-bootstrap \
  --skip-skills
```

## Secret Input Mode — plaintext vs ref

`--secret-input-mode` chooses how credentials are persisted into auth profiles:

- `plaintext` — stores the literal secret value (used in the baseline example above).
- `ref` — stores env-backed refs in auth profiles instead of plaintext values. Interactive selection between env refs and configured provider refs (`file` or `exec`) is available in the onboarding flow.

In non-interactive `ref` mode, **provider env vars must be set in the process environment**. Passing inline key flags without the matching env var now fails fast. The minimal `ref`-mode example (here selecting OpenAI and accepting the risk prompt non-interactively) is:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice openai-api-key \
  --secret-input-mode ref \
  --accept-risk
```

## Provider-Specific Non-Interactive Flag Sets

Each provider accordion in the source repeats the same baseline shape (`--non-interactive --mode local`, plus `--gateway-port 18789 --gateway-bind loopback`) and differs only in the `--auth-choice` value and the provider key/option flags. The flag sets, copied verbatim from the source, are:

| Provider | `--auth-choice` | Provider-specific flags |
|---|---|---|
| Anthropic API key | `apiKey` | `--anthropic-api-key "$ANTHROPIC_API_KEY"` |
| Gemini | `gemini-api-key` | `--gemini-api-key "$GEMINI_API_KEY"` |
| Z.AI | `zai-api-key` | `--zai-api-key "$ZAI_API_KEY"` |
| Vercel AI Gateway | `ai-gateway-api-key` | `--ai-gateway-api-key "$AI_GATEWAY_API_KEY"` |
| Cloudflare AI Gateway | `cloudflare-ai-gateway-api-key` | `--cloudflare-ai-gateway-account-id "your-account-id"` · `--cloudflare-ai-gateway-gateway-id "your-gateway-id"` · `--cloudflare-ai-gateway-api-key "$CLOUDFLARE_AI_GATEWAY_API_KEY"` |
| Moonshot | `moonshot-api-key` | `--moonshot-api-key "$MOONSHOT_API_KEY"` |
| Mistral | `mistral-api-key` | `--mistral-api-key "$MISTRAL_API_KEY"` |
| Synthetic | `synthetic-api-key` | `--synthetic-api-key "$SYNTHETIC_API_KEY"` |
| OpenCode | `opencode-zen` | `--opencode-zen-api-key "$OPENCODE_API_KEY"` (swap to `--auth-choice opencode-go --opencode-go-api-key "$OPENCODE_API_KEY"` for the Go catalog) |
| Ollama | `ollama` | `--custom-model-id "qwen3.5:27b"` · `--accept-risk` |
| Custom provider | `custom-api-key` | `--custom-base-url` · `--custom-model-id` · `--custom-api-key "$CUSTOM_API_KEY"` · `--custom-provider-id` · `--custom-compatibility` · `--custom-image-input` |

### Custom Provider Details

The custom-provider example targets an OpenAI/Anthropic-compatible endpoint:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --custom-provider-id "my-custom" \
  --custom-compatibility anthropic \
  --custom-image-input \
  --gateway-port 18789 \
  --gateway-bind loopback
```

`--custom-api-key` is optional; if omitted, onboarding checks `CUSTOM_API_KEY`. OpenClaw marks common vision model IDs as image-capable automatically — add `--custom-image-input` for unknown custom vision IDs, or `--custom-text-input` to force text-only metadata. In the ref-mode variant (export `CUSTOM_API_KEY` first, then pass `--secret-input-mode ref` instead of the inline key), onboarding stores `apiKey` as `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`.

### Anthropic Token Note

Anthropic setup-token remains available as a supported onboarding token path, but OpenClaw now prefers Claude CLI reuse when available. For production, prefer an Anthropic API key.

## Add Another Agent (Scripted)

Use `openclaw agents add <name>` to create a separate agent with its own workspace, sessions, and auth profiles. Running without `--workspace` launches the wizard, so a scripted invocation supplies `--workspace` (and `--non-interactive`). The source example provisions a `work` agent bound to a WhatsApp business channel:

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.5 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

What it sets: `agents.list[].name`, `agents.list[].workspace`, `agents.list[].agentDir`. Notes from the source: default workspaces follow `~/.openclaw/workspace-<agentId>`; add `bindings` to route inbound messages (the wizard can do this); the non-interactive flags are `--model`, `--agent-dir`, `--bind`, `--non-interactive`.

**Source**: OpenClaw documentation — `start/wizard-cli-automation` (mirror `inbox/openclaw_docs/start/wizard-cli-automation.md`)
**Last Updated**: 2026-06-22
**Status**: Active
