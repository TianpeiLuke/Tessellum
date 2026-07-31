---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - security
keywords:
  - openclaw security faq
  - inbound dm pairing
  - prompt injection untrusted content
  - dmpolicy pairing allowlist open
  - security audit deep
  - blast radius reduction
  - exec approval autonomy
  - third-party skill plugin trust
topics:
  - OpenClaw
  - Security and Access Control
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/help/faq
access_control_group: ["general"]
---

# OpenClaw — Why Exposing a Local-First Control Plane Demands Access Controls

## Overview

This note captures the argument the OpenClaw FAQ's **Security and access control** section makes: that running a local-first assistant which is reachable from chat apps is acceptable *only when* you treat all inbound and external content as untrusted and apply the platform's access controls. It mirrors the `help/faq` source page's "Security and access control" `<AccordionGroup>` — the ten Q&A entries spanning inbound-DM safety, prompt injection, the language/runtime objection, exposed instances, third-party skill/plugin trust, account isolation, message autonomy, cheaper models, and the Telegram/WhatsApp pairing flows. The claims are framed as a threat model with the recurring conclusion **reduce the blast radius** rather than chase a single silver-bullet control.

## Core Claim: Treat Everything Inbound and External as Untrusted

The central argument is that the practical risk surface of a personal OpenClaw agent is **not** its implementation language but its exposure and trust boundaries. The FAQ enumerates the real risks as "gateway exposure, who can message the bot, prompt injection, tool scope, credential handling, browser access, exec access, and third-party skill or plugin trust." From this premise it follows that the operator's job is to constrain *who can reach the bot* and *what untrusted content can make the model do* — defaults are designed to reduce risk, but they must be kept in place rather than opened up.

## Argument 1 — Inbound DMs Are Untrusted; Pairing Is the Default Control

**Claim:** It is safe to expose OpenClaw to inbound DMs *because* the defaults treat inbound DMs as untrusted input. On DM-capable channels the default behavior is **pairing**: unknown senders receive a pairing code and the bot does **not** process their message until approved. Approval is `openclaw pairing approve --channel <channel> [--account <id>] <code>`; pending requests are capped at **3 per channel**, and `openclaw pairing list --channel <channel> [--account <id>]` checks whether a code arrived. Opening DMs to the public is gated behind an explicit opt-in — `dmPolicy: "open"` *and* an allowlist of `"*"` — so public exposure can only happen deliberately. The supporting check is `openclaw doctor`, which surfaces risky DM policies.

## Argument 2 — Prompt Injection Is About Content, Not Just Public Exposure

**Claim:** Prompt injection is **not only a concern for public bots**, because injection is about **untrusted content**, not just who can DM the bot. If the assistant reads external content — web search/fetch, browser pages, emails, docs, attachments, pasted logs — that content can carry instructions that try to hijack the model, and "this can happen even if you are the only sender." **The biggest risk is when tools are enabled**: a tricked model can exfiltrate context or call tools on the operator's behalf. The recommended way to *reduce the blast radius*:

- use a read-only or tool-disabled "reader" agent to summarize untrusted content
- keep `web_search` / `web_fetch` / `browser` off for tool-enabled agents
- treat decoded file/document text as untrusted too — OpenResponses `input_file` and media-attachment extraction both wrap extracted text in **explicit external-content boundary markers** instead of passing raw file text
- apply sandboxing and strict tool allowlists

## Argument 3 — Language/Runtime Is Not the Primary Control

**Counter-claim addressed:** that OpenClaw is "less safe because it uses TypeScript/Node instead of Rust/WASM." **Rebuttal:** language and runtime matter but are not the main risk for a personal agent. Rust and WASM can provide stronger isolation for some classes of code, but "they do not solve prompt injection, bad allowlists, public gateway exposure, overbroad tools, or a browser profile that is already logged in to sensitive accounts." The argument therefore relocates the security effort onto the *primary controls* the operator owns:

