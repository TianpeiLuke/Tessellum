---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - artifacts
keywords:
  - deliverable mode
  - native attachments
  - file path extraction
  - supported file extensions
  - kanban_complete artifacts
  - Perplexity Computer comparison
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/deliverable-mode
access_control_group: ["general"]
---

# Deliverable Mode

## Overview

**Deliverable mode** is the gateway behavior that turns a generated file mentioned in an agent reply into a **native chat attachment** — not a path the user has to copy, but an inline image, a file download, or an audio bubble. When Hermes Agent runs inside a messaging gateway (Slack, Discord, Telegram, WhatsApp, Signal, etc.), the agent does **not** need to write a `MEDIA:` tag or do anything special: it generates the file, mentions its absolute path in the response, and the gateway picks the path out of the text, removes it from the visible message, and uploads the file natively. A chart shows up as an inline image, a PDF report shows up as a file download, and a spreadsheet uploads as `.xlsx`. It is a *concept* (a delivery pattern), not a single tool — it sits on top of any file-producing tool (`execute_code`, the latex/powerpoint skills, `image_generate`, `text_to_speech`) and routes their output through the gateway.

## How it works

Three pieces fit together:

1. **The agent has tools that produce files.** `execute_code` for charts via matplotlib, the `latex-pdf-report` skill for PDFs, the `powerpoint` skill for decks, `image_generate` for images, `text_to_speech` for audio, and so on.

2. **The gateway scans agent responses for file paths.** Any absolute path (`/tmp/...`) or home-relative path (`~/...`) ending in a supported extension gets extracted. Paths inside code blocks and inline code are **ignored** so code samples are never mutilated.

3. **The gateway dispatches by file type.** Images embed inline where the platform supports it; videos embed inline; audio routes to voice/audio attachments; everything else uploads as a file attachment.

## Supported file extensions

The extension of the mentioned path drives the delivery dispatch:

| Category | Extensions | Delivery |
|---|---|---|
| Images | `.png .jpg .jpeg .gif .webp .bmp .tiff .svg` | Inline embed |
| Video | `.mp4 .mov .avi .mkv .webm` | Inline embed (where supported) |
| Audio | `.mp3 .wav .ogg .m4a .flac` | Voice / audio attachment |
| Documents | `.pdf .docx .doc .odt .rtf .txt .md` | File upload |
| Data | `.xlsx .xls .csv .tsv .json .xml .yaml .yml` | File upload |
| Presentations | `.pptx .ppt .odp` | File upload |
| Archives | `.zip .tar .gz .tgz .bz2 .7z` | File upload |
| Web | `.html .htm` | File upload |

`.py`, `.log`, and other source-file extensions are **intentionally excluded** so the agent doesn't auto-ship arbitrary source files; if you want to send code to the user, use a code block.

## Encouraging the agent to produce artifacts

The agent doesn't reach for artifacts by default — it has to know to. Two ways to nudge it:

- **Per-session:** ask explicitly ("send me the comparison as a chart", "return the data as a CSV") or write your own custom-instructions / personality entry that biases toward artifact-style replies on messaging platforms.
- **Project-level:** add the bias to `AGENTS.md` / `CLAUDE.md` / `.cursorrules` in a project the agent works from, to your global persona in `~/.hermes/SOUL.md`, or as a named preset under `agent.personalities` in `~/.hermes/config.yaml` (switchable per session via `/personality`).

The mechanic the agent has to use is simple: render the file to an absolute path (e.g. `/tmp/q3-revenue.png`) and mention that path as plain text in the reply. The gateway does the rest. Paths inside fenced code blocks or backticks are ignored so code samples are never mutilated.

## Kanban: artifacts ride completion notifications

If you use Hermes' kanban multi-agent workflow, workers can attach deliverable files to their `kanban_complete` call:

```python
kanban_complete(
    summary="rendered Q3 revenue chart and report",
    artifacts=[
        "/tmp/q3-revenue.png",
        "/tmp/q3-report.pdf",
    ],
)
```

When the gateway notifier delivers the "task completed" message to whoever subscribed to the task in Slack/Telegram/etc., it also uploads each artifact as a native attachment to that chat. The human gets the deliverable and the summary in one place. Files that don't exist on disk when the notifier runs are silently skipped.

## Connecting more services with MCP

Beyond the artifact-delivery pipeline, the agent can reach into other services via MCP (Model Context Protocol). The MCP ecosystem ships community servers for most popular tools — install whichever you need:

| Service | What it unlocks |
|---|---|
| **Notion** | Read/write Notion pages, databases, query workspace |
| **GitHub** | Issues, PRs, comments, repo search beyond the gh CLI |
| **Linear** | Tickets, projects, cycles |
| **Slack** | Workspace-wide search, read other channels |
| **Gmail** | Inbox triage, send mail, label management |
| **Salesforce** | Leads, opportunities, account data |
| **Snowflake / BigQuery** | SQL against data warehouses |
| **Google Drive** | File search, contents, share management |

Install MCP servers via `~/.hermes/config.yaml` under the `mcp_servers` section. See the [MCP integration](hermes_mcp_concept_config.md) guide for the full setup guide.

## Comparison to Perplexity Computer in Slack

Perplexity Computer's Slack integration is built around the same idea: the agent generates a deliverable (chart, PDF, slide deck) and posts it back into the thread as a native attachment. Hermes Agent's deliverable mode provides the same user-facing pattern **locally**:

- Generation happens in the user's own venv / sandbox (no remote tenant).
- Files land in the chat via the same Slack `files.uploadV2` API.
- Connector breadth comes via MCP rather than a curated catalog of 400 hosted integrations — install the ones you actually use.

OAuth tokens stay on the user's machine in `auth.json` / `.env`. No hosted token storage. No multi-tenant microVM. Same end result.

**Source**: `inbox/hermes_agent_docs/user-guide/features/deliverable-mode.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/deliverable-mode
**Last Updated**: 2026-06-19
**Status**: Active
