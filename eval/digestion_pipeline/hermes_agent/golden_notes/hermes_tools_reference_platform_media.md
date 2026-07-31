---
tags:
  - resource
  - documentation
  - hermes_agent
  - tools
  - reference
keywords:
  - hermes built-in tools
  - platform and media tools
  - browser computer_use kanban
  - image video tts vision web
  - discord spotify feishu yuanbao
  - tool gating credentials
topics:
  - Hermes Agent
  - Built-in Tools
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/reference/tools-reference
access_control_group: ["general"]
---

# Hermes Agent — Built-in Tools Reference: Platform & Media

## Overview

This is the second half of the Hermes built-in tools registry — the **platform, media, and browser tools** the agent can call. Where the [core group](hermes_tools_reference_core.md) covers local-agent capabilities (file, terminal, code execution, memory, skills, delegation, cron), this group covers tools that reach **outward**: the browser-automation toolset (plus two CDP-gated escape hatches), macOS desktop control via `computer_use`, the multimodal media tools (`image_generate`, `video_generate`, `video_analyze`, `text_to_speech`, `vision_analyze`), web search/extract, X (Twitter) search, the 9 kanban multi-agent tools, messaging `send_message`, Home Assistant, Discord (+ admin), Spotify, Feishu doc/drive, and the Yuanbao platform tools. Each tool is a schema-guarded callable in the agent's function-calling registry; **availability varies by platform, enabled toolset, and the gating credential / environment** shown in each table's "Requires environment" column. Many entries register only on a specific platform toolset (e.g. Discord on `hermes-discord`, Yuanbao on `hermes-yuanbao`) or when a backend / plugin is present. This note is the reference enumeration; the feature prose and how-to for each capability live in the owning feature docs linked at the bottom.

## `browser` toolset

The 10 core browser tools drive a headless/automation browser. `browser_navigate` initializes the session and must be called before the others; for simple retrieval the docs recommend `web_search`/`web_extract` (faster, cheaper) over full browser automation.

| Tool | Description | Requires |
|------|-------------|----------|
| `browser_navigate` | Navigate to a URL; initializes the session and loads the page. Must be called before other browser tools. | — |
| `browser_back` | Navigate back to the previous page in browser history. Requires `browser_navigate` first. | — |
| `browser_click` | Click an element identified by its ref ID from the snapshot (e.g. `@e5`). Requires `browser_navigate` + `browser_snapshot` first. | — |
| `browser_type` | Type text into an input field by ref ID; clears the field first. Requires `browser_navigate` + `browser_snapshot` first. | — |
| `browser_press` | Press a keyboard key (Enter to submit, Tab to navigate, shortcuts). Requires `browser_navigate` first. | — |
| `browser_scroll` | Scroll the page in a direction to reveal content above/below the viewport. Requires `browser_navigate` first. | — |
| `browser_snapshot` | Get a text snapshot of the page's accessibility tree; returns interactive elements with ref IDs (`@e1`, `@e2`). `full=false` compact (default), `full=true` complete. | — |
| `browser_get_images` | List all images on the page with URLs + alt text (useful to feed into vision). Requires `browser_navigate` first. | — |
| `browser_console` | Get console output and JS errors (`console.log/warn/error/info` + uncaught exceptions) to detect silent failures. | — |
| `browser_vision` | Screenshot the page and analyze it with vision AI — for CAPTCHAs, visual verification, complex layouts, or when the text snapshot is insufficient. | — |

### `browser` toolset (CDP-gated tools)

These two live in the `browser` toolset but only register when a Chrome DevTools Protocol endpoint is reachable at session start — via `/browser connect`, `browser.cdp_url` config, a Browserbase session, or Camofox.

| Tool | Description | Requires |
|------|-------------|----------|
| `browser_cdp` | Send a raw Chrome DevTools Protocol command — escape hatch for browser operations not covered by the higher-level `browser_*` tools. | CDP endpoint |
| `browser_dialog` | Respond to a native JS dialog (alert / confirm / prompt / beforeunload). Call `browser_snapshot` first — pending dialogs appear in its `pending_dialogs` field — then `browser_dialog(action='accept'\|'dismiss')`. | CDP endpoint |

## `computer_use` toolset

| Tool | Description | Requires |
|------|-------------|----------|
| `computer_use` | Background macOS desktop control via cua-driver — screenshots (SOM / vision / AX), click / drag / scroll / type / key / wait, `list_apps`, `focus_app`. Does NOT steal the user's cursor/keyboard focus. Works with any tool-capable model. macOS only. | `cua-driver` on `$PATH` (install via `hermes tools`) |

## Media toolsets — `image_gen`, `video`, `video_gen`, `vision`, `tts`

