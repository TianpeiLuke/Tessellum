---
tags:
  - resource
  - documentation
  - hermes_agent
  - memory
  - plugins
keywords:
  - memory provider catalog
  - external memory plugins
  - openviking mem0 hindsight
  - holographic retaindb byterover
  - supermemory memori
  - provider comparison
  - profile isolation
topics:
  - Hermes Agent
  - Memory
  - Provider Plugins
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
access_control_group: ["general"]
---

# Hermes Agent — Memory Provider Catalog

## Overview

This is the catalog of the eight non-Honcho **external memory providers** that ship with Hermes Agent — OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory, and Memori. Each is a plugin that gives the agent persistent, cross-session knowledge beyond the built-in MEMORY.md/USER.md, and only **one** external provider can be active at a time alongside the always-on built-in memory. The providers differ along storage location (local SQLite vs. self-hosted server vs. cloud API), cost, tool count, dependencies, and one unique retrieval/recall capability each. The flagship Honcho provider plus the shared provider-system lifecycle (inject → prefetch → sync → extract → mirror → tools) are documented in [hermes_memory_providers_honcho](hermes_memory_providers_honcho.md); this note covers the remaining eight, the comparison matrix, per-profile data isolation, and where to author a custom provider.

## OpenViking

Context database by Volcengine (ByteDance) with a filesystem-style knowledge hierarchy, tiered retrieval, and automatic memory extraction into 6 categories.

- **Best for**: Self-hosted knowledge management with structured browsing
- **Requires**: `pip install openviking` + running server
- **Data storage**: Self-hosted (local or cloud)
- **Cost**: Free (open-source, AGPL-3.0)

**Tools:** `viking_search` (semantic search), `viking_read` (tiered: abstract/overview/full), `viking_browse` (filesystem navigation), `viking_remember` (store facts), `viking_add_resource` (ingest URLs/docs)

**Setup:**
```bash
# Start the OpenViking server first
pip install openviking
openviking-server

# Then configure Hermes
hermes memory setup    # select "openviking"
# Or manually:
hermes config set memory.provider openviking
echo "OPENVIKING_ENDPOINT=http://localhost:1933" >> ~/.hermes/.env
# Authenticated servers should use a user/admin API key:
echo "OPENVIKING_API_KEY=..." >> ~/.hermes/.env
```

Key features: tiered context loading L0 (~100 tokens) → L1 (~2k) → L2 (full); automatic memory extraction on session commit (profile, preferences, entities, events, cases, patterns); a `viking://` URI scheme for hierarchical knowledge browsing. `OPENVIKING_ACCOUNT`/`OPENVIKING_USER` are used for local/trusted mode; `OPENVIKING_AGENT` is Hermes' peer ID for peer-scoped memories.

## Mem0

Server-side LLM fact extraction with semantic search, reranking, and automatic deduplication.

- **Best for**: Hands-off memory management — Mem0 handles extraction automatically
- **Requires**: `pip install mem0ai` + API key
- **Data storage**: Mem0 Cloud
- **Cost**: Mem0 pricing

**Tools:** `mem0_profile` (all stored memories), `mem0_search` (semantic search + reranking), `mem0_conclude` (store verbatim facts). **Config:** `$HERMES_HOME/mem0.json` with `user_id` (default `hermes-user`) and `agent_id` (default `hermes`).

## Hindsight

Long-term memory with a knowledge graph, entity resolution, and multi-strategy retrieval. The `hindsight_reflect` tool provides cross-memory synthesis that no other provider offers, and it automatically retains full conversation turns (including tool calls) with session-level document tracking.

- **Best for**: Knowledge graph-based recall with entity relationships
- **Requires**: Cloud — API key from ui.hindsight.vectorize.io; Local — LLM API key (OpenAI, Groq, OpenRouter, etc.)
- **Data storage**: Hindsight Cloud or local embedded PostgreSQL
- **Cost**: Hindsight pricing (cloud) or free (local)

**Tools:** `hindsight_retain` (store with entity extraction), `hindsight_recall` (multi-strategy search), `hindsight_reflect` (cross-memory synthesis). The setup wizard installs only what the selected mode needs (`hindsight-client` for cloud, `hindsight-all` for local), requires `hindsight-client >= 0.4.22` (auto-upgraded if outdated), and config lives at `$HERMES_HOME/hindsight/config.json` (`mode`, `bank_id`, `recall_budget` low/mid/high, `memory_mode` hybrid/context/tools, `auto_retain`, `auto_recall`, retain/recall tags and prefixes). See the plugin README for the full reference.

## Holographic

Local SQLite fact store with FTS5 full-text search, trust scoring, and HRR (Holographic Reduced Representations) for compositional algebraic queries.

- **Best for**: Local-only memory with advanced retrieval, no external dependencies
- **Requires**: Nothing (SQLite is always available); NumPy optional for HRR algebra
- **Data storage**: Local SQLite
- **Cost**: Free

**Tools:** `fact_store` (9 actions: add, search, probe, related, reason, contradict, update, remove, list), `fact_feedback` (helpful/unhelpful rating that trains trust scores). Config is in `config.yaml` under `plugins.hermes-memory-store` (`db_path` default `$HERMES_HOME/memory_store.db`, `auto_extract` default `false`, `default_trust` default `0.5`). Unique capabilities: `probe` (entity-specific algebraic recall), `reason` (compositional AND queries across entities), `contradict` (automated conflicting-fact detection), and trust scoring with asymmetric feedback (+0.05 helpful / -0.10 unhelpful).