- keep the Gateway private or authenticated
- use pairing and allowlists for DMs and groups
- deny or sandbox risky tools for untrusted inputs
- install only trusted plugins and skills
- run `openclaw security audit --deep` after config changes

## Argument 4 — A Safer Baseline for Exposed Instances

**Prompted by:** "reports about exposed OpenClaw instances." **Claim:** first verify your actual deployment, then converge on a safer baseline. The verification step is:

```bash
openclaw security audit --deep
openclaw gateway status
```

The safer baseline asserted by the FAQ is: a Gateway bound to `loopback`, or exposed only through authenticated private access (a tailnet, SSH tunnel, token/password auth, or a correctly configured trusted proxy); DMs in `pairing` or `allowlist` mode; groups allowlisted and mention-gated unless every member is trusted; high-risk tools (`exec`, `browser`, `gateway`, `cron`) denied or tightly scoped for agents that read untrusted content; and sandboxing enabled where tool execution needs a smaller blast radius. The findings to fix *first* are explicitly ranked: "Public binds without auth, open DMs/groups with tools, and exposed browser control."

## Argument 5 — Third-Party Skills and Plugins Are Trust Decisions

**Claim:** ClawHub skills and third-party plugins should be treated "as code you are choosing to trust." ClawHub skill pages expose scan state before install, but the FAQ states plainly that "scans are not a complete security boundary" and that "OpenClaw does not run built-in local dangerous-code blocking during plugin or skill install/update flows"; operators should use the operator-owned `security.installPolicy` for local allow/block decisions. The safer pattern: prefer trusted authors and pinned versions; read the skill or plugin before enabling it; keep plugin and skill allowlists narrow; run untrusted-input workflows in a sandbox with minimal tools; and avoid giving third-party code broad filesystem, exec, browser, or secret access.

## Argument 6 — Isolate Accounts and Gate Autonomy

**Claim (account isolation):** for most setups the bot should have its **own** email, GitHub account, or phone number, because isolating it with separate accounts and numbers "reduces the blast radius if something goes wrong" and makes it easier to rotate credentials or revoke access without impacting personal accounts; the advice is to start small and grant access only to the tools and accounts actually needed. **Claim (message autonomy):** full autonomy over personal messages is **not recommended** — the safest pattern is to keep DMs in pairing mode or a tight allowlist, use a separate number or account if the bot should message on your behalf, and let it **draft, then approve before sending**; experimentation should stay on a dedicated, isolated account. **Claim (cheaper models):** smaller model tiers are usable *only* for chat-only agents with trusted input, because "smaller tiers are more susceptible to instruction hijacking" — avoid them for tool-enabled agents or untrusted content, and if a smaller model is required, lock down tools and run inside a sandbox.

## Pairing-Flow Clarifications (Telegram and WhatsApp)

The section closes with two operational clarifications that reinforce the pairing-as-control argument. On **Telegram**, pairing codes are sent **only** when an unknown sender messages the bot with `dmPolicy: "pairing"` enabled — `/start` by itself does not generate a code; check pending requests with `openclaw pairing list telegram`, or allowlist the sender id / set `dmPolicy: "open"` for immediate access. On **WhatsApp**, the default DM policy is **pairing**, so the bot will *not* message your contacts: unknown senders only get a pairing code and their message is **not processed**, and OpenClaw "only replies to chats it receives or to explicit sends you trigger." Approve with `openclaw pairing approve whatsapp <code>` and list with `openclaw pairing list whatsapp`. The wizard's phone-number prompt sets your **allowlist/owner** so your own DMs are permitted (it is not used for auto-sending); running on a personal WhatsApp number means using that number and enabling `channels.whatsapp.selfChatMode`.

**Source**: OpenClaw documentation — `help/faq` § Security and access control (mirror `inbox/openclaw_docs/help/faq.md`)
**Last Updated**: 2026-06-22
**Status**: Active
