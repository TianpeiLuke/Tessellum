---
title: Sub-Plan cw01 — OpenClaw Docs: ClawHub (Registry, API, Auth, CLI, Policy)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["clawhub/acceptable-usage", "clawhub/api", "clawhub/auth", "clawhub/cli", "clawhub/content-rights", "clawhub/how-it-works"]
---

# Sub-Plan cw01: ClawHub

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create, the 9-GATE
> validation, cross-references, and entry-point/series-wiring decisions are inherited verbatim from the master.

## Scope

The 6 foundational ClawHub pages: how the registry works (how-it-works), the public REST API v1 (api),
sign-in / API tokens / CLI login (auth), the full `clawhub` CLI command reference (cli), the marketplace
content/behavior policy (acceptable-usage), and the copyright/rights-request flow (content-rights). ClawHub
is the registry layer for OpenClaw skills and plugins — the discovery/publish/install/scan surface the CLI,
gateway, and plugin docs all reference. **Priority P2 (Phase B).** Code-side counterparts
`repo_openclaw_skills`, `repo_openclaw_apps`, and `repo_openclaw_security` are LINKED, not recreated. The
fraud, impersonation, spam) and maps onto existing `term_abuse_*` notes.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| acceptable-usage | clawhub/acceptable-usage | 900 | 0 | 5 | 0 | argument (policy) |
| api | clawhub/api | 560 | 1 | 6 | 0 | model (REST API reference) |
| auth | clawhub/auth | 353 | 5 | 5 | 0 | procedure |
| cli | clawhub/cli | 3,739 | 27 | 2 | 52 | procedure (SPLIT: skill CLI vs package/publisher CLI) |
| content-rights | clawhub/content-rights | 152 | 0 | 0 | 0 | argument (folded into the policy note) |
| how-it-works | clawhub/how-it-works | 500 | 3 | 7 | 0 | concept |

Code-block counts = fence-lines ÷ 2 (api 2/2=1; auth 10/2=5; cli 54/2=27; how-it-works 6/2=3). Total measured
usable words: **6,204** (CLI dominates at 3,739w).

## Content Strategy

- **Prioritize**: the CLI command reference (every publish/install/update/scan/moderation workflow lives here)
  lifecycle) and the API reference are the contracts those workflows run on.
- **Split**: `cli.md` (3,739w > 2,500w cap, 27 fences > 6 cap) splits into a **skill-CLI** note (install/auth/
  search/lifecycle of skills + global flags/config/proxy) and a **package-CLI** note (package/publisher/
  trusted-publisher publish + verify/validate/moderation/telemetry). Each stays ≤2,500w and ≤6 reproduced
  fences (commands reproduced selectively, verbatim).
- **Fold**: `content-rights.md` (152w, 0 H2, a single form-submission flow) is too thin for a standalone note;
  it is folded as the "Content Rights Requests" section of the acceptable-usage policy note (acceptable-usage
  already cross-references it under "## Content rights"). Both are argument-BB governance content.
