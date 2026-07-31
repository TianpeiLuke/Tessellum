---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - groups
keywords:
  - openclaw group chat model
  - group chat behavior across surfaces
  - visible replies automatic message_tool
  - context visibility allowlists
  - group session keys
  - personal dms public groups single agent
  - group context fields chattype wasmentioned
  - imessage whatsapp group specifics
topics:
  - OpenClaw
  - Group Chat Model
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/channels/groups
access_control_group: ["general"]
---

# OpenClaw — The Cross-Surface Group-Chat Behavior Model

## Overview

This note models how OpenClaw behaves in group chats consistently across surfaces (Discord, iMessage, Matrix, Microsoft Teams, QQBot, Signal, Slack, Telegram, WhatsApp, Zalo): the agent lives on the operator's own messaging accounts (no separate bot user), and a group message is shaped by three independent ideas — *trigger authorization* (who may drive the agent), *reply visibility* (how the agent's output reaches the room), and *context visibility* (what supplemental context is injected into the model). It mirrors the `channels/groups` source page's behavior half — the Beginner intro, Visible replies, Context visibility and allowlists, Session keys, the single-agent personal-DM/public-group pattern, Display labels, Context fields, and the iMessage/WhatsApp specifics. The *configuration* counterpart — `groupPolicy`, mention-gating, `mentionPatterns` scoping, tool restrictions, group allowlists, and owner-only `/activation` — is the procedure sibling [oc_channels_groups_policy](oc_channels_groups_policy.md); this note covers the conceptual model those knobs tune.

## How OpenClaw Lives in a Group

OpenClaw "lives" on your own messaging accounts — there is **no separate WhatsApp bot user**. If *you* are in a group, OpenClaw can see that group and respond there. By default a group is restricted (`groupPolicy: "allowlist"`), replies require a mention unless mention gating is explicitly disabled, and visible replies in groups/channels use the `message` tool by default. In short: allowlisted senders can trigger OpenClaw by mentioning it. The page's TL;DR separates the three control axes cleanly — **DM access** is controlled by `*.allowFrom`; **group access** is controlled by `*.groupPolicy` plus allowlists (`*.groups`, `*.groupAllowFrom`); and **reply triggering** is controlled by mention gating (`requireMention`, `/activation`). The quick flow describing what happens to a group message is a fixed pipeline:

```
groupPolicy? disabled -> drop
groupPolicy? allowlist -> group allowed? no -> drop
requireMention? yes -> mentioned? no -> store for context only
mention/reply/command/DM -> user request
always-on group chatter -> user request, or room event when configured
```

