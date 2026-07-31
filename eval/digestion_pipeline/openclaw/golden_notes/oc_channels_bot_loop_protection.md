---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - bot_loop_protection
keywords:
  - openclaw bot loop protection
  - pair loop protection
  - botLoopProtection config
  - maxEventsPerWindow windowSeconds cooldownSeconds
  - allowBots bot-to-bot loop
  - channels.defaults.botLoopProtection
  - bot pair sliding-window budget
topics:
  - OpenClaw
  - Bot Loop Protection
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/bot-loop-protection
access_control_group: ["general"]
---

# OpenClaw — Bot Loop Protection (Pair Loop Guard)

## Overview

This note is the procedure for configuring OpenClaw's **bot loop protection** — the pair-loop guard that prevents two bot identities from replying to each other indefinitely once a channel accepts bot-authored messages via `allowBots`. It mirrors the `channels/bot-loop-protection` source page: the built-in defaults (`maxEventsPerWindow` / `windowSeconds` / `cooldownSeconds`), how to set a shared baseline at `channels.defaults.botLoopProtection`, the per-channel / per-account / per-conversation override precedence chain, and which channels support the guard. The guard is enforced centrally by the gateway core inbound reply runner: each supporting channel maps its inbound event into generic facts (account or scope, conversation id, sender bot id, receiver bot id), and core tracks the participant pair in both directions, applies a sliding-window budget, and suppresses the pair during a cooldown after the budget is exceeded.

## When the Guard Applies

Pair loop protection is active only when a channel lets bot-authored messages reach dispatch — that is, when `allowBots` is enabled on a channel that supports the `allowBots` path. When that path is open, the guard prevents two bot identities from replying to each other indefinitely. The guard does **not** affect normal human-authored messages, single-bot deployments, self-message filtering, or one-shot bot replies that stay under the budget. In other words, it is a targeted safeguard for the bot-to-bot exchange surface that `allowBots` opens up, and it leaves ordinary human and single-bot traffic untouched.

## Defaults

When a channel lets bot-authored messages reach dispatch, pair loop protection runs with these built-in defaults:

- `maxEventsPerWindow: 20` — a bot pair can exchange 20 events within the window.
- `windowSeconds: 60` — sliding window length.
- `cooldownSeconds: 60` — suppression time after the pair exceeds the budget.

So a given bot pair may exchange up to 20 events inside any 60-second sliding window; once that budget is exceeded the pair is suppressed for a 60-second cooldown before exchanges resume.

## Configure Shared Defaults

Set `channels.defaults.botLoopProtection` once to give every supporting channel the same baseline. Channel and account overrides can still tune individual surfaces on top of this shared default.

```json5
{
  channels: {
    defaults: {
      botLoopProtection: {
        maxEventsPerWindow: 20,
        windowSeconds: 60,
        cooldownSeconds: 60,
      },
    },
  },
}
```

Set `enabled: false` only when your channel policy intentionally allows bot-to-bot conversations without automatic suppression.

## Override Per Channel or Account

Supporting channels layer their own config over the shared default. The precedence (from highest to lowest priority) is:

- `channels.<channel>.<room-or-space>.botLoopProtection`, when the channel supports per-conversation overrides.
- `channels.<channel>.accounts.<account>.botLoopProtection`, when the channel supports accounts.
- `channels.<channel>.botLoopProtection`, when the channel supports top-level defaults.
- `channels.defaults.botLoopProtection`.
- built-in defaults.

The example below layers all of these tiers: a shared default sets `maxEventsPerWindow: 20`; Discord overrides the top-level budget to `8` and tightens the `molty` account further (`maxEventsPerWindow: 5`, `cooldownSeconds: 90`) while opting that account into `allowBots: "mentions"`; Slack and Matrix and Google Chat each set their own `allowBots` and per-channel or per-room (`groups`) budgets.

```json5
{
  channels: {
    defaults: {
      botLoopProtection: {
        maxEventsPerWindow: 20,
      },
    },
    discord: {
      botLoopProtection: {
        maxEventsPerWindow: 8,
      },
      accounts: {
        molty: {
          allowBots: "mentions",
          botLoopProtection: {
            maxEventsPerWindow: 5,
            cooldownSeconds: 90,
          },
        },
      },
    },
    slack: {
      allowBots: "mentions",
      botLoopProtection: {
        maxEventsPerWindow: 8,
      },
    },
    matrix: {
      allowBots: "mentions",
      groups: {
        "!roomid:example.org": {
          botLoopProtection: {
            maxEventsPerWindow: 5,
          },
        },
      },
    },
    googlechat: {
      allowBots: true,
      groups: {
        "spaces/AAAA": {
          botLoopProtection: {
            maxEventsPerWindow: 5,
          },
        },
      },
    },
  },
}
```

## Channel Support

Each supporting channel identifies the bot pair from its own native inbound facts, keyed by the channel's account/scope, conversation, and the two bot identities:

- **Discord**: native `author.bot` facts, keyed by Discord account, channel, and bot pair.
- **Slack**: native `bot_id` facts for accepted bot-authored messages, keyed by Slack account, channel, and bot pair.
- **Matrix**: configured Matrix bot accounts, keyed by Matrix account, room, and configured bot pair.
- **Google Chat**: native `sender.type=BOT` facts for accepted bot-authored messages, keyed by account, space, and bot pair.

Channels that do not expose a reliable inbound bot identity keep using their normal self-message and access-policy filters. They should not opt into this guard until they can identify both participants in the bot pair. Plugin implementation details for the reusable runtime utilities behind the guard are documented under the SDK runtime reference (see References).

**Source**: OpenClaw documentation — `channels/bot-loop-protection` (mirror `inbox/openclaw_docs/channels/bot-loop-protection.md`)
**Last Updated**: 2026-06-22
**Status**: Active