## RetainDB

Cloud memory API with hybrid search (Vector + BM25 + Reranking), 7 memory types, and delta compression.

- **Best for**: Teams already using RetainDB's infrastructure
- **Requires**: RetainDB account + API key
- **Data storage**: RetainDB Cloud
- **Cost**: $20/month

**Tools:** `retaindb_profile` (user profile), `retaindb_search` (semantic search), `retaindb_context` (task-relevant context), `retaindb_remember` (store with type + importance), `retaindb_forget` (delete memories). Set via `hermes config set memory.provider retaindb` + `RETAINDB_API_KEY` in `~/.hermes/.env`.

## ByteRover

Persistent memory via the `brv` CLI — a hierarchical knowledge tree with tiered retrieval (fuzzy text → LLM-driven search), local-first with optional cloud sync.

- **Best for**: Developers who want portable, local-first memory with a CLI
- **Requires**: ByteRover CLI (`npm install -g byterover-cli` or install script)
- **Data storage**: Local (default) or ByteRover Cloud (optional sync)
- **Cost**: Free (local) or ByteRover pricing (cloud)

**Tools:** `brv_query` (search knowledge tree), `brv_curate` (store facts/decisions/patterns), `brv_status` (CLI version + tree stats). Key features: automatic pre-compression extraction (saves insights before context compression discards them), knowledge tree stored at `$HERMES_HOME/byterover/` (profile-scoped), and SOC2 Type II certified cloud sync (optional).

## Supermemory

Semantic long-term memory with profile recall, semantic search, explicit memory tools, and session-end conversation ingest via the Supermemory graph API.

- **Best for**: Semantic recall with user profiling and session-level graph building
- **Requires**: `pip install supermemory` + API key
- **Data storage**: Supermemory Cloud
- **Cost**: Supermemory pricing

**Tools:** `supermemory_store`, `supermemory_search`, `supermemory_forget`, `supermemory_profile`. Config at `$HERMES_HOME/supermemory.json` (`container_tag` default `hermes` with `{identity}` template support, `auto_recall`, `auto_capture`, `max_recall_results` 10, `profile_frequency` 50, `capture_mode`, `search_mode` hybrid/memories/documents, `api_timeout`); env vars `SUPERMEMORY_API_KEY` (required) and `SUPERMEMORY_CONTAINER_TAG`. Key features: automatic context fencing (strips recalled memories from captured turns to prevent recursive pollution), full-session ingest at session boundaries (to `/v4/conversations`), profile-scoped containers via `{identity}`, and multi-container mode (`enable_custom_container_tags` + `custom_containers`).

## Memori

Structured long-term memory using Memori Cloud, with background completed-turn capture, tool-aware turn context, and explicit recall tools for facts, summaries, quota, signup, and feedback.

- **Best for**: Agent-controlled recall with structured project and session attribution
- **Requires**: `pip install hermes-memori` + `hermes-memori install` + Memori API key
- **Data storage**: Memori Cloud
- **Cost**: Memori pricing

**Tools:** `memori_recall` (search long-term memory), `memori_recall_summary` (summarized context), `memori_quota` (usage/quota), `memori_signup` (request signup email), `memori_feedback` (send integration feedback).

```bash
pip install hermes-memori
hermes-memori install
hermes config set memory.provider memori
hermes memory setup
```

## Provider Comparison

| Provider | Storage | Cost | Tools | Dependencies | Unique Feature |
|----------|---------|------|-------|-------------|----------------|
| **Honcho** | Cloud | Paid | 5 | `honcho-ai` | Dialectic user modeling + session-scoped context |
| **OpenViking** | Self-hosted | Free | 5 | `openviking` + server | Filesystem hierarchy + tiered loading |
| **Mem0** | Cloud | Paid | 3 | `mem0ai` | Server-side LLM extraction |
| **Hindsight** | Cloud/Local | Free/Paid | 3 | `hindsight-client` | Knowledge graph + reflect synthesis |
| **Holographic** | Local | Free | 2 | None | HRR algebra + trust scoring |
| **RetainDB** | Cloud | $20/mo | 5 | `requests` | Delta compression |
| **ByteRover** | Local/Cloud | Free/Paid | 3 | `brv` CLI | Pre-compression extraction |
| **Supermemory** | Cloud | Paid | 4 | `supermemory` | Context fencing + session graph ingest + multi-container |
| **Memori** | Cloud | Free/Paid | 5 | `hermes-memori` | Tool-aware memory + structured recall |

(Honcho is included for completeness; its deep architecture lives in [hermes_memory_providers_honcho](hermes_memory_providers_honcho.md).)

## Profile Isolation

Each provider's data is isolated per profile by storage class:

- **Local storage providers** (Holographic, ByteRover) use `$HERMES_HOME/` paths which differ per profile.
- **Config file providers** (Honcho, Mem0, Hindsight, Supermemory) store config in `$HERMES_HOME/` so each profile has its own credentials.
- **Cloud providers** (RetainDB) auto-derive profile-scoped project names.
- **Env var providers** (OpenViking) are configured via each profile's `.env` file.

## Building a Memory Provider

To create your own provider, see the Developer Guide: Memory Provider Plugins (`/developer-guide/memory-provider-plugin`), which covers the plugin discovery, the provider ABC interface, and namespace registration every catalog provider plugs into. (That authoring page is owned by SP19.)

**Source**: `inbox/hermes_agent_docs/user-guide/features/memory-providers.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
**Last Updated**: 2026-06-19
**Status**: Active
