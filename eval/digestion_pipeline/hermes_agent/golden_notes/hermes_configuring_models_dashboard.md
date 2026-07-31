---
tags:
  - resource
  - documentation
  - hermes_agent
  - model_configuration
  - dashboard
keywords:
  - configuring models dashboard
  - main and auxiliary model slots
  - model picker provider columns
  - use as shortcut
  - config.yaml model auxiliary
  - hermes model rest api
topics:
  - Hermes Agent
  - Model Configuration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
access_control_group: ["general"]
---

# Configuring Models (Dashboard)

## Overview

This is the procedure for assigning models to Hermes Agent's slots from the dashboard's **Models** page. Hermes uses two kinds of slots: a single **main model** (what the agent thinks with on every message, tool-call loop, and streamed response) and **11 auxiliary models** (smaller side-jobs the agent offloads — context compression, vision, web-page summarization, approval scoring, MCP tool routing, session-title generation, skill search, and the Kanban/profile/curator tasks). Each slot has its own picker, every auxiliary task defaults to `auto` (reuse the main model), and saving writes the choice to `~/.hermes/config.yaml`. The page also documents the alternative paths — the CLI `/model` slash command, custom aliases, the `hermes model` subcommand, direct config edit, and the three REST endpoints the dashboard itself calls.

## The Models Page

Open the dashboard and click **Models** in the sidebar. You get two sections: **Model Settings** (the top panel, where you assign models to slots) and **Usage analytics** (ranked cards showing every model that ran a session in the selected period, with token counts, cost, and capability badges). The top **Model Settings** card always shows the main row — what the agent will spin up for new sessions. Click **Change** to open the picker.

For first-time provider setup, the fastest path is Nous Portal: `hermes setup --portal` logs in and sets Nous as your provider (300+ models under one subscription) in one command, and `hermes portal info` inspects what is wired up. On a brand-new install the bundled default config has `model: ""` (an empty-string sentinel meaning "not configured yet"); the first run of `hermes setup` or `hermes model` upgrades that key in-place to a mapping with `provider`, `default`, `base_url`, and `api_mode` sub-keys.

## Setting the Main Model

Click **Change** on the Main model row to open the picker. It has two columns:

