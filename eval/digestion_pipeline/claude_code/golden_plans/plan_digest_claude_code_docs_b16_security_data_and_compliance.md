---
title: Sub-Plan B16 — Claude Code Docs: Security, Data & Compliance
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["security", "security-guidance", "data-usage", "zero-data-retention", "legal-and-compliance"]
---

# Sub-Plan B16: Security, Data & Compliance

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 5 pages that document Claude Code's security posture, the security-guidance plugin, data-usage and
privacy policies, Zero Data Retention (ZDR), and legal/compliance terms. P2 (Phase B) — these build on the
permission/sandbox/MCP/hooks cores defined by Phase A and are referenced by enterprise and admin sub-plans
(B14B admin/auth, B05A/B05B permissions/sandboxing, B13B code-review, B15B monitoring). B16 owns the
**prompt-injection** vocabulary term (per master Undigested Terms ownership: "Prompt injection→B16").

**Source**: Claude Code docs (`code.claude.com/docs/en`), 5 pages, 7,054 measured words. **Planned: 7 notes.**

## Content Strategy

- **Prioritize**: the security-architecture and prompt-injection-defense concepts (security.md) and the
  data-training/retention/ZDR policy matrix (data-usage.md + zero-data-retention.md) that admin/enterprise
  sub-plans (B14B, B15B) and permission sub-plans (B05A/B05B) link.
- **Group**: split `security.md` (1.4Kw, 7 H2 mixed) into security-architecture (concept) vs
  prompt-injection-defense (concept) vs cloud/remote security (concept); keep `legal-and-compliance.md`
  (0.5Kw) as one compact concept note. Split `security-guidance.md` (2.4Kw >2,500-approaching, 6 code
  blocks) into a plugin-overview/install procedure note vs a rules/cost/integration reference note to keep
  each ≤6 code blocks and one BB. Keep `data-usage.md` as one data-policy + data-flow note (telemetry
  defaults table folded in) and `zero-data-retention.md` as the dedicated ZDR concept note.
- **Skip / link-out (own other sub-plans)**: detailed Permissions config → B05A (`permissions.md`);
  Sandboxing → B05B (`sandboxing.md`, `sandbox-environments.md`); IDE/VS Code security → B12A (`vs-code.md`);
  Cloud-execution web surface → B12B (`claude-code-on-the-web.md`); Remote Control → B12B
  (`remote-control.md`); Monitoring/OpenTelemetry → B15B (`monitoring-usage.md`); Hooks (`ConfigChange`,
  the hook-event registry) → B07A (`hooks.md`); Code Review → B13B (`code-review.md`); `/security-review`
  command → B06 (`commands.md`); dev containers → B15A (`devcontainer.md`); credential management →
  B14B (`authentication.md`); env-var opt-outs (`DISABLE_TELEMETRY`, etc.) → B03A (`env-vars.md`);
  cloud-provider encryption-at-rest specifics → B14A. These are referenced via links, never duplicated.
