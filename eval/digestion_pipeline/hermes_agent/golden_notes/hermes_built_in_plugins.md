---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugin_system
  - bundled_plugins
keywords:
  - built-in plugins
  - bundled plugins
  - disk-cleanup
  - security-guidance
  - langfuse observability
  - hermes-achievements
  - plugin discovery
topics:
  - Hermes Agent
  - Plugin System
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins
access_control_group: ["general"]
---

# Hermes Agent — Built-in Plugins

## Overview

Built-in plugins are the small set of plugins that ship **bundled inside the Hermes repository** rather than installed by the user. They live under `<repo>/plugins/<name>/` and load automatically alongside user-installed plugins in `~/.hermes/plugins/`, using the **same plugin surface as third-party plugins** — lifecycle hooks, tools, and slash commands — just maintained in-tree. The defining property is that bundling is purely about *where the code lives*, not about special privileges: a bundled plugin is discovered, opt-in, and enabled exactly like any other plugin, and a user plugin of the same name can override it. This note is the catalog of what ships, how the loader finds it, the opt-in rule, the per-plugin behaviour of the long-running hooks-based plugins, and the criteria that make a plugin a good bundling candidate.

## How discovery works

The `PluginManager` scans four sources, in order:

1. **Bundled** — `<repo>/plugins/<name>/` (what this page documents)
2. **User** — `~/.hermes/plugins/<name>/`
3. **Project** — `./.hermes/plugins/<name>/` (requires `HERMES_ENABLE_PROJECT_PLUGINS=1`)
4. **Pip entry points** — `hermes_agent.plugins`

On name collision, **later sources win** — a user plugin named `disk-cleanup` would replace the bundled one.

`plugins/memory/` and `plugins/context_engine/` are deliberately excluded from bundled scanning. Those directories use their own discovery paths because memory providers and context engines are single-select providers configured through `hermes memory setup` / `context.engine` in config.

## Bundled plugins are opt-in

Bundled plugins ship **disabled**. Discovery finds them (they appear in `hermes plugins list` and the interactive `hermes plugins` UI), but none load until you explicitly enable them:

```bash
hermes plugins enable disk-cleanup
```

Or via `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - disk-cleanup
```

This is the same mechanism user-installed plugins use. Bundled plugins are never auto-enabled — not on fresh install, not for existing users upgrading to a newer Hermes. You always opt in explicitly. To turn one off again: `hermes plugins disable disk-cleanup` (or remove it from `plugins.enabled`).

## Currently shipped

The repo ships these bundled plugins under `plugins/`. All are opt-in — enable them via `hermes plugins enable <name>`.

