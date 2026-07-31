---
tags:
  - resource
  - terminology
  - dm-policy
  - allowlist
  - channel-security
  - access-control
  - openclaw
keywords:
  - DM Policy
  - allowFrom
  - dmPolicy
  - wildcard allowlist
  - mergeDmAllowFromSources
  - isSenderIdAllowed
topics:
  - Channel access control
  - Per-channel policy
  - OpenClaw channels security
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: null
access_control_group: ["general"]
---

# DM Policy / Allowlist

## Definition

**DM Policy / Allowlist** is OpenClaw's per-channel security gate that decides whether an inbound direct-message (DM) sender is permitted to interact with the bot on a given messaging adapter (Slack, Discord, Telegram, Matrix, etc.). A channel's `dmPolicy` selects one of four modes — `pairing` (default; sender must redeem a time-limited code), `allowlist` (sender must appear in `allowFrom`), `open` (any DM permitted; requires `"*"` in `allowFrom` as an explicit consent marker), or `disabled` (inbound DMs ignored) — while the companion `allowFrom` array (and its group-scoped sibling `groupAllowFrom`) names the senders that clear the gate. Together they replace the per-platform whitelist mechanisms each chat vendor ships with a single cross-channel policy that OpenClaw enforces uniformly inside its channel kernel.

In allowlist security terminology this is a **default-deny allowlist** with an explicit wildcard escape hatch: the `"*"` token short-circuits to "grant", and an `open` policy without `"*"` is flagged as an inconsistent configuration by the audit. The same primitive (`isSenderIdAllowed` + `compileAllowlist`) services three call sites — DM ingress, group/channel ingress, and the security audit — so the matching semantics (wildcard-first, case-insensitive dedupe, first-seen-wins canonicalization) are guaranteed identical across runtime and audit views.

## Context

Every major chat platform ships its own access-control model: Slack scopes interactions via OAuth `chat:write` + workspace-admin allowlists, Discord uses per-server DM toggles and per-channel role permissions, and Telegram bots rely on `/setjoingroups` + per-bot ID/username lists. OpenClaw centralizes these into a single `channels.<provider>.dmPolicy` + `channels.<provider>.allowFrom` config surface so a single bot deployment can sit behind Slack, Discord, and Telegram simultaneously with one allowlist source of truth. The policy is consumed by `src/channels/allow-from.ts` (source merge + terminal enforcement), `src/channels/allowlist-match.ts` (compile-once-match-many), `src/channels/allowlists/resolve-utils.ts` (canonicalization), and `src/security/dm-policy-shared.ts` (audit primitives + telemetry reason codes).

## Key Characteristics

- **Four-mode `dmPolicy` enum**: `pairing` (default) | `allowlist` | `open` | `disabled`. Each mode produces a distinct `DmGroupAccessDecision` of `allow` | `block` | `pairing` with a typed reason code (`DM_POLICY_OPEN`, `DM_POLICY_ALLOWLISTED`, `DM_POLICY_NOT_ALLOWLISTED`, etc.) for telemetry.
- **`mergeDmAllowFromSources` policy gate**: When `dmPolicy === "allowlist"` or `"open"`, the store-provided `storeAllowFrom` is dropped; the policy itself owns reachability so stale store config cannot create privilege drift. The caller's own `allowFrom` is always preserved.
- **`resolveGroupAllowFromSources` explicit-then-fallback**: Group scope prefers `groupAllowFrom` when non-empty, falls back to `allowFrom` unless the caller passes `fallbackToAllowFrom: false`. An empty array means "not explicit", not "explicit empty".
- **`isSenderIdAllowed` four-gate cascade**: (a) no entries → return `allowWhenEmpty`; (b) wildcard present → grant; (c) no sender id → deny; (d) `entries.includes(senderId)`. The wildcard-before-presence ordering is load-bearing so `["*"]` grants anonymous traffic correctly.
- **`compileAllowlist` compile-once-match-many**: Lifts a `ReadonlyArray<string>` into `{set: ReadonlySet<string>, wildcard: boolean}` for O(1) per-entry lookup; the wildcard flag is computed once at compile time, never per match.
- **Case-insensitive dedupe (`dedupeAllowlistEntries`)**: Lowercases for the seen-Set key but pushes the trimmed original-case form onto output. Identity is the lowercased form; payload preserves display fidelity. First-seen-wins.
- **Audit consistency via `DM_GROUP_ACCESS_REASON`**: A frozen `as const` reason-code enum is shared between the runtime ingress and the security audit so telemetry dashboards aggregate identical reason codes across both surfaces.
- **`open` with no wildcard is flagged**: The audit raises a `dm.open_invalid` warning when `dmPolicy === "open"` and `allowFrom` lacks `"*"` — the policy is permissive but the config does not declare it, an inconsistency that typically signals a misconfigured deployment.
- **Pinnable single-owner allowlist**: `resolvePinnedMainDmOwnerFromAllowlist` returns the sole normalized owner when `dmScope === "main"` and exactly one non-wildcard entry remains after dedupe; used to keep `main`-scope DMs safe without forbidding shared sessions outright.

## Related Terms

- **[OpenClaw — Channel Access Groups (Reusable Sender Allowlists)](../documentation/openclaw/oc_channels_access_groups.md)** — This note is the procedure for configuring OpenClaw **access groups**: named sender lists you define once and reference from channel allowlists with…

## Related Code Snippets

- [Channels — DM Pairing Allowlist](../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — primary implementation: `mergeDmAllowFromSources` + `isSenderIdAllowed` + `compileAllowlist` + dedupe
- [Security — Audit Channel DM](../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — audit half: `warnDmPolicy` + `DM_GROUP_ACCESS_REASON` + pinned-owner derivation

## References

- [Blacklist (computing) — Wikipedia](https://en.wikipedia.org/wiki/Blacklist_(computing)) — Class-1 foundational reference covering allowlist vs blocklist semantics and the default-deny posture DM Policy adopts
- [Enabling interactions with bots — Slack API](https://api.slack.com/bot-users) — Class-2 industry doc for the Slack-specific bot interaction surface that `channels.slack.dmPolicy` wraps
- [Telegram Bots FAQ](https://core.telegram.org/bots/faq) — Class-2 industry doc for Telegram's per-bot user ID / username matching that informs OpenClaw's case-insensitive Telegram allowlist normalization
- [Allowlisting vs. blocklisting — TechTarget](https://www.techtarget.com/searchsecurity/tip/Allowlisting-vs-blocklisting-Benefits-and-challenges) — supplementary Class-2 industry analysis of the default-deny / wildcard-escape-hatch tradeoff
- [OpenClaw Channels source — GitHub](https://github.com/openclaw/openclaw/tree/main/src/channels) — primary upstream implementation
