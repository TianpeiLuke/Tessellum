---
tags:
  - resource
  - terminology
  - agentic_ai
  - open_source
  - self_improving
  - agent_framework
keywords:
  - Hermes Agent
  - Nous Research
  - self-improving agent
  - closed learning loop
  - agentskills.io
  - autonomous skill discovery
  - persistent memory
  - function calling
  - MCP
  - multi-platform agent
topics:
  - agentic AI
  - agent frameworks
  - self-improving systems
  - open source
language: markdown
date of note: 2026-05-15
status: active
building_block: concept
related_wiki: https://github.com/nousresearch/hermes-agent
access_control_group: ["general"]
---

# Hermes Agent - Self-Improving Autonomous Agent Framework (Nous Research)

## Definition

**Hermes Agent** is an open-source self-improving autonomous agent framework by Nous Research that implements a "closed learning loop" — executing tasks, autonomously creating reusable skills from complex interactions, and continuously improving those skills during deployment. Unlike static agent frameworks where tools are predefined, Hermes Agent discovers and refines its own capabilities through experience, persisting knowledge across sessions via LLM-curated memory and the agentskills.io open standard.

The framework runs on anything from a $5 VPS to serverless infrastructure (Modal/Daytona) and is accessible through 7+ messaging platforms (CLI, Telegram, Discord, Slack, WhatsApp, Signal, Email), positioning it as both a personal AI assistant and a research platform for training downstream models via trajectory compression.

## Context

- **Creator**: Nous Research (known for Hermes LLM fine-tunes on Llama)
- **Repository**: https://github.com/nousresearch/hermes-agent
- **Ecosystem**: Part of the Hermes model family (Hermes 3 on Llama-3.1); framework is model-agnostic (200+ models via OpenRouter/OpenAI/Anthropic/NVIDIA NIM/HuggingFace)
- **Standard**: Skills compatible with agentskills.io open standard
- **Competitors**: Claude Code (Anthropic), Devin (Cognition), Manus, OpenHands

## Key Characteristics

- **Closed learning loop**: Execute → learn from interaction → create/improve reusable skill → persist → apply to future sessions
- **Autonomous skill discovery**: Agent creates skills from complex interactions without explicit programming; skills improve with use
- **Persistent cross-session memory**: LLM-powered summarization, full-text search of past sessions, agent-curated with periodic nudges, user modeling via Honcho dialectic
- **200+ model support**: Swap models with `hermes model` command — no code changes
- **40+ built-in tools** + MCP server integration for extensibility
- **Multi-agent**: Spawn isolated subagents for parallel workstreams; RPC-based tool calling
- **7 terminal backends**: Docker, SSH, Singularity, Modal (serverless), Daytona
- **Cron scheduler**: Natural language scheduling for unattended automation ("daily reports, nightly backups, weekly audits")
- **Multi-platform gateway**: Single agent instance accessible from CLI, Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant
- **Research-ready**: Trajectory compression for training downstream models; batch trajectory generation

## References

- [Hermes Agent GitHub](https://github.com/nousresearch/hermes-agent)
- [agentskills.io](https://agentskills.io) — open standard for agent skills
- [Hermes 3 Technical Report (arXiv:2408.11857)](https://arxiv.org/abs/2408.11857) — underlying model
- [Nous Research](https://nousresearch.com/) — parent organization