| Plugin | Kind | Purpose |
|---|---|---|
| `disk-cleanup` | hooks + slash command | Auto-track ephemeral files and clean them on session end |
| `security-guidance` | hooks | Pattern-match dangerous code on `write_file`/`patch` and append a security warning (or block) — 25 rules (Apache-2.0 fork of Anthropic's `claude-plugins-official` patterns) |
| `observability/langfuse` | hooks | Trace turns / LLM calls / tools to Langfuse |
| `observability/nemo_relay` | hooks | Relay observability events (turns / LLM calls / tools) to an NVIDIA NeMo endpoint |
| `teams_pipeline` | standalone | Microsoft Teams meeting pipeline — Graph-backed, transcript-first meeting summaries |
| `spotify` | backend (7 tools) | Native Spotify playback, queue, search, playlists, albums, library |
| `google_meet` | standalone | Join Meet calls, live-caption transcription, optional realtime duplex audio |
| `image_gen/openai` | image backend | OpenAI `gpt-image-2` image generation backend (alternative to FAL) |
| `image_gen/openai-codex` | image backend | OpenAI image generation via Codex OAuth |
| `image_gen/xai` | image backend | xAI `grok-2-image` backend |
| `hermes-achievements` | dashboard tab | Steam-style collectible badges generated from your real Hermes session history |
| `kanban/dashboard` | dashboard tab | Kanban board UI for the multi-agent dispatcher — tasks, comments, fan-out, board switching |

Memory providers (`plugins/memory/*`) and context engines (`plugins/context_engine/*`) are listed separately on Memory Providers — they're managed through `hermes memory` and `hermes plugins` respectively. The full per-plugin detail for the two long-running hooks-based plugins (and three other notable ones) follows.

### disk-cleanup

Auto-tracks and removes **ephemeral files** created during sessions — test scripts, temp outputs, cron logs, stale chrome profiles — without requiring the agent to remember to call a tool. Two hooks drive it: `post_tool_call` silently tracks files matching `test_*`, `tmp_*`, or `*.test.*` inside `HERMES_HOME` or `/tmp/hermes-*` (as `test` / `temp` / `cron-output`), and `on_session_end` runs the safe `quick` cleanup if any test files were tracked that turn (staying silent otherwise).

**Deletion rules** scale confirmation by risk: `test` files clean every session end (never confirm); `temp` >7 days and `cron-output` >14 days clean without confirmation; `research` >30 days (beyond the 10 newest), `chrome-profile` >14 days, and files >500 MB always require confirmation (deep mode only). A `/disk-cleanup` slash command (CLI + gateway) exposes the surface:

```
/disk-cleanup status                     # breakdown + top-10 largest
/disk-cleanup dry-run                    # preview without deleting
/disk-cleanup quick                      # run safe cleanup now
/disk-cleanup deep                       # quick + list items needing confirmation
/disk-cleanup track <path> <category>    # manual tracking
/disk-cleanup forget <path>              # stop tracking (does not delete)
```

**State** lives at `$HERMES_HOME/disk-cleanup/`: `tracked.json` (paths + category/size/timestamp), `tracked.json.bak` (atomic-write backup), and `cleanup.log` (append-only audit of every track/skip/reject/delete). **Safety**: cleanup only ever touches paths under `HERMES_HOME` or `/tmp/hermes-*`; Windows mounts (`/mnt/c/...`) are rejected; and well-known top-level state dirs (`logs/`, `memories/`, `sessions/`, `cron/`, `cache/`, `skills/`, `plugins/`, `disk-cleanup/`) are never removed even when empty.

### security-guidance

Fast pattern-matched security warnings on file writes. When `write_file` / `patch` / `skill_manage` content matches a known-dangerous pattern — `pickle.load`, `yaml.load` without `SafeLoader`, `eval(`, `os.system`, `subprocess(..., shell=True)`, JS `child_process.exec`, React `dangerouslySetInnerHTML`, raw `.innerHTML =` / `.outerHTML =` / `document.write`, Node `crypto.createCipher`, AES ECB mode, disabled TLS verification, XXE-prone `xml.etree` / `minidom` parsers, `<script src="//...">` without SRI, `torch.load` without `weights_only=True`, GitHub Actions `${{ github.event.* }}` injection — the plugin appends a `⚠️ Security guidance` block to the tool result. **The file is still written**; the model reads the warning next turn and either fixes the code or documents why it's safe. Pattern matching has a non-trivial false-positive rate, which is why warn (not block) is the default.

**Coverage:** 25 rules across unsafe deserialization, command injection, XSS sinks, crypto footguns, XXE, supply-chain (SRI), and CI/CD workflow injection. The pattern data is a **verbatim Apache-2.0 fork of Anthropic's `claude-plugins-official`** (see the plugin's `LICENSE` and `NOTICE` files for attribution). Modes are env-controlled:

| Env var | Effect |
|---|---|
| (unset) | **warn mode** (default) — file is written, warning appended to result |
| `SECURITY_GUIDANCE_BLOCK=1` | **block mode** — write refused, warning returned as the block reason |
| `SECURITY_GUIDANCE_DISABLE=1` | kill switch — plugin loads but does nothing |

**What it does not do (yet):** the upstream Anthropic plugin has two more layers — an LLM diff review on each agent turn that touched files, and an agentic commit-time review that traces data flow across files. Neither is ported; the agent can already run those reviews on demand via `delegate_task`.

### observability/langfuse

Traces Hermes turns, LLM calls, and tool invocations to Langfuse (an open-source LLM observability platform): **one span per turn, one generation per API call, one tool observation per tool call**. Usage totals, per-type token counts, and cost estimates come from Hermes' canonical `agent.usage_pricing` numbers, so the Langfuse dashboard sees the same breakdown (input / output / `cache_read_input_tokens` / `cache_creation_input_tokens` / `reasoning_tokens`) that appears in `hermes logs`. The plugin is **fail-open**: no SDK installed, no credentials, or a transient Langfuse error all turn into a silent no-op in the hook — the agent loop is never impacted.

