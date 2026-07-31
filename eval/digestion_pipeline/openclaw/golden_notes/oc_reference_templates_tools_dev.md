---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - templates
keywords:
  - openclaw tools.dev template
  - tools.md user tool notes
  - c-3po dev agent tools
  - imsg imessage sms tool
  - sag elevenlabs tts tool
  - user tool notes editable
  - built-in tools provided internally
  - dev gateway templates
topics:
  - OpenClaw
  - Workspace Templates
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/templates/TOOLS.dev
access_control_group: ["general"]
---

# OpenClaw — TOOLS.dev Template (C-3PO User Tool Notes)

## Overview

This note models the `TOOLS.dev.md` workspace template — the worked example of the blank `TOOLS.md` "local notes" file, shipped as part of OpenClaw's `--dev`-mode debug-agent (C-3PO) persona. It mirrors the `reference/templates/TOOLS.dev` source page: the file's YAML summary (`"Dev agent tools notes (C-3PO)"`), its `read_when` triggers ("Using the dev gateway templates", "Updating the default dev agent identity"), the H1 framing that this is a `# TOOLS.md - User Tool Notes (editable)` file holding *the user's* notes about external tools and conventions, the explicit clarification that it "does not define which tools exist; OpenClaw provides built-in tools internally", and the two `## Examples` entries — `imsg` (iMessage/SMS) and `sag` (ElevenLabs TTS). The blank-template schema and the skills-vs-local-notes rationale live in its blank counterpart note (`oc_reference_templates_tools.md`); this note documents the `.dev` instantiation as the example.

## What This File Is

`TOOLS.dev.md` is the dev companion of the blank `TOOLS.md` workspace template — a markdown file the agent reads from the workspace root on session boot. Its YAML front matter carries `summary: "Dev agent tools notes (C-3PO)"` and `title: "TOOLS.dev template"`, and a `read_when` list with two triggers: "Using the dev gateway templates" and "Updating the default dev agent identity". The file body opens with the H1 `# TOOLS.md - User Tool Notes (editable)` and the framing that it is a user-owned, editable scratchpad: "This file is for _your_ notes about external tools and conventions." Crucially, the source states the file "does not define which tools exist; OpenClaw provides built-in tools internally" — i.e., the TOOLS file is descriptive (local conventions, preferences, device/tool specifics), not a registry that declares or wires up the agent's callable tool surface. That surface is supplied by OpenClaw's built-in tools (via skills), which TOOLS.dev merely annotates with user-specific notes.

## Example Tool Notes (C-3PO Conventions)

The source page gives two `## Examples` entries as the starter content for the `--dev` agent, each a named external tool with usage conventions:

### imsg

The `imsg` entry covers the iMessage/SMS messaging tool. Its starter notes are: "Send an iMessage/SMS: describe who/what, confirm before sending." and "Prefer short messages; avoid sending secrets." These are conventions (confirm-before-send, brevity, no secrets) the agent should follow when function-calling the messaging tool, not a definition of the tool itself.

### sag

The `sag` entry covers the text-to-speech tool (ElevenLabs TTS). Its single starter note is: "Text-to-speech: specify voice, target speaker/room, and whether to stream." This records the parameters a user cares about when invoking TTS — which voice, which target speaker/room to play through, and whether to stream the audio.

After the two examples the template closes the section with an open invitation: "Add whatever else you want the assistant to know about your local toolchain." The page's own `## Related` section links back to the blank `TOOLS.md template` at `/reference/templates/TOOLS` (digested as the sibling note `oc_reference_templates_tools.md`).

**Source**: OpenClaw documentation — `reference/templates/TOOLS.dev` (mirror `inbox/openclaw_docs/reference/templates/TOOLS.dev.md`)
**Last Updated**: 2026-06-22
**Status**: Active
