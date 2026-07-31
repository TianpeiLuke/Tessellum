---
title: Sub-Plan cl06 — OpenClaw Docs CLI: path, plugins, policy, proxy, qr, reset, sandbox
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/path", "cli/plugins", "cli/policy", "cli/proxy", "cli/qr", "cli/reset", "cli/sandbox"]
---

# Sub-Plan cl06: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_*`), format (YAML field order, `## Overview` → body →
> `## Related Notes` → `## References` → bold footer; ≤400L/≤2500w/≤6 code, one BB/note), dedup-before-create
> (term_dictionary + documentation/ + `repo_openclaw*`), 9-GATE, cross-refs, and entry-point (`entry_openclaw_docs.md`)
> are ALL inherited from the master and applied here. This file locks the per-page→note mapping, splits, candidate

## Scope

The 7 mid-alphabet CLI-reference pages: `openclaw path` (the `oc://` addressing substrate CLI), `openclaw plugins`
(plugin/bundle lifecycle), `openclaw policy` (enterprise conformance layer), `openclaw proxy` (managed-proxy
validation + debug capture), `openclaw qr` (mobile pairing QR/setup code), `openclaw reset` (local state reset), and
`openclaw sandbox` (sandbox-runtime management). **Priority: P1 (Phase A)** — the CLI surface that the gateway,
sandbox, security, and plugin docs reference; `policy`/`sandbox`/`plugins` are operationally load-bearing (the
config-conformance, isolation, and extension-lifecycle controls). The code-side counterparts (`repo_openclaw_security`,
`repo_openclaw_extensions`, `repo_openclaw_cli_wizard`, `repo_openclaw_gateway`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **13,862 measured words**. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| path | /cli/path | 2,591 | 22 | 16 | 9 | procedure + concept (split: addressing substrate vs verb usage) |
| plugins | /cli/plugins | 4,017 | 16 | 2 | 10 | procedure (split: install/lifecycle vs author/inspect/manage) |
| policy | /cli/policy | 5,286 | 19 | 7 | 1 | argument + model + procedure (split ×3: model/rules vs attestation/findings vs configure/repair) |
| proxy | /cli/proxy | 580 | 1 | 5 | 0 | procedure |
| qr | /cli/qr | 424 | 1 | 4 | 0 | procedure |
| reset | /cli/reset | 153 | 1 | 1 | 0 | procedure |
| sandbox | /cli/sandbox | 811 | 10 | 7 | 9 | procedure |

(Code = raw ` ``` ` fence count ÷ 2. path H3 count includes 4 file-kind recipe subheads + 5 subcommand-reference subheads.)

## Content Strategy

- **Prioritize**: the `policy` conformance model (rule schema, attestation tuple, findings catalog — the
  enterprise governance surface other security/gateway docs lean on) and the `oc://` addressing substrate (`path`),
  because the `oc://` scheme appears as evidence addresses throughout `policy`, `gateway`, and config docs.
- **Split**: `policy.md` (5,286w / mixed argument+model+procedure) → 3 notes; `plugins.md` (4,017w) → 2 notes;
  `path.md` (2,591w, just over the 2,500w cap and mixing the addressing-grammar concept with verb usage) → 2 notes.
  `proxy`/`qr`/`reset`/`sandbox` stay 1 note each (all ≤2,500w, single BB).
- **Link-out (do not redefine)**: sandbox/isolation internals → `cli/sandbox` already covers the CLI; deep
  sandboxing config lives in gw05 (`gateway/sandboxing`) — link, do not duplicate. Network-proxy deployment
  semantics → se01 (`security/network-proxy`) — link. Plugin manifest/architecture/bundles → pl01–pl25 — link.
  Doctor lint mode → cl03 (`cli/doctor`). Pairing/devices → cl05 (`cli/pairing`). Term vocabulary
  (`term_sandbox`, `term_mcp`, `term_reverse_proxy`, `term_oauth_token`, …) is LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_path_addressing.md` | concept | path.md: intro, Why use it, How it works, `oc://` syntax (slots/quotes/predicates/unions/wildcards/positional/ordinal/insertion/session), Addressing by file kind, Mutation contract | 700 | The `oc://` addressing substrate: kind-dispatched FILE/SECTION/ITEM/FIELD path grammar, per-kind addressing (md/jsonc/jsonl/yaml), and the byte-fidelity mutation contract behind `openclaw path`. |
| 2 | `oc_cli_path_commands.md` | procedure | path.md: enable plugin, How it is used, Subcommands, Global flags, Examples, Recipes by file kind, Subcommand reference (resolve/find/set/validate/emit), Exit codes, Output mode, Notes | 700 | Using `openclaw path`: enabling the `oc-path` plugin, the five verbs (resolve/find/set/validate/emit), global flags, `--dry-run`/`--diff` previews, per-kind recipes, and exit codes. |
| 3 | `oc_cli_plugins_install.md` | procedure | plugins.md: Commands (install subset), Install (auto-detect, ClawHub/npm/git/archive/marketplace sources, --force/--pin/--link), Uninstall, Update, Plugin index | 700 | Installing and lifecycle-managing plugins/bundles with `openclaw plugins`: source resolution (ClawHub/npm/git/archive/marketplace), `--force`/`--pin`/`--link`, uninstall, update, and the SQLite plugin index. |
| 4 | `oc_cli_plugins_manage.md` | procedure | plugins.md: Author (init/build/validate), List/search, Inspect/info, Doctor, Registry, Marketplace list, runtime-hook debugging | 650 | Authoring and inspecting plugins with `openclaw plugins`: scaffold (init/build/validate), list/search, inspect (shape classification, `--runtime`), doctor diagnostics, registry refresh, and marketplace listing. |
| 5 | `oc_cli_policy_model.md` | concept | policy.md: intro (conformance-layer model), Quick start, the minimal policy.jsonc, rule-authority semantics, Policy rule reference (scoped overlays + all category tables) | 750 | What `openclaw policy` is: an enterprise conformance layer over existing OpenClaw settings — `policy.jsonc` authored requirements, observed-evidence model, scoped overlays, and the full per-category rule reference. |
| 6 | `oc_cli_policy_attestation.md` | model | policy.md: `policy check`/`compare`/`watch`, Accept policy state (attestation tuple: policy/workspace/findings/attestation hashes), Findings catalog + finding JSON shape (target/requirement) | 700 | The policy evidence/attestation contract: `policy check`/`compare`/`watch`, the audit tuple (policy + evidence + findings + attestation hashes), the accept-state lifecycle, and the full findings catalog. |
| 7 | `oc_cli_policy_configure.md` | procedure | policy.md: Configure policy (`plugins.entries.policy.config`: enabled/path/workspaceRepairs/expectedHash/expectedAttestationHash), Repair (`doctor --fix` + workspaceRepairs), Exit codes | 450 | Configuring and repairing policy: the `plugins.entries.policy.config` block (path, hash-locks, workspaceRepairs), `doctor --lint`/`--fix` repair semantics, and per-command exit codes. |
| 8 | `oc_cli_proxy.md` | procedure | proxy.md: intro, Commands (start/run/validate/coverage/sessions/query/blob/purge), Validate (managed-proxy preflight + flags + APNs probe), Query presets, Notes | 550 | `openclaw proxy`: validating an operator-managed forward proxy (allowed/denied destinations, APNs reachability, CA trust) and the local debug capture proxy (start/run/sessions/query presets/blob/purge). |
| 9 | `oc_cli_qr.md` | procedure | qr.md: intro, Usage, Options (--remote/--url/--token/--password/--setup-code-only/--json), Notes (bootstrapToken, scopes, Tailscale/wss fail-closed, SecretRef resolution) | 450 | `openclaw qr`: generating a mobile pairing QR + setup code from gateway config — remote/local URL sources, bootstrapToken vs gateway token, operator-handoff scopes, and Tailscale/`wss://` fail-closed rules. |
| 10 | `oc_cli_reset.md` | procedure | reset.md: intro, Options (--scope/--yes/--non-interactive/--dry-run), Examples, Notes (backup-first) | 350 | `openclaw reset`: wiping local config/state (keeps the CLI installed) at `config` / `config+creds+sessions` / `full` scope, with `--dry-run`, non-interactive flags, and backup-first guidance. |
| 11 | `oc_cli_sandbox.md` | procedure | sandbox.md: Overview, Commands (explain/list/recreate), Use cases (after image/config/SSH/OpenShell/setupCommand changes), Why this is needed, Registry migration, Configuration | 600 | `openclaw sandbox`: inspecting effective sandbox policy (`explain`), listing runtimes (`list`), and forcing recreation (`recreate`) after Docker/SSH/OpenShell config changes, plus the SQLite registry migration. |

## Section Coverage Map

```
path.md (2,591w)
├── intro / CLI mirrors verbs / enable oc-path plugin ── → note 1 (concept) + note 2 (enable step)
├── Why use it ──────────────────────────────────────── → note 1
├── How it is used (5 examples) ─────────────────────── → note 2
├── How it works (parse/adapter/resolve/emit) ───────── → note 1
├── Subcommands (table) ─────────────────────────────── → note 2
├── Global flags (table) ────────────────────────────── → note 2
├── oc:// syntax (slot rules, quotes, predicates,
│   unions, wildcards, positional, ordinal, insertion,
│   session scope, reserved/control chars) ──────────── → note 1
├── Addressing by file kind (md/jsonc/jsonl/yaml) ───── → note 1
├── Mutation contract (md/jsonc/jsonl/yaml leaf+insert) → note 1
├── Examples (basic + grammar) ──────────────────────── → note 2
├── Recipes by file kind (Markdown/JSONC/JSONL/YAML) ── → note 2
├── Subcommand reference (resolve/find/set/validate/emit) → note 2
├── Exit codes / Output mode / Notes (sentinel/LKG) ─── → note 2
└── Related ─────────────────────────────────────────── → References (both notes)
plugins.md (4,017w)
├── intro / CardGroup pointers ──────────────────────── → notes 3 + 4 (Overview)
├── Commands (full block) ───────────────────────────── → note 3 (install verbs) + note 4 (author/list/inspect verbs)
├── trace env var / Nix-mode / bundled-plugin Note ──── → note 3
├── Author (init/build/validate) ────────────────────── → note 4
├── Install (sources, --force/--pin/--link, accordions,
│   ClawHub/npm/git/archive/marketplace, auto-detect) ─ → note 3
├── List (search, --enabled/--verbose/--json, restart) → note 4
├── Plugin index (SQLite install metadata) ──────────── → note 3
├── Uninstall ───────────────────────────────────────── → note 3
├── Update (id-vs-spec, beta, integrity drift) ──────── → note 3
├── Inspect (shape classification, --runtime) ───────── → note 4
├── Doctor (load errors, stale config) ──────────────── → note 4
├── Registry (cold read model, --refresh) ───────────── → note 4
├── Marketplace (list source) ───────────────────────── → note 4
└── Related ─────────────────────────────────────────── → References (both notes)
policy.md (5,286w)
├── intro (conformance-layer model, managed surfaces) ─ → note 5
├── Quick start (enable plugin, minimal policy.jsonc) ─ → note 5
├── rule-authority semantics (observed-state evidence) → note 5
├── Policy rule reference (strictness, scoped overlays,
│   all category tables: channels/mcp/models/network/
│   ingress/gateway/agent-workspace/sandbox/data-handling/
│   secrets/exec-approvals/auth-profiles/tool-metadata/
│   tool-posture) ───────────────────────────────────── → note 5
├── policy check / compare / watch ──────────────────── → note 6
├── Accept policy state (attestation tuple, lifecycle,
│   evidence JSON, watch drift) ─────────────────────── → note 6
├── Findings (full check-id catalog, finding JSON,
│   target/requirement, per-domain examples) ────────── → note 6
├── Configure policy (plugins.entries.policy.config) ── → note 7
├── Repair (doctor --fix, workspaceRepairs) ─────────── → note 7
├── Exit codes (check/compare/watch) ────────────────── → note 7
└── Related (doctor lint, path CLI) ─────────────────── → References (all 3 notes)
proxy.md (580w)
├── intro / Commands / Validate / Query presets / Notes → note 8 (whole page)
└── Related ─────────────────────────────────────────── → References (note 8)
qr.md (424w)
├── intro / Usage / Options / Notes ─────────────────── → note 9 (whole page)
└── Related ─────────────────────────────────────────── → References (note 9)
reset.md (153w)
├── intro / Options / Examples / Notes ──────────────── → note 10 (whole page)
└── Related ─────────────────────────────────────────── → References (note 10)
sandbox.md (811w)
├── Overview / Commands / Use cases / Why this is needed
│   / Registry migration / Configuration ────────────── → note 11 (whole page)
└── Related ─────────────────────────────────────────── → References (note 11)
```
No orphaned sections. Sandboxing config depth (gw05), network-proxy deployment (se01), plugin
manifest/architecture (pl01–25), doctor lint (cl03), and pairing (cl05) are linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| path.md (2,591w, 22 fences, 16 H2) | notes 1 + 2 | Exceeds the 2,500w cap AND mixes the addressing-grammar **concept** (`oc://` syntax, per-kind addressing model, mutation contract) with the verb-usage **procedure** (enable / resolve/find/set/validate/emit / flags / recipes). Splitting keeps each one BB and ≤700w; the 22 fences distribute (grammar/contract examples → note 1; usage/recipe transcripts → note 2) so each note stays ≤6 code blocks. |
| plugins.md (4,017w, 16 fences, 10 H3) | notes 3 + 4 | Far over the 2,500w cap. Two distinct task clusters: install/lifecycle (sources, --force/--pin/--link, uninstall, update, plugin index) vs author/inspect/manage (init/build/validate, list/search, inspect, doctor, registry, marketplace). Both procedure BB; split by task cluster keeps each ≤700w and ≤6 code blocks. |
| policy.md (5,286w, 19 fences, mixed BB) | notes 5 + 6 + 7 | More than 2× the 2,500w cap and mixes three BBs: the conformance-layer/rule **concept** (what policy is + rule reference), the evidence/attestation **model** (hashes, evidence JSON, findings catalog), and the configure/repair **procedure**. Three notes give one BB each, each ≤750w and ≤6 code blocks (the 19 fences split: minimal policy.jsonc + scoped-overlay + exec-approvals examples → note 5; check/compare/finding JSON → note 6; config + repair jsonc → note 7). |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (13,862 words). New `oc_*` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×8 (notes 2, 3, 4, 7, 8, 9, 10, 11) · concept ×2 (notes 1, 5) · model ×1 (note 6).
- Est. digest words ~6,600 (avg ~600/note). 70 source code fences distribute across the 11 notes; each note kept
  ≤6 by the splits above (config/policy/path snippets reproduced selectively, verbatim, capped per note).
- **Cross-refs (LOCKED 2026-06-21 in "Per-Note Related Notes Mapping"):** every note maps **≥8 relevance-selected
  docs + sibling `oc_*` planned-this-series), PLUS 2-3 `repo_openclaw*`, each with a per-link relevance statement.
  `oc_*` notes in this series are marked "(planned, this series)" and resolve once W1+execution land.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> the 2 missing first-pass snippet guesses — `snippet_hermes_agent_acp_event_ledger`, `snippet_openclaw_security_audit_ssrf` —
> were dropped/substituted). **Terms ≥8** (the floor, raised from the plan's ≥6). **Snippets ≥10** are ALL
> `hermes_agent/hermes_*`, `pi/pi_*`, `band/band_*` coding-agent corpora) plus sibling `oc_*` (this series,
> planned, not yet in DB) toward the 10. `entry_openclaw_docs.md` is the planned master-W1 hub. Each link is
> rendered `- [Name](relpath.md) — what it is; relevance: why THIS note`. Paths are relative FROM
> `resources/documentation/openclaw/oc_X.md`.