Its four hooks map cleanly onto the trace model: `pre_api_request`/`pre_llm_call` open (or reuse) a per-turn root span "Hermes turn" and start a `generation` child for the API call; `post_api_request`/`post_llm_call` close the generation (attaching `usage_details`, `cost_details`, `finish_reason`, output + tool calls) and close the turn when there are no tool calls; `pre_tool_call` starts a `tool` child observation with sanitized `args`; and `post_tool_call` closes it with sanitized `result` (large `read_file` payloads summarized to stay under `HERMES_LANGFUSE_MAX_CHARS`). Session grouping keys off the Hermes session ID (or task ID for sub-agents) via `langfuse.propagate_attributes`. The setup wizard collects keys, `pip install`s the SDK, and adds the plugin to `plugins.enabled`:

```bash
hermes tools          # → Langfuse Observability → Cloud or Self-Hosted
```

**Performance:** the Langfuse client is cached after the first hook call; a missing-SDK/missing-credentials decision is also cached so subsequent hooks fast-return without re-checking env or reloading config.

### google_meet

A **standalone** plugin that lets the agent join, transcribe, and participate in Google Meet calls. It adds a headless virtual participant that joins a Meet URL via browser automation, live transcription of the meeting audio through the configured STT provider, a `meet_summarize` / `meet_speak` / `meet_followup` toolset, and post-meeting artifacts (transcript, speaker-attributed notes, action items) saved under `~/.hermes/cache/google_meet/<meeting_id>/`. Enabling (`hermes plugins enable google_meet`) prompts an OAuth sign-in on first use and needs a Google account with Meet access; host approval may be required if the meeting enforces "only invited participants can join." It fits recurring standups, deposition-style interviews, or any case where you'd otherwise reach for Fireflies / Otter / Grain.

### hermes-achievements

A **dashboard-only** plugin that adds a Steam-style achievements tab — 60+ collectible, tiered badges (tool-chain feats, debugging patterns, vibe-coding streaks, skill/memory usage, model/provider variety, lifestyle quirks) generated from real Hermes session history. It scans the entire `~/.hermes/state.db` on the dashboard backend, caches per-session stats by `(started_at, last_active)` fingerprint (so only new/changed sessions re-analyze), runs the first scan in a background thread, and persists unlock state to `$HERMES_HOME/plugins/hermes-achievements/state.json`. Tier progression is Copper → Silver → Gold → Diamond → Olympian; badge states are Unlocked / Discovered / Secret. Routes mount under `/api/plugins/hermes-achievements/` (`GET /achievements`, `/scan-status`, `/recent-unlocks`, `/sessions/{id}/badges`, `POST /rescan`, `/reset-state`).

Critically, this plugin shows the **dashboard-tab discovery path**: there is **nothing to enable** — `plugins.enabled` only gates lifecycle/tool plugins, while dashboard plugins are discovered purely via their `dashboard/manifest.json` and auto-register a tab on first `hermes dashboard` launch. You opt out by deleting/renaming that `manifest.json` (or overriding the plugin with a user plugin that ships no dashboard); state files survive so reinstalling preserves your unlock history.

## Adding a bundled plugin

Bundled plugins are written exactly like any other Hermes plugin. The only differences are: the directory lives at `<repo>/plugins/<name>/` instead of `~/.hermes/plugins/<name>/`; the manifest source is reported as `bundled` in `hermes plugins list`; and user plugins with the same name override the bundled version.

A plugin is a **good candidate for bundling** when it has no optional dependencies (or they're already `pip install .[all]` deps); the behaviour benefits most users and is opt-out rather than opt-in; the logic ties into lifecycle hooks the agent would otherwise have to remember to invoke; and it complements a core capability without expanding the model-visible tool surface. Counter-examples that should stay user-installable: third-party integrations needing API keys, niche workflows, large dependency trees, and anything that would meaningfully change agent behaviour by default.

**Source**: `inbox/hermes_agent_docs/user-guide/features/built-in-plugins.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins
**Last Updated**: 2026-06-19
**Status**: Active
