---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - mantis
keywords:
  - openclaw mantis architecture
  - live visual e2e verification
  - before after baseline candidate
  - deterministic oracle screenshot evidence
  - crabbox warm linux vm
  - headless cdp vnc rescue
  - clawsweeper github actions ownership
  - mantis run lifecycle
topics:
  - OpenClaw
  - Mantis
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/mantis
access_control_group: ["general"]
---

# OpenClaw — Mantis Live Visual QA Architecture

## Overview

This note describes the design of **Mantis**, OpenClaw's end-to-end verification system for bugs that need a real runtime, a real transport, and visible proof. The architecture is: run a scenario against a known-bad baseline ref, capture **before** evidence, run the same scenario against a candidate ref, capture **after** evidence, then publish the comparison as artifacts a maintainer inspects from a PR or a local command. It mirrors the architecture-and-design sections of the `concepts/mantis` source page — the intro, Goals, Non goals, Ownership, Run lifecycle, Browser and VNC, Machines, Secrets, Private deployment notes, Provider expansion, and Open questions — while the CLI/scenario procedure and the evidence/artifact data model are split into sibling notes.

Mantis starts with Discord because Discord gives a high-value first lane: real bot auth, real guild channels, reactions, threads, native commands, and a browser UI where humans can visually confirm what the transport showed.

## Goals

The Mantis design pursues a fixed set of goals that frame every scenario:

- Reproduce a bug from a GitHub issue or PR with the same transport shape users see.
- Capture a **before** artifact on the baseline ref before applying the fix.
- Capture an **after** artifact on the candidate ref after applying the fix.
- Use a deterministic oracle whenever possible, such as a Discord REST reaction read or channel transcript check.
- Capture screenshots when the bug has a visible UI surface.
- Run locally from an agent-controlled CLI and remotely from GitHub.
- Preserve enough machine state for VNC rescue when login, browser automation, or provider auth gets stuck.
- Post concise status to an operator Discord channel when the run is blocked, needs manual VNC help, or finishes.

## Non Goals

The design also fixes what Mantis is deliberately not, to keep it scoped against unit tests and CI:

- Mantis is not a replacement for unit tests. A Mantis run should usually become a smaller regression test after the fix is understood.
- Mantis is not the normal fast CI gate. It is slower, uses live credentials, and is reserved for bugs where the live environment matters.
- Mantis should not require a human for normal operation. Manual VNC is a rescue path, not the happy path.
- Mantis does not store raw secrets in artifacts, logs, screenshots, Markdown reports, or PR comments.

## Ownership

Mantis lives in the OpenClaw QA stack, and its architecture splits responsibilities across five owners so transport knowledge, machine scheduling, and maintainer workflow glue stay separated:

- **OpenClaw** owns the scenario runtime, transport adapters, evidence schema, and local CLI under `pnpm openclaw qa mantis`.
- **QA Lab** owns the live transport harness pieces, browser capture helpers, and artifact writers.
- **Crabbox** owns warmed Linux machines when a remote VM is needed.
- **GitHub Actions** owns the remote workflow entrypoint and artifact retention.
- **ClawSweeper** owns GitHub comment routing: parsing maintainer commands, dispatching the workflow, and posting the final PR comment.
- **OpenClaw agents** drive Mantis through Codex when a scenario needs agentic setup, debugging, or stuck-state reporting.

This boundary keeps transport knowledge in OpenClaw, machine scheduling in Crabbox, and maintainer workflow glue in ClawSweeper.

## Run Lifecycle

A Mantis run follows a fixed 15-step lifecycle that captures the baseline and candidate on the same machine and ends with a comparison and status message:

1. Acquire credentials.
2. Allocate or reuse a VM.
3. Prepare the desktop/browser profile when the scenario needs UI evidence.
4. Prepare a clean checkout for the baseline ref.
5. Install dependencies and build only what the scenario needs.
6. Start a child OpenClaw Gateway with an isolated state directory.
7. Configure the live transport, provider, model, and browser profile.
8. Run the scenario and capture baseline evidence.
9. Stop the gateway and preserve logs.
10. Prepare the candidate ref in the same VM.
11. Run the same scenario and capture candidate evidence.
12. Compare the oracle results and visual evidence.
13. Write Markdown, JSON, logs, screenshots, and optional trace artifacts.
14. Upload GitHub Actions artifacts.
15. Post a concise PR or Discord status message.

The scenario should be able to fail in two distinct ways, and the final report must separate them so maintainers do not confuse a flaky environment with product behavior:

- **Bug reproduced**: baseline failed in the expected way.
- **Harness failure**: environment setup, credentials, Discord API, browser, or provider failed before the bug oracle was meaningful.

## Browser and VNC

The browser lane has two modes that together let CI run unattended while still allowing human rescue on the same VM:

- **Headless automation**: the default for CI. Chrome runs with CDP enabled, and Playwright or OpenClaw browser control captures screenshots.
- **VNC rescue**: enabled on the same VM when login, MFA, Discord anti-automation, or visual debugging needs a human.

