---
tags:
  - resource
  - terminology
  - agentic_ai
  - messaging
  - security_patterns
  - access_control
keywords:
  - DM pairing
  - direct message pairing
  - pairing code
  - hermes pairing
  - gateway pairing
  - out-of-band authorization
topics:
  - Messaging Gateway
  - Access Control
  - Agent Safety Patterns
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# DM Pairing - Direct-Message Authorization Handshake

## Definition

**DM pairing** is the user-authorization handshake of the Hermes [messaging gateway](term_messaging_gateway.md): instead of an operator hand-editing an allowlist of user IDs, an *unknown* user who direct-messages the bot is issued a **one-time pairing code**, which the operator then approves out-of-band from a trusted terminal. It is the interactive alternative to a static allowlist for answering the gateway's first security question — "can this person reach the bot at all?" — while preserving the gateway's default-deny posture (the gateway denies every user who is neither on an allowlist nor paired via DM).

The mechanism is a textbook **out-of-band (OOB) authorization** pattern: the in-band channel is the chat platform the unknown user contacted (Telegram, Discord, etc.), and the pairing code is confirmed on a separate, trusted channel — the operator's shell, via the `hermes pairing approve` command. Because admission requires action on both channels, a stranger who merely knows the bot's handle cannot grant themselves access. Pairing only governs *admission*; once a user is in, the separate admin-vs-regular-user tier split governs *what they may do*.

## Context

DM pairing lives in the cross-cutting **gateway operations** surface of the Hermes agent (the day-2 ops layer documented alongside gateway commands, allowlists, and the admin/user tier split). It is one of two admission paths into the gateway:

- **Static allowlist** — `TELEGRAM_ALLOWED_USERS`, `DISCORD_ALLOWED_USERS`, `GATEWAY_ALLOWED_USERS`, etc., set ahead of time in `.env`/config.
- **DM pairing** — issued on demand when an un-allowlisted user DMs the bot, approved later by the operator.

It is operated through the `hermes pairing` CLI command family:

```bash
# The user who DMs an un-allowlisted bot sees: "Pairing code: XKGH5N7P"
hermes pairing approve telegram XKGH5N7P     # operator admits the user
hermes pairing list                          # view pending + approved users
hermes pairing revoke telegram 123456789     # remove a previously granted user
```

Because the gateway exposes an agent with terminal access, this admission gate is a load-bearing safety control rather than a convenience feature — it is why the gateway ships locked down by default.

## Key Characteristics

- **Self-service request, operator-gated grant** — the unknown user *requests* access by DMing (and receiving a code); a human operator *grants* it via `hermes pairing approve`. This is a [human-in-the-loop](term_human_in_the_loop.md) approval, not an automatic admission.
- **One-time code** — each pairing code is single-use, conceptually a [one-time password](term_otp.md) (OTP) bound to a single admission, not a reusable credential.
- **Three hardening properties** — pairing codes (1) **expire after 1 hour**, (2) are **rate-limited** to blunt brute-force/spam, and (3) **use cryptographic randomness** so a code cannot be guessed.
- **Out-of-band confirmation** — the code travels in-band (the chat platform) but is approved out-of-band (the operator's trusted shell), so compromising one channel is insufficient.
- **Default-deny complement** — pairing is an *admission* path layered on top of a [deny-first](term_deny_first.md) posture; it never widens access beyond the operator's explicit approval.
- **Revocable** — `hermes pairing revoke <platform> <user_id>` removes a paired user, so a grant is not permanent.
- **Per-platform** — pairing is scoped per chat platform (`telegram`, `discord`, …) — a code approved on one platform does not admit the same human elsewhere.

## Related Terms

- **[OpenClaw — Connecting Discord: Bot Setup and Guild Workspace](../documentation/openclaw/oc_channels_discord_setup.md)** — This note is the connect-and-pair procedure for the OpenClaw Discord channel, mirroring the **Quick setup** and **Recommended: Set up a guild workspace**…

## References
- [Hermes Agent — Messaging Gateway (DM Pairing section)](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)
- [Out-of-band (OOB) communication and authentication — Wikipedia](https://en.wikipedia.org/wiki/Out-of-band)

---

**Last Updated**: 2026-06-19
**Status**: Active
