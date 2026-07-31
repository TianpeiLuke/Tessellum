---
tags:
  - resource
  - terminology
  - agentic_ai
  - agent_framework
  - workflow_orchestration
  - open_source
keywords:
  - OpenClaw
  - Clawdbot
  - Moltbot
  - AI agent framework
  - autonomous agent
  - self-hosted
  - Peter Steinberger
  - Gateway
  - Brain
  - Memory
  - Skills
  - Heartbeat
  - Lobster DSL
  - ReAct loop
topics:
  - Agentic AI
  - Agent Frameworks
  - Workflow Orchestration
language: markdown
date of note: 2026-03-29
status: active
building_block: concept
access_control_group: ["general"]
---

# OpenClaw

## Definition

**OpenClaw** is an open-source (MIT-licensed), self-hosted autonomous AI agent framework that runs 24/7, maintains persistent memory across sessions, and takes action on external services through messaging platforms (Slack, WhatsApp, Telegram, Discord, etc.) as its primary user interface. It is the fastest-growing AI agent framework in history, reaching 247,000+ GitHub stars by March 2026 — surpassing all prior AI projects in growth velocity.

OpenClaw's architecture consists of five core components: **Gateway** (message routing across 50+ channels), **Brain** (LLM orchestration via ReAct reasoning loop), **Memory** (persistent context in Markdown/YAML files), **Skills** (plug-in capabilities defined via Markdown manifests), and **Heartbeat** (scheduled autonomous tasks). The framework supports cloud-hosted LLMs (Anthropic, OpenAI, Google) or fully local inference (Ollama, LM Studio), allowing complete data sovereignty.

## Historical Context

| Date | Event |
|------|-------|
| Nov 24, 2025 | Peter Steinberger (Austrian developer) publishes **Clawdbot** on GitHub — a personal experiment giving AI persistent memory + tool access + messaging interfaces |
| Jan 27, 2026 | Renamed to **Moltbot** after trademark complaint from Anthropic (original name derived from "Claude") |
| Jan 30, 2026 | Renamed to **OpenClaw** — Steinberger found "Moltbot" didn't roll off the tongue |
| Feb 2026 | Reaches 100K GitHub stars; becomes fastest-growing AI agent framework |
| Mar 2026 | 247K stars, 47.7K forks, 5,700+ community-built skills, 50+ channel integrations |

## Taxonomy

### Five-Component Architecture

| Component | Function | Implementation |
|---|---|---|
| **Gateway** | Routes messages from 50+ messaging channels to agent sessions | Central control plane; manages WhatsApp, Slack, Telegram, Discord, Signal simultaneously |
| **Brain** | Orchestrates LLM reasoning via ReAct loop | Compiles system prompt with tools → sends to LLM → parses tool calls → executes → loops until final answer |
| **Memory** | Stores persistent context across sessions | Plain Markdown + YAML files under `~/.openclaw/`; Git-backupable; grep-searchable |
| **Skills** | Plug-in capabilities for external actions | Markdown manifests (skill.md) defining triggers, permissions, instructions; 5,700+ community skills |
| **Heartbeat** | Scheduled autonomous wake-ups | Every 30 min (configurable); reads HEARTBEAT.md; decides whether to act or notify |

### Workflow Orchestration

| Mechanism | Description |
|---|---|
| **Lobster DSL** | Deterministic YAML-based workflow engine; externalizes flow control from LLM reasoning into typed, testable pipeline definitions |
| **Clawflows** | Multi-step pipeline orchestration via chained skills |
| **Swarm orchestration** | Multi-agent coordination with Conductor Agent overseeing Specialist Agents |

## Key Properties

- **Self-hosted**: All data stays on your hardware; models can be cloud or local
- **Persistent memory**: Markdown-based memory survives across sessions and restarts
- **Channel-agnostic**: Same agent works across 50+ messaging platforms via Gateway
- **Skill marketplace**: 5,700+ community-built skills; each defined by a Markdown manifest
- **Heartbeat autonomy**: Agent can wake up on schedule without human prompting
- **ReAct reasoning**: Brain uses the ReAct (Reasoning + Acting) loop for tool-augmented LLM reasoning
- **Deterministic workflows**: Lobster DSL separates orchestration logic from LLM reasoning for reliable multi-step pipelines
- **Open source**: MIT license; 247K+ GitHub stars

## Applications

| Domain | Application |
|--------|-------------|
| **DevOps** | Automated CI/CD monitoring, deployment, incident response |
| **Data Teams** | Scheduled data quality checks, report generation, pipeline monitoring |
| **Customer Support** | Multi-channel agent handling inquiries across Slack, WhatsApp, email |
| **Personal Productivity** | Morning briefings, email triage, calendar management |
| **Smart Home** | IoT device orchestration via messaging interfaces |
| **Enterprise** | Internal knowledge bases, document processing, workflow automation |

