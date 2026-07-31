---
title: Sub-Plan to06 — OpenClaw Docs: Tools (PDF, Permission Modes, Search Providers, Plugins, Reactions, Skill Workshop)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["tools/pdf", "tools/permission-modes", "tools/perplexity-search", "tools/plugin", "tools/reactions", "tools/searxng-search", "tools/skill-workshop"]
---



# Sub-Plan to06: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_*`), format (YAML field order + body H2s + density caps),
> dedup (3-way across term_dictionary / documentation / repo_openclaw*), 9-GATE, cross-references, and entry-point
> wiring (W1–W5 → `entry_openclaw_docs.md`) are ALL inherited from the master and not re-derived here.

## Scope

The 7 `tools/` pages covering a mixed cluster of agent-tool reference + operator-policy docs: the `pdf` document-analysis
tool, the host-exec/Codex/ACPX **permission modes** policy surface, two `web_search` providers (**Perplexity** and
**SearXNG**), the cross-cutting **plugins** install/config/manage page (the largest in this sub-plan), the channel-agnostic
**reactions** tool semantics, and **Skill Workshop** (the governed in-chat skill authoring path). Priority **P2** (Phase B —
features/integration). These docs are how-to/reference for end users configuring agent tools and providers; the code-side
counterparts (`repo_openclaw_skills`, `repo_openclaw_extensions*`, `repo_openclaw_security`, `repo_openclaw_gateway`) are
LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 6,960 measured words. **Planned: 8 notes** (plugin.md splits into 2).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| PDF tool | tools/pdf | 890 | 5 | 9 | 2 | procedure |
| Permission modes | tools/permission-modes | 701 | 4 | 6 | 0 | procedure |
| Perplexity search | tools/perplexity-search | 735 | 4 | 8 | 3 | procedure |
| Plugins | tools/plugin | 2,388 | 12 | 8 | 5 | procedure (split: install vs config/policy/ops) |
| Reactions | tools/reactions | 488 | 1 | 4 | 0 | procedure |
| SearXNG search | tools/searxng-search | 579 | 6 | 6 | 0 | procedure |
| Skill Workshop | tools/skill-workshop | 1,179 | 15 | 13 | 0 | procedure |

