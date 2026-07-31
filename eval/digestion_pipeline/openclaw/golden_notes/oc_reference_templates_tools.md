---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - templates
keywords:
  - openclaw tools.md template
  - tools.md local notes
  - skills vs local notes
  - workspace local tool notes
  - camera ssh tts device nicknames
  - environment-specific tool details
  - blank workspace template tools
  - agent workspace cheat sheet
topics:
  - OpenClaw
  - Workspace Templates
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/templates/TOOLS
access_control_group: ["general"]
---

# OpenClaw — TOOLS.md Template (Local Tool Notes)

## Overview

This note models the blank `TOOLS.md` workspace template — the OpenClaw agent's per-user "local notes" file for environment-specific tool details — mirroring the `reference/templates/TOOLS` source page (H1 `# TOOLS.md - Local Notes`). The page is a starter file the onboarding wizard scaffolds into the workspace root for the user to fill in. Its YAML front matter carries `summary: "Workspace template for TOOLS.md"`, `title: "TOOLS.md template"`, and a `read_when` trigger of "Bootstrapping a workspace manually" — i.e., the file is referenced when a workspace is set up by hand rather than through the wizard. The body frames the core distinction the template exists to enforce: "Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup." The page has three H2 sections — `## What Goes Here`, `## Examples` (with `### Cameras`, `### SSH`, `### TTS` subsections inside a single markdown code fence), and `## Why Separate?` — plus a `## Related` pointer to `/concepts/agent-workspace`. The `.dev` instantiation (the C-3PO worked example with `imsg`/`sag`) lives in the sibling note `oc_reference_templates_tools_dev.md`; this note documents the blank schema and the skills-vs-local-notes rationale.

## What This File Is

`TOOLS.md` is one of the markdown workspace-root files an OpenClaw agent reads on session boot, alongside its identity, soul, and user records. Where skills are shared, reusable units that define _how_ a tool works, `TOOLS.md` is the user-owned scratchpad for the specifics unique to a given deployment — the local annotations a skill cannot know. The source frames it plainly: it "is your cheat sheet" and the closing line invites the user to "Add whatever helps you do your job." The file is descriptive (it records local conventions and device/tool details the agent should keep in mind) rather than a registry that declares which tools exist; that callable tool surface is supplied by skills, which this file merely annotates with per-environment notes.

## What Goes Here

The `## What Goes Here` section enumerates the kinds of environment-specific details the file is meant to hold ("Things like"):

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

Each item is a piece of local context that varies per setup and that a shared skill cannot embed — the names, aliases, and preferences that let the agent act correctly against the user's particular hardware and accounts.

## Examples

The `## Examples` section provides a single fenced markdown block showing the recommended shape: per-tool `###` subheadings (Cameras, SSH, TTS), each followed by bullet notes that map a friendly name/alias to its real target plus any relevant attributes. Reproduced verbatim from the source page:

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

These examples are illustrative starter content, not a fixed schema: the Cameras entries map a nickname to a location and capability, the SSH entry maps a host alias to its IP and login user, and the TTS entries record a preferred voice and a default playback speaker. A user adapts these to their own devices, hosts, and preferences.

## Why Separate?

The `## Why Separate?` section gives the rationale for keeping local notes out of shared skills: "Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure." Two concrete benefits follow from this separation. First, **maintainability**: because the user's specifics live in `TOOLS.md` rather than inside skill definitions, skills can be updated (or re-fetched/replaced) without overwriting the user's accumulated local notes. Second, **privacy/safety**: because infrastructure details (camera locations, SSH IPs and logins, speaker layout) stay in the user-owned file, skills can be shared or published without leaking that private setup information. This is the same shared-versus-local boundary that motivates separating reusable capability packages from per-user configuration.

**Source**: OpenClaw documentation — `reference/templates/TOOLS` (mirror `inbox/openclaw_docs/reference/templates/TOOLS.md`)
**Last Updated**: 2026-06-22
**Status**: Active