- **Terms**: B16 captures ONE new `term_dictionary` note — **`term_prompt_injection`** (master-assigned,
  no doc-page home, no existing note). All other security/data/compliance vocabulary links to existing
  term notes (see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 5 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| security | /security | 1,380 | 0 | 7 | 12 | concept |
| security-guidance | /security-guidance | 2,354 | 6 | 9 | 9 | procedure/concept |
| data-usage | /data-usage | 1,944 | 0 | 5 | 8 | concept |
| zero-data-retention | /zero-data-retention | 890 | 0 | 4 | 2 | concept |
| legal-and-compliance | /legal-and-compliance | 486 | 0 | 4 | 6 | concept |

> **H2 lists (document order):**
> - **security**: How we approach security (H3 Security foundation, Permission-based architecture, Built-in protections, User responsibility) · Protect against prompt injection (H3 Core protections, Privacy safeguards, Additional safeguards) · MCP security · IDE security · Cloud execution security · Security best practices (H3 Working with sensitive code, Team security, Reporting security issues) · Related resources
> - **security-guidance**: (intro) · Prerequisites · Install the plugin (H3 Enable in cloud sessions and shared repositories) · What the plugin checks (H3 On each file edit, At the end of each turn, On each commit or push Claude makes, Review independence and limits) · Add your own rules (H3 Add guidance for the model-backed reviews, Add custom per-edit patterns, Rule file lookup locations) · Usage cost · Disable or uninstall · How the plugin integrates with Claude Code · How this fits with other security tools · Troubleshooting · Related resources
> - **data-usage**: Data policies (H3 Data training policy, Development Partner Program, Feedback using /feedback, Session quality surveys, Data retention) · Data access · Local Claude Code: Data flow and dependencies (H3 Cloud execution: Data flow and dependencies) · Telemetry services · Default behaviors by API provider (H3 WebFetch domain safety check)
> - **zero-data-retention**: (intro) · ZDR scope (H3 What ZDR covers, What ZDR does not cover) · Features disabled under ZDR (H3 Model availability under ZDR) · Data retention for policy violations · Request ZDR
> - **legal-and-compliance**: Legal agreements (H3 License, Commercial agreements) · Compliance (H3 Healthcare compliance (BAA)) · Usage policy (H3 Acceptable use, Authentication and credential use) · Security and trust (H3 Trust and safety, Security vulnerability reporting)

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **7 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_security_architecture.md` | concept | security: How we approach security (foundation, permission architecture, built-in protections, user responsibility), MCP security, Security best practices | 600 | Security foundation (Trust Center, SOC2/ISO); read-only-by-default permission architecture; write-access confined to working dir; four built-in protections (sandboxed bash, write restriction, allowlisting, Accept-Edits); user responsibility; MCP-server trust; team/sensitive-code/reporting best practices. Detailed permissions → B05A; sandboxing → B05B; monitoring → B15B; HackerOne → note 7. |
| 2 | `cc_prompt_injection_defenses.md` | concept | security: Protect against prompt injection (core protections, additional safeguards, best practices for untrusted content); Privacy safeguards (pointer) | 550 | What prompt injection is (links new `term_prompt_injection`); core protections (permission system, context-aware analysis, input sanitization, network-command approval); additional safeguards (network-request approval, isolated web-fetch context, trust verification, command-injection detection, fail-closed matching, secure credential storage, Windows WebDAV warning); best practices for untrusted content. |
| 3 | `cc_security_guidance_plugin.md` | procedure | security-guidance: intro, Prerequisites, Install the plugin, Enable in cloud/shared repos, Disable or uninstall | 600 | Install/enable/disable the security-guidance plugin (in-session vulnerability review). Prerequisites (CLI 2.1.144+, Python 3.8+, git repo); `/plugin install` + `/reload-plugins`; project `enabledPlugins` for cloud/shared; per-layer + whole-plugin disable env vars; `/plugin disable`/`uninstall`. ≤6 code blocks. |
| 4 | `cc_security_guidance_layers_and_rules.md` | concept | security-guidance: What the plugin checks (3 layers + review independence), Add your own rules, Usage cost, How it integrates (hooks), How this fits with other tools, Troubleshooting | 650 | The three review depths (per-edit pattern match, end-of-turn diff review, commit/push agentic review) + limits; review independence (separate fresh-context Claude); extension points (`claude-security-guidance.md`, `security-patterns.yaml` schema); usage cost + caps; hook-event registry (link-out B07A); defense-in-depth stack (`/security-review`→B06, Code Review→B13B, CI); troubleshooting. ≤6 code blocks (1 YAML schema). |
| 5 | `cc_data_usage_and_telemetry.md` | concept | data-usage: Data policies (training, DPP, feedback, surveys, retention), Data access, Local + Cloud data flow, Telemetry services, Default behaviors by provider, WebFetch domain safety check | 700 | Data-training policy (consumer opt-in vs commercial no-train); Development Partner Program; `/feedback` (5yr) + session-quality surveys; retention by account type (consumer 5yr/30d, commercial 30d, local cache 30d); local/cloud data flow + encryption-at-rest-by-provider table; telemetry/Sentry/feedback opt-outs; per-provider default-behaviors matrix; WebFetch domain safety check. Env-var detail → B03A; provider encryption → B14A; monitoring → B15B. |
| 6 | `cc_zero_data_retention.md` | concept | zero-data-retention: full page (scope, covers/not-covers, features disabled, model availability, policy-violation retention, request) | 550 | ZDR for Claude Code on Claude for Enterprise: real-time inference, no post-response storage; per-org enablement (sales/account team, not admin self-serve); what ZDR covers vs not (chat/Cowork/analytics-metadata/seat-mgmt/third-party); features auto-disabled (web, desktop cloud sessions, `/feedback`); model availability (Fable 5 excluded, `best`→Opus); 2-year retention for Usage-Policy violations; how to request + API-key→Enterprise migration. |
| 7 | `cc_legal_and_compliance.md` | concept | legal-and-compliance: full page (legal agreements, BAA, usage policy, auth/credential use, security & trust) + security: Reporting security issues (HackerOne) | 450 | Legal agreements (Commercial vs Consumer Terms; 1P/3P commercial agreement carries over); healthcare BAA auto-extends with ZDR (per-org); Acceptable Use Policy + Pro/Max ordinary-usage assumption; OAuth (subscriptions) vs API-key (developers/Agent SDK) authentication boundary + enforcement; Trust Center/Transparency Hub; HackerOne vulnerability reporting; June 15 2026 Agent SDK credit note. |

**Estimate: 7 notes** — concept ×6 (notes 1,2,4,5,6,7), procedure ×1 (note 3). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 5 (7,054 words). New `cc_` notes: 7. New `term_dictionary` notes: 1 (`term_prompt_injection`).
- Est. total digest words: ~4,100 (avg ~585/note). Code blocks: ~9 total (notes 3 and 4 only; ≤6 each).
- **Building Block Distribution**: concept ×6 (notes 1,2,4,5,6,7) · procedure ×1 (note 3). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_security_architecture` (7 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Progressive permission modes where an agent earns broader autonomy; relevance: the note's read-only-by-default → request-explicit-approval → Accept-Edits permission architecture is exactly the graduated-trust escalation ladder.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Security posture where everything is denied unless explicitly allowed; relevance: Claude Code's "strict read-only permissions by default" plus fail-closed unmatched-command handling is the default-deny stance this note documents.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — Filesystem/network isolation that confines what code can touch; relevance: the note's "sandboxed bash tool" built-in protection and write-access restriction to the working dir are the sandbox boundary mechanism this term defines.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — Open protocol for connecting LLMs to external tools/data; relevance: the note's "MCP security" section governs which MCP servers are trusted and how their permissions are configured, a core part of the security surface.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool; relevance: this note documents Claude Code's own security model (permission architecture, write boundary, built-in protections), so the product term is the definitional anchor.
- [GRC - Governance, Risk & Compliance](../../term_dictionary/term_grc.md) — The discipline of aligning security controls with policy and audit; relevance: the note's Anthropic security-program framing (SOC 2 Type 2, ISO 27001, Trust Center) and team-security/managed-settings guidance is GRC applied to an AI dev tool.
- [AI Safety](../../term_dictionary/term_ai_safety.md) — Making AI systems behave safely and within bounds; relevance: the note's "mitigate risks in agentic systems" framing and user-responsibility-to-review stance are concrete AI-safety controls for an autonomous coding agent.

### 2. `cc_prompt_injection_defenses` (7 term notes)
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — Attack that overrides an LLM's instructions via malicious injected text (new B16 capture); relevance: this note IS Claude Code's prompt-injection defense page — the new term note is its canonical definitional anchor.
- [Jailbreak](../../term_dictionary/term_jailbreak.md) — Bypassing an AI model's safety constraints via crafted input; relevance: the note's safeguards against attacker text that "overrides or manipulates the assistant's instructions" defend against the jailbreak-class manipulation this term covers.
- [OWASP LLM - Top 10 Security Risks for LLM Applications](../../term_dictionary/term_owasp_llm.md) — Standard catalogue of LLM application risks; relevance: prompt injection is LLM01 and the note's input-sanitization / command-injection-detection safeguards map to several OWASP-LLM categories.
- [Adversarial Attack](../../term_dictionary/term_adversarial_attack.md) — Inputs crafted to make a model misbehave; relevance: prompt injection is an adversarial-input attack against the agent, and the note's "no system is completely immune" caveat reflects the adversarial-robustness limits this term describes.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — Programmatic controls that constrain LLM behavior/IO; relevance: the note's layered defenses (permission gates, context-aware analysis, isolated web-fetch context, network-request approval) are precisely the input/output guardrails this term defines.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — Protection against server-side request forgery via attacker-controlled URLs; relevance: the note's network-command approval (`curl`/`wget` not auto-approved), isolated web-fetch context, and Windows WebDAV warning are SSRF-style protections against attacker-triggered outbound requests.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — Filesystem/network isolation for executing untrusted operations; relevance: the note recommends VMs/isolation for untrusted content and the permission system as the boundary, the sandboxing approach this term defines.

### 3. `cc_security_guidance_plugin` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's agentic coding tool with a plugin system; relevance: this note is the install/enable procedure for a first-party Claude Code plugin, so the product term grounds the host whose plugin/marketplace mechanics are used.
- [Skills](../../term_dictionary/term_skills.md) — Packaged markdown workflows/capabilities loaded into Claude Code; relevance: the plugin ships as an installable extension over Claude Code's customization layer, the same `/plugin`-managed extension family skills belong to.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — Controls that constrain or check LLM behavior/output; relevance: installing this plugin adds an automated security-review guardrail layer over Claude's own code edits, the in-session enforcement this term covers.
- [GRC - Governance, Risk & Compliance](../../term_dictionary/term_grc.md) — Aligning controls with org policy via managed/checked-in settings; relevance: the note's org-wide enablement via `enabledPlugins` in managed settings is a GRC distribution mechanism for a security control.
- [OWASP LLM - Top 10 Security Risks for LLM Applications](../../term_dictionary/term_owasp_llm.md) — Catalogue of LLM/code security risks; relevance: the plugin this note installs targets the injection / unsafe-deserialization / unsafe-DOM vulnerability classes OWASP-LLM enumerates.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Block-unless-allowed control posture; relevance: the note explains pairing the plugin's advisory findings with a blocking hook for hard enforcement, the deny-first escalation this term defines for cases the advisory layer cannot stop.

### 4. `cc_security_guidance_layers_and_rules` (7 term notes)
- [Red Teaming](../../term_dictionary/term_red_teaming.md) — Adversarially probing a system to surface vulnerabilities; relevance: the plugin's separate fresh-context reviewer "instructed only to find problems" against the diff is an automated red-team pass over Claude's own code changes.
- [OWASP LLM - Top 10 Security Risks for LLM Applications](../../term_dictionary/term_owasp_llm.md) — Standard LLM/code vulnerability catalogue; relevance: the three layers detect injection, unsafe deserialization (`pickle`), DOM injection, SSRF, weak crypto, and authorization bypass — the OWASP/secure-coding categories this term indexes.
- [XSS (Cross-Site Scripting)](../../term_dictionary/term_xss.md) — Injection of malicious script into web pages via unsafe DOM/HTML APIs; relevance: the per-edit pattern layer explicitly flags `dangerouslySetInnerHTML`, `.innerHTML =`, and `document.write`, the unsafe-DOM APIs that cause the XSS this term defines.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — Programmatic checks constraining LLM-produced output; relevance: the three review depths plus user-defined `security-patterns.yaml` rules are layered guardrails on the code Claude writes, and the note distinguishes advisory findings from hard enforcement.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — Block-unless-allowed posture; relevance: the note notes the plugin's findings are advisory and recommends pairing with a blocking hook / CI gate for the deny-first hard-enforcement these layers deliberately do not provide.
- [Adversarial Attack](../../term_dictionary/term_adversarial_attack.md) — Crafted inputs/code that exploit a system; relevance: the layers exist to catch injection / SSRF / authorization-bypass code that creates adversarial-attack surface, the threat class this term covers.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The host agent whose loop the plugin hooks into; relevance: the note details how the plugin registers on Claude Code lifecycle events (SessionStart, Stop, PostToolUse) and integrates with `/security-review` and Code Review — all Claude Code surfaces.

### 5. `cc_data_usage_and_telemetry` (7 term notes)
- [Data Retention](../../term_dictionary/term_data_retention.md) — How long a system keeps collected data before deletion; relevance: the note's core retention matrix (consumer 5-year/30-day, commercial 30-day, local cache 30-day, `/feedback` 5-year, shared transcripts 6-month) is exactly the data-retention policy this term defines.
- [PII (Personally Identifiable Information)](../../term_dictionary/term_pii.md) — Data that identifies an individual, requiring protection; relevance: the note describes redaction of API-key/token patterns before upload and TLS/AES encryption of prompts and outputs, the sensitive-data handling this term concerns.
- [Data Handling](../../term_dictionary/term_data_handling.md) — Practices for storing, transmitting, and protecting data; relevance: the note's encryption-in-transit (TLS 1.2+) and encryption-at-rest-by-provider table, plus local plaintext caching under `~/.claude/projects/`, are the data-handling controls this term covers.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — Controls limiting what an LLM tool sends/does; relevance: the WebFetch domain-safety-check (hostname checked against an Anthropic blocklist before fetch) and the non-essential-traffic opt-outs are data-egress guardrails this note documents.
- [Data Classification](../../term_dictionary/term_data_classification.md) — Categorizing data by sensitivity to set handling rules; relevance: the note distinguishes telemetry/metrics (no code or file paths) from `/feedback` transcripts (full conversation + code), a sensitivity distinction that drives differential handling.
- [GDPR - General Data Protection Regulation](../../term_dictionary/term_gdpr.md) — EU regulation on personal-data processing and retention; relevance: the note's user-controlled training preferences, deletion of cloud sessions, and bounded retention periods are the privacy-regulation-aligned controls GDPR mandates.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The tool whose data flows the note diagrams; relevance: the note documents Claude Code's own install/runtime external connections, telemetry, and feedback data paths, so the product term is the subject anchor.

### 6. `cc_zero_data_retention` (7 term notes)
- [Data Retention](../../term_dictionary/term_data_retention.md) — Policy for how long data is stored; relevance: ZDR is the zero-retention end of the data-retention spectrum — prompts/responses not stored after the response returns — making this term the direct concept ZDR specializes.
- [GRC - Governance, Risk & Compliance](../../term_dictionary/term_grc.md) — Aligning data controls to compliance obligations with audit; relevance: ZDR's per-org enablement, audit-logged actions, and admin capabilities (cost controls, analytics, server-managed settings) are GRC machinery for an enterprise data-control regime.
- [Records of Processing (RoP)](../../term_dictionary/term_records_of_processing.md) — Documented inventory of data-processing activities; relevance: the note's covers/does-not-cover matrix (inference covered; chat, Cowork, analytics metadata, seat data, third-party integrations not covered) is effectively a processing-scope record for ZDR.
- [GDPR - General Data Protection Regulation](../../term_dictionary/term_gdpr.md) — Regulation favoring data minimization and storage limitation; relevance: ZDR's no-server-side-persistence model is the strongest expression of the storage-limitation principle this regulation enforces.
- [Data Handling](../../term_dictionary/term_data_handling.md) — How data is stored/processed/protected across systems; relevance: the note specifies ZDR applies only to Anthropic's direct platform (not Bedrock/Vertex/Foundry) and that third-party/MCP data follows their own handling — a data-handling-scope boundary.
- [Data Governance](../../term_dictionary/term_data_governance.md) — Org-level policy and ownership over data lifecycle; relevance: ZDR is governed at the organization level (each new org enabled separately, account-team-managed), the org-scoped governance this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The product ZDR applies to; relevance: the note scopes ZDR specifically to Claude Code inference on Claude for Enterprise and lists which Claude Code features are disabled under it, so the product term is the subject anchor.

### 7. `cc_legal_and_compliance` (7 term notes)
- [GRC - Governance, Risk & Compliance](../../term_dictionary/term_grc.md) — Governance, risk, and compliance discipline; relevance: this note IS the legal/compliance page — Commercial vs Consumer Terms, BAA, Acceptable Use, Trust Center — the GRC artifacts this term catalogues for Claude Code.
- [Data Retention](../../term_dictionary/term_data_retention.md) — Policy for storing data over time; relevance: the note's BAA coverage is conditioned on ZDR (a retention posture) being active, tying healthcare compliance directly to the data-retention regime.
- [GDPR - General Data Protection Regulation](../../term_dictionary/term_gdpr.md) — Personal-data protection regulation; relevance: the note's Privacy Policy reference and commercial/consumer terms split are the legal-basis documents privacy regulations like GDPR require a processor to publish.
- [DSAR - Data Subject Access Request](../../term_dictionary/term_dsar.md) — A data subject's right to access/delete their data; relevance: the note's Consumer/Commercial terms and Trust Center govern the data-subject-rights obligations DSAR exercises against a service.
- [Records of Processing (RoP)](../../term_dictionary/term_records_of_processing.md) — Inventory documenting processing activities and legal basis; relevance: the note's BAA, commercial agreements, and authentication-method restrictions are the contractual/processing records an RoP would reference.
- [AI Safety](../../term_dictionary/term_ai_safety.md) — Responsible-AI program and acceptable-use enforcement; relevance: the note's Anthropic Usage Policy, Trust & Safety / Transparency Hub, and HackerOne vulnerability program are the AI-safety governance surface this term covers.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The product these legal terms bind; relevance: the note defines the license, OAuth-vs-API-key authentication boundary, and usage-policy terms that govern Claude Code use, so the product term is the subject anchor.

## Section Coverage Map

```
security.md
├── How we approach security ───────────── → note 1 (cc_security_architecture)
│   ├── Security foundation ────────────── → note 1
│   ├── Permission-based architecture ──── → note 1 (detail → B05A permissions.md)
│   ├── Built-in protections ───────────── → note 1 (sandboxed bash detail → B05B)
│   └── User responsibility ────────────── → note 1
├── Protect against prompt injection ───── → note 2 (cc_prompt_injection_defenses)
│   ├── Core protections ───────────────── → note 2
│   ├── Privacy safeguards ─────────────── → note 2 (pointer; full data policy → note 5)
│   └── Additional safeguards ──────────── → note 2 (credential storage detail → B14B)
├── MCP security ───────────────────────── → note 1
├── IDE security ───────────────────────── → linked out (B12A vs-code.md#security-and-privacy)
├── Cloud execution security ───────────── → note 5 (data flow) + linked out (B12B web / remote-control)
├── Security best practices ────────────── → note 1
│   ├── Working with sensitive code ────── → note 1 (dev containers → B15A)
│   ├── Team security ──────────────────── → note 1 (managed settings → B03A; monitoring → B15B; ConfigChange hook → B07A)
│   └── Reporting security issues ──────── → note 7 (HackerOne)
└── Related resources ──────────────────── → notes 1/2/3 (links)
security-guidance.md
├── (intro) ────────────────────────────── → note 3 (cc_security_guidance_plugin)
├── Prerequisites ──────────────────────── → note 3
├── Install the plugin ─────────────────── → note 3
│   └── Enable in cloud/shared repos ───── → note 3
├── What the plugin checks ─────────────── → note 4 (cc_security_guidance_layers_and_rules)
│   ├── On each file edit ──────────────── → note 4
│   ├── At the end of each turn ────────── → note 4
│   ├── On each commit or push ─────────── → note 4
│   └── Review independence and limits ─── → note 4
├── Add your own rules ─────────────────── → note 4
│   ├── Guidance for model-backed reviews → note 4
│   ├── Add custom per-edit patterns ───── → note 4
│   └── Rule file lookup locations ─────── → note 4
├── Usage cost ─────────────────────────── → note 4
├── Disable or uninstall ───────────────── → note 3
├── How the plugin integrates (hooks) ──── → note 4 (hook-event registry → B07A hooks.md)
├── How this fits with other tools ─────── → note 4 (/security-review → B06; Code Review → B13B)
├── Troubleshooting ────────────────────── → note 4
└── Related resources ──────────────────── → notes 3/4 (links)
data-usage.md
├── Data policies ──────────────────────── → note 5 (cc_data_usage_and_telemetry)
│   ├── Data training policy ───────────── → note 5
│   ├── Development Partner Program ────── → note 5
│   ├── Feedback using /feedback ───────── → note 5
│   ├── Session quality surveys ────────── → note 5 (env-var opt-outs → B03A)
│   └── Data retention ─────────────────── → note 5 (ZDR → note 6; local cache → B02B claude-directory)
├── Data access ────────────────────────── → note 5 (remote control → B12B)
├── Local Claude Code: Data flow ───────── → note 5
│   └── Cloud execution: Data flow ─────── → note 5 (web surface → B12B)
├── Telemetry services ─────────────────── → note 5 (env-var detail → B03A)
├── Default behaviors by API provider ──── → note 5 (provider specifics → B14A)
│   └── WebFetch domain safety check ───── → note 5 (WebFetch permission rules → B05A)
zero-data-retention.md
├── (intro) ────────────────────────────── → note 6 (cc_zero_data_retention)
├── ZDR scope (covers / does not cover) ── → note 6
├── Features disabled under ZDR ────────── → note 6
│   └── Model availability under ZDR ───── → note 6
├── Data retention for policy violations ─ → note 6
└── Request ZDR ────────────────────────── → note 6
legal-and-compliance.md
├── Legal agreements (license, commercial) → note 7 (cc_legal_and_compliance)
├── Compliance (Healthcare BAA) ────────── → note 7 (ZDR dependency → note 6)
├── Usage policy (acceptable use, auth) ── → note 7 (credential mgmt → B14B; Agent SDK → B19A)
└── Security and trust (HackerOne) ─────── → note 7
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| security.md (1.4Kw, 7 H2 mixed) | notes 1, 2 (+ note 5/7 absorb cloud-data/reporting; 3 link-outs) | distinct concepts: architecture/permissions vs prompt-injection defense; IDE/cloud-web owned by B12; HackerOne folded into legal note 7 |
| security-guidance.md (2.4Kw, 6 code) | notes 3 (procedure: install/enable/disable), 4 (concept: layers/rules/cost/integration) | one BB per note (procedure vs concept); splitting keeps each ≤6 code blocks (combined would exceed) and under the word cap with comfortable margin |
| data-usage.md (1.9Kw, 8 H3) | note 5 (single concept note) | cohesive data-policy + data-flow + telemetry topic; ~700w within caps; env-var/provider detail linked out to B03A/B14A rather than inlined |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_security_architecture | concept | 600 | 0 | ✅ |
| 2 | cc_prompt_injection_defenses | concept | 550 | 0 | ✅ |
| 3 | cc_security_guidance_plugin | procedure | 600 | 5 | ✅ |
| 4 | cc_security_guidance_layers_and_rules | concept | 650 | 2 | ✅ |
| 5 | cc_data_usage_and_telemetry | concept | 700 | 0 | ✅ |
| 6 | cc_zero_data_retention | concept | 550 | 0 | ✅ |
| 7 | cc_legal_and_compliance | concept | 450 | 0 | ✅ |

No note approaches the caps (≤2,500w / ≤6 code / ≤400 lines). Notes 3 (install commands + JSON `enabledPlugins`)
and 4 (`security-patterns.yaml` schema + `.claude-security-guidance.md` example) carry code; both ≤6 blocks.
No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_security_architecture cc_prompt_injection_defenses cc_security_guidance_plugin cc_security_guidance_layers_and_rules cc_data_usage_and_telemetry cc_zero_data_retention cc_legal_and_compliance"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB (incl. new term_prompt_injection once captured)
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (7 notes, all P2). All gates must pass before commit. `term_prompt_injection` is captured
BEFORE the `cc_` notes that link it (note 2), so G5 finds no ghost.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts (new `term_prompt_injection` created first) | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 7 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability (inbound) | each of the 7 notes RECEIVES ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (entry) | each note linked from `entry_claude_code_docs.md` (B16 rows added at execution) | DB query on entry-point links |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes). This sub-plan **contributes its 7 rows** under a
"Security, Data & Compliance" cluster + increments the BB-distribution counts (concept ×6, procedure ×1).

## Undigested Terms Plan (Step 4e)

B16 creates **exactly ONE** new `term_dictionary` note — **`term_prompt_injection`** — which the master
assigns to B16 ("Prompt injection→B16"): it is a cross-cutting LLM-security vocabulary term with NO
dedicated Claude Code doc page (only a sub-section of `security.md`) and **no existing vault term note**
returns empty). All other security/data/compliance vocabulary maps to an existing substantive term note
(link) or a B16 `cc_` note (Pattern B):

| Term surfaced on B16 pages | Disposition |
|---|---|
| Prompt injection | **NEW capture `term_prompt_injection`** (B16-owned; defined generically, NOT a Claude Code doc concept) |
| Sandboxed bash / filesystem-network isolation | link `term_sandbox` (exists); detail owned by B05B |
| Permission mode / read-only-by-default / Accept-Edits | link `term_graduated_trust` + `term_deny_first` (exist); detail owned by B05A |
| MCP / MCP server trust | link `term_mcp` (exists); detail owned by B08A |
| Zero Data Retention (ZDR) | note 6 `cc_zero_data_retention` (doc concept) |
| Data retention / training policy / DPP | note 5 `cc_data_usage_and_telemetry` (doc concept); links `term_data_retention` |
| Telemetry / Sentry / WebFetch domain safety check | note 5 (doc concept); env-var opt-outs owned by B03A |
| Security-guidance plugin | notes 3/4 (doc procedure/concept); plugin mechanism owned by B09A |
| BAA / Acceptable Use Policy / OAuth-vs-API-key | note 7 `cc_legal_and_compliance` (doc concept); links `term_grc` |
| Defense in depth / vulnerability classes (injection, XSS, SSRF, deserialization) | linked to existing terms `term_owasp_llm`, `term_xss`, `term_ssrf_guard`, `term_adversarial_attack`, `term_red_teaming`, `term_guardrails` (all exist) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 5 pages scanning emphasis/tables/captions for
newly-surfaced terms. Beyond the master-assigned `prompt injection`, candidate non-glossary terms surfaced —
"command injection", "fail-closed matching", "trust verification", "WebDAV", "defense in depth", "Development
Partner Program", "session quality survey" — but each is either (a) a documentation concept captured inline
in a B16 `cc_` note, (b) covered by an existing term note (`term_deny_first` for fail-closed,
`term_ssrf_guard`/`term_owasp_llm` for command injection, `term_owasp_llm` for defense in depth), or (c) a
product-specific feature name not warranting a generic term note. **1 new B16 `term_dictionary` capture:
`term_prompt_injection`.**

**Step 10.5f Term-Slug Specificity + Collision Audit:** the one new slug `term_prompt_injection` is
**specific** (a single named attack technique, not an over-general bucket like `term_security`) and
**collision-checked**: no existing `term_prompt_injection.md` on disk or in the DB; nearest existing notes —
`term_jailbreak` (constraint bypass, different mechanism), `term_adversarial_attack` (broad parent class),
`term_owasp_llm` (catalogue listing injection as LLM01) — are **related but distinct senses**, so a dedicated
note is warranted and they are linked, not merged. Adversarial dedup-verify (skeptic pass): confirmed
`term_prompt_injection` is the canonical name used across the vault's LLM-security cluster
(`bedrock_security_prompt_injection`, `thought_llm_security`, `thought_openclaw_slipbox_dm_untrusted_input_boundary`)
yet none defines the term itself — a genuine gap, not a duplicate.

## Term-Note Authoring Requirements

**B16 authors ONE term note — `term_prompt_injection`** — per the full inherited spec (master Term-Note
Authoring Requirements). Requirements for this note:

- **File**: `resources/term_dictionary/term_prompt_injection.md`; H1 `# Term: Prompt Injection` (matches the
  `# Term: <Name>` convention of `term_jailbreak`, `term_red_teaming`, `term_adversarial_attack`).
- **Definition is generic**, NOT Claude-Code-specific: prompt injection = an attack where adversarial text
  inserted into model-visible content overrides or manipulates the LLM's instructions; cover direct vs
  indirect (data-borne) injection, and the agentic-tool risk (injected instructions triggering tool calls).
  vault LLM-security cluster (`term_owasp_llm` — LLM01, `term_jailbreak`, `term_adversarial_attack`,
  `term_guardrails`, `bedrock_security_prompt_injection`, `thought_llm_security`), and OWASP/standard
  references — do NOT author from intuition or from the Claude Code page alone.
- **Required H2 sections** per the term-note canonical: `## Definition`, `## Why It Matters` / `## Key
  Points`, `## Related Terms` (cross-domain, ≥6 indexed links incl. `term_jailbreak`, `term_owasp_llm`,
  `term_adversarial_attack`, `term_guardrails`, `term_ssrf_guard`, `term_red_teaming`, plus `cc_prompt_injection_defenses`),
  `## References`. YAML: first tag `resource`, then `term`/`glossary`; quoted year strings; itemized lists.
- **Glossary update**: add a `term_prompt_injection` entry to the matching acronym/glossary index (per
  `/tessellum-capture-term-note`).
- Captured via `/tessellum-capture-term-note` **before** note 2 (`cc_prompt_injection_defenses`) is written so
  the link resolves (G5).

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit. Capture `term_prompt_injection` first, then the 7 `cc_` notes.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (notes 3/4 carry install commands, `enabledPlugins` JSON, `security-patterns.yaml`,
  `.claude-security-guidance.md` — copy exactly). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer);
  reindex incrementally and verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7 in-degree ≥1 each):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 5 | product term → CC security model + data usage |