- **Link-out, do not redefine**: GitHub Actions trusted-publishing / OIDC details, plugin-validation
  remediation codes (`clawhub/plugin-validation-fixes` → cw02), moderation states (`clawhub/moderation` →
  cw02), security/scan internals (`clawhub/security`, `clawhub/security-audits`, `clawhub/telemetry`,
  `clawhub/skill-format` → cw03), and the HTTP-API deep dive (`clawhub/http-api` → cw02) are referenced as
  siblings, not duplicated. Existing terms (`term_oauth_token`, `term_rate_limiting`, `term_rest_api` absent
  → linked alternatives, `term_npm`, `term_supply_chain`, the `term_abuse_*` family) are linked, not redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_clawhub_how_it_works.md` | concept | how-it-works.md (all H2): Registry records, Skills, Plugins, Publishing, Installs and updates, Security state, API access | 550 | What ClawHub is and how its registry records, skill/plugin listings, immutable version publishing, install/update resolution, security/scan state, and public API access fit together. |
| 2 | `oc_clawhub_api.md` | model | api.md (all H2): Public catalog reuse, Auth, Rate limits, Errors, Endpoints, Legacy | 600 | The ClawHub public REST API v1 contract: base URL, public-catalog-reuse rules, Bearer vs anonymous auth, the auth-aware rate-limit buckets + headers, plain-text error conventions, and the public/auth/admin endpoint surface. |
| 3 | `oc_clawhub_auth.md` | procedure | auth.md (all H2): Web sign-in, CLI login, Headless login, Token storage, Revocation | 450 | Authenticating to ClawHub: GitHub web sign-in, the three CLI login flows (browser callback, `--token`, `--device`), where the API token is stored per OS, and how to revoke tokens / recover from 401s. |
| 4 | `oc_clawhub_cli_skills.md` | procedure | cli.md: install (npm/pnpm), Global flags, HTTP proxy, Config file, Commands `login`/`whoami`/`token`/`star`/`search`/`explore`/`inspect`/`install`/`uninstall`/`list`/`pin`/`unpin`/`update`/`skill publish`/`scan`/`scan download`/`delete`/`undelete`/`hide`/`unhide`/`skill rename`/`skill merge`/`transfer` | 850 | The `clawhub` CLI for skill workflows: install + global flags + proxy + config, login/whoami/token, discovery (search/explore/inspect), the install/pin/update lifecycle + lockfile, skill publish + ClawScan, and skill delete/undelete/hide/rename/merge/transfer. |
| 5 | `oc_clawhub_cli_packages.md` | procedure | cli.md: `package explore`/`package inspect`/`package download`/`package verify`/`package validate`/`package delete`/`package undelete`/`package transfer`/`package report`/`package moderation-status`/`package readiness`/`package migration-status`/`publisher create`/`package publish` (+ minimal `package.json`, GitHub Actions)/`package trusted-publisher get|set|delete`/Install telemetry | 850 | The `clawhub` CLI for plugin/package workflows: browse/inspect/download/verify/validate packages, the SHA-256/npm-integrity checks, package publish (folder/tarball/GitHub, minimal `package.json`, reusable GitHub Actions), org publisher + trusted-publisher (OIDC) config, package moderation/readiness/migration status, and install telemetry. |
| 6 | `oc_clawhub_acceptable_usage.md` | argument | acceptable-usage.md (all H2): Allowed content, Disallowed content, Disallowed marketplace behavior, Content rights, Review and enforcement + content-rights.md (folded as the Content Rights Requests subsection) | 700 | ClawHub's marketplace policy: allowed vs disallowed content categories, disallowed marketplace behavior (bulk/low-effort publishing, fake engagement, ban evasion), the copyright/content-rights request flow, and the review-and-enforcement actions (hide/remove/revoke/restrict/ban). |

## Section Coverage Map

```
how-it-works.md → note 1 (oc_clawhub_how_it_works)
├── (intro: registry layer) ──────────────────── → note 1 Overview
├── Registry records ─────────────────────────── → note 1
├── Skills ───────────────────────────────────── → note 1 (link-out: clawhub/skill-format → cw03)
├── Plugins ──────────────────────────────────── → note 1
├── Publishing ───────────────────────────────── → note 1 (link-out: clawhub/publishing → cw02)
├── Installs and updates ─────────────────────── → note 1
├── Security state ───────────────────────────── → note 1 (link-out: security/security-audits/moderation → cw03/cw02)
└── API access ───────────────────────────────── → note 1 (→ note 2; link-out clawhub/http-api → cw02)
api.md → note 2 (oc_clawhub_api)
├── (Base / OpenAPI) ─────────────────────────── → note 2 Overview
├── Public catalog reuse ─────────────────────── → note 2
├── Auth ─────────────────────────────────────── → note 2 (→ note 3 for token lifecycle)
├── Rate limits ──────────────────────────────── → note 2
├── Errors ───────────────────────────────────── → note 2
├── Endpoints (Public read / Auth required / Admin only) → note 2
└── Legacy ───────────────────────────────────── → note 2
auth.md → note 3 (oc_clawhub_auth)
├── Web sign-in ──────────────────────────────── → note 3
├── CLI login ────────────────────────────────── → note 3
├── Headless login ───────────────────────────── → note 3
├── Token storage ────────────────────────────── → note 3
└── Revocation ───────────────────────────────── → note 3
cli.md → notes 4 + 5 (split)
├── (intro: install npm/pnpm, --help/login/whoami) → note 4 Overview
├── Global flags / HTTP proxy / Config file ──── → note 4
├── login / whoami / token ───────────────────── → note 4
├── star / unstar / search / explore / inspect ─ → note 4
├── install / uninstall / list / pin / unpin / update → note 4
├── skill publish (+ GitHub Actions) ─────────── → note 4
├── scan / scan download (+ GitHub Actions) ──── → note 4
├── delete / undelete / hide / unhide ────────── → note 4
├── skill rename / skill merge / transfer ────── → note 4
├── package explore / inspect / download / verify / validate → note 5
├── package delete / undelete / transfer / report → note 5
├── package moderation-status / readiness / migration-status → note 5
├── publisher create ─────────────────────────── → note 5
├── package publish (+ minimal package.json, GitHub Actions) → note 5
├── package trusted-publisher get / set / delete → note 5
└── Install telemetry ────────────────────────── → note 5 (link-out: clawhub/telemetry → cw03)
content-rights.md → note 6 (folded)
└── (entire page: Content Rights Requests form flow) → note 6 "Content Rights Requests" subsection
acceptable-usage.md → note 6 (oc_clawhub_acceptable_usage)
├── (intro) ──────────────────────────────────── → note 6 Overview
├── Allowed content ──────────────────────────── → note 6
├── Disallowed content ───────────────────────── → note 6
├── Disallowed marketplace behavior ──────────── → note 6
├── Content rights ───────────────────────────── → note 6 (merges content-rights.md detail)
└── Review and enforcement ───────────────────── → note 6 (link-out: clawhub/moderation → cw02)
```
No orphaned sections. Sibling ClawHub pages (publishing, moderation, http-api, security, security-audits,
telemetry, skill-format, plugin-validation-fixes) are owned by cw02/cw03 and linked-out, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| cli.md (3,739w, 27 fences, 52 H3) | notes 4 (oc_clawhub_cli_skills) + 5 (oc_clawhub_cli_packages) | Exceeds the 2,500w word cap AND the 6-code-block cap. The page has two distinct command families — the top-level skill commands (`install`/`search`/`pin`/`skill publish`/`scan`/skill lifecycle) vs the `package …`/`publisher`/`trusted-publisher` plugin-package commands + telemetry. Splitting on that natural boundary keeps each ≤2,500w / ≤6 reproduced fences and keeps one task cluster per note. |
| content-rights.md (152w, 0 H2) | folded into note 6 (oc_clawhub_acceptable_usage) | Too thin for a standalone note (single form-submission flow); same argument BB as the policy note, and acceptable-usage.md already links to it under "## Content rights". Folding avoids a sub-150w orphan and keeps all governance content cohesive. |

## Summary Statistics & Building Block Distribution

- Source pages: **6** (6,204 measured words). New `oc_` notes: **6**. New `term_dictionary` notes: **0**.
- BB distribution: concept ×1 (note 1) · model ×1 (note 2) · procedure ×3 (notes 3, 4, 5) · argument ×1 (note 6).
- Est. digest words ~4,000 (avg ~667/note); all ≤2,500w cap. 36 source fences distribute across the procedure
  notes; commands/config reproduced selectively so each note stays ≤6 reproduced fences.
- Cross-refs (LOCKED 2026-06-21 — see `## Per-Note Related Notes Mapping`): each note carries ≥8
  Per-note locked counts: note 1 8t·11s·10d · note 2 8t·11s·10d · note 3 8t·11s·10d · note 4 8t·11s·10d ·
  note 5 8t·11s·10d · note 6 11t·10s·10d.
- Pages map 1:1 to notes except cli (1→2 split) and content-rights (folded into the policy note): 6 pages → 6 notes.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read 2026-06-21;
> sub-plans do not exist yet and are marked **(planned, this series)** — counted toward the 10-doc floor but

