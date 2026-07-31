---
title: Hermes Agent Docs Digestion — Sub-Plan 08b — Web & Tool Surface
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/
pages:
  - user-guide/features/browser.md
  - user-guide/features/web-search.md
  - user-guide/features/x-search.md
  - user-guide/features/computer-use.md
  - user-guide/features/lsp.md
  - user-guide/features/skins.md
  - user-guide/features/tool-search.md
  - user-guide/features/overview.md
  - user-guide/features/kanban-worker-lanes.md
---

# Sub-Plan 08b: Web & Tool Surface (browser / web-search / x-search / computer-use / lsp / skins / tool-search / features-overview / kanban-worker-lanes)

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP08b's note
> filenames/BBs/coverage are defined. **Part b of the SP08 split** (SP08a = media: voice/tts/vision/
> spotify/image-gen/deliverable; SP08b = web & tool surface, this file).

## Scope

The web-facing and tool-surface features of Hermes Agent: the multi-backend **browser automation**
toolset (cloud + local CDP + Camofox), **web search & extract** (8 backends incl. self-hosted SearXNG),
**X (Twitter) search** via Grok, macOS **computer use** (background desktop control), the **LSP**
semantic-diagnostics layer wired into write/patch, CLI **skins & themes**, **Tool Search**
progressive-disclosure for large tool catalogs, the **features overview** navigation page, and the
**kanban worker-lanes** contract. Source = 9 mirrored pages in `inbox/hermes_agent_docs/`
(all substantive). **P2 / features.** SP08b owns ONE new term capture (`term_browser_automation`) and
links existing verified terms (`term_cdp`, `term_subagent`, `term_kanban`, `term_computer_vision`,
`term_multimodal`, `term_autonomous_coding_agents`, `term_agent_harness`, …).

## Content Strategy

- **One BB per note.** `browser.md` (4121w, 33 code) exceeds density caps and mixes a `model` (backend
  matrix + session/dialog architecture) with a `procedure` (per-provider setup + tool usage) → split
  into 2 notes (see Split Decisions). Every other page is one BB-cohesive note.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content:
  the `config.yaml` web/browser blocks (SP02 `hermes_messaging_media_settings`), MCP integration
  (SP09 `hermes_mcp`), the browser-supervisor developer internals (SP18 `hermes_browser_supervisor`),
  the kanban user intro + tutorial (SP06b `hermes_kanban*`), xAI Grok OAuth setup guide (SP15), vision
  toolset (SP08a `hermes_vision`), image-gen / voice / tts (SP08a). `overview.md` links to every feature
  page across the corpus → it is the in-features navigation hub.
- **Collision (augment): `term_code_browser.md` (73L, active, concept) is the generic code-navigation /
  source-browsing concept, NOT the Hermes browser-automation tool** — a textbook LIKE false-positive
  (master caution list: `browser tool` ≠ `term_code_browser`). SP08b CREATES the NEW
  `term_browser_automation` term + the `hermes_browser_*` doc notes; do NOT link `term_code_browser`.
- **Collision: `term_cdp.md` (active) IS the Chrome DevTools Protocol** — relevant; LINK from the
  browser notes, do not recreate.

