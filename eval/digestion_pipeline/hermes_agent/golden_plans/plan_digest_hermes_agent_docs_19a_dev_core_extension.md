---
title: Hermes Agent Docs Digestion — Sub-Plan 19a — Developer: Core Extension
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/
pages:
  - developer-guide/adding-tools.md
  - developer-guide/adding-providers.md
  - developer-guide/adding-platform-adapters.md
  - developer-guide/creating-skills.md
  - developer-guide/extending-the-cli.md
  - developer-guide/contributing.md
  - developer-guide/programmatic-integration.md
---

# Sub-Plan 19a: Developer: Core Extension

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP19a's note
> filenames/BBs/coverage are defined. **Part `a` of the SP19 split** (SP19b owns the five
> `*-provider-plugin` pages + `context-engine-plugin` + `model-provider-plugin`); SP19a owns the
> seven *core-extension* developer pages below.

## Scope

How to extend Hermes Agent's core: author a built-in tool, wire a new inference provider, build a
messaging platform adapter (plugin path + built-in path), create a skill (SKILL.md format,
conditional activation, blueprints, publishing), extend the TUI via wrapper-CLI hooks, drive Hermes
from external programs (ACP / TUI-gateway JSON-RPC / OpenAI-compatible HTTP), and contribute to the
repo (dev setup, cross-platform rules, security, PR process). Source = **7 mirrored pages** in
`inbox/hermes_agent_docs/developer-guide/` (all substantive). **P3 / developer** — these pages are
the *authoring procedures* on top of the existing code-digestion notes (`snippet_hermes_agent_*`,
`repo_hermes_agent_*`) and the concept terms (`term_provider_plugin`, `term_skill_manifest`,
`term_acp`). Concepts already captured as term notes are **linked, not recreated**.

## Content Strategy