### oc_clawhub_how_it_works (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway that connects chat platforms to coding agents; relevance: ClawHub is OpenClaw's registry layer — the subject's parent system.
- [Software Skills](../../term_dictionary/term_skills.md) — agent-loadable SKILL.md capability bundles; relevance: skills are one of the two registry-record types ClawHub hosts (the Skills H2).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — declarative metadata describing a packaged plugin; relevance: plugin records store compatibility/manifest metadata ClawHub reads before install (the Plugins H2).
- [npm](../../term_dictionary/term_npm.md) — JavaScript package registry + CLI; relevance: ClawHub install sources, immutable versions, and `latest` tags mirror npm semantics directly.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — the trust path from publisher to installed artifact; relevance: registry records carry scan/moderation state precisely to harden the install supply chain.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — review/enforcement of hosted content; relevance: the Security-state H2 describes scan summaries, held/hidden/blocked states.
- [Catalog Trust](../../term_dictionary/term_catalog_trust.md) — confidence signals that a catalog entry is safe/genuine; relevance: download/install/star signals + scan status are exactly the trust signals ClawHub surfaces.

**Docs**
- [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code's plugin system overview; relevance: closest existing analog to ClawHub's listing/install model for a coding agent.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — marketplace + install resolution in Claude Code; relevance: parallels ClawHub's discover→install→update registry flow.
- [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — where Claude Code resolves plugin sources from; relevance: mirrors ClawHub's explicit install-source-as-source-of-truth model.
- [cc_marketplace_json_schema](../claude_code/cc_marketplace_json_schema.md) — marketplace catalog record schema; relevance: analogous to ClawHub's registry-record metadata fields.
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — agent-managed skills hub in the Hermes ecosystem; relevance: a sibling skills-registry concept downstream of OpenClaw.
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin packaging/loading system; relevance: parallels ClawHub's plugin package records + compatibility metadata.
- [pi_packages](../pi/pi_packages.md) — package/extension model in the pi coding agent; relevance: another coding-agent registry/package precedent.
- [oc_clawhub_api](oc_clawhub_api.md) — ClawHub public REST API v1 **(planned, this series, note 2)**; relevance: the API-access H2 points here for programmatic discovery/download.
- [oc_clawhub_cli_skills](oc_clawhub_cli_skills.md) — `clawhub` skill CLI **(planned, this series, note 4)**; relevance: the install/publish workflows this concept describes are run via the CLI.
- [oc_clawhub_acceptable_usage](oc_clawhub_acceptable_usage.md) — ClawHub marketplace policy **(planned, this series, note 6)**; relevance: the Security-state H2 links to acceptable usage + moderation.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills code; relevance: implements the skill-registry side ClawHub records.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw apps/plugin packaging; relevance: implements the plugin/package records ClawHub stores.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the gateway whose install/update commands use ClawHub as a source.

**Snippets**
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — skills-hub registry client; relevance: code-level of a skill registry record + version listing.
- [snippet_hermes_agent_tools_skills_hub_install](../../code_snippets/snippet_hermes_agent_tools_skills_hub_install.md) — hub install path; relevance: shows registry-as-source install resolution.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — CLI skill install; relevance: the install/update-from-registry workflow this concept describes.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — SKILL.md manifest parsing; relevance: ClawHub reads SKILL.md frontmatter for skill metadata (the Skills H2).
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract/metadata; relevance: plugin compatibility/artifact metadata in registry records.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/version lifecycle; relevance: install/update + version-record handling.
- [snippet_hermes_agent_optional_skills_registry](../../code_snippets/snippet_hermes_agent_optional_skills_registry.md) — optional-skills registry; relevance: registry catalog of installable skills.
- [snippet_hermes_agent_skills_index_cache](../../code_snippets/snippet_hermes_agent_skills_index_cache.md) — skills index cache; relevance: caching of registry listings for discovery.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill security scanner; relevance: the scan/moderation state surfaced on listings (Security-state H2).

### oc_clawhub_api (8t · 11s · 10d)

**Terms**
- [REST](../../term_dictionary/term_rest.md) — resource-oriented HTTP API style; relevance: ClawHub API v1 is a REST API with resource endpoints — the note's core BB.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — front door enforcing auth/rate/routing for an API; relevance: ClawHub's auth-aware enforcement + rate buckets are gateway-pattern behaviors.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request-rate caps per identity; relevance: the Rate-limits H2 defines per-IP/per-key buckets + `Retry-After`.
- [Throttling](../../term_dictionary/term_throttling.md) — slowing/rejecting excess requests; relevance: `429` + jittered retry handling is the client-side throttling contract.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential proving identity to an API; relevance: write/account endpoints require `Authorization: Bearer clh_...`.
- [Caching](../../term_dictionary/term_caching.md) — storing responses to avoid re-fetching; relevance: the Public-catalog-reuse H2 explicitly says cache responses and respect `429`/`Retry-After` instead of polling aggressively.
- [Access Control](../../term_dictionary/term_access_control.md) — who may call which endpoint; relevance: the public-read / auth-required / admin-only endpoint tiers + "do not bypass auth boundaries" are access-control gating.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller identity; relevance: the Auth H2 distinguishes anonymous read vs Bearer write.

**Docs**
- [hermes_dashboard_rest_api](../hermes_agent/hermes_dashboard_rest_api.md) — Hermes dashboard REST API reference; relevance: closest existing REST-API-reference doc analog (endpoint + auth conventions).
- [hermes_api_server_endpoints](../hermes_agent/hermes_api_server_endpoints.md) — Hermes API server endpoint surface; relevance: parallel public/auth endpoint enumeration.
- [band_rest_api_introduction](../band/band_rest_api_introduction.md) — Band REST API intro (base URL, auth, conventions); relevance: same shape as ClawHub's base/OpenAPI/auth/error conventions.
- [band_agent_api_messages_events](../band/band_agent_api_messages_events.md) — Band agent API endpoints; relevance: another REST endpoint-catalog precedent with pagination.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — Claude Code server/usage-limit (429) errors; relevance: maps to ClawHub's rate-limit + `429`/`Retry-After` semantics.
- [cc_cost_tracking](../claude_code/cc_cost_tracking.md) — usage/cost tracking via headers/telemetry; relevance: parallels rate-limit headers + usage-aware consumption guidance.
- [cc_otel_configuration_variables](../claude_code/cc_otel_configuration_variables.md) — header/telemetry config; relevance: HTTP header conventions analog for the rate-limit header set.
- [oc_clawhub_auth](oc_clawhub_auth.md) — ClawHub token lifecycle **(planned, this series, note 3)**; relevance: the Auth H2 defers token creation/storage/revocation to this note.
- [oc_clawhub_how_it_works](oc_clawhub_how_it_works.md) — ClawHub registry concept **(planned, this series, note 1)**; relevance: the API-access concept originates in how-it-works.
- [oc_clawhub_http_api](oc_clawhub_http_api.md) — ClawHub HTTP API deep dive **(planned, this series, cw02)**; relevance: the full HTTP-API surface this v1 overview links out to.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw apps/server; relevance: hosts the API surface for package/plugin endpoints.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the gateway consuming ClawHub read APIs for install/update.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills; relevance: backs the `/skills` endpoint family.

**Snippets**
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — HTTP request handler; relevance: code-level of REST endpoint dispatch + error handling.
- [snippet_hermes_agent_gw_platform_signal_rate_limit](../../code_snippets/snippet_hermes_agent_gw_platform_signal_rate_limit.md) — platform rate limiter; relevance: per-identity rate-bucket enforcement like ClawHub's per-IP/per-key buckets.
- [snippet_quip_exporter_rate_limiter](../../code_snippets/snippet_quip_exporter_rate_limiter.md) — client-side rate limiter; relevance: respecting `429`/`Retry-After` from a consuming client.
- [snippet_hermes_agent_core_retry_utils](../../code_snippets/snippet_hermes_agent_core_retry_utils.md) — retry/backoff utilities; relevance: the jittered-retry client guidance in the Rate-limits H2.
- [snippet_hermes_agent_core_conversation_loop_rate_limit_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_rate_limit_recovery.md) — rate-limit recovery loop; relevance: `Retry-After`-driven recovery behavior.
- [snippet_hermes_agent_core_conversation_loop_special_retries](../../code_snippets/snippet_hermes_agent_core_conversation_loop_special_retries.md) — special-case retry handling; relevance: handling `429` vs other HTTP error codes.
- [snippet_hermes_agent_core_error_classifier_taxonomy](../../code_snippets/snippet_hermes_agent_core_error_classifier_taxonomy.md) — HTTP error classification; relevance: the Errors H2's `400/401/403/404/429` plain-text taxonomy.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — API connectivity probe; relevance: client-side handling of API base URL + auth checks.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth + rate-limit install policy; relevance: combines Bearer auth with rate enforcement as ClawHub does.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — auth ticket for API access; relevance: Bearer-token-gated endpoint access pattern.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — token storage for API calls; relevance: where the Bearer token used by write endpoints is held.

### oc_clawhub_auth (8t · 11s · 10d)

**Terms**
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller identity; relevance: the note's core BB — ClawHub sign-in + token-based CLI auth.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: GitHub web sign-in + browser-callback CLI login are OAuth-style flows.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer API credential; relevance: ClawHub `clh_...` API tokens are the credential created/stored/revoked here.
- [PKCE](../../term_dictionary/term_pkce.md) — proof-key code exchange for public clients; relevance: the loopback-callback CLI login is the PKCE-style public-client pattern.
- [Access Control](../../term_dictionary/term_access_control.md) — who may do what; relevance: deleted/banned/disabled accounts cannot sign in or use tokens (account-standing gating).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the parent gateway; relevance: ClawHub auth is the credential layer OpenClaw install/publish workflows use.
- [Session Hijacking](../../term_dictionary/term_session_hijacking.md) — stealing a valid session/token; relevance: token storage paths + revocation are the defense against token theft.
- [Credential Stuffing](../../term_dictionary/term_credential_stuffing.md) — replaying stolen credentials; relevance: revocation + `401` handling are the credential-abuse mitigations.

**Docs**
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code authentication; relevance: closest analog — coding-agent sign-in + API-token flows.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/auth troubleshooting; relevance: maps to the Revocation H2's 401 recovery + re-login guidance.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth + network errors; relevance: firewall/VPN/proxy callback-failure case → headless flow.
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — MCP OAuth/token auth; relevance: browser-callback + token storage pattern parallel.
- [cc_sdk_mcp_auth_and_errors](../claude_code/cc_sdk_mcp_auth_and_errors.md) — SDK auth + error handling; relevance: `401 Unauthorized` handling + token refresh parallel.
- [pi_provider_auth](../pi/pi_provider_auth.md) — pi provider auth/token model; relevance: another coding-agent token-auth precedent with storage paths.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — credential pool/storage; relevance: token storage + config-path management analog.
- [oc_clawhub_cli_skills](oc_clawhub_cli_skills.md) — `clawhub` skill CLI **(planned, this series, note 4)**; relevance: `login`/`whoami`/`token` commands documented there reuse this auth.
- [oc_clawhub_api](oc_clawhub_api.md) — ClawHub REST API **(planned, this series, note 2)**; relevance: the Bearer token created here authorizes the API's write endpoints.
- [oc_clawhub_cli_packages](oc_clawhub_cli_packages.md) — `clawhub` package CLI **(planned, this series, note 5)**; relevance: trusted-publisher/OIDC publish is the keyless successor to long-lived tokens.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — OpenClaw CLI/setup wizard; relevance: implements the CLI login/token onboarding flows.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security; relevance: token revocation + account-standing enforcement live here.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: consumes ClawHub tokens for authenticated registry workflows.

**Snippets**
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — CLI login/logout; relevance: code-level of `clawhub login` / re-login on `401`.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — loopback OAuth callback server; relevance: the `127.0.0.1` temporary callback server in the CLI-login H2.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — token storage on disk; relevance: the per-OS config.json token storage in the Token-storage H2.
- [snippet_hermes_agent_cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — auth provider state; relevance: tracking signed-in account state like ClawHub session.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE device/browser auth; relevance: the `--device` one-time-code flow analog.
- [snippet_hermes_agent_cli_web_reveal_oauth](../../code_snippets/snippet_hermes_agent_cli_web_reveal_oauth.md) — web OAuth reveal/token; relevance: web-UI token creation handed to the CLI (headless `--token`).
- [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — auth config-dir doctor; relevance: per-OS config path resolution + override.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: env-var override (`CLAWHUB_CONFIG_PATH`) of stored token.
- [snippet_hermes_agent_tools_mcp_oauth_manager](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth_manager.md) — OAuth token manager; relevance: token creation/refresh/revoke lifecycle.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OpenClaw OAuth profile portability; relevance: portable token/profile storage across hosts (CI/headless).
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: passing a token to a CLI for terminal-only/CI environments.

### oc_clawhub_cli_skills (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent gateway; relevance: the CLI manages OpenClaw skill folders + install sources.
- [Software Skills](../../term_dictionary/term_skills.md) — SKILL.md capability bundles; relevance: every command here operates on skills (search/install/pin/publish).
- [npm](../../term_dictionary/term_npm.md) — package manager; relevance: install is `npm i -g clawhub`; versions/`latest` tags follow npm semantics.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — SKILL.md frontmatter contract; relevance: publish reads the local bundle manifest/fingerprint.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — publisher→install trust path; relevance: pin/lockfile/fingerprint guard the install supply chain.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — review/enforcement; relevance: delete/undelete/hide + ClawScan are moderation-adjacent skill commands.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `login`/`whoami`/`token` manage the API token the CLI uses.
- [Catalog Trust](../../term_dictionary/term_catalog_trust.md) — listing trust signals; relevance: search ranks by slug match + star/install popularity priors.

**Docs**
- [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — Claude Code plugin CLI commands; relevance: closest analog — a coding-agent install/manage CLI surface.
- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI reference; relevance: global-flags/login/whoami CLI-reference pattern.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — marketplace install resolution; relevance: install/update/pin lifecycle parallel.
- [hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md) — creating + publishing a skill; relevance: maps to `skill publish` + dry-run + version bump.
- [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — working-with-skills guide; relevance: search/inspect/install skill workflow parallel.
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — agent-managed skills hub; relevance: registry-managed skill folders outside a full workspace.
- [hermes_optional_skills_catalog](../hermes_agent/hermes_optional_skills_catalog.md) — optional skills catalog; relevance: explore/search discovery surface parallel.
- [pi_cli_reference](../pi/pi_cli_reference.md) — pi CLI reference; relevance: another coding-agent CLI command-reference precedent.
- [oc_clawhub_auth](oc_clawhub_auth.md) — ClawHub auth **(planned, this series, note 3)**; relevance: `login`/`token` reuse the auth flows documented there.
- [oc_clawhub_cli_packages](oc_clawhub_cli_packages.md) — package CLI half **(planned, this series, note 5)**; relevance: sibling split — `package …` commands live there.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/setup wizard; relevance: implements install + login + config behaviors.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills; relevance: the artifacts the skill CLI installs/publishes.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security; relevance: ClawScan (`scan`/`scan download`) backend.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: `openclaw skills install` uses ClawHub as a source.

**Snippets**
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — CLI skill install; relevance: code-level of `install @owner/slug` + extract-to-workdir.
- [snippet_hermes_agent_cli_skills_hub](../../code_snippets/snippet_hermes_agent_cli_skills_hub.md) — skills-hub CLI; relevance: search/explore/inspect registry commands.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — hub registry client; relevance: resolves slug→version→download like `install`/`update`.
- [snippet_hermes_agent_tools_skills_hub_install](../../code_snippets/snippet_hermes_agent_tools_skills_hub_install.md) — hub install path; relevance: registry-source install + lockfile write.
- [snippet_hermes_agent_skills_index_cache](../../code_snippets/snippet_hermes_agent_skills_index_cache.md) — skills index cache; relevance: `list`/`explore` reading cached registry listings.
- [snippet_hermes_agent_tools_skill_manager](../../code_snippets/snippet_hermes_agent_tools_skill_manager.md) — skill manager (pin/update); relevance: pin/unpin/update lifecycle + fingerprint compare.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — SKILL.md manifest format; relevance: `skill publish` reads the bundle manifest/fingerprint.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — CLI login/logout; relevance: the `login`/`whoami` commands at the top of the CLI.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill scanner; relevance: ClawScan invoked by `scan --slug`.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — skills validation; relevance: pre-publish validation of a skill bundle.
- [snippet_hermes_agent_tools_skills_invoke](../../code_snippets/snippet_hermes_agent_tools_skills_invoke.md) — skill invoke; relevance: post-install skill usage the registry folder feeds.

### oc_clawhub_cli_packages (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent gateway; relevance: package commands publish/install OpenClaw plugin packages (ClawPack).
- [npm](../../term_dictionary/term_npm.md) — package manager/integrity; relevance: ClawPack is an npm-pack tarball; download verifies npm `sha512`/shasum.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — `@scope/pkg` namespace ownership; relevance: scoped package names must match the selected publisher owner.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — artifact trust path; relevance: SHA-256 + npm-integrity + trusted-publisher OIDC harden the publish/install supply chain.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — namespace-hijack supply-chain attack; relevance: scope-owner matching + digest verification defend against confusion attacks.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `package.json`/`openclaw.plugin.json` metadata; relevance: publish auto-detects + validates the minimal `package.json` manifest.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK plugins build against; relevance: `package validate` runs the Plugin Inspector against SDK compatibility.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — review/enforcement; relevance: `package report`/`moderation-status`/delete are moderation commands.

**Docs**
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — Claude Code SDK plugins; relevance: closest analog — building/packaging a coding-agent plugin.
- [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — plugin manifest schema; relevance: maps to the minimal `package.json` + `openclaw.compat` fields.
- [cc_marketplace_json_schema](../claude_code/cc_marketplace_json_schema.md) — marketplace record schema; relevance: package metadata fields surfaced on publish.
- [cc_host_and_manage_marketplaces](../claude_code/cc_host_and_manage_marketplaces.md) — host/manage a marketplace (publisher); relevance: parallels `publisher create` + org publisher management.
- [cc_plugin_marketplace_walkthrough](../claude_code/cc_plugin_marketplace_walkthrough.md) — publish walkthrough; relevance: end-to-end publish flow parallel to `package publish`.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — build-a-plugin tutorial; relevance: folder→package build + publish parallel.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin types/surfaces; relevance: `--family code-plugin|bundle-plugin` distinction.
- [pi_packages](../pi/pi_packages.md) — pi package model; relevance: another coding-agent package publish/install precedent.
- [oc_clawhub_cli_skills](oc_clawhub_cli_skills.md) — skill CLI half **(planned, this series, note 4)**; relevance: sibling split — shared global flags/config/auth.
- [oc_clawhub_publishing](oc_clawhub_publishing.md) — ClawHub publishing model **(planned, this series, cw02)**; relevance: owner/review/trusted-publishing details linked from `package publish`.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins; relevance: the plugin packages this CLI publishes/installs.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw apps; relevance: package registry/API backend.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security; relevance: SHA-256/integrity verification + scan/readiness backend.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: `openclaw plugins install clawhub:<package>` consumer.

**Snippets**
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: the package metadata/artifact contract `package publish` produces.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: `openclaw.extensions` entrypoints validated at publish.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: install/version/readiness lifecycle the package commands report.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: what `package validate`'s Plugin Inspector checks against.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the minimal `package.json` fields validated at publish.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command; relevance: `package download` + install-from-registry parallel.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discover/explore; relevance: `package explore` filtered browse.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugin doctor/validate; relevance: `package validate` Plugin Inspector parallel.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — security scanner; relevance: `scan download --kind plugin` + readiness scan-state.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load + digest check; relevance: artifact digest verification before load (SHA-256).

### oc_clawhub_acceptable_usage (11t · 10s · 10d)

**Terms**
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — review/enforcement of hosted content; relevance: the Review-and-enforcement H2 (hide/hold/remove/revoke/ban) is moderation.
- [Abuse Policy](../../term_dictionary/term_abuse_policy.md) — rules defining disallowed behavior; relevance: this note IS ClawHub's acceptable-usage policy.
- [Abuse Detection](../../term_dictionary/term_abuse_detection.md) — identifying abusive activity; relevance: automated checks + statistical abuse signals drive review.
- [Spam Detection](../../term_dictionary/term_spam_detection.md) — flagging spam/mass-posting; relevance: bulk/low-effort publishing + spam bots are disallowed behavior.
- [Impersonation Scam](../../term_dictionary/term_impersonation_scam.md) — pretending to be another party; relevance: non-consensual impersonation + fake personas are disallowed.
- [Brand Impersonation](../../term_dictionary/term_brand_impersonation.md) — misusing another's brand; relevance: misleading users about affiliation/ownership is disallowed.
- [Social Engineering](../../term_dictionary/term_social_engineering.md) — manipulating people into unsafe actions; relevance: scam outreach + deceptive workflows are disallowed.
- [Fraud Detection](../../term_dictionary/term_fraud_detection.md) — catching deceptive financial activity; relevance: fake invoices/deceptive payment flows are disallowed.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — install trust path; relevance: pipe-to-shell / obfuscated install / undeclared secrets are disallowed execution requirements.
- [Counterfeit](../../term_dictionary/term_counterfeit.md) — passing off others' work; relevance: republishing others' skills/code without permission is disallowed (copyright/rights).

**Docs**
- [cc_marketplace_restrictions](../claude_code/cc_marketplace_restrictions.md) — Claude Code marketplace restrictions; relevance: closest analog — what a coding-agent marketplace will not host.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin security guidance; relevance: unsafe-execution/obfuscated-install disallowed-content parallel.
- [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — prompt-injection defenses; relevance: malicious-listing/hidden-execution threat parallel.
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure deployment principles; relevance: consent/review/dry-run framing for allowed content.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security architecture; relevance: defense-in-depth context for review-and-enforcement.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation; relevance: undeclared secret/private-key requirements are disallowed.
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — agent-managed skills hub; relevance: the listing surface these rules govern.
- [oc_clawhub_how_it_works](oc_clawhub_how_it_works.md) — ClawHub registry concept **(planned, this series, note 1)**; relevance: Security-state H2 there links to acceptable usage.
- [oc_clawhub_moderation](oc_clawhub_moderation.md) — moderation + account safety **(planned, this series, cw02)**; relevance: review/enforcement defers reports/holds/bans here.
- [oc_clawhub_security](oc_clawhub_security.md) — ClawHub security/vuln reporting **(planned, this series, cw03)**; relevance: unsafe-content + vulnerability reporting linked from the policy.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security; relevance: implements the abuse signals + enforcement actions.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills; relevance: the skill listings this policy governs.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: the marketplace these rules protect.

**Snippets**
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill security scanner; relevance: automated checks identifying unsafe content.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: scan findings feeding hide/block/revoke enforcement.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content safety checks; relevance: detecting unsafe/obfuscated execution requirements.
- [snippet_openclaw_opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — static-analysis rule compile/validate; relevance: the static-analysis signal behind abuse detection.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — skills install guard; relevance: blocking unsafe/disallowed skill installs.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security advisories surface; relevance: surfacing flagged/blocked listings to users.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — install policy + rate limit; relevance: rate-limit abuse + install-policy enforcement.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — skills validation; relevance: validation gate rejecting misleading/misdeclared listings.
- [snippet_hermes_agent_tools_cronjob_register](../../code_snippets/snippet_hermes_agent_tools_cronjob_register.md) — scheduled-job registration; relevance: detecting automation/self-install loops + fake-engagement scheduling.

**DB-verify ledger (existing targets, all PRESENT — 2026-06-21).** All term/doc/repo/snippet/entry IDs cited
candidate set (all verified present): `term_rest, term_throttling, term_caching, term_access_control,
term_pkce, term_session_hijacking, term_skill_manifest, term_npm_scoping, term_dependency_confusion,
term_social_engineering, term_fraud_detection, term_counterfeit, term_catalog_trust`. New docs added (all
cc_marketplace_json_schema, cc_plugin_manifest_schema, cc_plugin_cli_commands, cc_cli_commands,
cc_login_authentication_troubleshooting, cc_authentication_and_network_errors, cc_mcp_authentication,
cc_sdk_mcp_auth_and_errors, cc_server_and_usage_limit_errors, cc_cost_tracking, cc_otel_configuration_variables,
cc_marketplace_restrictions, cc_security_guidance_plugin, cc_prompt_injection_defenses,
cc_sdk_secure_deployment_principles, cc_security_architecture, cc_host_and_manage_marketplaces,
cc_plugin_marketplace_walkthrough, hermes_dashboard_rest_api, hermes_api_server_endpoints,
hermes_creating_skill_publish, hermes_skills_hub_agent_managed, hermes_optional_skills_catalog,
hermes_work_with_skills_guide, hermes_plugin_types_surfaces, hermes_build_plugin_tutorial,
hermes_plugins_system, hermes_credential_pools, hermes_security_isolation_credentials,
band_rest_api_introduction, band_agent_api_messages_events, pi_packages, pi_cli_reference, pi_provider_auth`.
sets cited per note (56 distinct snippet IDs, all = 1). **Absent (NOT cited — substitute used):**
use `term_counterfeit` + `term_content_moderation`; `term_semantic_versioning`→link `term_npm`;
`entry_openclaw_docs` (= 0, created as master W1 pre-step).

## Undigested Terms Plan

Per master: OpenClaw / ClawHub vocabulary is digested as `oc_*` doc notes by their home page, NOT promoted to
new `term_dictionary` entries; the only `term_dictionary` interaction is linking EXISTING terms.

| Term | Disposition |
|------|-------------|
| ClawHub | Subject of these notes (`oc_clawhub_*`) — not a `term_dictionary` entry; link `term_openclaw`. |
| skill / SKILL.md bundle | Documentation concept (note 1, cw03 skill-format); link existing `term_skills`. |
| plugin / package / ClawPack | Documentation concept (notes 1, 5); link `term_plugin_manifest`, `term_plugin_sdk`, `term_npm`. |
| ClawScan / security scan / scan download | Documentation concept (notes 4, 5; cw03 security-audits); link `term_content_moderation`, `term_supply_chain`. |
| API token / `clh_` Bearer / `--device` login | Documentation concept (notes 2, 3); link `term_oauth_token`, `term_authentication`, `term_oauth`. |
| rate-limit buckets / `Retry-After` / `429` | Documentation concept (note 2); link `term_rate_limiting`, `term_api_gateway`. |
| trusted publisher / OIDC / `publisher create` | Documentation concept (note 5); link existing terms (`term_oauth`, `term_supply_chain`); no new term. |
| impersonation / non-consensual identity / NSFW / fraud / scam | Policy concept (note 6); link `term_impersonation_scam`, `term_brand_impersonation`, `term_phishing`, `term_credit_card_fraud`. |
| supply-chain / pipe-to-shell / obfuscated install / SHA-256 / npm integrity | Policy + procedure concept (notes 5, 6); link `term_supply_chain`. |
| content rights / copyright / DMCA-style request | Policy concept (note 6, folded); link existing terms; `term_copyright`/`term_dmca` absent but NOT a reusable cross-cutting term worth a new note here (single form flow). |

**New `term_dictionary` captures expected: 0.** No genuinely cross-cutting term lacks both a doc-page home AND
an existing note. Closest borderline candidate is "supply-chain attack / pipe-to-shell installer" — already
covered by the existing `term_supply_chain` note, so link it; do not create. (If augment's re-scan disagrees,
the best-fit glossary is `acronym_glossary_security_*.md` / `acronym_glossary_abuse_*.md`.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only links existing terms. The
multi-source-research + glossary-update requirement (inherited from master W5) does not apply. If augment
proposes a new term, it must follow the master's `/tessellum-capture-term-note` + acronym-glossary requirement.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (6 notes, P2). Gate table inherited verbatim from the master.

| Gate | Check | Tool / Method | Pass criterion |
|------|-------|---------------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | YAML field order/required fields OK; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; footer present; 0 ERROR/LINK-003. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/clawhub/<page>.md` | every claim traces to source; no invented commands/endpoints/flags. |
| G3 | Density + Coverage | word/code count + section coverage map | each ≤400 lines / ≤2,500 words / ≤6 code blocks; every mapped H2/H3 represented; one BB/note. |
| G4 | Cross-Reference | Related Notes audit | ≥6 relevance-selected terms + repos/siblings/other vault notes, each an indexed link with a relevance statement. |
| G5 | Ghost-reference | detect + redirect | every cited existing note_id resolves in DB; sibling `oc_*` marked planned until created. |
| G6 | Broken-link | `/tessellum-fix-broken-links` after reindex | 0 broken links. |
| G7 | Discoverability | inbound link from outside `documentation/openclaw/` | each new note RECEIVES ≥1 outside-folder inbound link (via `entry_openclaw_docs.md`). |
| G8 | In-degree ≥1 | `note_links` query | every new note has in_degree ≥1 (anti-island). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_clawhub_how_it_works oc_clawhub_api oc_clawhub_auth oc_clawhub_cli_skills oc_clawhub_cli_packages oc_clawhub_acceptable_usage"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density: words (frontmatter excluded) + code blocks
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost / G6 broken-link: run incremental reindex then the broken-link sweep
bash scripts/update_notes_database.sh
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source words | Within caps (≤2500w / ≤6 code / ≤400 L)? |
|---|---|---|---:|---:|---|
| 1 | oc_clawhub_how_it_works | concept | 550 | 500 | ✅ (≤3 reproduced fences) |
| 2 | oc_clawhub_api | model | 600 | 560 | ✅ (1 reproduced fence: the 429 example) |
| 3 | oc_clawhub_auth | procedure | 450 | 353 | ✅ (≤5 reproduced fences) |
| 4 | oc_clawhub_cli_skills | procedure | 850 | ~1,900 (cli half) | ✅ (commands reproduced selectively → ≤6 fences) |
| 5 | oc_clawhub_cli_packages | procedure | 850 | ~1,840 (cli half) | ✅ (commands reproduced selectively → ≤6 fences) |
| 6 | oc_clawhub_acceptable_usage | argument | 700 | 1,052 (acceptable-usage 900 + content-rights 152) | ✅ (0 code) |

The cli split keeps both CLI notes well under the 2,500w cap and the 6-fence cap (the source's 27 fences are
distributed, with commands reproduced selectively, not wholesale). No other note approaches caps.

## Entry Point Decision (inherited from master)

Contributes **6 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step) under a "ClawHub" section
cluster — one row per planned note (notes 1–6). Each new note receives its entry-point back-link at
finalization (satisfies G7/G8). The master also wires W2 (parent hub `entry_gen_ai_dev.md` +

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):
- `entry_openclaw_docs.md` (planned, W1) → all 6 notes (primary discoverability source).
- `repo_openclaw_skills.md` → notes 1, 4 (skill registry/publish).
- `repo_openclaw_apps.md` → notes 1, 2 (registry/API surface).
- `repo_openclaw_security.md` → notes 4, 5, 6 (scan/policy/enforcement).
- `repo_openclaw_extensions.md` → note 5 (plugin packages).
- `repo_openclaw_cli_wizard.md` → notes 3, 4 (CLI login/install).
- `term_openclaw.md` → notes 1, 6; `term_oauth_token.md` → notes 2, 3; `term_content_moderation.md` → note 6;
  `term_supply_chain.md` → notes 5, 6; `term_npm.md` → notes 4, 5.

## Pacing Rules (inherited from master)

One execution phase; all 8 gates pass before commit. Re-read each source page during execution; reproduce
commands/config snippets verbatim and selectively (≤6 fences/note). One BB per note. Cap dynamic-workflow
fan-out at ~30 agents/run; `git pull --rebase --autostash` first; no Claude co-author trailer; reindex
incrementally and verify `note_links` + 0 broken links before commit; commit + push this sub-plan's wave as
one cycle.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope locked.** All 6 source pages re-read from `inbox/openclaw_docs/clawhub/` (measured words match the
Source table exactly: how-it-works 500, api 560, auth 353, cli 3,739, content-rights 152, acceptable-usage
900). The `## Per-Note Related Notes Mapping` was locked at the RAISED xref floors — **≥8 terms · ≥10
ghosts**. Every cited EXISTING note_id (129 distinct: terms, docs, repos, snippets) returned `1` from
relative paths resolve to the expected folders (terms `../../term_dictionary/`, docs `../<folder>/`, repos
`../../../areas/code_repos/`, snippets `../../code_snippets/`). Sibling `oc_*` docs (this/cw02/cw03 series)
(7–8 each).

**Per-note locked counts (terms · snippets · docs · repos · floorsMet):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met (≥8t·≥10s·≥10d) |
|------|------:|---------:|------------------------:|------:|----|
| oc_clawhub_how_it_works | 8 | 11 | 10 (7/3) | 3 | YES |
| oc_clawhub_api | 8 | 11 | 10 (7/3) | 3 | YES |
| oc_clawhub_auth | 8 | 11 | 10 (7/3) | 3 | YES |
| oc_clawhub_cli_skills | 8 | 11 | 10 (8/2) | 4 | YES |
| oc_clawhub_cli_packages | 8 | 11 | 10 (8/2) | 4 | YES |
| oc_clawhub_acceptable_usage | 11 | 10 | 10 (7/3) | 3 | YES |

**Relevance refinement applied during augment (note 2 `oc_clawhub_api`):** replaced two weakly-grounded
terms (`term_idempotency_key`, `term_webhook` — neither appears in `api.md`) with two source-grounded,
respect `429`/`Retry-After`") and `term_access_control` (the public-read / auth-required / admin-only
endpoint tiers + "do not bypass auth boundaries"). Note 2 stays at 8 terms; DB-verify ledger updated to
`term_abuse_detection`, `term_spam_detection`, `term_impersonation_scam`, `term_brand_impersonation`,
false positives — they map 1:1 onto acceptable-usage.md's Disallowed-content / Disallowed-marketplace-
behavior / Review-and-enforcement H2s (all `active`, `building_block: concept`).

**New-term candidates: NONE.** Per the master design decision, OpenClaw/ClawHub vocabulary is digested as
`oc_*` doc notes by their home page, NOT promoted to new `term_dictionary` entries. The re-read surfaced no
genuinely cross-cutting, vault-reusable term lacking BOTH a doc-page home AND an existing note. The closest
borderline ("supply-chain attack / pipe-to-shell installer") is already covered by the existing
`term_supply_chain` → link, do not create. Absent-but-substituted terms confirmed: `term_rest_api`→
+ `term_content_moderation`; `term_semantic_versioning`→`term_npm`. Best-fit glossary if augment ever
disagrees: `acronym_glossary_security_*.md` / `acronym_glossary_abuse_*.md`.

**Entry point:** `entry_openclaw_docs.md` confirmed NOT yet present in the DB (returns 0) — correctly
inherited as the master W1 pre-step that wires all 6 notes' inbound links (G7/G8). Parent/related entry
`entry_code_repos`. Sibling sub-plans `cw02`/`cw03` exist (cross-sub-plan `oc_clawhub_http_api`/
`moderation`/`publishing`/`security` planned references are legitimate).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|------------|--------|----------|
| CP2 | 9-GATE present (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present (G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7 discoverability, G8 in-degree). |
| CP4 | Size | **PASS** | 6 planned notes (1 cli split → 2; 1 fold) — well ≤30; single execution phase. |
| CP5 | Format derived | **PASS** | YAML/body format inherited verbatim from master Format Definition, derived from existing `claude_code/`(`cc_*`) + `pi/`(`pi_*`) doc corpora; `## Overview`/`## Related Notes`/footer convention. |
| CP6 | Density | **PASS** | `## Density Re-Assessment` — every note ≤2,500w / ≤6 fences / ≤400L; cli split keeps both halves under caps; no borderline note unaddressed. |
| CP7 | Sources measured | **PASS** | Re-measured all 6 pages via `wc -w`: 900/560/353/3,739/152/500 — exact match to Source table (ratio 1.0); 0 under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (Pattern: link existing terms, 0 new); `## Term-Note Authoring Requirements` present (N/A — 0 new terms — with master fallback if a term surfaces). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new `term_*` slugs to create (no specificity/collision risk); all referenced terms are EXISTING substantive `active` notes (link, not create) — generalized dedup confirms no `oc_*` doc note duplicates an existing term note. |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks` table maps every new note to ≥1 outside-folder inbound source (`entry_openclaw_docs` + `repo_openclaw*` + linked terms); G7/G8 in gate table mark inlink-addition as an executed/verified phase. |

**RESULT: 9/9 (CP1–CP9 incl. CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