## Source Pages (Measured 2026-06-15, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/features/browser.md | 4121 | 33 | MIXED model+procedure | 2 (split) |
| user-guide/features/web-search.md | 2102 | 29 | procedure | 1 |
| user-guide/features/x-search.md | 1153 | 2 | procedure | 1 |
| user-guide/features/computer-use.md | 1088 | 4 | procedure | 1 |
| user-guide/features/lsp.md | 1392 | 5 | model | 1 |
| user-guide/features/skins.md | 1642 | 6 | procedure | 1 |
| user-guide/features/tool-search.md | 1044 | 4 | model | 1 |
| user-guide/features/overview.md | 921 | 0 | navigation | 1 |
| user-guide/features/kanban-worker-lanes.md | 1447 | 1 | model | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **10 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_browser_automation_backends.md` | model | browser §intro (6 backend modes), §Overview (accessibility-tree model, key capabilities), §Available Tools (browser_navigate/snapshot/click/type/scroll/press/back/get_images/vision/console/cdp/dialog), §Session Recording, §Stealth Features, §Session Management, §Limitations | ~2000 | The browser-automation model: six backend modes (Browserbase / Browser Use / Firecrawl cloud, Camofox + local Chromium CDP + agent-browser local), accessibility-tree page representation with `@e` ref IDs, the 12 `browser_*` tools (incl. `browser_cdp` passthrough + `browser_dialog` via CDP supervisor), session isolation/recording/stealth/cleanup, limitations. |
| 2 | `hermes_browser_automation_setup.md` | procedure | browser §Setup (Nous tip), §Browserbase/Browser Use/Firecrawl cloud modes, §Hybrid routing (cloud public + local private), §Camofox local mode (persistence, externally-managed sessions, VNC), §Local Chromium CDP (`/browser connect`), §WSL2+Windows Chrome (prefer MCP), §Local browser mode, §Optional Env Vars, §Install agent-browser, §Practical Examples | ~1600 | Per-backend setup procedure: cloud API keys (Browserbase priority), hybrid cloud/local-private-URL auto-routing, Camofox Docker + persistent/externally-managed sessions, `/browser connect` CDP attach (CLI-only slash command), WSL2-prefers-MCP guidance, `agent-browser` install, env knobs, worked form-fill / dynamic-content examples. |
| 3 | `hermes_web_search_extract.md` | procedure | web-search §intro (`web_search`/`web_extract`), §Backends (8-provider table), §How web_extract handles long pages (size tiers, aux model), §Setup (per provider incl. SearXNG self-host), §Configuration (single/per-capability/auto-detect), §Verify, §Troubleshooting, §Optional skill searxng-search | ~1600 | The two model-callable web tools: `web_search` (8 backends — Firecrawl default, free SearXNG/DDGS, Brave/Tavily/Exa/Parallel/xAI) and `web_extract` (size-driven auxiliary-model summarization tiers), per-capability split, auto-detection precedence, SearXNG Docker self-host, troubleshooting. |
| 4 | `hermes_x_search_grok.md` | procedure | x-search §intro, §Authentication (OAuth vs API key, check_fn gating), §Enabling the tool, §Configuration (model/timeout/retries), §Tool parameters (handles/dates/image-video understanding, returns incl. degraded), §Date validation, §Example, §Troubleshooting | ~1000 | The `x_search` tool: searches X posts/threads via Grok's server-side `x_search` on the Responses API; dual-credential gating (SuperGrok OAuth preferred over `XAI_API_KEY`), config knobs, the parameter set + `degraded` unsourced-answer flag, client-side date validation, troubleshooting. |
| 5 | `hermes_computer_use_macos.md` | procedure | computer-use §intro, §How it works (cua-driver MCP, SkyLight SPIs), §Enabling (CLI vs toolset), §Keeping cua-driver up to date, §Quick example, §Provider compatibility, §Safety, §Token efficiency, §Limitations, §Configuration, §Troubleshooting | ~1000 | Background macOS desktop control: the `computer_use` toolset speaks MCP/stdio to `cua-driver` (SkyLight private SPIs — no cursor warp / Space switch), any tool-capable vision model, SOM/ax capture modes, install via `hermes computer-use install`, multi-layer safety guardrails, 4-layer screenshot-token optimization, macOS-only limitations. |
| 6 | `hermes_lsp_diagnostics.md` | model | lsp §intro, §When LSP runs (git-gated, layered syntax→LSP), §Supported languages (~25-server table), §CLI, §Configuration (per-server overrides), §Installation locations, §Performance characteristics, §Disabling, §Troubleshooting | ~1300 | The LSP semantic-diagnostics model: ~25 real language servers run as background subprocesses, feeding NEW (baseline-diffed) diagnostics into the post-write lint check on `write_file`/`patch`; git-workspace-gated, lazy-spawned, two independent channels (`lint` syntax + `lsp_diagnostics` semantic), Hermes-owned install staging, never-breaks-a-write fallback. |
| 7 | `hermes_skins_themes.md` | procedure | skins §intro (skin vs personality), §Change skins (`/skin`, config), §Built-in skins (9), §Complete configurable keys (colors/spinner/branding/other), §Custom skins (template + minimal), §Hermes Mod visual editor, §Operational notes | ~1300 | CLI visual presentation: `/skin` (session-only) vs `display.skin` config (permanent), the 9 built-in skins, the full configurable-key surface (colors, spinner faces/verbs/wings, branding, tool_prefix/emojis, banner art), custom-skin YAML inheriting from `default`, the community Hermes Mod editor, precedence/fallback notes. |
| 8 | `hermes_tool_search.md` | model | tool-search §intro, §How it works (3 bridge tools), §When does it activate (auto threshold), §Configuration, §When NOT to use, §Trade-offs, §Implementation details (BM25 retrieval, stateless catalog, session-scoped) | ~1000 | The progressive-disclosure tool-search model: MCP + non-core plugin tools replaced by `tool_search`/`tool_describe`/`tool_call` bridges when deferrable schemas would exceed ~10% of context (core tools never defer); BM25 retrieval over name/description/params, session-scoped stateless catalog, prompt-cache + round-trip trade-offs, `auto`/`on`/`off` modes. |
| 9 | `hermes_features_overview.md` | navigation | overview §intro, §Core, §Automation, §Media & Web, §Integrations, §Customization | ~700 | In-features navigation hub: indexes every Hermes feature (Core / Automation / Media & Web / Integrations / Customization) with one-line descriptions and link-outs to the owning doc note across SP05/06/08/09/10. The `hermes setup --portal` one-command tip. |
| 10 | `hermes_kanban_worker_lanes.md` | model | kanban-worker-lanes §intro, §The hierarchy, §What a lane provides (assignee/spawn/terminator), §Outputs + review-required convention, §Logs and audit trail, §Existing lane shapes (profile/orchestrator), §Adding external CLI worker lane, §Failure modes | ~1300 | The kanban worker-lane contract: a lane = assignee string + spawn mechanism (`hermes -p <assignee> chat` with `HERMES_KANBAN_*` env) + lifecycle terminator (`kanban_complete`/`kanban_block`/reap); the review-required block convention, audit trail via `task_runs`/`task_events`, profile vs orchestrator lane shapes, the not-yet-paved external-CLI lane, dispatcher-handled failure modes (stale claim TTL, crash reap, stranded detection). |

**SP08b totals:** 10 notes · procedure 5 · model 4 · navigation 1 · concept 0 (the one concept,
browser-automation, is captured as the NEW `term_browser_automation`, not a doc note).
9 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 10 · procedure 5 · model 4 · navigation 1 · concept 0.
- Source: 9 digested pages (~14.9K words) → ~12.8K words of notes (modest compression via link-outs to
  config / MCP / kanban-intro / developer-internals owning SPs).
- BB mix: procedure 50%, model 40%, navigation 10%.

## Section Coverage Map

```
browser.md (4121w, 33 code)
├── intro (6 backend modes) ─────────────────────────────── → Note 1 (model: backend enumeration)
├── Overview (accessibility tree, @e refs, key capabilities) → Note 1
├── Setup (Nous tip) / Browserbase / Browser Use / Firecrawl cloud modes → Note 2 (Nous Portal→SP14)
├── Hybrid routing (cloud-public + local-private URLs) ───── → Note 2
├── Camofox local mode (persistence / externally-managed / VNC) → Note 2
├── Local Chromium CDP (`/browser connect`) / status / disconnect → Note 2 (CDP term=link term_cdp)
├── WSL2 + Windows Chrome (prefer MCP) ──────────────────── → Note 2 (MCP→SP09; WSL2→SP03)
├── Local browser mode / Optional Env Vars / Install agent-browser → Note 2
├── Available Tools (browser_navigate…browser_dialog, 12 tools) → Note 1 (model: tool surface)
├── Session Recording / Stealth Features / Session Management → Note 1
├── Practical Examples (form fill / dynamic content) ─────── → Note 2
└── Limitations ─────────────────────────────────────────── → Note 1
web-search.md (2102w) ── all sections ─────────────────────── → Note 3 (config blocks→SP02; xai oauth→SP15; searxng skill→SP21 catalog)
x-search.md (1153w) ──── all sections ─────────────────────── → Note 4 (xai-grok-oauth guide→SP15; tools-reference→SP21; web-search→Note 3)
computer-use.md (1088w) ─ all sections ────────────────────── → Note 5 (browser cross-platform→Notes 1/2; vision→SP08a; approvals→SP02/06b)
lsp.md (1392w) ───────── all sections ─────────────────────── → Note 6 (write_file/patch tools→SP05; HERMES_HOME→SP02; tools-runtime→SP18)
skins.md (1642w) ─────── all sections ─────────────────────── → Note 7 (personality→SP05; profiles→SP04; TUI status bar→SP02)
tool-search.md (1044w) ─ all sections ─────────────────────── → Note 8 (MCP→SP09; toolsets→SP05/SP21; hooks/guardrails→SP06b)
overview.md (921w) ───── all sections ─────────────────────── → Note 9 (link-outs to every feature SP)
kanban-worker-lanes.md (1447w) ── all sections ────────────── → Note 10 (kanban intro+tutorial→SP06b; profiles→SP04; delegation→SP06a; kanban-worker skill→SP21)
```

No source H2/H3 orphaned. All 9 pages fully covered; feature-detail intentionally routed to owning SPs
as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| browser.md (4121w, 33 code, MIXED) | Note 1 (`hermes_browser_automation_backends`, model) + Note 2 (`hermes_browser_automation_setup`, procedure) | >2500w AND >6 code AND mixes a backend/tool **model** (what the backends + tool surface ARE) with the per-backend **setup procedure** (how to configure each). BB-atomicity split; each half ≤2000w and curated to ≤6 load-bearing code blocks (33 source blocks → keep canonical example per backend/tool, summarize rest in prose). |

All other pages are single-BB and ≤2500w → 1 note each, no split.

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note / slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_browser_automation_backends`, `hermes_browser_automation_setup` | none substantive in `documentation/` (no `hermes_agent/` notes exist yet); cc analogue `cc_chrome_browser_automation` is a DIFFERENT product | NEW | CREATE; link cc analogue as a cross-tool reference. |
| `hermes_web_search_extract` | `term_information_retrieval`, `term_bm25`, `term_web_scraping`(absent) | **NOT a dup** — those are component concepts | CREATE; LINK component terms. |
| `hermes_x_search_grok` | none | NEW | CREATE. |
| `hermes_computer_use_macos` | cc analogue `cc_computer_use` / `cc_computer_use_safety` (DIFFERENT product) | **NOT a dup** — different agent's computer-use docs | CREATE; link cc analogue as cross-tool reference. |
| `hermes_lsp_diagnostics` | `term_ast`, `term_language_server`(absent) | **NOT a dup** — `term_ast` is a component | CREATE; LINK `term_ast`. |
| `hermes_skins_themes` | cc analogue `cc_terminal_themes` (DIFFERENT product); `term_persona`/`term_theme`(absent) | **NOT a dup** — skin = visual layer, distinct from personality (`term_persona`) | CREATE; LINK `term_persona` (contrast); link cc analogue. |
| `hermes_tool_search` | cc analogue `cc_mcp_tool_search` (DIFFERENT product); `term_bm25`, `term_context_window` | **NOT a dup** — those are component concepts | CREATE; LINK component terms; link cc analogue. |
| `hermes_features_overview` | `hermes_learning_path` (SP01, navigation) | **NOT a dup** — learning-path routes by experience/use-case (reader router); features-overview indexes the FEATURE set by category | CREATE; cross-link the two navigation notes. |
| `hermes_kanban_worker_lanes` | `term_kanban.md` (active), SP06b `hermes_kanban*` (not yet created) | **NOT a dup** — `term_kanban` is the concept; SP06b owns the user intro/tutorial; this is the worker-lane CONTRACT model | CREATE; LINK `term_kanban`; cross-link SP06b kanban notes at finalization. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the `term_code_browser` hit is a confirmed LIKE false-positive
read at audit; the cc_* analogues are a DIFFERENT product (Claude Code) — link as cross-tool references,
not dups). New `hermes_agent/` folder → no doc-doc collisions (intra-series links resolve at finalization).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> Floor RAISED 2026-06-19 to the **FOUR-FLOOR standard** (master directive — supersedes both the 2026-06-14
> ≥8 term/≥8 snippet/≥5 doc floor AND the interim 3-floor ≥8 term/≥5 code-repo/≥10 doc "snippets-as-bonus" wording):
> each note's `## Related Notes` now carries FOUR COUNTED, relevancy-selected groups —
> digest the Hermes SOURCE CODE; pick the modules that implement what THIS doc note describes), ≥10 snippet notes
> pick the ≥10 whose CODE this note documents), ≥10 documentation notes (`../../documentation/`, sibling `hermes_*`
> + other relevant existing doc notes)** — all relevancy-selected, each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`.
> **The snippet group is NO LONGER a bonus — it is the third COUNTED floor, raised from the prior 8 to ≥10**; the
> previously-mapped snippets are retained and topped up to ≥10. Relevancy first, never pad.
> and are allowed un-verified. The 13 source-code repos: `repo_hermes_agent` (top-level: setup/config), `_agent_core`
> (agent loop / dispatch / lifecycle / harness / context), `_cli` (slash commands, `hermes` subcommands, skin engine),
> `_gateway_messaging` (gateway transports, MEDIA: attachments, approval buttons), `_mcp_toolsets` (MCP client +
> toolset assembly), `_tools` (the `tools/` package: browser_*, web_tools, computer_use, lsp, tool_search, x_search),
> `_skills` (official skills incl. searxng-search / kanban-worker / macos-computer-use), `_plugins` (non-core plugin
> tools + custom `spawn_fn`), `_providers_adapters` (provider/model adapters incl. xAI Grok + vision + auxiliary),
> `_cron`, `_acp`, `_trajectory_research`, `_tui_gateway`. New Hermes-specific terms owned by SP08b or other SPs that
> do NOT yet exist (`term_browser_automation` [own, captured Phase 1], `term_voice_mode`/`term_text_to_speech`→SP08a,
> `term_messaging_gateway`→SP11, `term_tool_gateway`→SP05, `term_nous_portal`→SP14, `term_kanban_multi_agent`→SP06a,
> `term_progressive_disclosure`→SP05) are ADDITIONAL forward-refs (+fin), EXCLUDED from the ≥8 floor.

**Note 1 `hermes_browser_automation_backends`** (model)
- Terms (8): term_cdp, term_websocket, term_computer_vision, term_multimodal, term_captcha, term_iframe_sandbox, term_autonomous_coding_agents, term_agent_harness — relevance: the model is a CDP/WebSocket-driven tool surface returning accessibility trees + screenshots (vision/multimodal), handling CAPTCHAs, cross-origin iframes, and the agent-harness tool registration. (+fin: term_browser_automation [own])
- Code-Repos (5): repo_hermes_agent_tools — the `tools/` package implements the 12 `browser_*` tools (navigate/snapshot/click/type/cdp/dialog) and the accessibility-tree representation this model documents; repo_hermes_agent_agent_core — the persistent CDP supervisor (one WebSocket per task subscribing to Page/Runtime/Target events) and session isolation/cleanup loop live in the agent-core runtime; repo_hermes_agent_providers_adapters — the `browser_vision` screenshot-analysis path routes through the vision/multimodal model adapter; repo_hermes_agent_mcp_toolsets — the `browser` toolset is registered/enabled through the toolset assembly the model's tool surface plugs into; repo_hermes_agent — the top-level repo defines the multi-backend provider matrix (Browserbase/Browser Use/Firecrawl/Camofox/CDP/agent-browser) this note enumerates.
- Snippets (≥10): snippet_hermes_agent_tools_browser_navigate — the `browser_navigate` session-init code (must precede all other browser tools) this model's tool surface documents; snippet_hermes_agent_tools_browser_dom — the accessibility-tree/`@e` ref-ID snapshot representation (`browser_snapshot`); snippet_hermes_agent_tools_browser_cdp — the raw `browser_cdp` passthrough + cross-origin-iframe `frame_id` routing; snippet_hermes_agent_tools_browser_screenshot — the `browser_vision` screenshot + AI-analysis path; snippet_hermes_agent_tools_browser_session — per-task session isolation + inactivity-timeout cleanup; snippet_hermes_agent_tools_browser_intercept — the `browser_dialog`/`pending_dialogs` native-dialog interception; snippet_hermes_agent_tools_browser_supervisor_lifecycle — the persistent CDP supervisor (one WebSocket per task) that detects dialogs + populates `frame_tree`; snippet_hermes_agent_tools_browser_supervisor_recovery — supervisor recovery/cleanup on disconnect; snippet_hermes_agent_tools_browser_camofox — the Camofox local-backend routing this matrix enumerates; snippet_hermes_agent_tools_registry — the tool-registration path through which the 12 `browser_*` core tools are exposed.
- Docs (≥10): hermes_browser_automation_setup — the per-backend setup procedure sibling for this model; hermes_computer_use_macos — the other agent-driven UI-control surface (browser is the cross-platform alternative cua-driver's Limitations section points to); hermes_web_search_extract — the cheaper non-interactive web alternative the browser intro tip steers users to; hermes_tool_search — the 12 `browser_*` tools are core tools that never defer (contrast); hermes_features_overview — Media & Web feature index linking this note; hermes_vision (SP08a) — the vision toolset `browser_vision` reuses; hermes_browser_supervisor (SP18) — the developer-internal supervisor/dialog plumbing this model summarizes; hermes_mcp (SP09) — the MCP route preferred for WSL2 Windows Chrome; cc_chrome_browser_automation (✓) — Claude Code's analogous Chrome-automation tool (cross-tool reference); cc_chrome_setup_and_troubleshooting (✓) — the analogous CDP-connect/troubleshooting doc; cc_built_in_tools (✓) — the analogous built-in-tool catalog framing.

**Note 2 `hermes_browser_automation_setup`** (procedure)
- Terms (8): term_cdp, term_docker, term_websocket, term_authentication, term_mcp, term_sandbox, term_autonomous_coding_agents, term_agent_harness — relevance: setup configures cloud API auth, Docker-hosted Camofox, CDP/WebSocket attach, MCP-bridge for WSL2 Windows Chrome, and sandboxed local browsing. (+fin: term_browser_automation [own], term_tool_gateway, term_nous_portal)
- Code-Repos (5): repo_hermes_agent_tools — the `tools/browser*` provider-routing code (Camofox env routing, hybrid cloud/private-URL sidecar, agent-browser local mode) this procedure configures; repo_hermes_agent_cli — `/browser connect` / `/browser status` / `/browser disconnect` are CLI slash commands, plus the `hermes setup tools` / `hermes tools` wizards; repo_hermes_agent — top-level repo holds `config.yaml` browser block + `.env` provider keys + `hermes setup --portal`; repo_hermes_agent_mcp_toolsets — the WSL2 `chrome-devtools-mcp` bridge route this page recommends over `/browser connect`; repo_hermes_agent_plugins — provider-dispatch/lazy-install plumbing for the swappable browser backends.
- Snippets (≥10): snippet_hermes_agent_tools_browser_camofox — the Camofox `CAMOFOX_URL`/persistence/externally-managed-session routing this procedure configures; snippet_hermes_agent_plugins_browser_dispatch — the swappable-backend provider dispatch (Browserbase/Browser Use/Firecrawl/Camofox/local) the setup selects; snippet_hermes_agent_tools_lazy_deps — the lazy `agent-browser` / npm dependency install fired by `hermes setup tools → Browser Automation`; snippet_hermes_agent_tools_browser_navigate — the `browser_navigate` entry the hybrid cloud/private-URL auto-router keys on; snippet_hermes_agent_tools_browser_cdp — the `/browser connect` CDP-attach passthrough this page wires; snippet_hermes_agent_tools_browser_session — the per-task session lifecycle the env knobs (timeouts, keep-alive) tune; snippet_hermes_agent_tools_browser_dom — the snapshot path the worked form-fill example drives; snippet_hermes_agent_cli_tools_config — the `hermes tools`/`hermes config set toolsets` wizard that writes the browser provider + `.env`; snippet_hermes_agent_cli_tools_enable — the toolset enable/disable that adds `browser` to the session's toolsets; snippet_hermes_agent_tools_registry — the registration the configured browser backend plugs into.
- Docs (≥10): hermes_browser_automation_backends — the model sibling describing what each backend IS; hermes_web_search_extract — shares the Nous-Portal Tool-Gateway tip + per-provider env-key pattern; hermes_computer_use_macos — its own `hermes computer-use install` upstream-installer setup parallels `agent-browser` install; hermes_tool_search — `browser_*` tools never defer (context note for setup); hermes_features_overview — Media & Web index; hermes_messaging_media_settings (SP02) — owns the `config.yaml` web/browser blocks this links out to; hermes_mcp (SP09) — the WSL2-bridge MCP setup; hermes_nous_portal (SP14) — the `setup --portal` Tool-Gateway browser provider; cc_chrome_browser_automation (✓) — Claude Code's analogous browser-tool setup; cc_chrome_setup_and_troubleshooting (✓) — the analogous CDP-port / user-data-dir launch guide; cc_sandboxed_bash_tool_setup (✓) — analogous local-sandbox setup framing.

**Note 3 `hermes_web_search_extract`** (procedure)
- Terms (8): term_information_retrieval, term_bm25, term_docker, term_authentication, term_context_window, term_progressive_summarization, term_multimodal, term_autonomous_coding_agents — relevance: `web_search` is ranked IR over 8 backends; `web_extract` summarizes long pages via an auxiliary model (progressive-summarization) to fit the context window; SearXNG self-hosts via Docker with API-key auth. (+fin: term_messaging_gateway, term_tool_gateway, term_nous_portal)
- Code-Repos (5): repo_hermes_agent_tools — `tools/web_tools.py` implements `web_search`/`web_extract` backend selection (the very module the Verify section runs: `python -m tools.web_tools`); repo_hermes_agent_providers_adapters — the `auxiliary.web_extract` model resolver and the xAI-Grok server-side `web_search` path live in the provider/adapter layer; repo_hermes_agent — top-level repo owns the `web:` config block (search_backend/extract_backend/auto-detect priority) + `.env` provider keys; repo_hermes_agent_skills — the optional `searxng-search` official skill (`hermes skills install official/research/searxng-search`); repo_hermes_agent_cli — the `hermes tools` Web-Search wizard + `hermes setup` backend-detection output.
- Snippets (≥10): snippet_hermes_agent_tools_web_tools — the `tools/web_tools.py` `web_search`/`web_extract` 8-backend selection + the `python -m tools.web_tools` verify entry this page documents; snippet_hermes_agent_plugins_web — the per-provider web backend dispatch (Firecrawl/SearXNG/DDGS/Brave/Tavily/Exa/Parallel/xAI); snippet_hermes_agent_cli_web_config_schema — the `web:` config schema (`search_backend`/`extract_backend`/`backend`/per-capability split) this Configuration section sets; snippet_hermes_agent_plugins_provider_xai_oauth — the xAI credential path used by the xAI `web_search` backend; snippet_hermes_agent_core_auxiliary_auth_resolution — the `auxiliary.web_extract` model resolver (`provider: auto` → main chat model) driving the size-tier summarization; snippet_hermes_agent_tools_lazy_deps — the lazy `pip install ddgs` install for the DDGS backend on first use; snippet_hermes_agent_tools_registry — the registration making `web_search`/`web_extract` core (never-defer) tools; snippet_hermes_agent_skills_research_arxiv — an official research skill that consumes `web_search`/`web_extract`; snippet_hermes_agent_skills_research_polymarket — another research skill built on the web tools; snippet_hermes_agent_cli_tools_config — the `hermes tools → Web Search & Extract` wizard that writes the provider URL/key.
- Docs (≥10): hermes_x_search_grok — the X-specific sibling that reuses the same xAI Grok credential + Responses-API path; hermes_browser_automation_setup — the browser fallback for raw unsummarized content the "When summarization gets in the way" section points to; hermes_browser_automation_backends — `web_search`/`web_extract` are the cheaper alternative to the browser tool surface; hermes_tool_search — `web_search`/`web_extract` are core tools that never defer; hermes_features_overview — Media & Web index; hermes_messaging_media_settings (SP02) — owns the `config.yaml` web blocks + auxiliary-model reference; hermes_nous_portal (SP14) — managed Firecrawl via the Tool Gateway; hermes_xai_grok_oauth (SP15) — the xAI OAuth login the xAI backend uses; cc_built_in_tools (✓) — Claude Code's analogous WebSearch/WebFetch built-in tools; cc_web_overview (✓) — the analogous web-tooling overview; cc_reduce_token_usage (✓) — the analogous long-content-summarization / token-reduction framing for `web_extract`'s size tiers.

**Note 4 `hermes_x_search_grok`** (procedure)
- Terms (8): term_oauth_token, term_authentication, term_information_retrieval, term_function_calling, term_structured_output, term_rate_limiting, term_failover, term_autonomous_coding_agents — relevance: `x_search` gates on an OAuth/API-key credential resolver, runs Grok's server-side search tool (function-calling) returning structured JSON, with retries/backoff on 5xx and a 401 token-refresh failover. (+fin: term_provider_routing)
- Code-Repos (5): repo_hermes_agent_providers_adapters — the xAI credential resolver (SuperGrok OAuth vs `XAI_API_KEY`), the 401 forced-token-refresh, and the Grok Responses-API call live in the provider/adapter layer; repo_hermes_agent_tools — `x_search` is a registered tool whose `check_fn` gating + client-side date validation + `degraded` result shape are in the `tools/` package; repo_hermes_agent — top-level repo owns the `x_search:` config block (model/timeout/retries) and `.env` `XAI_API_KEY`; repo_hermes_agent_cli — `hermes auth add xai-oauth` / `hermes auth status` / `hermes tools` toggle drive the OAuth-callback login; repo_hermes_agent_mcp_toolsets — the Search toolset registration the tool list rebuild re-runs `check_fn` against.
- Snippets (≥10): snippet_hermes_agent_plugins_provider_xai_oauth — the SuperGrok-OAuth-vs-`XAI_API_KEY` resolver + 401 forced-token-refresh `x_search` gates on; snippet_hermes_agent_core_auxiliary_auth_resolution — the shared xAI bearer resolution the `check_fn` calls; snippet_hermes_agent_tools_web_tools — the sibling tool that runs Grok's `web_search` over the same Responses API; snippet_hermes_agent_plugins_web — the xAI web backend dispatch parallel to `x_search`; snippet_hermes_agent_tools_registry — the registration whose tool-list rebuild re-runs `x_search`'s `check_fn`; snippet_hermes_agent_model_tools_introspection — the tool-schema rebuild that hides `x_search` when the credential resolver returns False; snippet_hermes_agent_core_tool_result_classification — the structured `degraded`/`error` result-shape classification `x_search` returns; snippet_hermes_agent_cli_auth_oauth_callback_server — the `accounts.x.ai` OAuth-callback login server `hermes auth add xai-oauth` runs; snippet_hermes_agent_cli_auth_resolve_provider — the `hermes auth status` provider-credential resolution; snippet_hermes_agent_core_codex_responses_adapter_request — the Responses-API request path the server-side `x_search` tool call rides.
- Docs (≥10): hermes_web_search_extract — the general-web sibling; "use this instead of web_search when you want X discussion"; hermes_browser_automation_backends — alternate retrieval surface; hermes_tool_search — the tool list rebuild that triggers `check_fn` (deferral context); hermes_features_overview — Media & Web / Integrations index; hermes_xai_grok_oauth (SP15) — the OAuth setup guide this page's Authentication section links out to; hermes_provider_routing (SP10) — provider selection that picks the xAI Grok model; hermes_fallback_providers (SP10) — the failover-on-error pattern paralleling x_search's retry/backoff; hermes_tts (SP08a) — the same xAI key is also used for TTS/inference (the "bill against the same key" tip); cc_built_in_tools (✓) — Claude Code's analogous built-in web/search tools; cc_web_overview (✓) — analogous web-tool overview (cross-tool reference); cc_authentication (✓) — analogous credential/OAuth resolution framing.

**Note 5 `hermes_computer_use_macos`** (procedure)
- Terms (8): term_mcp, term_computer_vision, term_multimodal, term_human_in_the_loop, term_prompt_injection, term_context_window, term_function_calling, term_autonomous_coding_agents — relevance: `computer_use` speaks MCP/stdio to cua-driver, uses a vision model (multimodal SOM capture), requires human-in-the-loop approval for destructive actions, defends against screenshot-embedded prompt injection, and applies 4-layer screenshot-token optimization to protect the context window. (+fin: term_browser_automation [own])
- Code-Repos (5): repo_hermes_agent_tools — the `computer_use` toolset (capture/click/type/key actions, SOM vs ax modes, the four screenshot-token optimizations) lives in the `tools/` package; repo_hermes_agent_mcp_toolsets — `computer_use` speaks MCP over stdio to the external `cua-driver` process, so the MCP-client/toolset layer is the transport; repo_hermes_agent_providers_adapters — the per-provider screenshot encoding (OpenAI `image_url` vs Anthropic native `tool_result` image blocks, the `clear_tool_uses` context-editing) is adapter-layer code; repo_hermes_agent_cli — `hermes computer-use install` / `status` / `--upgrade` subcommands run the upstream installer; repo_hermes_agent_skills — the universal `macos-computer-use` skill the See-also references.
- Snippets (≥10): snippet_hermes_agent_tools_computer_use_cua_backend — the MCP/stdio `cua-driver` backend (SkyLight SPIs, background event posting) this page's "How it works" documents; snippet_hermes_agent_tools_computer_use_tool — the `computer_use` capture/click/type/key/drag action dispatch; snippet_hermes_agent_tools_computer_use_schema — the SOM-vs-`ax` capture-mode + element-index tool schema; snippet_hermes_agent_tools_browser_screenshot — the screenshot-capture/analysis path the SOM capture reuses; snippet_hermes_agent_tools_vision_dispatch — the vision-model routing the screenshot analysis goes through; snippet_hermes_agent_tools_vision_input — the multimodal image-input encoding (inline `image_url` parts) per provider; snippet_hermes_agent_tools_approval_policy — the destructive-action approval gating (click/type/drag/key/focus_app); snippet_hermes_agent_tools_approval_ui — the CLI dialog + messaging-platform approval-button surface; snippet_hermes_agent_core_tool_guardrails_schema — the hard-blocked key-combo / type-pattern guardrails (`sudo rm -rf /`, lock screen, etc.); snippet_hermes_agent_skills_apple_macos — the macOS Apple-skill layer the `macos-computer-use` skill sits in.
- Docs (≥10): hermes_browser_automation_backends — the cross-platform GUI alternative the Limitations section names; hermes_browser_automation_setup — parallel install procedure (`agent-browser` vs `cua-driver`); hermes_vision (SP08a) — the vision toolset the SOM screenshot analysis reuses; hermes_tool_search — `computer_use` is a non-core toolset eligible for deferral context; hermes_features_overview — Automation/Media index; hermes_messaging_media_settings (SP02) — the `approvals.mode: manual` config + messaging-platform approval buttons; hermes_hooks (SP06b) — the guardrail/approval interception layer; cc_computer_use (✓) — Claude Code's analogous computer-use tool (cross-tool reference); cc_computer_use_safety (✓) — the analogous computer-use safety/guardrail doc; cc_prompt_injection_defenses (✓) — the analogous screenshot/embedded-instruction prompt-injection defenses.

**Note 6 `hermes_lsp_diagnostics`** (model)
- Terms (8): term_ast, term_function_calling, term_idempotency, term_caching, term_autonomous_coding_agents, term_agent_harness, term_structured_output, term_information_retrieval — relevance: the model layers an in-process AST syntax check before semantic LSP diagnostics, surfaces only NEW (baseline-diffed) structured diagnostics into the write/patch tool result the harness consumes, lazy-spawns + caches long-lived servers. (+fin: term_context_engineering)
- Code-Repos (5): repo_hermes_agent_tools — `write_file`/`patch` and the post-write lint check (AST syntax channel + `lsp_diagnostics` channel) are in the `tools/` package; the LSP manager (lazy spawn, baseline diff, broken-set, per-server registry) is the implementation this model documents; repo_hermes_agent_agent_core — the git-workspace gating + long-lived server lifecycle (kept alive for the process life, no idle reaper) is runtime-level; repo_hermes_agent — top-level repo owns the `lsp:` config block + `<HERMES_HOME>/lsp/bin` install staging; repo_hermes_agent_cli — `hermes lsp status/list/install/restart/which` subcommands; repo_hermes_agent_mcp_toolsets — language-server subprocesses are spawned/managed analogously to MCP stdio servers in the toolset/process layer.
- Snippets (≥10): snippet_hermes_agent_lsp_manager_dispatch — the LSP manager that captures baseline diagnostics, re-queries the server, and baseline-diffs to surface only NEW diagnostics this model documents; snippet_hermes_agent_lsp_manager_lifecycle — the lazy-spawn / long-lived-server / broken-set lifecycle (no idle reaper); snippet_hermes_agent_lsp_servers_config — the per-server `lsp.servers.*` overrides (disabled/command/env/initialization_options); snippet_hermes_agent_lsp_servers_install — the `<HERMES_HOME>/lsp/bin` auto-install staging (npm/go install) this page's Installation-locations section describes; snippet_hermes_agent_lsp_servers_registry — the ~25-language-server registry the Supported-languages table mirrors; snippet_hermes_agent_tools_patch_parser — the `patch` tool whose post-write check feeds the diagnostics; snippet_hermes_agent_tools_file_tools — the `write_file` tool whose result carries the `lint` + `lsp_diagnostics` fields; snippet_hermes_agent_tools_file_operations_a — the file-edit operations the layered syntax→LSP check runs after; snippet_hermes_agent_core_tool_result_classification — the structured tool-result shape (`lint`/`lsp_diagnostics` fields) the agent consumes; snippet_hermes_agent_tools_registry — the registration of the write/patch tools the LSP check hooks into.
- Docs (≥10): hermes_features_overview — Core feature index (file editing + diagnostics); hermes_browser_automation_backends — another tool-result-shaping model in this series; hermes_tool_search — both are model-BB notes describing tool-result/registry mechanics; hermes_kanban_worker_lanes — another model-BB note (peer cross-link); hermes_skins_themes — sibling in this sub-plan; hermes_tools (SP05) — `write_file`/`patch` tool reference this links out to; hermes_messaging_media_settings (SP02) — `HERMES_HOME` / config block; hermes_browser_supervisor (SP18) — the tools-runtime internals doc; cc_built_in_tools (✓) — Claude Code's analogous Edit/Write tools that surface lint results; cc_file_tool_behavior (✓) — the analogous file-edit tool behavior/diagnostics doc; cc_verification_loop (✓) — the analogous post-edit verification/diagnostics loop.

**Note 7 `hermes_skins_themes`** (procedure)
- Terms (8): term_persona, term_agent_harness, term_autonomous_coding_agents, term_self_evolving_agent, term_session_persistence, term_context_window, term_idempotency, term_multi_agent_systems — relevance: skins are the visual layer (contrast with `term_persona` conversational style); applied per-CLI-session by the harness; per-profile precedence ties into session/profile isolation. (+fin: term_progressive_disclosure)
- Code-Repos (5): repo_hermes_agent_cli — `hermes_cli/skin_engine.py` loads the 9 built-in skins, applies `/skin`, renders the banner/spinner/branding, and falls back to `default` — the core implementation of this page; repo_hermes_agent — top-level repo owns the `display.skin` config key + `~/.hermes/skins/` user-skin directory; repo_hermes_agent_tui_gateway — the TUI status/usage bar + completion-menu surfaces the color keys (`status_bar_bg`, `completion_menu_*`) drive; repo_hermes_agent_gateway_messaging — `voice_status_bg` and gateway display surfaces consume the skin's color keys; repo_hermes_agent_agent_core — `/skin` is a CLI slash command resolved by the agent-core command dispatcher.
- Snippets (≥10): snippet_hermes_agent_cli_skin_engine — `hermes_cli/skin_engine.py`: loads the 9 built-in skins, the configurable-key surface, and the `default` fallback this page documents; snippet_hermes_agent_cli_skin_apply — the `/skin` session-only apply + `display.skin` permanent-default precedence; snippet_hermes_agent_cli_banner_update — the banner/`banner_logo`/`banner_hero` rendering the branding keys drive; snippet_hermes_agent_gw_display_config — the gateway display config surfaces consuming the skin's color keys (`voice_status_bg`, status bar); snippet_hermes_agent_cli_tools_config — the config writer that persists `display.skin`; snippet_hermes_agent_tools_registry — the tool-prefix/`tool_emojis` per-tool spinner overrides resolved against the registry; snippet_hermes_agent_core_run_agent_cli — the CLI run loop that initializes the active skin per session; snippet_hermes_agent_cli_kanban_commands — a CLI surface that renders under the active skin's color keys; snippet_hermes_agent_toolset_distributions — the per-platform toolset surface the banner's Available-Tools section enumerates; snippet_hermes_agent_gw_runtime_footer — the gateway runtime footer that also renders skin-driven labels/colors.
- Docs (≥10): hermes_features_overview — Customization feature index; hermes_browser_automation_backends — sibling in this sub-plan; hermes_tool_search — sibling model note (CLI-surface context); hermes_kanban_worker_lanes — sibling in this sub-plan; hermes_lsp_diagnostics — sibling in this sub-plan; hermes_personality (SP05) — the conversational-style `SOUL.md`/`/personality` layer skins are explicitly contrasted with; hermes_profiles (SP04) — per-profile precedence / `HERMES_HOME` the skin engine respects; hermes_messaging_media_settings (SP02) — the TUI status-bar config this links out to; cc_terminal_themes (✓) — Claude Code's analogous terminal theme system (cross-tool reference); cc_terminal_configuration (✓) — the analogous terminal-appearance config; cc_statusline_setup (✓) — the analogous CLI status-line / branding customization; cc_output_styles (✓) — the analogous output-style customization layer.

**Note 8 `hermes_tool_search`** (model)
- Terms (8): term_bm25, term_context_window, term_mcp, term_information_retrieval, term_prompt_caching, term_function_calling, term_caching, term_autonomous_coding_agents — relevance: the model defers MCP/plugin tool schemas (saving context window), exposing 3 bridge tools (function-calling) backed by BM25 retrieval; trades prompt-cache integrity + a round trip for schema savings. (+fin: term_progressive_disclosure)
- Code-Repos (5): repo_hermes_agent_tools — `tools/tool_search.py` (the file the page's See-also names) implements the 3 bridge tools + BM25 retrieval + literal-substring fallback + stateless catalog rebuild; repo_hermes_agent_mcp_toolsets — only MCP + non-core plugin tools are deferral-eligible, so the toolset/MCP-client assembly is what computes the deferrable slice and the 10%-context threshold; repo_hermes_agent_plugins — non-core plugin tools are the other deferral-eligible source; repo_hermes_agent_agent_core — the tools-array assembly (re-evaluated every turn), pre/post-tool-call hooks + guardrails that run against the unwrapped real tool name, are runtime-level; repo_hermes_agent — top-level repo owns the `tools.tool_search` config block (`enabled`/`threshold_pct`/limits).
- Snippets (≥10): snippet_hermes_agent_tools_registry — the tools-array assembly that defines `_HERMES_CORE_TOOLS` (never-defer) and computes the deferrable slice this model gates on; snippet_hermes_agent_tools_schema_sanitizer — the per-tool schema sizing that decides whether deferrable schemas exceed the ~10% threshold; snippet_hermes_agent_model_tools_introspection — the model-visible tool-list rebuild that swaps deferred tools for the 3 bridge tools; snippet_hermes_agent_model_tools_capability_probe — the capability probe over the tool catalog (name/description/params) BM25 indexes; snippet_hermes_agent_core_tool_dispatch_helpers — the unwrap that dispatches `tool_call` to the real underlying tool (hooks/guardrails run on the real name); snippet_hermes_agent_tools_mcp_client — the MCP client whose tools are the primary deferral source; snippet_hermes_agent_tools_mcp_call — the MCP tool invocation the unwrapped `tool_call` ultimately drives; snippet_hermes_agent_cli_tools_config — the `tools.tool_search` (`enabled`/`threshold_pct`/limits) config; snippet_hermes_agent_cli_tools_enable — the per-session toolset enable/disable that bounds the deferrable catalog; snippet_hermes_agent_core_tool_result_classification — the structured bridge-tool result shape (`tool_search`/`tool_describe`/`tool_call` returns).
- Docs (≥10): hermes_features_overview — Core feature index; hermes_browser_automation_backends — core `browser_*` tools that never defer (the `_HERMES_CORE_TOOLS` contrast); hermes_web_search_extract — `web_search`/`web_extract` are also never-defer core tools; hermes_lsp_diagnostics — peer model note; hermes_kanban_worker_lanes — a kanban worker's session-scoped toolset slice limits the deferred catalog; hermes_mcp (SP09) — MCP servers are the primary deferral source this page targets; hermes_tools (SP05) — toolset definition / `_HERMES_CORE_TOOLS` reference; hermes_hooks (SP06b) — the hooks/guardrails that run on the unwrapped tool name; cc_mcp_tool_search (✓) — Claude Code's analogous MCP tool-search/deferral feature (cross-tool reference); cc_mcp_overview (✓) — the analogous MCP-integration overview; cc_reduce_token_usage (✓) — the analogous context-window / token-savings framing.

**Note 9 `hermes_features_overview`** (navigation)
- Terms (8): term_autonomous_coding_agents, term_agent_harness, term_mcp, term_subagent, term_skills, term_skill_manifest, term_multi_agent_systems, term_agentic_ai — relevance: the page indexes the whole feature set (tools/skills/memory/automation/integrations/customization) — each track's core concept term. (+fin: term_messaging_gateway, term_tool_gateway, term_nous_portal)
- Code-Repos (5): repo_hermes_agent — the top-level repo whose feature surface this overview indexes (the `hermes setup --portal` one-command entry); repo_hermes_agent_tools — the Tools & Toolsets / web-search / browser / code-execution features the Core+Media tracks link; repo_hermes_agent_skills — the Skills System track; repo_hermes_agent_mcp_toolsets — the MCP Integration track under Integrations; repo_hermes_agent_agent_core — the Subagent Delegation / memory / context-files automation tracks (delegate_task, MEMORY.md) live in agent-core.
- Snippets (≥10): snippet_hermes_agent_toolsets_definitions — the toolset definitions enumerated across the Core/Media/Integrations tracks this page indexes; snippet_hermes_agent_toolsets_materialize — the per-platform toolset materialization (enable/disable per gateway) the overview describes; snippet_hermes_agent_tools_registry — the master tool registry the feature surface is built from; snippet_hermes_agent_cli_tools_config — the `hermes tools` / `hermes setup --portal` config entry the intro tip names; snippet_hermes_agent_tools_skill_manager — the Skills-System track implementation; snippet_hermes_agent_tools_memory — the Persistent-Memory (`MEMORY.md`/`USER.md`) Core track; snippet_hermes_agent_tools_delegate_spawn — the Subagent-Delegation (`delegate_task`) Automation track; snippet_hermes_agent_tools_send_dispatch — the messaging/`send_message` surface the Media&Web + Integrations tracks span; snippet_hermes_agent_plugins_web — the Media&Web Web-Search feature backend; snippet_hermes_agent_tools_web_tools — the `web_search`/`web_extract` Media&Web entry the overview links.
- Docs (≥10): hermes_browser_automation_backends — the Media&Web Browser entry; hermes_web_search_extract — the Media&Web Web-Search entry; hermes_computer_use_macos — the Automation entry; hermes_tool_search — the progressive-disclosure tool layer; hermes_kanban_worker_lanes — the Automation/multi-agent entry; hermes_skins_themes — the Customization Skins entry; hermes_lsp_diagnostics — the Core file-editing diagnostics entry; hermes_learning_path (SP01) — the companion navigation note (router-by-experience vs index-by-feature); hermes_mcp (SP09) — the Integrations MCP entry it links; hermes_personality (SP05) — the Customization Personality entry; cc_overview (✓) — Claude Code's analogous product-feature overview (cross-tool nav reference); cc_feature_selection_guide (✓) — the analogous feature-selection guide.

**Note 10 `hermes_kanban_worker_lanes`** (model)
- Terms (8): term_kanban, term_subagent, term_multi_agent_systems, term_agent_orchestration, term_orchestration, term_heartbeat, term_idempotency, term_autonomous_coding_agents — relevance: a worker lane is a kanban-dispatched subagent (multi-agent orchestration) with a claim/heartbeat/terminator lifecycle; the dispatcher reaps dead PIDs and extends live claims (idempotent run-id gating). (+fin: term_kanban_multi_agent)
- Code-Repos (5): repo_hermes_agent_agent_core — the kanban dispatcher (`dispatch_once`, `_default_spawn`, claim TTL / `detect_crashed_workers` / stale-claim extension / stranded detection) and the `kanban_*` terminator tools live in the agent-core runtime; repo_hermes_agent_skills — the `kanban-worker` and `kanban-orchestrator` devops skills that encode the worker/orchestrator side of this contract; repo_hermes_agent_cli — `hermes -p <assignee> chat`, `hermes kanban show/tail/runs/diagnostics`, `hermes profile list` drive lane spawn + audit; repo_hermes_agent_plugins — non-Hermes external-CLI lanes register their own `spawn_fn` via a plugin (the not-yet-paved path); repo_hermes_agent — top-level repo owns the per-board SQLite (`task_runs`/`task_events`), `HERMES_KANBAN_*` env contract, and `kanban.stranded_threshold_seconds` config.
- Snippets (≥10): snippet_hermes_agent_tools_kanban_register — the lane registration / `spawn_fn` plumbing the dispatcher matches `task.assignee` against; snippet_hermes_agent_tools_kanban_mutate — the `kanban_complete`/`kanban_block`/`kanban_comment` terminator + annotation tools the review-required convention uses; snippet_hermes_agent_tools_kanban_query — the `kanban_show`/`kanban_create`/`kanban_link` query+decompose tools; snippet_hermes_agent_cli_kanban_crud — the `hermes kanban` board/task CRUD; snippet_hermes_agent_cli_kanban_query — the `hermes kanban show/runs` query surfacing `task_runs`/`task_events`; snippet_hermes_agent_cli_kanban_diagnostics — the `hermes kanban diagnostics` stranded-task detection this page's Failure-modes section describes; snippet_hermes_agent_cli_kanban_commands — `hermes kanban tail`/lane spawn + audit CLI; snippet_hermes_agent_cli_kanban_schema — the per-board SQLite (`task_runs`/`task_events`) schema the audit trail rides; snippet_hermes_agent_skills_devops_kanban_worker — the `kanban-worker` skill encoding the worker side of this contract; snippet_hermes_agent_skills_devops_kanban_orchestrator — the `kanban-orchestrator` skill encoding the orchestrator-lane shape.
- Docs (≥10): hermes_features_overview — the Automation feature index; hermes_tool_search — a kanban worker's session-scoped toolset slice limits its deferred catalog (peer model); hermes_lsp_diagnostics — peer model-BB note; hermes_browser_automation_backends — peer model-BB note; hermes_skins_themes — sibling in this sub-plan; hermes_kanban (SP06b) — the user-facing kanban intro this contract sits beneath; hermes_kanban_tutorial (SP06b) — the dashboard walkthrough; hermes_delegation (SP06a) — `delegate_task` subagent spawning the worker-lane model generalizes; hermes_profiles (SP04) — the profile lane = profile-name assignee; cc_orchestrate_agent_teams (✓) — Claude Code's analogous multi-agent orchestration (cross-tool reference); cc_dispatch_background_agents (✓) — the analogous background-agent dispatch/lifecycle; cc_run_agents_in_parallel (✓) — the analogous parallel-worker model.

All 10 notes meet the **FOUR-FLOOR standard: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**. Term IDs are under
`resources/term_dictionary/`, code-repo IDs under `areas/code_repos/`, snippet IDs under `resources/code_snippets/`
resolve in `resources/documentation/hermes_agent/` at finalization (G5/G8); the `cc_*` docs are existing
**One placeholder term slug was caught at the 2026-06-15 finalization (`term_subprocess` — DOES NOT exist) and

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 9 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 browser-backends | model | 2000 | ≤6 (curate from 33 src blocks; one canonical tool/backend block, tables in prose) | ✓ |
| 2 browser-setup | procedure | 1600 | ≤6 (curate per-backend YAML/env from 33 src blocks) | ✓ |
| 3 web-search-extract | procedure | 1600 | ≤6 (curate from 29 src blocks; keep canonical per-backend + size-tier table in prose) | ✓ |
| 4 x-search-grok | procedure | 1000 | 2 | ✓ |
| 5 computer-use-macos | procedure | 1000 | 4 | ✓ |
| 6 lsp-diagnostics | model | 1300 | ≤6 (from 5; supported-language table in prose) | ✓ |
| 7 skins-themes | procedure | 1300 | 6 (template + minimal + change-skin blocks; key tables in prose) | ✓ |
| 8 tool-search | model | 1000 | 4 | ✓ |
| 9 features-overview | navigation | 700 | 0 | ✓ |
| 10 kanban-worker-lanes | model | 1300 | ≤6 (from 1 src block + env table in prose) | ✓ |

No further splits needed beyond the planned browser→2. All 10 notes ≤2500w. Code-heavy pages
(browser 33, web-search 29) are curated to ≤6 load-bearing blocks each (kept verbatim), the rest
summarized in prose / rendered as tables. If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_chrome_browser_automation.md`
and `cc_computer_use.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** —
floor raised 2026-06-19; snippets are a COUNTED floor [≥10], not a bonus; prior floor was ≥8 term + ≥8 snippet + ≥5 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP08b)

**SP08b owns 1 new term capture: `term_browser_automation`.** Per the master's corpus-wide ownership
sweep, every other Hermes-specific concept SP08b touches is owned by another sub-plan (link at
finalization) or is an existing verified term. Augment re-read surfaced **0 additional new** undigested
terms that SP08b should own — the LSP / tool-search / computer-use / kanban-lane / skins concepts are each
captured as a doc note (model/procedure BB), and their component concepts are existing verified terms.

| Term | DF | Decision | Capture Phase | Stub/Full | Best-fit glossary | Note |
|------|---:|----------|---------------|-----------|-------------------|------|
| `term_browser_automation` | 13 | **CAPTURE (owned)** — Hermes browser tool/modes (≠ `term_code_browser`) | **Phase 1** (BEFORE Notes 1/2) | full (moderate, ~10 Related Terms) | `acronym_glossary_tools` | NEW; via `/tessellum-capture-term-note browser_automation`. Master caution confirmed: `browser tool` ≠ `term_code_browser` (read at audit — code_browser is generic code-navigation, 73L). |
| `term_voice_mode`, `term_text_to_speech`, `term_speech_to_text` | — | LINK only (+fin) | — | — | — | SP08a owns (media split a); referenced in `overview.md` Media & Web. |
| `term_messaging_gateway` | — | LINK only (+fin) | — | — | — | SP11 owns; `browser_vision` MEDIA: attachment + overview Integrations reference it. |
| `term_tool_gateway`, `term_progressive_disclosure`, `term_skills_hub` | — | LINK only (+fin) | — | — | — | SP05 owns; Nous-Portal Tool Gateway tip (browser/web-search) + tool-search progressive disclosure + overview Skills. |
| `term_nous_portal` | — | LINK only (+fin) | — | — | — | SP14 owns; `setup --portal` tip on browser/web-search/overview. |
| `term_kanban_multi_agent`, `term_persistent_goal` | — | LINK only (+fin) | — | — | — | SP06a owns; worker-lanes extends multi-agent kanban. |

### Renamed (general → specific)

`term_browser` → **`term_browser_automation`** — bare `term_browser` is a too-general one-word noun (collides
with the generic browser concept / `term_code_browser`); `term_browser_automation` scope-qualifies it to the
Hermes browser-automation tool surface. Recorded per Step 10.5f specificity heuristic (one-word common noun
without domain qualifier → add qualifier).

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_code_browser` (would be wrong target for browser-automation) | `term_code_browser.md` (73L, active, concept — generic code navigation) | Not captured / not linked — confirmed LIKE false-positive; the NEW `term_browser_automation` is the correct distinct capture. |
| `term_chrome_devtools_protocol` (would duplicate) | `term_cdp.md` (active) | Not captured — LINK the existing `term_cdp` from the browser notes. |
| `term_kanban_worker_lane` (would duplicate concept) | `term_kanban.md` (active) | Not captured — the worker-lane CONTRACT is a doc MODEL note (`hermes_kanban_worker_lanes`); LINK `term_kanban` + (+fin) SP06a `term_kanban_multi_agent`. |