The multimodal generation/analysis tools. `image_gen` and `vision` load by default; `video` and `video_gen` are opt-in (add `--toolsets video` / `--toolsets video_gen`, or enable in `hermes tools` → Video Generation). Both video and image-generation backends ship as plugins under `plugins/video_gen/<name>/` and `plugins/image_gen/`, and each tool's description is rebuilt at session start to reflect the active backend's actual capabilities.

| Tool | Toolset | Description | Requires |
|------|---------|-------------|----------|
| `image_generate` | `image_gen` | Text-to-image or edit/transform an existing image (image-to-image) via the configured backend; pass `image_url` to edit, `reference_image_urls` for style. Model is user-configured, not agent-selectable. | `FAL_KEY` / `OPENAI_API_KEY` / xAI OAuth / `KREA_API_KEY` |
| `video_generate` | `video_gen` | Text-to-video or animate a still (image-to-video) via the configured video backend; pass `image_url` to animate, omit it to generate from text. Backend auto-routes (xAI Grok-Imagine, FAL.ai Veo/Pixverse/Kling). | Active `video_gen` plugin + its credential (e.g. `XAI_API_KEY`, `FAL_KEY`) |
| `video_analyze` | `video` | Analyze video from a URL/file path — captions, scene breakdowns, key timestamps, visual descriptions. | — |
| `vision_analyze` | `vision` | Analyze images with AI vision. On vision-capable main models, returns raw image pixels as a multimodal tool result; on text-only models, falls back to an auxiliary vision model that describes the image. Signature is identical either way. | — |
| `text_to_speech` | `tts` | Convert text to speech; returns a `MEDIA:` path the platform delivers as a voice message (Telegram voice bubble, Discord/WhatsApp audio attachment, or `~/voice-memos/` in CLI). Voice/provider configurable. | — |

## Web & search toolsets — `web`, `x_search`

| Tool | Toolset | Description | Requires |
|------|---------|-------------|----------|
| `web_search` | `web` | Search the web; returns up to 5 results by default (`limit` 1–100) with titles/URLs/descriptions. Backend operators like `site:`, `filetype:`, `intitle:`, `-term`, `"exact phrase"` may work when supported. | `EXA_API_KEY` / `PARALLEL_API_KEY` / `FIRECRAWL_API_KEY` / `TAVILY_API_KEY` |
| `web_extract` | `web` | Extract page content as markdown (also works on PDF URLs). Pages under 5000 chars return full markdown; larger pages are LLM-summarized. | `EXA_API_KEY` / `PARALLEL_API_KEY` / `FIRECRAWL_API_KEY` / `TAVILY_API_KEY` |
| `x_search` | `x_search` | Search X (Twitter) posts/profiles/threads via xAI's built-in `x_search` Responses tool — for current discussion/reactions/claims on X. Off by default (opt in via `hermes tools` → X Search); schema registers only when xAI credentials are configured (check_fn-gated). | `XAI_API_KEY` **or** xAI Grok OAuth (SuperGrok / Premium+) |

## `kanban` toolset

Registered when the agent is (a) spawned by the kanban dispatcher (`HERMES_KANBAN_TASK` env set) or (b) running in a profile that explicitly enables the `kanban` toolset. Task-scoped workers get the lifecycle tools; orchestrator profiles additionally get board-routing tools (`kanban_list`, `kanban_unblock`).

| Tool | Description | Requires |
|------|-------------|----------|
| `kanban_show` | Show the active kanban task assigned to this worker (title, description, comments, dependencies). | `HERMES_KANBAN_TASK` or `kanban` toolset |
| `kanban_list` | List board tasks with filters. Orchestrator-only; hidden from dispatcher-spawned workers. | profile with `kanban` toolset |
| `kanban_complete` | Mark the current task done with a structured handoff payload (results, artifacts, follow-ups). | `HERMES_KANBAN_TASK` or `kanban` toolset |
| `kanban_block` | Block the current task on a question — the dispatcher pauses, surfaces the question, resumes once a human replies. | `HERMES_KANBAN_TASK` or `kanban` toolset |
| `kanban_heartbeat` | Send a progress heartbeat during a long operation so the dispatcher knows the worker is alive. | `HERMES_KANBAN_TASK` or `kanban` toolset |
| `kanban_comment` | Add a comment to the task thread without changing its state — for surfacing intermediate findings. | `HERMES_KANBAN_TASK` or `kanban` toolset |
| `kanban_create` | Fan out child tasks from the current task. Used by orchestrators and follow-up-spawning workers. | `HERMES_KANBAN_TASK` or `kanban` toolset |
| `kanban_link` | Link tasks with a parent → child dependency edge. | `HERMES_KANBAN_TASK` or `kanban` toolset |
| `kanban_unblock` | Return a blocked task to `ready`. Orchestrator-only; hidden from dispatcher-spawned workers. | profile with `kanban` toolset |