(Code = raw ``` fence count ÷ 2. Word counts via `wc -w` on the verbatim mirror including frontmatter.)

## Content Strategy

- **Prioritize**: the **plugins** page (install/discovery/policy is the prerequisite every provider+tool page references),
  **permission modes** (the exec authority surface that gates host commands), and the two **web_search providers**
  (operationally common). PDF + reactions + Skill Workshop are self-contained tool references.
- **Split**: `tools/plugin.md` (2,388w / 12 fences / 8 H2 / 5 H3) → two notes: an **install + quick-start + format** procedure
  and a **config / policy / hooks / verify / troubleshooting** procedure. One page over the dense band; splitting keeps each
  note ≤6 code blocks and well under the 2,500-word cap while preserving two clean task clusters. All other pages = 1 note.
- **Link-out (not duplicated)**: exec-approvals schema (`tools/exec-approvals`, sub-plan to03) — referenced from permission-modes;
  Codex harness app-server detail (`plugins/codex-harness`, Phase C) — referenced from permission-modes; ACP agents setup
  (`tools/acp-agents-setup`, to01); the `web` search overview (`tools/web`, to08) — referenced from both search-provider notes;
  `agent-send`/`message` tool (`tools/agent-send`, to01) — referenced from reactions; `tools/skills` + `tools/creating-skills`
  + `tools/skills-config` (to07) — referenced from Skill Workshop; `gateway/configuration-reference` (gw02) — referenced from PDF.
  Provider/tool vocabulary is digested as `oc_*` doc content, never inlined as a term definition.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_pdf.md` | procedure | tools/pdf.md (all H2: Availability, Input reference, Supported PDF references, Execution modes [Native/Extraction fallback], Config, Output details, Error behavior, Examples) | 650 | The `pdf` tool: model-availability resolution chain, input params (pdf/pdfs/pages/password/model/maxBytesMb), supported references, native-provider vs extraction-fallback execution modes, config, output `details`, error behavior, and examples. |
| 2 | `oc_tools_permission_modes.md` | procedure | tools/permission-modes.md (all H2: Recommended default, OpenClaw host exec modes, Codex Guardian mapping, ACPX harness permissions, Choosing a mode) | 600 | Permission modes for agent authority: `tools.exec.mode` (deny/allowlist/ask/auto/full) vs `tools.exec.host`, Codex Guardian approval mapping, ACPX harness `permissionMode`/`nonInteractivePermissions`, and the decision matrix. |
| 3 | `oc_tools_perplexity_search.md` | procedure | tools/perplexity-search.md (all H2: Install plugin, Getting an API key, OpenRouter compatibility, Config examples [Native/OpenRouter-Sonar], Where to set the key, Tool parameters, Notes) | 600 | The Perplexity `web_search` provider: install the plugin, get a `PERPLEXITY_API_KEY`/`OPENROUTER_API_KEY`, native Search-API vs Sonar/OpenRouter chat-completions paths, config examples, key placement, and tool parameters (query/count/freshness/domain_filter/etc.). |
| 4 | `oc_tools_plugin_install.md` | procedure | tools/plugin.md: intro, Requirements, Quick start (find/install/configure/reload/verify), Configuration → Choose an install source, Understand plugin formats | 600 | Installing OpenClaw plugins: requirements, the quick-start flow (search ClawHub → install from clawhub/npm/git/local/marketplace → enable → Gateway reload → verify runtime), install-source selection + bare-spec resolution, and native vs compatible-bundle plugin formats. |
| 5 | `oc_tools_plugin_config.md` | procedure | tools/plugin.md: Configuration → Operator install policy + Configure plugin policy, Plugin hooks, Verify the active Gateway, Troubleshooting (+ Blocked path ownership, Slow plugin tool setup) | 700 | Configuring and operating plugins: `security.installPolicy`, the `plugins.{enabled,allow,deny,load,slots,entries}` policy shape and precedence rules, typed (`api.on`) vs internal (`api.registerHook`) plugin hooks, verifying the live Gateway, and the troubleshooting matrix (ownership-blocked paths, slow tool factories). |
| 6 | `oc_tools_reactions.md` | procedure | tools/reactions.md (all H2: How it works, Channel behavior, Reaction level) | 450 | The `react` action on the `message` tool: add/remove emoji reactions, `remove`/`trackToolCalls` semantics, per-channel behavior across Discord/Slack/Google Chat/Nextcloud Talk/Telegram/WhatsApp/Zalo/Feishu/Signal/iMessage, and per-channel `reactionLevel`. |
| 7 | `oc_tools_searxng_search.md` | procedure | tools/searxng-search.md (all H2: Setup, Config, Environment variable, Plugin config reference, Notes) | 500 | The SearXNG self-hosted, key-free `web_search` provider: run an instance, configure `provider: "searxng"` + plugin `webSearch.{baseUrl,categories,language}`, the `SEARXNG_BASE_URL` env var + auto-detection order, transport/network-guard rules, and behavior notes (JSON API, category fallback). |
| 8 | `oc_tools_skill_workshop.md` | procedure | tools/skill-workshop.md (all H2: How it works, Lifecycle, Chat, CLI, Proposal content, Support files, Agent tool, Approval and autonomy, Gateway methods, Storage, Limits, Troubleshooting) | 700 | Skill Workshop, the governed proposal-first path for creating/updating workspace skills: proposal lifecycle (pending→applied/rejected/quarantined/stale), chat + CLI flows, `PROPOSAL.md` content + support-file rules, the `skill_workshop` agent tool, approval/autonomy config, Gateway methods + operator scopes, storage layout, and limits. |

## Section Coverage Map

```
tools/pdf.md
├── (intro: native vs fallback, single/multi, max 10) ── → note 1 (oc_tools_pdf)
├── ## Availability (model resolution chain, auth-aware) → note 1
├── ## Input reference (pdf/pdfs/prompt/pages/password/model/maxBytesMb + notes) → note 1
├── ## Supported PDF references (path/file/http/media://, rejections) → note 1
├── ## Execution modes → ### Native provider mode / ### Extraction fallback mode → note 1
├── ## Config (json5 agents.defaults.pdfModel/pdfMaxBytesMb/pdfMaxPages) → note 1
├── ## Output details (content[0].text, details.{model,native,attempts}) → note 1
├── ## Error behavior (too_many_pdfs / unsupported_pdf_reference / pages-native) → note 1
└── ## Examples (single/multi/page-filtered/encrypted) ── → note 1

tools/permission-modes.md
├── (intro + Note: mode vs host distinction) ─────────── → note 2 (oc_tools_permission_modes)
├── ## Recommended default (auto, verify cmds) ───────── → note 2
├── ## OpenClaw host exec modes (deny/allowlist/ask/auto/full table) → note 2
├── ## Codex Guardian mapping (approvalPolicy/reviewer/sandbox) → note 2
├── ## ACPX harness permissions (permissionMode / nonInteractivePermissions) → note 2
└── ## Choosing a mode (goal→config matrix, stricter-result rule) → note 2

tools/perplexity-search.md
├── (intro: Search API vs Sonar/OpenRouter switch) ──── → note 3 (oc_tools_perplexity_search)
├── ## Install plugin ───────────────────────────────── → note 3
├── ## Getting a Perplexity API key ─────────────────── → note 3
├── ## OpenRouter compatibility ─────────────────────── → note 3
├── ## Config examples → ### Native / ### OpenRouter-Sonar / ### Domain filter rules → note 3
├── ## Where to set the key (config / env / fail-fast) ─ → note 3
├── ## Tool parameters (query/count/country/.../domain_filter + Sonar restrictions + examples) → note 3
└── ## Notes (structured vs synthesized, 15-min cache) ─ → note 3

tools/plugin.md
├── (intro: what plugins extend) ────────────────────── → note 4 (oc_tools_plugin_install)
├── ## Requirements ─────────────────────────────────── → note 4
├── ## Quick start (find/install/configure/reload/verify) → note 4
├── ## Configuration → ### Choose an install source (+ bare-spec/npm-compat rules) → note 4
├── ## Understand plugin formats (native vs compatible bundle) → note 4
├── ## Configuration → ### Operator install policy (security.installPolicy) → note 5 (oc_tools_plugin_config)
├── ## Configuration → ### Configure plugin policy (plugins.{enabled,allow,deny,load,slots,entries} rules) → note 5
├── ## Plugin hooks (typed api.on vs api.registerHook) ─ → note 5
├── ## Verify the active Gateway ────────────────────── → note 5
└── ## Troubleshooting (matrix) → ### Blocked plugin path ownership / ### Slow plugin tool setup → note 5

tools/reactions.md
├── (intro: react action on message tool) ───────────── → note 6 (oc_tools_reactions)
├── ## How it works (emoji/remove/trackToolCalls) ───── → note 6
├── ## Channel behavior (per-channel accordion: Discord/Slack/Google Chat/Nextcloud Talk/Telegram/WhatsApp/Zalo/Feishu/Signal/iMessage) → note 6
└── ## Reaction level (per-channel reactionLevel) ───── → note 6

tools/searxng-search.md
├── (intro + advantages: free/privacy/anywhere) ─────── → note 7 (oc_tools_searxng_search)
├── ## Setup (docker run / configure / env) ─────────── → note 7
├── ## Config (json5 provider + plugin webSearch + transport rules) → note 7
├── ## Environment variable (SEARXNG_BASE_URL + auto-detect) → note 7
├── ## Plugin config reference (baseUrl/categories/language) → note 7
└── ## Notes (JSON API, network guard, order 200, category fallback) → note 7

tools/skill-workshop.md
├── (intro: governed skill authoring, proposal-first, workspace-only) → note 8 (oc_tools_skill_workshop)
├── ## How it works (proposal-first/apply-only-write/...) → note 8
├── ## Lifecycle (create→pending→applied/rejected/quarantined/stale) → note 8
├── ## Chat (create/update/iterate examples) ────────── → note 8
├── ## CLI (propose-create/propose-update/list/inspect/revise/apply/reject/quarantine) → note 8
├── ## Proposal content (PROPOSAL.md frontmatter, apply strips fields) → note 8
├── ## Support files (--proposal-dir, allowed folders, rejected paths) → note 8
├── ## Agent tool (skill_workshop actions, tools.profile coding) → note 8
├── ## Approval and autonomy (skills.workshop.* config) → note 8
├── ## Gateway methods (skills.proposals.* + operator.read/admin scopes) → note 8
├── ## Storage (state-dir layout) ───────────────────── → note 8
├── ## Limits (description/body/support-file/pending caps) → note 8
└── ## Troubleshooting (problem→resolution table) ───── → note 8
```
No orphaned sections. Every `## Related` block is mined for cross-references (it is not digested as body content). Link-out
targets (exec-approvals, codex-harness, acp-agents-setup, tools/web, agent-send, tools/skills*, configuration-reference) are
linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `tools/plugin.md` (2,388w · 12 fences · 8 H2 / 5 H3) | note 4 `oc_tools_plugin_install` + note 5 `oc_tools_plugin_config` | Single page in the dense band (near the 2,500w cap; would exceed once Overview + Related Notes are added) with two distinct task clusters: (a) get-a-plugin-running (requirements → quick start → install source → formats) and (b) govern/operate it (install policy + policy precedence + hooks + verify live Gateway + troubleshooting). Split keeps each note ≤6 code blocks and ≤~700w with a single clean procedure focus. |

All other 6 pages are 1 note each (each ≤1,200w, single procedure BB, ≤6 code blocks once trimmed).

## Summary Statistics & Building Block Distribution

- Source pages: 7 (6,960 measured words). New `oc_*` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×8** (every page is a tool/provider/policy how-to). No concept/model/argument notes in this sub-plan.
- Est. digest words ~4,800 (avg ~600/note); range 450–700. None approaches the 2,500-word cap.
- Source code fences total 47 (raw 94 ÷ 2): pdf 5 · permission-modes 4 · perplexity 4 · plugin 12 (→6+6 across notes 4/5) ·
  reactions 1 · searxng 6 · skill-workshop 15. Each note reproduces ≤6 fences (config blocks + CLI examples kept verbatim,
  selectively; skill-workshop's 15 fences trimmed to the load-bearing lifecycle/CLI/config/storage blocks).
- **Cross-refs (LOCKED at xref-augment 2026-06-21, raised floors):** each note carries **≥8 `term_dictionary` terms · ≥10
  `code_snippets` · ≥10 docs under `resources/documentation/`** (PLUS relevant `repo_openclaw*` + sibling `oc_*` planned),
  `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (against a fresh re-read of each source page),
> on 2026-06-21. Sibling `oc_tools_*` / other `oc_*` docs in this series do NOT exist yet → cited as **(planned, this series/subplan)**
> term → `../../term_dictionary/`, snippet → `../../code_snippets/`, cross-folder doc → `../<folder>/`, repo →
> `../../../areas/code_repos/`, sibling oc → `oc_*.md`.

### oc_tools_pdf (10t · 10s · 10d)

**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: every resolved `pdfModel` (Anthropic/Google/fallback) fronts an LLM that consumes the PDF.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: Anthropic is one of the two native-PDF providers that take raw PDF bytes.
- [Multimodal](../../term_dictionary/term_multimodal.md) — combined text+image modeling; relevance: PDF analysis mixes extracted text with rendered page images.
- [VLM](../../term_dictionary/term_vlm.md) — vision-language model; relevance: the fallback path renders pages to PNG that a vision-capable model reads.
- [Document Understanding](../../term_dictionary/term_document_understanding.md) — extracting structure/meaning from documents; relevance: the `pdf` tool IS a document-understanding capability.
- [Document VLM](../../term_dictionary/term_document_vlm.md) — VLMs specialized for document images; relevance: image-fallback mode is exactly document-VLM territory (rendered pages → vision model).
- [OCR](../../term_dictionary/term_ocr.md) — optical character recognition; relevance: extraction fallback renders pages to PNG when text is thin — the OCR-adjacent path.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: `pdf` is an agent tool the model invokes with structured args.
- [Bedrock](../../term_dictionary/term_bedrock.md) — AWS managed model service; relevance: a non-native provider reachable via the `model` override → extraction fallback.
- [Computer Vision](../../term_dictionary/term_computer_vision.md) — image analysis; relevance: the 4M-pixel page-render budget feeds a CV/vision model in fallback.

**Docs**
- [oc_tools_permission_modes](oc_tools_permission_modes.md) (planned, this series) — exec/sandbox authority; relevance: sandbox mode + workspace-only file policy gate the `pdf` tool's remote URLs and local paths.
- [oc_gateway_configuration_reference](../openclaw/oc_gateway_configuration_reference.md) (planned, gw02) — full config field reference; relevance: documents `agents.defaults.pdfModel/pdfMaxBytesMb/pdfMaxPages`.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — Hermes media/document tool reference; relevance: closest sibling-ecosystem doc for a media-analysis agent tool.
- [hermes_vision_image_paste](../hermes_agent/hermes_vision_image_paste.md) — image/vision input handling; relevance: parallels the rendered-page-image fallback path for vision models.
- [hermes_model_aux_provider_config](../hermes_agent/hermes_model_aux_provider_config.md) — auxiliary/vision-model provider config; relevance: analog of OpenClaw's pdfModel/imageModel resolution chain.
- [hermes_tools_reference_core](../hermes_agent/hermes_tools_reference_core.md) — core agent tool reference; relevance: same doc genre (per-tool params/limits/errors).
- [cc_sdk_tool_rich_content](../claude_code/cc_sdk_tool_rich_content.md) — tool results with documents/images; relevance: CC analog of a tool returning structured `details` + text content blocks.
- [cc_request_and_quality_errors](../claude_code/cc_request_and_quality_errors.md) — request/quality error taxonomy; relevance: maps to the `too_many_pdfs`/`unsupported_pdf_reference`/native-pages error behaviors.
- [bedrock_messages_api](../aws_bedrock/bedrock_messages_api.md) — Bedrock document/image content blocks; relevance: shows how a non-native provider receives PDF/document content (fallback target).
- [bedrock_foundation_models_reference](../aws_bedrock/bedrock_foundation_models_reference.md) — model capability reference; relevance: which Bedrock models support document/vision input (governs the auth-aware fallback chain).

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/model resolution; relevance: resolves the pdfModel→imageModel→default auth-aware chain.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin layer; relevance: the bundled `document-extract` plugin / `clawpdf` (PDFium WASM) lives here.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/file policy; relevance: workspace-only file policy + sandbox path rewrite for PDF refs.

**Snippets**
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision-tool dispatch; relevance: parallels native-vs-fallback routing of a document to a vision model.
- [snippet_brp_agent_tools_extract](../../code_snippets/snippet_brp_agent_tools_extract.md) — document/text extraction tool; relevance: the extract-text-first behavior of extraction fallback mode.
- [snippet_hermes_agent_core_anthropic_adapter_normalization](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_normalization.md) — Anthropic request normalization; relevance: how raw document bytes become native Anthropic document blocks.
- [snippet_hermes_agent_core_gemini_native_adapter_init](../../code_snippets/snippet_hermes_agent_core_gemini_native_adapter_init.md) — Google/Gemini native adapter; relevance: the second native-PDF provider path (Google).
- [snippet_hermes_agent_core_bedrock_adapter_format](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_format.md) — Bedrock request formatting; relevance: how a fallback (non-native) provider is fed extracted content.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — model fallback/cooldown; relevance: the `attempts` field + fallback chain when a provider fails.
- [snippet_hermes_agent_model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — model capability probe; relevance: the auth-aware "does this provider support PDF/vision" resolution.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — media-plugin dispatch; relevance: analog of the document-extract plugin owning a media capability.
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — building per-call model kwargs; relevance: how prompt + model + content assemble into the request the PDF tool sends.
- [snippet_hermes_agent_core_message_sanitization](../../code_snippets/snippet_hermes_agent_core_message_sanitization.md) — content sanitization before send; relevance: dedup/merge of `pdf`+`pdfs` inputs before loading.

### oc_tools_permission_modes (10t · 10s · 10d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated exec environment; relevance: modes choose the Codex sandbox posture (`workspace-write` vs `danger-full-access`).
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — the engine enforcing sandboxing; relevance: the layer that actually applies the chosen sandbox setting.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — human approval in an automated flow; relevance: `ask` mode + the human approval route on allowlist misses.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization surface; relevance: `tools.exec.mode` is the host-exec authorization surface.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints on agent actions; relevance: allowlist + auto-review are the exec guardrails between deny and full.
- [Deny First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: `deny` mode + "stricter result of two layers" embody deny-first.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — escalating authority by trust; relevance: deny→allowlist→ask→auto→full is a graduated-trust ladder.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: Codex Guardian auto-review is an autonomous coding-agent approval path (`term_codex` absent → this links the concept).
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client session protocol; relevance: ACPX harness permissions govern non-interactive ACP sessions.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: host `exec` is the tool call these modes gate.

**Docs**
- [oc_tools_plugin_config](oc_tools_plugin_config.md) (planned, this series) — `security.installPolicy`; relevance: a sibling operator-policy surface (install authority next to exec authority).
- [oc_tools_exec_approvals](../openclaw/oc_tools_exec_approvals.md) (planned, to03) — host exec policy + approvals file; relevance: the full allowlist schema / approvals file this page links out to.
- [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — CC permission-mode taxonomy; relevance: directly analogous deny/ask/auto/full-style mode taxonomy.
- [cc_permission_modes_detail](../claude_code/cc_permission_modes_detail.md) — CC mode behavior detail; relevance: per-mode behavior analog for the exec-mode table.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox-vs-permission distinction; relevance: mirrors the load-bearing `tools.exec.mode` (how-approved) vs `tools.exec.host` / sandbox (where-runs) distinction.
- [cc_tool_specific_permission_rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool permission rules; relevance: analog of allowlist matches for specific command shapes.
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — managed/precedence settings; relevance: parallels "stricter result of OpenClaw config and host-local approvals file".
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — Hermes command approval; relevance: sibling-ecosystem command-approval/allowlist flow.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — host/terminal exec backends; relevance: `tools.exec.host` (where a command runs) maps to terminal backends.
- [pi_security_model](../pi/pi_security_model.md) — Pi security/permission model; relevance: a third coding-agent's permission/sandbox model for cross-tool comparison.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec/approval enforcement; relevance: implements exec policy + approvals + stricter-of-two-layers.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway exec routing/restart; relevance: `gateway restart` applies mode changes; routes host exec.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent exec authority; relevance: the agent whose host-exec authority these modes constrain.

**Snippets**
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval decision engine; relevance: the engine that implements deny/allowlist/ask/auto/full.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec+filesystem policy resolution; relevance: the stricter-of-two-layers rule across config and approvals file.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — ACP permission relay; relevance: relays prompts for non-interactive ACPX sessions (`permissionMode`/`nonInteractivePermissions`).
- [snippet_hermes_agent_acp_tools_permission](../../code_snippets/snippet_hermes_agent_acp_tools_permission.md) — ACP tools permission; relevance: analog of approve-reads/approve-all/deny-all harness modes.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: maps to `approvalPolicy: on-request` / `auto_review` Codex fields.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denylist; relevance: `deny` mode + not preserving legacy unsafe Codex overrides.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — code-exec sandbox; relevance: the `workspace-write` vs `danger-full-access` sandbox posture.
- [snippet_hermes_agent_tools_terminal_session](../../code_snippets/snippet_hermes_agent_tools_terminal_session.md) — terminal session exec; relevance: where allowlisted host commands actually run.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: how `exec-policy show` / `approvals get` introspection is produced.
- [snippet_hermes_agent_skills_codex](../../code_snippets/snippet_hermes_agent_skills_codex.md) — Codex harness integration; relevance: the Codex Guardian app-server path mode "auto" maps onto.

### oc_tools_perplexity_search (9t · 10s · 10d)

**Terms**
- [Perplexity](../../term_dictionary/term_perplexity.md) — Perplexity search/answer engine; relevance: the provider this note configures.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: the Sonar path returns synthesized answers with citations (RAG over web).
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — finding relevant documents; relevance: the native Search-API path returns structured `title/url/snippet` IR results.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the Sonar/OpenRouter compatibility path is an LLM chat-completions call.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: Perplexity + OpenRouter are external GenAI services.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — API fronting/aggregation layer; relevance: OpenRouter is a gateway fronting Sonar via `baseUrl`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: `web_search` is the agent tool whose params this note documents.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider integration; relevance: Perplexity installs as a `web_search` provider plugin.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secure credential storage; relevance: the `apiKey` field accepts SecretRef objects; key fail-fast on unresolved ref.

**Docs**
- [oc_tools_searxng_search](oc_tools_searxng_search.md) (planned, this series) — sibling self-hosted provider; relevance: shares `tools.web.search.provider` + auto-detection order (SearXNG is order 200).
- [oc_tools_plugin_install](oc_tools_plugin_install.md) (planned, this series) — plugin install flow; relevance: `openclaw plugins install @openclaw/perplexity-plugin` follows this flow.
- [oc_tools_web](../openclaw/oc_tools_web.md) (planned, to08) — web-search overview + auto-detection; relevance: the providers/auto-detection-rules hub this page links to.
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — Hermes web-search provider plugin; relevance: direct analog of a web_search provider configured via plugin.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — web search + content extraction; relevance: maps to `max_tokens`/`max_tokens_per_page` content-budget params.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: analog of `PERPLEXITY_API_KEY`/`OPENROUTER_API_KEY` env placement.
- [hermes_x_search_grok](../hermes_agent/hermes_x_search_grok.md) — Grok/X web-search provider; relevance: another web_search provider config for contrast.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding an inference provider; relevance: parallels installing+keying a provider plugin.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tools incl. web; relevance: CC web/search tool analog.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — tool execution behavior; relevance: how a built-in tool's params/limits are applied (analog to Search-API-only filters erroring on Sonar).

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: the Perplexity plugin is an extension.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider/key resolution; relevance: provider/key-resolution analog for the apiKey/SecretRef/env chain.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway startup/key loading; relevance: env/SecretRef loading + fail-fast on unresolved key at startup/reload.

**Snippets**
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator routing; relevance: the exact `sk-or-...`/`baseUrl` OpenRouter compatibility path.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider plugin; relevance: analog of the OpenRouter-Sonar config shape.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef/env key resolution; relevance: resolves the `webSearch.apiKey` SecretRef / env fallback.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web_search tool implementation; relevance: the agent-side `web_search({query,count,freshness,...})` call surface.
- [snippet_hermes_agent_cli_tools_policy](../../code_snippets/snippet_hermes_agent_cli_tools_policy.md) — tool policy resolution; relevance: how `tools.web.search.provider` selects the active provider.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider config pattern; relevance: a sibling provider's config-resolution pattern for contrast.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret redaction; relevance: how `pplx-...`/`sk-or-...` keys are redacted in logs.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias lookup; relevance: how `model: "perplexity/sonar-pro"` is resolved on the OpenRouter path.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — auth profiles/key portability; relevance: where/how provider keys are stored and loaded.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — provider credential resolution; relevance: analog of resolving a provider key with env fallback and fail-fast.

### oc_tools_plugin_install (9t · 11s · 10d)

**Terms**
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json` metadata; relevance: native-format plugins ship a manifest (`term_plugin` absent → manifest+sdk cover it).
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — runtime module a plugin loads; relevance: a native plugin = manifest + runtime module loaded in process.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: npm install source + dist-tags + `@latest` compat scanning.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — scoped package names; relevance: `@openclaw/*` bare specs resolve to bundled copies vs `npm:@openclaw/<plugin>`.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: model providers are one plugin category installed this way.
- [Skills](../../term_dictionary/term_skills.md) — agent skills; relevance: skills are a plugin-delivered capability (and compatible bundles carry skills).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent execution harness; relevance: agent harnesses are a plugin category plugins can extend.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP servers are among the runtime capabilities plugins extend.
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: plugins are Node modules; the official image runs as `node` uid 1000.

**Docs**
- [oc_tools_plugin_config](oc_tools_plugin_config.md) (planned, this series) — the config/policy half; relevance: continuation (install policy, `plugins.{allow,deny,...}`, hooks, verify, troubleshoot).
- [oc_clawhub_how_it_works](../openclaw/oc_clawhub_how_it_works.md) (planned, cw01) — ClawHub discovery; relevance: ClawHub is the primary plugin discovery surface referenced in quick start.
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — CC plugins overview; relevance: directly analogous plugin-install/discovery overview.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — CC plugin install sources; relevance: analog of the ClawHub/npm/git/local/marketplace install-source table.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — CC marketplace install; relevance: the `--marketplace` Claude-compatible bundle install path.
- [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — CC plugin CLI; relevance: analog of `openclaw plugins search/install/enable/inspect`.
- [cc_host_and_manage_marketplaces](../claude_code/cc_host_and_manage_marketplaces.md) — hosting/managing marketplaces; relevance: marketplace-source semantics for compatible bundles.
- [hermes_plugins_management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin management; relevance: sibling-ecosystem install/enable/restart flow.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — building a plugin; relevance: the native-plugin authoring side referenced by "Understand plugin formats".
- [pi_packages](../pi/pi_packages.md) — Pi package/plugin install; relevance: a third coding agent's package-install model for cross-tool comparison.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework + load rules; relevance: implements bundled/official/source plugin resolution + formats.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — `openclaw` CLI; relevance: owns the `openclaw plugins ...` command surface used in quick start.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway reload/restart; relevance: install requires a Gateway restart (auto when managed).

**Snippets**
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — install→enable→load lifecycle; relevance: the exact quick-start lifecycle this note documents.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package metadata + compat contract; relevance: `openclaw.compat.pluginApi`/`minHostVersion` compat scanning at install.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — CLI plugin install; relevance: analogous `plugins install` command + source resolution.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — CLI plugin discovery; relevance: analog of `openclaw plugins search` (ClawHub discovery).
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: native `openclaw.plugin.json`-style manifest fields.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the native runtime-module load model.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugin doctor; relevance: `openclaw doctor --fix` for stale plugin state after install.
- [snippet_hermes_agent_cli_plugins_cmd_remove](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_remove.md) — plugin uninstall; relevance: the uninstall side of the lifecycle (requires restart).
- [snippet_hermes_agent_tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy dependency loading; relevance: plugin dependency install/import behavior referenced in troubleshooting.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: "treat plugin installs like running code" — trust check at install.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: how `openclaw plugins <sub>` commands dispatch.

### oc_tools_plugin_config (9t · 10s · 10d)

**Terms**
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest metadata; relevance: `channelConfigs.<id>.preferOver` + manifest default-on/off metadata.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin runtime API; relevance: typed `api.on(...)` hooks are an SDK surface vs internal `api.registerHook`.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: bundled opt-in provider plugins auto-activate when config names a provider/model ref.
- [Skills](../../term_dictionary/term_skills.md) — agent skills; relevance: skills + plugins share the `security.installPolicy` exec schema.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization list; relevance: `plugins.allow`/`deny` precedence is an access-control allow/deny list.
- [Guardrails](../../term_dictionary/term_guardrails.md) — operator safety controls; relevance: `security.installPolicy` is the operator install guardrail.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: plugin-owned tools stay gated by `plugins.allow` even when `tools.allow` is `"*"`.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: uid 1000 ownership repair for bind-mounted plugin roots (blocked-path troubleshooting).
- [SecOps](../../term_dictionary/term_secops.md) — security operations; relevance: operator-owned install policy + blocked-path ownership is a SecOps surface.

**Docs**
- [oc_tools_plugin_install](oc_tools_plugin_install.md) (planned, this series) — the install half; relevance: this note continues from install (formats/sources) into policy/ops.
- [oc_tools_skill_workshop](oc_tools_skill_workshop.md) (planned, this series) — skill governance; relevance: `security.installPolicy` is shared between skills and plugins.
- [oc_automation_hooks](../openclaw/oc_automation_hooks.md) (planned, au01) — internal hook system; relevance: `api.registerHook(...)` participates in the Hooks system documented there.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — CC managed plugin policy; relevance: direct analog of `plugins.{enabled,allow,deny}` operator policy.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — CC plugin security guidance; relevance: analog of install-policy + "treat installs like running code".
- [cc_subagent_and_plugin_settings](../claude_code/cc_subagent_and_plugin_settings.md) — CC plugin/subagent settings; relevance: analog of per-plugin enable/config precedence.
- [cc_marketplace_restrictions](../claude_code/cc_marketplace_restrictions.md) — marketplace restrictions; relevance: analog of allow/deny restricting which plugins may load.
- [hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — Hermes plugin hooks; relevance: typed-vs-internal hook distinction (`api.on` vs `registerHook`).
- [hermes_plugin_hook_reference](../hermes_agent/hermes_plugin_hook_reference.md) — Hermes hook reference; relevance: the lifecycle events (`message:sent`, `command:new`) registerHook reacts to.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Docker run modes/ownership; relevance: uid/ownership context for bind-mounted plugin/config roots.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin policy/load/slots; relevance: implements allow/deny precedence + slot force-enable + auto-activation.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — `security.installPolicy` + ownership; relevance: install-policy exec + blocked-path ownership checks.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — runtime registration/verify; relevance: `gateway status --deep --require-rpc` runtime plugin verification.

**Snippets**
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — config-driven plugin enablement; relevance: how `plugins.{enabled,allow,deny,slots,entries}` resolves at startup.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: live registration proven by `inspect --runtime` vs cold registry.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — blocked-path ownership; relevance: the `suspicious ownership (uid=1000, expected uid=0)` block.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: the diagnostic surfaced before "plugin present but blocked".
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — enable/disable + cold-registry refresh; relevance: enable/disable update config + refresh the cold registry.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/fs policy; relevance: the `security.installPolicy` exec schema shared with skills.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: `preferOver` + default-on/off manifest metadata.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — doctor cleanup; relevance: `openclaw doctor --fix` for stale ids / allowlist-tool mismatches.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK/hook architecture; relevance: typed `api.on` priority/merge/block semantics vs coarse internal hooks.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — denylist enforcement; relevance: `plugins.deny` winning over allow + per-plugin enablement.

### oc_tools_reactions (8t · 11s · 10d)

**Terms**
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: `react` is an action of the `message` agent tool the model invokes.
- [Slack](../../term_dictionary/term_slack.md) — Slack messaging platform; relevance: Discord/Slack reaction-removal semantics (the one channel with a DB term note).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — channel abstraction layer; relevance: per-channel reaction behavior is implemented in the channel kernel.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — message routing gateway; relevance: reactions traverse the messaging gateway per channel transport.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent socket transport; relevance: real-time reaction events ride channel WebSocket transports (Slack socket mode, Telegram).
- [Socket Mode](../../term_dictionary/term_socket_mode.md) — Slack socket-mode transport; relevance: how Slack reaction add/remove events are delivered.
- [Agentic AI](../../term_dictionary/term_agentic_ai.md) — autonomous agent behavior; relevance: reactions (ack/progress) are an agent UX affordance for tool-call progress.

**Docs**
- [oc_tools_agent_send](../openclaw/oc_tools_agent_send.md) (planned, to01) — the `message`/agent-send tool; relevance: owns the `react` action this note documents.
- [oc_channels_slack](../openclaw/oc_channels_slack.md) (planned, ch05) — Slack channel config; relevance: `reactionLevel` + reaction-removal config referenced here.
- [oc_channels_telegram](../openclaw/oc_channels_telegram.md) (planned, ch05) — Telegram channel config; relevance: `channels.telegram.reactionLevel` + reaction-notifications referenced here.
- [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Hermes Slack messaging; relevance: Slack reaction add/remove semantics analog.
- [hermes_telegram_advanced](../hermes_agent/hermes_telegram_advanced.md) — Hermes Telegram advanced; relevance: Telegram reaction/notification config analog.
- [hermes_messaging_signal](../hermes_agent/hermes_messaging_signal.md) — Hermes Signal messaging; relevance: Signal `reactionNotifications` (off/own/all) analog.
- [hermes_discord_advanced](../hermes_agent/hermes_discord_advanced.md) — Hermes Discord advanced; relevance: Discord reaction-removal behavior analog.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging gateway architecture; relevance: how per-channel reaction transport plugs into the gateway.
- [hermes_gateway_feishu_features](../hermes_agent/hermes_gateway_feishu_features.md) — Feishu/Lark features; relevance: the `feishu_reaction` tool (`emoji_type`/`reaction_id`) analog.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — CC channels overview; relevance: cross-tool channel-feature comparison for messaging integrations.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — per-channel transport; relevance: implements per-channel reaction add/remove/tapback behavior.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels + `message` tool; relevance: owns the `react` action across messaging channels.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent tool emission; relevance: the agent that emits the `react` tool call with `trackToolCalls`.

**Snippets**
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/progress reactions + trackToolCalls; relevance: the exact reaction mechanism this note documents.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack platform adapter; relevance: Slack `remove`/empty-emoji reaction-removal implementation analog.
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — Signal platform adapter; relevance: Signal inbound reaction-notification (off/own/all) handling.
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Matrix platform adapter; relevance: another channel adapter's reaction transport for contrast.
- [snippet_hermes_agent_gw_platform_feishu_acl](../../code_snippets/snippet_hermes_agent_gw_platform_feishu_acl.md) — Feishu platform adapter; relevance: the `feishu_reaction` add/remove/list tool path.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — base platform abstraction; relevance: the per-channel capability interface reactions specialize.
- [snippet_slipbot_slack_handlers](../../code_snippets/snippet_slipbot_slack_handlers.md) — Slack event handlers; relevance: handling inbound Slack reaction events.

### oc_tools_searxng_search (8t · 10s · 10d)

**Terms**
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: self-hosted `web_search` feeds retrieval into agent answers.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — meta-search aggregation; relevance: SearXNG aggregates Google/Bing/DuckDuckGo results (classic IR meta-search).
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: `web_search` is the agent tool SearXNG backs.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider; relevance: SearXNG is a `web_search` provider plugin (`plugins.entries.searxng`).
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: `docker run -d -p 8888:8080 searxng/searxng` runs the instance.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secure config storage; relevance: the `baseUrl` field accepts SecretRef objects.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: privacy/air-gap — queries never leave your network (PII-protective).
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side request forgery protection; relevance: public `https://` hosts keep strict SSRF protection; private hosts opt into the network guard.

**Docs**
- [oc_tools_perplexity_search](oc_tools_perplexity_search.md) (planned, this series) — sibling API-backed provider; relevance: shared `tools.web.search.provider` + auto-detection priority (SearXNG order 200, lowest).
- [oc_tools_plugin_install](oc_tools_plugin_install.md) (planned, this series) — provider install flow; relevance: the SearXNG plugin is installed via the plugin flow.
- [oc_tools_web](../openclaw/oc_tools_web.md) (planned, to08) — web-search overview + auto-detection; relevance: the providers/auto-detection hub this page links to.
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — Hermes web-search provider plugin; relevance: direct analog of a self-hosted/keyless web_search provider plugin.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — web search + extraction; relevance: the JSON-API result handling (`format=json`, `img_src`) analog.
- [hermes_docker_run_modes](../hermes_agent/hermes_docker_run_modes.md) — Docker run modes; relevance: running/operating the self-hosted SearXNG container.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation/credentials; relevance: private-network access opt-in + SecretRef `baseUrl` handling.
- [pi_containerization](../pi/pi_containerization.md) — Pi containerization; relevance: self-hosted/air-gapped deployment analog.
- [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tools incl. web; relevance: CC web/search tool analog.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — network isolation; relevance: the private-network guard vs strict web-search guard distinction.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin framework; relevance: the SearXNG plugin/extension lives here.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider config resolution; relevance: provider config-resolution analog for `webSearch.{baseUrl,categories,language}`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — network guard / SSRF protection; relevance: private-vs-public host transport rules + SSRF guard.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef resolution; relevance: resolves the SecretRef `baseUrl` value.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web_search tool impl; relevance: the agent-side `web_search` call SearXNG serves.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider config resolution; relevance: a sibling provider config-resolution path for contrast (API-backed vs keyless).
- [snippet_hermes_agent_cli_tools_policy](../../code_snippets/snippet_hermes_agent_cli_tools_policy.md) — tool/provider policy; relevance: how `tools.web.search.provider: "searxng"` + auto-detection selects the provider.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — security policy resolution; relevance: the network-guard policy layer for private vs public endpoints.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — provider plugin config; relevance: provider-plugin config-entry shape analog.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config assembly; relevance: how plugin `webSearch` config merges into effective runtime config.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker environment setup; relevance: running the `searxng/searxng` container as the instance.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret redaction; relevance: redacting a SecretRef-sourced `baseUrl` in logs.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider config pattern; relevance: contrast — an API-backed provider config that wins over keyless SearXNG in auto-detection.

### oc_tools_skill_workshop (9t · 11s · 10d)

**Terms**
- [Skills](../../term_dictionary/term_skills.md) — agent skills; relevance: Skill Workshop creates/updates workspace `SKILL.md` skills.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — `SKILL.md` frontmatter; relevance: apply writes `SKILL.md` and strips proposal-only fields from `PROPOSAL.md`.
- [Skill Curator](../../term_dictionary/term_skill_curator.md) — skill governance/curation; relevance: Workshop is the governed (proposal-first, scanner-gated) curation path.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated agent context; relevance: authored skills can carry subagent context/support files.
- [Human in the Loop](../../term_dictionary/term_human_in_the_loop.md) — human approval; relevance: approval prompts before agent-initiated apply/reject/quarantine.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization scopes; relevance: Gateway methods require `operator.read`/`operator.admin` scopes.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tools; relevance: `skill_workshop` is a built-in agent tool in `tools.profile: coding`.
- [Guardrails](../../term_dictionary/term_guardrails.md) — safety constraints; relevance: scanner-gated apply + no-clobber + `maxSkillBytes`/`maxPending` are guardrails.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — autonomous multi-step agent flow; relevance: `autonomous.enabled` creates proposals from durable conversation signals.

**Docs**
- [oc_tools_plugin_config](oc_tools_plugin_config.md) (planned, this series) — install policy; relevance: `security.installPolicy` is shared between skills and plugins.
- [oc_tools_skills](../openclaw/oc_tools_skills.md) (planned, to07) — skills load order/precedence/visibility; relevance: the runtime that consumes applied workspace skills.
- [oc_tools_creating_skills](../openclaw/oc_tools_creating_skills.md) (planned, to07) — hand-written `SKILL.md`; relevance: the manual authoring path Workshop governs the proposal-first alternative to.
- [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — CC skill authoring; relevance: direct analog of authoring a `SKILL.md` skill.
- [cc_skills_overview](../claude_code/cc_skills_overview.md) — CC skills overview; relevance: skill load order/precedence analog.
- [cc_sdk_skills](../claude_code/cc_sdk_skills.md) — CC SDK skills; relevance: programmatic skill creation/management analog.
- [cc_skill_dynamic_context_and_subagent](../claude_code/cc_skill_dynamic_context_and_subagent.md) — skill context + subagent; relevance: support-file/subagent-context semantics analog.
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — agent-managed skills hub; relevance: closest analog of an agent governing skill create/update.
- [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — working with skills; relevance: chat/CLI skill lifecycle analog.
- [pi_skills](../pi/pi_skills.md) — Pi workspace skills; relevance: a third coding agent's workspace-skill model for comparison.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — Skill Workshop service; relevance: proposal lifecycle + storage + apply/rollback live here.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — proposal scanner + path rules; relevance: scanner-gated apply + support-file path rejection + symlink-target trust.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — `skills.proposals.*` methods; relevance: the Gateway methods + operator scopes for proposal ops.

**Snippets**
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill scanner; relevance: the scanner that gates apply (reruns scanning before writing).
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — SKILL.md/PROPOSAL.md frontmatter; relevance: the proposal-only-field strip on apply.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability; relevance: how an applied workspace skill becomes available.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill planning; relevance: the runtime planning around applied skills.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — skill tool descriptor; relevance: how `skill_workshop` (and applied skills) expose their tool contract.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — skills guard; relevance: analog of restricting skill writes to the governed tool (no `write`/`edit`/`exec`).
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — skill frontmatter utils; relevance: parsing/writing `name`/`description`/`status`/`version`/`date` proposal frontmatter.
- [snippet_hermes_agent_optional_skills_migration_openclaw](../../code_snippets/snippet_hermes_agent_optional_skills_migration_openclaw.md) — OpenClaw skill migration; relevance: workspace-skill handling in the OpenClaw/Hermes ecosystem.
- [snippet_hermes_agent_skills_canonical_loading_runtime](../../code_snippets/snippet_hermes_agent_skills_canonical_loading_runtime.md) — canonical skill loading; relevance: how an applied `SKILL.md` is loaded into the runtime.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — install/enable lifecycle; relevance: the apply-writes-rollback-metadata-then-changes-live-files pattern parallels plugin enable.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — fs policy; relevance: the support-file path rules (no absolute/traversal/hidden/symlink) + `security.installPolicy` shared with plugins.

## Undigested Terms Plan

Per master: OpenClaw tool/provider/policy vocabulary is digested as `oc_*` doc content, NOT promoted to `term_dictionary`.
Existing terms are linked, never redefined. **Expected 0 new `term_dictionary` captures.** Augment re-runs the Step 2d scan.

| Term (appears in source) | Disposition |
|---|---|
| permission mode / exec mode (deny/allowlist/ask/auto/full) | Digest inline in `oc_tools_permission_modes` (OpenClaw-specific policy surface); link `term_access_control`, `term_guardrails`, `term_sandbox`. No new term. |
| Codex Guardian / approval review | Digest inline (note 2); link `term_autonomous_coding_agents`, `term_human_in_the_loop`. `term_codex` absent — document inline, do NOT create (provider/runtime name, owned by codex-harness Phase C). |
| ACPX / ACPX harness permissions | Digest inline (note 2); link `term_acp_agent_client_protocol`. No new term. |
| native PDF provider / extraction fallback / clawpdf / PDFium | Digest inline in `oc_tools_pdf`; link `term_multimodal`, `term_vlm`, `term_ocr`. Tool-internal names, not reusable terms. |
| web_search provider / Perplexity Search API / Sonar | Digest inline (notes 3/7); link `term_perplexity` (exists), `term_rag`, `term_provider_plugin`. `term_searxng` absent — document inline (provider name). |
| SearXNG / meta-search | Digest inline (note 7); link `term_docker`, `term_pii`. Self-hosted product name, not a reusable abstract term. |
| plugin / ClawHub / install source / plugin format / bundle | Digest inline (notes 4/5); link `term_plugin_manifest`, `term_plugin_sdk`, `term_npm`, `term_provider_plugin`. `term_plugin` absent — `term_plugin_manifest`/`term_plugin_sdk` cover it; do NOT create a too-general `term_plugin`. |
| security.installPolicy / plugins.allow/deny/slots | Digest inline (note 5); link `term_access_control`, `term_guardrails`. Config keys, not terms. |
| reaction / reactionLevel / tapback / trackToolCalls | Digest inline in `oc_tools_reactions`; `term_emoji_reaction` absent — document inline (channel-feature behavior, not a cross-cutting reusable term). Do NOT create. |
| Skill Workshop / proposal / PROPOSAL.md / quarantine | Digest inline in `oc_tools_skill_workshop`; link `term_skills`, `term_guardrails`, `term_human_in_the_loop`. Product feature name, not a new term. |

**New-term candidates: NONE.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note.
All candidate terms are either (a) existing (linked) or (b) OpenClaw-specific product/config names digested inline as `oc_*` content.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from master).
If augment's Step 2d re-scan surfaces a genuinely reusable cross-cutting term with no existing note and no doc-page home, capture
it via `/tessellum-capture-term-note` + add to the best-fit `acronym_glossary_*.md` (master W5) — not expected here.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` — YAML field order, required H2 (`## Overview`, `## Related Notes`), footer. |
| G2 | Grounding | Diff each note against `inbox/openclaw_docs/tools/<page>.md` — every claim traceable to source; config/CLI blocks verbatim. |
| G3 | Density + Coverage | ≤400 lines · ≤2,500 words · ≤6 code blocks · single building_block per note; every mapped H2/H3 covered (no omission). |
| G4 | Cross-Reference | **≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs** + relevant `repo_openclaw*`/sibling `oc_*` per note, each with a relevance statement (LOCKED at xref-augment 2026-06-21; see `## Per-Note Related Notes Mapping`). |
| G6 | Broken-link | `/tessellum-fix-broken-links` — 0 broken relative paths after reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island). |
| G8 | In-degree ≥1 | Confirmed via `note_links` after reindex; satisfied via `entry_openclaw_docs.md` + repo/term inlinks. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
NOTES="oc_tools_pdf oc_tools_permission_modes oc_tools_perplexity_search oc_tools_plugin_install oc_tools_plugin_config oc_tools_reactions oc_tools_searxng_search oc_tools_skill_workshop"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then grep -qE '^source_url:\s*https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"; fi
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # at least one sibling oc_ link present (G4 sanity)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING $SIBLING_PREFIX LINK in $n"
done

# YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference: confirm every cited EXISTING target resolves (run after draft)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
grep -rhoE '\]\(\.\./\.\./?[A-Za-z0-9_./-]+\.md\)' "$GATE_DIR" | sed -E 's/.*\/([a-z0-9_]+)\.md\)/\1/' | sort -u | while read stem; do
  case "$stem" in oc_*) continue;; esac  # siblings are (planned)
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6cb / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_tools_pdf | procedure | 650 | 4–5 | yes |
| 2 | oc_tools_permission_modes | procedure | 600 | 3–4 | yes |
| 3 | oc_tools_perplexity_search | procedure | 600 | 3–4 | yes |
| 4 | oc_tools_plugin_install | procedure | 600 | 5–6 | yes |
| 5 | oc_tools_plugin_config | procedure | 700 | 4–5 | yes |
| 6 | oc_tools_reactions | procedure | 450 | 1–2 | yes |
| 7 | oc_tools_searxng_search | procedure | 500 | 4–5 | yes |
| 8 | oc_tools_skill_workshop | procedure | 700 | 5–6 | yes |

No note approaches caps. The two code-dense pages (skill-workshop 15 fences; plugin 12 fences) are kept ≤6 each — skill-workshop
by selecting the load-bearing lifecycle/CLI/config/storage blocks; plugin by the install↔config split.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under the **Tools** section. Each new note
receives its entry-point back-link at finalization (satisfies G7/G8). No new entry point is created by this sub-plan; the master's
`entry_openclaw_docs.md` is the single docs hub. W2/W3 (parent-hub + code↔docs cross-links) are master-level steps.

## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` → all 8 notes (primary anti-island guarantee).
- `repo_openclaw_extensions.md` → notes 3, 4, 5, 7 (plugin/provider framework ↔ install/config/search-provider docs).
- `repo_openclaw_skills.md` → note 8 (Skill Workshop service ↔ doc).
- `repo_openclaw_security.md` → notes 2, 5, 8 (exec policy / install policy / skill scanner).
- `repo_openclaw_gateway.md` → notes 2, 4, 5, 8 (exec routing / Gateway reload / proposal methods).
- `repo_openclaw_agents.md` → notes 1, 6 (pdf model resolution / agent react action).
- `repo_openclaw_channels_messaging.md` → note 6 (the `message` tool `react` action).
- `term_perplexity.md` → note 3; `term_skills.md` → note 8; `term_plugin_manifest.md` / `term_plugin_sdk.md` → notes 4, 5;
  `term_sandbox.md` → notes 1, 2; `term_access_control.md` → notes 2, 5, 8 (reciprocal term backlinks).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each source page during execution; reproduce config/CLI blocks verbatim;
one building_block per note. Cap dynamic-workflow fan-out at ~30 agents/run (8 notes is well under). Incremental reindex per wave;
verify `note_links` + 0 broken links before commit. `git pull --rebase --autostash` first; commit+push after the phase; no Claude
co-author trailer.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note Related Notes LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Skill:** `/tessellum-augment-digestion-plan` (xref-augment pass — per-note Related Notes mapping at raised floors).

**What was locked.** Replaced the candidate-pool `## Candidate Cross-References` with `## Per-Note Related Notes Mapping
(LOCKED — xref-augment 2026-06-21)`. Standard raised from the plan-stage ≥6-terms candidate pool to **≥8 `term_dictionary`
terms · ≥10 `code_snippets` · ≥10 docs per note**, plus relevant `repo_openclaw*` (3 per note) and sibling `oc_*` (planned).
false-positives from BM25 (e.g. `term_document_verification`, `term_concession_leakage`, `term_protected_account_types`,
`term_auto_labeling`) were discarded. Each link is rendered as `[Name](relpath.md) — what it is; relevance: why THIS note`.

'%/<stem>.md'"`. Programmatic sweep of the LOCKED section: **238 EXISTING xref links resolved OK, 16 planned `oc_*`
its planned `oc_*` siblings.

**Per-note locked counts (terms / snippets / docs / repos · floors met):**

| Note | Terms | Snippets | Docs | Repos | ≥8t·≥10s·≥10d |
|---|---:|---:|---:|---:|:--:|
| oc_tools_pdf | 10 | 10 | 10 | 3 | ✅ |
| oc_tools_permission_modes | 10 | 10 | 10 | 3 | ✅ |
| oc_tools_perplexity_search | 9 | 10 | 10 | 3 | ✅ |
| oc_tools_plugin_install | 9 | 11 | 10 | 3 | ✅ |
| oc_tools_plugin_config | 9 | 10 | 10 | 3 | ✅ |
| oc_tools_reactions | 8 | 11 | 10 | 3 | ✅ |
| oc_tools_searxng_search | 8 | 10 | 10 | 3 | ✅ |
| oc_tools_skill_workshop | 9 | 11 | 10 | 3 | ✅ |

**New-term candidates + best-fit glossary.** **NONE.** The Step 2d re-scan over all 7 re-read pages surfaced no genuinely
cross-cutting, vault-reusable term lacking BOTH a doc-page home AND an existing note. Every source vocabulary item is either
(a) an existing linked term (`term_perplexity`, `term_skills`, `term_plugin_manifest`, `term_plugin_sdk`, `term_npm`,
`term_sandbox`, `term_access_control`, `term_guardrails`, `term_acp_agent_client_protocol`, `term_human_in_the_loop`,
`term_autonomous_coding_agents`, `term_rag`, `term_provider_plugin`, `term_secrets_manager`, `term_ssrf_guard`, `term_pii`,
`term_docker`, …) or (b) an OpenClaw-specific product/config name (`term_codex`, `term_searxng`, `term_plugin`,
`term_emoji_reaction` — all absent) digested inline as `oc_*` content per the master's corpus-wide ownership decision. No
`acronym_glossary_*.md` change is required for this sub-plan.

**CP7 source re-measure (body words, frontmatter excluded):** pdf 843 (plan 890), permission-modes 655 (701),
perplexity 703 (735), plugin 2353 (2388), reactions 460 (488), searxng 539 (579), skill-workshop 1123 (1179). All within
±10% of the plan's Source table — no under-estimation; no re-split required.

**Issues / notes.** (1) Floors raised this pass exceed the master's plan-stage ≥6-term floor and the inline G4 wording — G4
in the Per-Phase gate table was updated to the raised standard. (2) `entry_openclaw_docs.md` is correctly NOT yet in the DB
(planned at master pre-step W1); the 8 entry-point back-links + repo/term reciprocal inlinks (G7/G8) are executed at
finalization. (3) No source section is orphaned; the Section Coverage Map remains complete.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|:--:|---|
| CP1 | Related Notes step (≥8 terms + raised floors, each with relevance statement) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 8 notes ≥8 terms / ≥10 snippets / ≥10 docs (table above); every link carries `— desc; relevance: …`. |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table has G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (raised), G5 ghost-detect, G6 broken-link, G7 discoverability, G8 in-degree≥1. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` + `## Inlinks`: 8 rows into `entry_openclaw_docs.md` (master W1 pre-step); no per-sub-plan entry point created. Confirmed entry not yet in DB (planned). |
| CP4 | Size | **PASS** | 8 planned notes (≤30); single execution phase. |
| CP5 | Format derived (not invented) | **PASS** | Master Format Definition derived from `claude_code/`+`pi/` corpora; confirmed `cc_permission_modes_overview.md` uses `## Overview` / `## Related Notes` + `building_block` + same forbidden-field list. |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment`: all 8 notes 450–700w, ≤6 code blocks, ≤400 lines; plugin (2353w source) already split install↔config; skill-workshop (15 fences) trimmed to ≤6. None borderline. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured all 7 pages this pass; every page within ±10% of the plan's Source table (pdf 843/890 … plugin 2353/2388 … skill-workshop 1123/1179). No page >1.5× estimate. |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (10 rows, all dispositioned inline, **0 new terms**); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, with capture fallback specified). |
| CP8f | Slug specificity / collision dedup | **PASS** | 0 new term slugs to audit (Pattern B: vocabulary digested as `oc_*` doc content). All-notes collision check: the 8 planned `oc_tools_*` doc slugs do not duplicate existing `term_*` or `documentation/` notes (existing OpenClaw notes are CODE-side `repo_*`/`snippet_*`, distinct from these product-doc pages — linked, not recreated). 0 doc-note-vs-term duplicates. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks` maps every new note to ≥1 outside-folder inbound link (entry_openclaw_docs + repo_openclaw* + reciprocal term backlinks); G7/G8 in the gate table; inlink addition is a gated finalization phase, not "recommended". |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan `status` advanced `pending → ready`.