| `term_dictionary/term_prompt_injection.md` (new) | note 2 | term ↔ CC prompt-injection-defense doc (reciprocal) |
| `term_dictionary/term_graduated_trust.md` | note 1 | permission-modes term → CC permission architecture |
| `term_dictionary/term_data_retention.md` | notes 5, 6 | retention term → CC data-usage + ZDR |
| `term_dictionary/term_grc.md` | note 7 | governance/compliance term → CC legal & compliance |
| `term_dictionary/term_owasp_llm.md` | notes 2, 4 | LLM-risk catalogue → CC injection defenses + security-guidance layers |
| `analysis_thoughts/thought_llm_security.md` | notes 2, 4 | vault LLM-security thought → CC prompt-injection + code-review layers |

## Follow-up Recommendations

- After the 7 notes + 1 term note land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above;
  queue the 7 rows for `entry_claude_code_docs.md`; update the glossary index with `term_prompt_injection`;
  `/tessellum-check-broken-links`; verify G7 in-degree ≥1 for each new note.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY** — see Review Sign-Off below (9/9) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B16, 2026-06-13)

- **Source re-read (Step 2)**: all 5 pages re-read from `inbox/claude_code_docs/`; measured words match the
  master's figures within tolerance (security 1,380 · security-guidance 2,354 · data-usage 1,944 ·
  zero-data-retention 890 · legal-and-compliance 486 = 7,054). No >1.5× under-estimate; one planned split of
  `security-guidance.md` (highest density + code) into notes 3/4, documented in Split Decisions.
