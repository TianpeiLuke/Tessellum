---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - crestodian
keywords:
  - openclaw crestodian
  - configless-safe repair helper
  - safe startup probe
  - typed operations approval
  - setup bootstrap backend order
  - model-assisted planner
  - message rescue mode
  - remote rescue security contract
  - crestodian audit log
topics:
  - OpenClaw
  - Crestodian CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/cli/crestodian
access_control_group: ["general"]
---

# OpenClaw — Crestodian, the Configless-Safe Setup & Repair Helper

## Overview

This note describes **Crestodian**, OpenClaw's local setup, repair, and configuration helper, as documented on the `cli/crestodian` source page. The defining idea is that Crestodian is *configless-safe*: it is designed to stay reachable when the normal agent path is broken — when `openclaw.json` is missing or invalid, when the Gateway is down, when plugin command registration is unavailable, or when no agent has been configured yet. The note covers the conceptual model of Crestodian as a security and trust boundary: its TUI startup probe, the safe-startup conditions, the typed read-only vs approval-gated operation split, the setup-bootstrap backend-selection order, the bounded model-assisted planner, agent handoff, and the message-channel **rescue mode** security contract. Operationally, bare `openclaw` (no command) routes to classic onboarding when the config is empty/metadata-only, and routes to Crestodian once the config file has authored settings.

## What Crestodian Shows

On startup, interactive Crestodian opens the same TUI shell used by `openclaw tui`, but with a **Crestodian chat backend**. The chat log starts with a short greeting that reports: when to start Crestodian; the model or deterministic planner path Crestodian is actually using; config validity and the default agent; Gateway reachability from the first startup probe; and the next debug action Crestodian can take. It deliberately does **not** dump secrets or load plugin CLI commands just to start. The TUI still provides the normal header, chat log, status line, footer, autocomplete, and editor controls. Use `status` for the detailed inventory with config path, docs/source paths, local CLI probes, API-key presence, agents, model, and Gateway details.

Crestodian uses the same OpenClaw reference discovery as regular agents. In a Git checkout it points itself at the local `docs/` and the local source tree; in an npm package install it uses the bundled package docs and links to `https://github.com/openclaw/openclaw`, with explicit guidance to review source whenever the docs are not enough.

## Invocation Surfaces and Examples

Crestodian is reached three ways: bare `openclaw` (no command, after the config has authored settings), the explicit `openclaw crestodian` command, and the message-channel `/crestodian <request>` rescue entrypoint. `openclaw crestodian --json` emits structured output; `--message "<request>"` runs a single one-shot request; `--yes` pre-approves a persistent operation for a direct command. The page's command examples:

```bash
openclaw
openclaw crestodian
openclaw crestodian --json
openclaw crestodian --message "models"
openclaw crestodian --message "validate config"
openclaw crestodian --message "setup workspace ~/Projects/work model openai/gpt-5.5" --yes
openclaw crestodian --message "set default model openai/gpt-5.5" --yes
openclaw onboard --modern
```

Inside the Crestodian TUI, the documented command vocabulary spans inspection (`status`, `health`, `audit`), repair (`doctor`, `doctor fix`, `validate config`), setup (`setup`, `setup workspace ... model ...`), typed config edits (`config set gateway.port 19001`, `config set-ref gateway.auth.token env OPENCLAW_GATEWAY_TOKEN`), Gateway control (`gateway status`, `restart gateway`), agent management (`agents`, `create agent work workspace ~/Projects/work`), model selection (`models`, `set default model openai/gpt-5.5`), plugin operations (`plugins list`, `plugins search slack`, `plugin install clawhub:openclaw-codex-app-server`, `plugin uninstall openclaw-codex-app-server`), and agent handoff (`talk to work agent`, `talk to agent for ~/Projects/work`).

## Safe Startup

Crestodian's startup path is deliberately small. It can run when: `openclaw.json` is missing; `openclaw.json` is invalid; the Gateway is down; plugin command registration is unavailable; or no agent has been configured yet. `openclaw --help` and `openclaw --version` still use the normal fast paths. **Noninteractive** bare `openclaw` exits with a short message instead of printing root help — on a fresh install the message points to non-interactive onboarding, and after setup it points to one-shot Crestodian commands. This minimal startup surface is what lets Crestodian remain a usable repair console even when every richer subsystem (config, Gateway, plugins, agents) is degraded.

## Operations and Approval (Trust Split)

Crestodian uses **typed operations** instead of editing config ad hoc — the central security mechanism. Operations divide into two trust classes. **Read-only operations** can run immediately: show overview; list agents; list installed plugins; search ClawHub plugins; show model/backend status; run status or health checks; check Gateway reachability; run doctor without interactive fixes; validate config; and show the audit-log path. **Persistent operations** require conversational approval in interactive mode unless you pass `--yes` for a direct command: write config; run `config set`; set supported SecretRef values through `config set-ref`; run setup/onboarding bootstrap; change the default model; start, stop, or restart the Gateway; create agents; install plugins from ClawHub or npm; uninstall plugins; and run doctor repairs that rewrite config or state.

Applied writes are recorded in the audit log at `~/.openclaw/audit/crestodian.jsonl`. **Discovery is not audited** — only applied operations and writes are logged. Separately, `openclaw onboard --modern` starts Crestodian as the modern onboarding preview, while plain `openclaw onboard` still runs classic onboarding.

## Setup Bootstrap (Backend Selection Order)

`setup` is the chat-first onboarding bootstrap. It writes only through typed config operations and asks for approval first (`setup`, `setup workspace ~/Projects/work`, `setup workspace ~/Projects/work model openai/gpt-5.5`). When no model is configured, setup selects the first usable backend in this order and tells you what it chose:

- existing explicit model, if already configured
- `OPENAI_API_KEY` -> `openai/gpt-5.5`
- `ANTHROPIC_API_KEY` -> `anthropic/claude-opus-4-8`
- Claude Code CLI -> `claude-cli/claude-opus-4-8`
- Codex -> `openai/gpt-5.5` through the Codex app-server harness

If none are available, setup still writes the default workspace and leaves the model unset; the operator must install or log into Codex/Claude Code, or expose `OPENAI_API_KEY`/`ANTHROPIC_API_KEY`, then run setup again.

## Model-Assisted Planner

Crestodian **always starts in deterministic mode**. For fuzzy commands the deterministic parser does not understand, local Crestodian can make **one bounded planner turn** through OpenClaw's normal runtime paths. It first uses the configured OpenClaw model; if no configured model is usable yet, it can fall back to local runtimes already present on the machine — Claude Code CLI (`claude-cli/claude-opus-4-8`) or the Codex app-server harness (`openai/gpt-5.5`). Crucially, the model-assisted planner **cannot mutate config directly**: it must translate the request into one of Crestodian's typed commands, after which the normal approval and audit rules apply. Crestodian prints the model it used and the interpreted command before it runs anything. Configless fallback planner turns are temporary, tool-disabled where the runtime supports it, and use a temporary workspace/session. Message-channel rescue mode does **not** use the model-assisted planner — remote rescue stays deterministic so a broken or compromised normal agent path cannot be used as a config editor.

## Switching to an Agent

A natural-language selector leaves Crestodian and opens the normal TUI (`talk to agent`, `talk to work agent`, `switch to main agent`). `openclaw tui`, `openclaw chat`, and `openclaw terminal` still open the normal agent TUI directly — they do not start Crestodian. After switching into the normal TUI, `/crestodian` returns to Crestodian and can include a follow-up request (`/crestodian`, `/crestodian restart gateway`). Agent switches inside the TUI leave a breadcrumb that `/crestodian` is available.

## Message Rescue Mode and Security Contract

Message rescue mode is the message-channel entrypoint for Crestodian, for the case where the normal agent is dead but a trusted channel such as WhatsApp still receives commands. The supported text command is `/crestodian <request>`. A representative operator flow shows the approval roundtrip — `/crestodian status` returns a deterministic report (Gateway reachable / config valid), a repair request such as `/crestodian restart gateway` returns a plan with `Reply /crestodian yes to apply`, and `/crestodian yes` applies it with an audit entry written. Agent creation can also be queued from the local prompt or rescue mode (`create agent work workspace ~/Projects/work model openai/gpt-5.5`, `/crestodian create agent work workspace ~/Projects/work`). Remote rescue mode is an **admin surface** and must be treated like remote config repair, not like normal chat.

**Security contract for remote rescue:**

- Disabled when sandboxing is active. If an agent/session is sandboxed, Crestodian must refuse remote rescue and explain that local CLI repair is required.
- Default effective state is `auto`: allow remote rescue only in trusted YOLO operation, where the runtime already has unsandboxed local authority.
- Require an explicit owner identity. Rescue must not accept wildcard sender rules, open group policy, unauthenticated webhooks, or anonymous channels.
- Owner DMs only by default. Group/channel rescue requires explicit opt-in.
- Plugin search and list are read-only. Plugin install is local-only by default because it downloads executable code. Plugin uninstall can be allowed as an approved repair operation when rescue policy permits persistent writes.
- Remote rescue cannot open the local TUI or switch into an interactive agent session. Use local `openclaw` for agent handoff.
- Persistent writes still require approval, even in rescue mode.
- Audit every applied rescue operation. Message-channel rescue records channel, account, sender, and source-address metadata. Config-mutating operations also record config hashes before and after.
- Never echo secrets. SecretRef inspection should report availability, not values.
- If the Gateway is alive, prefer Gateway typed operations. If the Gateway is dead, use only the minimal local repair surface that does not depend on the normal agent loop.

The rescue config shape is:

```jsonc
{
  "crestodian": {
    "rescue": {
      "enabled": "auto",
      "ownerDmOnly": true,
    },
  },
}
```

`enabled` accepts `"auto"` (default — allow only when the effective runtime is YOLO and sandboxing is off), `false` (never allow message-channel rescue), and `true` (explicitly allow rescue when the owner/channel checks pass, still without bypassing the sandboxing denial). The default `"auto"` **YOLO posture** resolves sandbox mode to `off`, `tools.exec.security` to `full`, and `tools.exec.ask` to `off`.

## Test Lanes

The page documents the test coverage for these surfaces (link-referenced rather than reproduced as the primary content): remote rescue is covered by the Docker lane `pnpm test:docker:crestodian-rescue`; the configless local planner fallback by `pnpm test:docker:crestodian-planner`; an opt-in live channel command-surface smoke (`/crestodian status` plus a persistent approval roundtrip through the rescue handler) by `pnpm test:live:crestodian-rescue-channel`; and configless setup through explicit Crestodian commands by `pnpm test:docker:crestodian-first-run`. The first-run lane starts with an empty state dir, verifies the modern onboard Crestodian entrypoint, sets the default model, creates an additional agent, configures Discord through a plugin enablement plus token SecretRef, validates config, and checks the audit log. QA Lab also has a repo-backed Ring 0 scenario, `pnpm openclaw qa suite --scenario crestodian-ring-zero-setup`.

**Source**: OpenClaw documentation — `cli/crestodian` (mirror `inbox/openclaw_docs/cli/crestodian.md`)
**Last Updated**: 2026-06-22
**Status**: Active
