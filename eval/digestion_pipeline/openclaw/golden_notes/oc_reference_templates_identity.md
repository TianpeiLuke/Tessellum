---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - templates
keywords:
  - openclaw identity template
  - identity.md workspace file
  - agent self-record schema
  - name creature vibe emoji avatar
  - workspace root identity file
  - agent persona definition
  - first conversation fill-in
  - signature emoji avatar path
topics:
  - OpenClaw
  - Workspace Templates
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/templates/IDENTITY
access_control_group: ["general"]
---

# OpenClaw — IDENTITY.md Workspace Template (Agent Self-Record)

## Overview

This note models the blank **`IDENTITY.md`** workspace template — the OpenClaw self-record file an agent reads to know "Who Am I?". It mirrors the `reference/templates/IDENTITY` source page, which is the canonical *schema* (a fill-in template with five bullet fields) behind the agent-persona vocabulary; the *semantics* of the workspace-file system live in the linked `concepts/agent-workspace` page. The page's YAML header gives a `summary` of "Agent identity record", a `title` of "IDENTITY template", and a single `read_when` trigger: **"Bootstrapping a workspace manually."** The file is meant to be filled in during the agent's first conversation and saved at the workspace root.

## Purpose and Read-When Trigger

`IDENTITY.md` is, per the source page YAML, the **"Agent identity record"** — the file an agent reads to answer the H1 question "IDENTITY.md - Who Am I?". The page frames this as more than configuration: "This isn't just metadata. It's the start of figuring out who you are." Its declared `read_when` trigger is a single situation — **"Bootstrapping a workspace manually"** — so the template is the artifact you fill by hand when scaffolding a workspace outside the onboarding wizard. The page's own instruction is to **"Fill this in during your first conversation. Make it yours."**, establishing the file as the start of the agent's persistent identity rather than a one-time static config.

## Field Schema

The template body is a flat bullet list of five fill-in fields, each with an italic prompt describing what to enter (the prompts are guidance hints, not enumerated values). Reproduced verbatim from the source:

- **Name:** — _(pick something you like)_
- **Creature:** — _(AI? robot? familiar? ghost in the machine? something weirder?)_
- **Vibe:** — _(how do you come across? sharp? warm? chaotic? calm?)_
- **Emoji:** — _(your signature — pick one that feels right)_
- **Avatar:** — _(workspace-relative path, http(s) URL, or data URI)_

The `Name`, `Creature`, `Vibe`, and `Emoji` fields are free-text persona attributes (the agent's chosen name, its self-concept, the tone it comes across with, and a signature emoji). The `Avatar` field is the only one with a typed value set: it accepts a **workspace-relative path**, an **http(s) URL**, or a **data URI**. No defaults, formats, or required/optional markers beyond these are specified in the source.

## Storage Location and Avatar Notes

The source page closes with two explicit notes about where the file lives and how to set the avatar:

- **Save at workspace root** — "Save this file at the workspace root as `IDENTITY.md`." The filename and location are fixed; this is a workspace-root file, not a nested config.
- **Avatar path convention** — "For avatars, use a workspace-relative path like `avatars/openclaw.png`." This is the recommended form of the `Avatar` field's workspace-relative-path option (the other accepted forms — http(s) URL and data URI — remain valid per the field schema above).

**Source**: OpenClaw documentation — `reference/templates/IDENTITY` (mirror `inbox/openclaw_docs/reference/templates/IDENTITY.md`)
**Last Updated**: 2026-06-22
**Status**: Active