- **Notes**: 7 (concept 6, procedure 1) — matches master estimate. No new splits beyond the documented ones.
- **Per-Note Related Notes Mapping (Step 8)**: authored to the **≥6 relevancy-selected term-note** standard —
  6–7 term notes per note (18 distinct `term_dictionary/` terms), each with a per-link what-it-is + relevancy
  (G5 PASS)** including the new `term_prompt_injection` (created in this sub-plan); relpaths
  `../../term_dictionary/`.
- **Dedup (Step 2b/master G-B)**: checked across `term_dictionary/` AND `resources/documentation/` — no
  existing `cc_*` security/data/compliance note (`claude_code/` dir is empty); the LLM-security concepts are
  covered by *term* notes (linked, not recreated). Only genuine gap = `term_prompt_injection` → capture.
- **Step 2d new-term scan**: 1 new capture (`term_prompt_injection`, master-assigned); all other surfaced
  terms route to existing notes or B16 `cc_` doc concepts.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5/G7/G8 verification rows, Term-Note Authoring Requirements (1 term).
- **28-item checklist**: PASS — term-note items satisfied for the single `term_prompt_injection` capture;
  entry-point + pacing inherited from master.
- **Status**: augmented and self-reviewed; set to `ready` after the 9 review checkpoints below all passed.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | All gates per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase) incl. G7/G8 Discoverability (inbound in-degree ≥1 + entry-point link). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE); B16 contributes 7 rows under a "Security, Data & Compliance" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 7 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + `## Overview` / source-mirrored H2 / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer match the master Format Definition verbatim. |
| CP6 | Borderline density → split | ✅ PASS | `security-guidance.md` (2.4Kw + 6 code) PROMOTED to a split (notes 3/4) to stay ≤6 code + comfortable word margin; all 7 notes 450–700w. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: security 1,380 · security-guidance 2,354 · data-usage 1,944 · zero-data-retention 890 · legal-and-compliance 486 = 7,054 = master figure. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