## Challenges and Limitations

- **Resource requirements**: Self-hosting requires infrastructure management (Docker, compute, storage)
- **Security**: Self-hosted model means organization is responsible for security hardening
- **Skill quality**: Community skills vary in quality and maintenance status
- **LLM dependency**: Brain quality depends on underlying LLM capability and cost
- **Rapid evolution**: Framework changing rapidly (3 name changes in 2 months); API stability uncertain

## Related Terms

### Architectural Components (authored from OpenClaw snippet decomposition)


### Cross-Domain Bridges (industry concepts OpenClaw composes against)


### Industry / Cross-Domain

- **[Band OpenCode Adapter (local coding-agent server analogue)](../documentation/band/band_adapter_opencode.md)**: Band's adapter wiring a local OpenCode coding-agent server (local-server + `provider_id`/`model_id` + single-turn-per-session) into a chat room; relevance: OpenClaw is the closest internal equivalent of a long-lived local coding-agent server with provider/model selection (Gateway / Brain / ReAct loop / per-session memory, local-or-cloud provider incl. Ollama/LM Studio), and the band note already cites OpenClaw repos as internal analogues of OpenCode's local server, so a reader of this term would want to discover Band's OpenCode adapter.
- **[OpenClaw — Built-in Agent Runtime Architecture](../documentation/openclaw/oc_agent_runtime_architecture.md)** — This note describes the **built-in OpenClaw agent runtime** that OpenClaw owns directly — its module layout, the core-vs-plugin boundaries it enforces, the…
- **[OpenClaw — The Embedded Agent Runtime Contract](../documentation/openclaw/oc_concepts_agent.md)** — This note defines OpenClaw's **embedded agent runtime** contract: the single agent process per Gateway, with its own workspace, injected bootstrap files, and…
- **[OpenClaw — The Help Hub (Get-Unstuck Index)](../documentation/openclaw/oc_help.md)** — This note covers the OpenClaw **Help** page (`/help`), the symptom-first "get unstuck" navigation hub that points an operator to the fastest path to a fix when…
- **[OpenClaw — Talk Mode (Continuous Speech Conversation)](../documentation/openclaw/oc_nodes_talk.md)** — This note is the procedure for configuring and operating OpenClaw **Talk mode**: a continuous speech conversation between a node (macOS/iOS/Android or browser)…
- **[OpenClaw — Platform Support and Gateway Service Install](../documentation/openclaw/oc_platforms_overview.md)** — This note is the platform-support overview procedure for OpenClaw, mirroring the `platforms` source page: it covers the runtime recommendation (TypeScript…
- **[OpenClaw — Model Provider Directory](../documentation/openclaw/oc_provider_directory.md)** — This note is the conceptual index of the OpenClaw **provider directory**: the catalog of LLM, transcription, and media-generation model backends OpenClaw can…
- **[OpenClaw — Personal Assistant Setup Walkthrough](../documentation/openclaw/oc_start_openclaw.md)** — This note is the end-to-end procedure for running OpenClaw as a "personal assistant": a dedicated WhatsApp number that behaves like an always-on AI assistant…
- **[OpenClaw — Background exec and the process Tool](../documentation/openclaw/oc_gateway_background_process.md)** — This note covers the OpenClaw gateway's **background-process model**: how shell commands run through the `exec` tool, how long-running tasks are…

## References

### Vault Sources

### External Sources
- [OpenClaw Explained (Medium)](https://medium.com/@cenrunzhe/openclaw-explained-how-the-hottest-agent-framework-works-and-why-data-teams-should-pay-attention-69b41a033ca6) — Architecture deep-dive
- [What Is OpenClaw? (MindStudio)](https://www.mindstudio.ai/blog/what-is-openclaw-ai-agent) — Overview and use cases
- [OpenClaw Complete Tutorial 2026 (Towards AI)](https://pub.towardsai.net/openclaw-complete-guide-setup-tutorial-2026-14dd1ae6d1c2) — Setup and configuration guide
- [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) — History and growth
- [How I Built a Deterministic Pipeline Inside OpenClaw (DEV)](https://dev.to/ggondim/how-i-built-a-deterministic-multi-agent-dev-pipeline-inside-openclaw-and-contributed-a-missing-4ool) — Lobster DSL deep-dive
- [GitHub: openclaw/openclaw](https://github.com/openclaw/openclaw) — Source code (247K+ stars)

### Related Code Repos
- [OpenClaw (code repo)](../../areas/code_repos/repo_openclaw.md) — Open-source personal AI agent framework; this term's reference upstream
- [OpenClaw Gateway](../../areas/code_repos/repo_openclaw_gateway.md) — Message routing across 50+ channels (the Gateway component documented in this term's taxonomy)
- [OpenClaw Extensions](../../areas/code_repos/repo_openclaw_extensions.md) — LLM provider and voice/speech extension subsystems

### Related Code Snippets