Specificity + collision audit performed for the owned slug AND all 10 doc notes (term_dictionary AND
documentation/ searched); 1 owned capture, 1 rename, 3 would-be slugs removed (link existing instead).

## Term-Note Authoring Requirements (SP08b — Inherited from `/tessellum-capture-term-note` canonical)

`term_browser_automation` MUST be authored via **`/tessellum-capture-term-note browser_automation`**
(NOT inline-authored in a doc note), in **Phase 1, BEFORE Notes 1/2** (so the doc notes can link it via +fin).
The capture skill enforces (verbatim from the canonical):

- **YAML**: `tags` (resource, terminology, tools, agentic_ai), `keywords` (Browser Automation, browser tool,
  CDP, accessibility tree, headless browser), `topics`, `language: markdown`, `date of note`, `status: active`,
  `building_block: concept`, `access_control_group: ["general"]`, `related_wiki` (null or the Hermes docs URL).
  No forbidden fields (`title`/`category`/`created`/`updated`/`source`/`parent`/`author`/`note_second_category`).
- **H1 `# Browser Automation`** → `## Definition` (what it is: agentic browser control via accessibility-tree
  snapshots + ref IDs across cloud/local CDP backends; the problem it solves) → `## Context` (Hermes Agent,
  other autonomous coding agents) → `## Key Characteristics` (multi-backend, accessibility-tree-not-pixels,
  CDP passthrough, session isolation, stealth) → `## Related Terms` (**≥8-10 indexed links**, in-domain +
  cross-domain: `term_cdp`, `term_code_browser` [contrast — generic code-navigation, NOT this], `term_computer_vision`,
  `term_captcha`, `term_websocket`, `term_iframe_sandbox`, `term_autonomous_coding_agents`, `term_agent_harness`,
  `term_multimodal`, `term_mcp`) → `## References` (external URLs ONLY — Hermes browser docs, Browserbase, CDP
  protocol; NO `term_*.md` here).
  Wikipedia "browser automation") for definition orthogonality; cross-reference vault via `/tessellum-search-notes`.
