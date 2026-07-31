---
title: External Documentation Digestion Master Plan — OpenClaw Docs (docs.openclaw.ai)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
source_index: https://docs.openclaw.ai/llms.txt
---

# Master Plan: Digest the OpenClaw Documentation into Vault Notes

> **Index hub only** (per `/tessellum-plan-digestion` Step 1e). This file holds shared decisions + the
> sub-plan index. Per-note tables, section coverage maps, and gate tables live in each **self-contained
> sub-plan**, authored from a fresh re-read of its source pages, then run through
> `/tessellum-augment-digestion-plan` → `/tessellum-review-digestion-plan` before execution.

## Objective

Digest the official OpenClaw documentation (`docs.openclaw.ai`) — **665 leaf pages** (from `llms.txt`,
22 redirects excluded), grouped into **105 sub-plans**, **~1,053 estimated notes**. OpenClaw is the
open-source self-hosted gateway that connects 11+ chat platforms to AI coding agents (the upstream of the
complementary to those code notes.

## Source

- **Local mirror (digestion source, NOT vault notes):** `inbox/openclaw_docs/<slug>.md` (665 `.md`, verbatim
  copies; append `.md` to any `docs.openclaw.ai/<slug>` URL).
- Page index: `docs.openclaw.ai/llms.txt`. Manifests used to build this plan: `/tmp/openclaw_pages.json`,
  `/tmp/openclaw_subplans.json` (regenerate from `llms.txt` if stale).
- Per-page measured stats (`wc -w` / grep) recorded during each sub-plan's authoring; **each sub-plan MUST
  re-read its assigned pages** for the section coverage map (measured, not estimated — Step 1c/Step 8).

## Routing Decision (Shared)

- **Location:** `resources/documentation/openclaw/`  **Prefix:** `oc_<topic>_*.md`  (NEW subfolder)
- **Rationale (3-criterion):** open-source product documentation for a coding-agent dev tool, directly
  analogous to the existing `claude_code/` (`cc_*`), `pi/` (`pi_*`), and `hermes_agent/` (`hermes_*`)
  corpora. Novelty HIGH (no `openclaw/` docs folder), operational relevance HIGH (OpenClaw is the FZ 15
  integration target), maintenance MEDIUM. >15-note series ⇒ dedicated subfolder.
- **Scan-script mapping (W4, DONE 2026-06-20):** `scripts/notes_scan.py` `FOLDER_TO_SUBCATEGORY` maps
  `"openclaw": "dev_tool_docs"`; verified `resources/documentation/openclaw/* → dev_tool_docs`.

## Dedup Policy (Shared) — REQUIRED before authoring ANY note

The vault already covers OpenClaw heavily on the code side. Before creating ANY note, each sub-plan MUST run
the three-way existence check across `term_dictionary/` AND `resources/documentation/` AND the existing
grep). Outcome per candidate: (1) no note → create; (2) stub → fill; (3) **substantive note exists (term OR
doc OR repo) → do NOT recreate; link, or enrich via `/tessellum-update-feedback`**. Adversarial dedup-verify
any merge before applying.