### oc_cli_path_addressing (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway whose state files this scheme addresses; relevance: `oc://` is OpenClaw's own kind-agnostic addressing substrate.
- [Markdown](../../term_dictionary/term_markdown.md) — lightweight markup; relevance: one of the four addressable kinds — H2 section / bullet-item slugs / `[frontmatter]` block.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — JSON structural contract; relevance: JSONC/JSON addressing descends by object keys and array indexes.
- [AST](../../term_dictionary/term_ast.md) — abstract syntax tree; relevance: each kind resolves slots against the file's parsed AST (markdown headings, JSONC keys, YAML nodes).
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config representation; relevance: YAML/`.lobster` workflow + JSONC config are the config the scheme reads and edits.
- [Regular Expression](../../term_dictionary/term_regex.md) — pattern matching; relevance: the `oc://` grammar (predicates, unions, wildcards, ordinals) is a structured alternative to ad-hoc grep/regex per file.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — substitute/facade indirection; relevance: the per-kind adapter dispatch is a substrate facade over heterogeneous file parsers.
- [Enforcement Pattern Validation](../../term_dictionary/term_enforcement_pattern_validation.md) — validate-before-act guard; relevance: `validate` is parse-only and `set` applies the redaction-sentinel guard (`__OPENCLAW_REDACTED__` refused).

