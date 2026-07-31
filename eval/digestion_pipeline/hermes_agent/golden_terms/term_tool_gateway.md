---
tags:
  - resource
  - terminology
  - agentic_ai
  - hermes_agent
  - tools
keywords:
  - tool gateway
  - nous tool gateway
  - managed tools
  - use_gateway
  - nous portal
  - tool-execution proxy
topics:
  - agentic AI
  - agent tools
  - managed tool routing
language: markdown
date of note: 2026-06-15
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway
---

# Tool Gateway (Nous Tool Gateway)

## Definition

The **Tool Gateway** (Nous Tool Gateway) is a managed tool-execution proxy in the [Hermes Agent](term_hermes_agent.md) framework: a single paid [Nous Portal](https://portal.nousresearch.com) subscription routes the agent's tool calls — web search/extraction, image generation, text-to-speech, and cloud browser automation — through infrastructure that Nous Research already operates, so a builder does not have to individually sign up with Firecrawl, FAL, OpenAI, or Browser Use to make an agent useful. It collapses the "stitch together 5+ third-party API subscriptions" problem into one bill, one signup, and one OAuth credential while still using the same upstream backends a direct-key route would use.

Architecturally it is a [reverse-proxy](term_reverse_proxy.md) / [proxy-pattern](term_proxy_pattern.md) layer that sits in front of provider backends: the agent's tool surface is unchanged, but each tool's outbound call is transparently fronted by Nous-managed infrastructure rather than the builder's own provider account. It is not a lock-in — keys can be brought per-tool at any time, and the gateway falls back to direct keys when its per-tool flag is off.

## Context

The Tool Gateway is a Hermes-specific feature documented under the Hermes Agent user guide. It is purchased and billed through Nous Portal (the subscription/billing home), and it operates at the **tool-execution layer**, not the CLI — so every interface that can call a tool (CLI, Telegram, Discord, Slack, IRC, Teams, the API server) benefits from it transparently. Within the Hermes feature set it is a sibling concept to the agent's broader tool registry/toolsets and to the external memory-provider plugins (both route capabilities through pluggable backends), and it complements the per-platform delivery of generated media (voice notes, images) that those tools produce.

Builders enable it three ways: `hermes setup --portal` (fresh install: Nous OAuth + set Nous as inference provider + enable the gateway for all tools), `hermes model` (switch inference provider to Nous Portal, then opt the gateway on for all tools), or `hermes tools` (the à-la-carte path — enable the gateway for a single tool category, logging in inline if needed without switching the inference provider). Routing state is inspected with `hermes portal info`, `hermes portal tools`, and `hermes status`.

## Key Characteristics

- **Four managed tool categories** — web search & extraction (Firecrawl backend), image generation (multiple models under one endpoint, defaulting to a fast FLUX-class model with per-call override via the `image_generate` model ID), text-to-speech (OpenAI TTS voices wired into the `text_to_speech` tool), and cloud browser automation (headless Chromium via Browser Use, exposing `browser_navigate`/`browser_click`/`browser_type`/`browser_vision`).
- **One OAuth credential** — the builder's Nous Portal OAuth covers every gateway tool; no per-provider key management. Auth is normally auto-populated from the Portal login.
- **Per-tool `use_gateway` flag** — each tool's `config.yaml` block carries a `use_gateway` boolean. Precedence: `use_gateway: true` routes through Nous regardless of any direct keys present in `.env`; `false`/absent uses direct keys when available and only falls back to the gateway when none exist.
- **Mix-and-match** — routing is per-tool, so an agent can run web + images through Nous while keeping a builder's own ElevenLabs key for TTS, or route only the tools for which the builder lacks keys.
- **Pay-as-you-use billing** — all categories are metered against the Nous subscription; the Portal dashboard breaks usage down per tool. A subscription lapse stops gateway-routed tools until renewal or swap-in of direct keys (Hermes surfaces a clear error).
- **Eligibility** — a paid-subscription feature; free-tier accounts get Portal inference but not managed tools. Some accounts also receive a small **free tool pool** allowance that covers gateway calls without a paid subscription, surfaced with a first-use opt-in prompt.
- **Self-hosted override (advanced)** — `TOOL_GATEWAY_DOMAIN`/`TOOL_GATEWAY_SCHEME`/`TOOL_GATEWAY_USER_TOKEN` and per-endpoint URL overrides (set in `~/.hermes/.env`) point Hermes at a custom Nous-compatible gateway for enterprise/dev deployments.
- **Not a lock-in** — existing API keys can stay in `.env`; flipping `use_gateway` back to `false` restores them as the source.

## Related Terms


## References

- [Nous Tool Gateway — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway)
- [Nous Portal — Subscription & Billing Home](https://portal.nousresearch.com)
- [Nous Portal — Manage Subscription](https://portal.nousresearch.com/manage-subscription)
- [Hermes Agent (Nous Research, GitHub)](https://github.com/nousresearch/hermes-agent)
- [Firecrawl — Web Scraping & Extraction API](https://www.firecrawl.dev/)
- [FAL — Generative Media Inference (image models)](https://fal.ai/)
- [Browser Use — Headless Browser Automation for Agents](https://browser-use.com/)
- [OpenAI Text-to-Speech API](https://platform.openai.com/docs/guides/text-to-speech)

---

**Last Updated**: 2026-06-15
**Status**: Active
