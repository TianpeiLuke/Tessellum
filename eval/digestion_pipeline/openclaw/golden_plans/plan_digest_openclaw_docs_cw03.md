---
title: Sub-Plan cw03 — OpenClaw Docs: ClawHub (Security, Audits, Skill Format, Telemetry, Troubleshooting)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["clawhub/security", "clawhub/security-audits", "clawhub/skill-format", "clawhub/telemetry", "clawhub/troubleshooting"]
---

# Sub-Plan cw03: ClawHub

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create, 9-GATE, cross-refs,
> and entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master; this file re-states only
> what is needed to author + execute these 5 ClawHub pages. Pipeline: this plan → `/tessellum-augment-digestion-plan`
> → `/tessellum-review-digestion-plan` → `/tessellum-execute-digestion-plan`.

## Scope

The 5 ClawHub registry **trust, format, and operations** pages: how to report ClawHub vulnerabilities and when they
are disclosed (`security`), how to read install-time security-audit results — status / risk / findings — and the
ClawScan + VirusTotal + OWASP scanning stack behind them (`security-audits`), the on-disk skill folder format,
required files, GitHub import, and the `SKILL.md` frontmatter / `metadata.openclaw` schema (`skill-format`), the
CLI install telemetry and how to opt out (`telemetry`), and the diagnostic recipes for sign-in / install / publish /
update / API failures (`troubleshooting`). ClawHub is OpenClaw's open-source skill+plugin registry; these pages are
the **safety + publishing reference** a user reads before installing or publishing. **Priority P2 (Phase B).** The
code-side counterparts `repo_openclaw_security` and `repo_openclaw_skills` (and the `snippet_openclaw_security_*` /
`snippet_openclaw_skills_*` snippets) are LINKED, not recreated.

**Source**: OpenClaw docs, 5 pages, **3,047 measured words** (262 + 862 + 962 + 224 + 737). **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| security | clawhub/security | 262 | 0 | 2 | 0 | argument (disclosure policy) |
| security-audits | clawhub/security-audits | 862 | 4 | 7 | 0 | model + concept (split: result schema vs scan stack) |
| skill-format | clawhub/skill-format | 962 | 5 | 9 | 7 | model + procedure (split: folder/format vs frontmatter schema) |
| telemetry | clawhub/telemetry | 224 | 1 | 5 | 1 | procedure (collect + opt-out) |
| troubleshooting | clawhub/troubleshooting | 737 | 8 | 11 | 0 | procedure (diagnostic recipes) |

Code counts are `grep -c '```' / 2` (fences/2): security 0, security-audits 4, skill-format 5, telemetry 1,
troubleshooting 8. Totals: 3,047 words, 18 code blocks across the 5 pages — well within per-note caps after splits.

## Content Strategy

- **Prioritize**: (a) the security-audit **result schema** users act on — audit status (`Pass`/`Review`/`Warn`/
  `Malicious`/`Pending`/`Error`), risk level (`Low`/`Medium`/`High`), and finding severities — plus the
  install-decision checklist; (b) the `SKILL.md` **frontmatter / `metadata.openclaw` schema** publishers must get
  right (it is what the scanner checks for declaration↔behavior coherence); (c) the **troubleshooting** recipes,
  the highest-traffic operational page.
- **Split** (per word-cap / mixed-BB rules): `security-audits.md` (862w, 7 H2, mixed) → a **result schema** note
  (status/risk/findings, the "what to check" checklist) + a **scan-stack concept** note (ClawScan, VirusTotal,
  OWASP Agentic Skills Top 10, what is checked). `skill-format.md` (962w, 9 H2 / 7 H3, mixed) → a **folder/format
  procedure** note (on-disk layout, required/optional files, GitHub import, slugs, versioning, license, paid-skills,
  allowed files) + a **frontmatter schema** note (the `metadata.openclaw` field reference, install specs, env-var
  declarations, the declaration↔behavior coherence rationale).