**Known substantive existing notes to LINK (not duplicate):** `repo_openclaw` (+ `_agents`, `_apps`,
`_channels`, `_channels_messaging`, `_channels_voice_phone`, `_cli_wizard`, `_extensions`,
`_extensions_llm_providers`, `_extensions_voice_speech`, `_gateway`, `_memory`, `_security`, `_sessions`,
`term_agent_harness`, `term_autonomous_coding_agents`, `term_function_calling`, `term_sandbox`,
`term_llm`, `term_claude`, `term_oauth_token`, `term_websocket`, `term_json_rpc`, `term_cron`; the FZ 15

## Undigested Terms — Corpus-Wide Inventory + Ownership (Step 4e)

> **Design decision (mirrors the `claude_code` / `pi` precedents):** OpenClaw vocabulary terms are the
> *subjects of dedicated doc pages*, so they are digested as **documentation concept notes (`oc_*`) by their
> home sub-plan**, NOT as new `term_dictionary` entries. The only `term_dictionary` interaction is **linking
> existing** terms. Each sub-plan's augment re-runs Step 2d; a genuinely cross-cutting, vault-reusable term
> with no doc-page home AND no existing note is captured via `/tessellum-capture-term-note` + added to its
> acronym glossary (expected near-0; the agentic/LLM glossary is already rich). **No term definition is ever
> inlined in an `oc_*` digest note.**

## Format Definition (Shared) — aligned to existing `resources/documentation/` notes

Derived from the existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora (closest precedent: same
source type — open-source coding-agent docs). Match exactly; inherited verbatim by every sub-plan.

### YAML frontmatter (fixed field order)
```yaml
---
tags:                       # itemized; first two ALWAYS resource, documentation; third ALWAYS openclaw
  - resource
  - documentation
  - openclaw
  - <area_tag>             # e.g. channels, gateway, cli, providers, tools, plugins, automation, concepts
  - <subtopic_tag>         # 0–2 optional
keywords:                   # itemized; 5–12 lowercase search phrases
topics:                     # itemized; first ALWAYS "OpenClaw"
  - OpenClaw
  - <specific area>
language: markdown
date of note: 2026-06-20
status: active
building_block: <concept | procedure | model | argument>
source_url: https://docs.openclaw.ai/<slug>
access_control_group: ["general"]
---
```
- **Forbidden YAML fields:** title, category, created, updated, source, parent, author, related_wiki,
  note_second_category, last_updated.

### Body structure
- `# OpenClaw — <Descriptive Title>` → `## Overview` (1–2 paragraphs) → source-mirrored body H2/H3 (one BB
  per note) → `## Related Notes` (**≥6 relevancy-selected `term_dictionary/` term notes** + sibling `oc_*` +
  `repo_openclaw*` + other vault notes, each an indexed link WITH a relevance statement) → `## References`
  (external URLs only) → bold footer `**Source**` / `**Last Updated**` / `**Status**`.
- Density caps: ≤400 lines, ≤2500 words, ≤6 code blocks; one building_block per note.

## Sub-Plans Index

| # | Sub-Plan File | Section | Pages | Notes (est.) | Priority | Status |
|---|---|---|---:|---:|---|---|
| pl01 | `plan_digest_openclaw_docs_pl01.md` | Plugins | 7 | 11 | P3 | pending |
| pl02 | `plan_digest_openclaw_docs_pl02.md` | Plugins | 7 | 11 | P3 | pending |
| pl03 | `plan_digest_openclaw_docs_pl03.md` | Plugins | 7 | 11 | P3 | pending |
| pl04 | `plan_digest_openclaw_docs_pl04.md` | Plugins | 7 | 11 | P3 | pending |
| pl05 | `plan_digest_openclaw_docs_pl05.md` | Plugins | 7 | 11 | P3 | pending |
| pl06 | `plan_digest_openclaw_docs_pl06.md` | Plugins | 7 | 11 | P3 | pending |
| pl07 | `plan_digest_openclaw_docs_pl07.md` | Plugins | 7 | 11 | P3 | pending |
| pl08 | `plan_digest_openclaw_docs_pl08.md` | Plugins | 7 | 11 | P3 | pending |
| pl09 | `plan_digest_openclaw_docs_pl09.md` | Plugins | 7 | 11 | P3 | pending |
| pl10 | `plan_digest_openclaw_docs_pl10.md` | Plugins | 7 | 11 | P3 | pending |
| pl11 | `plan_digest_openclaw_docs_pl11.md` | Plugins | 7 | 11 | P3 | pending |
| pl12 | `plan_digest_openclaw_docs_pl12.md` | Plugins | 7 | 11 | P3 | pending |
| pl13 | `plan_digest_openclaw_docs_pl13.md` | Plugins | 7 | 11 | P3 | pending |
| pl14 | `plan_digest_openclaw_docs_pl14.md` | Plugins | 7 | 11 | P3 | pending |
| pl15 | `plan_digest_openclaw_docs_pl15.md` | Plugins | 7 | 11 | P3 | pending |
| pl16 | `plan_digest_openclaw_docs_pl16.md` | Plugins | 7 | 11 | P3 | pending |
| pl17 | `plan_digest_openclaw_docs_pl17.md` | Plugins | 7 | 11 | P3 | pending |
| pl18 | `plan_digest_openclaw_docs_pl18.md` | Plugins | 7 | 11 | P3 | pending |
| pl19 | `plan_digest_openclaw_docs_pl19.md` | Plugins | 7 | 11 | P3 | pending |
| pl20 | `plan_digest_openclaw_docs_pl20.md` | Plugins | 7 | 11 | P3 | pending |
| pl21 | `plan_digest_openclaw_docs_pl21.md` | Plugins | 7 | 11 | P3 | pending |
| pl22 | `plan_digest_openclaw_docs_pl22.md` | Plugins | 7 | 11 | P3 | pending |
| pl23 | `plan_digest_openclaw_docs_pl23.md` | Plugins | 7 | 11 | P3 | pending |
| pl24 | `plan_digest_openclaw_docs_pl24.md` | Plugins | 7 | 11 | P3 | pending |
| pl25 | `plan_digest_openclaw_docs_pl25.md` | Plugins | 7 | 11 | P3 | pending |
| pr01 | `plan_digest_openclaw_docs_pr01.md` | Providers | 7 | 11 | P2 | pending |
| pr02 | `plan_digest_openclaw_docs_pr02.md` | Providers | 7 | 11 | P2 | pending |
| pr03 | `plan_digest_openclaw_docs_pr03.md` | Providers | 7 | 11 | P2 | pending |
| pr04 | `plan_digest_openclaw_docs_pr04.md` | Providers | 7 | 11 | P2 | pending |
| pr05 | `plan_digest_openclaw_docs_pr05.md` | Providers | 7 | 11 | P2 | pending |
| pr06 | `plan_digest_openclaw_docs_pr06.md` | Providers | 7 | 11 | P2 | pending |
| pr07 | `plan_digest_openclaw_docs_pr07.md` | Providers | 7 | 11 | P2 | pending |
| pr08 | `plan_digest_openclaw_docs_pr08.md` | Providers | 7 | 11 | P2 | pending |
| pr09 | `plan_digest_openclaw_docs_pr09.md` | Providers | 6 | 10 | P2 | pending |
| cl01 | `plan_digest_openclaw_docs_cl01.md` | CLI | 7 | 11 | P1 | pending |
| cl02 | `plan_digest_openclaw_docs_cl02.md` | CLI | 7 | 11 | P1 | pending |
| cl03 | `plan_digest_openclaw_docs_cl03.md` | CLI | 7 | 11 | P1 | pending |
| cl04 | `plan_digest_openclaw_docs_cl04.md` | CLI | 7 | 11 | P1 | pending |
| cl05 | `plan_digest_openclaw_docs_cl05.md` | CLI | 7 | 11 | P1 | pending |
| cl06 | `plan_digest_openclaw_docs_cl06.md` | CLI | 7 | 11 | P1 | pending |
| cl07 | `plan_digest_openclaw_docs_cl07.md` | CLI | 7 | 11 | P1 | pending |
| cl08 | `plan_digest_openclaw_docs_cl08.md` | CLI | 7 | 11 | P1 | pending |
| cl09 | `plan_digest_openclaw_docs_cl09.md` | CLI | 2 | 3 | P1 | pending |
| to01 | `plan_digest_openclaw_docs_to01.md` | Tools | 7 | 11 | P2 | pending |
| to02 | `plan_digest_openclaw_docs_to02.md` | Tools | 7 | 11 | P2 | pending |
| to03 | `plan_digest_openclaw_docs_to03.md` | Tools | 7 | 11 | P2 | pending |
| to04 | `plan_digest_openclaw_docs_to04.md` | Tools | 7 | 11 | P2 | pending |
| to05 | `plan_digest_openclaw_docs_to05.md` | Tools | 7 | 11 | P2 | pending |
| to06 | `plan_digest_openclaw_docs_to06.md` | Tools | 7 | 11 | P2 | pending |
| to07 | `plan_digest_openclaw_docs_to07.md` | Tools | 7 | 11 | P2 | pending |
| to08 | `plan_digest_openclaw_docs_to08.md` | Tools | 7 | 11 | P2 | pending |
| co01 | `plan_digest_openclaw_docs_co01.md` | Concepts | 7 | 11 | P1 | pending |
| co02 | `plan_digest_openclaw_docs_co02.md` | Concepts | 7 | 11 | P1 | pending |
| co03 | `plan_digest_openclaw_docs_co03.md` | Concepts | 7 | 11 | P1 | pending |
| co04 | `plan_digest_openclaw_docs_co04.md` | Concepts | 7 | 11 | P1 | pending |
| co05 | `plan_digest_openclaw_docs_co05.md` | Concepts | 7 | 11 | P1 | pending |
| co06 | `plan_digest_openclaw_docs_co06.md` | Concepts | 7 | 11 | P1 | pending |
| co07 | `plan_digest_openclaw_docs_co07.md` | Concepts | 7 | 11 | P1 | pending |
| gw01 | `plan_digest_openclaw_docs_gw01.md` | Gateway | 7 | 11 | P1 | pending |
| gw02 | `plan_digest_openclaw_docs_gw02.md` | Gateway | 7 | 11 | P1 | pending |
| gw03 | `plan_digest_openclaw_docs_gw03.md` | Gateway | 7 | 11 | P1 | pending |
| gw04 | `plan_digest_openclaw_docs_gw04.md` | Gateway | 7 | 11 | P1 | pending |
| gw05 | `plan_digest_openclaw_docs_gw05.md` | Gateway | 7 | 11 | P1 | pending |
| gw06 | `plan_digest_openclaw_docs_gw06.md` | Gateway | 7 | 11 | P1 | pending |
| gw07 | `plan_digest_openclaw_docs_gw07.md` | Gateway | 3 | 5 | P1 | pending |
| ch01 | `plan_digest_openclaw_docs_ch01.md` | Channels | 7 | 11 | P2 | pending |
| ch02 | `plan_digest_openclaw_docs_ch02.md` | Channels | 7 | 11 | P2 | pending |
| ch03 | `plan_digest_openclaw_docs_ch03.md` | Channels | 7 | 11 | P2 | pending |
| ch04 | `plan_digest_openclaw_docs_ch04.md` | Channels | 7 | 11 | P2 | pending |
| ch05 | `plan_digest_openclaw_docs_ch05.md` | Channels | 7 | 11 | P2 | pending |
| ch06 | `plan_digest_openclaw_docs_ch06.md` | Channels | 6 | 10 | P2 | pending |
| rf01 | `plan_digest_openclaw_docs_rf01.md` | Reference | 7 | 11 | P2 | pending |
| rf02 | `plan_digest_openclaw_docs_rf02.md` | Reference | 7 | 11 | P2 | pending |
| rf03 | `plan_digest_openclaw_docs_rf03.md` | Reference | 7 | 11 | P2 | pending |
| rf04 | `plan_digest_openclaw_docs_rf04.md` | Reference | 7 | 11 | P2 | pending |
| rf05 | `plan_digest_openclaw_docs_rf05.md` | Reference | 5 | 8 | P2 | pending |
| in01 | `plan_digest_openclaw_docs_in01.md` | Install | 6 | 10 | P1 | pending |
| in02 | `plan_digest_openclaw_docs_in02.md` | Install | 6 | 10 | P1 | pending |
| in03 | `plan_digest_openclaw_docs_in03.md` | Install | 6 | 10 | P1 | pending |
| in04 | `plan_digest_openclaw_docs_in04.md` | Install | 6 | 10 | P1 | pending |
| in05 | `plan_digest_openclaw_docs_in05.md` | Install | 6 | 10 | P1 | pending |
| pf01 | `plan_digest_openclaw_docs_pf01.md` | Platforms | 6 | 10 | P2 | pending |
| pf02 | `plan_digest_openclaw_docs_pf02.md` | Platforms | 6 | 10 | P2 | pending |
| pf03 | `plan_digest_openclaw_docs_pf03.md` | Platforms | 6 | 10 | P2 | pending |
| pf04 | `plan_digest_openclaw_docs_pf04.md` | Platforms | 5 | 8 | P2 | pending |
| rt01 | `plan_digest_openclaw_docs_rt01.md` | Top-level | 7 | 11 | P1 | pending |
| rt02 | `plan_digest_openclaw_docs_rt02.md` | Top-level | 7 | 11 | P1 | pending |
| rt03 | `plan_digest_openclaw_docs_rt03.md` | Top-level | 7 | 11 | P1 | pending |
| cw01 | `plan_digest_openclaw_docs_cw01.md` | ClawHub | 6 | 10 | P2 | pending |
| cw02 | `plan_digest_openclaw_docs_cw02.md` | ClawHub | 6 | 10 | P2 | pending |
| cw03 | `plan_digest_openclaw_docs_cw03.md` | ClawHub | 5 | 8 | P2 | pending |
| st01 | `plan_digest_openclaw_docs_st01.md` | Start / Getting Started | 7 | 11 | P1 | pending |
| st02 | `plan_digest_openclaw_docs_st02.md` | Start / Getting Started | 7 | 11 | P1 | pending |
| hp01 | `plan_digest_openclaw_docs_hp01.md` | Help | 5 | 8 | P2 | pending |
| hp02 | `plan_digest_openclaw_docs_hp02.md` | Help | 5 | 8 | P2 | pending |
| nd01 | `plan_digest_openclaw_docs_nd01.md` | Nodes | 4 | 6 | P1 | pending |
| nd02 | `plan_digest_openclaw_docs_nd02.md` | Nodes | 4 | 6 | P1 | pending |
| au01 | `plan_digest_openclaw_docs_au01.md` | Automation | 5 | 8 | P1 | pending |
| se01 | `plan_digest_openclaw_docs_se01.md` | Security | 5 | 8 | P1 | pending |
| rx01 | `plan_digest_openclaw_docs_rx01.md` | Refactor | 4 | 6 | P2 | pending |
| wb01 | `plan_digest_openclaw_docs_wb01.md` | Web | 4 | 6 | P2 | pending |
| pn01 | `plan_digest_openclaw_docs_pn01.md` | Plan | 2 | 3 | P2 | pending |
| an01 | `plan_digest_openclaw_docs_an01.md` | Announcements | 1 | 2 | P2 | pending |
| db01 | `plan_digest_openclaw_docs_db01.md` | Debug | 1 | 2 | P2 | pending |
| dg01 | `plan_digest_openclaw_docs_dg01.md` | Diagnostics | 1 | 2 | P2 | pending |

**Total: 105 sub-plans, 665 pages, ~1,053 estimated notes.** Final counts lock during each sub-plan's augmentation.

## Page → Sub-Plan Assignment (exhaustive — all 665 pages, each assigned once)

- **pl01** (Plugins): `plugins/adding-capabilities`, `plugins/admin-http-rpc`, `plugins/architecture`, `plugins/architecture-internals`, `plugins/building-plugins`, `plugins/bundles`, `plugins/cli-backend-plugins`
- **pl02** (Plugins): `plugins/codex-computer-use`, `plugins/codex-harness`, `plugins/codex-harness-reference`, `plugins/codex-harness-runtime`, `plugins/codex-native-plugins`, `plugins/community`, `plugins/compatibility`
- **pl03** (Plugins): `plugins/copilot`, `plugins/dependency-resolution`, `plugins/google-meet`, `plugins/hooks`, `plugins/install-overrides`, `plugins/llama-cpp`, `plugins/manage-plugins`
- **pl04** (Plugins): `plugins/manifest`, `plugins/memory-lancedb`, `plugins/memory-wiki`, `plugins/message-presentation`, `plugins/oc-path`, `plugins/plugin-inventory`, `plugins/plugin-permission-requests`
- **pl05** (Plugins): `plugins/reference`, `plugins/reference/acpx`, `plugins/reference/admin-http-rpc`, `plugins/reference/alibaba`, `plugins/reference/amazon-bedrock`, `plugins/reference/amazon-bedrock-mantle`, `plugins/reference/anthropic`
- **pl06** (Plugins): `plugins/reference/anthropic-vertex`, `plugins/reference/arcee`, `plugins/reference/azure-speech`, `plugins/reference/bonjour`, `plugins/reference/brave`, `plugins/reference/browser`, `plugins/reference/byteplus`
- **pl07** (Plugins): `plugins/reference/canvas`, `plugins/reference/cerebras`, `plugins/reference/chutes`, `plugins/reference/clickclack`, `plugins/reference/cloudflare-ai-gateway`, `plugins/reference/codex`, `plugins/reference/codex-supervisor`
- **pl08** (Plugins): `plugins/reference/cohere`, `plugins/reference/comfy`, `plugins/reference/copilot`, `plugins/reference/copilot-proxy`, `plugins/reference/deepgram`, `plugins/reference/deepinfra`, `plugins/reference/deepseek`
- **pl09** (Plugins): `plugins/reference/diagnostics-otel`, `plugins/reference/diagnostics-prometheus`, `plugins/reference/diffs`, `plugins/reference/diffs-language-pack`, `plugins/reference/discord`, `plugins/reference/document-extract`, `plugins/reference/duckduckgo`
- **pl10** (Plugins): `plugins/reference/elevenlabs`, `plugins/reference/exa`, `plugins/reference/fal`, `plugins/reference/feishu`, `plugins/reference/file-transfer`, `plugins/reference/firecrawl`, `plugins/reference/fireworks`
- **pl11** (Plugins): `plugins/reference/github-copilot`, `plugins/reference/gmi`, `plugins/reference/google`, `plugins/reference/google-meet`, `plugins/reference/googlechat`, `plugins/reference/gradium`, `plugins/reference/groq`
- **pl12** (Plugins): `plugins/reference/huggingface`, `plugins/reference/imessage`, `plugins/reference/inworld`, `plugins/reference/irc`, `plugins/reference/kilocode`, `plugins/reference/kimi`, `plugins/reference/line`
- **pl13** (Plugins): `plugins/reference/litellm`, `plugins/reference/llama-cpp`, `plugins/reference/llm-task`, `plugins/reference/lmstudio`, `plugins/reference/lobster`, `plugins/reference/matrix`, `plugins/reference/mattermost`
- **pl14** (Plugins): `plugins/reference/memory-core`, `plugins/reference/memory-lancedb`, `plugins/reference/memory-wiki`, `plugins/reference/microsoft`, `plugins/reference/microsoft-foundry`, `plugins/reference/migrate-claude`, `plugins/reference/migrate-hermes`
- **pl15** (Plugins): `plugins/reference/minimax`, `plugins/reference/mistral`, `plugins/reference/moonshot`, `plugins/reference/msteams`, `plugins/reference/nextcloud-talk`, `plugins/reference/nostr`, `plugins/reference/novita`
- **pl16** (Plugins): `plugins/reference/nvidia`, `plugins/reference/oc-path`, `plugins/reference/ollama`, `plugins/reference/open-prose`, `plugins/reference/openai`, `plugins/reference/opencode`, `plugins/reference/opencode-go`
- **pl17** (Plugins): `plugins/reference/openrouter`, `plugins/reference/openshell`, `plugins/reference/perplexity`, `plugins/reference/pixverse`, `plugins/reference/policy`, `plugins/reference/qa-channel`, `plugins/reference/qa-lab`
- **pl18** (Plugins): `plugins/reference/qa-matrix`, `plugins/reference/qianfan`, `plugins/reference/qqbot`, `plugins/reference/qwen`, `plugins/reference/runway`, `plugins/reference/searxng`, `plugins/reference/senseaudio`
- **pl19** (Plugins): `plugins/reference/sglang`, `plugins/reference/signal`, `plugins/reference/slack`, `plugins/reference/sms`, `plugins/reference/stepfun`, `plugins/reference/synology-chat`, `plugins/reference/synthetic`
- **pl20** (Plugins): `plugins/reference/tavily`, `plugins/reference/telegram`, `plugins/reference/tencent`, `plugins/reference/tlon`, `plugins/reference/together`, `plugins/reference/tokenjuice`, `plugins/reference/tts-local-cli`
- **pl21** (Plugins): `plugins/reference/twitch`, `plugins/reference/venice`, `plugins/reference/vercel-ai-gateway`, `plugins/reference/vllm`, `plugins/reference/voice-call`, `plugins/reference/volcengine`, `plugins/reference/voyage`
- **pl22** (Plugins): `plugins/reference/vydra`, `plugins/reference/web-readability`, `plugins/reference/webhooks`, `plugins/reference/whatsapp`, `plugins/reference/workboard`, `plugins/reference/xai`, `plugins/reference/xiaomi`
- **pl23** (Plugins): `plugins/reference/zai`, `plugins/reference/zalo`, `plugins/reference/zalouser`, `plugins/sdk-agent-harness`, `plugins/sdk-channel-inbound`, `plugins/sdk-channel-ingress`, `plugins/sdk-channel-outbound`
- **pl24** (Plugins): `plugins/sdk-channel-plugins`, `plugins/sdk-entrypoints`, `plugins/sdk-migration`, `plugins/sdk-overview`, `plugins/sdk-provider-plugins`, `plugins/sdk-runtime`, `plugins/sdk-setup`
- **pl25** (Plugins): `plugins/sdk-subpaths`, `plugins/sdk-testing`, `plugins/tool-plugins`, `plugins/voice-call`, `plugins/webhooks`, `plugins/workboard`, `plugins/zalouser`
- **pr01** (Providers): `providers/alibaba`, `providers/anthropic`, `providers/arcee`, `providers/azure-speech`, `providers/bedrock`, `providers/bedrock-mantle`, `providers/cerebras`
- **pr02** (Providers): `providers/chutes`, `providers/claude-max-api-proxy`, `providers/cloudflare-ai-gateway`, `providers/cohere`, `providers/comfy`, `providers/deepgram`, `providers/deepinfra`
- **pr03** (Providers): `providers/deepseek`, `providers/ds4`, `providers/elevenlabs`, `providers/fal`, `providers/fireworks`, `providers/github-copilot`, `providers/gmi`
- **pr04** (Providers): `providers/google`, `providers/gradium`, `providers/groq`, `providers/huggingface`, `providers/inferrs`, `providers/inworld`, `providers/kilocode`
- **pr05** (Providers): `providers/litellm`, `providers/lmstudio`, `providers/minimax`, `providers/mistral`, `providers/models`, `providers/moonshot`, `providers/novita`
- **pr06** (Providers): `providers/nvidia`, `providers/ollama`, `providers/ollama-cloud`, `providers/openai`, `providers/opencode`, `providers/opencode-go`, `providers/openrouter`
- **pr07** (Providers): `providers/perplexity-provider`, `providers/pixverse`, `providers/qianfan`, `providers/qwen`, `providers/qwen-oauth`, `providers/runway`, `providers/senseaudio`
- **pr08** (Providers): `providers/sglang`, `providers/stepfun`, `providers/synthetic`, `providers/tencent`, `providers/together`, `providers/venice`, `providers/vercel-ai-gateway`
- **pr09** (Providers): `providers/vllm`, `providers/volcengine`, `providers/vydra`, `providers/xai`, `providers/xiaomi`, `providers/zai`
- **cl01** (CLI): `cli/acp`, `cli/agent`, `cli/agents`, `cli/approvals`, `cli/backup`, `cli/browser`, `cli/channels`
- **cl02** (CLI): `cli/clawbot`, `cli/commitments`, `cli/completion`, `cli/config`, `cli/configure`, `cli/crestodian`, `cli/cron`
- **cl03** (CLI): `cli/daemon`, `cli/dashboard`, `cli/devices`, `cli/directory`, `cli/dns`, `cli/docs`, `cli/doctor`
- **cl04** (CLI): `cli/gateway`, `cli/health`, `cli/hooks`, `cli/infer`, `cli/logs`, `cli/mcp`, `cli/memory`
- **cl05** (CLI): `cli/message`, `cli/migrate`, `cli/models`, `cli/node`, `cli/nodes`, `cli/onboard`, `cli/pairing`
- **cl06** (CLI): `cli/path`, `cli/plugins`, `cli/policy`, `cli/proxy`, `cli/qr`, `cli/reset`, `cli/sandbox`
- **cl07** (CLI): `cli/secrets`, `cli/security`, `cli/sessions`, `cli/setup`, `cli/skills`, `cli/status`, `cli/system`
- **cl08** (CLI): `cli/tasks`, `cli/transcripts`, `cli/tui`, `cli/uninstall`, `cli/update`, `cli/voicecall`, `cli/webhooks`
- **cl09** (CLI): `cli/wiki`, `cli/workboard`
- **to01** (Tools): `tools/acp-agents`, `tools/acp-agents-setup`, `tools/agent-send`, `tools/apply-patch`, `tools/brave-search`, `tools/browser`, `tools/browser-control`
- **to02** (Tools): `tools/browser-linux-troubleshooting`, `tools/browser-login`, `tools/browser-wsl2-windows-remote-cdp-troubleshooting`, `tools/btw`, `tools/code-execution`, `tools/creating-skills`, `tools/diffs`
- **to03** (Tools): `tools/duckduckgo-search`, `tools/elevated`, `tools/exa-search`, `tools/exec`, `tools/exec-approvals`, `tools/exec-approvals-advanced`, `tools/firecrawl`
- **to04** (Tools): `tools/gemini-search`, `tools/goal`, `tools/grok-search`, `tools/image-generation`, `tools/kimi-search`, `tools/llm-task`, `tools/lobster`
- **to05** (Tools): `tools/loop-detection`, `tools/media-overview`, `tools/minimax-search`, `tools/multi-agent-sandbox-tools`, `tools/music-generation`, `tools/ollama-search`, `tools/parallel-search`
- **to06** (Tools): `tools/pdf`, `tools/permission-modes`, `tools/perplexity-search`, `tools/plugin`, `tools/reactions`, `tools/searxng-search`, `tools/skill-workshop`
- **to07** (Tools): `tools/skills`, `tools/skills-config`, `tools/slash-commands`, `tools/steer`, `tools/subagents`, `tools/tavily`, `tools/thinking`
- **to08** (Tools): `tools/tokenjuice`, `tools/tool-search`, `tools/trajectory`, `tools/tts`, `tools/video-generation`, `tools/web`, `tools/web-fetch`
- **co01** (Concepts): `concepts/active-memory`, `concepts/agent`, `concepts/agent-loop`, `concepts/agent-runtimes`, `concepts/agent-workspace`, `concepts/architecture`, `concepts/channel-docking`
- **co02** (Concepts): `concepts/commitments`, `concepts/compaction`, `concepts/context`, `concepts/context-engine`, `concepts/delegate-architecture`, `concepts/dreaming`, `concepts/experimental-features`
- **co03** (Concepts): `concepts/features`, `concepts/mantis`, `concepts/mantis-slack-desktop-runbook`, `concepts/markdown-formatting`, `concepts/memory`, `concepts/memory-builtin`, `concepts/memory-honcho`
- **co04** (Concepts): `concepts/memory-qmd`, `concepts/memory-search`, `concepts/message-lifecycle-refactor`, `concepts/messages`, `concepts/model-failover`, `concepts/model-providers`, `concepts/models`
- **co05** (Concepts): `concepts/multi-agent`, `concepts/oauth`, `concepts/parallel-specialist-lanes`, `concepts/personal-agent-benchmark-pack`, `concepts/presence`, `concepts/progress-drafts`, `concepts/qa-e2e-automation`
- **co06** (Concepts): `concepts/qa-matrix`, `concepts/queue`, `concepts/queue-steering`, `concepts/retry`, `concepts/session`, `concepts/session-pruning`, `concepts/session-tool`
- **co07** (Concepts): `concepts/soul`, `concepts/streaming`, `concepts/system-prompt`, `concepts/timezone`, `concepts/typebox`, `concepts/typing-indicators`, `concepts/usage-tracking`
- **gw01** (Gateway): `gateway/authentication`, `gateway/background-process`, `gateway/bonjour`, `gateway/bridge-protocol`, `gateway/cli-backends`, `gateway/config-agents`, `gateway/config-channels`
- **gw02** (Gateway): `gateway/config-tools`, `gateway/configuration`, `gateway/configuration-examples`, `gateway/configuration-reference`, `gateway/diagnostics`, `gateway/discovery`, `gateway/doctor`
- **gw03** (Gateway): `gateway/external-apps`, `gateway/gateway-lock`, `gateway/health`, `gateway/heartbeat`, `gateway/local-model-services`, `gateway/local-models`, `gateway/logging`
- **gw04** (Gateway): `gateway/multiple-gateways`, `gateway/openai-http-api`, `gateway/openresponses-http-api`, `gateway/openshell`, `gateway/opentelemetry`, `gateway/operator-scopes`, `gateway/pairing`
- **gw05** (Gateway): `gateway/prometheus`, `gateway/protocol`, `gateway/remote`, `gateway/remote-gateway-readme`, `gateway/sandbox-vs-tool-policy-vs-elevated`, `gateway/sandboxing`, `gateway/secrets`
- **gw06** (Gateway): `gateway/secrets-plan-contract`, `gateway/security`, `gateway/security/audit-checks`, `gateway/security/exposure-runbook`, `gateway/security/secure-file-operations`, `gateway/security/shrinkwrap`, `gateway/tailscale`
- **gw07** (Gateway): `gateway/tools-invoke-http-api`, `gateway/troubleshooting`, `gateway/trusted-proxy-auth`
- **ch01** (Channels): `channels/access-groups`, `channels/ambient-room-events`, `channels/bot-loop-protection`, `channels/broadcast-groups`, `channels/channel-routing`, `channels/clickclack`, `channels/discord`
- **ch02** (Channels): `channels/feishu`, `channels/googlechat`, `channels/group-messages`, `channels/groups`, `channels/imessage`, `channels/imessage-from-bluebubbles`, `channels/irc`
- **ch03** (Channels): `channels/line`, `channels/location`, `channels/matrix`, `channels/matrix-migration`, `channels/matrix-presentation`, `channels/matrix-push-rules`, `channels/mattermost`
- **ch04** (Channels): `channels/msteams`, `channels/nextcloud-talk`, `channels/nostr`, `channels/pairing`, `channels/qa-channel`, `channels/qqbot`, `channels/signal`
- **ch05** (Channels): `channels/slack`, `channels/sms`, `channels/synology-chat`, `channels/telegram`, `channels/tlon`, `channels/troubleshooting`, `channels/twitch`
- **ch06** (Channels): `channels/wechat`, `channels/whatsapp`, `channels/yuanbao`, `channels/zalo`, `channels/zaloclawbot`, `channels/zalouser`
- **rf01** (Reference): `reference/AGENTS.default`, `reference/RELEASING`, `reference/api-usage-costs`, `reference/application-modernization-plan`, `reference/code-mode`, `reference/credits`, `reference/device-models`
- **rf02** (Reference): `reference/full-release-validation`, `reference/memory-config`, `reference/prompt-caching`, `reference/release-performance-sweep`, `reference/rich-output-protocol`, `reference/rpc`, `reference/secret-placeholder-conventions`
- **rf03** (Reference): `reference/secretref-credential-surface`, `reference/session-management-compaction`, `reference/templates/AGENTS.dev`, `reference/templates/BOOT`, `reference/templates/BOOTSTRAP`, `reference/templates/CLAUDE`, `reference/templates/HEARTBEAT`
- **rf04** (Reference): `reference/templates/IDENTITY`, `reference/templates/IDENTITY.dev`, `reference/templates/SOUL`, `reference/templates/SOUL.dev`, `reference/templates/TOOLS`, `reference/templates/TOOLS.dev`, `reference/templates/USER`
- **rf05** (Reference): `reference/templates/USER.dev`, `reference/test`, `reference/token-use`, `reference/transcript-hygiene`, `reference/wizard`
- **in01** (Install): `install/ansible`, `install/azure`, `install/bun`, `install/clawdock`, `install/development-channels`, `install/digitalocean`
- **in02** (Install): `install/docker`, `install/docker-vm-runtime`, `install/exe-dev`, `install/fly`, `install/gcp`, `install/hetzner`
- **in03** (Install): `install/hostinger`, `install/installer`, `install/kubernetes`, `install/macos-vm`, `install/migrating`, `install/migrating-claude`
- **in04** (Install): `install/migrating-hermes`, `install/nix`, `install/node`, `install/northflank`, `install/oracle`, `install/podman`
- **in05** (Install): `install/railway`, `install/raspberry-pi`, `install/render`, `install/uninstall`, `install/updating`, `install/upstash`
- **pf01** (Platforms): `platforms/android`, `platforms/easyrunner`, `platforms/ios`, `platforms/linux`, `platforms/mac/bundled-gateway`, `platforms/mac/canvas`
- **pf02** (Platforms): `platforms/mac/child-process`, `platforms/mac/dev-setup`, `platforms/mac/health`, `platforms/mac/icon`, `platforms/mac/logging`, `platforms/mac/menu-bar`
- **pf03** (Platforms): `platforms/mac/peekaboo`, `platforms/mac/permissions`, `platforms/mac/remote`, `platforms/mac/signing`, `platforms/mac/skills`, `platforms/mac/voice-overlay`
- **pf04** (Platforms): `platforms/mac/voicewake`, `platforms/mac/webchat`, `platforms/mac/xpc`, `platforms/macos`, `platforms/windows`
- **rt01** (Top-level): `agent-runtime-architecture`, `auth-credential-semantics`, `automation`, `channels`, `ci`, `clawhub`, `cli`
- **rt02** (Top-level): `date-time`, `gateway`, `help`, `install`, `logging`, `network`, `nodes`
- **rt03** (Top-level): `openclaw-agent-runtime`, `platforms`, `prose`, `providers`, `tools`, `vps`, `web`
- **cw01** (ClawHub): `clawhub/acceptable-usage`, `clawhub/api`, `clawhub/auth`, `clawhub/cli`, `clawhub/content-rights`, `clawhub/how-it-works`
- **cw02** (ClawHub): `clawhub/http-api`, `clawhub/moderation`, `clawhub/namespace-claims`, `clawhub/plugin-validation-fixes`, `clawhub/publishing`, `clawhub/quickstart`
- **cw03** (ClawHub): `clawhub/security`, `clawhub/security-audits`, `clawhub/skill-format`, `clawhub/telemetry`, `clawhub/troubleshooting`
- **st01** (Start / Getting Started): `start/bootstrapping`, `start/docs-directory`, `start/getting-started`, `start/hubs`, `start/lore`, `start/onboarding`, `start/onboarding-overview`
- **st02** (Start / Getting Started): `start/openclaw`, `start/quickstart`, `start/setup`, `start/showcase`, `start/wizard`, `start/wizard-cli-automation`, `start/wizard-cli-reference`
- **hp01** (Help): `help/debugging`, `help/environment`, `help/faq`, `help/faq-first-run`, `help/faq-models`
- **hp02** (Help): `help/scripts`, `help/testing`, `help/testing-live`, `help/testing-updates-plugins`, `help/troubleshooting`
- **nd01** (Nodes): `nodes/audio`, `nodes/camera`, `nodes/images`, `nodes/location-command`
- **nd02** (Nodes): `nodes/media-understanding`, `nodes/talk`, `nodes/troubleshooting`, `nodes/voicewake`
- **au01** (Automation): `automation/cron-jobs`, `automation/hooks`, `automation/standing-orders`, `automation/taskflow`, `automation/tasks`
- **se01** (Security): `security/CONTRIBUTING-THREAT-MODEL`, `security/THREAT-MODEL-ATLAS`, `security/formal-verification`, `security/incident-response`, `security/network-proxy`
- **rx01** (Refactor): `refactor/acp`, `refactor/canvas`, `refactor/database-first`, `refactor/ingress-core`
- **wb01** (Web): `web/control-ui`, `web/dashboard`, `web/tui`, `web/webchat`
- **pn01** (Plan): `plan/codex-context-engine-harness`, `plan/ui-channels`
- **an01** (Announcements): `announcements/bluebubbles-imessage`
- **db01** (Debug): `debug/node-issue`
- **dg01** (Diagnostics): `diagnostics/flags`

## Execution Order (by priority)

- **Phase A (P1 — conceptual/operational core, 37 sub-plans):** concepts (co01–07), CLI (cl01–09), gateway
  (gw01–07), install (in01–05), top-level (rt01–03), start (st01–02), nodes (nd01–02), automation (au01),
  security (se01). Define the architecture/runtime/gateway/CLI vocabulary the rest reference.
- **Phase B (P2 — features/integration, 43 sub-plans):** providers (pr01–09), tools (to01–08), channels
  (ch01–06), reference (rf01–05), platforms (pf01–04), clawhub (cw01–03), help (hp01–02), web (wb01),
  refactor (rx01), plan (pn01), announcements/debug/diagnostics (an01/db01/dg01).
- **Phase C (P3 — plugin reference sprawl, 25 sub-plans):** plugins (pl01–25), the 1-per-plugin pages.

Within a phase, sub-plans are independent and may run in parallel (no cross-sub-plan execution dependency).

## Per-Sub-Plan Pipeline (every sub-plan)
1. **Author** via `/tessellum-plan-digestion` Steps 2-8 from a fresh re-read of assigned pages (mirror at
   `inbox/openclaw_docs/`): inherit the Format Definition, dedup-before-create across term_dictionary AND
   documentation/ AND repo_openclaw*, section coverage map (every H2/H3 mapped), planned-notes table
   (filename + BB + source section + ~words), per-note Related mapping (≥6 relevancy terms, locked at
   augment), inlinks, split decisions, Step 2d new-term scan, per-phase 9-GATE table, density re-assessment.
2. `/tessellum-augment-digestion-plan` → 3. `/tessellum-review-digestion-plan` → READY → 4. `/tessellum-execute-digestion-plan`.

## Validation Gates (Shared — 9-GATE per execution phase of each sub-plan)
G1 Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) · G2 Grounding (diff vs
`inbox/openclaw_docs/<page>`) · G3 Density+Coverage · G4 Cross-Reference · G5 Ghost-reference detect+redirect ·
G6 Broken-link fix · G7/G8 Discoverability (every new note RECEIVES ≥1 inbound link from outside
`documentation/openclaw/`, in-degree ≥1, anti-island — satisfied via `entry_openclaw_docs.md`) ·
G9 Prose integrity (no mid-paragraph hard-wrap — each paragraph on ONE logical source line; a prose line
ending mid-sentence MUST NOT be immediately followed by another prose line; enforced by
`/tessellum-check-note-format` PROSE-001, which is an **error**, so 0 PROSE-001 per note is required).

