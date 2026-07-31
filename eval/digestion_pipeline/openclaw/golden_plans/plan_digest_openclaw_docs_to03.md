---
title: Sub-Plan to03 — OpenClaw Docs: Tools (Search Providers, Exec & Exec Approvals)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["tools/duckduckgo-search", "tools/elevated", "tools/exa-search", "tools/exec", "tools/exec-approvals", "tools/exec-approvals-advanced", "tools/firecrawl"]
---

<!-- status set ready 2026-06-21 by /tessellum-review-digestion-plan (9/9 CP PASS); see Review Sign-Off -->


# Sub-Plan to03: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview` … `## Related Notes` … `## References`, ≤400L/≤2500w/≤6 code, one BB/note), dedup-before-create (term_dictionary AND documentation/ AND `repo_openclaw*`), the 9-GATE table, cross-references, and entry-point wiring are INHERITED from the master.

## Scope

The seven `tools/` pages in this batch cover two operational clusters: (1) **web-research tool providers** — DuckDuckGo (key-free, experimental HTML search), Exa (neural/keyword/hybrid search + content extraction), and Firecrawl (search, scrape, and `web_fetch` fallback with bot-circumvention); and (2) the **shell-execution surface and its safety interlocks** — the `exec` tool itself, the `elevated` sandbox-escape mode, and the two-page exec-approvals system (policy knobs, allowlists, YOLO mode, safe-bins, interpreter binding, and approval-forwarding to chat channels).