- **Left — authenticated providers.** Only providers you have set up (API key set, OAuth'd, or defined as a custom endpoint) show here. If a provider is missing, add its credential under **Keys**.
- **Right — the curated model list** for the selected provider. These are the agentic models Hermes recommends for that provider, *not* the raw `/models` dump (which on OpenRouter includes 400+ models including TTS, image generators, and rerankers).

Type in the filter box to narrow by provider name, slug, or model ID. Pick a model, hit **Switch**, and Hermes writes it to `~/.hermes/config.yaml` under the `model` section. **This applies to new sessions only** — any chat tab already open keeps running whatever model it started with. To hot-swap the current chat, use the `/model` slash command inside it.

## Setting Auxiliary Models

Click **Show auxiliary** to reveal the 11 task slots. Every auxiliary task defaults to `auto` — Hermes tries your main model for that job too. If that route is unavailable or hits a capacity-style failure, `auto` follows any task-specific `auxiliary.<task>.fallback_chain`, then the main `fallback_providers` / `fallback_model` chain, then Hermes' built-in auxiliary discovery chain. Override a task when you want a cheaper or faster model for a side-job.

### Common override patterns

| Task | When to override |
|---|---|
| **Title Gen** | Almost always. A $0.10/M flash model writes session titles as well as Opus. Default config sets this to `google/gemini-3-flash-preview` on OpenRouter. |
| **Vision** | When your main model lacks vision support. Point it at `google/gemini-2.5-flash` or `gpt-4o-mini`. |
| **Compression** | When you are burning reasoning tokens on Opus/M2.7 just to summarize context. A fast chat model does the job at 1/50th the cost. |
| **Approval** | For `approval_mode: smart` — a fast/cheap model (haiku, flash, gpt-5-mini) decides whether to auto-approve low-risk commands. Expensive models here are waste. |
| **Web Extract** | When you use `web_extract` heavily. Same logic as compression — summarization does not need reasoning. |
| **Skills Hub** | `hermes skills search` uses this. Usually fine at `auto`. |
| **MCP** | MCP tool routing. Usually fine at `auto`. |
| **Triage Specifier** | Routes the Kanban triage specifier (`hermes kanban specify`) that expands a rough one-liner into a concrete spec. |
| **Kanban Decomposer** | Routes Kanban task decomposition — splits a triage task into a graph of child tasks for specialist profiles. |
| **Profile Describer** | Routes profile-description generation (`hermes profile describe --auto`). Short, cheap call. |
| **Curator** | Routes the curator skill-usage review pass. Can run for minutes on reasoning models, so a cheaper aux model is often worthwhile. |

**Per-task override:** click **Change** on any auxiliary row — the same picker opens, same behavior (pick provider + model, hit Switch). The row updates to show `provider · model` instead of `auto (use main model)`. **Reset all to auto:** click **Reset all to auto** at the top of the auxiliary section to send every slot back to the main model.

## The "Use as" Shortcut

Every model card on the page has a **Use as** dropdown — the fast path to assign a model you see in your analytics to a slot in one click. The dropdown has:

- **Main model** — same as clicking Change on the main row.
- **All auxiliary tasks** — assigns this model to all 11 aux slots at once (useful for putting every side-job on a cheap flash model).
- **Individual task options** — Vision, Web Extract, Compression, etc. The currently-assigned model for each task is marked `current`.

Cards are badged with `main` or `aux · <task>` when currently assigned, so you can see at a glance which of your historical models are wired in where.

## What Gets Written to `config.yaml`

When you save via the dashboard, Hermes writes to `~/.hermes/config.yaml`. The main model is a mapping:

```yaml
model:
  provider: openrouter
  default: anthropic/claude-opus-4.7
  base_url: ''        # cleared on provider switch
  api_mode: chat_completions
```

An auxiliary override (example — vision on gemini-flash):

```yaml
auxiliary:
  vision:
    provider: openrouter
    model: google/gemini-2.5-flash
    base_url: ''
    api_key: ''
    timeout: 120
    extra_body: {}
    download_timeout: 30
```

An auxiliary slot left on auto uses `provider: auto` with `model: ''`, which tells Hermes to use the main model for that task while still honoring fallback policy if the main route cannot serve the auxiliary call. Optional task-specific fallback chains live under the same auxiliary task (e.g. a `title_generation.fallback_chain` with a `provider`/`model` entry); when `fallback_chain` is absent, `auto` uses the top-level `fallback_providers` chain before the built-in auxiliary discovery chain.

## When Does It Take Effect?

- **CLI** (`hermes chat`): next `hermes chat` invocation.
- **Gateway** (Telegram, Discord, Slack, etc.): next *new* session. Existing sessions keep their model. Restart the gateway (`hermes gateway restart`) to force all sessions to pick up the change.
- **Dashboard chat tab** (`/chat`): next new PTY. The currently-open chat keeps its model — use `/model` inside it to hot-swap.

Changes never invalidate prompt caches on running sessions: swapping the main model inside a session requires a cache reset (the system prompt contains model-specific content), reserved for the explicit `/model` slash command inside chat.

## Troubleshooting

- **"No authenticated providers" in the picker** — Hermes lists a provider only with a working credential. Check **Keys**: you should see an API key, a successful OAuth, or a custom endpoint URL. Run `hermes setup` or add the env var.
- **Main model did not change in my running chat** — Expected. The dashboard writes `config.yaml`, which new sessions read; the open chat is a live agent process keeping its spawn-time model. Use `/model <name>` inside the chat to hot-swap that session.
- **Auxiliary override "did not take effect"** — Check three things: (1) did you start a new session? (2) is `provider` set to something other than `auto`? (if it shows `auto`, the task still uses your main model) (3) is the provider authenticated? An unauthenticated aux provider falls back to the openrouter default and logs a warning in `agent.log`.
- **I picked a model but Hermes switched providers** — On OpenRouter (or any aggregator) bare model names resolve *within* the aggregator first, so `claude-sonnet-4` becomes `anthropic/claude-sonnet-4.6` and stays on your OpenRouter auth; on native Anthropic auth it would stay `claude-sonnet-4-6`. The picker always shows the current main at the top of the dialog.

## Alternative Methods

**CLI slash command** — inside any `hermes chat` session:

```
/model gpt-5.4 --provider openrouter             # session-only
/model gpt-5.4 --provider openrouter --global    # also persists to config.yaml
```

`--global` does the same thing as the dashboard's **Change** button, plus it switches the running session in-place.

**Custom aliases** — define short names. The canonical top-level `model_aliases:` form gives full control over provider + base_url; the short string form (`hermes config set model.aliases.<name> provider/model`) is convenient from the shell but cannot carry a custom `base_url`. Both paths feed the same loader (`hermes_cli/model_switch.py`); `model_aliases:` entries take precedence over `model.aliases:` entries with the same name. User aliases shadow built-in short names (`sonnet`, `kimi`, `opus`, etc.).

**`hermes model` subcommand** — `hermes model` walks you through picking a provider, authenticating (OAuth flows open a browser; API-key providers prompt for the key), then choosing a specific model from that provider's curated catalog. The choice is written to `model.provider` and `model.model`. Inspect the current model with `hermes config show | grep '^model\.'` and `hermes status`.

**Direct config edit** — edit `~/.hermes/config.yaml` and restart whatever reads it.

**REST API** — the dashboard uses three endpoints (useful for scripting); the session token rotates on every server restart:

```bash
# List authenticated providers + curated model lists
curl -H "X-Hermes-Session-Token: $TOKEN" http://localhost:PORT/api/model/options

# Set the main model
curl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \
  -d '{"scope":"main","provider":"openrouter","model":"anthropic/claude-opus-4.7"}' \
  http://localhost:PORT/api/model/set

# Override a single auxiliary task
curl -X POST -H "Content-Type: application/json" -H "X-Hermes-Session-Token: $TOKEN" \
  -d '{"scope":"auxiliary","task":"vision","provider":"openrouter","model":"google/gemini-2.5-flash"}' \
  http://localhost:PORT/api/model/set
```

**Source**: `inbox/hermes_agent_docs/user-guide/configuring-models.md` · https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
**Last Updated**: 2026-06-19
**Status**: Active
