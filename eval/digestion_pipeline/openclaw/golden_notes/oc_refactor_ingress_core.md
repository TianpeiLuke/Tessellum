---
tags:
  - resource
  - documentation
  - openclaw
  - top_level
  - channels
keywords:
  - openclaw ingress core deletion plan
  - channel ingress refactor
  - ResolvedChannelMessageIngress
  - deletion-first acceptance rule
  - core vs plugin boundary
  - message-access runtime
  - deprecated-channel-access lint
  - bundled plugin production loc budget
topics:
  - OpenClaw
  - Channel Ingress Refactor
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/refactor/ingress-core
access_control_group: ["general"]
---

# OpenClaw — Ingress Core Deletion-First Refactor Plan

## Overview

This note captures the **argument** of the OpenClaw `refactor/ingress-core` design doc: the channel-ingress refactor is **not healthy while it adds thousands of net lines**, so the plan is **deletion-first** — core centralization only counts when bundled-plugin production code gets smaller and old third-party SDK compatibility is quarantined to SDK/core shims. It mirrors every section of the source page: the LOC `## Budget` (measured against the PR merge-base), the `## Diagnosis` of why the first pass over-grew, the `## Hotspots` still positive, the `## Current Code Read` of the healthy `src/channels/message-access/runtime.ts` seam, the core-vs-plugin `## Boundary`, the `## Acceptance Rule` ("every new core helper must delete bundled plugin production code immediately"), nine `## Work Packages`, six ordered `## Deletion Waves`, the `## Do Not Move` list, the `## Verification` loop, and the `## Exit Criteria`. It is a design/deletion plan, not an end-user how-to; the code-side detail it argues over lives in the linked `repo_openclaw_channels` / `snippet_openclaw_channels_*` notes.

## Thesis: Deletion-First, Not Addition-First

The page's central claim is that the ingress refactor is unhealthy whenever it adds thousands of net lines. The desired runtime shape is: a bundled plugin event extracts platform facts locally, resolves the shared ingress **once** when facts are available, branches on generic ingress projections/outcomes, then performs platform side effects locally; an old third-party helper goes through an SDK compatibility shim to a shared-ingress-compatible projection where possible, with the old return shape preserved. The hard rule on shapes: bundled plugins should **not** translate ingress back into local `AccessResult`, `GroupAccessDecision`, `CommandAuthDecision`, `DmCommandAccess`, or `{ allowed, reasonCode }` shapes unless that type is public plugin API.

## Budget

The budget is measured against the PR merge-base with `origin/main` (merge-base `1671e7532adb`), including untracked files. Current vs required vs stretch targets are reproduced verbatim:

```text
merge-base            1671e7532adb

current:
core production       +3,922 / -546    = +3,376
docs                  +601 / -17       = +584
other                 +145 / -2        = +143
plugin production     +4,148 / -5,388  = -1,240
tests                 +2,326 / -2,414  = -88
total                 +11,142 / -8,367 = +2,775

required:
plugin production     <= -1,500
core production       <= +1,500, or paid for by larger plugin deletion
tests                 <= +1,000
total                 <= +2,000

stretch:
plugin production     <= -2,500
core production       <= +1,200
total                 <= 0
```

The minimum remaining cleanup is quantified: **plugin production needs 260 more net deleted lines**, **total needs 775 more net deleted lines**, and **core production is still +1,876 over the standalone budget unless paid down by plugin deletion**. A load-bearing accounting rule: **comment-only deletion does not count as cleanup** — the previous budget pass was too generous because it counted restored QQBot explanatory comments, so this doc tracks only executable/docs/test code movement. The page mandates re-measuring after each cleanup wave with `git merge-base HEAD origin/main`, `git diff --shortstat "$base"`, a `git diff --numstat` over `src/channels/message-access src/plugin-sdk extensions` sorted by additions, and `pnpm lint:extensions:no-deprecated-channel-access`.

## Diagnosis

The first pass added the shared ingress kernel but then left too much plugin-local authorization beside it — `platform facts -> shared ingress state and decision -> plugin-local DTO or legacy projection -> plugin-local if/else ladder` — which duplicates the model. Core production grew ~3,376 lines while bundled plugin production is 1,240 lines smaller: better than the first pass, but not inside the minimum budget. The fix remains deletion-first: delete plugin DTOs that only rename ingress fields; delete tests that only assert wrapper shape; add core helpers **only when the same patch deletes bundled plugin code**; keep old SDK compatibility in SDK/core shims only; and repack core after wrapper deletion exposes the stable shape.

## Hotspots

These bundled-production files are still net positive and must shrink (verbatim deltas):

