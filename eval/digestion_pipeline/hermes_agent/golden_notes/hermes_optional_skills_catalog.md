---
tags:
  - resource
  - documentation
  - hermes_agent
  - skills
  - navigation
keywords:
  - optional skills catalog
  - hermes skills install
  - install on demand skills
  - official category skill
  - optional-skills directory
  - skill categories
topics:
  - Hermes Agent
  - Skills
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog
access_control_group: ["general"]
---

# Hermes Agent — Optional Skills Catalog

## Overview

The Optional Skills Catalog is the **install-on-demand index** of skills that ship inside the `hermes-agent` repository under `optional-skills/` but are **not active by default**. It is the on-demand counterpart to the bundled-skills catalog: where bundled skills load automatically at session start, optional skills are pulled in only when a reader explicitly installs them, so the agent's default surface stays lean while a large library of specialized capabilities remains one command away. Each entry names a skill, gives a one-line description, and links to a dedicated page carrying that skill's full definition, setup, and usage. This note is a navigation enumeration — it catalogs *what is available and how to install it*, not the implementation of any single skill; the skills concept and SKILL.md format live in their own term notes (see Related Notes).

Install is a single command keyed on `official/<category>/<skill>`; uninstall removes by skill name. The catalog groups skills into ~18 categories spanning autonomous AI agents, blockchain, communication, creative, devops, dogfood, email, finance, gaming, health, MCP, migration, mlops, payments, productivity, research, security, software-development, and web-development — with mlops being by far the largest cluster (training, inference, vector-search, and fine-tuning skills). The page closes with a Contributing-Optional-Skills pointer for adding new entries.

## Installing Optional Skills

Optional skills install explicitly via `hermes skills install`, keyed on the `official/<category>/<skill>` path:

```bash
hermes skills install official/<category>/<skill>
```

For example:

```bash
hermes skills install official/blockchain/solana
hermes skills install official/mlops/flash-attention
```

To uninstall, remove by skill name:

```bash
hermes skills uninstall <skill-name>
```

Each skill below links to a dedicated page with its full definition, setup, and usage.

## Skill Categories

The catalog enumerates optional skills by category. Skill names and one-line descriptions are mirrored verbatim from the source; long descriptions are condensed to their lead clause.

**autonomous-ai-agents** — `antigravity-cli` (operate the Antigravity CLI: plugins, auth, sandbox); `blackbox` (delegate coding to Blackbox AI CLI, multi-model with built-in judge); `grok` (delegate coding to xAI Grok Build CLI); `honcho` (Honcho memory with Hermes — cross-session user modeling, multi-profile peer isolation); `openhands` (delegate coding to OpenHands CLI, model-agnostic, LiteLLM).

**blockchain** — `evm` (read-only EVM client: wallets, tokens, gas across 8 chains); `hyperliquid` (Hyperliquid market data, account history, trade review); `solana` (query Solana data with USD pricing — balances, portfolios, NFTs, whale detection; Solana RPC + CoinGecko, no API key).

**communication** — `one-three-one-rule` (structured decision-making framework for technical proposals and trade-off analysis).

**creative** — `baoyu-article-illustrator` (article illustrations: type × style × palette); `baoyu-comic` (knowledge comics); `blender-mcp` (control Blender via socket to the blender-mcp addon); `concept-diagrams` (flat minimal light/dark-aware SVG diagrams as HTML); `ideation` (project ideas via creative constraints); `hyperframes` (HTML-based video compositions); `kanban-video-orchestrator` (multi-agent video production pipeline backed by Hermes Kanban); `meme-generation` (real meme images via Pillow); `pixel-art` (pixel art with era palettes).

**devops** — `inference-sh-cli` (run 150+ AI apps via inference.sh CLI); `docker-management` (manage Docker containers, images, volumes, networks, Compose); `hermes-s6-container-supervision` (modify/debug the s6-overlay supervision tree in the Hermes Docker image); `pinggy-tunnel` (zero-install localhost tunnels over SSH); `watchers` (poll RSS, JSON APIs, GitHub with watermark dedup).

**dogfood** — `adversarial-ux-test` (roleplay a difficult tech-resistant user, find UX pain points, file actionable tickets).

**email** — `agentmail` (give the agent its own dedicated email inbox via AgentMail).