- **MathJax** for any notation (N/A expected). **Fleeting-content guard** (strip product-version specifics).
- **Glossary**: append a 4-5-sentence entry to `acronym_glossary_tools.md` per the exact
  `**Full Name** / **Description** / **Documentation** / **Wiki** / **Related**` template; bold the single
  most distinguishing fact; no metrics.
- **Backlink expansion** (Step 6e): add `term_browser_automation` to the `## Related Terms` of in/cross-domain
  existing terms (`term_cdp`, `term_computer_vision`, `term_autonomous_coding_agents`, `term_agent_harness`),
  target 5-10 inlinks. Convert ≥1 plain-text mention in a non-term note to a link (Step 6a-6d).
- **Depth-scaled Related Terms minimum**: moderate (80-150 lines) → **10 links**. If >200 lines, decompose
  per Step 7. Section ordering: Related Terms before References; footer last.
- **Acceptance**: single-source (only the Hermes doc) → FAIL; <10 Related Terms → FAIL; no cross-domain
  diversity → FAIL; `building_block != concept` → FAIL; substantive note overwritten → FAIL (none exists).

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (owned term capture + browser pilot, P2 features):** capture `term_browser_automation` via
  `/tessellum-capture-term-note browser_automation` FIRST; then pilot Note 1 (`hermes_browser_automation_backends`)
  → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (browser setup + web tools):** Notes 2, 3, 4. GATE G1–G8.