The Discord observer browser profile should be persistent enough to avoid logging in for every run, but isolated from personal browser state — a profile belongs to the Mantis machine pool, not to a developer laptop. When Mantis gets stuck, it posts a Discord status message carrying the run id, scenario id, machine provider, artifact directory, VNC or noVNC connection instructions if available, and short blocker text. The first private deployment can post these messages to the existing operator channel and move to a dedicated Mantis channel later.

## Machines

Mantis should prefer AWS through Crabbox for the first remote implementation, because Crabbox provides warmed machines, lease tracking, hydration, logs, results, and cleanup; if AWS capacity is too slow or unavailable, add a Hetzner provider behind the same machine interface. The minimum VM requirements are:

- Linux with a desktop-capable Chrome or Chromium install
- CDP access for browser automation
- VNC or noVNC for rescue
- Node 22 and pnpm
- OpenClaw checkout and dependency cache
- Playwright Chromium browser cache when Playwright is used
- enough CPU and memory for one OpenClaw Gateway, one browser, and one model run
- outbound access to Discord, GitHub, model providers, and the credential broker

The VM should not keep long-lived raw secrets outside the expected credential or browser profile stores.

## Secrets

Secrets live in GitHub organization or repository secrets for remote runs, and in a local operator-controlled secret file for local runs. The recommended Discord-lane secret names are:

```text
OPENCLAW_QA_DISCORD_MANTIS_BOT_TOKEN
OPENCLAW_QA_DISCORD_DRIVER_BOT_TOKEN
OPENCLAW_QA_DISCORD_SUT_BOT_TOKEN
OPENCLAW_QA_DISCORD_GUILD_ID
OPENCLAW_QA_DISCORD_CHANNEL_ID
OPENCLAW_QA_DISCORD_NOTIFY_CHANNEL_ID
OPENCLAW_QA_REDACT_PUBLIC_METADATA=1
OPENCLAW_QA_CONVEX_SITE_URL
OPENCLAW_QA_CONVEX_SECRET_CI
OPENCLAW_QA_MANTIS_CRABBOX_COORDINATOR
OPENCLAW_QA_MANTIS_CRABBOX_COORDINATOR_TOKEN
```

Long term, the Convex credential pool should remain the normal source for live transport credentials, while GitHub secrets bootstrap the broker and fallback lanes. The Discord status-reactions workflow maps the Mantis Crabbox secrets back to the `CRABBOX_COORDINATOR` and `CRABBOX_COORDINATOR_TOKEN` environment variables that the Crabbox CLI expects, and the plain `CRABBOX_*` GitHub secret names remain accepted as a compatibility fallback. The Mantis runner must never print Discord bot tokens, provider API keys, browser cookies, auth profile contents, VNC passwords, or raw credential payloads. Public artifact uploads should also redact Discord target metadata such as bot, guild, channel, and message ids — the GitHub smoke workflow enables `OPENCLAW_QA_REDACT_PUBLIC_METADATA=1` for this reason. If a token is accidentally pasted into an issue, PR, chat, or log, rotate it after the new secret has been stored.

## Private Deployment Notes

A private deployment may already have a Mantis Discord application; reuse that application instead of creating another app when it has the right bot permissions and can be safely rotated. Set the initial operator notification channel through secrets or deployment configuration — it can point at an existing maintainer or operations channel first, then move to a dedicated Mantis channel once one exists. Do not put guild ids, channel ids, bot tokens, browser cookies, or VNC passwords in the design document; store them in GitHub secrets, the credential broker, or the operator's local secret store.

## Provider Expansion

After Discord, the same runner can extend to additional live transports, each contributing its own bug-class observables:

- **Slack**: reactions, threads, app mentions, modals, file uploads.
- **Email**: Gmail auth and message threading using `gog` where connectors are not enough.
- **WhatsApp**: QR login, re-identification, message delivery, media, reactions.
- **Telegram**: group mention gating, commands, reactions where available.
- **Matrix**: encrypted rooms, thread or reply relations, restart resume.

Each transport should have one cheap smoke scenario and one or more bug-class scenarios, and expensive visual scenarios should stay opt-in.

## Open Questions

The design leaves several open questions about identity, retention, and automation:

- Which Discord bot should be the driver, and which should be the SUT, when the existing Mantis bot is reused?
- Should the observer browser login use a human Discord account, a test account, or only bot-readable REST evidence for the first phase?
- How long should GitHub retain Mantis artifacts for PRs?
- When should ClawSweeper automatically recommend Mantis instead of waiting for a maintainer command?
- Should screenshots be redacted or cropped before upload for public PRs?

**Source**: OpenClaw documentation — `concepts/mantis` (mirror `inbox/openclaw_docs/concepts/mantis.md`)
**Last Updated**: 2026-06-22
**Status**: Active