**finance** — `3-statement-model`, `comps-analysis`, `dcf-model`, `excel-author`, `lbo-model`, `merger-model`, `pptx-author` (institutional-quality Excel/PowerPoint financial modeling, all pairing with `excel-author`); `stocks` (stock quotes, history, compare, crypto via Yahoo).

**gaming** — `minecraft-modpack-server` (host modded Minecraft servers); `pokemon-player` (play Pokemon via headless emulator + RAM reads).

**health** — `fitness-nutrition` (workout planner + nutrition tracker via wger and USDA FoodData Central); `neuroskill-bci` (incorporate a NeuroSkill instance's real-time cognitive/emotional state into responses).

**mcp** — `fastmcp` (build, test, inspect, install, deploy MCP servers with FastMCP in Python); `mcporter` (mcporter CLI to list, configure, auth, and call MCP servers/tools).

**migration** — `openclaw-migration` (migrate an OpenClaw customization footprint — memories, SOUL.md, allowlists, user skills — into Hermes Agent).

**mlops** (largest cluster) — distributed training and acceleration: `huggingface-accelerate`, `axolotl`, `peft-fine-tuning`, `pytorch-fsdp`, `pytorch-lightning`, `simpo-training`, `slime-rl-training`, `distributed-llm-pretraining-torchtitan`, `fine-tuning-with-trl`, `unsloth`; structured generation: `guidance`, `instructor`, `outlines`; vector search / RAG: `chroma`, `faiss`, `pinecone`, `qdrant-vector-search`; attention/inference optimization: `optimizing-attention-flash`, `tensorrt-llm`; vision/speech: `clip`, `llava`, `whisper`, `stable-diffusion-image-generation`; data + GPU cloud: `nemo-curator`, `lambda-labs-gpu-cloud`, `modal-serverless-gpu`, `huggingface-tokenizers`; research: `dspy`, `sparse-autoencoder-training`, `obliteratus`.

**payments** — `mpp-agent` (pay HTTP 402 APIs via Machine Payments Protocol); `stripe-link-cli` (agent payments via Stripe Link); `stripe-projects` (provision SaaS services + sync creds via Stripe Projects).

**productivity** — `canvas` (Canvas LMS integration); `here.now` (publish static sites + private Drives for agent-to-agent handoff); `memento-flashcards` (spaced-repetition flashcards); `shop` (catalog search, checkout, order tracking); `shopify` (Shopify Admin/Storefront GraphQL); `siyuan` (SiYuan Note API); `telephony` (Twilio SMS/MMS + AI-driven calls via Bland.ai/Vapi).

**research** — `bioinformatics` (gateway to 400+ bioinformatics skills); `darwinian-evolver` (evolve prompts/regex/SQL/code); `domain-intel` (passive domain reconnaissance); `drug-discovery` (pharmaceutical research assistant); `duckduckgo-search`, `searxng-search` (free web/meta-search, no API key); `gitnexus-explorer` (codebase knowledge graph); `osint-investigation` (public-records OSINT framework); `parallel-cli` (agent-native web search/research); `qmd` (local hybrid-retrieval knowledge-base search); `scrapling` (web scraping with stealth browser automation).

**security** — `1password` (1Password CLI `op` secret access); `godmode` (jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN); `oss-forensics` (supply-chain investigation + forensic analysis of GitHub repos); `sherlock` (OSINT username search across 400+ networks); `web-pentest` (authorized web pentesting with "No Exploit, No Report" guardrails).

**software-development** — `code-wiki` (wiki docs + Mermaid diagrams for any codebase); `rest-graphql-debug` (debug REST/GraphQL APIs); `subagent-driven-development` (execute plans via `delegate_task` subagents, 2-stage review).

**web-development** — `page-agent` (embed alibaba/page-agent — a pure-JavaScript in-page GUI agent — into your own web app).

## Contributing Optional Skills

To add a new optional skill to the repository:

1. Create a directory under `optional-skills/<category>/<skill-name>/`.
2. Add a `SKILL.md` with standard frontmatter (name, description, version, author).
3. Include supporting files in `references/`, `templates/`, or `scripts/` subdirectories.
4. Submit a pull request — the skill appears in this catalog and gets its own docs page once merged.

**Source**: `inbox/hermes_agent_docs/reference/optional-skills-catalog.md` · https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog
**Last Updated**: 2026-06-19
**Status**: Active