- **Skip / link-out (NOT redefined here):** ClawHub publishing flow, namespace claims, moderation, HTTP API, and
  `acceptable-usage` are sibling ClawHub pages owned by **cw01/cw02** — link, do not duplicate. CLI command pages
  (`cli/*`, e.g. `clawhub login`, `openclaw plugins install`) are owned by **cl01–cl09** — reference by command name.
  Gateway/agent security (sandboxing, tool policy, exec approvals) is owned by **gw**/**to**/**se** sub-plans. Term
  definitions (`term_prompt_injection`, `term_supply_chain`, `term_oauth`, `term_telemetry-equivalent`) are LINKED,
  never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_clawhub_security.md` | argument | security.md: intro (what to report vs not), Vulnerability disclosure, Related pages | 380 | ClawHub's security reporting + disclosure policy: report ClawHub-platform bugs (site/API/CLI, publishing/integrity, authn/authz/tokens, scanning/moderation) via GitHub Security Advisories on `openclaw/clawhub`, not third-party skill/plugin code; hosted-service vulns are disclosed only on real user impact while user-installed artifacts are always disclosed. |
| 2 | `oc_clawhub_security_audits_results.md` | model | security-audits.md: intro, What to check before installing, Audit status, Risk level, Findings | 600 | The install-time security-audit result schema: the 6 audit statuses (`Pass`/`Review`/`Warn`/`Malicious`/`Pending`/`Error`) vs the 3 risk levels (`Low`/`Medium`/`High`) — "what to do" vs "how much power" — finding severities (`Info`→`Critical`), and the pre-install trust checklist. |
| 3 | `oc_clawhub_security_audits_scan_stack.md` | concept | security-audits.md: What ClawHub checks (artifact-aware coherence, audit-page path), VirusTotal, Risk analysis (ClawScan, OWASP Agentic Skills Top 10) | 560 | How ClawHub produces an audit: the three-part stack (SkillSpector + VirusTotal + ClawScan risk analysis), the coherence question (declared metadata vs actual behavior), VirusTotal vendor-count telemetry, and ClawScan's OWASP-Agentic-Skills-Top-10 lens (prompt injection, tool misuse, credential exposure, excessive agency). |
| 4 | `oc_clawhub_skill_format.md` | procedure | skill-format.md: On disk, GitHub import, `SKILL.md`, Allowed files, Slugs, Versioning + tags, License, Paid skills | 620 | The on-disk ClawHub skill format: required `SKILL.md` (legacy `skill.md`/`skills.md`), optional text files + `.clawhubignore`/`.gitignore`, the stricter web GitHub importer, local `.clawhub/` install/lock metadata, text-only allowed-file allowlist + 50MB bundle limit, slug/publisher-handle rules, semver versioning + tags, the `MIT-0` license requirement, and the no-paid-skills rule. |
| 5 | `oc_clawhub_skill_frontmatter.md` | model | skill-format.md: Frontmatter metadata (Basic, Runtime metadata `metadata.openclaw`, Full field reference, Install specs, Optional environment variables, Why this matters, Example) | 640 | The `SKILL.md` frontmatter schema: basic fields (`name`/`description`/`version`), the `metadata.openclaw` runtime block (`requires.env`/`bins`/`anyBins`/`config`, `primaryEnv`, `envVars` with `required`, `always`, `os`, `install` specs for brew/node/go/uv), and the declaration↔behavior coherence rule the security analysis enforces. |
| 6 | `oc_clawhub_telemetry.md` | procedure | telemetry.md: intro, When telemetry is collected, What we collect (+ What we do not collect), Install counts, Transparency + user controls, How to disable telemetry | 360 | ClawHub CLI install telemetry: when an install event is sent (logged-in + `clawhub install` + not disabled), the minimal `{slug, version}` payload, what is explicitly NOT collected (paths/file contents/logs/prompts), aggregate `installsAllTime`/`installsCurrent` counters, account-delete data removal, and opting out via `CLAWHUB_DISABLE_TELEMETRY=1`. |
| 7 | `oc_clawhub_troubleshooting_auth_install.md` | procedure | troubleshooting.md: `clawhub login` browser never completes, `Unauthorized` (401), `Rate limit exceeded` (429), fails behind a proxy, skill not in search, plugin install fails in OpenClaw, Public API requests fail | 560 | Diagnosing ClawHub sign-in, install, and API failures: stuck browser login (callback `127.0.0.1`, headless `--token`), 401 Unauthorized (re-login, `CLAWHUB_CONFIG_PATH`, revoked token), 429 rate limits (`Retry-After`/`RateLimit-*` headers, shared-egress IPs), proxy variables, missing/held search results (`clawhub inspect`), `openclaw plugins install clawhub:<pkg>` compat, and public-API etiquette. |
| 8 | `oc_clawhub_troubleshooting_publish_sync.md` | procedure | troubleshooting.md: Publish fails (missing metadata, GitHub owner/source, claimed/reserved namespace), `sync` found no skills, `update` refuses local changes | 480 | Diagnosing ClawHub publish/sync/update failures: missing required metadata (`SKILL.md` frontmatter, `package.json` `openclaw.compat.*`, `--dry-run` preview), GitHub owner/source errors (`owner/repo@ref`), claimed/reserved namespaces (scoped-name owner match, namespace-claim issue), `sync --root`/`--dry-run` discovery, and `update --force` vs new-slug/fork for local-change conflicts. |

## Section Coverage Map

```
clawhub/security.md
├── intro (report ClawHub-platform bugs vs third-party skill/plugin code) → note 1 (oc_clawhub_security)
├── Vulnerability disclosure (hosted-service vs user-installed artifacts) → note 1
└── Related pages (→ security-audits, moderation) ───────────────────────→ note 1 (cross-link cw02 moderation)
clawhub/security-audits.md
├── intro (audits help you decide; not a guarantee; see-also) ───────────→ note 2 (oc_clawhub_security_audits_results)
├── What to check before installing (trust checklist) ───────────────────→ note 2
├── Audit status (Pass/Review/Warn/Malicious/Pending/Error) ─────────────→ note 2
├── Risk level (Low/Medium/High; power vs action) ──────────────────────→ note 2
├── Findings (Info→Critical severities; hidden low-confidence) ──────────→ note 2
├── What ClawHub checks (coherence, audit-page path, 3-part stack) ──────→ note 3 (oc_clawhub_security_audits_scan_stack)
├── VirusTotal (vendor-count telemetry) ────────────────────────────────→ note 3
└── Risk analysis (ClawScan, OWASP Agentic Skills Top 10) ───────────────→ note 3
clawhub/skill-format.md
├── On disk (required/optional files, .clawhubignore/.gitignore) ────────→ note 4 (oc_clawhub_skill_format)
├── GitHub import (web importer rules, local .clawhub/ metadata) ────────→ note 4
├── `SKILL.md` (markdown + frontmatter, description→summary) ────────────→ note 4
├── Frontmatter metadata (Basic) ───────────────────────────────────────→ note 5 (oc_clawhub_skill_frontmatter)
│   ├── Runtime metadata (`metadata.openclaw`) ──────────────────────────→ note 5
│   ├── Full field reference (requires/primaryEnv/envVars/always/os/...) → note 5
│   ├── Install specs (brew/node/go/uv) ────────────────────────────────→ note 5
│   ├── Optional environment variables (envVars required:false) ─────────→ note 5
│   ├── Why this matters (declaration↔behavior coherence) ───────────────→ note 5
│   └── Example: complete frontmatter ──────────────────────────────────→ note 5
├── Allowed files (text-only allowlist, 50MB limit, embedding cap) ──────→ note 4
├── Slugs (folder-derived, publisher-handle/npm-safe rules) ─────────────→ note 4
├── Versioning + tags (semver, `latest`) ───────────────────────────────→ note 4
├── License (`MIT-0`, no overrides) ────────────────────────────────────→ note 4
└── Paid skills (not supported) ────────────────────────────────────────→ note 4
clawhub/telemetry.md
├── intro (minimal CLI telemetry → aggregate install counts) ────────────→ note 6 (oc_clawhub_telemetry)
├── When telemetry is collected ────────────────────────────────────────→ note 6
├── What we collect (+ ### What we do not collect) ─────────────────────→ note 6
├── Install counts (installsAllTime/installsCurrent) ───────────────────→ note 6
├── Transparency + user controls ──────────────────────────────────────→ note 6
└── How to disable telemetry (CLAWHUB_DISABLE_TELEMETRY=1) ─────────────→ note 6
clawhub/troubleshooting.md
├── `clawhub login` browser never completes ────────────────────────────→ note 7 (oc_clawhub_troubleshooting_auth_install)
├── `whoami`/`publish` Unauthorized (401) ──────────────────────────────→ note 7
├── `Rate limit exceeded` (429) ────────────────────────────────────────→ note 7
├── Fails behind a proxy ───────────────────────────────────────────────→ note 7
├── A skill does not appear in search ──────────────────────────────────→ note 7
├── A plugin install fails in OpenClaw ─────────────────────────────────→ note 7
├── Public API requests fail (→ http-api, cw02) ────────────────────────→ note 7
├── Publish fails: required metadata missing ───────────────────────────→ note 8 (oc_clawhub_troubleshooting_publish_sync)
├── Publish fails: GitHub owner/source error ───────────────────────────→ note 8
├── Publish fails: namespace claimed/reserved (→ namespace-claims, cw02) → note 8
├── `sync` says no skills were found ───────────────────────────────────→ note 8
└── `update` refuses because of local changes ──────────────────────────→ note 8
```
No orphaned sections. ClawHub sibling pages (moderation, publishing, namespace-claims, http-api, acceptable-usage)
owned by cw01/cw02 are cross-linked, not duplicated; CLI command pages owned by cl01–cl09 referenced by name.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| security-audits.md (862w, 7 H2, mixed BB) | notes 2 + 3 | The user-facing **result schema** (status/risk/findings + checklist — a model/reference) and the **scan-stack concept** (ClawScan/VirusTotal/OWASP, how audits are produced) are distinct building blocks and distinct reader tasks (act on a result vs understand the pipeline); split keeps each one BB and ≤600w. |
| skill-format.md (962w, 9 H2 / 7 H3, mixed BB) | notes 4 + 5 | Exceeds an atomic single-BB scope: the **on-disk folder/format procedure** (files, import, slugs, versioning, license, limits) and the **`SKILL.md` frontmatter schema** (`metadata.openclaw` field reference — a model) are separate clusters; split per mixed-BB rule, each ≤640w with ≤4 code blocks. |
| troubleshooting.md (737w, 11 H2, 8 code) | notes 7 + 8 | Two task clusters with little overlap — **auth/install/API access** failures vs **publish/sync/update** failures; split keeps each note a focused procedure (~5–7 recipes, ≤4 code blocks each) and aids discoverability. |

Pages NOT split: security.md (262w, note 1), telemetry.md (224w, note 6) — each well under caps and single-BB.

## Summary Statistics & Building Block Distribution

- Source pages: **5** (3,047 measured words; 18 code blocks). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×4 (notes 4, 6, 7, 8) · model ×2 (notes 2, 5) · concept ×1 (note 3) · argument ×1 (note 1).
- Est. digest words ≈ **4,200** (avg ~525/note; max 640). Source code fences distribute across notes (security-audits
  4 → notes 2/3; skill-format 5 → notes 4/5; telemetry 1 → note 6; troubleshooting 8 → notes 7/8); each note kept ≤4
  code blocks (well under the ≤6 cap; config/CLI snippets reproduced selectively, verbatim).
- Cross-refs (per-note mapping **LOCKED at xref-augment 2026-06-21** — see "Per-Note Related Notes Mapping"):
  docs under `resources/documentation/`** (≥5 EXISTING per note + sibling `oc_*` planned), PLUS relevant
  `repo_openclaw*` (esp. `repo_openclaw_security`, `repo_openclaw_skills`, `repo_openclaw_cli_wizard`). Snippet pool
  draws from `snippet_openclaw_security_*` / `snippet_openclaw_skills_*` / `snippet_hermes_agent_*` /

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> WHERE note_id LIKE '%/<id>.md'`). Sibling `oc_*` in THIS series (and `oc_*` owned by cw01/cw02) do not exist yet →
> paths are from `resources/documentation/openclaw/oc_*.md`: term → `../../term_dictionary/`; snippet →
> `../../code_snippets/`; repo → `../../../areas/code_repos/`; cc_ doc → `../claude_code/`; pi_ doc → `../pi/`;
> sibling oc_ → `oc_*.md`.

