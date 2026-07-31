---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - onboarding
keywords:
  - openclaw onboarding outputs
  - openclaw.json config fields
  - wizard rpc gateway
  - wizard.start wizard.next wizard.cancel wizard.status
  - signal-cli install
  - auth-profiles.json sessions whatsapp credentials
  - agents.defaults.workspace tools.profile
  - wizard lastRunAt lastRunCommit
topics:
  - OpenClaw
  - Onboarding Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/wizard
access_control_group: ["general"]
---

# OpenClaw — Onboarding Outputs: What the Wizard Writes, the `wizard.*` RPC, and Signal Setup

## Overview

This note is the output/integration half of the `reference/wizard` onboarding reference: it documents what `openclaw onboard` actually persists to disk, the Gateway RPC surface that lets remote clients drive the same flow, and the `signal-cli` install procedure invoked during the Channels step. It mirrors the source page's `## Gateway wizard RPC`, `## Signal setup (signal-cli)`, `## What the wizard writes`, and `## Related docs` sections. The interactive 10-step flow and non-interactive flags are documented in the split sibling [oc_reference_onboarding_flow](oc_reference_onboarding_flow.md); this note picks up where that one ends — at the config file and state directory the flow produces, the RPC that fronts it, and the signal-cli side install.

## What the wizard writes

Onboarding persists its decisions to the per-user config file `~/.openclaw/openclaw.json`. The page lists the typical fields written there:

- `agents.defaults.workspace` — the workspace path chosen at the Workspace step (default `~/.openclaw/workspace`).
- `agents.defaults.model` / `models.providers` — the default model and provider config (the page notes `models.providers` is written when MiniMax is chosen during Model/Auth).
- `tools.profile` — local onboarding defaults this to `"coding"` when unset; existing explicit values are preserved (not overwritten on re-run).
- `gateway.*` — the Gateway step's `mode`, `bind`, `auth`, and `tailscale` settings.
- `session.dmScope` — DM-scope behavior (behavior details cross-link to the CLI Setup Reference `#outputs-and-internals`).
- `channels.telegram.botToken`, `channels.discord.token`, `channels.matrix.*`, `channels.signal.*`, `channels.imessage.*` — per-channel credentials/config for the channels enabled during setup.
- Channel allowlists (Slack / Discord / Matrix / Microsoft Teams) when you opt in during the prompts — names resolve to IDs when possible.
- `skills.install.nodeManager` — the chosen node manager. `setup --node-manager` accepts `npm`, `pnpm`, or `bun`; manual config can still use `yarn` by setting `skills.install.nodeManager` directly.
- Run metadata recorded by the wizard: `wizard.lastRunAt`, `wizard.lastRunVersion`, `wizard.lastRunCommit`, `wizard.lastRunCommand`, and `wizard.lastRunMode`.

Beyond `openclaw.json`, two CLI/state side effects are called out. `openclaw agents add` writes `agents.list[]` and optional `bindings` (it does not only write defaults). And some channels ship as plugins: when you pick one during setup, onboarding prompts to install it (npm or a local path) before it can be configured.

### State directory layout

Auth, sessions, and channel credentials are written under the `~/.openclaw/` state directory rather than into `openclaw.json`:

- Auth profiles (API keys + OAuth tokens) live at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`. `~/.openclaw/credentials/oauth.json` is legacy import-only. *(These auth-profile paths are stated under the Model/Auth step on the same source page and are owned by the [oc_reference_onboarding_flow](oc_reference_onboarding_flow.md) note; repeated here only to anchor the state-dir layout.)*
- WhatsApp credentials go under `~/.openclaw/credentials/whatsapp/<accountId>/`.
- Sessions are stored under `~/.openclaw/agents/<agentId>/sessions/`.

When the gateway-token is SecretRef-managed, the resolved plaintext value is deliberately NOT persisted into supervisor service environment metadata (per the Daemon install step on the same page) — so the secret stays in its SecretRef source, not the written service unit.

## Gateway wizard RPC

The Gateway exposes the onboarding flow over RPC so remote clients can render and drive it without re-implementing onboarding logic. The four documented methods are:

- `wizard.start`
- `wizard.next`
- `wizard.cancel`
- `wizard.status`

The page names the macOS app and the Control UI as the clients that use this surface — they "can render steps without re-implementing onboarding logic." This RPC fronts the same step machine described in the flow note; the methods correspond to starting a session, advancing a step, cancelling, and polling status.

## Signal setup (signal-cli)

When the Signal channel is enabled, onboarding can install `signal-cli` from GitHub releases. The install procedure:

- Downloads the appropriate release asset.
- Stores it under `~/.openclaw/tools/signal-cli/<version>/`.
- Writes `channels.signal.cliPath` to your config (so the Gateway knows where to invoke the binary).

Platform notes from the source page:

- JVM builds require **Java 21**.
- Native builds are used when available.
- Windows uses WSL2; the signal-cli install follows the Linux flow inside WSL.

This is the only built-in channel that ships a side binary install during onboarding; the resulting `channels.signal.cliPath` is one of the `channels.signal.*` fields written to `openclaw.json` above.

**Source**: OpenClaw documentation — `reference/wizard` (mirror `inbox/openclaw_docs/reference/wizard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
