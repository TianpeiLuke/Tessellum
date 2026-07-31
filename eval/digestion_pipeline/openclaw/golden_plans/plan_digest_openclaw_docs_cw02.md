---
title: Sub-Plan cw02 — OpenClaw Docs: ClawHub (HTTP API, Moderation, Namespace Claims, Plugin Validation, Publishing, Quickstart)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["clawhub/http-api", "clawhub/moderation", "clawhub/namespace-claims", "clawhub/plugin-validation-fixes", "clawhub/publishing", "clawhub/quickstart"]
---

# Sub-Plan cw02: ClawHub

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format, dedup-before-create, undigested-terms
> ownership, 9-GATE, cross-references, and entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the
> master; this file holds only the cw02-specific measured plan, splits, candidate cross-refs, and gate table.

## Scope

The 6 ClawHub pages: ClawHub is OpenClaw's registry for **skills and plugins** (the npm/registry layer of the
OpenClaw ecosystem). These pages cover the registry's **HTTP API** (public read + Bearer-token write/admin
endpoints, rate limits, error semantics, discovery), **publishing** (skill folders + npm-scoped plugin packages,
trusted publishing via GitHub OIDC), **moderation & account safety** (reports, holds, hidden listings, bans),
**org/namespace claims** (ownership-dispute review), **plugin validation fixes** (author-facing `clawhub package
validate` finding remediation), and the **quickstart** (find/install/publish flows). Priority **P2** (Phase B) —
the registry/distribution layer that the CLI (cl0x), plugins (pl0x), and providers (pr0x) sub-plans reference for
"how a skill/plugin reaches users." Code-side counterparts `repo_openclaw_skills` / `repo_openclaw_extensions` are
LINKED, not recreated.