**Docs**
- [oc_cli_path_commands](oc_cli_path_commands.md) — the `openclaw path` verb usage (planned, this series); relevance: the procedure half that consumes this grammar.
- [oc_cli_policy_model](oc_cli_policy_model.md) — policy conformance model (planned, this series); relevance: policy evidence `source`/`target` are `oc://` addresses produced by this scheme.
- [oc_cli_policy_attestation](oc_cli_policy_attestation.md) — policy findings/attestation (planned, this series); relevance: finding `target`/`requirement` fields are `oc://` paths.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — Claude Code settings field reference; relevance: sibling-tool analog of the structured config files this scheme leaf-edits.
- [cc_settings_files](../claude_code/cc_settings_files.md) — settings file locations/precedence; relevance: the JSON config-file substrate `path resolve/set` operates on, in a sibling tool.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — inspect effective config; relevance: parallels `path resolve`/`validate` for debugging a config address.
- [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — `.claude/` config layout; relevance: the markdown + JSON workspace files a kind-dispatched addresser targets.
- [pi_settings_reference](../pi/pi_settings_reference.md) — Pi settings reference; relevance: another coding-agent's structured config the same leaf-addressing problem applies to.
- [hermes_config_files_precedence](../hermes_agent/hermes_config_files_precedence.md) — Hermes config file precedence; relevance: the layered JSONC/YAML config a path scheme would resolve against.
- [cc_managed_settings](../claude_code/cc_managed_settings.md) — managed/locked settings; relevance: comment-preserving JSONC leaf writes matter most for hand-maintained managed config.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the `oc://` substrate + adapters live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: the gateway/agent config files the scheme addresses are gateway-owned.

**Snippets**
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config-leaf edit + reload plan; relevance: the mutation-contract analog (edit one leaf, preserve the rest).
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — CLI config-set leaf write; relevance: direct analog of `path set` writing one config leaf.
- [snippet_hermes_agent_cli_config_load](../../code_snippets/snippet_hermes_agent_cli_config_load.md) — CLI config load/parse; relevance: the parse step before slot resolution.
- [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migration/round-trip; relevance: byte-fidelity emit/round-trip the `emit` diagnostic verifies.
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — markdown frontmatter parse; relevance: the `[frontmatter]` markdown addressing model.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest (markdown+frontmatter); relevance: a markdown-with-frontmatter file kind the scheme can address by section/field.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — JSONL session-fs index read; relevance: the append-only JSONL line-record addressing model (`L1`, `[event=…]`).
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — append-only JSONL event ledger; relevance: a JSONL log the `find '…/[event=…]/field'` predicate path queries.

### oc_cli_path_commands (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `openclaw path` is its bundled `oc-path` CLI.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — shell/command execution surface; relevance: the verbs are copy-pasteable into hooks/scripts as shell commands.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config representation; relevance: `resolve`/`set` operate on config leaves with `--dry-run`/`--diff` previews.
- [Markdown](../../term_dictionary/term_markdown.md) — markup; relevance: the markdown recipe verbs (section/item/frontmatter).
- [JSON Schema](../../term_dictionary/term_json_schema.md) — JSON contract; relevance: the JSONC/JSONL recipe verbs and `--value-json` shape changes.
- [Enforcement Pattern Validation](../../term_dictionary/term_enforcement_pattern_validation.md) — validate guard; relevance: the `validate` parse-only verb + the 0/1/2 exit-code contract.
- [AST](../../term_dictionary/term_ast.md) — parsed tree; relevance: `resolve`/`find`/`set` walk the per-kind AST to reach the addressed node.
- [Regular Expression](../../term_dictionary/term_regex.md) — pattern matching; relevance: `find` expands wildcards/predicates/unions in lieu of bespoke regex/grep.

**Docs**
- [oc_cli_path_addressing](oc_cli_path_addressing.md) — the `oc://` grammar (planned, this series); relevance: the concept half these verbs consume.
- [oc_cli_sandbox](oc_cli_sandbox.md) — sandbox CLI (planned, this series); relevance: `sandbox explain --json` is a sibling TTY-aware JSON-vs-human CLI like `path --json/--human`.
- [oc_cli_policy_configure](oc_cli_policy_configure.md) — configure policy (planned, this series); relevance: `policy.jsonc` hash-locks edit the same JSONC config `path set` mutates.
- [cc_cli_flags](../claude_code/cc_cli_flags.md) — Claude Code CLI flag reference; relevance: sibling-tool CLI flag/output-mode (`--json`) conventions.
- [cc_cli_commands](../claude_code/cc_cli_commands.md) — CLI command reference; relevance: the verb-per-subcommand CLI shape (resolve/find/set/validate/emit) in a sibling tool.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — config debugging; relevance: `path resolve`/`validate` are the OpenClaw equivalent of inspecting an effective config value.
- [cc_settings_files](../claude_code/cc_settings_files.md) — settings files; relevance: the JSON config files the `set`/`resolve` verbs read and write.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI reference; relevance: another coding-agent CLI with structured (JSON) output modes.
- [hermes_profile_commands_reference](../hermes_agent/hermes_profile_commands_reference.md) — Hermes profile/config commands; relevance: sibling CLI surface for reading/setting config values.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — settings field reference; relevance: the addressable config keys the verbs target.

**Repos**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: hosts the `oc-path` plugin and CLI.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/bundle tree; relevance: `oc-path` is a bundled optional plugin enabled via `plugins enable oc-path`.

**Snippets**
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — CLI config-set; relevance: direct analog of `path set <oc-path> <value>`.
- [snippet_hermes_agent_cli_config_load](../../code_snippets/snippet_hermes_agent_cli_config_load.md) — CLI config load; relevance: analog of `path resolve` reading a value.
- [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migrate/round-trip; relevance: analog of `path emit` byte-fidelity round-trip.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — OpenClaw CLI command routing; relevance: how a plugin-registered subcommand group is dispatched.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — JSONL index read; relevance: the JSONL `find`/`resolve` line-record path in practice.
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — frontmatter parse; relevance: the `[frontmatter]` markdown recipe.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — JSONL event ledger; relevance: the append (`+`) JSONL recipe and predicate find.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin enable/disable; relevance: `plugins enable oc-path` is the enable step before first use.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config edit + reload; relevance: the `--dry-run`/`--diff` preview-before-apply workflow.

### oc_cli_plugins_install (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw plugins install` is its plugin install surface.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: npm is the default + fallback install source (`npm:<package>`, managed per-plugin npm projects).
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — scoped `@org/*` packages; relevance: raw `@openclaw/*` specs resolve to the image-owned bundled copy before npm fallback.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: native plugin archives must carry a valid manifest, validated on install.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: installed plugins can declare MCP server support, surfaced post-install.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model/speech provider plugin; relevance: provider plugins are a major install target (`@openclaw/*` providers).
- [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — sibling plugin ecosystem; relevance: analogous install/lifecycle ecosystem in the Hermes corpus.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — supply-chain substitution attack; relevance: bare-name → npm cutover + `--pin` + registry scans mitigate confusion/typosquat risk ("treat installs like running code").
- [Node.js](../../term_dictionary/term_node_js.md) — JS runtime; relevance: installs run in a managed npm project with `--ignore-scripts` under Node's `node_modules` resolution.

**Docs**
- [oc_cli_plugins_manage](oc_cli_plugins_manage.md) — author/inspect plugins (planned, this series); relevance: the management half of the same CLI.
- [oc_cli_policy_configure](oc_cli_policy_configure.md) — configure policy (planned, this series); relevance: `security.installPolicy` (operator-owned) governs installs.
- [oc_cli_sandbox](oc_cli_sandbox.md) — sandbox CLI (planned, this series); relevance: openshell/ssh sandbox backends are plugin-backed installs.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — sibling plugin install/marketplace; relevance: directly analogous install + marketplace model.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — plugin source taxonomy; relevance: the ClawHub/npm/git/archive/marketplace source set in a sibling tool.
- [cc_plugin_install_hints](../claude_code/cc_plugin_install_hints.md) — install hints; relevance: install-time resolution + pinning guidance analog.
- [cc_plugin_dependencies](../claude_code/cc_plugin_dependencies.md) — plugin dependency resolution; relevance: managed dependency install + `dependencyStatus` analog.
- [hermes_plugins_management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin install/manage; relevance: the closest-corpus install/update/uninstall lifecycle.
- [pi_packages](../pi/pi_packages.md) — Pi package install; relevance: another coding-agent's package install model (sources, pinning).
- [cc_marketplace_restrictions](../claude_code/cc_marketplace_restrictions.md) — marketplace allow/deny; relevance: marketplace source rules + remote-source path restrictions analog.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/bundle system; relevance: the install target tree + lifecycle code.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider-plugin family; relevance: a concrete installable provider-plugin set.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard surface; relevance: drives setup-time plugin installs (with install overrides).

**Snippets**
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — install/enable/disable lifecycle; relevance: the core install→enable flow.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/manifest contract; relevance: the `openclaw.plugin.json` + `package.json` agreement verified on install.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — CLI plugins install command; relevance: direct sibling analog of `plugins install`.
- [snippet_hermes_agent_cli_plugins_cmd_remove](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_remove.md) — CLI plugins uninstall; relevance: the `plugins uninstall` counterpart.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discovery/auto-detect; relevance: source auto-detection across local path/archive/bundle kinds.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: manifest validation on install.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: registry-scan / install-policy trust gating ("blocked by a registry scan").
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolution; relevance: resolving whether an install source/spec is trusted.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — setup-time import/install; relevance: the wizard install path with guarded source overrides.
- [snippet_hermes_agent_tools_lazy_deps](../../code_snippets/snippet_hermes_agent_tools_lazy_deps.md) — lazy dependency loading; relevance: dependency-presence checks without importing plugin runtime (`dependencyStatus`).

### oc_cli_plugins_manage (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw plugins` author/inspect/manage verbs.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: `build` writes it, `validate` checks it agrees with the entry export.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — `defineToolPlugin` SDK; relevance: `init` scaffolds a minimal TypeScript SDK tool plugin.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registered tool/command catalog; relevance: `inspect --runtime` reports registered tools/commands/services/methods/routes.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: `inspect` surfaces detected MCP/LSP server support.
- [Microkernel Architecture](../../term_dictionary/term_microkernel_architecture.md) — core + plugin extensions; relevance: the registry/inspect model treats plugins as runtime-classified contributions to a core.
- [Skills](../../term_dictionary/term_skills.md) — agent skill packs; relevance: `doctor`/registry classify skill/bundle contributions (vs `skills search`).

**Docs**
- [oc_cli_plugins_install](oc_cli_plugins_install.md) — install lifecycle (planned, this series); relevance: the lifecycle half of the same CLI.
- [oc_cli_policy_configure](oc_cli_policy_configure.md) — configure policy (planned, this series); relevance: `policy`/`doctor --lint` read the same plugin registry/index.
- [oc_cli_path_commands](oc_cli_path_commands.md) — path verbs (planned, this series); relevance: `inspect --json` is TTY-aware JSON-vs-human like `path`.
- [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — sibling plugin CLI verbs; relevance: the list/inspect/doctor/registry verb set analog.
- [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — manifest schema; relevance: what `build`/`validate` produce and check.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin component types; relevance: the capability/shape classification `inspect` reports (plain/hybrid/hook-only/non-capability).
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — SDK plugin authoring; relevance: the `defineToolPlugin` SDK scaffold `init` writes.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin types/surfaces; relevance: the runtime surface taxonomy (tools/commands/services/hooks) inspect enumerates.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — build-a-plugin tutorial; relevance: the init→build→validate authoring workflow.
- [cc_plugin_directory_structure](../claude_code/cc_plugin_directory_structure.md) — plugin directory layout; relevance: the scaffold layout `init` creates and `validate` inspects.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin runtime/tree; relevance: the runtime `inspect --runtime` loads.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: `doctor`/registry classify skill/bundle contributions.

**Snippets**
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK entry points; relevance: the `defineToolPlugin` entry `init` scaffolds.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: the module-load path `inspect --runtime` triggers.
- [snippet_hermes_agent_cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — CLI plugins list/info; relevance: direct analog of `plugins list`/`info`/`inspect`.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — CLI plugins doctor; relevance: analog of `plugins doctor` load-error/stale-config diagnostics.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discovery; relevance: registry cold-read discovery model.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: what `build` writes and `validate` checks.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK shape `init` scaffolds against.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/manifest contract; relevance: the `package.json` `openclaw.extensions` alignment `build` keeps.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry/manifest model; relevance: the persisted cold registry `plugins registry` inspects/refreshes.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — skills hub registry; relevance: marketplace/registry listing model for plugin/skill packages.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: `inspect` audits trusted-surface declarations (`contracts.trustedToolPolicies`).

### oc_cli_policy_model (10t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: policy is a conformance layer over OpenClaw's own settings.
- [Policy Engine Governance](../../term_dictionary/term_policy_engine_governance.md) — policy-as-governance; relevance: policy IS an enterprise conformance/governance layer authored in `policy.jsonc`.
- [Fine-Grained Access Control](../../term_dictionary/term_fine_grained_access_control.md) — granular permission rules; relevance: rules constrain channels/MCP/models/tools/sandbox/exec posture at fine granularity.
- [FGAC](../../term_dictionary/term_fgac.md) — fine-grained access control (acronym); relevance: the per-category allow/deny rule schema is FGAC over config surfaces.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: `denyRules`, deny-lists, and strict fail-closed `policy-jsonc-invalid` semantics.
- [Data Governance](../../term_dictionary/term_data_governance.md) — data-handling controls; relevance: the data-handling posture domain (redaction, telemetry capture, retention, memory indexing).
- [Data Handling](../../term_dictionary/term_data_handling.md) — data-handling posture; relevance: the `dataHandling.*` policy category mirrors this exact concept.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: `mcp.servers.allow/deny` is a governed surface.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated runtime; relevance: `sandbox.requireMode/allowBackends/containers.*` rules.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config representation; relevance: policy overlays existing OpenClaw config as observed evidence (not a second config system).

**Docs**
- [oc_cli_policy_attestation](oc_cli_policy_attestation.md) — evidence/findings/attestation (planned, this series); relevance: the model half that tests these rules.
- [oc_cli_policy_configure](oc_cli_policy_configure.md) — enable/hash-lock policy (planned, this series); relevance: how this rule model is turned on and pinned.
- [oc_cli_sandbox](oc_cli_sandbox.md) — sandbox CLI (planned, this series); relevance: sandbox posture is a policy domain (`sandbox.*`).
- [cc_managed_settings](../claude_code/cc_managed_settings.md) — managed/enterprise settings; relevance: the enterprise managed-policy-over-config analog.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — admin enforcement; relevance: org-authored conformance/enforcement over agent config, the closest analog.
- [cc_sandbox_org_enforcement](../claude_code/cc_sandbox_org_enforcement.md) — org sandbox enforcement; relevance: org-level sandbox posture enforcement analog of `sandbox.requireMode`.
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — managed permission precedence; relevance: the allow/deny + scoped-overlay strictness model.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security architecture; relevance: the layered posture surfaces (network/exec/fs/tools) policy governs.
- [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — restrict model providers; relevance: direct analog of `models.providers.allow/deny`.
- [hermes_managed_scope](../hermes_agent/hermes_managed_scope.md) — managed config scope; relevance: org-managed scope over agent config in the closest corpus.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/policy subsystem; relevance: implements the policy posture checks.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin tree; relevance: policy ships as a bundled plugin (`plugins enable policy`).

**Snippets**
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny list; relevance: the deny-list tool posture (`tools.denyTools`, `group:runtime`/`group:fs`).
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/fs policy; relevance: matches `tools.exec.*` / `tools.fs.requireWorkspaceOnly`.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool policy; relevance: per-agent tool posture = scoped `agentIds` overlays.
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — openshell backend posture; relevance: `sandbox.allowBackends`/`shell-sandbox` scope evidence.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel DM audit; relevance: `ingress.channels.allowDmPolicies`/`denyOpenGroups` evidence.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: `channels.denyRules[].when.provider` evidence.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node/gateway command policy; relevance: the gateway exposure/HTTP-endpoint governed surfaces.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool approval policy; relevance: the exec-approval / ask-mode posture (`tools.exec.requireAsk`).
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content/SSRF posture; relevance: `network.privateNetwork.allow` SSRF governed surface.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill scanner; relevance: governed-declaration scanning analog (`tools.requireMetadata`).

### oc_cli_policy_attestation (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: the attestation/findings are emitted by `openclaw policy`.
- [Privacy Attestation](../../term_dictionary/term_privacy_attestation.md) — signed conformance claim; relevance: the stable `attestationHash` is the audit claim (policy + evidence + findings, excludes `checkedAt`).
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — audit logging/evidence; relevance: evidence + findings + hashes form the audit tuple recorded by a supervisor.
- [Policy Engine Governance](../../term_dictionary/term_policy_engine_governance.md) — policy-as-governance; relevance: conformance findings are the governance signals on the shared lint surface.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — JSON contract; relevance: the evidence/finding JSON shape (`checkId`/`target`/`requirement`/`severity`).
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: denied-provider / denied-server / unapproved findings are deny-driven.
- [Enforcement Pattern Validation](../../term_dictionary/term_enforcement_pattern_validation.md) — observed-vs-required check; relevance: each check verifies observed config against the required rule and emits a finding.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — provenance/integrity; relevance: hash-locked attestation gives tamper-evident provenance for a release gate.
- [CloudTrail](../../term_dictionary/term_cloudtrail.md) — audit event log; relevance: an analog audit-evidence store a supervisor records the attestation hash into.

**Docs**
- [oc_cli_policy_model](oc_cli_policy_model.md) — rule reference (planned, this series); relevance: the rule definitions these findings test.
- [oc_cli_policy_configure](oc_cli_policy_configure.md) — configure policy (planned, this series); relevance: recording `expectedHash`/`expectedAttestationHash`.
- [oc_cli_path_addressing](oc_cli_path_addressing.md) — `oc://` grammar (planned, this series); relevance: `target`/`requirement` are `oc://` addresses.
- [cc_sandbox_org_enforcement](../claude_code/cc_sandbox_org_enforcement.md) — org enforcement reporting; relevance: org-conformance reporting analog.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — admin enforcement; relevance: the conformance-finding-over-config reporting model.
- [cc_zero_data_retention](../claude_code/cc_zero_data_retention.md) — data-retention attestation; relevance: a privacy/retention conformance-claim analog.
- [cc_enterprise_best_practices](../claude_code/cc_enterprise_best_practices.md) — enterprise hardening; relevance: CI/release-gate conformance practice the attestation feeds.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security architecture; relevance: the evidence surfaces (network/exec/fs/secrets) findings cover.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — security/credential posture; relevance: the secret-provenance evidence findings record (never raw secrets).
- [cc_managed_settings](../claude_code/cc_managed_settings.md) — managed settings; relevance: the managed config whose drift the attestation detects (`policy watch`).

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/policy subsystem; relevance: emits/consumes findings + attestation.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: a gateway/supervisor records the attestation hash to block/approve runtime actions.

**Snippets**
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composing audit findings; relevance: the findings-catalog composition analog.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — read-only vs repair; relevance: the read-only-`check` vs gated-`fix` distinction findings drive.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: exec-posture findings (`policy/tools-exec-*`).
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe execution; relevance: how a check observes evidence then emits a finding.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel DM audit; relevance: `policy/ingress-*` findings.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: `policy/channels-denied-provider` evidence/finding.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — trust findings; relevance: the finding-record shape (id/severity/message/target).
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — gateway method gating; relevance: a supervisor gating actions on the recorded attestation hash.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — JSONL evidence read; relevance: the JSON evidence-payload model the workspace hash covers.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny-list posture; relevance: `policy/tools-required-deny-missing` finding source.

### oc_cli_policy_configure (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: policy config lives under `plugins.entries.policy.config`.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config representation; relevance: `enabled`/`path`/`workspaceRepairs`/`expectedHash` are config keys.
- [Policy Engine Governance](../../term_dictionary/term_policy_engine_governance.md) — policy-as-governance; relevance: this is how the conformance layer is turned on for a workspace.
- [Privacy Attestation](../../term_dictionary/term_privacy_attestation.md) — conformance claim; relevance: `expectedHash`/`expectedAttestationHash` hash-locks pin an accepted clean check.
- [Deny-First](../../term_dictionary/term_deny_first.md) — default-deny posture; relevance: `workspaceRepairs` repair can disable denied channels (fail-closed).
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — audit/CI gating; relevance: `doctor --lint` in CI/release gates is the shared conformance gate.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: the bundled policy plugin entry config (`plugins.entries.policy`).
- [Enforcement Pattern Validation](../../term_dictionary/term_enforcement_pattern_validation.md) — validate-then-fix; relevance: `check`/`compare`/`watch` are read-only validate; `--fix` is gated repair, with per-command exit codes.

**Docs**
- [oc_cli_policy_model](oc_cli_policy_model.md) — rule reference (planned, this series); relevance: what is being configured.
- [oc_cli_policy_attestation](oc_cli_policy_attestation.md) — attestation (planned, this series); relevance: the hashes recorded by config.
- [oc_cli_plugins_install](oc_cli_plugins_install.md) — install plugins (planned, this series); relevance: enabling the bundled policy plugin.
- [oc_cli_sandbox](oc_cli_sandbox.md) — sandbox CLI (planned, this series); relevance: `doctor --fix` migrations are an adjacent repair path.
- [cc_managed_settings](../claude_code/cc_managed_settings.md) — managed settings; relevance: managed-config enable/lock analog of hash-locking.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — admin enforcement; relevance: turning org conformance on + repair behavior.
- [cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md) — managed plugin policy; relevance: enabling a policy plugin via managed config, the closest analog.
- [cc_settings_scopes_and_precedence](../claude_code/cc_settings_scopes_and_precedence.md) — settings precedence; relevance: where the policy config block sits and how includes/overrides resolve.
- [hermes_managed_scope](../hermes_agent/hermes_managed_scope.md) — managed scope; relevance: org-managed enable/lock of agent posture.
- [cc_admin_setup_decision_map](../claude_code/cc_admin_setup_decision_map.md) — admin setup decisions; relevance: deciding when to enable repair (`workspaceRepairs`) after review.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — policy/repair subsystem; relevance: implements `doctor --fix` repair semantics.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin tree; relevance: `plugins.entries.policy` plugin config.

**Snippets**
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — gated `--fix` remediation; relevance: `workspaceRepairs`-gated repair behavior.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config edit + reload; relevance: applying/locking the policy config keys.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — CLI config set; relevance: writing `expectedHash`/`workspaceRepairs` config leaves.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin enable; relevance: `plugins enable policy` prerequisite.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin entry contract; relevance: the bundled policy plugin entry/config-schema contract.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit composition; relevance: the `doctor --lint` shared findings surface this config feeds.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — trust findings; relevance: the lint/findings surface the policy plugin contributes to.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — CLI doctor; relevance: the `doctor --lint`/`--fix` command surface analog.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — gated repair/reset hooks; relevance: the opt-in-gated workspace mutation pattern repair follows.

### oc_cli_proxy (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw proxy` validates its managed-proxy routing + runs the debug capture proxy.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — forward/reverse proxy; relevance: the operator-managed forward/HTTPS proxy + CONNECT tunnels validated.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — intermediary routing; relevance: the proxy-routing posture validated and debugged.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side request forgery defense; relevance: denied-destination + loopback-canary checks are SSRF posture validation.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — child-process execution; relevance: `proxy run -- <cmd>` runs a child command with capture enabled.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config representation; relevance: the effective proxy URL comes from `--proxy-url`, config, or `OPENCLAW_PROXY_URL`.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: `https://` proxy endpoints + `--proxy-ca-file` trust the proxy's TLS.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — pinned-cert trust; relevance: trusting a private CA PEM for the HTTPS proxy connection is a pin-style trust anchor.

**Docs**
- [oc_cli_policy_model](oc_cli_policy_model.md) — policy model (planned, this series); relevance: `network.privateNetwork`/SSRF posture is a policy domain.
- [oc_cli_sandbox](oc_cli_sandbox.md) — sandbox CLI (planned, this series); relevance: sandbox network mode interacts with proxy posture.
- [oc_cli_policy_attestation](oc_cli_policy_attestation.md) — findings (planned, this series); relevance: `policy/network-private-access-enabled` is the conformance counterpart to a proxy denial check.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — sibling proxy/gateway config; relevance: directly analogous proxy/gateway configuration model.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network/TLS/access; relevance: TLS-to-proxy + CA-trust + allowed/denied destination semantics analog.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — cloud network egress; relevance: allowed/denied egress destination validation analog.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — network error diagnosis; relevance: the preflight/validate failure semantics (`exit 1` on config/destination fail).
- [hermes_subscription_proxy](../hermes_agent/hermes_subscription_proxy.md) — Hermes proxy mode; relevance: the closest-corpus managed-proxy routing analog.
- [hermes_messaging_matrix_proxy_mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — proxy-mode transport; relevance: routing transport through a proxy in the closest corpus.
- [cc_claude_platform_on_aws_proxy_and_sdk](../claude_code/cc_claude_platform_on_aws_proxy_and_sdk.md) — platform proxy + SDK; relevance: enterprise forward-proxy preflight analog.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — network/proxy posture; relevance: SSRF + proxy validation logic.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway transport; relevance: the transport the managed proxy fronts (and the debug proxy captures).

**Snippets**
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client CONNECT-through-proxy; relevance: the CONNECT-tunnel path `validate`/`--apns-reachable` exercises.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — proxy-URL resolution from config/env; relevance: the `--proxy-url`/`OPENCLAW_PROXY_URL` resolution analog.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — gateway TLS pinning; relevance: trusting a CA for the HTTPS proxy TLS connection.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity TLS; relevance: the TLS-to-endpoint trust the `--proxy-ca-file` flag configures.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC protocol envelope; relevance: the transport traffic the debug capture proxy inspects.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — connectivity preflight; relevance: the reachability-probe pattern `proxy validate` implements.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime config broadcast; relevance: where managed-proxy config is resolved at runtime.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — APNs/webhook verification; relevance: the APNs reachability probe (`403 InvalidProviderToken` = success) signal model.
- [snippet_hermes_agent_gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — HTTP middleware; relevance: the local debug proxy intercept/capture layer analog.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content/SSRF posture; relevance: the denied-destination / private-network deny semantics the proxy validates.

### oc_cli_qr (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw qr` builds the pairing payload from gateway config.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — short-lived bearer token; relevance: the setup code carries an opaque short-lived `bootstrapToken` + operator-handoff token, not the shared gateway token.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: token/password gateway auth resolution determines the payload's `auth`.
- [Fine-Grained Access Control](../../term_dictionary/term_fine_grained_access_control.md) — granular permissions; relevance: the operator-handoff token is scoped to `operator.approvals/read/talk.secrets/write` only.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret store; relevance: gateway auth SecretRefs are resolved from the active snapshot via `secrets.resolve`.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: mobile routes over `ws://`/`wss://` gateway URLs (fail-closed for public `ws://`).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — device/peer pairing; relevance: this is the mobile-node pairing handshake (scan → approve).
- [Device ID](../../term_dictionary/term_device_id.md) — device identity; relevance: post-scan `devices list`/`approve <requestId>` keys on the requesting device.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — mDNS/`.local` discovery; relevance: `.local` Bonjour hosts remain supported over `ws://` for LAN pairing.

**Docs**
- [oc_cli_policy_model](oc_cli_policy_model.md) — policy model (planned, this series); relevance: gateway exposure/remote posture (relevant to remote QR) is a policy domain.
- [oc_cli_proxy](oc_cli_proxy.md) — proxy CLI (planned, this series); relevance: remote QR over `wss://`/Tailscale shares the gateway-transport reachability concern.
- [oc_cli_reset](oc_cli_reset.md) — reset CLI (planned, this series); relevance: a `creds`/`full` reset clears the auth material the QR payload encodes.
- [cc_remote_control](../claude_code/cc_remote_control.md) — remote-control pairing; relevance: the closest sibling analog of remote-device pairing/handoff.
- [cc_authentication](../claude_code/cc_authentication.md) — auth flows; relevance: token vs password auth-mode resolution analog.
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — remote OAuth handoff; relevance: short-lived-token remote-onboarding analog.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: remote-URL + auth resolution for a remote client.
- [hermes_desktop_remote_backend](../hermes_agent/hermes_desktop_remote_backend.md) — remote backend pairing; relevance: `--remote` gateway-URL/Tailscale Serve/Funnel routing analog.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth/token; relevance: another coding-agent's token/credential resolution model.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth troubleshooting; relevance: the fail-fast/version-skew (`secrets.resolve` unknown-method) failure modes.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway subsystem; relevance: generates the QR/setup-code payload from gateway config.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — mobile/node apps; relevance: the mobile node app that scans the QR and pairs.

**Snippets**
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token-vs-password auth-mode resolution; relevance: how the payload's `auth` is chosen (mode inference rules).
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android gateway WS session; relevance: the paired mobile device's `ws://`/`wss://` transport.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing flow; relevance: the `devices list`/`approve` pairing approval step.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS gateway pairing; relevance: the mobile-side scan-and-pair flow.
- [snippet_hermes_agent_gw_pairing](../../code_snippets/snippet_hermes_agent_gw_pairing.md) — gateway pairing; relevance: the closest-corpus pairing-handshake analog.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef credential resolution; relevance: resolving gateway auth SecretRefs from the active snapshot.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — short-lived auth ticket; relevance: the opaque short-lived `bootstrapToken` model.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch + scopes; relevance: the bounded operator-handoff token scope grant.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — iOS push/operator approvals; relevance: the `operator.approvals` scope the handoff token grants.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — remote URL/config resolution; relevance: `gateway.remote.url`/Tailscale serve|funnel remote-URL source for `--remote`.

### oc_cli_reset (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw reset` wipes its local state (keeps the CLI installed).
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config representation; relevance: `config` scope resets local config.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret/credential store; relevance: `config+creds+sessions` removes credential stores.
- [Authentication](../../term_dictionary/term_authentication.md) — auth material; relevance: the creds scope clears auth/login material.
- [Deny-First](../../term_dictionary/term_deny_first.md) — confirmation-gated destructive op; relevance: scope-gated, confirmation-required (`--yes`/`--non-interactive`) fail-closed destructive action.
- [Data Governance](../../term_dictionary/term_data_governance.md) — data-handling/retention; relevance: a `full` state/retention wipe is a data-handling action (backup-first guidance).
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: `config+creds+sessions`/`full` removes persisted session state.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — stored credential set; relevance: the credential stores the creds scope clears.

**Docs**
- [oc_cli_sandbox](oc_cli_sandbox.md) — sandbox CLI (planned, this series); relevance: sandbox runtimes live in state a `full` reset clears.
- [oc_cli_policy_configure](oc_cli_policy_configure.md) — configure policy (planned, this series); relevance: the post-reset re-enable/repair flow.
- [oc_cli_qr](oc_cli_qr.md) — qr CLI (planned, this series); relevance: re-pairing is needed after a creds/full reset clears auth.
- [cc_uninstall](../claude_code/cc_uninstall.md) — uninstall/clean; relevance: the closest sibling analog (reset keeps the CLI; uninstall removes it).
- [hermes_updating_uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update/uninstall; relevance: state-removal vs binary-removal distinction analog.
- [hermes_cli_commands_ops_maintenance_auth](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — ops/maintenance/auth CLI; relevance: clearing auth/credential state via CLI, the closest-corpus analog.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — credential pools; relevance: the credential stores a creds-scope reset removes.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth/login reset; relevance: clearing auth state to recover login, analogous to creds reset.
- [cc_settings_files](../claude_code/cc_settings_files.md) — settings/config files; relevance: the config files a `config`-scope reset wipes.
- [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential/fs controls; relevance: the credential + filesystem state scopes a reset clears.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/setup wizard; relevance: reset is the inverse of the setup the wizard performs.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session subsystem; relevance: session state removed by `config+creds+sessions`/`full`.

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup writes config; relevance: setup writes the config a reset wipes (inverse op).
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup imports/state; relevance: the local state directories reset removes.
- [snippet_hermes_agent_cli_backup_save](../../code_snippets/snippet_hermes_agent_cli_backup_save.md) — backup create; relevance: `openclaw backup create` first (backup-first guidance).
- [snippet_hermes_agent_cli_backup_restore](../../code_snippets/snippet_hermes_agent_cli_backup_restore.md) — backup restore; relevance: restoring the snapshot a pre-reset backup created.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session reset/compact; relevance: the session-state removal of `config+creds+sessions`/`full`.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — perform session reset; relevance: the destructive state-removal mutation reset performs.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — reset helper hooks; relevance: the confirmation/`--dry-run`-gated removal pattern.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — auth credential storage; relevance: the credential store the creds scope clears.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — login/logout state; relevance: the auth material a creds reset removes.

### oc_cli_sandbox (9t · 10s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — gateway product; relevance: `openclaw sandbox` manages its isolated agent runtimes.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: the core subject — isolated agent runtimes inspected/recreated.
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — runtime backend selector; relevance: `docker`/`ssh`/`openshell` backends (`agents.defaults.sandbox.backend`).
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the default `docker` backend (image/recreate after image change).
- [OpenShell](../../term_dictionary/term_openshell.md) — OpenShell sandbox backend; relevance: the `openshell` backend whose `remote` workspace `recreate` deletes/reseeds.
- [Configuration Model](../../term_dictionary/term_configuration_model.md) — config representation; relevance: `agents.defaults.sandbox.*` (mode/backend/scope/docker/prune) config.
- [Fine-Grained Access Control](../../term_dictionary/term_fine_grained_access_control.md) — granular permissions; relevance: `explain` reports effective workspace access + sandbox tool policy + elevated gates.
- [Deny-First](../../term_dictionary/term_deny_first.md) — security isolation posture; relevance: agents run isolated "for security" — the deny-by-default isolation stance.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell; relevance: the `ssh` backend (target/workspaceRoot/identity material) whose remote workspace `recreate` reseeds.

**Docs**
- [oc_cli_policy_model](oc_cli_policy_model.md) — policy model (planned, this series); relevance: `sandbox.*` is a policy domain (`requireMode`/`allowBackends`/`containers.*`).
- [oc_cli_plugins_install](oc_cli_plugins_install.md) — install plugins (planned, this series); relevance: openshell/ssh backends are plugin-backed installs.
- [oc_cli_path_commands](oc_cli_path_commands.md) — path verbs (planned, this series); relevance: `sandbox explain --json` is TTY-aware JSON-vs-human output.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox runtime/containers; relevance: directly analogous sandbox-container runtime model.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — sandbox modes; relevance: the off/non-main/all mode model (`sandbox.mode`).
- [cc_sandbox_settings](../claude_code/cc_sandbox_settings.md) — sandbox config; relevance: the `sandbox.*` config keys `recreate` re-applies.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — fs/network isolation; relevance: the workspace-access + network-mode isolation `explain` reports.
- [cc_sandbox_limitations_and_troubleshooting](../claude_code/cc_sandbox_limitations_and_troubleshooting.md) — sandbox troubleshooting; relevance: when/why to `recreate` after config drift (stale runtimes).
- [pi_containerization](../pi/pi_containerization.md) — Pi containerization; relevance: another coding-agent's container-runtime management model.
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — terminal/exec backends; relevance: the docker/ssh/remote backend selection analog in the closest corpus.
- [cc_sandbox_org_enforcement](../claude_code/cc_sandbox_org_enforcement.md) — org sandbox enforcement; relevance: the org-mandated sandbox posture `explain`/policy reports against.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox/openshell isolation subsystem; relevance: implements the sandbox/openshell runtimes.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway/runtime registry; relevance: the runtime registry `recreate` uses (vs manual backend cleanup).

**Snippets**
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — OpenShell backend; relevance: the OpenShell sandbox backend `recreate` manages.
- [snippet_openclaw_security_openshell_cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — OpenShell CLI; relevance: the openshell `from`/`mode`/`policy` config `recreate` re-applies.
- [snippet_openclaw_security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — OpenShell fs bridge; relevance: the remote-workspace seed/reseed `recreate` triggers.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — docker environment; relevance: the `docker` backend container lifecycle.
- [snippet_hermes_agent_tools_environments_ssh](../../code_snippets/snippet_hermes_agent_tools_environments_ssh.md) — ssh environment; relevance: the `ssh` backend remote-workspace model.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — code-exec sandbox; relevance: isolated agent code execution the runtimes provide.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node/runtime command policy; relevance: the runtime registry/policy the gateway manages.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| `oc://` / oc-path addressing scheme | Digested as concept content in `oc_cli_path_addressing` (oc_ doc note). NOT a `term_dictionary` capture — it is a product-specific addressing substrate, the subject of its own doc page. |
| openclaw path / plugins / policy / proxy / qr / reset / sandbox (subcommands) | CLI vocabulary → the respective `oc_cli_*` doc notes. Not term notes. |
| Policy conformance layer / policy.jsonc / attestation tuple / findings / scoped overlays | Digested in `oc_cli_policy_*` notes; link existing `term_policy_engine_governance`, `term_privacy_attestation`, `term_audit_operations`, `term_data_governance` — do NOT recreate. |
| Plugin / bundle / ClawHub / marketplace / plugin index / registry | Digested in `oc_cli_plugins_*`; link existing `term_plugin_manifest`, `term_plugin_sdk`, `term_provider_plugin`, `term_npm`, `term_npm_scoping`. |
| Sandbox runtime / backend (docker/ssh/openshell) / recreate | Digested in `oc_cli_sandbox`; link existing `term_sandbox`, `term_docker`. |
| Managed proxy / debug capture proxy / SSRF posture / APNs reachability | Digested in `oc_cli_proxy`; link existing `term_reverse_proxy`, `term_proxy_pattern`, `term_ssrf_guard`. |
| bootstrapToken / operator-handoff token / setup code / mobile pairing | Digested in `oc_cli_qr`; link existing `term_oauth_token`, `term_authentication`, `term_fine_grained_access_control`. |
| MCP / model provider / channel / agent workspace (policy-governed surfaces) | Link existing `term_mcp`, `term_llm`, `term_claude` — referenced as governed surfaces, not redefined. |

**New `term_dictionary` captures: 0** (matches master expectation). All OpenClaw vocabulary on these pages is
product-specific and digested as `oc_*` doc-note content; every cross-cutting concept already has a substantive
existing term note to link. No genuinely reusable, vault-wide term lacking a home was found. Augment re-runs the
Step 2d new-term scan to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only links existing terms. The
augment's Step 2d scan surfaces a genuinely new reusable term — not expected here.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P1). All 8 gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order/forbidden fields; H1/`## Overview`/`## Related Notes`/`## References`/bold footer; ≤400L/≤2500w/≤6 code; one BB) | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traces to `inbox/openclaw_docs/cli/<page>.md`; no invented flags/findings/codes) | diff vs mirror source |
| G3 | Density + Coverage (within caps; every mapped H2/H3 represented; no over-compression of the policy rule/finding catalogs) | word/code count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected terms + repo/sibling/other per note, each with a relevance statement) | Candidate Cross-References → locked at augment |
| G6 | Broken-link fix (correct relative paths; 0 broken links) | `/tessellum-fix-broken-links` |
| G7 | Discoverability (each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/`) | inlink mapping below |
| G8 | In-degree ≥1 (anti-island; satisfied via `entry_openclaw_docs.md` + repo/term inlinks) | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_path_addressing oc_cli_path_commands oc_cli_plugins_install oc_cli_plugins_manage oc_cli_policy_model oc_cli_policy_attestation oc_cli_policy_configure oc_cli_proxy oc_cli_qr oc_cli_reset oc_cli_sandbox"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + broken-link class
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present (REQUIRE_SOURCE_URL=1)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density caps (frontmatter-stripped word count; fences/2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # G4 sibling-link presence (at least one oc_ sibling link)
  grep -q "($SIBLING_PREFIX" "$f" || echo "$n NO SIBLING ($SIBLING_PREFIX) LINK"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost sweep on all cited note_ids (run after draft):
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
```

## Density Re-Assessment

| # | Note | BB | ~Words | Within caps? |
|---|---|---|---:|---|
| 1 | oc_cli_path_addressing | concept | 700 | ✅ (≤2500w / ≤6 code after split) |
| 2 | oc_cli_path_commands | procedure | 700 | ✅ |
| 3 | oc_cli_plugins_install | procedure | 700 | ✅ |
| 4 | oc_cli_plugins_manage | procedure | 650 | ✅ |
| 5 | oc_cli_policy_model | concept | 750 | ✅ (rule-reference tables condensed, not dropped) |
| 6 | oc_cli_policy_attestation | model | 700 | ✅ (findings catalog summarized as a grouped table) |
| 7 | oc_cli_policy_configure | procedure | 450 | ✅ |
| 8 | oc_cli_proxy | procedure | 550 | ✅ |
| 9 | oc_cli_qr | procedure | 450 | ✅ |
| 10 | oc_cli_reset | procedure | 350 | ✅ |
| 11 | oc_cli_sandbox | procedure | 600 | ✅ |

No note approaches caps. The three over-cap source pages (path 2,591w, plugins 4,017w, policy 5,286w) split per
the Split Decisions so each note stays ≤750w and ≤6 code blocks; the 70 source fences distribute so no note
exceeds 6 (config/policy/path examples reproduced selectively, verbatim).

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (CREATED as master pre-step W1) under the **CLI** section, in a
cl06 cluster: path (×2), plugins (×2), policy (×3), proxy, qr, reset, sandbox. Each new note receives its
entry-point back-link at finalization (the primary G7/G8 inbound source). Per master W2/W3, the hub itself
(handled once at the series level, not per sub-plan).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify + apply at execution; ≥1 per new note for G7/G8):

|---|---|
| `0_entry_points/entry_openclaw_docs.md` (planned, master W1) | → ALL 11 (primary inbound) |
| `areas/code_repos/repo_openclaw.md` | → oc_cli_path_addressing, oc_cli_path_commands |
| `areas/code_repos/repo_openclaw_extensions.md` | → oc_cli_plugins_install, oc_cli_plugins_manage |
| `areas/code_repos/repo_openclaw_security.md` | → oc_cli_policy_model, oc_cli_policy_attestation, oc_cli_policy_configure, oc_cli_proxy, oc_cli_sandbox |
| `areas/code_repos/repo_openclaw_gateway.md` | → oc_cli_qr, oc_cli_proxy, oc_cli_sandbox |
| `areas/code_repos/repo_openclaw_cli_wizard.md` | → oc_cli_reset |
| `resources/term_dictionary/term_sandbox.md` | → oc_cli_sandbox |
| `resources/term_dictionary/term_policy_engine_governance.md` | → oc_cli_policy_model |
| `resources/term_dictionary/term_reverse_proxy.md` | → oc_cli_proxy |
| `resources/term_dictionary/term_plugin_manifest.md` | → oc_cli_plugins_install, oc_cli_plugins_manage |

## Pacing Rules (inherited from master)

Single phase; 8 gates before commit. Cap dynamic-workflow fan-out at ~30 agents/run; embed the per-note contract
manifest in the script. Re-read each source page; reproduce config/policy snippets verbatim. One BB per note.
`git pull --rebase --autostash` before committing; no Claude co-author trailer. Incremental reindex; verify
`note_links` + 0 broken links + in-degree ≥1 before commit; commit+push after the phase.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors ≥8t/≥10s/≥10d) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of the per-note Related Notes mapping at raised floors (≥8 `term_dictionary` terms · ≥10
`code_snippets` · ≥10 docs per note), re-reading all 7 source pages and DB-verifying every cited existing note_id.

**Source re-read (measured 2026-06-21, `wc -w` on `inbox/openclaw_docs/cli/*.md`):** path 2,591 · plugins 4,017 ·
policy 5,286 · proxy 580 · qr 424 · reset 153 · sandbox 811 = **13,862 w** — identical to the plan's Source table
(0 drift; no re-splits required). The three over-cap pages (path/plugins/policy) split per the locked Split
Decisions; all 11 notes stay ≤750 w / ≤6 code.

**What was LOCKED — `## Candidate Cross-References` replaced by `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.**
Per-note grouped Terms / Docs / Repos / Snippets, each link `- [Name](relpath.md) — what it is; relevance: …`:

| # | Note | Terms | Snippets | Docs (≥5 existing + planned sibling) | Repos | Floors met |
|---|---|---:|---:|---:|---:|---|
| 1 | oc_cli_path_addressing | 8 | 10 | 10 (7 existing + 3 oc_) | 2 | YES |
| 2 | oc_cli_path_commands | 8 | 10 | 10 (7 existing + 3 oc_) | 2 | YES |
| 3 | oc_cli_plugins_install | 9 | 11 | 10 (7 existing + 3 oc_) | 3 | YES |
| 4 | oc_cli_plugins_manage | 8 | 11 | 10 (7 existing + 3 oc_) | 2 | YES |
| 5 | oc_cli_policy_model | 10 | 11 | 10 (7 existing + 3 oc_) | 2 | YES |
| 6 | oc_cli_policy_attestation | 9 | 11 | 10 (7 existing + 3 oc_) | 2 | YES |
| 7 | oc_cli_policy_configure | 8 | 10 | 10 (6 existing + 4 oc_) | 2 | YES |
| 8 | oc_cli_proxy | 8 | 10 | 10 (7 existing + 3 oc_) | 2 | YES |
| 9 | oc_cli_qr | 9 | 10 | 10 (7 existing + 3 oc_) | 2 | YES |
| 10 | oc_cli_reset | 8 | 10 | 10 (7 existing + 3 oc_) | 2 | YES |
| 11 | oc_cli_sandbox | 9 | 10 | 11 (8 existing + 3 oc_) | 2 | YES |

`snippet_hermes_agent_acp_event_ledger` + `snippet_openclaw_security_audit_ssrf` were MISSING → substituted with
`snippet_openclaw_acp_event_ledger` / dropped); all 78 distinct cited docs + 12 repos return 1. A full ghost-sweep
planned-this-series notes (correct relative paths; not yet in DB — marked "(planned, this series)"), and
sub-floor (6-8 existing per note).

**New-term scan (Step 2d re-run):** 0 new `term_dictionary` captures — matches master expectation. All OpenClaw
CLI vocabulary on these 7 pages is product-specific (digested as `oc_*` doc-note content) and every cross-cutting
terms now LOCKED into the mapping (e.g. `term_ast`, `term_regex`, `term_openshell`, `term_sandbox_backend`,
`term_ssh`, `term_tls`, `term_tls_pinning`, `term_dependency_confusion`, `term_node_js`, `term_skills`,
`term_microkernel_architecture`, `term_fgac`, `term_grc`, `term_data_handling`, `term_supply_chain`,
`term_cloudtrail`, `term_dm_pairing`, `term_device_id`, `term_bonjour_discovery`, `term_session_persistence`,
`term_credential_pool`). **New-term candidates: NONE** (best-fit glossary N/A; 0 captures).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| Checkpoint | Result | Evidence |
|---|---|---|
| CP1 — Related Notes ≥8 terms + floors | **PASS** | Per-note mapping present; all 11 notes ≥8 terms · ≥10 snippets · ≥10 docs · 2-3 repos; each link carries a `relevance:` statement (no bare links); programmatic count table above. |
| CP2 — 9-GATE present per batch | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect, G6 broken-link-fix, G7/G8 discoverability/in-degree. |
| CP3 — Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | "Entry Point Decision (inherited from master)" contributes 11 rows to `entry_openclaw_docs.md` (CREATED at master pre-step W1; DB-confirmed not-yet-present → correctly "(planned)"); parent-hub back-links handled at series level (W2/W3). |
| CP4 — Size | **PASS** | 11 notes (≤30); single execution phase; no split needed. |
| CP5 — Format derived | **PASS** | Format inherited verbatim from master "Format Definition" (derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora): YAML field order, `# Title` → `## Overview` → body → `## Related Notes` → `## References` → bold footer; forbidden-field list matches term-note list; one BB/note. |
| CP6 — Density | **PASS** | Density Re-Assessment: all 11 notes ≤750 w / ≤6 code after the path/plugins/policy splits; no borderline note unaddressed. |
| CP7 — Sources measured | **PASS** | Re-measured 2026-06-21: 7 pages = 13,862 w, identical to the Source table (ratio 1.00; 0 under-estimation). |
| CP8 — Undigested terms + authoring reqs | **PASS** | "Undigested Terms Plan" present (8 rows, all dispositioned to `oc_*` notes or existing-term links); 0 new captures → "Term-Note Authoring Requirements: N/A (0 new terms)" present per master policy; Step 2d re-run confirms 0 new reusable terms. |
| CP8f — Slug/collision | **PASS** | 0 new `term_dictionary` slugs to specificity-audit. Collision audit generalized to ALL 11 planned `oc_*` doc notes (searched `term_dictionary/` AND `documentation/`): each digests a product-specific OpenClaw CLI page (`oc://` substrate, `policy` conformance layer, plugin lifecycle, sandbox CLI) with no existing same-concept term/doc note — cross-cutting concepts are LINKED not recreated; 0 oc_ docs exist yet (DB-confirmed). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
