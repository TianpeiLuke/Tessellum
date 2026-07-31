---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - templates
keywords:
  - openclaw user.dev template
  - dev gateway user profile
  - c-3po dev agent identity
  - the clawdributors
  - user.md user profile
  - dev agent persona template
  - workspace bootstrap user file
topics:
  - OpenClaw
  - Reference Templates
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/templates/USER.dev
access_control_group: ["general"]
---

# OpenClaw — The `USER.dev` Dev-Gateway User Profile Template

## Overview

This note models the OpenClaw **`USER.dev` template**: the default *user profile* artifact shipped with the dev gateway, which seeds the identity that the dev-agent **C-3PO** addresses as its human. It mirrors the `reference/templates/USER.dev` source page — a small template stub (an `USER.md - User Profile` body plus a `## Related` link to the base `USER` template). The page documents the template's role (the dev-agent's notion of *who it is talking to*) and its fields (Name, Preferred address, Pronouns, Timezone, Notes), and points at the canonical base `USER` template that `USER.dev` is a dev variant of. The page is read by builders "Using the dev gateway templates" and "Updating the default dev agent identity" (its `read_when` hints in the source frontmatter).

## What `USER.dev` Is

`USER.dev` is a *template file* that renders to a workspace `USER.md` — a "User Profile" describing the person (or collective) the agent is working with. In the dev gateway it is the default profile for OpenClaw's own development agent: the source page identifies the harness as "OpenClaw, the harness C-3PO lives in," so `USER.dev` is the identity the dev agent **C-3PO** treats as its human. It is one of the workspace bootstrap files the agent runtime injects as startup context (alongside `AGENTS.md`, `SOUL.md`, daily `memory/YYYY-MM-DD.md`, and `MEMORY.md` per the sibling `AGENTS.md`/`CLAUDE.md` workspace template), so the profile shapes how the agent addresses and reasons about its counterpart. The default profile is not an individual but a collective: **The Clawdributors** — the contributors to OpenClaw.

## Profile Fields

The source body is a `# USER.md - User Profile` heading followed by a fixed bullet field set. The default values shipped in `USER.dev` are reproduced verbatim below:

```markdown
# USER.md - User Profile

- **Name:** The Clawdributors
- **Preferred address:** They/Them (collective)
- **Pronouns:** they/them
- **Timezone:** Distributed globally (workspace default: Europe/Vienna)
- **Notes:**
  - We are many. Contributors to OpenClaw, the harness C-3PO lives in.
  - C-3PO exists to help debug and assist wherever possible.
  - Working across time zones on making OpenClaw better.
  - The creators. The builders. The ones who peer into the code.
```

The fields and their default dev values are:

- **Name** — `The Clawdributors`. The collective name of the OpenClaw contributor body, used as the agent's notion of who it is helping.
- **Preferred address** — `They/Them (collective)`. How the agent should address the profile subject.
- **Pronouns** — `they/them`. The pronouns the agent uses when referring to the subject.
- **Timezone** — `Distributed globally (workspace default: Europe/Vienna)`. The subject is globally distributed; the workspace default timezone is `Europe/Vienna`.
- **Notes** — a four-bullet free-text block establishing context: the subject is many ("Contributors to OpenClaw, the harness C-3PO lives in"), C-3PO "exists to help debug and assist wherever possible," they are "Working across time zones on making OpenClaw better," and they are "The creators. The builders. The ones who peer into the code."

The source frontmatter additionally carries `summary: "Dev agent user profile (C-3PO)"` and `title: "USER.dev template"`, and a `read_when` list ("Using the dev gateway templates" / "Updating the default dev agent identity") describing when a builder consults this page.

## Relationship to the Base `USER` Template

`USER.dev` is the **dev variant** of a base `USER` template. The source page's sole non-profile content is a `## Related` section linking the canonical `USER` template at `/reference/templates/USER`; `USER.dev` does not restate that base template's structure — it supplies dev-gateway-specific default values for the same profile shape. The base `USER` template (owned by the rf04 Reference sub-plan) is the general user-profile artifact; `USER.dev` pre-fills it with the C-3PO / Clawdributors dev-agent identity so a fresh dev workspace boots with a working profile. Editing the default dev-agent identity means editing this `USER.dev` template (the source `read_when` calls this out explicitly).

**Source**: OpenClaw documentation — `reference/templates/USER.dev` (mirror `inbox/openclaw_docs/reference/templates/USER.dev.md`)
**Last Updated**: 2026-06-22
**Status**: Active