- **One BB per note.** Every SP19a page is a developer how-to → **procedure** (programmatic-integration
  leans model — protocol comparison — but the page's body is a "pick + drive" procedure, kept procedure).
  Two pages exceed density caps and SPLIT (see Split Decisions): `adding-platform-adapters.md` (3454w,
  20 code) → 2; `creating-skills.md` (2753w, 21 code) → 2.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content:
  the plugin *system* concept (SP06b `plugins`/`term_hermes_plugin`), the five `*-provider-plugin`
  authoring pages + `model-provider-plugin` (SP19b), provider *runtime/internals* (SP18
  `provider-runtime`, SP09 protocols/providers), the skills *feature* page + curator + skills-hub
  (SP05), MCP/ACP/api-server *features* (SP09), the messaging *platform setup* pages (SP11-13),
  tool *config* + toolsets (SP02 config, SP21 reference), cron *feature* + delegation (SP06).
- **Collision (augment): no existing term OR documentation note covers these authoring procedures.**
  `term_channel_adapter.md` (67L, active) is an Amazon-CS multi-channel transformation layer (LIKE
  false-positive) — UNRELATED to a Hermes messaging platform adapter; the planned
  `hermes_adding_platform_adapter_plugin` is NOT a duplicate. `term_plugin_sdk.md` (84L, active) is
  the **OpenClaw TypeScript** plugin SDK — a different system; LINK only where contrasting, do not
  treat as the Hermes plugin concept. `term_provider_plugin`, `term_skill_manifest`, `term_acp` are
  substantive existing concept terms → **LINK, do not recreate.**

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| developer-guide/adding-platform-adapters.md | 3454 | 20 | procedure | 2 (split) |
| developer-guide/creating-skills.md | 2753 | 21 | procedure | 2 (split) |
| developer-guide/adding-providers.md | 2193 | 6 | procedure | 1 |
| developer-guide/contributing.md | 1316 | 13 | procedure | 1 |
| developer-guide/programmatic-integration.md | 809 | 3 | procedure (protocol picker) | 1 |
| developer-guide/adding-tools.md | 796 | 5 | procedure | 1 |
| developer-guide/extending-the-cli.md | 767 | 8 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **9 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_adding_built_in_tool.md` | procedure | adding-tools §Overview, §Step 1 Create the Tool File (+Key Rules), §Step 2 Add to Toolset, §Async Handlers, §Handlers That Need task_id, §Agent-Loop Intercepted Tools, §Setup Wizard Integration, §Checklist | ~900 | Authoring a built-in core tool: the 2-file touch (`tools/your_tool.py` + `toolsets.py`), the handler/schema/check_fn/`registry.register()` structure, JSON-string return + `{"error":...}` rules, auto-discovery, async + `task_id` handlers, agent-loop-intercepted tools, and `OPTIONAL_ENV_VARS` wizard integration. Leads with "skill vs tool" decision. |
| 2 | `hermes_adding_inference_provider.md` | procedure | adding-providers §mental model, §Choose path (A OpenAI-compatible / B native), §File checklist, §Fast path (plugin), §Full path, §Steps 1-10 (id/auth/models/runtime/CLI/aux/native-adapter/tests/verify/docs), §checklists, §Common pitfalls, §Search targets | ~1500 | Wiring a built-in inference provider across the auth → runtime → CLI → aux layers: canonical provider id, `PROVIDER_REGISTRY` auth, model catalog + `provider:model` aliases, `resolve_runtime_provider()` branch + `api_mode`, `hermes model` menu, aux defaults + context lengths, native adapter + `run_agent.py` branches, tests/smoke, fast-path plugin shortcut, and the 7 common pitfalls. |
| 3 | `hermes_adding_platform_adapter_plugin.md` | procedure | adapters §Architecture Overview, §Plugin Path (plugin.yaml, adapter.py, register, Configuration), §What the Plugin System Handles Automatically, §Env-Driven Auto-Config, §YAML→env Config Bridge, §Cron Delivery (+out-of-process standalone_sender_fn), §Surfacing Env Vars, §Platform-Specific Slow-LLM UX (keep_typing/send overrides), §Reference Implementations | ~1700 | The recommended plugin path for a messaging platform adapter: the `BasePlatformAdapter` contract (connect/disconnect/send/handle_message), the `plugin.yaml`+`adapter.py` two-file plugin, `ctx.register_platform()` and the ~20 integration points it wires automatically, env-driven auto-config + YAML→env bridge, cron `deliver=` + out-of-process `standalone_sender_fn`, `hermes config` env surfacing, and the slow-LLM `_keep_typing`/`send` override patterns (LINE postback). |
| 4 | `hermes_adding_platform_adapter_builtin.md` | procedure | adapters §Step-by-Step Checklist (Built-in Path) Steps 1-11 (enum, adapter file, gateway config, runner, cross-platform delivery, CLI integration, tools, toolsets, platform hints, tests, docs), §Parity Audit, §Common Patterns (long-poll, callback/webhook, token locks), §Reference Implementations | ~1500 | The built-in (core-contributor) path for a platform adapter — the 20+-file checklist: `Platform` enum, `gateway/platforms/<p>.py`, the gateway-config/runner touchpoints, cross-platform delivery (webhook + cron), CLI integration (config/gateway/setup/status), tools + toolsets, prompt-builder `_PLATFORM_HINTS`, tests + the 8-file doc set; plus the parity audit, long-poll/callback/token-lock patterns, and reference adapters. |
| 5 | `hermes_creating_skill_format.md` | procedure | creating-skills §Should it be a Skill or a Tool, §Skill Directory Structure, §SKILL.md Format, §Platform-Specific Skills, §Conditional Skill Activation, §Environment Variable Requirements, §Secure Setup on Load, §Config Settings, §Credential File Requirements | ~1500 | Authoring a skill: the skill-vs-tool decision, the `skills/<category>/<name>/SKILL.md`+`scripts/` layout, the SKILL.md frontmatter (name/description/version/`metadata.hermes` tags/`platforms`/conditional `requires_*`/`fallback_for_*`/`config`/`required_environment_variables`/`required_credential_files`), secure on-load secret prompting + sandbox passthrough, and config.yaml `skills.config` settings. |
| 6 | `hermes_creating_skill_publish.md` | procedure | creating-skills §Skill Guidelines (No deps, Progressive Disclosure, Helper Scripts, as_document, template tokens, inline shell, Test It), §Where Should the Skill Live, §Blueprints, §Suggested Cron Jobs, §Publishing Skills, §Security Scanning | ~1200 | Skill authoring guidelines + lifecycle: the guideline set (stdlib-only, progressive disclosure, helper scripts, `[[as_document]]` media, `${HERMES_SKILL_DIR}`/`${HERMES_SESSION_ID}` tokens, opt-in inline shell), where a skill lives (bundled vs optional vs hub), blueprints (schedule-in-frontmatter automations + `/suggestions`), Suggested Cron Jobs surface, publishing/tap, and the trust-level security scanner. |
| 7 | `hermes_extending_cli_wrapper.md` | procedure | extending-the-cli §Extension points (5 seams), §Quick start wrapper CLI, §Hook reference (`_get_extra_tui_widgets`, `_register_extra_tui_keybindings`, `_build_tui_layout_children`), §Layout diagram, §Tips | ~750 | Building a wrapper CLI on `HermesCLI` without overriding `run()`: the five protected extension seams (extra TUI widgets, extra keybindings, layout-children override, `process_command`, style dict), a working `MyCLI` example, per-hook reference + keybinding-conflict list, the top-to-bottom layout diagram, and `_invalidate()`/`self.agent` tips. |
| 8 | `hermes_programmatic_integration.md` | procedure | programmatic-integration §three-protocol table, §ACP, §TUI Gateway JSON-RPC (method catalog, events, Pi-style mapping), §OpenAI-Compatible API Server, §Which one should I use, §Model hot-swapping, §note on --mode rpc | ~800 | Driving Hermes from external programs: the three protocols (ACP over stdio JSON-RPC for IDEs, the TUI-gateway JSON-RPC for full-feature hosts, the OpenAI-compatible HTTP+SSE API server), their method/endpoint catalogs + event streams, the Pi-style RPC mapping, the "which one" decision (incl. in-process `AIAgent` embed), cross-surface `/model` hot-swap, and why there is no `--mode rpc`. |
| 9 | `hermes_contributing_dev_setup.md` | procedure | contributing §Contribution Priorities, §Common contribution paths, §Development Setup (prereqs, clone/install, configure, run, tests), §Code Style, §Cross-Platform Compatibility (4 patterns), §Security Considerations, §Pull Request Process (branch/commit/conventional), §Reporting Issues, §Community, §License | ~1100 | Contributing to Hermes: contribution priorities + the "which extension path" router, dev setup (`uv venv`, `.[all,dev]`, config + `.env`, symlink, `hermes doctor`), code style + profile-safe paths (`get_hermes_home()`), the cross-platform rules (SIGKILL/OSError/`setsid`/encoding/`pathlib` + termios/fcntl fallback), security protections + sensitive-code rules (`shlex.quote`, realpath), and the Conventional-Commits PR process. |

**SP19a totals:** 9 notes · procedure 9 · concept 0 (concepts owned by existing term notes / other SPs).
7 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 9 · procedure 9 · concept 0 (plugin/provider/skill/ACP concepts are existing term notes or owned by SP06b/SP19b).
- Source: 7 digested pages (~11.9K words) → ~10.9K words of notes (modest compression via link-outs to feature/internals/reference SPs).
- BB mix: procedure 100% (developer how-to family).

## Section Coverage Map

```
adding-tools.md (796w)
├── intro (skill-vs-tool warning) / Make it a Skill / Make it a Tool → Note 1
├── Overview (2 files) / Step 1 Create File (+Key Rules) / Step 2 Toolset / ~~Step 3~~ → Note 1
├── Async Handlers / Handlers That Need task_id / Agent-Loop Intercepted Tools → Note 1 (intercept detail→SP18 agent-loop)
└── Optional Setup Wizard Integration / Checklist ──────────── → Note 1 (OPTIONAL_ENV_VARS→SP21 env-vars ref)
adding-providers.md (2193w)
├── intro / mental model / api_mode abstraction ──────────── → Note 2 (runtime resolution detail→SP18 provider-runtime)
├── Choose path (A/B) / File checklist / Fast path (plugin) → Note 2 (plugin field ref→SP19b model-provider-plugin)
├── Full path / Steps 1-10 (id/auth/models/runtime/CLI/aux/native/tests/verify/docs) → Note 2 (provider catalog→SP14)
└── checklists / Common pitfalls / Good search targets / Related docs → Note 2
adding-platform-adapters.md (3454w)
├── intro (two ways) / Architecture Overview / Plugin Path (plugin.yaml, adapter.py, register, Config) → Note 3
├── What the Plugin System Handles Automatically (table) / Env-Driven Auto-Config / YAML→env Bridge → Note 3
├── Cron Delivery (+out-of-process standalone_sender_fn) / Surfacing Env Vars in hermes config → Note 3 (cron feature→SP06)
├── Platform-Specific Slow-LLM UX (_keep_typing / send overrides / when) / Reference Impls (plugin) → Note 3 (platform setup→SP11-13)
├── Step-by-Step Checklist (Built-in) Steps 1-11 (enum/adapter/config/runner/delivery/CLI/tools/toolsets/hints/tests/docs) → Note 4
├── Parity Audit ──────────────────────────────────────────── → Note 4
└── Common Patterns (long-poll/callback/token-lock) / Reference Implementations (table) → Note 4 (gateway internals→SP18)
creating-skills.md (2753w)
├── intro / Should it be a Skill or a Tool ────────────────── → Note 5 (skills feature→SP05)
├── Skill Directory Structure / SKILL.md Format / Platform-Specific Skills → Note 5
├── Conditional Skill Activation / Env Var Requirements / Secure Setup on Load / Config Settings / Credential Files → Note 5 (sandbox passthrough→SP03 security)
├── Skill Guidelines (deps/progressive-disclosure/helper-scripts/as_document/tokens/inline-shell/Test It) → Note 6
├── Where Should the Skill Live / Blueprints / Suggested Cron Jobs → Note 6 (cron→SP06; curator/hub→SP05)
└── Publishing Skills / Security Scanning ─────────────────── → Note 6 (skills-guard impl→snippet; hub→SP05)
extending-the-cli.md (767w) ── ALL sections ─────────────────── → Note 7 (TUI usage→SP02 tui; dashboard→SP10)
programmatic-integration.md (809w) ── ALL sections ──────────── → Note 8 (acp/api-server/tui-gateway features→SP09/SP10/SP02; internals→SP18)
contributing.md (1316w) ── ALL sections ─────────────────────── → Note 9 (install→SP01; security feature→SP03)
```

No source H2/H3 orphaned. All 7 pages fully covered; feature/internals/reference detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| adding-platform-adapters.md (3454w, 20 code) | Note 3 (plugin path) + Note 4 (built-in path) | >2500w, 20 code blocks; two self-contained authoring arcs — the recommended plugin path (drop-in directory, `register_platform`, env/yaml/cron/slow-LLM hooks) vs the 20+-file built-in core path (enum→runner→CLI→tools→docs + parity audit). Each cluster keeps ≤6 curated code blocks. |
| creating-skills.md (2753w, 21 code) | Note 5 (SKILL.md format) + Note 6 (guidelines + publish) | >2500w, 21 code blocks; separates the *declarative spec* (directory + frontmatter + conditional activation + env/config/credential declarations) from the *authoring lifecycle* (guidelines, where it lives, blueprints, Suggested Cron Jobs, publishing, security scanning). |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_adding_platform_adapter_plugin`, `hermes_adding_platform_adapter_builtin` | `term_channel_adapter.md` (67L active), `term_adapter_pattern.md` (active) | **NOT a dup** — `term_channel_adapter` is an Amazon-CS chat/voice/touch transformation layer (LIKE false-positive); `term_adapter_pattern` is the generic GoF pattern. Neither covers authoring a Hermes messaging-platform adapter. | CREATE; LINK `term_adapter_pattern`/`term_channel_adapter`(contrast)/`term_messaging_gateway`(+fin SP11). |
| `hermes_adding_inference_provider` | `term_provider_plugin.md` (active), `term_plugin_sdk.md` (84L active OpenClaw TS SDK) | **NOT a dup** — `term_provider_plugin` is the concept; this is the built-in-provider wiring *procedure*. `term_plugin_sdk` is a different (OpenClaw TypeScript) system. | CREATE; LINK `term_provider_plugin`; LINK `term_plugin_sdk` only as cross-system contrast. |
| `hermes_creating_skill_format`, `hermes_creating_skill_publish` | `term_skill_manifest.md` (active), `term_skills.md` (active) | **NOT a dup** — those are the concept terms; these are the authoring procedure + lifecycle. Skills *feature* page is SP05, not here. | CREATE; LINK `term_skill_manifest`/`term_skills`. |
| `hermes_programmatic_integration` | `term_acp.md` (active), `term_json_rpc.md`, `term_rest`, `term_openai_responses_api` (active) | **NOT a dup** — those are component protocol concepts the note uses. ACP/api-server *features* are SP09. | CREATE; LINK all four. |
| `hermes_adding_built_in_tool` | `term_function_calling.md`, `term_json_rpc.md`, `term_strategy_pattern.md` (active) | **NOT a dup** — component concepts; tool *config*/toolsets are SP02/SP21. | CREATE; LINK the component terms. |
| `hermes_extending_cli_wrapper` | `term_oop_inheritance.md`, `term_template_method_pattern`(via factory/strategy) | **NOT a dup** — generic OOP terms the note uses (subclass-hook = template-method/inheritance). TUI *usage* is SP02. | CREATE; LINK `term_oop_inheritance`/`term_oop_polymorphism`. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords; **0 substantive same-concept duplicates** (the LIKE hits — `term_channel_adapter`, `term_plugin_sdk`, `term_adapter_pattern` — are confirmed-different by reading the notes). New `hermes_agent/` folder → no doc-doc collisions (SP18/19b not yet executed; intra-series doc links resolve at finalization, verified by G5/G8).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Four-floor standard set 2026-06-19 (user directive — supersedes BOTH the 2026-06-14 floor of ≥8 term + ≥8
> snippet + ≥5 doc AND the interim 2026-06-19 partial-run floor of ≥8 term + ≥5 code-repo + ≥10 doc with snippets
> as a bonus).** Snippets are NO LONGER a bonus group — they are now a COUNTED floor raised to ≥10. Each note's
> `## Related Notes` now carries FOUR counted groups, all relevancy-selected to that note's actual content and each
> rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   `repo_hermes_agent_*` notes that digest the Hermes SOURCE CODE; each note lists the repos whose modules
>   implement what THIS doc note documents.
>   517-note Hermes implementation corpus; each note picks the ≥10 whose CODE it documents (the code paths the page
>   drives). This is a COUNTED floor, promoted from the prior bonus group and raised from the old ≥8.
> - **≥10 DOCUMENTATION notes** (sibling `hermes_*` in this series, which resolve at finalization per G5/G8 +
>
> snippet IDs shown without the `snippet_hermes_agent_` prefix, the master/SP02 convention). Intra-series doc
> links (sibling `hermes_*`) resolve at finalization (G5/G8). New Hermes-specific terms owned by other SPs
> (e.g. `term_hermes_plugin`→SP06b, `term_messaging_gateway`→SP11, `term_provider_routing`/
> `term_fallback_provider`→SP09) are ADDITIONAL forward-refs marked `[own]` in `(+fin …)`, EXCLUDED from the
> ≥8 term floor (they don't exist yet).

**Note 1 `hermes_adding_built_in_tool`**
- Terms (8): term_function_calling, term_json_rpc, term_strategy_pattern, term_factory_method, term_skill_manifest, term_autonomous_coding_agents, term_agent_harness, term_sandbox_backend — relevance: a tool is a JSON-schema function-call handler registered (factory/strategy dispatch) into the agent harness; the JSON-string return contract is JSON-RPC-shaped; the skill-vs-tool decision points at the skill manifest; aux tools run in the sandbox. (+fin: term_code_execution_tool [own], term_delegate_task [own])
- Code-Repos (5): repo_hermes_agent_tools — the `tools/` package this page edits (handler/schema/check_fn/`registry.register()`); repo_hermes_agent_mcp_toolsets — `toolsets.py` + `_HERMES_CORE_TOOLS` the Step-2 add lands in; repo_hermes_agent_agent_core — `run_agent.py` agent-loop interception of `todo`/`memory`/`delegate_task`; repo_hermes_agent_cli — `hermes_cli/config.py` `OPTIONAL_ENV_VARS` wizard integration; repo_hermes_agent — top-level repo doc anchoring the 2-file-touch + auto-discovery contract.
- Snippets (10): tools_registry, toolsets_definitions, toolsets_materialize, toolset_distributions, tools_schema_sanitizer, tools_lazy_deps, tools_send_dispatch, tools_skill_manager, core_tool_dispatch_helpers, core_tool_guardrails_schema — relevance: the registry `register()`/`discover_builtin_tools()` auto-discovery, toolset definitions + materialization + distributions, JSON-schema sanitizing, the `check_fn`/`requires_env` lazy-dep gate, the dispatch path (JSON-string-or-`{"error":...}`), the skill-manager (skill-vs-tool boundary), and the agent-loop tool-dispatch + guardrail-schema code this page drives.
- Docs (10): hermes_creating_skill_format, hermes_adding_inference_provider, hermes_contributing_dev_setup, hermes_adding_platform_adapter_plugin, hermes_programmatic_integration, hermes_adding_platform_adapter_builtin, hermes_creating_skill_publish, hermes_extending_cli_wrapper [sibling hermes_* — resolve at finalization], cc_sdk_custom_tool_definition [the analogous Claude-Code SDK custom-tool definition procedure], cc_built_in_tools [Claude-Code built-in tool catalog — the parallel "what a tool is" reference].

**Note 2 `hermes_adding_inference_provider`**
- Terms (8): term_provider_plugin, term_model_catalog, term_llm, term_oauth_token, term_authentication, term_openai_responses_api, term_converse_api, term_abstract_factory — relevance: wiring a provider spans auth/OAuth (Nous/Codex/Gemini token refresh), the model catalog + `provider:model` aliases, and the `api_mode` adapter family (chat_completions/anthropic_messages/codex_responses — an abstract-factory over request shapes); aux + token budgeting. (+fin: term_provider_routing [own], term_fallback_provider [own], term_nous_portal [own])
- Code-Repos (5): repo_hermes_agent_providers_adapters — the `agent/<provider>_adapter.py` + `run_agent.py` `api_mode` branches the native (Path B) provider adds; repo_hermes_agent_cli — `hermes_cli/{auth,models,runtime_provider,main}.py` the 10-step checklist edits; repo_hermes_agent_plugins — `plugins/model-providers/` fast-path plugin shortcut (`register_provider`); repo_hermes_agent_agent_core — `agent/{auxiliary_client,model_metadata}.py` aux defaults + context lengths; repo_hermes_agent — top-level repo anchoring the auth→runtime→CLI→aux layer line-up.
- Snippets (10): cli_providers_registry, cli_auth_resolve_provider, cli_main_provider_flows, cli_model_switch_entry, cli_model_catalog, core_agent_init_api_mode_resolution, core_auxiliary_auth_resolution, core_error_classifier_provider_maps, plugins_provider_registry, plugins_provider_custom — relevance: the `PROVIDER_REGISTRY` auth resolution, `provider_flows`/`_model_flow_*` menu, model catalog + alias parsing, `api_mode` resolution at agent init, aux-model auth, provider error-map taxonomy, and the bundled provider-plugin registry + custom-provider profile the fast-path shortcut and Step-1-10 wiring touch.
- Docs (10): hermes_adding_built_in_tool, hermes_contributing_dev_setup, hermes_adding_platform_adapter_plugin, hermes_programmatic_integration, hermes_creating_skill_format, hermes_adding_platform_adapter_builtin, hermes_creating_skill_publish, hermes_extending_cli_wrapper [sibling hermes_* — resolve at finalization], cc_model_selection [the analogous Claude-Code provider/model selection reference], cc_llm_gateway [Claude-Code LLM-gateway / provider-routing parallel — the "wire a non-default inference endpoint" doc].

**Note 3 `hermes_adding_platform_adapter_plugin`**
- Terms (8): term_adapter_pattern, term_plugin_manifest, term_oop_inheritance, term_oop_polymorphism, term_cron, term_human_in_the_loop, term_authentication, term_webhook — relevance: a plugin adapter subclasses `BasePlatformAdapter` (inheritance/polymorphism over connect/send/handle_message) declared by a `plugin.yaml` manifest, wires cron `deliver=`/`standalone_sender_fn`, auth (`requires_env`), and long-poll/webhook transports; the slow-LLM postback bubble is a human-in-the-loop UX. (+fin: term_messaging_gateway [own], term_hermes_plugin [own], term_silence_token [own])
- Code-Repos (5): repo_hermes_agent_plugins — the `plugins/platforms/` drop-in directory + `register_platform()` path this page is the procedure for; repo_hermes_agent_gateway_messaging — `gateway/platforms/base.py` `BasePlatformAdapter` + the ~20 integration points the registry wires; repo_hermes_agent_cron — `cron_deliver_env_var` + out-of-process `standalone_sender_fn` delivery; repo_hermes_agent_cli — `hermes_cli/config.py` `plugin.yaml`→`OPTIONAL_ENV_VARS` env surfacing; repo_hermes_agent_tools — `tools/send_message_tool.py` send-dispatch the plugin platform routes through.
- Snippets (10): plugins_interfaces_abcs, plugins_namespace_init, plugins_manifest_schema, plugins_platform_irc, plugins_platform_line, plugins_platform_teams, plugins_platform_google_chat, gw_platform_base_abstract, gw_platform_base_outbound, tools_cronjob_register — relevance: the plugin ABC interfaces + `register_platform` namespace loader, the `plugin.yaml` manifest schema, the four reference plugin adapters (IRC/LINE/Teams/Google-Chat — including LINE's postback `_keep_typing`/`send` overrides), the `BasePlatformAdapter` abstract base + outbound path the page extends, and the cronjob register that `deliver=<plugin>` resolves against.
- Docs (10): hermes_adding_platform_adapter_builtin, hermes_adding_built_in_tool, hermes_adding_inference_provider, hermes_creating_skill_publish, hermes_contributing_dev_setup, hermes_creating_skill_format, hermes_programmatic_integration, hermes_extending_cli_wrapper [sibling hermes_* — resolve at finalization], cc_plugin_components [the analogous Claude-Code plugin-component authoring doc], cc_plugin_manifest_schema [Claude-Code plugin manifest schema — parallel to `plugin.yaml`].

**Note 4 `hermes_adding_platform_adapter_builtin`**
- Terms (8): term_adapter_pattern, term_oop_inheritance, term_websocket, term_webhook, term_authentication, term_api_gateway, term_human_in_the_loop, term_modularity — relevance: the built-in path adds a `Platform` enum + `BasePlatformAdapter` subclass (adapter pattern / inheritance) and wires the gateway runner, cross-platform/cron delivery, CLI, tools/toolsets, and prompt hints across 20+ files; transports span WebSocket/long-poll and webhook/callback servers; the parity-audit is the modularity discipline. (+fin: term_messaging_gateway [own], term_hermes_profile [own])
- Code-Repos (5): repo_hermes_agent_gateway_messaging — `gateway/platforms/<p>.py` + `gateway/{config,run}.py` enum/runner touchpoints the checklist edits; repo_hermes_agent_cli — the `hermes_cli/{config,gateway,platforms,setup,status,dump}.py` CLI-integration touchpoints; repo_hermes_agent_cron — `cron/scheduler.py` `_KNOWN_DELIVERY_PLATFORMS` + cross-platform delivery; repo_hermes_agent_tools — `tools/{send_message_tool,cronjob_tools}.py` + the per-platform toolset; repo_hermes_agent_agent_core — `agent/prompt_builder.py` `_PLATFORM_HINTS` injected into the system prompt.
- Snippets (10): gw_platform_base_abstract, gw_platform_base_outbound, gw_platform_base_normalize, gw_runner_init, gw_runner_router, gw_runner_acl, gw_platform_webhook, gw_config_schema, gw_platform_telegram_connect, core_prompt_builder_environment — relevance: the platform-base abstract contract + outbound/normalize, the gateway runner init/router/ACL (`_create_adapter`/`_is_user_authorized`), the webhook cross-platform delivery, the gateway config schema, the Telegram long-poll reference adapter the checklist mirrors, and the prompt-builder environment where `_PLATFORM_HINTS` lands.
- Docs (10): hermes_adding_platform_adapter_plugin, hermes_adding_inference_provider, hermes_adding_built_in_tool, hermes_contributing_dev_setup, hermes_programmatic_integration, hermes_creating_skill_format, hermes_creating_skill_publish, hermes_extending_cli_wrapper [sibling hermes_* — resolve at finalization], cc_extending_claude_code [the analogous Claude-Code "extend the core surface" doc], cc_build_a_channel [Claude-Code build-a-channel — the parallel core-contributor messaging-surface integration].

**Note 5 `hermes_creating_skill_format`**
- Terms (8): term_skill_manifest, term_skills, term_oauth_token, term_authentication, term_sandbox_backend, term_pii, term_prompt_injection, term_function_calling — relevance: the SKILL.md frontmatter IS the skill manifest; conditional `requires_*`/`fallback_for_*` gate by tools/toolsets, `required_environment_variables`/`required_credential_files` declare OAuth tokens/secrets auto-passed-through into the Docker/Modal sandbox; security guard scans for injection/PII; the skill-vs-tool decision contrasts with function-calling tools. (+fin: term_progressive_disclosure [own], term_skills_hub [own])
- Code-Repos (5): repo_hermes_agent_skills — the `skills/<category>/<name>/SKILL.md`+`scripts/` layout + frontmatter loader this page specifies; repo_hermes_agent_tools — `tools/` skill-manager + `environments/*` sandbox file-sync + credential-file mounting; repo_hermes_agent_agent_core — `agent/prompt_builder.py` skills snapshot that injects the skill into the system prompt; repo_hermes_agent_cli — `hermes_cli/setup.py` + `hermes config` skill-settings flow; repo_hermes_agent_mcp_toolsets — `requires_toolsets`/`fallback_for_toolsets` conditional activation against the toolset registry.
- Snippets (10): tools_skill_manager, tools_skills_validate, tools_skills_invoke, tools_skills_guard, core_prompt_builder_skills_snapshot, tools_credential_files, tools_environments_file_sync, cli_setup_skills, core_skill_utils_frontmatter, tools_environments_docker — relevance: the skill-manager load/validate/invoke, the security guard, the system-prompt skills snapshot, `required_credential_files` mounting, sandbox file-sync, setup-skills code, the SKILL.md frontmatter parser, and the Docker sandbox the declared env/credential files mount into.
- Docs (10): hermes_creating_skill_publish, hermes_adding_built_in_tool, hermes_contributing_dev_setup, hermes_adding_platform_adapter_plugin, hermes_programmatic_integration, hermes_adding_inference_provider, hermes_adding_platform_adapter_builtin, hermes_extending_cli_wrapper [sibling hermes_* — resolve at finalization], cc_create_a_skill [the analogous Claude-Code skill-authoring procedure], cc_skill_frontmatter_reference [Claude-Code SKILL.md frontmatter reference — direct parallel to the Hermes SKILL.md format].

**Note 6 `hermes_creating_skill_publish`**
- Terms (8): term_skills, term_skill_manifest, term_cron, term_prompt_injection, term_human_in_the_loop, term_autonomous_coding_agents, term_self_evolving_agent, term_progressive_summarization — relevance: guidelines + blueprints turn a skill into a scheduled (cron) automation gated by `/suggestions` (human-in-the-loop, opt-in accept); the trust-level scanner blocks injection/destructive/exfiltration findings; progressive disclosure keeps token cost low; published skills extend a self-evolving agent's capability set. (+fin: term_skills_hub [own], term_skill_curator [own], term_progressive_disclosure [own])
- Code-Repos (5): repo_hermes_agent_skills — the guideline set + `hermes skills publish`/tap lifecycle + `[[as_document]]`/template-token semantics this page documents; repo_hermes_agent_tools — the skills-hub registry/install + security guard (`tools/skills_guard`); repo_hermes_agent_cron — blueprint `schedule:`→cron-job register/handoff + Suggested Cron Jobs; repo_hermes_agent_cli — `hermes skills install/browse`/`/suggestions` CLI surface; repo_hermes_agent — top-level repo anchoring the skills-feature publishing model.
- Snippets (10): tools_skills_hub_registry, tools_skills_hub_install, tools_skills_guard, cli_skills_install, cli_skills_hub, tools_cronjob_register, tools_cronjob_handoff, tools_skill_manager, cron_job_crud, cron_run_job_execute — relevance: the skills-hub registry/install, the trust-level security guard, CLI install/browse, the blueprint→cron register/handoff, the skill-manager, and the `cron.jobs.create_job` CRUD + run-execute path `/suggestions accept` calls.
- Docs (10): hermes_creating_skill_format, hermes_adding_built_in_tool, hermes_contributing_dev_setup, hermes_programmatic_integration, hermes_adding_platform_adapter_plugin, hermes_adding_inference_provider, hermes_adding_platform_adapter_builtin, hermes_extending_cli_wrapper [sibling hermes_* — resolve at finalization], cc_host_and_manage_marketplaces [the analogous Claude-Code marketplace publish/host procedure], cc_create_routine [Claude-Code routine/automation authoring — parallel to blueprint→cron].

**Note 7 `hermes_extending_cli_wrapper`**
- Terms (8): term_oop_inheritance, term_oop_polymorphism, term_template_method_pattern, term_strategy_pattern, term_agent_harness, term_autonomous_coding_agents, term_persona, term_session_persistence — relevance: a wrapper CLI subclasses `HermesCLI` and overrides protected template-method hooks (`_get_extra_tui_widgets`/`_register_extra_tui_keybindings`/`_build_tui_layout_children`/`process_command`) without touching the 1000+-line `run()` — classic inheritance + template-method extension of the harness front-end; `self.agent`/`self.conversation_history` expose session state. (+fin: term_voice_mode [own])
- Code-Repos (5): repo_hermes_agent_cli — `HermesCLI` + the five protected extension seams this page is the procedure for; repo_hermes_agent_tui_gateway — the TUI render/layout/keybinding machinery the hooks plug widgets/keybindings into; repo_hermes_agent_agent_core — `self.agent` (`AIAgent`) state the wrapper reads; repo_hermes_agent — top-level repo anchoring the wrapper-CLI-without-overriding-`run()` contract; repo_hermes_agent_mcp_toolsets — `process_command` slash commands can drive toolset/tool changes the wrapper surfaces.
- Snippets (10): tui_entry, tui_server_render, tui_server_input, tui_server_slash, tui_slash_worker, tui_transport, tui_server_jsonrpc, tui_server_agent_build, cli_hermescli_run, cli_hermescli_process_command — relevance: the TUI entry/render/input/slash/transport/agent-build code paths the extension hooks plug into, plus the `HermesCLI.run()` the page says NOT to override and the existing `process_command` hook a wrapper extends.
- Docs (10): hermes_programmatic_integration, hermes_adding_built_in_tool, hermes_contributing_dev_setup, hermes_creating_skill_format, hermes_adding_platform_adapter_plugin, hermes_adding_inference_provider, hermes_adding_platform_adapter_builtin, hermes_creating_skill_publish [sibling hermes_* — resolve at finalization], cc_keybindings_customization [the analogous Claude-Code keybinding/UI customization doc], cc_output_styles [Claude-Code output-style / status-line customization — parallel TUI-extension surface].

**Note 8 `hermes_programmatic_integration`**
- Terms (8): term_acp_agent_client_protocol, term_json_rpc, term_rest, term_openai_responses_api, term_sse, term_websocket, term_multi_agent_systems, term_subagent — relevance: the three protocols are ACP (JSON-RPC/stdio over the Agent Client Protocol), the TUI-gateway JSON-RPC (+WebSocket), and the OpenAI-compatible REST API server (`/v1/chat/completions` + `/v1/responses` streamed via SSE); tool-call events + `session.branch` power IDE/multi-agent/subagent embedding. (+fin: term_provider_routing [own])
- Code-Repos (5): repo_hermes_agent_acp — `acp_adapter/` the ACP-over-stdio protocol; repo_hermes_agent_tui_gateway — `tui_gateway/server.py` + `ws.py` the JSON-RPC method/event catalog; repo_hermes_agent_gateway_messaging — `gateway/platforms/api_server.py` the OpenAI-compatible HTTP+SSE server; repo_hermes_agent_agent_core — the shared `AIAgent` core all three drive (incl. in-process embed) + `model_switch.py` `/model` hot-swap; repo_hermes_agent_cli — `hermes acp`/`hermes --tui` entrypoints that start the servers.
- Snippets (10): acp_entry, acp_server_prompt, acp_server_session_methods, acp_events, acp_tools_fanout, tui_server_jsonrpc, tui_server_slash, core_run_agent_cli, gw_platform_api_server_routes, tui_ws_primitives — relevance: the ACP entry/prompt/session/event/tool-fanout, the TUI-gateway JSON-RPC + slash dispatch + WebSocket primitives, the in-process `AIAgent` run path, and the OpenAI-compatible `/v1/*` API-server routes the three protocols expose.
- Docs (10): hermes_extending_cli_wrapper, hermes_adding_inference_provider, hermes_adding_built_in_tool, hermes_adding_platform_adapter_plugin, hermes_contributing_dev_setup, hermes_creating_skill_format, hermes_creating_skill_publish, hermes_adding_platform_adapter_builtin [sibling hermes_* — resolve at finalization], cc_agent_sdk_overview [the analogous Claude-Code Agent-SDK programmatic-drive overview], cc_sdk_connect_mcp_servers [Claude-Code SDK MCP/protocol connection — parallel external-program integration surface].

**Note 9 `hermes_contributing_dev_setup`**
- Terms (8): term_prompt_injection, term_sandbox_backend, term_docker, term_oauth_token, term_authentication, term_human_in_the_loop, term_code_review, term_ci_cd — relevance: dev setup (`uv venv`, `.[all,dev]`, `.env` provider key) configures providers/secrets; the security section covers shell/prompt-injection + Docker sandbox hardening + dangerous-command approval (human-in-the-loop); the PR process is Conventional-Commits + tests + cross-platform review (code-review / CI discipline). (+fin: term_hermes_profile [own], term_tirith [own])
- Code-Repos (5): repo_hermes_agent_cli — the installer/doctor/`hermes_cli/*` dev-setup + cross-platform (`stdio_windows`/`gateway_windows`) code the rules govern; repo_hermes_agent_tools — `tools/approval.py` dangerous-command policy + skills security guard + `shlex.quote` shell hardening; repo_hermes_agent_agent_core — `hermes_constants.get_hermes_home()` profile-safe paths + UTF-8/redaction primitives; repo_hermes_agent_gateway_messaging — `gateway.status.terminate_pid` centralized cross-platform process primitive; repo_hermes_agent — top-level repo + AGENTS.md the contributing rules anchor to.
- Snippets (10): cli_setup_installer, cli_doctor_primitives, cli_doctor_api_connectivity, core_credential_sources, tools_approval_policy, tools_skills_guard, gw_run_helpers, cli_config_validate, core_hermes_home, cli_stdio_windows — relevance: the installer/doctor/credential-source, the dangerous-command approval policy, the skills security guard, cross-platform process helpers, config-validate, the `get_hermes_home()` profile-safe-path primitive, and the Windows stdio fallback the cross-platform rules require.
- Docs (10): hermes_adding_built_in_tool, hermes_adding_inference_provider, hermes_creating_skill_format, hermes_adding_platform_adapter_builtin, hermes_programmatic_integration, hermes_creating_skill_publish, hermes_adding_platform_adapter_plugin, hermes_extending_cli_wrapper [sibling hermes_* — resolve at finalization], cc_devcontainer_setup [the analogous Claude-Code dev-container / dev-environment setup doc], cc_prompt_injection_defenses [Claude-Code prompt-injection-defense reference — parallel to the Hermes security section].

All 9 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (forward-ref `[own]` terms are EXCLUDED from the
≥8 term floor; the ≥10 doc floor is satisfied by 8 sibling `hermes_*` notes in this series — which resolve at
links resolve in `resources/documentation/hermes_agent/` (intra-series links land at finalization, verified by
G5/G8). **No placeholder/non-existent term, code-repo, or snippet IDs survive in any `Terms (8)`/`Code-Repos
active before lock-in (the prior `term_acp` was corrected to the active `term_acp_agent_client_protocol`).**

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 7 source pages from `inbox/hermes_agent_docs/developer-guide/`; measured counts match the Source
Pages table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 adding-built-in-tool | procedure | 900 | ≤6 (curate from 5 short blocks) | ✓ |
| 2 adding-inference-provider | procedure | 1500 | ≤6 (page has only 6; curate to the load-bearing 3-5) | ✓ |
| 3 platform-adapter-plugin | procedure | 1700 | ≤6 (curate from ~12 plugin-path blocks; one canonical plugin.yaml + adapter.py + register) | ✓ |
| 4 platform-adapter-builtin | procedure | 1500 | ≤6 (curate from ~8 built-in-path blocks; enum+adapter+patterns) | ✓ |
| 5 creating-skill-format | procedure | 1500 | ≤6 (curate from ~12 frontmatter blocks; one canonical SKILL.md + conditional + env/config) | ✓ |
| 6 creating-skill-publish | procedure | 1200 | ≤6 (curate from ~9 guideline/blueprint/publish blocks) | ✓ |
| 7 extending-cli-wrapper | procedure | 750 | ≤6 (curate from 8 hook blocks; wrapper example + 1-2 hook refs) | ✓ |
| 8 programmatic-integration | procedure | 800 | 3 (page has 3; keep verbatim) | ✓ |
| 9 contributing-dev-setup | procedure | 1100 | ≤6 (curate from 13 setup/cross-platform blocks) | ✓ |

No further splits needed — all 9 notes ≤1700w (well under 2500w). Code-heavy pages (platform-adapters,
creating-skills, contributing) are curated to ≤6 load-bearing blocks (kept verbatim), with the rest summarized
in prose. Borderline check: Notes 3/5 (~1500-1700w) are each one topically-cohesive procedural arc (single BB,
no mixing) → KEEP (review CP6 default-to-keep justification). If any note exceeds 350 lines during writing,
STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it
IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP19a)

**SP19a owns 0 new term captures.** Per the master's corpus-wide ownership sweep and the SP01/SP02 precedent,
every Hermes-specific concept SP19a touches is owned by another sub-plan (link at finalization) or is an
existing verified term. The augment re-read surfaced candidate concepts (`platform adapter`, `built-in tool`,
`wrapper CLI`) — but each is a **developer procedure** documented by an SP19a note, NOT a standalone reusable
concept warranting a term; their concept-homes are existing terms (`term_adapter_pattern`, `term_provider_plugin`,
`term_skill_manifest`) or owner sub-plans (`term_hermes_plugin`→SP06b, `term_messaging_gateway`→SP11). Collision
audit confirmed the LIKE-matched `term_channel_adapter`/`term_plugin_sdk`/`term_adapter_pattern` are
different/generic concepts, so no SP19a-owned capture survives the audit.

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_hermes_plugin` | LINK only (forward-ref, +fin) `[own]` | SP06b | the plugin *system* concept (tools/hooks/providers/platform adapters); SP19a documents the adapter/provider authoring procedure, SP06b owns the concept. |
| `term_messaging_gateway` | LINK only (+fin) `[own]` | SP11 | platform↔agent bridge; the adapter notes wire into it, SP11 owns it. |
| `term_provider_routing`, `term_fallback_provider` | LINK only (+fin) `[own]` | SP09 | provider-wiring page references aux/fallback; concept home is SP09 protocols/providers. |
| `term_nous_portal` | LINK only (+fin) `[own]` | SP14 | OAuth provider example in adding-providers; captured by SP14. |
| `term_progressive_disclosure`, `term_skills_hub`, `term_skill_curator` | LINK only (+fin) `[own]` | SP05 | skill-authoring pages reference progressive disclosure + hub + curator; concept homes are SP05. |
| `term_code_execution_tool`, `term_delegate_task` | LINK only (+fin) `[own]` | SP06 | agent-loop-intercepted tools referenced in adding-tools; owned by SP06. |
| `term_voice_mode`, `term_silence_token`, `term_hermes_profile`, `term_tirith` | LINK only (+fin) `[own]` | SP08 / SP11 / SP04 / SP03 | referenced in passing; concept homes are their owner sub-plans. |

### Renamed (general → specific)

— (audit performed; SP19a owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP19a links; all are already scope-qualified by their owners
— e.g. `term_hermes_plugin` not bare `term_plugin`, `term_messaging_gateway` not bare `term_gateway`.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_platform_adapter` (would-be) | `term_channel_adapter.md` (67L active — UNRELATED Amazon-CS concept) + `term_adapter_pattern.md` (active, generic) | Not captured — the Hermes adapter is a *procedure* (Notes 3/4); link `term_adapter_pattern` (generic) + `term_messaging_gateway` (+fin SP11). No SP19a capture. |
| `term_built_in_tool` (would-be) | none substantive; concept = `term_function_calling` (active) + `term_provider_plugin`/`term_skill_manifest` | Not captured — documented as procedure (Note 1); link `term_function_calling`. |
| `term_wrapper_cli` (would-be) | none substantive; concept = `term_oop_inheritance` + `term_template_method_pattern` (active) | Not captured — documented as procedure (Note 7); link the OOP terms. |

## Term-Note Authoring Requirements

N/A (inherited) — SP19a owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP03/04/05/06/06b/08/09/11/14). The full
diversity, MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12,
backlink expansion, >200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (tool/provider authoring, P3 pilot):** Notes 1, 2. Pilot Note 1 first → reindex → verify
  format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (platform adapters + skills):** Notes 3, 4, 5, 6. GATE G1–G8.
- **Phase 3 (CLI/integration/contributing):** Notes 7, 8, 9. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/developer-guide/<page>`
(code verbatim for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4,
DB-verify every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7
single-BB · **G8 in-degree ≥1 from outside the folder**.

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
for n in hermes_adding_built_in_tool hermes_adding_inference_provider hermes_adding_platform_adapter_plugin hermes_adding_platform_adapter_builtin hermes_creating_skill_format hermes_creating_skill_publish hermes_extending_cli_wrapper hermes_programmatic_integration hermes_contributing_dev_setup; do
```

## Entry Point Decision (inherited)

Contributes 9 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Developer: Core Extension" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP19a does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_tools.md` | → `hermes_adding_built_in_tool` | tools repo ↔ tool-authoring procedure |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_adding_inference_provider`, `hermes_adding_platform_adapter_builtin` | provider/adapter repo ↔ authoring procedures |
| `repo_hermes_agent_plugins.md` | → `hermes_adding_platform_adapter_plugin`, `hermes_adding_inference_provider` | plugins repo ↔ plugin-path authoring |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_adding_platform_adapter_builtin`, `hermes_adding_platform_adapter_plugin` | gateway/messaging repo ↔ adapter authoring |
| `repo_hermes_agent_skills.md` | → `hermes_creating_skill_format`, `hermes_creating_skill_publish` | skills repo ↔ skill-authoring procedures |
| `repo_hermes_agent_cli.md` | → `hermes_extending_cli_wrapper`, `hermes_contributing_dev_setup` | CLI repo ↔ wrapper-CLI + dev-setup docs |
| `repo_hermes_agent_acp.md` | → `hermes_programmatic_integration` | ACP repo ↔ programmatic-integration doc |
| `repo_hermes_agent_tui_gateway.md` | → `hermes_programmatic_integration`, `hermes_extending_cli_wrapper` | TUI/gateway repo ↔ integration + wrapper docs |
| `term_provider_plugin.md` | → `hermes_adding_inference_provider` | concept term → provider-authoring procedure |
| `term_skill_manifest.md` | → `hermes_creating_skill_format` | concept term → SKILL.md authoring procedure |
| `term_acp.md` | → `hermes_programmatic_integration` | concept term → programmatic-integration doc |
| `term_adapter_pattern.md` | → `hermes_adding_platform_adapter_plugin` | generic pattern term → concrete Hermes adapter authoring |
| `term_channel_adapter.md` | (NO inlink — unrelated Amazon-CS concept) | confirmed LIKE false-positive; do NOT link |
| `entry_code_snippets_hermes_agent.md` | → `hermes_adding_built_in_tool`, `hermes_adding_inference_provider` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 9 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_adding_built_in_tool`) → reindex → verify format/ghost/in-degree BEFORE authoring the
rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each
note — do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes
(platform-adapters, creating-skills, contributing) to ≤6 load-bearing blocks, summarize the rest in prose.
If a note exceeds 350 lines during writing, STOP and split. If multi-agent: agents return note content, master
writes serially where there is write-contention; ≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP19a lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 9 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- Coordinate with SP19b at finalization: cross-link `hermes_adding_inference_provider` ↔ the SP19b
  `*-provider-plugin` notes (the fast-path plugin shortcut + field reference); cross-link
  `hermes_adding_platform_adapter_plugin` ↔ SP06b `plugins`/`built-in-plugins`.
- After P3 wave: bidirectional links from SP18 internals (`provider-runtime`, `gateway-internals`,
  `agent-loop`, `acp-internals`) — the internals notes explain *how* the surfaces these authoring procedures
  extend actually run.
- Consider one `thought_` note comparing Hermes' docs-stated extension model vs the code-digestion findings
  in `snippet_hermes_agent_plugins_*` / `gw_platform_base_*`.

## Augmentation Report

- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  to ≥10; code-repos confirmed ≥5 (from the 13 `repo_hermes_agent_*`); docs raised to ≥10 (8 sibling `hermes_*` +
  ≥2 `cc_*`). Re-read all 7 owned `inbox/hermes_agent_docs/developer-guide/` pages before re-selecting so every
  relevance clause is grounded in real content; corrected the one dead term id (`term_acp`→`term_acp_agent_client_protocol`).
- Sections added/updated: Collision&Dedup Audit (LIKE false-positives `term_channel_adapter`/`term_plugin_sdk`/
  `term_adapter_pattern` confirmed by reading the notes), finalized Per-Note Mapping (FOUR-FLOOR ≥8 term + ≥5
  floor), Doc-Note Authoring Spec (derived from `cc_*.md`), Density Re-Assessment (re-read confirmed), G5 ghost +
  G8 scripts, Inlinks.
- Density re-read: counts match measured (adding-tools 796, adding-providers 2193, adding-platform-adapters
  3454, creating-skills 2753, extending-cli 767, contributing 1316 [re-measured 2026-06-19], programmatic-integration 809); **2 splits
  applied** (platform-adapters→2, creating-skills→2); all 9 notes ≤1700w; code-heavy notes curated to ≤6 blocks.
- Collision audit: **0 removals from a substantive same-concept note** — `term_channel_adapter` (Amazon CS),
  `term_plugin_sdk` (OpenClaw TS), `term_adapter_pattern` (generic GoF) are all LINK-not-dup; 3 would-be SP19a
  slugs (`term_platform_adapter`, `term_built_in_tool`, `term_wrapper_cli`) recorded in Removed (documented as
  procedures, not captured).
- Term placeholder catch: term-id, code-repo-id, snippet-id, and `cc_*` doc-id lines re-checked; **no
  `term_acp`, was replaced by the active `term_acp_agent_client_protocol`; `term_websocket`+`term_webhook` both
  retained where the page uses both transports).
- Undigested terms surfaced at augment: **0 new owned** (SP19a owns 0 captures; all concepts owned by other SPs
  or existing terms).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (FOUR-FLOOR
G5/G6/G8 ✓ Note Format Def (derived) ✓
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth Reqs (N/A-inherited) ✓ invokes
capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (N/A — 0 owned;
audit noted) ✓ Slug Collision (3 LIKE false-positives + 3 would-be slugs recorded Removed) ✓ dedup generalized
to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED ✓
Doc-Note Authoring Spec derived ✓). Term-capture items are N/A-pass (SP19a owns 0 captures); dedup/collision
items are substantively PASS (audit performed on all 9 doc notes).

## Review Sign-Off

**Re-reviewed 2026-06-19 (independent, FOUR-FLOOR standard) — READY FOR EXECUTION (9/9 checkpoints pass).**
Supersedes the 2026-06-15 review (which used the prior ≥8 term/≥8 snippet/≥5 doc floor).

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (9 rows under a Developer: Core Extension section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 9 notes ≤30; master holds the corpus-level split (SP19 split into 19a/19b). |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | adding-platform-adapters→2, creating-skills→2; all 9 notes ≤1700w; code-heavy notes curated ≤6; Notes 3/5 checked → cohesive single-BB procedures, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15; re-measured 2026-06-19 (mirror c253b07): adding-platform-adapters 3454, creating-skills 2753, adding-providers 2193, contributing 1316 (was 1117 — upstream grew), programmatic-integration 809, adding-tools 796, extending-cli 767 — measured == plan (ratio 1.00). Review spot-re-measure (2026-06-19, strip leading frontmatter only): contributing 1316w/13code, adding-tools 796w/5code, adding-providers 2193w/6code, programmatic-integration 809w/3code — all match plan exactly. |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP19a owns 0 term captures (all concepts owned by SP03/04/05/06/06b/08/09/11/14 or existing terms); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 9 doc notes (term_dictionary AND documentation/); 3 LIKE false-positives confirmed (channel-adapter Amazon-CS / plugin-sdk OpenClaw-TS / adapter-pattern generic = LINK not dup); 3 would-be slugs recorded in Removed; Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 9 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION** (independent FOUR-FLOOR re-review, 2026-06-19).

## Re-Sync Note (2026-06-19)

Re-downloaded the local mirror `inbox/hermes_agent_docs/` from upstream `main` HEAD (mirror_commit
`c253b07`, was pinned `95715dc`) and independently re-measured all 7 SP19a pages with the ledger convention
(body words after stripping YAML frontmatter; code blocks = `^\s*```` lines ÷ 2).

**Changed page (old → new):**
- developer-guide/contributing.md — 1117w/10code → 1316w/13code

**Unchanged pages (spot-re-measured, stable):** adding-tools.md 796w/5code, extending-the-cli.md 767w/8code,
programmatic-integration.md 809w/3code, adding-providers.md 2193w/6code — all match the prior ledger.
adding-platform-adapters.md (3454w/20code) and creating-skills.md (2753w/21code) unchanged (split pages).

**Density re-evaluation:** Note 9 `hermes_contributing_dev_setup` (derived from contributing.md) was
re-assessed. Source grew +199w (1117→1316, still far under the 2500w cap) and +3 raw code blocks (10→13,
curated to ≤6 load-bearing blocks regardless). The note's ~Words estimate was nudged 1050→1100. **Outcome:
no-split** — the page remains a single topically-cohesive procedural arc well within all caps; no cap breach.
No other planned-note density decision changed.

**Cross-ref floor:** RAISED 2026-06-19 to the FOUR-FLOOR standard — every note now carries ≥8 term + ≥5
code-repo + ≥10 snippet + ≥10 doc (snippets promoted from bonus to a counted ≥10 floor; docs raised to ≥10 via 8
sibling `hermes_*` + ≥2 `cc_*`; forward-ref `[own]` terms excluded from the term floor). No filenames, BB types,
or gates altered.

**Verdict:** plan remains **READY** for execution.

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-19 re-augment to FOUR-FLOOR; orig 2026-06-15, 31/31) · Review: **DONE** (2026-06-19 independent FOUR-FLOOR re-review, 9/9 READY; orig 2026-06-15) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/developer-guide/{adding-tools,adding-providers,adding-platform-adapters,creating-skills,extending-the-cli,contributing,programmatic-integration}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