- **Phase 3 (tool surface + nav):** Notes 5, 6, 7, 8, 9, 10. GATE G1–G8.
- **Phase 3b (inlinks — EXECUTED, G8):** add the inlinks in the Inlinks table; verify every new note
  in-degree ≥1 from outside the folder.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_browser_automation_backends hermes_browser_automation_setup hermes_web_search_extract hermes_x_search_grok hermes_computer_use_macos hermes_lsp_diagnostics hermes_skins_themes hermes_tool_search hermes_features_overview hermes_kanban_worker_lanes; do
```

## Entry Point Decision (inherited)

Contributes 10 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Web & Tool Surface" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP08b does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_tools.md` | → `hermes_browser_automation_backends`, `hermes_web_search_extract`, `hermes_computer_use_macos`, `hermes_lsp_diagnostics`, `hermes_tool_search` | tools repo ↔ tool-surface docs |
| `repo_hermes_agent.md` | → `hermes_browser_automation_setup`, `hermes_features_overview` | implementation ↔ browser setup + feature index |
| `repo_hermes_agent_cli.md` | → `hermes_skins_themes` | CLI repo ↔ skins/themes (CLI visual layer) |
| `repo_hermes_agent_mcp_toolsets.md` | → `hermes_tool_search`, `hermes_computer_use_macos` | MCP/toolsets repo ↔ tool-search deferral + cua-driver MCP |
| `repo_hermes_agent_agent_core.md` | → `hermes_kanban_worker_lanes` | agent core (dispatch/lifecycle) ↔ worker-lane contract |
| `term_cdp.md` | → `hermes_browser_automation_backends`, `hermes_browser_automation_setup` | concept term → the browser-automation docs that use CDP |
| `term_kanban.md` | → `hermes_kanban_worker_lanes` | concept term → worker-lane contract model |
| `term_code_browser.md` | (NO inlink — unrelated generic code-navigation concept) | confirmed false-positive; do NOT link |
| `term_browser_automation.md` (new, Phase 1) | → `hermes_browser_automation_backends`, `hermes_browser_automation_setup`, `hermes_computer_use_macos` | new concept term → its documenting doc notes |
| `entry_code_snippets_hermes_agent.md` | → `hermes_browser_automation_backends`, `hermes_tool_search` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 10 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Capture `term_browser_automation` FIRST, then pilot Note 1 (`hermes_browser_automation_backends`) → reindex
→ verify format/ghost/in-degree BEFORE authoring the rest. Commit per phase (per-wave commits for multi-agent
runs). Re-read the source page before writing each note — do NOT work from memory. Code blocks verbatim for
kept blocks; curate code-heavy notes (browser 33, web-search 29) to ≤6 load-bearing blocks, summarize the
rest in prose / tables. If a note exceeds 350 lines during writing, STOP and split. If multi-agent: agents
return note content, master writes serially where there is write-contention; ≤30 agents/run; embed the
manifest in the workflow script.

