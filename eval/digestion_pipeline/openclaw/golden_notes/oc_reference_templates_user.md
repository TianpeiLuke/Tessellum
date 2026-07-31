---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - templates
keywords:
  - openclaw user.md template
  - user profile record
  - about your human
  - name pronouns timezone notes
  - user context field
  - workspace template user
  - learn a person not a dossier
  - agent user model
topics:
  - OpenClaw
  - Workspace Templates
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/templates/USER
access_control_group: ["general"]
---

# OpenClaw — USER.md Workspace Template (About Your Human)

## Overview

This note models the blank **USER.md** workspace template — the human-profile record an OpenClaw agent maintains about the person it is helping. Its YAML header is `summary: "User profile record"`, `title: "USER template"`, and a `read_when` trigger of "Bootstrapping a workspace manually", so this is the file the onboarding wizard (or a builder by hand) scaffolds at the workspace root for the agent to fill in and keep current across sessions. The template defines a small structured field block (Name, What to call them, Pronouns, Timezone, Notes), an open-ended `## Context` prompt the agent grows over time, and a closing guidance line drawing the line between learning about a person and building a dossier. It mirrors the `reference/templates/USER.md` source page; the deeper workspace-file semantics live in the `concepts/agent-workspace` page (its in-page `## Related` target), and the agent self-record companion is the IDENTITY.md template.

## Purpose and Read-When Trigger

USER.md is the agent's record **about its human** — distinct from IDENTITY.md (the agent's record about *itself*). The source page frames it directly under the H1 **`USER.md - About Your Human`** with the italic instruction *"Learn about the person you're helping. Update this as you go."* — so the file is not a one-time form but a living profile the agent revises whenever it learns something new about the user. The YAML `read_when` value is **"Bootstrapping a workspace manually"**, marking this as the template a builder pulls in when setting up a workspace by hand (as opposed to letting the onboarding wizard generate it). The blank template ships with empty field values for the user to fill in during early conversations.

## Field Schema

The template carries a fixed bullet-field block, reproduced verbatim from the source:

- **Name:** — the user's name (value left blank in the template).
- **What to call them:** — the preferred form of address, which may differ from the formal name.
- **Pronouns:** *(optional)* — the only field the source explicitly marks optional.
- **Timezone:** — the user's timezone, used for time-aware behavior.
- **Notes:** — a free-text field for any other standing facts about the user.

Every value is empty in the blank template; the agent populates them as it learns them. The source does not prescribe value formats (no enumerations, no required syntax) beyond the optional marker on Pronouns — so the field block is a lightweight, free-form profile rather than a typed record. *(Not specified in source: any validation, length limits, or default values for these fields.)*

## The Context Section

Below the field block, the template provides an open-ended **`## Context`** section seeded with a single italic prompt: *"(What do they care about? What projects are they working on? What annoys them? What makes them laugh? Build this over time.)"* This is deliberately unstructured — it invites the agent to accumulate a richer, narrative understanding of the user (interests, active projects, irritations, sense of humor) rather than confining the user model to the fixed fields above. The instruction **"Build this over time"** reinforces that Context is grown incrementally across sessions, consistent with the H1 subtitle's *"Update this as you go."*

## Guidance — Learn a Person, Not a Dossier

After a horizontal rule, the template closes with a guidance paragraph that frames the file's intent and its limits: *"The more you know, the better you can help. But remember — you're learning about a person, not building a dossier. Respect the difference."* This is the privacy / restraint principle for the user profile: the agent is encouraged to know its human well enough to help effectively, but explicitly cautioned against turning the profile into an exhaustive surveillance record. The phrasing draws a line between helpful personalization and intrusive data collection, which the agent is expected to "respect."

## In-Page Related Link

The source page ends with a **`## Related`** section linking out to "Agent workspace" at the docs path `/concepts/agent-workspace` (canonical URL `https://docs.openclaw.ai/concepts/agent-workspace`) — the concept page that explains the workspace-file model USER.md is part of. Here that target is the planned `oc_concepts_agent_workspace` note (co01); see Related Notes below.

**Source**: OpenClaw documentation — `reference/templates/USER` (mirror `inbox/openclaw_docs/reference/templates/USER.md`)
**Last Updated**: 2026-06-22
**Status**: Active