**Priority: P2 (Phase B — features/integration).** The exec/approvals/elevated trio is the most operationally important content here (it is OpenClaw's host-command security model and the FZ 15 integration's sandbox-escape surface); the three search providers are configuration-reference pages. The code-side counterparts (`repo_openclaw_security`, `repo_openclaw_extensions`, `repo_openclaw_extensions_llm_providers`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **10,325 measured words.** **Planned: 10 notes** (4 single-note pages + 3 split pages).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| DuckDuckGo search | `tools/duckduckgo-search` | 366 | 3 | 5 | 0 | procedure |
| Elevated mode | `tools/elevated` | 606 | 3 | 6 | 0 | procedure |
| Exa search | `tools/exa-search` | 612 | 4 | 7 | 2 | procedure |
| Exec tool | `tools/exec` | 2,275 | 9 | 9 | 1 | procedure (split: usage vs config/policy) |
| Exec approvals | `tools/exec-approvals` | 2,760 | 7 | 14 | 11 | procedure (split: policy/storage vs YOLO/allowlist/flow) |
| Exec approvals — advanced | `tools/exec-approvals-advanced` | 2,995 | 6 | 4 | 11 | procedure (split: safe-bins vs approval-forwarding) |
| Firecrawl | `tools/firecrawl` | 711 | 3 | 8 | 3 | procedure |

(Code counts = raw ``` fences ÷ 2. The `# otherwise` on line 82 of `exec-approvals.md` is a comment INSIDE a fenced block, not a real H1; the single real H1 per file is the YAML `title`.)

## Content Strategy

- **Prioritize**: the exec authorization model and the approvals policy surface (`tools.exec.mode`/`security`/`ask`/`askFallback`, allowlist + `argPattern`, safe-bins, YOLO mode, denied-approval/fail-closed behavior). This is the host-command security boundary the rest of the tool ecosystem (and FZ 15 sandbox-escape analysis) depends on; reproduce config snippets verbatim.
- **Split**: `exec.md` (2,275w / 9 code) → usage+parameters vs config+policy+apply_patch (code-cap and BB-cluster driven); `exec-approvals.md` (2,760w / 14 H2 / 11 H3) → policy-knobs+storage vs operations (YOLO/allowlist/flow/events); `exec-approvals-advanced.md` (2,995w / 11 H3) → safe-bins+interpreter-binding vs approval-forwarding+native-delivery. See Split Decisions.
- **Keep 1 note each**: the three search-provider pages (each ≤711w, ≤4 code, single config-procedure BB) and `elevated.md` (606w, cohesive sandbox-escape procedure).
- **Link-out, do NOT redefine**: sandboxing internals → `gateway/sandboxing` (gw05, planned) + `cc_sandbox_*` docs; permission-mode taxonomy → `tools/permission-modes` (to06, planned); the generic `web`/`web-fetch` overview + sibling search providers (Brave/Tavily/Perplexity/etc.) → their own Tools sub-plans (to01/to07/to08, planned); plugin-permission-request internals → `plugins/plugin-permission-requests` (pl04, planned). Channel-native approval delivery references (`channels/slack`, `channels/telegram`, …) link to the Channels series (ch01–06, planned), not duplicated.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_duckduckgo_search.md` | procedure | duckduckgo-search.md: Setup, Config, Tool parameters, Notes | 350 | Configuring DuckDuckGo as a key-free `web_search` provider: `openclaw configure --section web`, `tools.web.search.provider`, plugin region/SafeSearch config, per-query `query`/`count`/`region`/`safeSearch` params, and the experimental HTML-scraping / bot-challenge caveats. |
| 2 | `oc_tools_elevated.md` | procedure | elevated.md: Directives, How it works, Resolution order, Availability and allowlists, What elevated does not control | 550 | Elevated mode — letting a sandboxed agent break out and run `exec` on the host: `/elevated on/ask/full/off` directives, the inline/session/global resolution order, the `tools.elevated.enabled` + per-channel `allowFrom` gating, and what elevated does NOT override (tool policy, host selection, the separate `!`/`/bash` gate). |
| 3 | `oc_tools_exa_search.md` | procedure | exa-search.md: Install plugin, Get an API key, Config, Base URL override, Tool parameters, Content extraction, Search modes, Notes | 550 | Configuring Exa AI as a `web_search` provider: plugin install, `EXA_API_KEY`, `plugins.entries.exa` config + base-URL override, the `type`/`freshness`/`date_*` params, the six search modes, and `contents` content-extraction (text/highlights/summary). |
| 4 | `oc_tools_exec_usage.md` | procedure | exec.md: intro, Parameters, Notes (host routing), Session overrides (`/exec`), Authorization model, Examples | 600 | The `exec` tool's invocation surface: parameters (`command`/`workdir`/`env`/`yieldMs`/`background`/`timeout`/`pty`/`host`/`ask`/`node`/`elevated`), `host=auto` routing rules, `/exec` per-session overrides + the authorized-sender authorization model, and foreground/background/send-keys `process` examples. |
| 5 | `oc_tools_exec_config.md` | procedure | exec.md: Config, PATH handling, Allowlist + safe bins (pointer), apply_patch | 600 | `tools.exec.*` configuration: timeout/notify/host/security/ask knobs, `strictInlineEval`, `pathPrepend` + per-host PATH handling and PATH/loader-override rejection, the safe-bins controls (pointer to to03 advanced), and the `apply_patch` subtool (OpenAI/Codex-only, `workspaceOnly`, policy interaction). |
| 6 | `oc_tools_exec_approvals_policy.md` | procedure | exec-approvals.md: intro, Inspecting the effective policy, Where it applies (Trust model, macOS split), Settings and storage, Policy knobs (mode/security/ask/askFallback/strictInlineEval/commandHighlighting) | 650 | The host exec-approvals policy model: stricter-of-config-vs-host-file resolution, `openclaw approvals`/`exec-policy` inspection commands, gateway-vs-node enforcement + trust model + macOS IPC split, the `exec-approvals.json` storage schema, and the `tools.exec.mode`/`security`/`ask`/`askFallback`/`strictInlineEval`/`commandHighlighting` knobs. |
| 7 | `oc_tools_exec_approvals_operations.md` | procedure | exec-approvals.md: YOLO mode (+ presets/node/session shortcuts), Allowlist (per agent, argPattern, entry fields), Auto-allow skill CLIs, Control UI editing, Approval flow, System events, Denied approval behavior, Implications | 650 | Operating exec approvals: YOLO no-approval setup (both policy layers + `exec-policy preset yolo`), per-agent allowlists with `argPattern` + entry schema, auto-allow skill CLIs, Control-UI editing, the request→resolve→forward approval flow with canonical `systemRunPlan` binding, `Exec running/finished` system events, and fail-closed denied-approval behavior. |
| 8 | `oc_tools_exec_approvals_safe_bins.md` | procedure | exec-approvals-advanced.md: intro, Safe bins (stdin-only) (Argv validation/denied flags, Trusted binary directories, Shell chaining/wrappers/multiplexers, Safe bins vs allowlist), Interpreter/runtime commands (Followup delivery behavior) | 650 | The advanced safe-bin fast-path: `safeBins` stdin-only defaults + custom `safeBinProfiles`, deterministic argv validation / denied flags / literal-token rules, `safeBinTrustedDirs`, shell-chaining/wrapper/multiplexer unwrapping, safe-bins-vs-allowlist comparison, and conservative interpreter/runtime file-binding (deny-on-ambiguity) with async-followup delivery. |
| 9 | `oc_tools_exec_approvals_forwarding.md` | procedure | exec-approvals-advanced.md: Approval forwarding to chat channels (Plugin approval forwarding, Same-chat approvals, Native approval delivery, macOS IPC flow), FAQ | 650 | Forwarding exec/plugin approval prompts to chat channels: `approvals.exec`/`approvals.plugin` config (mode/agentFilter/sessionFilter/targets), `/approve` decisions, same-chat approval on any deliverable channel, native approval clients per channel (`channels.<ch>.execApprovals`), the macOS IPC flow, and the `accountId`/`threadId` + session-authorization FAQ. |
| 10 | `oc_tools_firecrawl.md` | procedure | firecrawl.md: intro (three modes), Install plugin, Keyless web_fetch and API keys, Configure Firecrawl search, Configure web_fetch fallback (Self-hosted), Firecrawl plugin tools (firecrawl_search/firecrawl_scrape), Stealth/bot circumvention, How web_fetch uses Firecrawl | 650 | Firecrawl in OpenClaw three ways — `web_search` provider, explicit `firecrawl_search`/`firecrawl_scrape` tools, and keyless `web_fetch` fallback: plugin install, `FIRECRAWL_API_KEY`, search + fetch config (self-hosted private-only base-URL rule), proxy/stealth bot-circumvention, and the `web_fetch` extraction order (Readability → Firecrawl → basic cleanup). |

## Section Coverage Map

Every source H2/H3 maps to exactly one planned note; no orphans.

```
duckduckgo-search.md
├── (intro: key-free web_search provider) ────────────── → note 1 (oc_tools_duckduckgo_search)
├── Setup ────────────────────────────────────────────── → note 1
├── Config ───────────────────────────────────────────── → note 1
├── Tool parameters ──────────────────────────────────── → note 1
└── Notes ────────────────────────────────────────────── → note 1
elevated.md
├── (intro: sandbox break-out) ───────────────────────── → note 2 (oc_tools_elevated)
├── Directives ───────────────────────────────────────── → note 2
├── How it works ─────────────────────────────────────── → note 2
├── Resolution order ─────────────────────────────────── → note 2
├── Availability and allowlists ──────────────────────── → note 2
└── What elevated does not control ───────────────────── → note 2
exa-search.md
├── (intro: neural/keyword/hybrid + extraction) ──────── → note 3 (oc_tools_exa_search)
├── Install plugin ───────────────────────────────────── → note 3
├── Get an API key ───────────────────────────────────── → note 3
├── Config ───────────────────────────────────────────── → note 3
├── Base URL override ────────────────────────────────── → note 3
├── Tool parameters ──────────────────────────────────── → note 3
│   ├── ### Content extraction ───────────────────────── → note 3
│   └── ### Search modes ─────────────────────────────── → note 3
└── Notes ────────────────────────────────────────────── → note 3
exec.md
├── (intro: mutating shell surface, process) ─────────── → note 4 (oc_tools_exec_usage)
├── Parameters ───────────────────────────────────────── → note 4
├── Notes (host routing / SHELL / PATH rejection) ────── → note 4
├── Session overrides (`/exec`) ──────────────────────── → note 4
├── Authorization model ──────────────────────────────── → note 4
├── Exec approvals (companion app / node host) (pointer) → note 4 (→ notes 6–7)
├── Examples ─────────────────────────────────────────── → note 4
├── Config ───────────────────────────────────────────── → note 5 (oc_tools_exec_config)
│   └── ### PATH handling ────────────────────────────── → note 5
├── Allowlist + safe bins (pointer) ──────────────────── → note 5 (→ note 8)
└── apply_patch ──────────────────────────────────────── → note 5
exec-approvals.md
├── (intro: companion-app/node-host guardrail) ───────── → note 6 (oc_tools_exec_approvals_policy)
├── Inspecting the effective policy ──────────────────── → note 6
├── Where it applies ─────────────────────────────────── → note 6
│   ├── ### Trust model ──────────────────────────────── → note 6
│   └── ### macOS split ──────────────────────────────── → note 6
├── Settings and storage ─────────────────────────────── → note 6
├── Policy knobs ─────────────────────────────────────── → note 6
│   ├── ### tools.exec.mode ──────────────────────────── → note 6
│   ├── ### exec.security ────────────────────────────── → note 6
│   ├── ### exec.ask ─────────────────────────────────── → note 6
│   ├── ### askFallback ──────────────────────────────── → note 6
│   ├── ### tools.exec.strictInlineEval ──────────────── → note 6
│   └── ### tools.exec.commandHighlighting ───────────── → note 6
├── YOLO mode (no-approval) ──────────────────────────── → note 7 (oc_tools_exec_approvals_operations)
│   ├── ### Persistent gateway-host "never prompt" setup → note 7
│   ├── ### Local shortcut ───────────────────────────── → note 7
│   ├── ### Node host ────────────────────────────────── → note 7
│   └── ### Session-only shortcut ────────────────────── → note 7
├── Allowlist (per agent) ────────────────────────────── → note 7
│   └── ### Restricting arguments with argPattern ────── → note 7
├── Auto-allow skill CLIs ────────────────────────────── → note 7
├── Safe bins and approval forwarding (pointer) ──────── → note 7 (→ notes 8–9)
├── Control UI editing ───────────────────────────────── → note 7
├── Approval flow ────────────────────────────────────── → note 7
├── System events ────────────────────────────────────── → note 7
├── Denied approval behavior ─────────────────────────── → note 7
└── Implications ─────────────────────────────────────── → note 7
exec-approvals-advanced.md
├── (intro) ──────────────────────────────────────────── → note 8 (oc_tools_exec_approvals_safe_bins)
├── Safe bins (stdin-only) ───────────────────────────── → note 8
│   ├── ### Argv validation and denied flags ─────────── → note 8
│   ├── ### Trusted binary directories ───────────────── → note 8
│   ├── ### Shell chaining, wrappers, and multiplexers ─ → note 8
│   └── ### Safe bins versus allowlist ───────────────── → note 8
├── Interpreter/runtime commands ─────────────────────── → note 8
│   └── ### Followup delivery behavior ───────────────── → note 8
├── Approval forwarding to chat channels ─────────────── → note 9 (oc_tools_exec_approvals_forwarding)
│   ├── ### Plugin approval forwarding ───────────────── → note 9
│   ├── ### Same-chat approvals on any channel ───────── → note 9
│   ├── ### Native approval delivery ─────────────────── → note 9
│   └── ### macOS IPC flow ───────────────────────────── → note 9
└── FAQ (accountId/threadId; session-approval auth) ──── → note 9
firecrawl.md
├── (intro: three modes) ─────────────────────────────── → note 10 (oc_tools_firecrawl)
├── Install plugin ───────────────────────────────────── → note 10
├── Keyless web_fetch and API keys ───────────────────── → note 10
├── Configure Firecrawl search ───────────────────────── → note 10
├── Configure Firecrawl web_fetch fallback ───────────── → note 10
│   └── ### Self-hosted Firecrawl ────────────────────── → note 10
├── Firecrawl plugin tools ───────────────────────────── → note 10
│   ├── ### firecrawl_search ─────────────────────────── → note 10
│   └── ### firecrawl_scrape ─────────────────────────── → note 10
├── Stealth / bot circumvention ──────────────────────── → note 10
└── How `web_fetch` uses Firecrawl ───────────────────── → note 10
```

Pointer-only sections (`exec.md` → Exec approvals; `exec.md` → Allowlist+safe-bins; `exec-approvals.md` → Safe bins and approval forwarding) are cross-links to notes 6–9, not separately digested. Sandboxing internals, `permission-modes`, generic `web`/`web-fetch`, sibling search providers, and `plugins/plugin-permission-requests` are linked-out to their own sub-plans (gw05/to06/to01/to07/to08/pl04), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| exec.md (2,275w, 9 code, 9 H2 / 1 H3) | notes 4 (`oc_tools_exec_usage`) + 5 (`oc_tools_exec_config`) | Raw code-fence count (9) exceeds the ≤6 cap, and the page mixes a tool-invocation procedure (params, `/exec`, authorization, examples) with a configuration procedure (`tools.exec.*`, PATH handling, apply_patch). Split by task cluster keeps each note ≤6 code blocks and ≤700w. |
| exec-approvals.md (2,760w, 7 code, 14 H2 / 11 H3) | notes 6 (`oc_tools_exec_approvals_policy`) + 7 (`oc_tools_exec_approvals_operations`) | Exceeds the 2,500w cap. Split at the policy/operations seam: declarative policy model + storage + knobs (note 6) vs operating workflows — YOLO setup, allowlists, approval flow, events, denied behavior (note 7). Each ≤650w, ≤4 code. |
| exec-approvals-advanced.md (2,995w, 6 code, 4 H2 / 11 H3) | notes 8 (`oc_tools_exec_approvals_safe_bins`) + 9 (`oc_tools_exec_approvals_forwarding`) | Exceeds the 2,500w cap. Split at the two independent topic blocks: safe-bins fast-path + interpreter binding (note 8) vs approval-forwarding to chat channels + native delivery + IPC + FAQ (note 9). Each ≤650w, ≤4 code. |

The four remaining pages stay 1 note each (all ≤711w, ≤4 code, single config-procedure BB).

## Summary Statistics & Building Block Distribution

- Source pages: **7** (10,325 measured words). New `oc_` notes: **10**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×10** (all 10 notes). These are tool-configuration / authorization / approval-operations procedures; no concept/model/argument note in this batch (the security-design *argument* is carried by linked `repo_openclaw_security` + `term_threat_model`, not re-argued here).
- Est. digest words ≈ 5,900 (avg ~590/note). 35 source code fences distribute across the 10 procedure notes; each note kept ≤6 (config snippets reproduced selectively, verbatim).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_tools_duckduckgo_search (8t · 10s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: DuckDuckGo is configured as one of OpenClaw's `web_search` providers.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: agent web search supplies external context for grounding, the RAG retrieval step.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — query→ranked-results discipline; relevance: a `web_search` provider IS an IR backend (`query`/`count`/`region`).
- [Bot Detection](../../term_dictionary/term_bot_detection.md) — automated-traffic identification; relevance: the page's core caveat is DuckDuckGo serving bot-challenge pages under automated use.
- [CAPTCHA](../../term_dictionary/term_captcha.md) — human-verification challenge; relevance: the docs warn DuckDuckGo may serve CAPTCHAs to block scraped requests.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI/data services an agent calls; relevance: DuckDuckGo is an external service reached via HTML scraping, not an official API.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: `web_search` is exposed to the model as a callable tool with typed params.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: DuckDuckGo blocks under heavy/automated use, an effective rate limit on the key-free provider.

**Docs** (11; 6 existing)
- [Claude Code: Web Overview](../claude_code/cc_web_overview.md) — CC web search/fetch tooling; relevance: closest precedent for an agent web-search provider surface.
- [Claude Code: Web Security and Limits](../claude_code/cc_web_security_and_limits.md) — CC web tool guardrails/limits; relevance: parallels DuckDuckGo's experimental-breakage and bot-block caveats.
- [Claude Code: Web Quickstart](../claude_code/cc_web_quickstart.md) — enabling CC web tools; relevance: analogue to `openclaw configure --section web` provider selection.
- [Claude Code: Advisor Tool](../claude_code/cc_advisor_tool.md) — an external-information tool wired into the agent; relevance: comparison for tool-as-external-information-source design.
- [Claude Code: Built-In Tools](../claude_code/cc_built_in_tools.md) — CC's tool catalog incl. web search; relevance: positions web_search within an agent's built-in tool set.
- [Claude Code: Tools Catalog](../claude_code/cc_tools_catalog.md) — full CC tool inventory; relevance: where a web-search provider sits among agent tools.
- [oc_tools_exa_search](oc_tools_exa_search.md) (planned, this series) — Exa provider; relevance: sibling API-backed `web_search` provider contrasted with key-free DuckDuckGo.
- [oc_tools_firecrawl](oc_tools_firecrawl.md) (planned, this series) — Firecrawl provider; relevance: sibling provider with bot-circumvention, the recommended upgrade from scraped DuckDuckGo.
- [oc_tools_web](oc_tools_web.md) (planned, to08) — web search overview / auto-detection; relevance: parent page listing all providers and selection rules.
- [oc_tools_brave_search](oc_tools_brave_search.md) (planned, to01) — Brave provider; relevance: the docs explicitly recommend Brave (free tier) over experimental DuckDuckGo.
- [oc_tools_perplexity_search](oc_tools_perplexity_search.md) (planned, to06) — Perplexity provider; relevance: another API-backed sibling in the provider family.

**Repos** (2)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw codebase; relevance: the `web_search` provider dispatch lives here.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension layer; relevance: DuckDuckGo is delivered as a search-provider plugin.

**Snippets** (10)
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregation pattern; relevance: shows how OpenClaw selects/routes among external providers like search backends.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content handling/guard; relevance: scraped web results are untrusted external content, the bot-challenge risk surface.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web search/fetch tool impl; relevance: parallel coding-agent web_search/web_fetch tool definitions.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: how a web-search tool is registered/exposed to the model.
- [snippet_hermes_agent_tools_schema_sanitizer](../../code_snippets/snippet_hermes_agent_tools_schema_sanitizer.md) — tool-param schema sanitizing; relevance: the typed `query`/`count`/`region`/`safeSearch` param schema.
- [snippet_hermes_agent_skills_research_arxiv](../../code_snippets/snippet_hermes_agent_skills_research_arxiv.md) — research/search skill; relevance: a concrete agent search-for-retrieval workflow.
- [snippet_slipbot_bm25_search](../../code_snippets/snippet_slipbot_bm25_search.md) — BM25 search backend; relevance: keyword IR engine analogous to a keyword `web_search` provider.
- [snippet_slipbox_dense_search](../../code_snippets/snippet_slipbox_dense_search.md) — dense/semantic search; relevance: neural-search counterpart contrasting DuckDuckGo's plain keyword HTML scrape.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — browser navigation tool; relevance: alternative to HTML scraping for JS-rendered search pages.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry/config; relevance: provider-selection plumbing mirroring `tools.web.search.provider`.

**Entry Points**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1) · [entry_claude_code_docs](../../../0_entry_points/entry_claude_code_docs.md)

### oc_tools_elevated (8t · 10s · 10d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: elevated mode is an OpenClaw exec directive.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: elevated mode lets a sandboxed agent break OUT of the sandbox onto the host.
- [Access Control](../../term_dictionary/term_access_control.md) — who-may-do-what gating; relevance: elevated is gated by `enabled` + per-channel `allowFrom` sender allowlists.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints on agent actions; relevance: elevated keeps approval gates in `on`/`ask` and only `full` skips them.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human approval in the loop; relevance: `/elevated on` retains approvals so a human still gates host commands.
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/attack-surface analysis; relevance: sandbox break-out is the core attack surface the gating defends.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: elevated changes how the `exec` tool call routes/executes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving dev agents; relevance: elevated controls how much host access such an agent gets.

**Docs** (10; 6 existing)
- [Claude Code: Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — how sandbox and permission gates compose; relevance: direct analogue to OpenClaw's sandbox-vs-tool-policy-vs-elevated composition.
- [Claude Code: Permission Modes Overview](../claude_code/cc_permission_modes_overview.md) — agent permission modes; relevance: `/elevated on/ask/full/off` is OpenClaw's permission-mode dial.
- [Claude Code: Execution Environments](../claude_code/cc_execution_environments.md) — where commands run; relevance: elevated chooses host vs sandbox execution target.
- [Claude Code: Desktop Permission Modes](../claude_code/cc_desktop_permission_modes.md) — interactive permission switching; relevance: parallels the per-session `/elevated` directive UX.
- [Claude Code: Sandbox Modes](../claude_code/cc_sandbox_modes.md) — sandbox on/off/levels; relevance: elevated only matters when the agent is sandboxed.
- [Claude Code: Security Architecture](../claude_code/cc_security_architecture.md) — layered security model; relevance: break-glass elevation as a controlled exception in a layered model.
- [oc_tools_exec_usage](oc_tools_exec_usage.md) (planned, this series) — the exec tool; relevance: elevated modifies the `exec` tool's host routing and the `elevated` param.
- [oc_tools_exec_approvals_policy](oc_tools_exec_approvals_policy.md) (planned, this series) — approvals policy; relevance: elevated stacks on top of (and in `full` skips) exec approvals.
- [oc_gateway_sandboxing](oc_gateway_sandboxing.md) (planned, gw05) — gateway sandbox config; relevance: defines the sandbox elevated breaks out of.
- [oc_gateway_sandbox_vs_tool_policy_vs_elevated](oc_gateway_sandbox_vs_tool_policy_vs_elevated.md) (planned, gw05) — three-gate composition; relevance: the canonical page on what elevated does/doesn't override.

**Repos** (3)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/sandbox/exec code; relevance: implements the elevated gating + sandbox escape path.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: per-agent `tools.elevated.enabled`/`allowFrom` restriction.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session state; relevance: `/elevated` sets a per-session level via the resolution order.

**Snippets** (10)
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem policy; relevance: governs what host filesystem an elevated exec can mutate.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime security audit; relevance: audits the host-exec surface elevated unlocks.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool policy; relevance: elevated cannot override `exec` denied by tool policy.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — per-channel sender allowlist; relevance: the `allowFrom` per-channel sender allowlist gating elevated.
- [snippet_hermes_agent_core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — shell-command allowlist hook; relevance: pre-shell gating parallel to elevated's break-out checks.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denial; relevance: the tool-policy deny that elevated can't override.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: routes the elevated exec onto the configured host path.


### oc_tools_exa_search (8t · 10s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: Exa is configured as an OpenClaw `web_search` provider plugin.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: Exa's `contents` text/summary extraction directly feeds RAG context.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — query→ranked-results; relevance: Exa is a neural/keyword/hybrid IR backend.
- [Dense Retrieval](../../term_dictionary/term_dense_retrieval.md) — embedding-based semantic search; relevance: Exa's `neural` mode is dense/semantic retrieval.
- [Caching](../../term_dictionary/term_caching.md) — result reuse; relevance: Exa results cache 15 min and the endpoint is part of the cache key.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: `baseUrl` routes Exa requests through a compatible proxy/alternate endpoint.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI service; relevance: Exa is an external API integration requiring `EXA_API_KEY`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: `web_search` with Exa's typed params (`type`/`freshness`/`contents`) is a tool call.

**Docs** (11; 6 existing)
- [Claude Code: Web Overview](../claude_code/cc_web_overview.md) — CC web tooling; relevance: precedent for an agent web-search provider with content extraction.
- [Claude Code: Web Security and Limits](../claude_code/cc_web_security_and_limits.md) — web tool limits; relevance: parallels Exa's result-count/freshness limits.
- [Claude Code: Advisor Tool](../claude_code/cc_advisor_tool.md) — external-info tool; relevance: comparison for content-extraction-as-tool design.
- [Claude Code: Web Quickstart](../claude_code/cc_web_quickstart.md) — enabling web tools; relevance: analogue to plugin install + key setup for Exa.
- [Claude Code: Web Session Management](../claude_code/cc_web_session_management.md) — web-session lifecycle; relevance: comparison for stateful web tool config.
- [Claude Code: Built-In Tools](../claude_code/cc_built_in_tools.md) — tool catalog; relevance: positions Exa search among agent tools.
- [oc_tools_duckduckgo_search](oc_tools_duckduckgo_search.md) (planned, this series) — key-free provider; relevance: sibling contrasted with Exa's API-backed neural search.
- [oc_tools_firecrawl](oc_tools_firecrawl.md) (planned, this series) — Firecrawl provider; relevance: sibling search+extraction provider.
- [oc_tools_web](oc_tools_web.md) (planned, to08) — provider overview; relevance: parent page listing Exa among providers.
- [oc_tools_perplexity_search](oc_tools_perplexity_search.md) (planned, to06) — Perplexity provider; relevance: another semantic/structured search sibling.
- [oc_tools_brave_search](oc_tools_brave_search.md) (planned, to01) — Brave provider; relevance: keyword-filtered search sibling in the provider family.

**Repos** (3)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw codebase; relevance: search-provider dispatch + cache-key resolution.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin layer; relevance: Exa ships as `@openclaw/exa-plugin`.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider-plugin layer; relevance: Exa is a provider-style extension with key/base-URL config.

**Snippets** (10)
- [snippet_slipbox_dense_search](../../code_snippets/snippet_slipbox_dense_search.md) — dense/semantic search; relevance: concrete neural-search analogue of Exa's `neural` mode.
- [snippet_slipbot_bm25_search](../../code_snippets/snippet_slipbot_bm25_search.md) — BM25 keyword search; relevance: keyword-mode analogue (`fast`) contrasted with neural.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web search/fetch tools; relevance: parallel web_search tool with content extraction.
- [snippet_hermes_agent_tools_schema_sanitizer](../../code_snippets/snippet_hermes_agent_tools_schema_sanitizer.md) — param-schema handling; relevance: Exa's rich typed param schema (`type`/`contents`/`freshness`).
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: how the Exa-backed web_search tool is registered.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry/config; relevance: provider-selection + key plumbing like `plugins.entries.exa`.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregation; relevance: base-URL override / proxy routing pattern mirrors Exa `baseUrl`.
- [snippet_hermes_agent_skills_research_arxiv](../../code_snippets/snippet_hermes_agent_skills_research_arxiv.md) — research/search skill; relevance: neural-search-for-retrieval workflow feeding the agent.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embedding generation; relevance: embedding machinery underlying neural/dense search.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent memory search; relevance: in-agent semantic retrieval comparable to Exa neural results.

**Entry Points**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1) · [entry_claude_code_docs](../../../0_entry_points/entry_claude_code_docs.md)

### oc_tools_exec_usage (9t · 12s · 11d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: `exec` is OpenClaw's core mutating shell tool.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: `exec` is invoked as a tool with typed params (`command`/`host`/`pty`/`background`).
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: `host=auto` resolves to sandbox when a sandbox runtime is active.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving dev agents; relevance: `exec` is the shell surface those agents act through.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime wrapping an agent; relevance: exec's host routing + `process` background sessions are harness-level concerns.
- [Access Control](../../term_dictionary/term_access_control.md) — gating; relevance: `/exec` is honored only for authorized senders with access groups.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agents; relevance: background `process` sessions are scoped per agent (subagents don't see each other's).
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client wire protocol; relevance: node host exec rides ACP/RPC paths to a paired node.
- [Cron](../../term_dictionary/term_cron.md) — scheduled job execution; relevance: docs direct long-running/scheduled work to cron instead of exec sleep/timeout polling loops.

**Docs** (11; 6 existing)
- [Claude Code: Built-In Tools](../claude_code/cc_built_in_tools.md) — CC tool catalog incl. Bash; relevance: closest analogue to OpenClaw's `exec` tool.
- [Claude Code: Execution Tool Behavior](../claude_code/cc_execution_tool_behavior.md) — Bash/exec tool semantics; relevance: direct counterpart to exec params + foreground/background behavior.
- [Claude Code: Execution Environments](../claude_code/cc_execution_environments.md) — where commands run; relevance: `host=auto/sandbox/gateway/node` routing.
- [Claude Code: File Tool Behavior](../claude_code/cc_file_tool_behavior.md) — write/edit tool semantics; relevance: docs note disabling write/edit does NOT make exec read-only.
- [Claude Code: SDK Tool Execution](../claude_code/cc_agent_sdk_tool_execution.md) — programmatic tool execution; relevance: how an exec-style tool runs in an agent loop.
- [Claude Code: Sandboxed Bash Tool Setup](../claude_code/cc_sandboxed_bash_tool_setup.md) — sandboxed shell; relevance: the sandbox-vs-gateway routing exec resolves.
- [oc_tools_exec_config](oc_tools_exec_config.md) (planned, this series) — `tools.exec.*` config; relevance: split sibling holding exec's configuration knobs.
- [oc_tools_elevated](oc_tools_elevated.md) (planned, this series) — elevated mode; relevance: the `elevated` param + sandbox break-out path.
- [oc_tools_exec_approvals_policy](oc_tools_exec_approvals_policy.md) (planned, this series) — approvals; relevance: the `approval-pending` return + host approvals the tool obeys.
- [oc_gateway_background_process](oc_gateway_background_process.md) (planned, gw01) — background process/`process` tool; relevance: foreground/background `process` lifecycle referenced in Examples.
- [oc_tools_permission_modes](oc_tools_permission_modes.md) (planned, to06) — `tools.exec.mode` taxonomy; relevance: deny/allowlist/ask/auto/full mode pointer.

**Repos** (4)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw codebase; relevance: the exec tool + host-routing implementation.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: per-agent exec node binding + background-session scoping.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session state; relevance: `/exec` per-session host/security/ask/node overrides.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: PATH/loader-override rejection + authorized-sender model.

**Snippets** (12)
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: the core foreground/background exec dispatch.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — background process supervisor; relevance: the `process` tool's session supervision + `yieldMs`/background.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process tree teardown; relevance: timeout/termination of exec sessions.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows shell shim; relevance: exec's PowerShell-7-then-5.1 host shell selection on Windows.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: env merge + `OPENCLAW_SHELL=exec` + shell-snapshot path.
- [snippet_hermes_agent_tools_terminal_exec](../../code_snippets/snippet_hermes_agent_tools_terminal_exec.md) — terminal exec tool; relevance: parallel coding-agent shell-exec tool.
- [snippet_hermes_agent_tools_terminal_bg](../../code_snippets/snippet_hermes_agent_tools_terminal_bg.md) — background terminal; relevance: background execution analogue to `background`/`yieldMs`.
- [snippet_hermes_agent_tools_terminal_session](../../code_snippets/snippet_hermes_agent_tools_terminal_session.md) — terminal session mgmt; relevance: PTY/send-keys session model like exec's `process` send-keys.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: `host=node` routing + node approvals path.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: forwarding exec to a paired node host.
- [snippet_openclaw_sessions_level_overrides](../../code_snippets/snippet_openclaw_sessions_level_overrides.md) — per-session overrides; relevance: `/exec` session-default override mechanism.
- [snippet_hermes_agent_tools_process_register](../../code_snippets/snippet_hermes_agent_tools_process_register.md) — process registration; relevance: registering background `process` sessions per agent.


### oc_tools_exec_config (8t · 11s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: `tools.exec.*` is OpenClaw's exec config surface.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: these knobs shape every `exec` tool call's policy/timeout/PATH.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation; relevance: `tools.exec.host` default resolves to sandbox; sandbox is off by default.
- [Access Control](../../term_dictionary/term_access_control.md) — gating; relevance: `security`/`ask` knobs are the host-exec access-control dials.
- [Threat Model](../../term_dictionary/term_threat_model.md) — attack-surface; relevance: PATH + `LD_*`/`DYLD_*` rejection defends against binary hijacking / injected code.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints; relevance: `strictInlineEval` forces approval for `python -c`-style inline eval.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial-input attack; relevance: loader/PATH-override rejection blocks an injection→RCE escalation path.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: `apply_patch` is an OpenAI/Codex-only subtool (contrast with Claude models).

**Docs** (11; 6 existing)
- [Claude Code: Execution Tool Behavior](../claude_code/cc_execution_tool_behavior.md) — exec/Bash semantics; relevance: counterpart to the exec timeout/PATH/eval behaviors configured here.
- [Claude Code: Sandboxed Bash Tool Setup](../claude_code/cc_sandboxed_bash_tool_setup.md) — sandbox shell setup; relevance: PATH handling in sandbox (`sh -lc` + profile reset) mirrors this.
- [Claude Code: Permission System and Rules](../claude_code/cc_permission_system_and_rules.md) — permission rules engine; relevance: the policy layer `security`/`mode` knobs feed.
- [Claude Code: Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool permission rules; relevance: per-tool exec policy analogue.
- [Claude Code: Settings Reference](../claude_code/cc_settings_reference.md) — config field reference; relevance: precedent for a documented exec-config-field surface.
- [Claude Code: Sandbox Settings](../claude_code/cc_sandbox_settings.md) — sandbox config fields; relevance: parallels exec host/sandbox config defaults.
- [oc_tools_exec_usage](oc_tools_exec_usage.md) (planned, this series) — exec invocation; relevance: split sibling whose params these knobs back.
- [oc_tools_exec_approvals_safe_bins](oc_tools_exec_approvals_safe_bins.md) (planned, this series) — safe bins detail; relevance: `safeBins`/`safeBinTrustedDirs`/`safeBinProfiles` knobs point here.
- [oc_tools_exec_approvals_policy](oc_tools_exec_approvals_policy.md) (planned, this series) — approvals policy; relevance: `mode`/`security`/`ask` resolve against host approvals.
- [oc_gateway_sandboxing](oc_gateway_sandboxing.md) (planned, gw05) — sandbox config; relevance: defines the sandbox `host=sandbox` runs in.
- [oc_tools_apply_patch](oc_tools_apply_patch.md) (planned, to01) — apply_patch tool; relevance: the `apply_patch` exec subtool detail page.

**Repos** (3)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw codebase; relevance: `tools.exec.*` config loading + PATH merge.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: PATH/loader-override rejection + inline-eval strictness.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: per-agent exec node binding + config overrides.

**Snippets** (11)
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec FS policy; relevance: the policy these `security`/`mode` knobs configure.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env merge; relevance: PATH merge + `pathPrepend` + env-snapshot config.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec security audit; relevance: `openclaw security audit` warns on unprofiled interpreter safe-bins.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe; relevance: audit/doctor probe that scaffolds `safeBinProfiles`.
- [snippet_hermes_agent_tools_patch_parser](../../code_snippets/snippet_hermes_agent_tools_patch_parser.md) — apply-patch parser; relevance: the `apply_patch` structured multi-file edit subtool.
- [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tool config loading; relevance: parallel `tools.*` config parse/validate.
- [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — config schema; relevance: typed config-field schema like `tools.exec.*`.
- [snippet_openclaw_process_windows_cmd_shim](../../code_snippets/snippet_openclaw_process_windows_cmd_shim.md) — Windows shell shim; relevance: per-host shell/PATH handling on Windows.
- [snippet_hermes_agent_core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — shell allowlist hook; relevance: the `strictInlineEval` interpreter-gating concept.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous tool deny; relevance: interaction of tool-policy deny with exec config.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: applying changed `tools.exec.*` config at runtime.

**Entry Points**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1) · [entry_claude_code_docs](../../../0_entry_points/entry_claude_code_docs.md)

### oc_tools_exec_approvals_policy (9t · 12s · 11d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: exec approvals are OpenClaw's host-command guardrail.
- [Access Control](../../term_dictionary/term_access_control.md) — who-may-do-what; relevance: the effective policy is the stricter of config vs host approvals file.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: gateway-authenticated callers are trusted operators (yet approvals are NOT a per-user auth boundary).
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety interlocks; relevance: approvals are the safety interlock around host exec.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human gate; relevance: `ask=on-miss/always` keeps a human approving commands.
- [Threat Model](../../term_dictionary/term_threat_model.md) — attack surface; relevance: trust-model section frames what approvals do/don't defend.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation; relevance: approvals govern when a sandboxed agent may run on the real host.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: approvals gate the `exec` tool call before it runs.
- [IPC (Inter-Process Communication)](../../term_dictionary/term_ipc.md) — local process messaging; relevance: macOS split forwards `system.run` to the app over local IPC.

**Docs** (11; 6 existing)
- [Claude Code: Permission Modes Overview](../claude_code/cc_permission_modes_overview.md) — permission modes; relevance: `mode`/`security`/`ask` map to CC permission modes.
- [Claude Code: Permission Modes Detail](../claude_code/cc_permission_modes_detail.md) — per-mode behavior; relevance: deny/allowlist/ask/full per-mode semantics.
- [Claude Code: Permission System and Rules](../claude_code/cc_permission_system_and_rules.md) — rule engine + precedence; relevance: stricter-of resolution mirrors CC rule precedence.
- [Claude Code: SDK Tool Access Control](../claude_code/cc_sdk_tool_access_control.md) — programmatic access control; relevance: per-agent access-control policy analogue.
- [Claude Code: SDK Permissions Evaluation](../claude_code/cc_sdk_permissions_evaluation.md) — how permissions are evaluated; relevance: the effective-policy resolution algorithm.
- [Claude Code: Managed Permission Settings and Precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — org/managed precedence; relevance: config-vs-host-file precedence parallel.
- [oc_tools_exec_approvals_operations](oc_tools_exec_approvals_operations.md) (planned, this series) — operations; relevance: split sibling covering YOLO/allowlist/flow.
- [oc_tools_exec_usage](oc_tools_exec_usage.md) (planned, this series) — exec tool; relevance: the tool whose calls these approvals gate.
- [oc_tools_permission_modes](oc_tools_permission_modes.md) (planned, to06) — mode taxonomy; relevance: the mode-first overview the page points to.
- [oc_gateway_sandbox_vs_tool_policy_vs_elevated](oc_gateway_sandbox_vs_tool_policy_vs_elevated.md) (planned, gw05) — gate composition; relevance: approvals stack on tool policy + elevated.
- [oc_gateway_security](oc_gateway_security.md) (planned, gw06) — security model; relevance: the broader hardening context for approvals.

**Repos** (3)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: the approvals policy engine + `exec-approvals.json` handling.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw codebase; relevance: `openclaw approvals`/`exec-policy` inspection commands.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: per-agent approval defaults/allowlist scoping.

**Snippets** (12)
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: the core approval-policy resolution + state engine.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec FS policy; relevance: the policy approvals enforce on the execution host.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: gateway-vs-node enforcement split.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec audit; relevance: auditing the effective exec approval policy.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — approval push to client; relevance: surfacing pending approvals to the companion app UI.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool approval policy; relevance: parallel approval-policy model (modes/fallback).
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — auth/authorize dispatch; relevance: gateway-authenticated-caller trust model.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — RPC method gating; relevance: operator-scope gating for approval inspect/set methods.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool policy; relevance: approvals stack on top of tool policy.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload; relevance: applying changed approvals/`tools.exec.*` policy.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: paired nodes extend trusted-operator capability onto the node host.


### oc_tools_exec_approvals_operations (8t · 12s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: operating OpenClaw exec approvals (YOLO/allowlist/flow).
- [Access Control](../../term_dictionary/term_access_control.md) — gating; relevance: per-agent allowlists + `argPattern` are the fine-grained access controls.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human gate; relevance: the request→resolve approval flow keeps a human in the loop unless YOLO.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints; relevance: allowlist/argPattern/auto-allow are the operational guardrails.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: approvals gate each exec tool call; `systemRunPlan` pins the approved call.
- [Subagent](../../term_dictionary/term_subagent.md) — child agents; relevance: per-agent allowlists prevent one agent's approvals leaking to others; subagent denials aren't posted back.
- [Threat Model](../../term_dictionary/term_threat_model.md) — attack surface; relevance: YOLO mode's risk + approval-mismatch rejection defend the host.
- [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — fail-fast safety; relevance: denied/timed-out approvals are terminal and fail-closed (the command does not run).

**Docs** (11; 6 existing)
- [Claude Code: SDK Tool Approval Handling](../claude_code/cc_sdk_tool_approval_handling.md) — programmatic approve/deny; relevance: direct analogue to the request→resolve→forward approval flow.
- [Claude Code: Permission Modes Detail](../claude_code/cc_permission_modes_detail.md) — per-mode behavior; relevance: YOLO=`full`+`ask=off` maps to a bypass permission mode.
- [Claude Code: Managed Permission Settings and Precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — managed precedence; relevance: opening BOTH config + host-file YOLO layers mirrors managed precedence.
- [Claude Code: Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel security controls; relevance: forwarded approvals + native approval cards across channels.
- [Claude Code: Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool rules; relevance: allowlist `pattern`/`argPattern` parallels CC tool-specific rules.
- [Claude Code: Hooks Guardrail and Audit Recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail/audit hooks; relevance: `Exec running`/`Exec finished` system events + audit pattern.
- [oc_tools_exec_approvals_policy](oc_tools_exec_approvals_policy.md) (planned, this series) — policy; relevance: split sibling holding the policy knobs these operations exercise.
- [oc_tools_exec_approvals_forwarding](oc_tools_exec_approvals_forwarding.md) (planned, this series) — forwarding; relevance: the "Safe bins and approval forwarding" pointer target.
- [oc_tools_exec_approvals_safe_bins](oc_tools_exec_approvals_safe_bins.md) (planned, this series) — safe bins; relevance: auto-allow / allowlist-vs-safe-bin interplay.
- [oc_tools_skills](oc_tools_skills.md) (planned, to07) — skills; relevance: "Auto-allow skill CLIs" uses `skills.bins` over the Gateway RPC.
- [oc_cli_approvals](oc_cli_approvals.md) (planned, cl01) — `openclaw approvals` CLI; relevance: the CLI that edits gateway/node approvals + allowlists.

**Repos** (3)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: YOLO/allowlist/flow + denied-approval fail-closed logic.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: per-agent allowlists + auto-allow scoping.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills layer; relevance: `skills.bins` feeding the auto-allow skill-CLI path.

**Snippets** (12)
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — approval manager; relevance: the request→resolve→forward flow + allowlist matching.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: `systemRunPlan` canonical-plan binding for node approvals.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node exec events; relevance: `Exec running`/`Exec finished` system-event surfacing.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: forwarding the approved `system.run` to the node host.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — approval push; relevance: broadcasting `exec.approval.requested` to operator clients.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: allowlist/YOLO/mode operational policy analogue.
- [snippet_hermes_agent_tools_approval_ui](../../code_snippets/snippet_hermes_agent_tools_approval_ui.md) — approval UI; relevance: Control-UI allowlist editing + allow-once/always decisions.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec audit; relevance: auditing allowlist/auto-allow drift.
- [snippet_hermes_agent_core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — shell allowlist; relevance: per-segment allowlist matching for chained commands.
- [snippet_openclaw_agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — subagent spawn policy; relevance: subagent-session denial-handling difference.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: hard-block via tool policy vs allowlist trust.

**Entry Points**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1) · [entry_claude_code_docs](../../../0_entry_points/entry_claude_code_docs.md)

### oc_tools_exec_approvals_safe_bins (8t · 12s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: safe bins are an OpenClaw exec fast-path.
- [Access Control](../../term_dictionary/term_access_control.md) — gating; relevance: safe bins auto-allow narrow stdin filters without explicit allowlist entries.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints; relevance: deterministic argv validation + denied flags are the safe-bin guardrails.
- [Threat Model](../../term_dictionary/term_threat_model.md) — attack surface; relevance: rejecting file operands / `$()` / globs prevents file-read smuggling and existence oracles.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: safe bins decide which exec tool calls skip approval.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation; relevance: docs recommend sandboxing for ambiguous interpreter/runtime forms safe bins refuse.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human gate; relevance: deny-on-ambiguity falls back to explicit approval rather than auto-allow.
- [Circuit Breaker](../../term_dictionary/term_circuit_breaker.md) — fail-safe; relevance: file-binding drift / unbindable interpreter → deny (fail-closed) instead of executing.

**Docs** (11; 6 existing)
- [Claude Code: Permission System and Rules](../claude_code/cc_permission_system_and_rules.md) — rule engine; relevance: safe-bin argv policy + denied flags are deterministic permission rules.
- [Claude Code: Sandbox Filesystem Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — FS/network isolation; relevance: safe bins reject file operands to keep stdin-only filesystem confinement.
- [Claude Code: Execution Tool Behavior](../claude_code/cc_execution_tool_behavior.md) — exec semantics; relevance: shell-chaining / wrapper unwrapping behavior of exec.
- [Claude Code: SDK Tool Access Control](../claude_code/cc_sdk_tool_access_control.md) — access control; relevance: safe-bins-vs-allowlist trust distinction.
- [Claude Code: Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool rules; relevance: allowlist `argPattern` vs safe-bin profile argv policy.
- [Claude Code: Security Guidance Layers and Rules](../claude_code/cc_security_guidance_layers_and_rules.md) — layered guidance; relevance: don't-add-interpreters guidance + audit warnings.
- [oc_tools_exec_config](oc_tools_exec_config.md) (planned, this series) — exec config; relevance: `safeBins`/`safeBinTrustedDirs`/`safeBinProfiles` config knobs live there.
- [oc_tools_exec_approvals_policy](oc_tools_exec_approvals_policy.md) (planned, this series) — policy; relevance: safe bins run within `allowlist` mode policy.
- [oc_tools_exec_approvals_forwarding](oc_tools_exec_approvals_forwarding.md) (planned, this series) — forwarding; relevance: split sibling of the advanced page; async followup delivery.
- [oc_gateway_sandboxing](oc_gateway_sandboxing.md) (planned, gw05) — sandbox; relevance: recommended alternative for ambiguous runtime forms.
- [oc_cli_security](oc_cli_security.md) (planned, cl07) — `openclaw security audit`; relevance: audit warns on unprofiled interpreter safe bins.

**Repos** (3)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: safe-bin argv validator + interpreter file-binding logic.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw codebase; relevance: `tools.exec.safeBins*` parsing + trusted-dir checks.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: per-agent `safeBinProfiles` override keys.

**Snippets** (12)
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec FS policy; relevance: literal-token / no-glob / no-`$VARS` argv rules for safe bins.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec audit; relevance: `tools.exec.safe_bins_interpreter_unprofiled` audit warning.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe; relevance: `openclaw doctor --fix` scaffolding `safeBinProfiles`.
- [snippet_hermes_agent_core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — shell allowlist hook; relevance: per-segment allowlist + safe-bin chaining rules.
- [snippet_hermes_agent_core_tool_guardrails_schema](../../code_snippets/snippet_hermes_agent_core_tool_guardrails_schema.md) — tool guardrail schema; relevance: argv-shape guardrail / denied-flag schema analogue.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — approval manager; relevance: safe-bin fast-path bypass within the approval engine.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: why interpreters must NOT be added to safe bins.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content guard; relevance: literal-text treatment prevents smuggled file reads.
- [snippet_hermes_agent_tools_patch_parser](../../code_snippets/snippet_hermes_agent_tools_patch_parser.md) — argv/command parser; relevance: deterministic argv parsing for flag validation.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: where the bound-file snapshot + denied-on-drift check sits.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: allow-always-doesn't-persist-inline-eval behavior.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit composition; relevance: composing audit warnings for broad-behavior bins like `jq`.


### oc_tools_exec_approvals_forwarding (9t · 11s · 11d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: approval forwarding is an OpenClaw delivery feature.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — human gate; relevance: forwarding puts the approval decision in front of a human in chat.
- [Access Control](../../term_dictionary/term_access_control.md) — gating; relevance: same-chat `/approve` uses the channel auth model; native clients use resolved approver lists.
- [Slack](../../term_dictionary/term_slack.md) — chat platform; relevance: Slack is a primary native approval-delivery channel (`channels.slack.execApprovals`).
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: forwarded prompts gate the underlying exec/plugin tool call.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety; relevance: forwarding preserves the approval guardrail across chat surfaces.
- [IPC (Inter-Process Communication)](../../term_dictionary/term_ipc.md) — local messaging; relevance: macOS IPC flow (UDS + token + HMAC + TTL) delivers approvals to the Mac app.
- [Webhook](../../term_dictionary/term_webhook.md) — event callback; relevance: outbound delivery pipeline + channel callbacks carry approval cards/decisions.

**Docs** (11; 6 existing)
- [Claude Code: Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel security; relevance: forwarding approvals to chat channels with per-channel auth.
- [Claude Code: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — relaying permission prompts to a channel; relevance: direct analogue to forwarding exec/plugin approvals to chat.
- [Claude Code: SDK Tool Approval Handling](../claude_code/cc_sdk_tool_approval_handling.md) — approve/deny handling; relevance: `/approve` allow-once/allow-always/deny decision semantics.
- [Claude Code: Permission Modes Detail](../claude_code/cc_permission_modes_detail.md) — modes; relevance: host policy still decides whether approval is required before forwarding.
- [Claude Code: Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — channel reply/delivery; relevance: same-chat approval delivery on deliverable channels.
- [Claude Code: Security Architecture](../claude_code/cc_security_architecture.md) — security model; relevance: the IPC challenge/response + same-UID peer-check trust model.
- [oc_tools_exec_approvals_operations](oc_tools_exec_approvals_operations.md) (planned, this series) — operations; relevance: the approval flow these channels surface.
- [oc_tools_exec_approvals_safe_bins](oc_tools_exec_approvals_safe_bins.md) (planned, this series) — safe bins; relevance: split sibling of the same advanced page (followup delivery).
- [oc_channels_slack](oc_channels_slack.md) (planned, ch05) — Slack channel; relevance: Slack native approval client + plugin approvers.
- [oc_channels_telegram](oc_channels_telegram.md) (planned, ch05) — Telegram channel; relevance: Telegram DM/topic approval routing + `accountId`/`threadId`.
- [oc_plugins_plugin_permission_requests](oc_plugins_plugin_permission_requests.md) (planned, pl04) — plugin permission requests; relevance: `approvals.plugin` shares the forwarding pipeline.

**Repos** (3)
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel layer; relevance: per-channel native approval clients + delivery targets.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: Slack/Telegram/Matrix/Discord approval-card rendering.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security; relevance: macOS IPC HMAC/TTL + approver-resolution authorization.

**Snippets** (11)
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — approval push delivery; relevance: pushing approval prompts to a native client.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — approval manager; relevance: `/approve` resolution + exec-vs-plugin id routing.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack transport; relevance: Slack native button/interactive-reply delivery.
- [snippet_openclaw_channels_telegram_dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram dispatch; relevance: Telegram DM/forum-topic + multi-account (`accountId`/`threadId`) routing.
- [snippet_openclaw_channels_thread_bindings_policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread binding policy; relevance: `threadId` topic-scoped approval delivery.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM/approver allowlist; relevance: resolved-approver authorization for `/approve`.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke (IPC); relevance: gateway→node-service→Mac-app IPC delivery path.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node exec events; relevance: post-approval followup events into the session.
- [snippet_hermes_agent_tools_approval_ui](../../code_snippets/snippet_hermes_agent_tools_approval_ui.md) — approval UI; relevance: native approval-card UX per channel.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix channel ACL; relevance: Matrix reaction-shortcut approvals + approver auth.


### oc_tools_firecrawl (9t · 10s · 11d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: Firecrawl is a configurable OpenClaw web provider used three ways.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: Firecrawl scrape/extraction feeds page content as RAG context.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — query→results; relevance: Firecrawl is a `web_search` provider plus `firecrawl_search`.
- [Bot Detection](../../term_dictionary/term_bot_detection.md) — anti-bot defenses; relevance: Firecrawl's stealth proxy circumvents bot-blocking on JS-heavy sites.
- [Caching](../../term_dictionary/term_caching.md) — result reuse; relevance: `maxAgeMs`/`storeInCache` control Firecrawl result caching (default 2-day).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy; relevance: proxy modes (`basic`/`stealth`/`auto`) + `baseUrl` self-hosted overrides.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external service; relevance: hosted Firecrawl extraction service requiring `FIRECRAWL_API_KEY`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: `firecrawl_search`/`firecrawl_scrape` are explicit callable tools.
- [DNS](../../term_dictionary/term_dns.md) — name resolution; relevance: base-URL override rejects public hosts, allowing only loopback/private/`.local`/`.internal` targets (SSRF guard).

**Docs** (11; 6 existing)
- [Claude Code: Web Overview](../claude_code/cc_web_overview.md) — web tooling; relevance: precedent for a web search+fetch provider.
- [Claude Code: Web Security and Limits](../claude_code/cc_web_security_and_limits.md) — web limits/safety; relevance: the hosted-vs-private base-URL SSRF guard parallels CC web limits.
- [Claude Code: Advisor Tool](../claude_code/cc_advisor_tool.md) — external-info tool; relevance: scrape-as-tool extraction analogue.
- [Claude Code: Web Quickstart](../claude_code/cc_web_quickstart.md) — enabling web tools; relevance: plugin install + keyless fallback setup analogue.
- [Claude Code: Sandbox Filesystem Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — network isolation; relevance: rejecting private/loopback/metadata targets is a network-safety contract.
- [Claude Code: Built-In Tools](../claude_code/cc_built_in_tools.md) — tool catalog; relevance: where web fetch/scrape sits among tools.
- [oc_tools_exa_search](oc_tools_exa_search.md) (planned, this series) — Exa provider; relevance: sibling search+extraction provider.
- [oc_tools_duckduckgo_search](oc_tools_duckduckgo_search.md) (planned, this series) — key-free provider; relevance: sibling provider that suffers bot blocks Firecrawl circumvents.
- [oc_tools_web_fetch](oc_tools_web_fetch.md) (planned, to08) — web_fetch tool; relevance: Firecrawl is the fallback extractor in `web_fetch`'s extraction order.
- [oc_tools_web](oc_tools_web.md) (planned, to08) — provider overview; relevance: parent page listing Firecrawl + auto-detection.
- [oc_tools_tavily](oc_tools_tavily.md) (planned, to07) — Tavily provider; relevance: another search+extract sibling.

**Repos** (3)
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw codebase; relevance: `web_fetch` extraction order + provider auto-detection.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin layer; relevance: Firecrawl ships as `@openclaw/firecrawl-plugin`.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider-plugin layer; relevance: Firecrawl is a provider-style extension with key/base-URL config.

**Snippets** (10)
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web search/fetch tools; relevance: parallel web_fetch with extractor-fallback ordering.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content guard; relevance: scraped pages are untrusted external content.
- [snippet_hermes_agent_tools_browser_camofox](../../code_snippets/snippet_hermes_agent_tools_browser_camofox.md) — stealth browser; relevance: stealth/anti-bot fetching analogue to Firecrawl stealth proxy.
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — CDP browser control; relevance: JS-heavy-site extraction alternative to plain HTTP fetch.
- [snippet_hermes_agent_tools_browser_intercept](../../code_snippets/snippet_hermes_agent_tools_browser_intercept.md) — request interception; relevance: proxy/interception layer like Firecrawl proxy modes.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: registering `firecrawl_search`/`firecrawl_scrape` tools.
- [snippet_hermes_agent_tools_schema_sanitizer](../../code_snippets/snippet_hermes_agent_tools_schema_sanitizer.md) — param schema; relevance: scrape param schema (`url`/`extractMode`/`proxy`/`maxAgeMs`).
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregation; relevance: base-URL override + provider auto-detect mirrors Firecrawl config.
- [snippet_slipbot_bm25_search](../../code_snippets/snippet_slipbot_bm25_search.md) — keyword search; relevance: `web_search`-via-Firecrawl keyword IR analogue.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: provider-selection plumbing for fetch/search provider.

**Entry Points**: [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) (planned, master W1) · [entry_claude_code_docs](../../../0_entry_points/entry_claude_code_docs.md)

## Undigested Terms Plan

Per master: OpenClaw vocabulary terms are digested as `oc_` doc notes (here, config/procedure subjects), NOT as new `term_dictionary` entries; the only `term_dictionary` interaction is LINKING existing terms. **Expected: 0 new `term_dictionary` captures.**

| Term (surface vocabulary in this batch) | Disposition |
|---|---|
| exec tool, `/exec`, host routing (auto/sandbox/gateway/node) | Digested in `oc_tools_exec_usage` (oc doc note); link `term_function_calling`, `term_sandbox`. |
| `tools.exec.*` config (mode/security/ask/askFallback/strictInlineEval/pathPrepend/apply_patch) | Digested in `oc_tools_exec_config` (oc doc note). |
| elevated mode, `/elevated`, break-glass | Digested in `oc_tools_elevated` (oc doc note); link `term_sandbox`, `term_access_control`. |
| exec approvals, allowlist, `argPattern`, YOLO mode, `askFallback` | Digested in `oc_tools_exec_approvals_*` (oc doc notes); link `term_access_control`, `term_guardrails`, `term_human_in_the_loop`. |
| safe bins, `safeBinProfiles`, interpreter binding | Digested in `oc_tools_exec_approvals_safe_bins` (oc doc note). |
| approval forwarding, `/approve`, native approval delivery, `systemRunPlan` | Digested in `oc_tools_exec_approvals_forwarding` / `_operations` (oc doc notes); link `term_slack`, `term_ipc`. |
| DuckDuckGo / Exa / Firecrawl search providers, `web_search`, `web_fetch`, `firecrawl_scrape` | Digested in `oc_tools_duckduckgo_search` / `oc_tools_exa_search` / `oc_tools_firecrawl` (oc doc notes); link `term_rag`, `term_information_retrieval`, `term_bot_detection`, `term_third_party_genai_services` — provider names are config subjects, NOT promoted to term notes. |


## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from master). If augment Step 2d surfaces a genuinely cross-cutting, vault-reusable term with no doc-page home AND no existing note, it would be captured via `/tessellum-capture-term-note` + added to the best-fit `acronym_glossary_*.md` (most likely `acronym_glossary_a_e.md` for an agent/auth term or `acronym_glossary_s_z.md` for a security term) — but none is expected.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (10 notes, P2). All gates must pass before commit.

| Gate | Check | How |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` on all 10 notes (YAML field order, `## Overview`/`## Related Notes`, footer). |
| G2 | Grounding | Diff each note vs its `inbox/openclaw_docs/tools/<page>.md` source section(s); no invented config keys/params/flags; verbatim snippets. |
| G3 | Density + Coverage | ≤400L / ≤2500w / ≤6 code, single BB per note; every mapped H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevancy-selected terms + repo/sibling/doc links per note, each with a relevance statement. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` after incremental reindex; 0 broken links. |
| G7/G8 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` rows + the W3 inlinks below. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_tools_duckduckgo_search oc_tools_elevated oc_tools_exa_search oc_tools_exec_usage oc_tools_exec_config oc_tools_exec_approvals_policy oc_tools_exec_approvals_operations oc_tools_exec_approvals_safe_bins oc_tools_exec_approvals_forwarding oc_tools_firecrawl"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + required sections
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # REQUIRE_SOURCE_URL
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url:|^\*\*Source\*\*' "$f" || echo "$n MISSING source_url"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done

# G1 YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost-reference: every cited EXISTING note_id must resolve (sibling oc_* planned excluded)
# G6 broken links after reindex
bash scripts/update_notes_database.sh
# then /tessellum-fix-broken-links
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_tools_duckduckgo_search | procedure | 350 | 3 | ✅ |
| 2 | oc_tools_elevated | procedure | 550 | 3 | ✅ |
| 3 | oc_tools_exa_search | procedure | 550 | 4 | ✅ |
| 4 | oc_tools_exec_usage | procedure | 600 | 5 | ✅ |
| 5 | oc_tools_exec_config | procedure | 600 | 4 | ✅ |
| 6 | oc_tools_exec_approvals_policy | procedure | 650 | 4 | ✅ |
| 7 | oc_tools_exec_approvals_operations | procedure | 650 | 4 | ✅ |
| 8 | oc_tools_exec_approvals_safe_bins | procedure | 650 | 3 | ✅ |
| 9 | oc_tools_exec_approvals_forwarding | procedure | 650 | 4 | ✅ |
| 10 | oc_tools_firecrawl | procedure | 650 | 3 | ✅ |

No note approaches caps. The three split pages (exec / exec-approvals / exec-approvals-advanced) each fan their fences across two notes so every note stays ≤6 code blocks; the four single-note pages are already ≤4 code / ≤711w.

## Entry Point Decision (inherited from master)

Contributes **10 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before first execution), under a **Tools** section, sub-clustered as "Web research providers" (notes 1, 3, 10) and "Shell exec & approvals" (notes 2, 4–9). Each note receives its entry-point back-link at finalization. No standalone entry point is created for this sub-plan (the series shares the single master-level `entry_openclaw_docs.md`).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify + add at execution for G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` (planned, master W1) → ALL 10 notes (primary anti-island guarantee).
- `repo_openclaw_security.md` → notes 2, 4, 5, 6, 7, 8 (exec/elevated/approvals security surface).
- `repo_openclaw_extensions.md` → notes 1, 3, 10 (search-provider plugins).
- `repo_openclaw_extensions_llm_providers.md` → notes 3, 10 (Exa/Firecrawl provider extensions).
- `repo_openclaw_channels.md` / `repo_openclaw_channels_messaging.md` → note 9 (approval forwarding to chat channels).
- `repo_openclaw_agents.md` → notes 4, 5, 6 (per-agent exec policy/allowlists).
- `term_sandbox.md` → notes 2, 4 (sandbox break-out + host routing); `term_access_control.md` → notes 6, 7 (approvals policy); `term_function_calling.md` → notes 4, 6 (the exec tool surface); `term_rag.md` → notes 1, 3, 10 (search-for-retrieval); `term_bot_detection.md` → notes 1, 10 (HTML-scrape / anti-bot); `term_human_in_the_loop.md` → notes 6, 7, 9 (approval gating).
- `term_openclaw.md` + `repo_openclaw.md` → cross-link to `entry_openclaw_docs.md` per master W3 (hub-level, covers all notes transitively).

## Pacing Rules (inherited from master)

One execution phase, 10 notes (well under the ~30-agent fan-out cap). Re-read each source page before authoring its note(s); reproduce config snippets verbatim; one BB per note. Run all 8 gates before commit; reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1; then `git pull --rebase --autostash origin main`, commit (no Claude co-author trailer), and `git push origin main` in the same turn.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — READY (9/9 CP PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Source re-read + remeasurement (CP7 input):** exec.md 2247w/9 fences · exec-approvals.md 2718w/5 fences · exec-approvals-advanced.md 2949w/6 fences · exa-search.md 573w/3 · duckduckgo-search.md 322w/2 · elevated.md 568w/0 · firecrawl.md 660w/3. All within ±5% of the plan's Source table; the three >2,500w pages confirm the existing splits.

**What was locked — per-note counts (terms / snippets / docs / repos):**

| # | Note | Terms | Snippets | Docs (existing) | Repos | Floors (≥8t·≥10s·≥10d) |
|---|---|---:|---:|---:|---:|:---:|
| 1 | oc_tools_duckduckgo_search | 8 | 10 | 11 (6) | 2 | ✅ |
| 2 | oc_tools_elevated | 8 | 10 | 10 (6) | 3 | ✅ |
| 3 | oc_tools_exa_search | 8 | 10 | 11 (6) | 3 | ✅ |
| 4 | oc_tools_exec_usage | 9 | 12 | 11 (6) | 4 | ✅ |
| 5 | oc_tools_exec_config | 8 | 11 | 11 (6) | 3 | ✅ |
| 6 | oc_tools_exec_approvals_policy | 9 | 12 | 11 (6) | 3 | ✅ |
| 7 | oc_tools_exec_approvals_operations | 8 | 12 | 11 (6) | 3 | ✅ |
| 8 | oc_tools_exec_approvals_safe_bins | 8 | 12 | 11 (6) | 3 | ✅ |
| 9 | oc_tools_exec_approvals_forwarding | 9 | 11 | 11 (6) | 3 | ✅ |
| 10 | oc_tools_firecrawl | 9 | 10 | 11 (6) | 3 | ✅ |



**Notes corrected during augment:** removed a duplicate `term_autonomous_coding_agents` entry in `oc_tools_exec_usage` and substituted `term_cron` (page directs scheduled/long-running work to cron, not exec sleep/timeout loops) — keeps 9 distinct relevant terms.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

PLAN REVIEW — FINAL SIGN-OFF · Plan: `plan_digest_openclaw_docs_to03.md` · Date: 2026-06-21

| CP | Checkpoint | Result | Evidence |
|---|---|:---:|---|
| CP2 | 9-GATE present (G1–G6 + G7/G8 + G9) per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link-fix, G7/G8 discoverability (in-degree ≥1); single execution phase. |
| CP4 | Size manageable | **PASS** | 10 notes (well ≤30 and ≤ the ~30-agent fan-out cap); single execution phase. |
| CP5 | Format derived (not invented) from target-dir notes | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` corpora (`## Overview` … `## Related Notes` … `## References`, YAML field order, forbidden-field list); matches existing `resources/documentation/` notes. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: every note ≤650w / ≤6 code; the three >2,500w pages (exec/exec-approvals/exec-approvals-advanced) each split into 2 notes (Split Decisions table); no note approaches caps. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 7 pages 2026-06-21 (2247/2718/2949/573/322/568/660 w); all within ±5% of the plan's Source table; ratio 0.97–1.04 — no under-estimation, no further split needed. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows disposition = digest-as-oc-doc / link existing term; 0 new captures); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, with the `/tessellum-capture-term-note` + best-fit-glossary fallback path documented should one surface). |
| CP8f | Slug specificity / collision audit (term AND doc) | **PASS** | 0 new term slugs to specificity-audit. Doc-vs-term collision audit: planned `oc_tools_*` slugs checked against `term_dictionary/` + `documentation/` — no `oc_` note duplicates an existing term/doc; OpenClaw concepts are doc-page subjects linked to existing terms (`term_openclaw`, `term_sandbox`, etc.), not re-captured. Dedup-before-create inherited from master. |
| CP9 | Discoverability / inlinks (G8, in-degree ≥1, no islands) | **PASS** | `## Inlinks (existing notes → new notes)` maps outside-folder inbound links to all 10 notes (`entry_openclaw_docs` → all 10 primary anti-island, plus `repo_openclaw_security`/`_extensions`/`_extensions_llm_providers`/`_channels`/`_agents` + term backlinks); G7/G8 in the gate table; inlinks are an EXECUTED phase, not "recommended". |

**RESULT: 9/9 (CP1–CP9 incl. CP8f) PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