## Cross-References (Shared — link from sub-plans)
`term_acp_agent_client_protocol`, `term_mcp`, `term_agent_harness`, `term_autonomous_coding_agents`,
`term_function_calling`, `term_sandbox`, `term_llm`, `term_claude`, `term_oauth_token`, `term_websocket`,
the FZ 15 analysis/trail notes. Sub-plan augment verifies its subset in the DB (G5) before locking.

## Series Wiring Steps (REQUIRED)
- **W1 — CREATE `0_entry_points/entry_openclaw_docs.md`** ✅ DONE 2026-06-22 (>30 notes ⇒ required):
  `building_block: navigation`; Quick Stats (665 pages, ~809 notes, 105 sub-plans); per-section/per-phase
  `entry_pi_docs`, `entry_code_repos`, `entry_gen_ai_dev`); `## References`. Built as a pre-step before the
  first sub-plan executes — per-note inbound links are filled in section-by-section as each sub-plan lands.
- **W2 — UPDATE parent hub** `0_entry_points/entry_gen_ai_dev.md` (back-link row) + the existing
- **W3 — UPDATE code↔docs cross-links:** `term_openclaw.md` + `areas/code_repos/repo_openclaw.md` → link
  `entry_openclaw_docs.md`.
- **W4 — Scan-script mapping ✅ DONE (2026-06-20):** `notes_scan.py` maps `openclaw → dev_tool_docs`.
- **W5 — New-term capture + glossary:** any new `term_dictionary` note (expected near-0) is captured via
  `/tessellum-capture-term-note` and added to its `acronym_glossary_*.md`.

## Pacing Rules (Shared)
- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script; commit per sub-plan / per wave
  (`git pull --rebase --autostash` first; no Claude co-author trailer). Reindex incrementally per wave; verify
  `note_links` + 0 broken links before commit.

## Summary Statistics
- Pages: 665 (llms.txt, redirects excluded). Sub-plans: 105. Est. notes: ~1,053.
- Section sizes: plugins 175 · providers 62 · cli 58 · tools 56 · concepts 49 · gateway 45 · channels 41 ·
  reference 33 · install 30 · top-level 21 · platforms 23 · clawhub 17 · start 14 · help 10 · nodes 8 ·
  automation 5 · security 5 · refactor 4 · web 4 · plan 2 · announcements/debug/diagnostics 1 each.
- BB skew (expected): procedure (setup/config/CLI/channel/provider/plugin how-to) dominant, with concept
  (architecture/runtime/concepts), model (event/protocol/reference schemas), some argument (security/design).

## Pipeline Status
> **Gate amendment 2026-06-22:** added **G9 Prose Integrity** (no mid-paragraph hard-wrap — each paragraph on
> ONE logical source line) to the shared 9-GATE suite and every sub-plan's gate table. Enforced at execute
> time by `/tessellum-check-note-format` PROSE-001 (an **error**, already run by `/tessellum-execute-digestion-plan`).