## Follow-up Recommendations

- After SP08b lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 10 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P2 wave: cross-link `hermes_features_overview` ↔ `hermes_learning_path` (SP01) and the per-feature
  doc notes across SP05/06/08a/09/10 once those land (the overview is the in-features nav hub).
- Cross-link `hermes_kanban_worker_lanes` ↔ SP06b `hermes_kanban*` (user intro/tutorial) bidirectionally
  once SP06b lands.
- Consider one `thought_` note comparing Hermes' docs-stated browser/tool-search design vs the
  code-digestion findings in `snippet_hermes_agent_tools_browser_*` / `snippet_hermes_agent_tools_registry`.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (1 LIKE false-positive `term_code_browser` confirmed by
  reading the note; cc_* analogues confirmed DIFFERENT product → cross-tool link not dup), finalized
  Per-Note Mapping (now the **FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**, all term/repo/snippet/cc_* IDs
  (for the 1 owned capture), Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  3-floor (snippets-as-bonus) wording; the snippet group is now a COUNTED floor raised to ≥10. Re-read all 9 owned
  source pages from the c253b07 mirror to ground the new code-repo + snippet + doc relevance clauses; each note's
  Code-Repos line names the implementing module among the 13 `repo_hermes_agent_*` source-code notes, each
  active 2026-06-19), and the Docs line expands to ≥10 (in-series `hermes_*` siblings [resolve at finalization] +
  density breach on re-read.
- Density re-read: counts match measured; **no additional splits** beyond the planned browser→2.
  All 10 notes ≤2500w; code-heavy notes (browser/web-search) curated to ≤6 blocks.
- Collision audit: **0 removals of doc notes**; **1 owned term capture** (`term_browser_automation`),
  1 rename (`term_browser`→`term_browser_automation`), 3 would-be slugs removed (link `term_cdp`/`term_kanban`
  /reject `term_code_browser`).
- Term placeholder catch: **1 non-existent term slug caught at finalization** (`term_subprocess` in Note 6)
- Undigested terms surfaced at augment: **1 owned** (`term_browser_automation`); 0 additional.
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (FOUR-FLOOR
Inlinks (all 10) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (Phase 1, browser_automation) ✓ best-fit glossary (acronym_glossary_tools — verified exists) ✓
Term-Note Auth Reqs (for the owned capture) ✓ invokes capture-term-note (`/tessellum-capture-term-note browser_automation`) ✓
Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (term_browser→term_browser_automation) ✓
Slug Collision (term_code_browser LIKE false-positive + term_subprocess placeholder caught) ✓ dedup generalized
to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓
Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15; re-reviewed 2026-06-19 (FOUR-FLOOR verification) — READY FOR EXECUTION (9/9 checkpoints pass).**

> **2026-06-19 re-review (four-floor + Docs-floor focus).** All 10 planned notes independently re-counted:
> every note carries **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** (min observed per group across the 10
> notes: term 8, code-repo 5, snippet 10, doc 10 — Note 5 sits exactly at the ≥10 doc floor, the rest 11–12).
> The Docs floor is MET for every note (the audit-flagged short Docs lines were already topped up in the
> ID found; no content fix required. **RESULT: 9/9 → READY.**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases + 3b inlinks, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (10 rows under a Web & Tool Surface section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 10 notes ≤30 (part b of SP08 split); master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_chrome_browser_automation.md`/`cc_computer_use.md`); not invented. |
| CP6 | Borderline density → split | PASS | browser.md→2 (model+procedure, >2500w + >6 code); all notes ≤2500w; code-heavy notes curated ≤6; the 4 model + 5 procedure + 1 nav notes are cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15: browser 4121, web-search 2102, x-search 1153, computer-use 1088, lsp 1392, skins 1642, tool-search 1044, overview 921, kanban-worker-lanes 1447 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP08b owns 1 capture (`term_browser_automation`, Phase 1, full); best-fit glossary `acronym_glossary_tools` verified; Term-Note Authoring Requirements present (YAML, H1/H2, multi-source mandate, MathJax, depth-scaled 10 Related Terms, backlink expansion, glossary template). |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 10 doc notes + the owned slug (term_dictionary AND documentation/); `term_code_browser` LIKE false-positive confirmed by reading (73L generic code-navigation); `term_browser`→`term_browser_automation` rename; 3 would-be slugs removed; cc_* analogues confirmed cross-tool (different product) not dups; 1 placeholder term (`term_subprocess`) caught + replaced inline. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 10 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |


## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-synced from upstream `NousResearch/hermes-agent`
`website/docs/` — moving the pin from **95715dc → c253b07** on **2026-06-19** (now byte-identical to
upstream `main` HEAD). All 9 of this sub-plan's owned pages were independently re-measured against the
fresh mirror (measurement convention: body-only word count after stripping YAML frontmatter; code-block
count = count of lines matching `^\s*```` divided by 2). **Word/code counts are UNCHANGED** — every number
still matches the Source Pages table exactly (ratio 1.00):

- `user-guide/features/browser.md` — 4121w / 33code (unchanged)
- `user-guide/features/web-search.md` — 2102w / 29code (unchanged)
- `user-guide/features/x-search.md` — 1153w / 2code (unchanged)
- `user-guide/features/computer-use.md` — 1088w / 4code (unchanged)
- `user-guide/features/lsp.md` — 1392w / 5code (unchanged)
- `user-guide/features/skins.md` — 1642w / 6code (unchanged)
- `user-guide/features/tool-search.md` — 1044w / 4code (unchanged)
- `user-guide/features/overview.md` — 921w / 0code (unchanged)
- `user-guide/features/kanban-worker-lanes.md` — 1447w / 1code (unchanged)

Because no source count moved, **no planned-note, split, or density decision is affected**:
the browser→2 split, all per-note ~Words targets, and the ≤2500w/≤6-code/≤400-line density caps all stand as
written. The cross-ref floor was subsequently **set 2026-06-19** to the **FOUR-FLOOR standard: ≥8 term / ≥5 code-repo /
≥10 snippet / ≥10 doc** (all counted; supersedes the original ≥8 term / ≥8 snippet / ≥5 doc and the interim 3-floor
snippets-as-bonus wording) — see the Per-Note Related Notes Mapping and the Augmentation Report. **Plan remains READY.**

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented 2026-06-19 — cross-ref floor set to the FOUR-FLOOR standard ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc, all counted) · Review: **DONE** (2026-06-15, 9/9 READY) · Execute: pending · Re-synced 2026-06-19 (counts unchanged)

**Source**: `inbox/hermes_agent_docs/user-guide/features/{browser,web-search,x-search,computer-use,lsp,skins,tool-search,overview,kanban-worker-lanes}.md`
**Last Updated**: 2026-06-15 (re-verified 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