```text
extensions/telegram/src/ingress.ts                        +126
extensions/discord/src/monitor/dm-command-auth.ts         +101
extensions/signal/src/monitor/access-policy.ts             +92
extensions/feishu/src/policy.ts                            +85
extensions/slack/src/monitor/auth.ts                       +64
extensions/googlechat/src/monitor-access.ts                +59
extensions/nextcloud-talk/src/inbound.ts                   +51
extensions/matrix/src/matrix/monitor/access-state.ts       +49
extensions/irc/src/inbound.ts                              +44
extensions/imessage/src/monitor/inbound-processing.ts      +36
extensions/qa-channel/src/inbound.ts                       +34
extensions/qqbot/src/bridge/sdk-adapter.ts                 +33
extensions/tlon/src/monitor/utils.ts                       +30
extensions/twitch/src/access-control.ts                    +22
extensions/qqbot/src/engine/commands/slash-command-handler.ts +20
extensions/telegram/src/bot-handlers.runtime.ts            +19
```

The branch is not inside the minimum budget yet; the remaining review-relevant work should **delete** repeated authorization flow, turn scaffolding, or wrapper tests before adding another core abstraction.

## Current Code Read

The healthy core seam already exists in `src/channels/message-access/runtime.ts`: it owns identity adapters, effective allowlists, pairing-store reads, route descriptors, command/event presets, access groups, and the final resolved `ResolvedChannelMessageIngress` projection. The remaining growth is mostly plugin glue layered on top of that seam. `extensions/telegram/src/ingress.ts` wraps core decisions in Telegram-specific command/event helpers while call sites still pass precomputed normalized allowlists and owner lists. `extensions/discord/src/monitor/dm-command-auth.ts`, `extensions/feishu/src/policy.ts`, `extensions/googlechat/src/monitor-access.ts`, and `extensions/matrix/src/matrix/monitor/access-state.ts` still keep local policy DTOs or legacy decision names beside ingress. `extensions/signal/src/monitor/access-policy.ts` correctly keeps Signal identity normalization and pairing replies local but still has a wrapper seam that should collapse into direct ingress consumption. `extensions/nextcloud-talk/src/inbound.ts`, `extensions/irc/src/inbound.ts`, `extensions/qa-channel/src/inbound.ts`, `extensions/zalo/src/monitor.ts`, and `extensions/zalouser/src/monitor.ts` still repeat route/envelope/turn assembly that can move to shared turn helpers outside the ingress kernel. The conclusion: moving more code into core is only useful if it deletes these plugin wrapper layers in the same patch — adding another abstraction while leaving wrapper returns in place repeats the mistake.

## Boundary

The page draws an explicit core-vs-plugin boundary. **Core owns generic policy**: allowlist normalization and matching; access-group expansion and diagnostics; pairing-store DM allowlist reads; route, sender, command, event, and activation gates; admission mapping (dispatch, drop, skip, observe, pairing); redacted state, decisions, diagnostics, and SDK compatibility projections; and reusable generic descriptors for identity, route, command, event, activation, and outcomes. **Plugins own transport facts and side effects**: webhook/socket/request authenticity; platform identity extraction and API lookups; channel-specific policy defaults; and pairing challenge delivery, replies, acks, reactions, typing, media, history, setup, doctor, status, logs, and user-facing copy. Core must stay channel-agnostic: **no Discord, Slack, Telegram, Matrix, room, guild, space, API client, or plugin-specific default** in `src/channels/message-access`.

## Acceptance Rule

The governing rule: **every new core helper must delete bundled plugin production code immediately.** The caller-count gate is reproduced verbatim:

```text
one bundled caller        reject; keep plugin-local
two bundled callers       accept only if plugin production LOC drops
three or more callers     plugin deletion must be at least 2x new core LOC
compatibility-only helper SDK/core shim only; never bundled hot paths
```

The plan says to **stop and redesign** if: plugin production LOC increases; tests grow faster than production shrinks; a bundled hot path returns a DTO that only renames `ResolvedChannelMessageIngress`; or a core helper needs a channel id, platform object, API client, or channel-specific default.

## Work Packages

