---
tags:
  - resource
  - documentation
  - hermes_agent
  - features
  - navigation
keywords:
  - features overview
  - feature index
  - core automation media integrations customization
  - hermes setup portal
  - tool gateway tools
  - capability map
topics:
  - Hermes Agent
  - Features
language: markdown
date of note: 2026-06-19
status: active
building_block: navigation
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/overview
access_control_group: ["general"]
---

# Hermes Agent — Features Overview

## Overview

The Features Overview is the **in-features navigation hub** for the Hermes Agent documentation: a categorized index of every capability that extends Hermes beyond basic chat. Where the [Learning Path](hermes_learning_path.md) routes a reader by experience level and goal (a reader router), this page routes by the **feature set itself** — grouping the full capability surface into five tracks (Core, Automation, Media & Web, Integrations, Customization) and giving each feature a one-line description plus a link-out to the page that actually documents it. It is a directory, not a deep-dive: the substance of each feature lives in its owning doc note. The source opens with a "where to start?" tip: `hermes setup --portal` is a single command that covers a model provider plus all four Tool Gateway tools (web search, image generation, TTS, browser), routing through [Nous Portal](hermes_nous_portal_subscription.md).

## Core

The foundational capabilities every Hermes session can use:

- **Tools & Toolsets** — Functions that extend the agent's capabilities, organized into logical toolsets that can be enabled or disabled per platform (web search, terminal execution, file editing, memory, delegation, and more).
- **Skills System** — On-demand knowledge documents the agent loads when needed, following a progressive-disclosure pattern to minimize token usage; compatible with the [agentskills.io](https://agentskills.io/specification) open standard.
- **Persistent Memory** — Bounded, curated memory that persists across sessions via `MEMORY.md` and `USER.md` (preferences, projects, environment, learned facts).
- **Context Files** — Automatic discovery and loading of project context files (`.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `SOUL.md`, `.cursorrules`) that shape behavior per project.
- **Context References** — Type `@` followed by a reference to inject files, folders, git diffs, and URLs directly into a message; Hermes expands the reference inline and appends the content.
- **Checkpoints** — Automatic snapshots of the working directory before file changes, with `/rollback` as a safety net.

## Automation

Capabilities for running work autonomously and at scale:

- **Scheduled Tasks (Cron)** — Schedule tasks with natural language or cron expressions; jobs can attach skills, deliver to any platform, and support pause/resume/edit.
- **Subagent Delegation** — The `delegate_task` tool spawns child agent instances with isolated context, restricted toolsets, and their own terminal sessions (3 concurrent subagents by default, configurable).
- **Code Execution** — The `execute_code` tool lets the agent write Python that calls Hermes tools programmatically, collapsing multi-step workflows into a single LLM turn via sandboxed RPC.
- **Event Hooks** — Run custom code at lifecycle points: gateway hooks for logging/alerts/webhooks, plugin hooks for tool interception/metrics/guardrails.
- **Batch Processing** — Run the agent across hundreds or thousands of prompts in parallel, generating structured ShareGPT-format trajectory data for training-data generation or evaluation.

## Media & Web

The web-facing and multimodal feature surface (the heart of SP08's coverage):

- **Voice Mode** — Full voice interaction across CLI and messaging platforms, including live voice conversations in Discord voice channels.
- **Browser Automation** — Full [browser automation](../../term_dictionary/term_browser_automation.md) with multiple backends: Browserbase cloud, Browser Use cloud, local Chrome/Brave/Chromium/Edge via CDP, or local Chromium. Navigate, fill forms, and extract information.
- **Vision & Image Paste** — Multimodal vision support; paste clipboard images into the CLI and have any vision-capable model analyze them.
- **Image Generation** — Generate images from text prompts using FAL.ai (nine models: FLUX 2 Klein/Pro, GPT-Image 1.5/2, Nano Banana Pro, Ideogram V3, Recraft V4 Pro, Qwen, Z-Image Turbo); pick one via `hermes tools`.
- **Voice & TTS** — Text-to-speech output and voice-message transcription across all messaging platforms, with ten native provider options (Edge TTS free, ElevenLabs, OpenAI TTS, MiniMax, Mistral Voxtral, Google Gemini, xAI, NeuTTS, KittenTTS, Piper) plus custom command providers.

## Integrations

External-system connectivity and provider control:

- **MCP Integration** — Connect to any MCP server via stdio or HTTP, accessing external tools (GitHub, databases, file systems, internal APIs) without writing native Hermes tools; includes per-server tool filtering and sampling.
- **Provider Routing** — Fine-grained control over which AI providers handle requests (cost/speed/quality optimization via sorting, allowlists, denylists, priority ordering).
- **Fallback Providers** — Automatic failover to backup LLM providers on error, including independent fallback for auxiliary tasks (vision, compression).
- **Credential Pools** — Distribute API calls across multiple keys for the same provider, with automatic rotation on rate limits or failures.
- **Prompt caching** — Built-in cross-session 1-hour prefix cache for Claude on native Anthropic, OpenRouter, and Nous Portal; always-on, no configuration.
- **Memory Providers** — Plug in external memory backends (Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory) for cross-session user modeling.
- **API Server** — Expose Hermes as an OpenAI-compatible HTTP endpoint (Open WebUI, LobeChat, LibreChat).
- **IDE Integration (ACP)** — Use Hermes inside ACP-compatible editors (VS Code, Zed, JetBrains); chat, tool activity, file diffs, and terminal commands render in-editor.
- **Batch Processing** — Run the agent over many prompts in parallel from the CLI, with structured outputs and trajectory capture for evals or training pipelines.

## Customization

Tailoring the agent's identity and presentation:

- **Personality & SOUL.md** — Fully customizable personality; `SOUL.md` is the primary identity file (first in the system prompt) and `/personality` swaps built-in or custom presets per session.
- **Skins & Themes** — Customize the CLI's visual presentation: banner colors, spinner faces and verbs, response-box labels, branding text, and the tool-activity prefix.
- **Plugins** — Add custom tools, hooks, and integrations without modifying core code; three types (general plugins, memory providers, context engines) managed via `hermes plugins`.

**Source**: `inbox/hermes_agent_docs/user-guide/features/overview.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/overview
**Last Updated**: 2026-06-19
**Status**: Active