| Stage | Skill | Status |
|---|---|---|
| 1. Plan (master + sub-plans) | `/tessellum-plan-digestion` | ✅ DONE — master + 105/105 sub-plans authored (7 waves) + adversarially verified (all sections, measured sources, ghosts redirected). ~843 notes planned. |
| 3. Review (per sub-plan) | `/tessellum-review-digestion-plan` | ✅ DONE 2026-06-21 — 105/105 READY (9-CP sign-off each; status: ready) |

## Follow-up Recommendations
- Author the 105 sub-plan files in priority waves (Phase A → B → C), ~25–30 per workflow wave (fan-out cap).
- Before first execution: create `entry_openclaw_docs.md` + parent-hub back-link (W1/W2).
- Measured per-page word counts are recorded in each sub-plan's Source table at authoring (Step 1c).

## Execution Report (COMPLETE — 2026-06-25)

| Metric | Value |
|---|---|
| Notes created | **816 / 816** (Phase A 306 + resume 510; planned-set == disk-set, 0 missing) |
| Sub-plans executed | 105 / 105 (all `status: completed`) |
| Resume run | `plans/wf_openclaw_resume_execute.js` (68 sub-plans, capture→validate→bounded-fix); 68/68 verdict=pass |
| Capture agents that errored mid-return | 4 (`oc_channels_zalouser`, `oc_reference_templates_tools`, `oc_plugins_reference_file_transfer`, `oc_sdk_channel_outbound`) — files written before error; independently gate-verified PASS |
| Full gate suite (`digest_note_gate.sh`) across 816 | ALL PASS (after trimming `oc_plugins_sdk_overview_registration_api` 2578→2480w) |
| Format check (`check_note_format.py`) | 0 errors |
| Broken links touching openclaw | 0 |
| Ghost references from openclaw (post-fix) | **0** — 114 split-rename/slug-variant ghosts introduced by the resume were resolved via two-sided verification (`/tessellum-fix-ghost-references`): 108 redirect + 6 drop (1st pass) + 2 redirect (stragglers); 288+3 links rewritten across ~193 files |
| Vault-wide ghosts after fix | 0 |
| G8-Discoverability | all 816 indexed in `entry_openclaw_docs.md` (each has ≥1 inbound link from outside `openclaw/`) |
| `notes_scan.py` subcategory | `openclaw → dev_tool_docs` (already present) |
| Resume agents / tokens | 586 agents · ~63M subagent tokens · ~5.7h wall-clock |

**Ghost lesson (carried forward):** the resume reused the per-sub-plan LOCKED mappings, which referenced several PRE-SPLIT sibling slugs (notes split for density during authoring, e.g. `oc_gateway_protocol` → 5 children). These surfaced as 114 ghosts only after the cross-sub-plan notes all landed. Resolution was a clean redirect-dominant batch (split-child overview chosen by referrer link_context). Future resumes of a split-heavy plan should pre-scan locked mappings for pre-split stems before fan-out.

## Status

Execution complete (2026-06-25). Master + all 105 sub-plans → `completed`. 816 notes live under `resources/documentation/openclaw/`, all gates green (0 broken / 0 ghost / G8 satisfied), indexed in `entry_openclaw_docs.md`.