Nine work packages structure the cleanup. (1) **Freeze the budget** — put LOC in the PR, keep the deprecated-ingress lint green, and include before/after LOC in cleanup commits. (2) **Delete thin DTO seams** — replace plugin-local wrapper returns with `ResolvedChannelMessageIngress`, `senderAccess`, `commandAccess`, `routeAccess`, or `ingress` directly, starting with QQBot, Telegram, Slack, Discord, Signal, Feishu, Matrix, iMessage, and Tlon; delete wrapper-shape tests and keep behavior tests. (3) **Add outcome classification only with deletions** — a generic classifier may expose `dispatch`, `pairing-required`, `skip-activation`, `drop-command`, `drop-route`, `drop-sender`, and `drop-ingress`, but it must derive from the decision graph (not reason strings) and migrate at least three plugins in the same patch. (4) **Add route descriptor builders only with deletions** — generic route-target and route-sender helpers are acceptable only if they immediately shrink route-heavy plugins (Google Chat, IRC, Microsoft Teams, Nextcloud Talk, Mattermost, Slack, Zalo, Zalo Personal). (5) **Add command/event presets only with deletions** — centralize text-command, native-command, callback, and origin-subject shapes; command consumers must default to unauthorized when no command gate ran, and events must not start pairing. (6) **Add identity presets only where they remove boilerplate** — stable-id, stable-id-plus-aliases, phone/e164, and multi-identifier helpers are allowed when raw values enter only adapter input and redacted state keeps opaque ids/counts. (7) **Share authorized turn assembly** — outside the ingress kernel, remove repeated route/envelope/context/reply scaffolding from QA Channel, IRC, Nextcloud Talk, Zalo, and Zalo Personal; core may own route/session/envelope/dispatch sequencing while plugins keep delivery and channel-specific context. (8) **Quarantine compatibility** — deprecated SDK helpers stay source-compatible, but bundled hot paths must not import deprecated ingress or command-auth facades, and compatibility tests should use fake third-party plugins, not bundled-plugin internals. (9) **Repack core** — after wrapper deletion, collapse one-use modules, remove unused exports, move compatibility projection out of hot paths, and keep focused tests for identity, route, command/event, activation, access groups, and compatibility shims.

## Deletion Waves

Six waves run **in order**; each wave must lower bundled production LOC. (1) **Wrapper collapse** (expected plugin delta −400 to −600) — replace plugin-local `resolveXAccess`, `resolveXCommandAccess`, and `accessFromIngress` result types with direct reads from `ResolvedChannelMessageIngress`; first targets are Discord DM command auth, Feishu policy, Matrix access state, Telegram ingress, Signal access policy, and the QQBot SDK adapter. (2) **Shared outcome helpers** (−200 to −350) — add one generic classifier only if it deletes repeated `shouldBlockControlCommand`, pairing, activation-skip, route-block, and sender-block ladders across at least three plugins. (3) **Route descriptor builders** (−200 to −350) — move repeated route-target and route-sender descriptor assembly into core helpers (Google Chat, IRC, Microsoft Teams, Nextcloud Talk, Mattermost, Slack, Zalo, Zalo Personal). (4) **Turn assembly sharing** (−250 to −450) — use common route/session/envelope/dispatch sequencing for simple inbound plugins (QA Channel, IRC, Nextcloud Talk, Zalo, Zalo Personal). (5) **Core repack** (core delta −300 to −700) — after plugins consume runtime projections directly, delete one-use modules, merge tiny files back into `runtime.ts` or focused siblings, and keep SDK compatibility files separate from bundled hot paths. (6) **Test pruning** (−300 to −600) — delete tests that only assert removed wrapper shapes; keep behavior tests for command denial, group fallback, origin-subject matching, activation skip, access groups, pairing, and redaction. The expected minimum landing shape after these waves:

```text
plugin production     <= -1,500
core production       about +1,800 to +2,200 before final repack
tests                 <= +500
total                 <= +2,000
```

## Do Not Move

Explicitly kept plugin-local: platform config defaults, setup UX, doctor/fix copy, API lookups, Slack owner-presence checks, Matrix alias/verification handling, Telegram callback parsing, command syntax parsing, native command registration, reaction payload parsing, pairing replies, command replies, acks, typing, media, history, and logs.

## Verification

The targeted local loop is reproduced verbatim:

```sh
pnpm lint:extensions:no-deprecated-channel-access
pnpm test src/channels/message-access/message-access.test.ts src/plugin-sdk/channel-ingress-runtime.test.ts src/plugin-sdk/access-groups.test.ts
pnpm test extensions/<changed-plugin>/src/...
pnpm plugin-sdk:api:check
pnpm config:docs:check
pnpm check:docs
git diff --check
```

Use **Testbox** for broad changed-gates / full-suite proof once the LOC trend is inside budget. Each work package records: before/after LOC by category; deleted plugin wrappers; new core helper LOC, if any; targeted tests run; and the remaining hotspot list.

## Exit Criteria

The refactor is done when: bundled production imports no deprecated channel-access or command-auth facades; compatibility code is isolated to SDK/core seams; bundled plugins consume ingress projections or generic outcomes directly; plugin production LOC is **at least 1,500 net negative** against `origin/main`; core production LOC is `<= +1,500` (or any excess is paid for while total stays `<= +2,000`); and representative tests cover redaction, route, command/event, activation, access-group, and channel-specific fallback behavior.

**Source**: OpenClaw documentation — `refactor/ingress-core` (mirror `inbox/openclaw_docs/refactor/ingress-core.md`)
**Last Updated**: 2026-06-22
**Status**: Active
