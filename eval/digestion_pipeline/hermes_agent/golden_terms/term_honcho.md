---
tags:
  - resource
  - terminology
  - agentic_ai
  - memory
  - hermes_agent
keywords:
  - honcho
  - memory provider
  - dialectic reasoning
  - user modeling
  - peer
  - cross-session memory
topics:
  - Agent Memory
  - Agentic AI Infrastructure
  - User Modeling
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho/
---

# Honcho - AI-Native Memory Provider (Dialectic User Modeling)

## Definition

**Honcho** is an AI-native, server-side memory backend that adds *dialectic reasoning* and deep
*user modeling* on top of an agent's built-in file-based memory. Instead of simple key-value or append-only note storage, Honcho maintains a running, evolving model of *who the user is* — their preferences, communication style, goals, and behavioral patterns — by reasoning about conversations *after* they happen rather than just recording what was explicitly said. In the [Hermes Agent](term_hermes_agent.md) framework it is integrated as one of the eight external [memory providers](term_agentic_memory.md) (only one external provider is active at a time, always alongside the built-in `MEMORY.md`/`USER.md`), selected via `hermes memory setup` or `memory.provider: honcho` in `config.yaml`.

Honcho is built by Plastic Labs as a standalone open-source project; the Hermes integration wraps it as a provider plugin. Its distinguishing feature is that it derives *conclusions* — synthesized insights about the user — through an LLM "dialectic" pass, so the agent's understanding deepens beyond the literal transcript. This makes it directly analogous to the research [Dialectic Knowledge System](term_dks_dialectic_knowledge_system.md) pattern, applied here to per-user personalization instead of rule refinement.

## Context

Honcho appears in the *external memory provider* layer of an agent harness. When active, the host agent automatically (1) injects provider context into the system prompt, (2) prefetches relevant memories before each turn, (3) syncs conversation turns after each response, (4) extracts memories on session end, (5) mirrors built-in memory writes to the provider, and (6) exposes provider-specific tools. It is positioned for **multi-agent systems** where several agent profiles (e.g. a coding assistant and a personal assistant) talk to the same human and must keep separate-but-coordinated context — each agent is a distinct "peer" with its own representation, sharing one workspace and one user peer. On messaging gateways (Telegram/Discord/Slack), Honcho also resolves platform-native runtime IDs to peers via identity-mapping config (`pinUserPeer`, `userPeerAliases`, `runtimePeerPrefix`).

It is consumed through five agent tools — `honcho_profile`, `honcho_search`, `honcho_context`, `honcho_reasoning`, and `honcho_conclude` — and managed via the `hermes honcho` CLI subcommand (registered only when Honcho is the active provider). It is a sibling concept to the other catalog providers (OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory, Memori) and a deep-personalization complement to the agent's bounded built-in memory.

## Key Characteristics

- **Dialectic reasoning.** After conversation turns (gated by `dialecticCadence`), Honcho analyzes the exchange via an LLM and derives accumulating insights about the user. Supports multi-pass depth ($1 \le \text{dialecticDepth} \le 3$): pass 0 issues a cold/warm prompt, pass 1 self-audits gaps, pass 2 reconciles contradictions into a final synthesis. Passes bail out early on strong signal, so depth 3 does not always cost 3 LLM calls.
- **Two-layer context injection.** Every turn (in `hybrid`/`context` mode) it concatenates a *base layer* (session summary + user representation + peer card + AI identity, refreshed on `contextCadence`) and a *dialectic supplement* (LLM-synthesized "what matters right now", refreshed on `dialecticCadence`), truncated to the `contextTokens` budget.
- **Cold/warm prompt selection.** With no base context yet, the dialectic asks a general "who is this person?" query; once base context exists it asks a session-scoped "what is most relevant given this session?" query — selected automatically.
- **Three orthogonal knobs.** `contextCadence`, `dialecticCadence`, and `dialecticDepth` independently trade off cost vs. depth — frequent base refresh with infrequent deep dialectic is expressible.
- **Per-peer multi-agent isolation.** Multiple agent profiles maintain separate peer profiles against the same shared user/workspace; each peer sees only its own observations and conclusions, preventing cross-contamination.
- **Observation modes.** Per-peer `observeMe`/`observeOthers` toggles (two peers × two toggles = four flags) with `directional` (full mutual observation, enables cross-peer dialectic) and `unified` (single-observer shared pool) presets, overridable per-peer.
- **Recall modes.** `hybrid` (auto-inject + tools), `context` (inject only), and `tools` (model calls `honcho_reasoning`/`honcho_search` explicitly); cadence and budget knobs apply only to the injection modes.
- **Server-side conclusions + semantic search.** Honcho stores derived conclusions server-side and supports semantic search over them (vs. the built-in FTS5 lexical session search), aligning with dense-retrieval-style recall over distilled insight rather than raw transcript.
- **Deployment.** Honcho Cloud (`pip install honcho-ai` + API key) or self-hosted (free, JWT/bearer auth via `AUTH_JWT_SECRET`); config in `$HERMES_HOME/honcho.json` or `~/.honcho/config.json`.

## Related Terms


## References
- [Hermes Agent Docs — Honcho Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho/)
- [Hermes Agent Docs — Memory Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers/)
- [Honcho — Plastic Labs (GitHub)](https://github.com/plastic-labs/honcho)
- [Honcho Documentation](https://docs.honcho.dev/)
- [Honcho — Hermes Integration Guide](https://docs.honcho.dev/v3/guides/integrations/hermes)
- [Honcho Cloud Dashboard](https://app.honcho.dev/)

---

**Last Updated**: 2026-06-19
**Status**: Active