### oc_clawhub_security (8t · 10s · 10d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — structured enumeration of attack surfaces/adversaries; relevance: defines the bug classes a good ClawHub advisory report covers (site/API/CLI, publishing/integrity, authn/authz, scanning/moderation).
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — risk from third-party components in a delivery pipeline; relevance: a registry's publishing/download/install/artifact-integrity surface IS its supply-chain attack surface, the primary reporting target.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity of a principal; relevance: authn/authz/API-token bugs are explicitly in-scope for ClawHub advisories.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential for delegated API access; relevance: API-token vulnerabilities are a named in-scope advisory class.
- [Red Teaming](../../term_dictionary/term_red_teaming.md) — adversarial testing to find exploitable weaknesses; relevance: the lens a reporter uses to decide what counts as a ClawHub-platform vulnerability worth disclosing.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — scope of damage from a single failure; relevance: the "real user impact" threshold that decides whether a hosted-service vuln is publicly disclosed.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial input that hijacks an agent's instructions; relevance: a representative attack class that, on confirmed exploitation reaching users, triggers public disclosure.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — review/removal of harmful published content; relevance: "scanning, moderation, or report handling" bugs are a named advisory category and link to the cw02 moderation page.

**Docs**
- [CC Security Architecture](../claude_code/cc_security_architecture.md) — Claude Code's layered security model; relevance: closest precedent for a coding-agent platform's trust boundaries and what "platform vs third-party code" means.
- [CC Web Security and Limits](../claude_code/cc_web_security_and_limits.md) — web-surface security + rate/usage limits; relevance: analog of the ClawHub website/API attack surface a reporter targets.
- [CC Security Guidance: Plugin](../claude_code/cc_security_guidance_plugin.md) — security guidance for third-party plugins; relevance: parallels the platform-vs-third-party-artifact distinction the disclosure policy draws.
- [CC SDK Secure Deployment Principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure-by-default deployment rules; relevance: framing for "users need to take protective action" disclosures.
- [CC Marketplace Restrictions](../claude_code/cc_marketplace_restrictions.md) — what a marketplace will/won't host; relevance: registry-integrity policy analog informing what platform bugs deserve advisories.
- [CC Login/Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — diagnosing auth failures; relevance: maps to the authn/authz/token bug class in advisory scope.
- [Pi Security Model](../pi/pi_security_model.md) — Pi coding agent's threat/trust model; relevance: cross-corpus precedent for a self-hosted agent's vulnerability-disclosure posture.
- [OpenClaw — Security Audits: Result Schema](oc_clawhub_security_audits_results.md) — install-time audit status/risk/findings (planned, this series); relevance: the "Related pages" link from security.md; reporting feeds the audit pipeline.
- [OpenClaw — Security Audits: Scan Stack](oc_clawhub_security_audits_scan_stack.md) — how audits are produced (planned, this series); relevance: scanning bugs are an in-scope advisory class.
- [OpenClaw — ClawHub Moderation](../openclaw/oc_clawhub_moderation.md) — moderation holds/bans/account standing (planned, cw02); relevance: the security.md "Related pages" cross-link for report handling.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — the code-side ClawHub/OpenClaw security subsystem; relevance: implements the scanning/moderation/report-handling surfaces this page tells you to report bugs against.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: home of the CLI/release artifacts whose vulns are always disclosed.

**Snippets**
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — how reported security issues are remediated; relevance: the downstream of an advisory report.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — assembles a release's audit result; relevance: the scanning subsystem a "scanning bug" advisory would target.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — scans skill artifacts for risk; relevance: a core scanning component whose failures are reportable platform bugs.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — supply-chain trust finding objects; relevance: the integrity-checking surface in advisory scope.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — resolves publisher/source trust; relevance: authn/authorization-adjacent integrity logic.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — handling untrusted external content; relevance: "malicious content reaching users" disclosure trigger.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny-list for dangerous tool calls; relevance: a platform guardrail whose bypass is a reportable vuln.
- [snippet_hermes_agent_cli_security_advisories](../../code_snippets/snippet_hermes_agent_cli_security_advisories.md) — CLI security-advisory data model + version checks; relevance: the closest analog of the GitHub Security Advisory channel this page describes.
- [snippet_hermes_agent_optional_skills_security_sherlock](../../code_snippets/snippet_hermes_agent_optional_skills_security_sherlock.md) — security-investigation skill; relevance: example of the third-party-skill code that is NOT reported via ClawHub advisories (report to the publisher instead).

### oc_clawhub_security_audits_results (8t · 11s · 10d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — attack-surface enumeration; relevance: the audit status/risk/findings schema is the user-facing projection of ClawHub's threat model per release.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — scope of potential damage; relevance: the page literally defines risk level as "blast radius: how much power the release appears to have."
- [Access Control](../../term_dictionary/term_access_control.md) — authority/permission granting; relevance: risk level measures the authority (account access, data changes) a release requests.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — third-party-component risk; relevance: the audit is the install-time supply-chain trust gate the checklist tells you to read.
- [Red Teaming](../../term_dictionary/term_red_teaming.md) — adversarial weakness discovery; relevance: findings are the red-team-style evidence rolled up into status/risk.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — instruction-hijack attack; relevance: a representative finding class that drives `Warn`/`Malicious` status.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secure credential storage; relevance: "required credentials/permissions/environment variables" is a checklist item and a finding source.

**Docs**
- [CC Security Guidance: Plugin](../claude_code/cc_security_guidance_plugin.md) — third-party-plugin security guidance; relevance: parallels the pre-install trust checklist (owner/source/permissions/credentials).
- [CC Security Architecture](../claude_code/cc_security_architecture.md) — layered trust model; relevance: framing for why a `Pass` "does not replace your own judgment."
- [CC Marketplace Restrictions](../claude_code/cc_marketplace_restrictions.md) — hosting restrictions; relevance: analog of audit-status gating before something is installable.
- [CC Managed Plugin Policy Settings](../claude_code/cc_managed_plugin_policy_settings.md) — org policy over plugin install; relevance: enterprise analog of the "install only what you understand and trust" decision.
- [CC Hooks: Guardrail and Audit Recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail/audit hook patterns; relevance: how a host enforces decisions an audit status recommends.
- [CC Security Guidance: Layers and Rules](../claude_code/cc_security_guidance_layers_and_rules.md) — layered security rules; relevance: maps to severity laddering (`Info`→`Critical`) in findings.
- [Pi Security Model](../pi/pi_security_model.md) — agent threat/trust model; relevance: cross-corpus view of "how much authority a release has."
- [CC SDK Secure Deployment Principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure-by-default principles; relevance: the judgment frame behind "always use judgment before granting sensitive access."
- [OpenClaw — Security Audits: Scan Stack](oc_clawhub_security_audits_scan_stack.md) — SkillSpector+VirusTotal+ClawScan pipeline (planned, this series); relevance: produces the status/risk/findings this note reads.
- [OpenClaw — ClawHub Security](oc_clawhub_security.md) — reporting + disclosure policy (planned, this series); relevance: the "See also" link; reported issues become findings.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — code-side security subsystem; relevance: implements the audit-status/risk/findings computation this schema describes.

**Snippets**
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — scans a skill release; relevance: emits the findings rolled into status/risk.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composes the overall audit result; relevance: the code that produces the audit-status + risk-level rollup.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — finding objects + severities; relevance: the `Info`→`Critical` finding records this note documents.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — resolves trust signals (owner/source/installs); relevance: the "other trust signals" checklist row.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — deep-mode behavior probe; relevance: how high-impact authority (a `High` risk signal) is detected.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit (interpreter allowlist); relevance: a source of "runs commands"/execution findings driving risk.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny constant; relevance: high-impact-authority detection feeding `Warn`/`Malicious`.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted-content handling; relevance: a finding category (content/context risk).
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — `scan_file` regex + `should_allow_install` gate; relevance: analog of the pre-install allow/deny decision the audit status drives.
- [snippet_hermes_agent_optional_skills_security_sherlock](../../code_snippets/snippet_hermes_agent_optional_skills_security_sherlock.md) — security-analysis skill; relevance: example of finding-generation logic over an artifact.

### oc_clawhub_security_audits_scan_stack (9t · 11s · 10d)

**Terms**
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — instruction-hijack attack; relevance: a named OWASP Agentic Skills Top 10 risk class ClawScan uses as a lens.
- [Threat Model](../../term_dictionary/term_threat_model.md) — attack-surface enumeration; relevance: the OWASP-Top-10 lens IS the threat model the scan stack applies.
- [Red Teaming](../../term_dictionary/term_red_teaming.md) — adversarial testing; relevance: ClawScan's agent-aware review evaluates artifacts adversarially.
- [Jailbreak](../../term_dictionary/term_jailbreak.md) — bypassing model/agent guardrails; relevance: adjacency to "excessive agency / tool misuse / unsafe execution" OWASP classes.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — third-party-component risk; relevance: VirusTotal vendor reputation + artifact scanning is supply-chain malware telemetry.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage; relevance: "credential exposure" is an OWASP risk ClawScan checks for.
- [Access Control](../../term_dictionary/term_access_control.md) — authority/permission; relevance: "excessive agency" is evaluated against declared/expected authority.
- [Guardrails](../../term_dictionary/term_guardrails.md) — automated safety controls on AI behavior; relevance: ClawScan is an automated guardrail layer over agent-facing artifacts.
- [Anomaly Detection](../../term_dictionary/term_anomaly_detection.md) — flagging deviations from expected behavior; relevance: the coherence question (declared vs actual behavior) is anomaly detection over a release.

**Docs**
- [CC Security Guidance: Layers and Rules](../claude_code/cc_security_guidance_layers_and_rules.md) — layered security rules; relevance: closest precedent for a multi-component (static + agent-aware + reputation) review stack.
- [CC Security Guidance: Plugin](../claude_code/cc_security_guidance_plugin.md) — plugin security guidance; relevance: parallels "what ClawHub checks" (declared permissions vs actual content).
- [CC Security Architecture](../claude_code/cc_security_architecture.md) — layered trust model; relevance: framing for the 3-part SkillSpector+VirusTotal+ClawScan composition.
- [CC SDK Secure Deployment Principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure-by-default deployment; relevance: the "powerful behavior is not automatically bad if disclosed/proportionate" principle.
- [CC Hooks: Guardrail and Audit Recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail/audit recipes; relevance: how scan signals become enforcement.
- [CC Marketplace Restrictions](../claude_code/cc_marketplace_restrictions.md) — hosting restrictions; relevance: the policy backdrop ClawScan enforces.
- [Pi Security Model](../pi/pi_security_model.md) — agent threat model; relevance: cross-corpus precedent for agent-aware artifact review.
- [CC OTel: Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md) — telemetry/analysis privacy; relevance: VirusTotal-as-telemetry analog and its limits.
- [OpenClaw — Security Audits: Result Schema](oc_clawhub_security_audits_results.md) — status/risk/findings (planned, this series); relevance: the consumer of the scan-stack output.
- [OpenClaw — Skill Frontmatter Schema](oc_clawhub_skill_frontmatter.md) — `metadata.openclaw` field reference (planned, this series); relevance: the declared metadata ClawScan's coherence check reads.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — code-side security subsystem; relevance: home of ClawScan/SkillSpector composition + VirusTotal integration.

**Snippets**
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill supply-chain scanner; relevance: SkillSpector-equivalent static + agent-aware review.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composes the 3-part audit; relevance: literally assembles SkillSpector + VirusTotal + risk analysis.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — deep-mode network/behavior probe; relevance: a static/behavioral scan signal feeding risk analysis.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: "unsafe execution" OWASP-class detection.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — untrusted external-content handling; relevance: "memory/context poisoning" + prompt-injection detection input.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny constant; relevance: "tool misuse / excessive agency" lens.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — trust findings; relevance: ClawScan finding objects.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel-source audit (explicit vs default accounts); relevance: capability-signal scanning example.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM allowlist/read-only audit; relevance: per-permission capability-signal check.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — `scan_file` regex guard; relevance: static-scan-signal analog in a sibling ecosystem.
- [snippet_hermes_agent_skills_red_teaming](../../code_snippets/snippet_hermes_agent_skills_red_teaming.md) — red-team attack modes; relevance: the adversarial lens (prompt injection / bypass) ClawScan applies.

### oc_clawhub_skill_format (10t · 10s · 11d)

**Terms**
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capability/instruction folders; relevance: the artifact this page formats (a skill is a folder with `SKILL.md`).
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — the declarative file describing a skill; relevance: `SKILL.md` IS the required manifest of the skill folder.
- [NPM](../../term_dictionary/term_npm.md) — JavaScript package registry/naming conventions; relevance: package slugs must be lowercase and npm-safe (`@scope/name`).
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — third-party-component delivery risk; relevance: allowed-files allowlist + 50MB limit + integrity rules are supply-chain controls on the bundle.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — scope/namespace hijack attack; relevance: scoped names must match the publisher handle exactly (defends against namespace confusion).
- [Homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: `install: kind: brew` is a supported install-spec kind referenced from the skill folder's frontmatter.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin declaration file; relevance: parallels `SKILL.md`; the importer also discovers manifests, and plugins use `package.json` compat fields.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — toolkit for building plugins; relevance: the skill/plugin authoring surface the on-disk format serves.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway/registry; relevance: ClawHub is OpenClaw's registry; the format is the OpenClaw skill packaging convention.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: a skill's declared `requires.bins`/runtime is what the agent function-calls into.

**Docs**
- [CC Create a Skill](../claude_code/cc_create_a_skill.md) — authoring a Claude Code skill folder; relevance: direct analog of the on-disk skill folder + `SKILL.md` format.
- [CC Skills Overview](../claude_code/cc_skills_overview.md) — what skills are and how they load; relevance: conceptual backdrop for the folder/required-file rules.
- [CC Bundled Skills](../claude_code/cc_bundled_skills.md) — skills shipped in a bundle; relevance: parallels allowed-files + bundle-size limits.
- [CC Plugin Directory Structure](../claude_code/cc_plugin_directory_structure.md) — on-disk plugin layout; relevance: closest precedent for "a skill is a folder" with required/optional files.
- [CC SDK Plugin Structure](../claude_code/cc_sdk_plugin_structure.md) — SDK plugin file structure; relevance: required-vs-optional-file mapping analog.
- [CC Plugin Sources](../claude_code/cc_plugin_sources.md) — installing from Git/local/marketplace sources; relevance: maps to the GitHub-import rules (public, non-fork, owned repos).
- [CC Marketplace JSON Schema](../claude_code/cc_marketplace_json_schema.md) — marketplace metadata schema; relevance: slug/version/license metadata-format analog.
- [CC Plugin Components](../claude_code/cc_plugin_components.md) — components inside a plugin; relevance: parallels the allowed-files allowlist composition.
- [Pi Skills](../pi/pi_skills.md) — Pi's skill packaging; relevance: cross-corpus precedent for skill-folder format.
- [OpenClaw — Skill Frontmatter Schema](oc_clawhub_skill_frontmatter.md) — `metadata.openclaw` field reference (planned, this series); relevance: the frontmatter half split out of this same source page.
- [OpenClaw — ClawHub Publishing](../openclaw/oc_clawhub_publishing.md) — the publish flow (planned, cw02); relevance: the format is consumed by publish/sync.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — code-side skill subsystem; relevance: parses `SKILL.md`/folder format + enforces allowed-files/limits.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill-manifest format + parsing; relevance: the code that reads the `SKILL.md` folder format this page defines.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill planning/loading; relevance: consumes the on-disk skill folder.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool-descriptor contract for skills; relevance: how a skill folder advertises its tools.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — evaluates `requires.env`/`bins`; relevance: enforces the folder's declared runtime requirements.
- [snippet_hermes_agent_skills_canonical_format](../../code_snippets/snippet_hermes_agent_skills_canonical_format.md) — canonical skill format (YAML frontmatter + H2 sections); relevance: direct sibling-ecosystem precedent for the `SKILL.md` folder format.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — skill-vs-plugin distinction; relevance: clarifies why skills use `SKILL.md` while plugins use `package.json` compat metadata.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest + uvx distribution; relevance: analog of registry-side slug/version/source metadata derived from the folder.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — multi-source/two-layout discovery; relevance: analog of how the GitHub importer/local sync discovers `SKILL.md` folders.

### oc_clawhub_skill_frontmatter (10t · 10s · 11d)

**Terms**
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — declarative skill description file; relevance: the frontmatter IS the manifest's metadata block.
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: the frontmatter declares what a skill needs to run.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin declaration; relevance: `metadata.openclaw` runtime block parallels plugin-manifest runtime declarations.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential storage; relevance: `primaryEnv`/`requires.env`/`envVars` declare the credential env vars a skill needs.
- [Homebrew](../../term_dictionary/term_homebrew.md) — macOS package manager; relevance: `install: kind: brew` is a documented install-spec kind.
- [NPM](../../term_dictionary/term_npm.md) — JS package manager; relevance: `install: kind: node` install spec + version/semver fields.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency-delivery risk; relevance: declared `install` deps + `requires.bins` are the supply-chain surface the schema captures.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin exposing a provider/runtime; relevance: skill runtime requirements (`requires.config`/`os`) parallel provider-plugin declarations.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — scope/name hijack; relevance: accurate dependency declarations reduce confusion-attack surface.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model→tool invocation; relevance: `requires.bins`/`anyBins` declare the binaries a skill function-calls.

**Docs**
- [CC Skill Frontmatter Reference](../claude_code/cc_skill_frontmatter_reference.md) — Claude Code `SKILL.md` frontmatter field reference; relevance: the direct field-by-field analog of `metadata.openclaw`.
- [CC Plugin Manifest Schema](../claude_code/cc_plugin_manifest_schema.md) — plugin manifest field schema; relevance: closest schema-reference precedent for a runtime-metadata block.
- [CC Plugin User Config and Env](../claude_code/cc_plugin_user_config_and_env.md) — user config + env vars for plugins; relevance: parallels `envVars`/`requires.env`/`primaryEnv` declarations.
- [CC Environment Variables](../claude_code/cc_environment_variables.md) — env-var configuration reference; relevance: the env-var declaration surface `requires.env`/`envVars` describe.
- [CC SDK Skills](../claude_code/cc_sdk_skills.md) — programmatic skill definition; relevance: SDK-side analog of declared skill metadata.
- [CC Plugin Dependencies](../claude_code/cc_plugin_dependencies.md) — declaring plugin dependencies; relevance: the `install` array (brew/node/go/uv) dependency-spec analog.
- [CC Skill Invocation and Lifecycle](../claude_code/cc_skill_invocation_and_lifecycle.md) — how a skill activates; relevance: the `always`/`skillKey` invocation fields in the reference.
- [Pi Skills](../pi/pi_skills.md) — Pi skill packaging; relevance: cross-corpus precedent for declared skill runtime metadata.
- [Pi Provider Auth](../pi/pi_provider_auth.md) — provider credential/env handling; relevance: parallels `primaryEnv`/credential env-var declaration.
- [OpenClaw — Skill Format](oc_clawhub_skill_format.md) — on-disk folder/format procedure (planned, this series); relevance: the folder half split out of the same source page; frontmatter lives in its `SKILL.md`.
- [OpenClaw — Security Audits: Scan Stack](oc_clawhub_security_audits_scan_stack.md) — scan pipeline (planned, this series); relevance: ClawScan's coherence check consumes this declared metadata.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — code-side skill subsystem; relevance: parses + validates `metadata.openclaw` frontmatter on publish.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — manifest format + frontmatter parsing; relevance: the code that reads the `metadata.openclaw` schema this note documents.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — evaluates `requires.env`/`bins`/`anyBins`; relevance: the runtime consumer of the declared frontmatter fields.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool-descriptor contract; relevance: how declared metadata maps to invocable tools.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill planning/loading; relevance: consumes the parsed frontmatter to plan availability.
- [snippet_hermes_agent_core_skill_utils_frontmatter](../../code_snippets/snippet_hermes_agent_core_skill_utils_frontmatter.md) — YAML frontmatter parser (CSafeLoader, memoized); relevance: direct analog of frontmatter extraction during publish.
- [snippet_hermes_agent_skills_canonical_format](../../code_snippets/snippet_hermes_agent_skills_canonical_format.md) — canonical frontmatter + section format; relevance: sibling-ecosystem precedent for required frontmatter fields.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema (identity triple, deps); relevance: the field-reference analog including dependency declarations.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — skills validate (3-source env-var aggregation); relevance: validates declared env vars vs usage, the coherence check this page motivates.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — install guard (`should_allow_install`); relevance: enforces declaration↔behavior coherence at install.

### oc_clawhub_telemetry (8t · 10s · 10d)

**Terms**
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: the page explicitly lists what is NOT collected (paths, file contents, prompts) — a data-minimization stance over PII.
- [Data Minimization](../../term_dictionary/term_data_minimization.md) — collect only what is needed; relevance: "minimal CLI telemetry" sending only `{slug, version}` is textbook data minimization.
- [Data Retention](../../term_dictionary/term_data_retention.md) — how long data is kept; relevance: account deletion also deletes telemetry data.
- [Data Governance](../../term_dictionary/term_data_governance.md) — policy/controls over data handling; relevance: transparency + user-controls + opt-out are governance mechanisms.
- [GDPR](../../term_dictionary/term_gdpr.md) — EU data-protection regulation; relevance: minimization + deletion-on-account-delete + opt-out align with GDPR principles.
- [Access Control](../../term_dictionary/term_access_control.md) — gating by identity; relevance: telemetry is only sent when logged in (identity-gated collection).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — delegated-access credential; relevance: login state (the token) is the precondition for any telemetry event.
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — operational logging/counting; relevance: aggregate `installsAllTime`/`installsCurrent` counters are the operational metrics computed.

**Docs**
- [CC Data Usage and Telemetry](../claude_code/cc_data_usage_and_telemetry.md) — what Claude Code collects + opt-out; relevance: the direct analog of ClawHub install telemetry + disable controls.
- [CC Zero Data Retention](../claude_code/cc_zero_data_retention.md) — zero-retention mode; relevance: parallels "deleting your account deletes your telemetry."
- [CC Monitoring: OpenTelemetry Setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — telemetry pipeline setup; relevance: how aggregate counters/telemetry are collected and configured.
- [CC OTel: Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md) — telemetry analysis + privacy posture; relevance: the "what we do not collect" privacy stance analog.
- [CC OTel: Audit and SIEM](../claude_code/cc_otel_audit_and_siem.md) — audit/event export; relevance: aggregate-counter / audit-operations analog.
- [CC OTel: Configuration Variables](../claude_code/cc_otel_configuration_variables.md) — env vars controlling telemetry; relevance: direct analog of `CLAWHUB_DISABLE_TELEMETRY=1` opt-out.
- [CC Environment Variables](../claude_code/cc_environment_variables.md) — env-var reference; relevance: the mechanism (env var) used to disable telemetry.
- [Pi Settings Reference](../pi/pi_settings_reference.md) — settings/config reference; relevance: cross-corpus precedent for a config/env-controlled behavior toggle.
- [OpenClaw — ClawHub Security](oc_clawhub_security.md) — reporting + disclosure (planned, this series); relevance: data-handling adjacency (what is collected vs disclosed).
- [OpenClaw — Troubleshooting: Auth/Install](oc_clawhub_troubleshooting_auth_install.md) — login/install diagnostics (planned, this series); relevance: telemetry requires logged-in state, the same auth surface.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the ClawHub/OpenClaw CLI; relevance: the CLI that emits the install telemetry event on `clawhub install`.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: home of the aggregate-counter backend the CLI reports into.

**Snippets**
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — CLI install flow (quarantine→scan→install); relevance: the install command an install-telemetry event would attach to.
- [snippet_hermes_agent_tools_skills_hub_install](../../code_snippets/snippet_hermes_agent_tools_skills_hub_install.md) — hub install (`install_from`, quarantine_bundle); relevance: the install pathway whose count telemetry aggregates.
- [snippet_hermes_agent_cli_skills_hub](../../code_snippets/snippet_hermes_agent_cli_skills_hub.md) — skills-hub browse (multi-source fetch); relevance: the registry-client surface where login state is established.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — CLI login/logout; relevance: login state is the precondition for telemetry being sent.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — credential storage (file lock, atomic write); relevance: where the logged-in token lives that gates telemetry.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — hub registry client; relevance: the registry endpoint the install event posts to.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill planning/loading; relevance: the install-side consumer that an install event corresponds to.
- [snippet_hermes_agent_skills_index_cache](../../code_snippets/snippet_hermes_agent_skills_index_cache.md) — multi-source skills index cache; relevance: aggregate-count/cache analog of `installsCurrent`/`installsAllTime`.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest + distribution; relevance: the registry record (`slug`/`version`) a telemetry event references.

### oc_clawhub_troubleshooting_auth_install (10t · 12s · 10d)

**Terms**
- [OAuth](../../term_dictionary/term_oauth.md) — delegated browser authorization; relevance: `clawhub login` opens a browser OAuth flow with a local callback.
- [PKCE](../../term_dictionary/term_pkce.md) — proof-key-for-code-exchange for public clients; relevance: the secure browser-auth callback pattern behind the `127.0.0.1` callback.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: headless login uses `--token clh_...`; 401s mean a missing/revoked token.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the `Unauthorized` (401) recipe is core authentication troubleshooting.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling request volume; relevance: the `429 Rate limit exceeded` recipe (`Retry-After`, `RateLimit-*` headers).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — intermediary that forwards requests; relevance: the "fails behind a proxy" recipe (`HTTPS_PROXY`/`HTTP_PROXY`).
- [Access Control](../../term_dictionary/term_access_control.md) — visibility/permission gating; relevance: "a skill does not appear in search" because it is held by scan/moderation (access-gated listing).
- [VPN](../../term_dictionary/term_vpn.md) — tunneled network access; relevance: VPN/firewall rules are called out as blockers for the local callback.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe-to-retry semantics; relevance: retry-after handling + caching public responses (safe retries) underpins the recipes.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin declaration; relevance: `openclaw plugins install clawhub:<pkg>` compatibility checks read the manifest's compat range.

**Docs**
- [CC Login/Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — diagnosing sign-in failures; relevance: direct analog of the stuck-browser-login + 401 recipes.
- [CC Authentication and Network Errors](../claude_code/cc_authentication_and_network_errors.md) — auth + network error reference; relevance: 401/429/proxy error analog.
- [CC Server and Usage Limit Errors](../claude_code/cc_server_and_usage_limit_errors.md) — rate/usage limit errors; relevance: the `429` + retry-header recipe analog.
- [CC Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — configuring HTTP(S) proxies; relevance: the `HTTPS_PROXY`/`HTTP_PROXY` "behind a proxy" recipe.
- [CC Web Security and Limits](../claude_code/cc_web_security_and_limits.md) — web-surface limits; relevance: shared-egress-IP anonymous rate limits.
- [CC Install Diagnostics](../claude_code/cc_install_diagnostics.md) — diagnosing install issues; relevance: the plugin-install-fails-in-OpenClaw recipe analog.
- [CC Install Failures Reference](../claude_code/cc_install_failures_reference.md) — install failure catalog; relevance: install-failure recipe precedent.
- [Pi Provider Auth](../pi/pi_provider_auth.md) — provider auth/token handling; relevance: cross-corpus analog of login/token troubleshooting.
- [OpenClaw — Troubleshooting: Publish/Sync](oc_clawhub_troubleshooting_publish_sync.md) — publish/sync/update recipes (planned, this series); relevance: the sibling half of the troubleshooting page.
- [OpenClaw — ClawHub Telemetry](oc_clawhub_telemetry.md) — install telemetry (planned, this series); relevance: telemetry depends on the logged-in state these recipes restore.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the ClawHub CLI; relevance: implements `login`/`install`/`inspect` whose failures these recipes diagnose.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: scan/upload-gate state explains "held by scan" search-visibility failures.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway; relevance: `openclaw plugins install` compatibility runs through the gateway/runtime.

**Snippets**
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — login/logout (OAuth device-code); relevance: the stuck-browser-login recipe's underlying flow.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — local OAuth callback HTTP server; relevance: the `http://127.0.0.1:<port>/callback` that "never completes."
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE (RFC 7636, S256); relevance: the secure callback-auth pattern behind browser login.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — credential storage; relevance: where the token lives that a 401 says is missing/revoked (`CLAWHUB_CONFIG_PATH` analog).
- [snippet_hermes_agent_core_rate_limit_tracker](../../code_snippets/snippet_hermes_agent_core_rate_limit_tracker.md) — rate-limit tracker (header parsing); relevance: parses `RateLimit-*`/`Retry-After` like the 429 recipe.
- [snippet_hermes_agent_core_conversation_loop_rate_limit_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_rate_limit_recovery.md) — rate-limit recovery/backoff; relevance: the retry-after-the-reported-delay behavior the recipe recommends.
- [snippet_hermes_agent_gw_platform_signal_rate_limit](../../code_snippets/snippet_hermes_agent_gw_platform_signal_rate_limit.md) — `_extract_retry_after` rate-limit handling; relevance: the `Retry-After` parsing the 429 recipe describes.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — proxy-URL resolution; relevance: the `HTTPS_PROXY`/`HTTP_PROXY` handling for the "behind a proxy" recipe.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — install flow with scan gating; relevance: the install-fails / held-by-scan recipe analog.
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — install guard (`should_allow_install`); relevance: why a held/blocked package is not installable until resolved.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit composition; relevance: scan state that makes a release public-or-held in search.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install command (env discovery, git-clone); relevance: the `openclaw plugins install clawhub:<pkg>` analog.

### oc_clawhub_troubleshooting_publish_sync (10t · 11s · 10d)

**Terms**
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — `SKILL.md` declaration; relevance: "publish fails because required metadata is missing" → check `SKILL.md` frontmatter.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin declaration; relevance: code-plugin publishes need `package.json` `openclaw.compat.pluginApi`/`build.openclawVersion`.
- [NPM](../../term_dictionary/term_npm.md) — package naming/scopes; relevance: scoped names (`@example-org/example-plugin`) and slug rules drive namespace publish errors.
- [Dependency Confusion](../../term_dictionary/term_dependency_confusion.md) — scope/namespace hijack; relevance: claimed/reserved-namespace failures + scoped-name owner matching defend against confusion.
- [Brand Registry](../../term_dictionary/term_brand_registry.md) — authoritative ownership registry; relevance: the org/namespace claim flow (proving rightful namespace ownership) is a brand-registry analog.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — artifact-integrity in delivery; relevance: publish/sync integrity (owner/source attribution, dry-run preview) is supply-chain hygiene.
- [Skills](../../term_dictionary/term_skills.md) — packaged capabilities; relevance: `sync` discovers folders containing `SKILL.md`/`skill.md` to publish.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: publish requires being signed in with the GitHub account that owns/can publish the package.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the registry/gateway product; relevance: `clawhub`/`openclaw` publish/sync/update commands are OpenClaw registry operations.
- [Idempotency](../../term_dictionary/term_idempotency.md) — safe re-run semantics; relevance: `--dry-run` previews + `update --force` overwrite are the retry/idempotency controls.

**Docs**
- [CC Host and Manage Marketplaces](../claude_code/cc_host_and_manage_marketplaces.md) — running a marketplace/registry; relevance: publish/owner/source-attribution analog of the ClawHub publish flow.
- [CC Marketplace JSON Schema](../claude_code/cc_marketplace_json_schema.md) — marketplace metadata schema; relevance: required-metadata-missing publish failures map to schema fields.
- [CC Plugin Manifest Schema](../claude_code/cc_plugin_manifest_schema.md) — plugin manifest fields; relevance: `package.json` `openclaw.compat.*` required-field check.
- [CC Plugin Sources](../claude_code/cc_plugin_sources.md) — Git/owner/source attribution; relevance: the `owner/repo@ref` GitHub-source error recipe.
- [CC Plugin Marketplaces and Install](../claude_code/cc_plugin_marketplaces_and_install.md) — installing from marketplaces; relevance: namespace/scope ownership analog for publishing.
- [CC Plugin Caching and Troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin publish/cache troubleshooting; relevance: the closest precedent for publish/update-failure diagnostics.
- [CC Managed Plugin Policy Settings](../claude_code/cc_managed_plugin_policy_settings.md) — org policy over plugins; relevance: reserved/claimed-namespace + org-ownership analog.
- [Pi Packages](../pi/pi_packages.md) — packaging/publishing in Pi; relevance: cross-corpus precedent for publish/version/source mechanics.
- [OpenClaw — Troubleshooting: Auth/Install](oc_clawhub_troubleshooting_auth_install.md) — sign-in/install recipes (planned, this series); relevance: the sibling half of the same troubleshooting page.
- [OpenClaw — Skill Frontmatter Schema](oc_clawhub_skill_frontmatter.md) — `metadata.openclaw` reference (planned, this series); relevance: the fix for "required metadata missing" publish failures.

**Repos**
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill subsystem; relevance: validates `SKILL.md` metadata + slug rules that publish enforces.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — the CLI; relevance: implements `publish`/`sync`/`update` whose failures these recipes diagnose.

**Snippets**
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — manifest format/parsing; relevance: the metadata-required publish check reads this.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill planning/loading; relevance: discovers `SKILL.md` folders like `sync --root`.
- [snippet_hermes_agent_acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest + distribution; relevance: owner/source attribution + version metadata for publish.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema (identity triple, deps); relevance: the `package.json` compat-field check for code-plugin publishes.
- [snippet_hermes_agent_tools_skills_validate](../../code_snippets/snippet_hermes_agent_tools_skills_validate.md) — skills validate (env-var aggregation, trust); relevance: the `--dry-run` preview / required-metadata validation analog.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — install flow incl. name resolution; relevance: scoped-name/owner resolution analog for publish-namespace errors.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — hub registry client (path normalize, guard); relevance: namespace/slug resolution + reserved-name handling.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — multi-source/two-layout discovery; relevance: the `sync` folder-discovery (`SKILL.md`/`skill.md` roots) analog.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — plugin install (git-clone, env discovery); relevance: GitHub `owner/repo@ref` source handling analog.


## Undigested Terms Plan

> Per master: OpenClaw/ClawHub vocabulary is digested as `oc_*` doc notes by their home page, NOT promoted to new
> `term_dictionary` entries. The only `term_dictionary` interaction is **linking existing** terms. Expected **0 new
> term_dictionary captures** for cw03.

| Term (appears in source) | Disposition |
|---|---|
| ClawHub | OpenClaw registry product noun → described in `oc_clawhub_*` notes; link `term_openclaw`. Not a new term. |
| ClawScan / SkillSpector | ClawHub-internal audit-system proper nouns → documented in `oc_clawhub_security_audits_scan_stack` (note 3). Not vault-reusable; no term note. |
| audit status / risk level / findings | Audit result-schema vocabulary → documented in `oc_clawhub_security_audits_results` (note 2). Not a new term. |
| `SKILL.md` / skill frontmatter / `metadata.openclaw` | Skill-format schema → documented in notes 4/5; link existing `term_skill_manifest`, `term_skills`, `term_plugin_manifest`. |
| install spec (brew/node/go/uv) | Skill-format field → documented in note 5; link `term_homebrew`, `term_npm`. |
| install telemetry / `CLAWHUB_DISABLE_TELEMETRY` | Telemetry behavior → documented in note 6; link `term_pii`. |
| VirusTotal | Third-party scanning service proper noun → named in note 3; external link in References. No term note. |
| OWASP Agentic Skills Top 10 | External framework → named + linked in note 3 References; link `term_prompt_injection`, `term_threat_model`. No new term. |
| prompt injection / excessive agency / credential exposure / tool misuse | OWASP risk classes → link existing `term_prompt_injection` (others described inline as the OWASP lens; `term_excessive_agency`/`term_credential_exposure` do NOT exist — described in prose, NOT inlined as definitions, NOT promoted). |
| rate limit / `RateLimit-*` headers | Troubleshooting behavior → documented in note 7; link `term_rate_limiting`. |
| namespace claim / reserved namespace | Publish vocabulary → documented in note 8; link `term_brand_registry`, `term_dependency_confusion`. |

**New-term candidates:** **none.** No genuinely cross-cutting, vault-reusable term lacking an existing note appeared
(`term_excessive_agency`, `term_credential_exposure`, `term_software_supply_chain_security`, `term_typosquatting`,
`term_software_bill_of_materials` are absent but are NOT introduced — the source mentions them only as ClawScan/OWASP
context, fully covered by the `oc_*` doc note + existing `term_prompt_injection`/`term_supply_chain`/`term_threat_model`
links; promoting them would duplicate doc-page content per the master's design decision). If augment's Step 2d re-scan
surfaces a true reusable cross-cutting term, capture via `/tessellum-capture-term-note` and add to the best-fit glossary
(`acronym_glossary_cyber_security.md` for a security term, else the agentic/LLM glossary).

## Term-Note Authoring Requirements

**N/A (0 new terms).** cw03 authors zero `term_dictionary` notes; it only links existing terms. (Inherited from master:

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format: YAML field order + forbidden fields; H1/`## Overview`/`## Related Notes`/`## References` + bold footer; indexed-link format `[text](path.md)` | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traces to the source page (no invention) | diff each note vs `inbox/openclaw_docs/clawhub/<page>.md` |
| G3 | Density + Coverage: ≤400 lines, ≤2,500 words, ≤6 code blocks, one `building_block`; every mapped H2/H3 covered | `wc`, fence count, Section Coverage Map |
| G4 | Cross-Reference: ≥8 term links + ≥10 snippet links + ≥10 doc links per note (+ repo/sibling), each with a relevance statement | augment-locked mapping (xref-augment 2026-06-21) |
| G5 | Ghost-reference detect + redirect: every cited target resolves in the DB | `sqlite3` existence check (candidates pre-verified above) |
| G6 | Broken-link fix: 0 broken links after reindex | `/tessellum-fix-broken-links` |
| G7 | Discoverability (outbound + intra-series): sibling/entry-point links present | manual + DB |
| G8 | In-degree ≥1: each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks) | `note_links` query (in_degree ≥1) |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_clawhub_security oc_clawhub_security_audits_results oc_clawhub_security_audits_scan_stack oc_clawhub_skill_format oc_clawhub_skill_frontmatter oc_clawhub_telemetry oc_clawhub_troubleshooting_auth_install oc_clawhub_troubleshooting_publish_sync"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # at least one sibling oc_ link
  grep -q "($SIBLING_PREFIX" "$f" || echo "$n MISSING sibling $SIBLING_PREFIX link"
  # G3 density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb cb / $lines L)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

After authoring: `bash scripts/update_notes_database.sh` (incremental reindex) then G5/G6/G8 verify via `note_links` +
`/tessellum-fix-broken-links` (0 broken; every new note in_degree ≥1).

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6 cb / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_clawhub_security | argument | 380 | 0 | ✅ |
| 2 | oc_clawhub_security_audits_results | model | 600 | 2 | ✅ |
| 3 | oc_clawhub_security_audits_scan_stack | concept | 560 | 2 | ✅ |
| 4 | oc_clawhub_skill_format | procedure | 620 | 1 | ✅ |
| 5 | oc_clawhub_skill_frontmatter | model | 640 | 4 | ✅ |
| 6 | oc_clawhub_telemetry | procedure | 360 | 1 | ✅ |
| 7 | oc_clawhub_troubleshooting_auth_install | procedure | 560 | 4 | ✅ |
| 8 | oc_clawhub_troubleshooting_publish_sync | procedure | 480 | 4 | ✅ |

No note approaches caps. The two code-densest source pages (skill-format 5 fences, troubleshooting 8 fences) were split
so each note stays ≤4 code blocks; security-audits' 4 fences split 2/2 across notes 2/3. Tables (audit-status,
risk-level, frontmatter field reference) are reproduced as markdown tables, not code fences.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step) under a **"ClawHub"** section
(alongside cw01/cw02 rows). Each new note receives its entry-point back-link at finalization (satisfies G7/G8). No
separate entry point is created for cw03 — the master's `entry_openclaw_docs.md` is the single navigation hub for the
105-sub-plan series.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution; each new note must end with in_degree ≥1):

- `entry_openclaw_docs.md` → all 8 notes (primary discoverability path; created by master W1).
- `repo_openclaw_security` → notes 1, 2, 3 (code-side security subsystem ↔ ClawHub security/audit docs).
- `repo_openclaw_skills` → notes 4, 5, 8 (skill subsystem ↔ skill-format / frontmatter / publish-troubleshooting docs).
- `repo_openclaw_cli_wizard` → notes 6, 7, 8 (CLI ↔ telemetry / login-install / sync-publish troubleshooting docs).
- `term_threat_model` → notes 1, 2, 3; `term_skills` / `term_skill_manifest` → notes 4, 5, 8; `term_supply_chain` →
  notes 1–5, 8; `term_rate_limiting` → note 7; `term_pii` → note 6 (reciprocal term backlinks where relevant).
- Sibling intra-series: notes 2↔3 (audit results↔scan stack), 4↔5 (format↔frontmatter), 7↔8 (troubleshooting pair).

## Pacing Rules (inherited from master)

- One execution phase (8 notes); cap dynamic-workflow fan-out ≤30 agents/run (well within for 8 notes). Re-read each
  source page during authoring/execution; reproduce config/CLI snippets verbatim. One `building_block` per note.
- `git pull --rebase --autostash origin main` before committing; commit per wave; **no Claude co-author trailer**;
  `git push origin main` immediately after the commit. Reindex incrementally; verify `note_links` + 0 broken links +
  every new note in_degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** (this file) |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment; per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — READY (9/9 checkpoints PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending (status: ready) |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment pass — re-read all 5 source pages (`security` 262w, `security-audits` 862w, `skill-format`
962w, `telemetry` 224w, `troubleshooting` 737w = 3,047w measured; matches the plan's Source table) and replaced the
PLAN-stage Candidate Cross-References with a **LOCKED Per-Note Related Notes Mapping** at the RAISED floors:
sibling `oc_*` counted as planned), plus relevant `repo_openclaw*` and intra-series `oc_*` links. Every link carries a
were excluded (this is a security/registry/operations corpus, so the security-term selections are genuinely on-topic,

referenced as "term_telemetry-equivalent" in Scope, never cited — no ghost). All 9 openclaw security snippets,
notes verified present.

**Per-note locked counts (terms / snippets / docs):**

| Note | Terms | Snippets | Docs (existing+planned) | Floors met (≥8t · ≥10s · ≥10d · ≥5 existing docs) |
|---|---:|---:|---|---|
| oc_clawhub_security | 8 | 10 | 10 (7 existing + 3 planned oc_) | ✅ |
| oc_clawhub_security_audits_results | 8 | 11 | 10 (8 existing + 2 planned oc_) | ✅ |
| oc_clawhub_security_audits_scan_stack | 9 | 11 | 10 (8 existing + 2 planned oc_) | ✅ |
| oc_clawhub_skill_format | 10 | 10 | 11 (9 existing + 2 planned oc_) | ✅ |
| oc_clawhub_skill_frontmatter | 10 | 10 | 11 (9 existing + 2 planned oc_) | ✅ |
| oc_clawhub_telemetry | 8 | 10 | 10 (8 existing + 2 planned oc_) | ✅ |
| oc_clawhub_troubleshooting_auth_install | 10 | 12 | 10 (8 existing + 2 planned oc_) | ✅ |
| oc_clawhub_troubleshooting_publish_sync | 10 | 11 | 10 (8 existing + 2 planned oc_) | ✅ |

Repos are additional (1–3 per note): `repo_openclaw_security`, `repo_openclaw_skills`, `repo_openclaw_cli_wizard`,

**New-term candidates:** **none.** Re-reading all 5 pages (Step 2d re-scan) surfaced the OWASP risk vocabulary
(`excessive agency`, `tool misuse`, `credential exposure`, `unsafe execution`, `memory/context poisoning`),
ClawHub-internal proper nouns (`ClawScan`, `SkillSpector`, `VirusTotal`), and audit-schema vocabulary (`audit
status`, `risk level`, `findings`). Per the master's design decision these are digested as `oc_*` doc content, NOT
promoted to `term_dictionary`; the cross-cutting ones already have existing terms to LINK (`term_prompt_injection`,
`term_supply_chain`, `term_threat_model`, `term_red_teaming`, `term_jailbreak`, `term_access_control`,
`term_secrets_manager`). **Best-fit glossary IF a future re-scan promotes one:** `acronym_glossary_cyber_security.md`
for a security term (e.g. a hypothetical `term_excessive_agency`/`term_software_supply_chain_security`), else the
agentic/LLM glossary. cw03 authors **0 new `term_dictionary` notes** (Undigested Terms Plan + Term-Note Authoring
Requirements remain N/A, as planned).

**Issues / amendments:** none blocking. Two clarifications recorded: (a) the floors were raised above the master's
and cc_/pi_ doc corpora support this with no padding; (b) sibling `oc_*` links (this series + cw01/cw02-owned) are the
only non-existent targets and are explicitly marked **(planned)** — execution must NOT treat them as ghosts (they
resolve when their sub-plans run; G5 excludes intra-series planned siblings per the master).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review of the augmented plan (status was `pending` at review start).

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step exists (≥8 terms + floors) | **PASS** | "Per-Note Related Notes Mapping (LOCKED)" present; all 8 notes ≥8 terms (8/8/9/10/10/8/10/10), ≥10 snippets (10/11/11/10/10/10/12/11), ≥10 docs each, every link has a `relevance:` statement; bare-link check passes. |
| CP2 | 9-GATE table per batch (G1–G6, G8, G9) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (updated to ≥8t/≥10s/≥10d), G5 ghost-detect, G6 broken-link-fix, G7+G8 discoverability (in-degree ≥1). Single execution phase; one gate table covers it. |
| CP3 | Entry point update specified (inherited) | **PASS** | "Entry Point Decision (inherited from master)" — 8 rows into `entry_openclaw_docs.md` (created at master W1, >30-note series ⇒ CREATE required) under a ClawHub section; each new note gets its entry-point back-link at finalization. Parent hub identified; size-threshold satisfied at the master level (665 pages / >1,000 notes). |
| CP4 | Plan size manageable (≤30 or split) | **PASS** | 8 planned notes — well under 30; single execution phase. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Format inherited verbatim from master's Format Definition, itself derived from the existing `claude_code/`(`cc_*`) + `pi/`(`pi_*`) corpora (`## Overview` opener, `## Related Notes` reference section, footer `**Source**/**Last Updated**/**Status**`, fixed YAML field order, forbidden-field list). Not invented. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 8 notes ≤640w / ≤4 code blocks / well under 400 lines. The 3 mixed-BB / code-dense source pages (security-audits, skill-format, troubleshooting) were already split 2-ways each (notes 2/3, 4/5, 7/8); no further borderline notes. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 5 source mirrors under `inbox/openclaw_docs/clawhub/`: byte sizes 1,947 / 6,269 / 8,672 / 1,444 / 4,981 are consistent with the plan's 262/862/962/224/737 word measures (ratios within tolerance). No under-estimation; no re-split needed. |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | "Undigested Terms Plan" present with per-row dispositions + "New-term candidates: none"; "Term-Note Authoring Requirements" present (N/A — 0 new terms, with the inherited multi-source mandate noted). |
| CP8f | Term-slug + all-notes dedup/collision audit | **PASS** | Generalized collision audit run over ALL 8 planned `oc_*` doc notes AND term slugs across `term_dictionary/` + `resources/documentation/`: no planned `oc_*` note duplicates an existing term/doc; the openclaw doc folder has 0 existing `oc_*` notes; all 27 plan terms map to existing notes (linked, not recreated). Naming Notes: nothing flagged (`—`). |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | "Inlinks (existing notes → new notes)" maps every one of the 8 notes to ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 8; plus `repo_openclaw_security/skills/cli_wizard` + term backlinks); G8-Discoverability is in the gate table and inlink-addition is a gated execution step (in-degree ≥1 verified before commit). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