A key behavioral nuance: an allowed-but-unmentioned message (when mention gating is on) is **stored for context only**, not dropped and not treated as a user request — it remains available as supplemental context for a later triggering turn. For always-on rooms that should provide quiet context unless the agent explicitly sends a visible message, the source points to [Ambient room events](https://docs.openclaw.ai/channels/ambient-room-events).

## Visible Replies (automatic vs message_tool)

For normal group/channel requests OpenClaw defaults to `messages.groupChat.visibleReplies: "automatic"`: the final assistant text posts through the legacy visible reply path unless the room is opted into message-tool-only output. The two modes embody different trust assumptions about the model. With `"message_tool"`, a shared room lets the agent decide *when* to speak by calling `message(action=send)` — this works best for latest-generation, tool-reliable models such as GPT 5.5; if the model misses that tool and returns substantive final text, OpenClaw keeps that final text **private** instead of posting it to the room. With `"automatic"` (the default, for weaker models or runtimes that do not reliably understand tool-only delivery), the agent's final assistant text *is* the visible reply path, so a model that cannot consistently call `message(action=send)` can still answer normally; even in automatic mode the agent may still use `message(action=send)` when the visible reply needs files, images, or other attachments.

Several safety and scoping behaviors round out the model. If the message tool is unavailable under the active tool policy, OpenClaw falls back to automatic visible replies instead of silently suppressing the response, and `openclaw doctor` warns about this mismatch. The global `messages.visibleReplies: "message_tool"` applies tool-only visible-reply behavior to direct chats and any other source event, while `messages.groupChat.visibleReplies` stays the more specific override for group/channel rooms; internal WebChat direct turns default to automatic final-reply delivery so Pi and Codex receive the same visible-reply contract. This model replaces the old pattern of forcing the model to answer `NO_REPLY` for most lurk-mode turns — in tool-only mode the prompt does not define a `NO_REPLY` contract, and doing nothing visible simply means not calling the message tool. Plugin-owned conversation bindings are the exception: once a plugin binds a thread and claims the inbound turn, the plugin's returned reply is the visible binding response and does not need `message(action=send)` (that reply is plugin runtime output, not private model final text). Typing indicators are still sent for direct group requests, while ambient always-on room events stay strict and quiet unless the agent calls the message tool. Sessions suppress verbose tool/progress summaries by default; `/verbose on` shows them for the current session (across direct chats, groups, channels, and forum topics) and `/verbose off` returns to final-reply-only behavior.

## Context Visibility vs Trigger Authorization

The page draws a sharp conceptual line between two different group-safety controls that are easy to conflate. **Trigger authorization** decides *who can trigger the agent* (`groupPolicy`, `groups`, `groupAllowFrom`, channel-specific allowlists). **Context visibility** decides *what supplemental context is injected into the model* — reply text, quotes, thread history, forwarded metadata. By default OpenClaw prioritizes normal chat behavior and keeps context mostly as received, which means allowlists primarily decide who can trigger actions and are **not** a universal redaction boundary for every quoted or historical snippet.

Current behavior here is channel-specific: some channels already apply sender-based filtering for supplemental context in specific paths (for example Slack thread seeding, Matrix reply/thread lookups), while other channels still pass quote/reply/forward context through as received. The page documents a planned hardening direction with three `contextVisibility` modes: `"all"` (the default) keeps current as-received behavior; `"allowlist"` filters supplemental context to allowlisted senders; and `"allowlist_quote"` is `allowlist` plus one explicit quote/reply exception. Until this hardening model is implemented consistently across channels, the page warns to expect differences by surface.

## Session Keys

Group conversations get their own session keys, distinct from direct chats:

- Group sessions use `agent:<agentId>:<channel>:group:<id>` session keys (rooms/channels use `agent:<agentId>:<channel>:channel:<id>`).
- Telegram forum topics add `:topic:<threadId>` to the group id so each topic has its own session.
- Direct chats use the main session (or per-sender if configured).
- Heartbeats are skipped for group sessions.

## Pattern: Personal DMs + Public Groups (Single Agent)

A common single-agent design works well when "personal" traffic is **DMs** and "public" traffic is **groups**. The reason is the session-key split: in single-agent mode, DMs typically land in the **main** session key (`agent:main:main`), while groups always use **non-main** session keys (`agent:main:<channel>:group:<id>`). If sandboxing is enabled with `mode: "non-main"`, those group sessions run in the configured sandbox backend while the main DM session stays on-host (Docker is the default backend if you do not choose one). This yields one agent "brain" (shared workspace + memory) but two execution postures — **DMs** get full tools on the host, while **groups** get sandbox plus restricted tools. The page notes that if you need truly separate workspaces/personas ("personal" and "public" must never mix), you instead use a second agent plus bindings via [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent). A representative config illustrates the two postures (config-key details belong to [Gateway configuration](https://docs.openclaw.ai/gateway/config-agents#agentsdefaultssandbox)):

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // groups/channels are non-main -> sandboxed
        scope: "session", // strongest isolation (one container per group/channel)
        workspaceAccess: "none",
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        // If allow is non-empty, everything else is blocked (deny still wins).
        allow: ["group:messaging", "group:sessions"],
        deny: ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"],
      },
    },
  },
}
```

To give groups access to only an allowlisted folder rather than no host access, keep `workspaceAccess: "none"` and mount only allowlisted paths into the sandbox via Docker `binds` (e.g. `"/home/user/FriendsShared:/data:ro"`, in `hostPath:containerPath:mode` form). For debugging why a tool is blocked, the page points to [Sandbox vs Tool Policy vs Elevated](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated), and for bind-mount details to [Sandboxing](https://docs.openclaw.ai/gateway/sandboxing#custom-bind-mounts).

## Display Labels

How groups are labeled in the UI follows fixed rules: UI labels use `displayName` when available, formatted as `<channel>:<token>`. The `#room` prefix is reserved for rooms/channels, while group chats use the form `g-<slug>` (lowercase, spaces become `-`, keeping the characters `#@+._-`).

## Context Fields

Group inbound payloads set a fixed set of context fields that the model can see:

- `ChatType=group`
- `GroupSubject` (if known)
- `GroupMembers` (if known)
- `WasMentioned` (the mention-gating result)
- Telegram forum topics also include `MessageThreadId` and `IsForum`.

The agent system prompt includes a group intro on the first turn of a new group session: it reminds the model to respond like a human, minimize empty lines and follow normal chat spacing, and avoid typing literal `\n` sequences. Non-Telegram groups also discourage Markdown tables, while Telegram rich-text guidance comes from the Telegram channel prompt. Importantly for safety, channel-sourced group names and participant labels are rendered as **fenced untrusted metadata**, not inline system instructions — so a hostile group name cannot inject instructions into the model.

## iMessage and WhatsApp Specifics

A few surface-specific behaviors sit on top of the general model. For **iMessage**, prefer `chat_id:<id>` when routing or allowlisting; list chats with `imsg chats --limit 20`; and group replies always go back to the same `chat_id`. For **WhatsApp**, the canonical system-prompt rules (group and direct prompt resolution, wildcard behavior, account override semantics) live in [WhatsApp](https://docs.openclaw.ai/channels/whatsapp#system-prompts), and WhatsApp-only group behavior (history injection, mention-handling details) is documented in [Group messages](https://docs.openclaw.ai/channels/group-messages) — captured in the sibling [oc_channels_group_messages](oc_channels_group_messages.md).

**Source**: OpenClaw documentation — `channels/groups` (mirror `inbox/openclaw_docs/channels/groups.md`)
**Last Updated**: 2026-06-22
**Status**: Active