## Messaging & smart-home — `messaging`, `homeassistant`

| Tool | Toolset | Description | Requires |
|------|---------|-------------|----------|
| `send_message` | `messaging` | Send a message to a connected messaging platform, or list available targets. When the user names a specific channel/person, call `send_message(action='list')` FIRST to see available targets. | — |
| `ha_call_service` | `homeassistant` | Call a Home Assistant service to control a device. Use `ha_list_services` to discover services/parameters per domain. | — |
| `ha_get_state` | `homeassistant` | Get the detailed state of a single HA entity, including all attributes (brightness, color, setpoint, sensor readings). | — |
| `ha_list_entities` | `homeassistant` | List HA entities, optionally filtered by domain (light/switch/climate/sensor/…) or area name. | — |
| `ha_list_services` | `homeassistant` | List available HA services (actions) for device control, showing parameters; use to discover how to control entities found via `ha_list_entities`. | — |

## Platform toolsets — Discord, Spotify, Feishu, Yuanbao

These register only on their respective platform toolsets. Discord registers on `hermes-discord` (gateway only, same bot token as the messaging adapter); Spotify is registered by the bundled `spotify` plugin (run `hermes spotify setup` to authorize); Feishu doc/drive are scoped to the Feishu document-comment intelligent-reply handler (`gateway/platforms/feishu_comment.py`, not exposed on `hermes-cli` or the regular Feishu chat adapter); Yuanbao registers only on the `hermes-yuanbao` platform toolset (Tencent's chat app).

| Tool | Toolset | Description | Requires |
|------|---------|-------------|----------|
| `discord` | `discord` | Read and participate in a Discord server: `search_members`, `fetch_messages`, `send_message`, `react`, `fetch_channel`, `list_channels`, and more. | `DISCORD_BOT_TOKEN` |
| `discord_admin` | `discord_admin` | Manage a Discord server via REST: list guilds/channels/roles, create/edit/delete channels, manage role grants, timeouts, kicks, bans. | `DISCORD_BOT_TOKEN` + bot permissions |
| `spotify_playback` | `spotify` | Control playback, inspect active playback state, or fetch recently played tracks. | Spotify OAuth |
| `spotify_devices` | `spotify` | List Spotify Connect devices or transfer playback to another device. | Spotify OAuth |
| `spotify_queue` | `spotify` | Inspect the queue or add an item to it. | Spotify OAuth |
| `spotify_search` | `spotify` | Search the catalog for tracks, albums, artists, playlists, shows, episodes. | Spotify OAuth |
| `spotify_playlists` | `spotify` | List, inspect, create, update, and modify playlists. | Spotify OAuth |
| `spotify_albums` | `spotify` | Fetch album metadata or album tracks. | Spotify OAuth |
| `spotify_library` | `spotify` | List, save, or remove the user's saved tracks or albums. | Spotify OAuth |
| `feishu_doc_read` | `feishu_doc` | Read the full text of a Feishu/Lark document (Docx, Doc, or Sheet) by file_type + token. | Feishu app credentials |
| `feishu_drive_add_comment` | `feishu_drive` | Add a top-level comment on a Feishu/Lark document or file. | Feishu app credentials |
| `feishu_drive_list_comments` | `feishu_drive` | List whole-document comments on a Feishu/Lark file, most recent first. | Feishu app credentials |
| `feishu_drive_list_comment_replies` | `feishu_drive` | List replies on a specific Feishu comment thread (whole-doc or local-selection). | Feishu app credentials |
| `feishu_drive_reply_comment` | `feishu_drive` | Post a reply on a Feishu comment thread, with optional `@`-mention. | Feishu app credentials |
| `yb_query_group_info` | `hermes-yuanbao` | Query basic info about a group ("派/Pai"): name, owner, member count. | Yuanbao credentials |
| `yb_query_group_members` | `hermes-yuanbao` | Query group members (for `@`-mentions, finding a user by name, listing bots). | Yuanbao credentials |
| `yb_send_dm` | `hermes-yuanbao` | Send a private/direct message to a user in a group, with optional media files. | Yuanbao credentials |
| `yb_search_sticker` | `hermes-yuanbao` | Search the built-in Yuanbao sticker (TIM face) catalogue by keyword. | Yuanbao credentials |
| `yb_send_sticker` | `hermes-yuanbao` | Send a built-in sticker to the current Yuanbao chat. | Yuanbao credentials |

**Source**: `inbox/hermes_agent_docs/reference/tools-reference.md` · https://hermes-agent.nousresearch.com/docs/reference/tools-reference
**Last Updated**: 2026-06-19
**Status**: Active