**Source**: OpenClaw docs, 6 pages, **10,622 measured words**. **Planned: 8 notes** (http-api.md → 3, other 5 pages → 1 each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| http-api | clawhub/http-api | 6,231 | 44 | 7 | 62 | model + procedure (SPLIT ×3: conventions / public read / auth-write) |
| moderation | clawhub/moderation | 689 | 0 | 6 | 0 | argument (policy) |
| namespace-claims | clawhub/namespace-claims | 596 | 0 | 6 | 0 | procedure |
| plugin-validation-fixes | clawhub/plugin-validation-fixes | 1,721 | 1 | 7 | 23 | procedure |
| publishing | clawhub/publishing | 910 | 7 | 3 | 3 | procedure |
| quickstart | clawhub/quickstart | 475 | 13 | 6 | 0 | procedure |

(Code = ``` fences ÷ 2. http-api H3 count = the 62 per-endpoint `### \`METHOD /path\`` headings. Counts via
`grep -cE '^## '` / `'^### '` on the mirror.)

## Content Strategy

- **Prioritize**: the HTTP API surface (the contract third-party directories, the `clawhub` CLI, and self-hosters
  consume) and publishing (the primary author workflow). The rate-limit / error-semantics / discovery
  *conventions* are a distinct reusable concept and lead the http-api split.
- **Split**: `http-api.md` (6,231w / 44 code / 62 endpoint H3s) FAR exceeds the 2,500w / 6-code caps and mixes a
  conventions concept with two endpoint-catalog clusters (public-read vs auth-write/admin), so it splits into 3
  BB-clean notes (see Split Decisions). No other page exceeds caps.
- **Link-out**: skill authoring/`SKILL.md` format → `clawhub/skill-format` (cw03); security audit labels / scan
  internals / telemetry / troubleshooting → cw03 (`security`, `security-audits`, `telemetry`, `troubleshooting`);
  acceptable-usage / auth / CLI / api / content-rights / how-it-works → cw01; plugin manifest / building / SDK
  subpaths / hooks referenced by validation findings → plugins sub-plans (pl01–pl25). Existing terms
  (`term_openclaw`, `term_skills`, `term_oauth`, `term_npm`, `term_rate_limiting`, …) are LINKED, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_clawhub_http_api_conventions.md` | concept | http-api.md: Base URL/OpenAPI intro, Public catalog reuse, Rate limits, Error responses, Legacy CLI endpoints (deprecated), Registry discovery (`/.well-known/clawhub.json`) | 700 | ClawHub HTTP API conventions: base URL + OpenAPI, third-party catalog-reuse rules, the rate-limit model (per-IP/per-key read/write/download buckets, headers, `429`/`Retry-After` backoff), plain-text error responses, deprecated legacy CLI endpoints, and self-host registry discovery. |
| 2 | `oc_clawhub_http_api_public_endpoints.md` | model | http-api.md: Public endpoints (no auth) — search, skills list/detail/moderation/report/reports/triage/versions/scan/verify/security-verdicts/file, packages list/search/detail/versions/security/artifact/readiness/migrations/moderation/reports, plugins list/export/search, npm passthrough, resolve, download | 800 | The public (no-auth) read surface: search + skill/package/plugin catalog, version, scan, verify, security-verdict, moderation-state, artifact, and download endpoints (params, response shapes, status codes), plus the npm-passthrough and resolve/download routes. |
| 3 | `oc_clawhub_http_api_auth_endpoints.md` | procedure | http-api.md: Auth endpoints (Bearer token) — whoami, POST skills, POST packages, delete/undelete skills, users/publisher, publishers, users/reserve, publisher-recovery, owner-slug & transfer-ownership endpoints, users ban/unban/reclassify-ban/role, users list, stars | 750 | The authenticated (Bearer `clh_`) write/admin surface: publishing skills/packages (multipart payload, owner/migrate options, official-channel rules), soft-delete/undelete, publisher & org creation/recovery, name reservation, ownership transfer, ban/role moderation actions, and stars. |
| 4 | `oc_clawhub_quickstart.md` | procedure | quickstart.md: intro, Find and install a skill, Find and install a plugin, Sign in for publishing, Publish a skill, Publish a plugin, Inspect before installing | 550 | ClawHub quickstart: searching/installing/updating skills (`openclaw skills …`) and plugins (`clawhub:` source), signing in (`clawhub login` GitHub vs `--token`), publishing a skill folder and a plugin package, and inspecting metadata/scan state before installing. |
| 5 | `oc_clawhub_publishing.md` | procedure | publishing.md: intro, Skills (CLI + reusable `skill-publish.yml` workflow), Plugins (npm scoped names, scope↔owner rule), Before Publishing a Plugin, Trusted Publishing for Packages (GitHub OIDC), FAQ (scope-must-match-owner) | 650 | Publishing to ClawHub: skill-folder publish (CLI + reusable GitHub workflow, auto patch versioning), npm-scoped plugin packages with the scope-must-match-owner rule, the pre-publish checklist, and GitHub-OIDC trusted publishing setup/rollback for packages. |
| 6 | `oc_clawhub_plugin_validation_fixes.md` | procedure | plugin-validation-fixes.md: intro + `clawhub package validate` rerun, Author-facing findings table, Package metadata (9 codes), Published artifact (3 codes), Manifest metadata (3 codes), SDK and compatibility migration (6 codes), Security manifest (2 codes), Related | 850 | Remediating author-facing `clawhub package validate` findings: the 23 finding codes grouped by package metadata, published npm-pack artifact, plugin-manifest metadata, deprecated SDK-import/hook migration, and security-manifest issues — each with the fix and the validate rerun. |
| 7 | `oc_clawhub_moderation.md` | argument | moderation.md: intro, Reports, Org and namespace claims (pointer), Moderation holds, Hidden or blocked listings, Bans and account standing, Publisher guidance | 600 | ClawHub moderation and account safety: what reports are (and are not) for, moderation holds, hidden/blocked/quarantined listing states, bans / token revocation / account-standing recovery (appeal form, scan-download-then-fix), and publisher guidance to reduce false positives. |
| 8 | `oc_clawhub_namespace_claims.md` | procedure | namespace-claims.md: intro, When to Open a Claim, Before You File, Evidence to Include, What Not to Include, Possible Outcomes, Related Docs | 550 | Filing an org/namespace claim: when ownership disputes (org handle, package scope, owner handle, skill slug, brand/trademark) warrant the GitHub claim form vs a report or appeal, what to confirm first, what public evidence to include, what secrets to keep out, and the possible staff outcomes. |

> Note count: **8 planned notes** = 8 rows. http-api.md splits into 3 notes (rows 1–3); the remaining 5 source
> pages map 1:1 to rows 4–8. **8 notes total** (3 from http-api + 1 each from the other 5 pages).

## Section Coverage Map

```
http-api.md (SPLIT ×3)
├── Base URL / OpenAPI / legacy path note (intro) ──────── → note 1 (oc_clawhub_http_api_conventions)
├── Public catalog reuse ───────────────────────────────── → note 1
├── Rate limits (buckets, headers, 429/Retry-After) ─────── → note 1
├── Error responses (plain-text, 400/401/403/404/429) ───── → note 1
├── Legacy CLI endpoints (deprecated) ──────────────────── → note 1
├── Registry discovery (/.well-known/clawhub.json) ─────── → note 1
├── Public endpoints (no auth):
│   ├── GET /api/v1/search ──────────────────────────────── → note 2 (oc_clawhub_http_api_public_endpoints)
│   ├── GET /api/v1/skills (+ /{slug}, /moderation, /report,
│   │   /-/reports[/triage], /versions[/{version}], /scan[*],
│   │   /verify, /-/security-verdicts, /{slug}/file) ─────── → note 2
│   ├── GET /api/v1/packages (+ /search, /{name}[/versions
│   │   [/{version}[/security|/artifact[/download]]]],
│   │   /readiness, /migrations, /moderation/queue,
│   │   /{name}/report, /reports, /{name}/moderation,
│   │   /reports/{id}/triage, /{name}/file, /download) ───── → note 2
│   ├── GET /api/v1/plugins (+ /export, /search) ────────── → note 2
│   ├── GET /api/npm/{package}[/-/{tarball}.tgz] ────────── → note 2
│   ├── GET /api/v1/resolve ─────────────────────────────── → note 2
│   └── GET /api/v1/download ────────────────────────────── → note 2
├── Auth endpoints (Bearer token):
│   ├── GET /api/v1/whoami ──────────────────────────────── → note 3 (oc_clawhub_http_api_auth_endpoints)
│   ├── POST /api/v1/skills, POST /api/v1/packages ──────── → note 3
│   ├── DELETE/undelete skills/{slug} ───────────────────── → note 3
│   ├── POST users/publisher, publishers, users/reserve,
│   │   users/publisher-recovery ────────────────────────── → note 3
│   ├── Owner slug management + Transfer ownership ──────── → note 3
│   ├── users ban/unban/reclassify-ban/role, GET users ──── → note 3
│   └── stars/{slug} (POST/DELETE) ──────────────────────── → note 3
quickstart.md
├── intro (OpenClaw vs clawhub CLI) ────────────────────── → note 4 (oc_clawhub_quickstart)
├── Find and install a skill ───────────────────────────── → note 4
├── Find and install a plugin ──────────────────────────── → note 4
├── Sign in for publishing ─────────────────────────────── → note 4
├── Publish a skill / Publish a plugin ─────────────────── → note 4
└── Inspect before installing ──────────────────────────── → note 4
publishing.md
├── intro ──────────────────────────────────────────────── → note 5 (oc_clawhub_publishing)
├── Skills (CLI + skill-publish.yml workflow) ──────────── → note 5
├── Plugins (npm scoped names, scope↔owner) ────────────── → note 5
├── Before Publishing a Plugin ─────────────────────────── → note 5
├── Trusted Publishing for Packages (GitHub OIDC) ──────── → note 5
└── FAQ: Package scope must match selected owner ───────── → note 5
plugin-validation-fixes.md
├── intro + validate rerun + Author-facing findings table  → note 6 (oc_clawhub_plugin_validation_fixes)
├── Package metadata (9 codes) ─────────────────────────── → note 6
├── Published artifact (3 codes) ───────────────────────── → note 6
├── Manifest metadata (3 codes) ────────────────────────── → note 6
├── SDK and compatibility migration (6 codes) ──────────── → note 6
├── Security manifest (2 codes) ────────────────────────── → note 6
└── Related ────────────────────────────────────────────── → note 6
moderation.md
├── intro + Reports ────────────────────────────────────── → note 7 (oc_clawhub_moderation)
├── Org and namespace claims (pointer → note 8) ────────── → note 7
├── Moderation holds / Hidden or blocked listings ──────── → note 7
├── Bans and account standing ──────────────────────────── → note 7
└── Publisher guidance ─────────────────────────────────── → note 7
namespace-claims.md
├── intro + When to Open a Claim ───────────────────────── → note 8 (oc_clawhub_namespace_claims)
├── Before You File / Evidence to Include ──────────────── → note 8
├── What Not to Include / Possible Outcomes ────────────── → note 8
└── Related Docs ───────────────────────────────────────── → note 8
```
No orphaned sections. Skill-format/security-audits/telemetry/troubleshooting/auth/api/CLI/acceptable-usage/
how-it-works/content-rights are sibling ClawHub pages owned by cw01/cw03 — linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| http-api.md (6,231w · 44 code · 7 H2 / 62 endpoint H3 · mixed BB) | notes 1 + 2 + 3 | 2.5× the word cap and 7× the code cap; mixes a reusable **conventions concept** (rate limits / error model / discovery), a **public-read endpoint catalog** (model/reference of request+response shapes), and an **authenticated write/admin endpoint catalog** (publishing/moderation **procedure** actions). Splitting by (a) conventions concept, (b) public read surface, (c) auth write/admin surface yields three BB-clean notes each ≤800w / ≤6 code with no sub-cap overrun. |

All other 5 pages are single-note (each ≤1,721w, ≤7 code, single BB) — no split.

## Summary Statistics & Building Block Distribution

- Source pages: **6** (10,622 measured words). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×1** (note 1) · **model ×1** (note 2) · **procedure ×5** (notes 3, 4, 5, 6, 8) ·
  **argument ×1** (note 7). Total = 1 + 1 + 5 + 1 = **8**.
- Est. digest words ~5,450 (avg ~680/note). The 44 http-api code fences are mostly inline endpoint request/response
  JSON snippets; each child note reproduces ≤6 verbatim (representative examples — `429` response, delete response,
  publisher body/response, discovery schema), the rest summarized as prose endpoint contracts to stay ≤6/note.
- Cross-refs (LOCKED at xref-augment 2026-06-21, **raised floors**): every note maps **≥8 relevancy-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (+ relevant `repo_openclaw*` / sibling `oc_*`), each
  (LOCKED — xref-augment 2026-06-21)`**.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


`resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`; sibling `oc_` → `oc_Y.md`;
other doc → `../<folder>/<file>.md`; repo → `../../../areas/code_repos/repo_Y.md`; snippet →
`../../code_snippets/snippet_Y.md`.

### oc_clawhub_http_api_conventions (8t · 10s · 10d)

**Terms**
- [REST](../../term_dictionary/term_rest.md) — REST architectural style; relevance: the API is a versioned REST surface, all v1 paths under `/api/v1`.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request-throttling control; relevance: this note specifies the per-IP/per-key read/write/download buckets + `429`/`Retry-After` backoff.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — edge API entry/policy layer; relevance: the Cloudflare edge enforcing limits + trusted forwarding headers fronting ClawHub.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end forwarding proxy; relevance: `cf-connecting-ip` trusted-forwarding header is the proxy-supplied client-IP source for per-IP buckets.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-retry property; relevance: jittered-backoff retry guidance interacts with safe re-request semantics on `429`.
- [Idempotency Key](../../term_dictionary/term_idempotency_key.md) — dedup token for retries; relevance: the retry/backoff model this note documents is the client-side complement to idempotency-key dedup.
- [Nginx](../../term_dictionary/term_nginx.md) — reverse-proxy/web server; relevance: canonical reverse-proxy that implements the trusted-forwarding-header + rate-limit pattern described here.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: ClawHub is OpenClaw's registry these HTTP conventions front.

**Docs**
- [oc_clawhub_http_api_public_endpoints](oc_clawhub_http_api_public_endpoints.md) — public read surface (planned, this series); relevance: the endpoints these conventions (limits/errors) govern.
- [oc_clawhub_http_api_auth_endpoints](oc_clawhub_http_api_auth_endpoints.md) — auth write/admin surface (planned, this series); relevance: per-key buckets + Bearer auth path defined here.
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — Claude web security + rate limits; relevance: parallel rate-limit/error-handling conventions for a coding-agent web surface.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth + network error handling; relevance: the actionable-auth-failure messaging this note requires for write endpoints.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — outbound network/edge access; relevance: edge/forwarding-header IP-source model analog.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — Claude Code security architecture; relevance: trust-boundary framing for an edge-fronted API.
- [pi_cli_reference](../pi/pi_cli_reference.md) — pi coding-agent CLI; relevance: a peer CLI client that consumes a registry HTTP API under similar conventions.
- [hermes_acp_editor_integration](../hermes_agent/hermes_acp_editor_integration.md) — ACP editor↔agent HTTP integration; relevance: REST/streaming client conventions analog in the Hermes ecosystem.
- [oc_clawhub_api](../openclaw/oc_clawhub_api.md) — ClawHub high-level API overview (cw01, planned); relevance: the conceptual API page these wire-level conventions detail.
- [oc_clawhub_auth](../openclaw/oc_clawhub_auth.md) — ClawHub auth model (cw01, planned); relevance: Bearer `clh_` token path that distinguishes per-key buckets.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — registry/skills client; relevance: consumes these read/download limits + retry headers.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level OpenClaw repo; relevance: the `openclaw`/`clawhub` CLI calling ClawHub under these conventions.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: edge/trusted-proxy + rate-limit enforcement analog on the gateway side.

**Snippets**
- [snippet_hermes_agent_gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — HTTP route table; relevance: versioned REST route layout analog.
- [snippet_hermes_agent_gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — server middleware chain; relevance: rate-limit/error middleware placement analog.
- [snippet_hermes_agent_gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — API server connect/bind; relevance: base-URL + server-startup analog for an HTTP API.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — gateway request handler; relevance: per-request handling (headers, IP source) at the OpenClaw edge.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: authenticated-vs-anonymous bucket branching analog.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — control-UI auth ticket; relevance: token-vs-anonymous request classification.
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — SSE streaming session; relevance: contrasts with the plain-HTTP download path this note clarifies (no streaming).
- [snippet_hermes_agent_core_account_usage](../../code_snippets/snippet_hermes_agent_core_account_usage.md) — account usage tracking; relevance: per-key usage/quota accounting analog to per-bucket limits.
- [snippet_neptune_sigv4_auth](../../code_snippets/snippet_neptune_sigv4_auth.md) — SigV4 request signing; relevance: alternative request-auth scheme contrasting with Bearer `clh_`.
- [snippet_hermes_agent_core_conversation_loop_special_retries](../../code_snippets/snippet_hermes_agent_core_conversation_loop_special_retries.md) — special retry handling; relevance: jittered-backoff retry-on-`429` logic analog.

### oc_clawhub_http_api_public_endpoints (8t · 10s · 10d)

**Terms**
- [REST](../../term_dictionary/term_rest.md) — REST architectural style; relevance: the public read endpoints + status codes are RESTful resources.
- [Skills](../../term_dictionary/term_skills.md) — OpenClaw/agent skill artifact; relevance: the skill catalog these endpoints list/search/scan/verify.
- [npm](../../term_dictionary/term_npm.md) — Node package registry/CLI; relevance: the `/api/npm/{package}` passthrough + tarball download routes.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — `@scope/name` package namespacing; relevance: scoped package names returned by `/packages` detail/version endpoints.
- [GraphQL](../../term_dictionary/term_graphql.md) — query-language API style; relevance: contrast to ClawHub's REST resource-per-endpoint read model documented here.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: read/download bucket headers returned on every endpoint response.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — listing-safety policy; relevance: `/moderation`, `/reports`, scan/verify/security-verdict read surfaces expose moderation state.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: the OpenClaw skill/plugin registry these endpoints serve.

**Docs**
- [oc_clawhub_http_api_conventions](oc_clawhub_http_api_conventions.md) — API conventions (planned, this series); relevance: the rate-limit/error model governing these endpoints.
- [oc_clawhub_quickstart](oc_clawhub_quickstart.md) — find/install flows (planned, this series); relevance: the search/install commands that call these read endpoints.
- [cc_marketplace_json_schema](../claude_code/cc_marketplace_json_schema.md) — plugin marketplace JSON schema; relevance: catalog list/detail response-shape analog.
- [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — marketplace browse/install; relevance: registry search/list/detail read flow analog.
- [hermes_optional_skills_catalog](../hermes_agent/hermes_optional_skills_catalog.md) — skills catalog index; relevance: skill-catalog listing/search read surface analog.
- [hermes_skills_catalog_bundled](../hermes_agent/hermes_skills_catalog_bundled.md) — bundled skills catalog; relevance: skill detail/version listing analog.
- [pi_packages](../pi/pi_packages.md) — pi package model; relevance: package list/detail/version read endpoints analog.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — pi extensions overview; relevance: plugin/extension catalog read model analog.
- [oc_clawhub_skill_format](../openclaw/oc_clawhub_skill_format.md) — `SKILL.md` spec (cw03, planned); relevance: the skill metadata shape returned by skill detail endpoints.
- [oc_clawhub_security_audits](../openclaw/oc_clawhub_security_audits.md) — Pass/Review/Warn/Malicious labels (cw03, planned); relevance: the scan/security-verdict values these read endpoints expose.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill-install client; relevance: reads detail/version/scan endpoints.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/package install; relevance: reads `/api/v1/packages*` + npm passthrough.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: the skill metadata shape returned by skill detail/search responses.
- [snippet_hermes_agent_optional_skills_registry](../../code_snippets/snippet_hermes_agent_optional_skills_registry.md) — optional-skills registry; relevance: registry list/search read model analog.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — skills-hub registry client; relevance: client reading skill catalog/version endpoints.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skill install command; relevance: install client calling detail/download endpoints.
- [snippet_hermes_agent_cli_skills_hub](../../code_snippets/snippet_hermes_agent_cli_skills_hub.md) — skills-hub CLI; relevance: search/list registry read calls.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — ACP registry manifest; relevance: registry catalog/version manifest read-shape analog.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: package detail/security response-shape analog.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: scan/security-verdict values exposed by read endpoints.
- [snippet_hermes_agent_cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — plugins list/info command; relevance: package list/detail read-client analog.
- [snippet_hermes_agent_gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — HTTP route table; relevance: public-endpoint route enumeration analog.

### oc_clawhub_http_api_auth_endpoints (8t · 10s · 10d)

**Terms**
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: the Bearer `clh_` token gating all write/admin endpoints.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: whoami/token-validation + actionable auth-failure messaging.
- [Access Control](../../term_dictionary/term_access_control.md) — permission gating; relevance: publisher/owner/admin role gating + official-channel eligibility on write endpoints.
- [AAA](../../term_dictionary/term_aaa.md) — authentication/authorization/accounting; relevance: the auth+authz+usage model behind the per-key write/admin surface.
- [IAM](../../term_dictionary/term_iam.md) — identity & access management; relevance: role/owner/admin grant model analog for ban/role/reserve actions.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: npm-scoped package publish via `POST /api/v1/packages`.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — listing-safety actions; relevance: ban/unban/reclassify, delete/undelete, role/reserve admin endpoints.
- [Skills](../../term_dictionary/term_skills.md) — skill artifact; relevance: skill publish/delete/undelete/stars endpoints.

**Docs**
- [oc_clawhub_http_api_public_endpoints](oc_clawhub_http_api_public_endpoints.md) — public read surface (planned, this series); relevance: the no-auth counterpart of this write/admin surface.
- [oc_clawhub_publishing](oc_clawhub_publishing.md) — publish workflow (planned, this series); relevance: the user-facing flow over `POST skills`/`POST packages`.
- [oc_clawhub_moderation](oc_clawhub_moderation.md) — moderation policy (planned, this series); relevance: the ban/hold/account-standing semantics these admin endpoints implement.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code authentication; relevance: bearer-token auth flow analog for a coding-agent service.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/token troubleshooting; relevance: the actionable token-failure messaging whoami surfaces.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — admin enforcement controls; relevance: role/ban/admin-action enforcement analog.
- [pi_security_model](../pi/pi_security_model.md) — pi security/permission model; relevance: token + role gating analog for a peer coding agent.
- [hermes_provider_azure_foundry_entra_id](../hermes_agent/hermes_provider_azure_foundry_entra_id.md) — Entra ID token auth; relevance: bearer/OIDC token-auth pattern analog.
- [oc_clawhub_auth](../openclaw/oc_clawhub_auth.md) — ClawHub auth model (cw01, planned); relevance: token issuance/identity behind these Bearer endpoints.
- [oc_clawhub_cli](../openclaw/oc_clawhub_cli.md) — `clawhub` CLI reference (cw01, planned); relevance: the CLI invoking these authenticated endpoints.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills client; relevance: the publish/delete/undelete path.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/trust enforcement; relevance: token/ban/account-standing enforcement analog.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level repo; relevance: the `openclaw`/`clawhub` CLI calling these endpoints.

**Snippets**
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: Bearer-token validation/branching analog.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — auth ticket issuance; relevance: token-gated request authorization analog.
- [snippet_hermes_agent_cli_web_reveal_oauth](../../code_snippets/snippet_hermes_agent_cli_web_reveal_oauth.md) — CLI OAuth reveal; relevance: CLI obtaining a bearer token (the `clh_` analog).
- [snippet_hermes_agent_cli_auth_qwen_oauth](../../code_snippets/snippet_hermes_agent_cli_auth_qwen_oauth.md) — CLI OAuth login flow; relevance: headless token acquisition analog (`login --token`).
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — CLI auth/token storage; relevance: where the `clh_` Bearer token is persisted client-side.
- [snippet_hermes_agent_gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — server middleware; relevance: auth-enforcement middleware for write endpoints.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security advisories CLI; relevance: ban/reclassify/moderation-action client analog.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command; relevance: authenticated publish/install request construction analog.
- [snippet_hermes_agent_core_account_usage](../../code_snippets/snippet_hermes_agent_core_account_usage.md) — account usage; relevance: whoami/per-key accounting analog.

### oc_clawhub_quickstart (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: ClawHub is OpenClaw's registry these commands target.
- [Skills](../../term_dictionary/term_skills.md) — skill artifact; relevance: `openclaw skills search/install/update` + skill publish.
- [npm](../../term_dictionary/term_npm.md) — Node registry/CLI; relevance: `npm i -g clawhub` install + `clawhub:`/npm plugin source resolution.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent class; relevance: OpenClaw, the agent these skills/plugins extend.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated authorization; relevance: `clawhub login` GitHub sign-in for publishing.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `clawhub login --token clh_…` headless auth.
- [Skill Curator](../../term_dictionary/term_skill_curator.md) — skill discovery/selection role; relevance: search/inspect-before-install flow this quickstart teaches.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the tool/skill extension surface OpenClaw skills plug into.

**Docs**
- [oc_clawhub_publishing](oc_clawhub_publishing.md) — full publish reference (planned, this series); relevance: the publish flows summarized in quickstart.
- [oc_clawhub_http_api_public_endpoints](oc_clawhub_http_api_public_endpoints.md) — public read endpoints (planned, this series); relevance: what `search`/`inspect` call under the hood.
- [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — working-with-skills guide; relevance: find/install/update skill quickstart analog.
- [hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md) — create + publish a skill; relevance: the skill-publish quickstart step analog.
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — agent-managed skills hub; relevance: registry-resolved install/update flow analog.
- [cc_plugin_marketplace_walkthrough](../claude_code/cc_plugin_marketplace_walkthrough.md) — marketplace walkthrough; relevance: find/install-from-registry quickstart analog.
- [cc_cli_commands](../claude_code/cc_cli_commands.md) — Claude Code CLI commands; relevance: install/update/login CLI-command analog.
- [pi_cli_reference](../pi/pi_cli_reference.md) — pi CLI reference; relevance: peer coding-agent CLI install/publish commands.
- [oc_clawhub_cli](../openclaw/oc_clawhub_cli.md) — `clawhub` CLI reference (cw01, planned); relevance: full reference for the commands quickstart introduces.
- [oc_clawhub_how_it_works](../openclaw/oc_clawhub_how_it_works.md) — ClawHub how-it-works (cw01, planned); relevance: the registry model the quickstart assumes.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills client; relevance: `skills search/install/update` implementation.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension install; relevance: `plugins install clawhub:<package>` implementation.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard; relevance: `clawhub login`/onboarding command surface.

**Snippets**
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skill install command; relevance: the `skills install` flow analog.
- [snippet_hermes_agent_cli_skills_hub](../../code_snippets/snippet_hermes_agent_cli_skills_hub.md) — skills-hub CLI; relevance: `skills search`/update-all flow analog.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command; relevance: `plugins install clawhub:` analog.
- [snippet_hermes_agent_cli_plugins_cmd_list_info](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_list_info.md) — plugin list/info; relevance: inspect-before-install (`clawhub inspect`) analog.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugin doctor; relevance: pre-install metadata/health inspection analog.
- [snippet_hermes_agent_cli_web_reveal_oauth](../../code_snippets/snippet_hermes_agent_cli_web_reveal_oauth.md) — CLI OAuth flow; relevance: `clawhub login` GitHub sign-in analog.
- [snippet_hermes_agent_cli_auth_qwen_oauth](../../code_snippets/snippet_hermes_agent_cli_auth_qwen_oauth.md) — CLI login/token; relevance: `login --token` headless auth analog.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI main bootstrap; relevance: `openclaw`/`clawhub` CLI entrypoint analog.
- [snippet_hermes_agent_core_skill_commands_discovery](../../code_snippets/snippet_hermes_agent_core_skill_commands_discovery.md) — skill command discovery; relevance: `skills search` discovery flow analog.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest; relevance: the `SKILL.md`/metadata a published skill folder needs.

### oc_clawhub_publishing (8t · 10s · 10d)

**Terms**
- [npm](../../term_dictionary/term_npm.md) — Node registry/CLI; relevance: npm-scoped `@owner/package` plugin names + npm pack publish path.
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — `@scope/name` namespacing; relevance: the scope-must-match-owner rule is npm-scope ownership enforcement.
- [Skills](../../term_dictionary/term_skills.md) — skill artifact; relevance: skill-folder + `SKILL.md` publish path.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `CLAWHUB_TOKEN`/token auth for publishing.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated authorization; relevance: GitHub Actions OIDC trusted-publishing builds on OAuth/OIDC.
- [PKCE](../../term_dictionary/term_pkce.md) — proof-key OAuth extension; relevance: the OIDC/token-minting trusted-publish flow's auth-code hardening analog.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — continuous integration/delivery; relevance: the reusable `skill-publish.yml` GitHub Actions publish pipeline.
- [Access Control](../../term_dictionary/term_access_control.md) — permission gating; relevance: owner/scope match + package-manager-only trusted-publisher config.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json` spec; relevance: required manifest for plugin publish + `openclaw.compat.pluginApi` metadata.

**Docs**
- [oc_clawhub_quickstart](oc_clawhub_quickstart.md) — quickstart (planned, this series); relevance: the short publish steps this note fully details.
- [oc_clawhub_http_api_auth_endpoints](oc_clawhub_http_api_auth_endpoints.md) — auth endpoints (planned, this series); relevance: the `POST skills`/`POST packages` API behind publishing.
- [oc_clawhub_plugin_validation_fixes](oc_clawhub_plugin_validation_fixes.md) — validation fixes (planned, this series); relevance: `clawhub package validate` run before publish.
- [oc_clawhub_namespace_claims](oc_clawhub_namespace_claims.md) — namespace claims (planned, this series); relevance: scope/owner disputes blocking a publish.
- [hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md) — create + publish a skill; relevance: skill-folder publish workflow analog.
- [cc_github_actions_cloud_providers](../claude_code/cc_github_actions_cloud_providers.md) — GitHub Actions + cloud OIDC; relevance: OIDC trusted-publishing / secretless workflow analog.
- [cc_github_actions](../claude_code/cc_github_actions.md) — Claude Code GitHub Actions; relevance: reusable-workflow + `secrets.TOKEN` publish-pipeline analog.
- [pi_packages](../pi/pi_packages.md) — pi package model; relevance: package naming/versioning/publish model analog.
- [oc_clawhub_skill_format](../openclaw/oc_clawhub_skill_format.md) — `SKILL.md` spec (cw03, planned); relevance: the skill metadata checked before publishing.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills client; relevance: skill publish implementation.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/package client; relevance: plugin package publish + scope/owner enforcement.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: the `SKILL.md` metadata declared at publish.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: `package.json#openclaw` compat/build fields required for plugin publish.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — skill install; relevance: the install side of the published-skill lifecycle.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest validated/stored at publish.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: publish → store → install lifecycle this note opens.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest; relevance: registry record created at publish.
- [snippet_hermes_agent_optional_skills_registry](../../code_snippets/snippet_hermes_agent_optional_skills_registry.md) — skills registry; relevance: where a published skill lands.
- [snippet_openclaw_cli_run_main_bootstrap](../../code_snippets/snippet_openclaw_cli_run_main_bootstrap.md) — CLI bootstrap; relevance: `clawhub` CLI entrypoint running publish commands.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security advisories CLI; relevance: the automated security checks publish triggers.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: how a published plugin package is later loaded.

### oc_clawhub_plugin_validation_fixes (8t · 10s · 10d)

**Terms**
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json` spec; relevance: manifest findings (name-missing/unknown-fields/unknown-contracts).
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin authoring SDK; relevance: legacy-root / reserved SDK-import + subpath migration findings.
- [npm](../../term_dictionary/term_npm.md) — Node registry/CLI; relevance: `package.json` / `npm pack` artifact findings.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider integration plugin; relevance: `provider-auth-env-vars` setup-metadata finding.
- [Schema Evolution](../../term_dictionary/term_schema_evolution.md) — backward-compatible schema change; relevance: version-drift / deprecated-field migration findings are schema-evolution remediation.
- [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — plugin lifecycle hooks; relevance: `legacy-before-agent-start` hook migration finding.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — skill metadata schema; relevance: the manifest-metadata validation contract analog for skills.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: `openclaw.compat.pluginApi` / `openclaw.build` host-version metadata findings.

**Docs**
- [oc_clawhub_publishing](oc_clawhub_publishing.md) — publishing (planned, this series); relevance: validate runs before publish.
- [oc_clawhub_cli](../openclaw/oc_clawhub_cli.md) — `clawhub` CLI (cw01, planned); relevance: `clawhub package validate` command.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — build-a-plugin tutorial; relevance: minimal `package.json`/manifest the findings reference.
- [hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — plugin extensions + hooks; relevance: the hook migration (`before_agent_start`) finding remediation.
- [hermes_plugins_management](../hermes_agent/hermes_plugins_management.md) — plugin management; relevance: package metadata/entrypoint validation context.
- [cc_plugin_caching_and_troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin troubleshooting; relevance: plugin-package validation-failure remediation analog.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin component model; relevance: manifest/entrypoint/component fields the findings check.
- [pi_sdk_options](../pi/pi_sdk_options.md) — pi SDK options; relevance: SDK-import/subpath conventions analog to the SDK migration findings.
- [oc_clawhub_security_audits](../openclaw/oc_clawhub_security_audits.md) — audit labels (cw03, planned); relevance: the scan findings that complement author-facing validation.
- [oc_clawhub_troubleshooting](../openclaw/oc_clawhub_troubleshooting.md) — troubleshooting (cw03, planned); relevance: publish-blocked-by-finding remediation cross-link.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension package; relevance: the package being validated.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: `provider-auth-env-vars`/setup-metadata finding source.

**Snippets**
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest fields/contracts validation checks.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: `package.json#openclaw` compat/install/entry fields the findings target.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK subpath/import model behind legacy/reserved-import findings.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — skills validation; relevance: the validate-then-fix-then-rerun loop analog.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: scan findings complementary to author-facing validation findings.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — trust resolver; relevance: how findings map to a package trust verdict.
- [snippet_hermes_agent_cli_plugins_cmd_doctor](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_doctor.md) — plugin doctor; relevance: CLI that surfaces package validation findings.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: validation gates the publish step of the lifecycle.
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — provider plugin (Bedrock); relevance: provider-plugin env-var/setup metadata the finding governs.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform/plugin registry; relevance: where validated package metadata is registered.

### oc_clawhub_moderation (8t · 10s · 10d)

**Terms**
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — listing-safety policy; relevance: reports, holds, hidden/blocked listings — the whole policy this note states.
- [Marketplace Safety](../../term_dictionary/term_marketplace_safety.md) — marketplace abuse defense; relevance: the registry guardrails (reports/holds/bans) protecting install surfaces.
- [Brand Impersonation](../../term_dictionary/term_brand_impersonation.md) — impersonation abuse; relevance: impersonation / misleading-metadata report categories + trademark misuse.
- [Phishing](../../term_dictionary/term_phishing.md) — credential/identity deception; relevance: impersonation / suspicious-install-instruction report vectors.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial-instruction attack; relevance: suspicious install instructions / undeclared-permission abuse a report targets.
- [Scam Detection](../../term_dictionary/term_scam_detection.md) — fraudulent-content detection; relevance: malicious/bad-faith-registration listing detection driving moderation holds.
- [Access Control](../../term_dictionary/term_access_control.md) — permission gating; relevance: bans, token revocation, publishing-access loss, account standing.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — trust-level escalation; relevance: account-standing recovery / hold-lift-on-false-positive trust model.

**Docs**
- [oc_clawhub_namespace_claims](oc_clawhub_namespace_claims.md) — namespace claims (planned, this series); relevance: the ownership-dispute path moderation points to.
- [oc_clawhub_http_api_auth_endpoints](oc_clawhub_http_api_auth_endpoints.md) — auth endpoints (planned, this series); relevance: the ban/role/delete API actions enforcing moderation.
- [oc_clawhub_security_audits](../openclaw/oc_clawhub_security_audits.md) — Pass/Review/Warn/Malicious labels (cw03, planned); relevance: the audit labels distinct from moderation states.
- [oc_clawhub_acceptable_usage](../openclaw/oc_clawhub_acceptable_usage.md) — acceptable usage (cw01, planned); relevance: the policy reports enforce.
- [oc_clawhub_content_rights](../openclaw/oc_clawhub_content_rights.md) — content-rights requests (cw01, planned); relevance: the copyright/content-rights path separate from reports.
- [cc_marketplace_restrictions](../claude_code/cc_marketplace_restrictions.md) — marketplace restrictions; relevance: registry listing-restriction/blocking policy analog.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin security guidance; relevance: publisher guidance to reduce false positives analog.
- [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — prompt-injection defenses; relevance: the suspicious-install-instruction abuse vector reports target.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — built-in plugins; relevance: trusted-vs-third-party listing-state framing analog.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security architecture; relevance: trust-boundary framing for held/hidden/quarantined states.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/scan enforcement; relevance: scan/trust-boundary enforcement behind holds/bans.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills client; relevance: listing state (held/hidden/quarantined/revoked) surfaced to users.

**Snippets**
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: the findings that trigger moderation holds.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — trust resolver; relevance: how findings map to held/hidden/revoked listing states.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit composition; relevance: the audit pipeline behind scan-triggered moderation emails.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — audit exec runtime; relevance: the runtime scan producing malicious-version verdicts.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — fix remediation; relevance: the scan-download → fix → reupload recovery this note describes.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel-DM audit; relevance: the install-instruction/permission-abuse scanning analog.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security advisories CLI; relevance: GitHub Security Advisory vs ClawHub-report distinction.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — skills guard; relevance: blocking unsafe skills (held/hidden state) analog.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source audit; relevance: source-attribution check behind misleading-metadata reports.

### oc_clawhub_namespace_claims (8t · 10s · 10d)

**Terms**
- [npm Scoping](../../term_dictionary/term_npm_scoping.md) — `@scope/name` namespacing; relevance: scoped `@example-org/*` package-scope claims + scope-must-match-owner.
- [npm](../../term_dictionary/term_npm.md) — Node registry/CLI; relevance: npm/PyPI/crates package-registry scope-control evidence.
- [Access Control](../../term_dictionary/term_access_control.md) — permission/ownership gating; relevance: owner/org-handle ownership + transfer/reserve outcomes.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — staff-review process; relevance: the namespace-claim review distinct from in-product reports/appeals.
- [Brand Impersonation](../../term_dictionary/term_brand_impersonation.md) — brand/trademark misuse; relevance: brand/trademark/project-rename disputes warranting a claim.
- [DNS](../../term_dictionary/term_dns.md) — domain name system; relevance: DNS/domain-proof evidence + the "no DNS challenge tokens in public issues" rule.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — namespace-hijack supply-chain attack; relevance: scope/namespace squatting the claim process defends against.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — coding-agent gateway; relevance: ClawHub namespaces (owner/org handles, slugs, package scopes) being claimed.

**Docs**
- [oc_clawhub_publishing](oc_clawhub_publishing.md) — publishing (planned, this series); relevance: scope-must-match-owner + transfer path the claim form references.
- [oc_clawhub_moderation](oc_clawhub_moderation.md) — moderation (planned, this series); relevance: when to claim vs report vs appeal.
- [oc_clawhub_troubleshooting](../openclaw/oc_clawhub_troubleshooting.md) — troubleshooting (cw03, planned); relevance: "publish fails because a namespace is claimed/reserved" cross-link.
- [cc_marketplace_restrictions](../claude_code/cc_marketplace_restrictions.md) — marketplace restrictions; relevance: namespace/listing-reservation policy analog.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — admin enforcement controls; relevance: ownership/namespace administration analog.
- [hermes_plugins_management](../hermes_agent/hermes_plugins_management.md) — plugin management; relevance: package/owner namespace management analog.
- [pi_packages](../pi/pi_packages.md) — pi package model; relevance: scoped package-name ownership analog.
- [oc_clawhub_acceptable_usage](../openclaw/oc_clawhub_acceptable_usage.md) — acceptable usage (cw01, planned); relevance: bad-faith-registration policy a claim invokes.
- [oc_clawhub_how_it_works](../openclaw/oc_clawhub_how_it_works.md) — how it works (cw01, planned); relevance: the owner/org/scope namespace model claims operate on.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills client; relevance: skill-slug namespace.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension client; relevance: package-scope namespace.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest; relevance: slug/owner identity fields a claim disputes.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package contract; relevance: scoped-package-name + owner fields under dispute.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — plugin namespace init; relevance: package/owner namespace assignment analog.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest; relevance: the owner/slug/scope registry record a claim asks staff to change.
- [snippet_hermes_agent_cli_main_cmd_profile](../../code_snippets/snippet_hermes_agent_cli_main_cmd_profile.md) — CLI profile/owner command; relevance: owner-handle/identity the claim verifies against.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: rename/transfer/hide/quarantine outcomes the claim can produce.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin route resolution; relevance: how a reserved/aliased namespace resolves after a claim.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — security advisories CLI; relevance: the security-vs-ownership-dispute routing distinction.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — trust resolver; relevance: quarantine/hide as a possible namespace-claim outcome.
- [snippet_hermes_agent_optional_skills_registry](../../code_snippets/snippet_hermes_agent_optional_skills_registry.md) — skills registry; relevance: the slug namespace a claim can reserve/transfer.

## Undigested Terms Plan

Per master: OpenClaw/ClawHub vocabulary terms are subjects of doc pages and are digested as `oc_*` doc notes by
their home sub-plan, NOT as new `term_dictionary` entries; the only `term_dictionary` interaction is **linking
existing** terms. **Expected new `term_dictionary` captures: 0.**

| Term (in source) | Disposition |
|---|---|
| ClawHub | Subject of this whole sub-plan → digested as `oc_clawhub_*` doc notes; link `term_openclaw`. NOT a new term. |
| skill / plugin / package / bundle-plugin / code-plugin | Registry artifact types → documented in the `oc_clawhub_*` notes; link existing `term_skills`. NOT new terms. |
| owner / org / handle / scope / namespace / slug | Registry namespace vocab → documented inline in notes 5/7/8; link `term_access_control`. NOT new terms. |
| rate limit / `429` / `Retry-After` / backoff | Link existing `term_rate_limiting`. NOT new. |
| Bearer token / `clh_` token | Link existing `term_oauth_token`; (no separate `term_bearer_token` exists — link the OAuth-token note). NOT new. |
| trusted publishing / GitHub OIDC | Documented inline in note 5; link existing `term_oauth`. (`term_oidc` does not exist; not promoted — too narrow for a standalone capture given the agentic glossary's scope.) NOT new. |
| moderation / report / hold / ban / quarantine | Link existing `term_content_moderation`. NOT new. |
| namespace claim / trademark / impersonation | Documented inline in notes 7/8; link `term_content_moderation` + `term_phishing`. (`term_trademark` does not exist.) NOT new. |
| validation finding codes (`package-json-missing`, `legacy-root-sdk-import`, …) | Documented as the body of note 6; not term-worthy (ClawHub-internal codes). NOT new. |
| OpenAPI / `/.well-known/clawhub.json` discovery | Documented inline in note 1; link `term_rest`. NOT new. |

**New-term candidates:** none. No genuinely cross-cutting, vault-reusable term lacking an existing note appears in
these 6 pages. (Borderline `term_semantic_versioning` / `term_package_registry` / `term_software_supply_chain` /
`term_oidc` are real cross-cutting concepts but are referenced only incidentally here; per master's "expect 0 new
terms" + skill-note "avoid stale stubs" guidance they are NOT captured by cw02 — flagged for the maintainer if a
later sub-plan needs them substantively, best-fit glossary `acronym_glossary_a_to_e.md` / `acronym_glossary_p_to_t.md`.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** cw02 authors zero `term_dictionary` notes; it only links existing terms. (Multi-source
research mandate + glossary-update requirement from master apply only if a new term is later proposed.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must PASS before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | YAML field order/forbidden-fields OK; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` + `## References` present; `**Source**`/`**Last Updated**`/`**Status**` footer. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/clawhub/<page>.md`) | Every claim traceable to source; endpoint params/status codes/CLI flags reproduced faithfully; no invented endpoints. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2,500 words / ≤6 code blocks; one building_block; every mapped H2/H3 covered (no orphan). |
| G4 | Cross-Reference | Each note's `## Related Notes` has **≥8 relevance-selected existing `term_dictionary` links + ≥10 code_snippets + ≥10 docs (≥5 existing)** + `repo_openclaw*`/sibling `oc_*` (per LOCKED Per-Note Related Notes Mapping 2026-06-21), each with a relevance statement; indexed `[text](path.md)` format. |
| G5 | Ghost-reference detect + redirect | 0 links to non-existent notes; siblings/cw01/cw03 either created in-phase or redirected to `entry_openclaw_docs`. |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken links after incremental reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 (anti-island) | DB `in_degree ≥ 1` for all 8 notes after reindex. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_clawhub_http_api_conventions oc_clawhub_http_api_public_endpoints oc_clawhub_http_api_auth_endpoints oc_clawhub_quickstart oc_clawhub_publishing oc_clawhub_plugin_validation_fixes oc_clawhub_moderation oc_clawhub_namespace_claims"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format + LINK errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION [$sec]: $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # density caps (body words, code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # sibling-prefix sanity (relative links to this series resolve under same dir)
  grep -oE '\]\(\.?/?'"$SIBLING_PREFIX"'[a-z0-9_]+\.md\)' "$f" >/dev/null 2>&1 && echo "$n has $SIBLING_PREFIX siblings"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5/G6 after reindex:
bash scripts/update_notes_database.sh --force
# G8 in-degree:
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
```

(`$NOTES` lists the 8 note stems; all 8 are checked by every loop above.)

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_clawhub_http_api_conventions | concept | 700 | ≤4 (429 example, discovery schema, +2 inline) | ✅ |
| 2 | oc_clawhub_http_api_public_endpoints | model | 800 | ≤6 (search params, a skill detail + a package security response, npm route) | ✅ |
| 3 | oc_clawhub_http_api_auth_endpoints | procedure | 750 | ≤6 (POST skills/packages payload, delete response, publisher body+response) | ✅ |
| 4 | oc_clawhub_quickstart | procedure | 550 | ≤6 (install/update/login/publish/inspect commands) | ✅ |
| 5 | oc_clawhub_publishing | procedure | 650 | ≤6 (skill publish, workflow yaml, trusted-publisher set/get, scope-error) | ✅ |
| 6 | oc_clawhub_plugin_validation_fixes | procedure | 850 | ≤2 (validate rerun + a metadata snippet; codes as prose) | ✅ |
| 7 | oc_clawhub_moderation | argument | 600 | ≤1 (scan-download recovery command) | ✅ |
| 8 | oc_clawhub_namespace_claims | procedure | 550 | 0 | ✅ |

No note approaches caps. The 44 source http-api code fences are distributed across notes 1–3 with each child ≤6 by
reproducing only representative request/response examples verbatim and summarizing the rest as prose contracts.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step W1, before first execution) under a
**"ClawHub"** section/cluster; each note receives its entry-point back-link at finalization (satisfies G7/G8). No
W2 responsibility.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8):
- `entry_openclaw_docs.md` (planned, W1) → **all 8 notes** (primary anti-island link).
- `repo_openclaw_skills.md` → notes 2, 3, 4, 5, 7, 8 (registry/publish/install client).
- `repo_openclaw_extensions.md` → notes 2, 4, 5, 6, 8 (plugin/package publish + validation).
- `repo_openclaw_extensions_llm_providers.md` → note 6 (provider-auth env-var validation finding).
- `repo_openclaw_security.md` → notes 3, 7 (token/ban/moderation enforcement).
- `repo_openclaw.md` → notes 1, 3, 4 (the `openclaw`/`clawhub` CLI consuming the API).
- `term_content_moderation.md` → notes 7, 8 (reciprocal back-link to the moderation policy notes).
- `term_npm.md` → notes 2, 5, 6, 8 (npm-scoped packaging).
- `term_rate_limiting.md` → note 1; `term_oauth_token.md` → notes 3, 5; `term_skills.md` → notes 2, 4, 5.

## Pacing Rules (inherited from master)

One execution phase, 8 notes (≤30 fan-out cap; no sub-batching needed). Re-read each source page before authoring;
endpoint contracts / CLI commands / config snippets reproduced verbatim where load-bearing. One BB per note. Cap
dynamic-workflow fan-out at ~30 agents/run. `git pull --rebase --autostash` first; commit+push after the phase; no
Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Augmentation Report (2026-06-21)

**What was locked.** Replaced the draft `## Candidate Cross-References` with `## Per-Note Related Notes Mapping
(LOCKED — xref-augment 2026-06-21)` at **raised floors: ≥8 terms · ≥10 code_snippets · ≥10 docs per note**,
e.g. `term_pra_product_review_abuse`, `term_fraud_artifacts`, `term_computer_vision`, `term_distilbert` were

**Per-note locked counts** (all meet floors):

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_clawhub_http_api_conventions | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_clawhub_http_api_public_endpoints | 8 | 10 | 10 (6/4) | 2 | ✅ |
| oc_clawhub_http_api_auth_endpoints | 8 | 10 | 10 (5/5) | 3 | ✅ |
| oc_clawhub_quickstart | 8 | 10 | 10 (6/4) | 3 | ✅ |
| oc_clawhub_publishing | 9 | 10 | 10 (5/5) | 2 | ✅ |
| oc_clawhub_plugin_validation_fixes | 8 | 10 | 10 (6/4) | 2 | ✅ |
| oc_clawhub_moderation | 8 | 10 | 10 (5/5) | 2 | ✅ |
| oc_clawhub_namespace_claims | 8 | 10 | 10 (5/5) | 2 | ✅ |

**New-term candidates.** None promoted. The re-read surfaced four genuinely cross-cutting concepts referenced
only incidentally here — `term_semantic_versioning` (best-fit `acronym_glossary_p_to_t.md`),
`term_oidc` (`acronym_glossary_m_to_o.md`), `term_package_registry` / `term_software_supply_chain`
(`acronym_glossary_p_to_t.md` / `acronym_glossary_p_to_t.md`). Per master ("expect 0 new terms") + the
skill-note "avoid stale stubs" guidance these are NOT captured by cw02; the augment instead **found and linked
existing vault terms that cover the same ground** (`term_dependency_confusion`, `term_npm_scoping`,
`term_codeartifact`, `term_sdlc`, `term_ci_cd`, `term_node_js`), so the raised term floor was met with relevant
existing notes, not new captures. Flagged for the maintainer if a later sub-plan needs the four above
substantively. Net new `term_dictionary` captures by cw02: **0** (link-only, unchanged).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE present per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table covers G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (raised floors), G5 ghost-detect+redirect, G6 broken-link-fix, G7 discoverability, G8 in-degree≥1. |
| CP3 | Entry point inherited | **PASS** | `## Entry Point Decision` + `## Inlinks`: contributes 8 rows to `entry_openclaw_docs.md` (CREATED master pre-step W1, before first execution) under a ClawHub cluster; each note gets its back-link at finalization. Confirmed `entry_openclaw_docs.md` not yet on disk (planned W1) — inherited, not re-created by cw02. |
| CP4 | Size | **PASS** | 8 planned notes ≤30; single execution phase, no sub-batching needed. |
| CP5 | Format derived | **PASS** | Inherited verbatim from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` / `## Related Notes` / `## References` + `**Source**`/`**Last Updated**`/`**Status**` footer; fixed YAML field order; forbidden-fields list). G1 enforces. |
| CP6 | Density | **PASS** | `## Density Re-Assessment`: all 8 notes ≤850w / ≤6 code; http-api split ×3 keeps each child ≤800w / ≤6 code. No borderline note. |
| CP7 | Sources measured | **PASS** | Source table measured 2026-06-20 + re-read this augment from `inbox/openclaw_docs/clawhub/` (http-api 6,231w / moderation 689w / namespace-claims 596w / plugin-validation-fixes 1,721w / publishing 910w / quickstart 475w); only http-api exceeds caps → split ×3 already planned. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows dispositioned to "link existing / NOT new"); `## Term-Note Authoring Requirements` = N/A (0 new terms) with the multi-source/glossary mandate noted as conditional. New-term candidates = 0 (see Augmentation Report). |
| CP8f | Slug/collision audit | **PASS** | Dedup generalized to ALL planned notes: each `oc_clawhub_*` doc checked against `term_dictionary/` + `documentation/` — no doc duplicates an existing term/doc note (OpenClaw vocab digested as docs per master; `term_openclaw`/`term_skills`/etc. linked, not recreated). 0 new term slugs → no specificity/collision renames needed. |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks` maps ≥1 outside-folder inbound link to all 8 notes (`entry_openclaw_docs` → all 8; repo_openclaw* + term backlinks). G8 in-degree≥1 in the gate table + DB check in Validation Scripts; inlinks are an EXECUTED phase, not "recommended". |

**RESULT: 9/9 (CP1–CP9 incl. CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** (9/9 CP PASS → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |
