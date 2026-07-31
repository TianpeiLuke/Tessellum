---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - multi_agent
keywords:
  - openclaw multi-agent routing
  - isolated agent agentId agentDir
  - binding most-specific wins
  - cross-agent qmd memory search
  - single-agent mode main
  - per-agent auth profiles isolation
  - deterministic message routing rules
  - agentId accountId binding glossary
topics:
  - OpenClaw
  - Multi-Agent Routing
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/multi-agent
access_control_group: ["general"]
---

# OpenClaw — Multi-Agent Isolation and Routing

## Overview

This note captures the OpenClaw **multi-agent isolation and routing concept** from the `concepts/multi-agent` source page: what one isolated agent is, single-agent versus multi-agent mode, how a single Gateway process hosts multiple fully scoped personas, cross-agent QMD memory search, and the deterministic most-specific-wins binding rules that route an inbound message to one agent. It covers the conceptual half of the page — the per-channel binding-config *procedure* (wizard, platform examples, per-agent sandbox/tool config) lives in the sibling note `oc_concepts_multi_agent_bindings_config`.

OpenClaw runs multiple *isolated* agents — each with its own workspace, state directory (`agentDir`), and session history — plus multiple channel accounts (e.g. two WhatsApps) in one running Gateway. Inbound messages are routed to the right agent through **bindings**.

## What Is "One Agent"?

An **agent** is the full per-persona scope: workspace files, auth profiles, model registry, and session store. It is a fully scoped "brain" with its own:

- **Workspace** — files, `AGENTS.md`/`SOUL.md`/`USER.md`, local notes, and persona rules. The workspace is the **default cwd**, *not a hard sandbox*: relative paths resolve inside the workspace, but absolute paths can reach other host locations unless sandboxing is enabled.
- **State directory** (`agentDir`) — the on-disk directory holding per-agent config (auth profiles, model registry) at `~/.openclaw/agents/<agentId>/`.
- **Session store** — chat history plus routing state under `~/.openclaw/agents/<agentId>/sessions`.

Auth profiles are **per-agent**. Each agent reads from its own `auth-profiles.json`:

```text
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

The source page warns: **never reuse `agentDir` across agents** (it causes auth/session collisions). Agents *can* read through to the default/main agent's auth profiles when they have no local profile, but OpenClaw does **not** clone OAuth refresh tokens into the secondary agent store. To get an independent OAuth account, sign in from that agent; if copying credentials manually, copy only portable static `api_key` or `token` profiles. Skills are loaded from each agent workspace plus shared roots such as `~/.openclaw/skills`, then filtered by the effective agent skill allowlist when configured (`agents.defaults.skills` for a shared baseline, `agents.list[].skills` for a per-agent replacement). The Gateway can host **one agent** (default) or **many agents** side-by-side. A **binding** maps a channel account (e.g. a Slack workspace or a WhatsApp number) to one of those agents.

## Paths (Quick Map)

The per-agent state layout the source page documents:

- **Config**: `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`).
- **State dir**: `~/.openclaw` (or `OPENCLAW_STATE_DIR`).
- **Workspace**: `~/.openclaw/workspace` (or `~/.openclaw/workspace-<agentId>`).
- **Agent dir**: `~/.openclaw/agents/<agentId>/agent` (or `agents.list[].agentDir`).
- **Sessions**: `~/.openclaw/agents/<agentId>/sessions`.

### Single-Agent Mode (default)

If you do nothing, OpenClaw runs a single agent:

- `agentId` defaults to **`main`**.
- Sessions are keyed as `agent:main:<mainKey>`.
- Workspace defaults to `~/.openclaw/workspace` (or `~/.openclaw/workspace-<profile>` when `OPENCLAW_PROFILE` is set).
- State defaults to `~/.openclaw/agents/main/agent`.

## Multiple Agents = Multiple People, Multiple Personalities

With **multiple agents**, each `agentId` becomes a **fully isolated persona** with:

- **Different phone numbers/accounts** (per channel `accountId`).
- **Different personalities** (per-agent workspace files like `AGENTS.md` and `SOUL.md`).
- **Separate auth + sessions** (no cross-talk unless explicitly enabled).

This lets **multiple people** share one Gateway server while keeping their AI "brains" and data isolated.

## Cross-Agent QMD Memory Search

Isolation is the default, but one agent can search another agent's QMD session transcripts by adding extra collections under `agents.list[].memorySearch.qmd.extraCollections`. Use `agents.defaults.memorySearch.qmd.extraCollections` only when every agent should inherit the same shared transcript collections.

```json5
{
  agents: {
    defaults: {
      workspace: "~/workspaces/main",
      memorySearch: {
        qmd: {
          extraCollections: [{ path: "~/agents/family/sessions", name: "family-sessions" }],
        },
      },
    },
    list: [
      {
        id: "main",
        workspace: "~/workspaces/main",
        memorySearch: {
          qmd: {
            extraCollections: [{ path: "notes" }], // resolves inside workspace -> collection named "notes-main"
          },
        },
      },
      { id: "family", workspace: "~/workspaces/family" },
    ],
  },
  memory: {
    backend: "qmd",
    qmd: { includeDefaultMemory: false },
  },
}
```

The extra-collection path can be shared across agents, but the collection name stays explicit when the path is **outside** the agent workspace. Paths **inside** the workspace remain agent-scoped, so each agent keeps its own transcript search set.

## Routing Rules (How Messages Pick an Agent)

Bindings are **deterministic** and **most-specific wins**. The tier order, highest precedence first:

1. **peer match** — exact DM/group/channel id.
2. **parentPeer match** — thread inheritance.
3. **guildId + roles** — Discord role routing.
4. **guildId** — Discord.
5. **teamId** — Slack.
6. **accountId match for a channel** — per-account fallback.
7. **Channel-level match** — `accountId: "*"`.
8. **Default agent** — fallback to `agents.list[].default`, else the first list entry, default: `main`.

Two qualifications from the source page govern ties and account scope:

- **Tie-breaking and AND semantics** — if multiple bindings match in the same tier, the first one in config order wins. If a binding sets multiple match fields (for example `peer` + `guildId`), all specified fields are required (`AND` semantics).
- **Account-scope detail** — a binding that omits `accountId` matches the **default account only**; it does not match all accounts. Use `accountId: "*"` for a channel-wide fallback across all accounts, or `accountId: "<name>"` to match one account. If you later add the same binding for the same agent with an explicit account id, OpenClaw **upgrades** the existing channel-only binding to account-scoped instead of duplicating it.

A related isolation boundary: with one shared channel account (e.g. one WhatsApp number) you can route different DMs to different agents, but **DM access control is global per account** (pairing/allowlist), *not* per agent. Direct chats collapse to the agent's **main session key**, so true per-person isolation requires **one agent per person**.

## Concepts (Glossary)

The page's vocabulary for routing:

- **`agentId`** — one "brain" (workspace, per-agent auth, per-agent session store).
- **`accountId`** — one channel account instance (e.g. WhatsApp account `"personal"` vs `"biz"`).
- **`binding`** — routes inbound messages to an `agentId` by `(channel, accountId, peer)` and optionally guild/team ids.
- Direct chats collapse to `agent:<agentId>:<mainKey>` (per-agent "main"; `session.mainKey`).

Channels that support **multiple accounts** (e.g. WhatsApp) use `accountId` to identify each login, and each `accountId` can be routed to a different agent — so one server can host multiple phone numbers without mixing sessions. To set a channel-wide default account when `accountId` is omitted, set `channels.<channel>.defaultAccount`; when unset, OpenClaw falls back to `default` if present, otherwise the first configured account id (sorted).

**Source**: OpenClaw documentation — `concepts/multi-agent` (mirror `inbox/openclaw_docs/concepts/multi-agent.md`)
**Last Updated**: 2026-06-22
**Status**: Active
