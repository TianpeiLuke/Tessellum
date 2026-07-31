---
title: Sub-Plan se01 — OpenClaw Docs: Security
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["security/CONTRIBUTING-THREAT-MODEL", "security/THREAT-MODEL-ATLAS", "security/formal-verification", "security/incident-response", "security/network-proxy"]
---

# Sub-Plan se01: Security

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview` → body → `## Related Notes` → `## References` → bold footer, ≤400L/≤2500w/≤6 code, one BB/note), dedup-before-create (three-way across `term_dictionary` + `documentation/` + `repo_openclaw*`), the 9-GATE, cross-references, and entry-point wiring are ALL inherited from the master.

## Scope

The 5 OpenClaw `security/` pages — the platform's security posture corpus: the MITRE ATLAS threat model (architecture/trust boundaries, per-tactic threat catalog, ClawHub supply-chain analysis, risk matrix, recommendations), how to contribute to that threat model, the TLA+/TLC formal-verification suite for the highest-risk paths, the incident-response runbook, and the operator-managed forward-proxy (egress-filtering / SSRF defense-in-depth) feature. **Priority P1 (Phase A)** per master — security is part of the conceptual/operational core, and these pages define the trust-boundary / threat / SSRF / exec-approval / pairing / session-isolation vocabulary that the gateway, tools, channels, and ClawHub sub-plans reference. The code-side counterparts `repo_openclaw_security` and the `snippet_openclaw_security_*` / `snippet_openclaw_gateway_*` snippets are LINKED, not recreated.

**Source**: OpenClaw docs, 5 pages, 8,011 measured words. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| CONTRIBUTING-THREAT-MODEL | security/CONTRIBUTING-THREAT-MODEL | 690 | 0 | 7 | 7 | procedure (contribution process + ATLAS/threat-ID/risk taxonomy) |
| THREAT-MODEL-ATLAS | security/THREAT-MODEL-ATLAS | 3,660 | 5 | 9 | 26 | argument + model (split: architecture/model · threat catalog/argument · ClawHub supply chain + risk/recs/argument) |
| formal-verification | security/formal-verification | 783 | 1 | 5 | 8 | argument (machine-checked security models, TLA+/TLC) |
| incident-response | security/incident-response | 341 | 0 | 5 | 0 | procedure |
| network-proxy | security/network-proxy | 2,537 | 13 | 8 | 1 | procedure (split: routing/config · requirements/denylist/validation) |

(Code = ```` ``` ```` fence pairs, i.e. raw-fence-count ÷ 2.)

## Content Strategy

- **Prioritize**: (1) the trust-boundary / system-architecture model and the per-ATLAS-tactic threat catalog (the canonical security reference every other OpenClaw note points back to); (2) the network-proxy egress/SSRF configuration (operationally load-bearing for hardened deployments); (3) the formal-verification claims (the unique machine-checked-guarantee argument).
- **Split**: `THREAT-MODEL-ATLAS.md` (3,660w > 2,500w cap, mixed BB, 26 H3) → 3 notes (architecture+data-flows model · ATLAS threat catalog argument · ClawHub supply-chain + risk matrix + recommendations argument). `network-proxy.md` (2,537w > 2,500w, 13 code fences ≫ 6 cap) → 2 notes (why/routing/config procedure · requirements/denylist/validation/CA-trust/limits procedure) so each note stays ≤6 code fences.
- **Link-out (do NOT redefine)**: MITRE ATLAS/ATT&CK → link `term_mitre_attack`; prompt injection → `term_prompt_injection`; SSRF classifier internals → `term_ssrf_guard` + `repo_openclaw_security` + `snippet_openclaw_security_*`; exec-approvals → `snippet_openclaw_gateway_exec_approval_manager`; gateway auth modes / trusted-proxy → gw06/gw04 sub-plan notes (cross-link, planned); `web_fetch` trusted-env-proxy → to08 (planned); `openclaw proxy` debug command → cl06 (planned); ClawHub moderation/security → cw01/cw03 (planned); pairing/routing/session isolation impl → `repo_openclaw_gateway` / `repo_openclaw_sessions` / `repo_openclaw_channels` + sibling oc_ notes.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_security_threat_model_architecture.md` | model | THREAT-MODEL-ATLAS.md: MITRE ATLAS framework (attribution), §1 Introduction (Purpose/Scope/Out-of-Scope), §2 System Architecture (2.1 Trust Boundaries, 2.2 Data Flows) | 600 | OpenClaw's security architecture model: the 5 trust boundaries (Channel Access → Session Isolation → Tool Execution → External Content → Supply Chain), the in-scope component matrix, and the F1–F6 data-flow protections, framed on MITRE ATLAS. |
| 2 | `oc_security_threat_catalog_atlas.md` | argument | THREAT-MODEL-ATLAS.md: §3 Threat Analysis by ATLAS Tactic (3.1 Recon → 3.8 Impact, all T-* threats), §7.1 ATLAS Technique Mapping, §7.3 Glossary | 750 | The per-ATLAS-tactic threat catalog: ~22 T-* threats (Recon, Initial Access, Execution incl. prompt injection, Persistence, Defense Evasion, Discovery, Collection/Exfiltration, Impact) with vector, affected components, current mitigations, residual risk, and the AML.T0xxx technique mapping. |
| 3 | `oc_security_clawhub_supply_chain.md` | argument | THREAT-MODEL-ATLAS.md: §4 ClawHub Supply Chain Analysis (4.1 Controls, 4.2 Moderation Flag Patterns, 4.3 Planned Improvements), §5 Risk Matrix (5.1 Likelihood vs Impact, 5.2 Critical Path Attack Chains), §6 Recommendations Summary, §7.2 Key Security Files | 700 | ClawHub skill-marketplace supply-chain security: current controls + their effectiveness, the `moderation.ts` FLAG_RULES patterns and their limits, planned improvements (VirusTotal Code Insight), the likelihood×impact risk matrix, the three critical attack chains, and the P0–P2 recommendation roadmap. |
| 4 | `oc_security_contributing_threat_model.md` | procedure | CONTRIBUTING-THREAT-MODEL.md: Ways to contribute (Add a threat / Suggest a mitigation / Propose an attack chain / Fix content), What we use (ATLAS, Threat IDs, Risk levels), Review process, Resources, Contact, Recognition | 550 | How to contribute to the OpenClaw threat model: the four contribution paths, the threat-ID category codes (RECON/ACCESS/EXEC/…/IMPACT), the four risk levels, the maintainer review/triage/merge process, and the live-vuln vs threat-model distinction. |
| 5 | `oc_security_formal_verification.md` | argument | formal-verification.md: goal/what-this-is/caveats, Where the models live, Reproducing results (TLA+/TLC setup), per-claim models (gateway exposure, node exec pipeline, pairing store, ingress gating, routing/session-key isolation), v1++ bounded models (concurrency/idempotency/trace correctness) | 650 | OpenClaw's machine-checked security regression suite (TLA+/TLC): the bounded-model-checking approach, its explicit caveats (model≠code, results bounded by explored state space), how to reproduce with the vendored `tla2tools.jar`, and each green/red claim — gateway-exposure, node-exec approvals, pairing TTL/caps, ingress mention-gating, session-key isolation, plus the v1++ concurrency/idempotency/trace models. |
| 6 | `oc_security_incident_response.md` | procedure | incident-response.md: §1 Detection and triage, §2 Assessment (severity guide), §3 Response, §4 Communication (disclosure policy), §5 Recovery and follow-up | 450 | The OpenClaw security incident runbook: signal sources + initial triage, the Critical/High/Medium/Low severity guide, the reproduce-patch-validate response flow, GHSA/CVE coordinated-disclosure communication, and post-incident review + follow-up hardening. |
| 7 | `oc_security_network_proxy_routing.md` | procedure | network-proxy.md: intro, Why use a proxy, How OpenClaw routes traffic (Proxyline, http/https proxy schemes, no_proxy clearing), Related proxy terms, Configuration (proxyUrl, env var, Gateway Loopback Mode) | 650 | Routing OpenClaw runtime HTTP/WebSocket egress through an operator-managed forward proxy: why (central egress/SSRF/DNS-rebinding/auditability), how routing works via Proxyline, http:// vs https:// proxy endpoints, the related proxy settings, and configuration incl. the `proxy.loopbackMode` (gateway-only/proxy/block) Gateway control-plane exception. |
| 8 | `oc_security_network_proxy_hardening.md` | procedure | network-proxy.md: Proxy Requirements, Recommended blocked destinations (denylist table + ssrf.ts parity hooks), Validation (`openclaw proxy validate`, JSON, curl), Proxy CA trust (`proxy.tls.caFile` vs `NODE_EXTRA_CA_CERTS`), Limits (surface table) | 650 | Hardening the forward proxy: required proxy policy (bind loopback, post-DNS IP blocking, fail-closed bypass rejection), the recommended SSRF denylist of loopback/RFC1918/link-local/cloud-metadata/NAT64/6to4/Teredo ranges (mirroring `ssrf.ts` parity hooks), validating with `openclaw proxy validate`, private-CA proxy-endpoint trust, and the coverage limits (raw sockets, IRC, debug proxy). |

## Section Coverage Map

```
CONTRIBUTING-THREAT-MODEL.md (690w)
├── Ways to contribute (Add a threat / Suggest a mitigation / Propose
│   an attack chain / Fix or improve existing content) ─────────────── → note 4 (oc_security_contributing_threat_model)
├── What we use (MITRE ATLAS framework / Threat ids / Risk levels) ─── → note 4
├── Review process ────────────────────────────────────────────────── → note 4
├── Resources / Contact / Recognition ─────────────────────────────── → note 4
└── Related ───────────────────────────────────────────────────────── → note 4 (cross-links to notes 1-3, 5)
THREAT-MODEL-ATLAS.md (3,660w)
├── MITRE ATLAS framework (attribution, key resources) ────────────── → note 1 (oc_security_threat_model_architecture)
├── Contributing to This Threat Model (pointer) ───────────────────── → note 1 (→ note 4)
├── §1 Introduction (1.1 Purpose, 1.2 Scope, 1.3 Out of Scope) ────── → note 1
├── §2 System Architecture (2.1 Trust Boundaries, 2.2 Data Flows) ─── → note 1
├── §3 Threat Analysis by ATLAS Tactic (3.1 Recon → 3.8 Impact,
│   all T-RECON/ACCESS/EXEC/PERSIST/EVADE/DISC/EXFIL/IMPACT) ──────── → note 2 (oc_security_threat_catalog_atlas)
├── §7.1 ATLAS Technique Mapping ──────────────────────────────────── → note 2
├── §7.3 Glossary ─────────────────────────────────────────────────── → note 2
├── §4 ClawHub Supply Chain Analysis (4.1/4.2/4.3) ────────────────── → note 3 (oc_security_clawhub_supply_chain)
├── §5 Risk Matrix (5.1 Likelihood vs Impact, 5.2 Attack Chains) ──── → note 3
├── §6 Recommendations Summary (6.1 P0, 6.2 P1, 6.3 P2) ───────────── → note 3
├── §7.2 Key Security Files ───────────────────────────────────────── → note 3
└── Related ───────────────────────────────────────────────────────── → notes 1-3 (cross-links to 4, 5)
formal-verification.md (783w)
├── goal / what this is / caveats (intro) ─────────────────────────── → note 5 (oc_security_formal_verification)
├── Where the models live ─────────────────────────────────────────── → note 5
├── Important caveats ─────────────────────────────────────────────── → note 5
├── Reproducing results (TLA+/TLC, make targets) ──────────────────── → note 5
├── per-claim models (Gateway exposure / Node exec pipeline / Pairing
│   store / Ingress gating / Routing-session-key isolation) ───────── → note 5
├── v1++ additional bounded models (Pairing concurrency/idempotency,
│   Ingress trace correlation/idempotency, Routing dmScope precedence) → note 5
└── Related ───────────────────────────────────────────────────────── → note 5 (cross-links to 1, 4)
incident-response.md (341w)
├── §1 Detection and triage ───────────────────────────────────────── → note 6 (oc_security_incident_response)
├── §2 Assessment (severity guide) ────────────────────────────────── → note 6
├── §3 Response ───────────────────────────────────────────────────── → note 6
├── §4 Communication (disclosure policy) ──────────────────────────── → note 6
└── §5 Recovery and follow-up ─────────────────────────────────────── → note 6
network-proxy.md (2,537w)
├── intro (optional defense in depth) ─────────────────────────────── → note 7 (oc_security_network_proxy_routing)
├── Why use a proxy ───────────────────────────────────────────────── → note 7
├── How OpenClaw routes traffic (Proxyline, http/https schemes,
│   no_proxy clearing, plugin custom transports) ──────────────────── → note 7
├── Related proxy terms ───────────────────────────────────────────── → note 7 (link-out gw04/gw06/to08/cl06)
├── Configuration (proxyUrl, env var, ### Gateway Loopback Mode,
│   container caveat) ─────────────────────────────────────────────── → note 7
├── Proxy Requirements ────────────────────────────────────────────── → note 8 (oc_security_network_proxy_hardening)
├── Recommended blocked destinations (denylist table, ssrf.ts hooks) ─ → note 8
├── Validation (`openclaw proxy validate`, JSON, curl) ─────────────── → note 8
├── Proxy CA trust (proxy.tls.caFile vs NODE_EXTRA_CA_CERTS) ───────── → note 8
└── Limits (surface table) ────────────────────────────────────────── → note 8
```
No orphaned sections. Every H2/H3 across all 5 pages maps to exactly one planned note. Pointers to other-section/other-sub-plan content (ATLAS external links, `openclaw proxy` CLI, trusted-proxy auth, web_fetch trusted-env-proxy, ClawHub moderation) are link-outs, not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| THREAT-MODEL-ATLAS.md (3,660w, 9 H2 / 26 H3, mixed BB) | notes 1 + 2 + 3 | Exceeds the 2,500w cap by ~46% and mixes three distinct building blocks: the architecture/trust-boundary/data-flow **model** (§1–2), the per-ATLAS-tactic threat **argument** catalog (§3 + §7.1/7.3), and the ClawHub supply-chain + risk-matrix + recommendations **argument** (§4–6 + §7.2). Splitting keeps one BB per note and each note ≤750w / ≤2 code fences (the ASCII trust-boundary diagram → note 1; the moderation regex + attack-chain fences → notes 2/3). |
| network-proxy.md (2,537w, 8 H2 / 1 H3, 13 code fences) | notes 7 + 8 | Exceeds the 2,500w cap and has 13 code fences (≫ the 6-fence cap) — un-splittable into one compliant note. Natural seam between the **routing/why/config** procedure (intro → Why → How routes → Related terms → Configuration incl. Gateway Loopback Mode) and the **requirements/denylist/validation/CA/limits** hardening procedure (Proxy Requirements → blocked destinations → Validation → CA trust → Limits). Each half lands ~650w with ≤6 code fences (note 7 ≈ 6 yaml/bash/text fences selectively reproduced; note 8 ≈ 5 yaml/bash/json fences). |

## Summary Statistics & Building Block Distribution

- Source pages: **5** (8,011 measured words). New `oc_` notes: **8**. New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **model ×1** (note 1) · **argument ×3** (notes 2, 3, 5) · **procedure ×4** (notes 4, 6, 7, 8).
- Est. digest words ≈ 5,000 (avg ~625/note; range 450–750). 19 source code fences (5 ATLAS + 1 formal-verification + 13 network-proxy) distribute across the model/argument/procedure notes; every note kept ≤6 fences (config/denylist/validation snippets reproduced selectively, verbatim where load-bearing).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_security_threat_model_architecture (10t · 11s · 11d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — structured enumeration of assets, trust boundaries, and adversary capabilities; relevance: this note IS OpenClaw's threat-model architecture (the 5 trust boundaries + scope matrix).
- [MITRE ATT&CK / ATLAS](../../term_dictionary/term_mitre_attack.md) — adversary tactic/technique taxonomy; relevance: the whole model is framed on MITRE ATLAS (AML.T0xxx), attributed in §MITRE ATLAS framework.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment limiting tool/command blast radius; relevance: Trust Boundary 3 (Tool Execution) is the Docker/host execution sandbox.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial instructions smuggled into LLM input; relevance: Trust Boundary 4 (External Content) exists to contain prompt-injection from fetched URLs/emails.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — server-side-request-forgery defense via DNS pinning + IP blocking; relevance: Trust Boundary 3 lists "SSRF protection (DNS pinning + IP blocking)".
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — risk from third-party/dependency code paths; relevance: Trust Boundary 5 is the ClawHub supply chain.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool-provider interface; relevance: MCP servers are an in-scope component in the §1.2 scope matrix and §7.3 glossary.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted multi-channel coding-agent gateway; relevance: this is the system the architecture model documents.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity before granting access; relevance: Trust Boundary 1 (Channel Access) does Token/Password/Tailscale auth + AllowFrom validation.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: gateway control-plane and channel ingress ride WebSocket connections crossing Boundary 1→2.

**Docs**
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — Claude Code's permission/sandbox trust-boundary architecture; relevance: the closest peer trust-boundary model for a coding agent.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — fs+network isolation layers; relevance: peer realization of Trust Boundary 3 (execution sandbox).
- [cc_channels_security_and_enterprise_controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — channel access controls; relevance: peer of Trust Boundary 1 (channel access gating).
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — session isolation + credential handling; relevance: peer of Boundary 2 (session isolation) + token-at-rest concern.
- [pi_security_model](../pi/pi_security_model.md) — pi agent's end-to-end security model; relevance: sibling-ecosystem whole-system trust model for comparison.
- [band_a2a_gateway](../band/band_a2a_gateway.md) — Band agent-to-agent gateway trust surface; relevance: another gateway-fronted agent platform's boundary set.
- [oc_security_threat_catalog_atlas](oc_security_threat_catalog_atlas.md) — per-ATLAS-tactic threat catalog (planned, this series); relevance: enumerates the threats this architecture's boundaries defend.
- [oc_security_clawhub_supply_chain](oc_security_clawhub_supply_chain.md) — ClawHub supply-chain analysis (planned, this series); relevance: deep-dive on Trust Boundary 5.
- [oc_security_formal_verification](oc_security_formal_verification.md) — TLA+/TLC models (planned, this series); relevance: machine-checks the boundary properties (gateway exposure, session-key isolation).
- [oc_security_network_proxy_routing](oc_security_network_proxy_routing.md) — egress proxy routing (planned, this series); relevance: the operator control for the F4 external data-flow / SSRF boundary.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — the `src/security/*` + `src/infra/net/ssrf.ts` code; relevance: code-side counterpart of the architecture's mitigations.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway auth/routing; relevance: implements Trust Boundary 1.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session key + isolation; relevance: implements Trust Boundary 2.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime + tool policy; relevance: implements Trust Boundary 3 (tool execution).
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel ingress/pairing; relevance: untrusted-zone → Boundary 1 entry surface.

**Snippets**
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — assembles the trust-axis audit finding set; relevance: code expression of the boundary-by-boundary risk view.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime trust matrix collector; relevance: Boundary 3 risk escalation logic.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content XML wrap policy; relevance: Boundary 4 "external content wrapping" mechanism.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token/password/tailscale auth modes; relevance: Boundary 1 auth options listed in the diagram.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — per-call authorization dispatch; relevance: Boundary 1 access-control enforcement.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing + AllowFrom allowlist; relevance: Boundary 1 device pairing + AllowList validation.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — `agent:channel:peer` session key; relevance: Boundary 2 session-key isolation primitive.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool policy; relevance: Boundary 3 "tool policies per agent".
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval gating; relevance: Boundary 3 host-exec approval path.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — managed-proxy + loopback connect; relevance: F4 external data-flow egress control.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — static skill analyzer; relevance: Boundary 5 supply-chain moderation control.

### oc_security_threat_catalog_atlas (10t · 12s · 11d)

**Terms**
- [MITRE ATT&CK / ATLAS](../../term_dictionary/term_mitre_attack.md) — AI/ML adversary technique taxonomy; relevance: every T-* entry carries its AML.T0xxx ATLAS ID (§7.1 mapping).
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial-instruction smuggling; relevance: T-EXEC-001 (direct) / T-EXEC-002 (indirect) / T-EXEC-003 are prompt injection.
- [Jailbreak](../../term_dictionary/term_jailbreak.md) — bypassing model guardrails; relevance: the execution-tactic threats are jailbreak-style manipulations of agent behavior.
- [Adversarial Attack](../../term_dictionary/term_adversarial_attack.md) — crafted input to subvert a model; relevance: AML.T0043 "Craft Adversarial Data" backs T-EXEC-004/T-EVADE-001/002.
- [Content Exfiltration](../../term_dictionary/term_content_exfiltration.md) — unauthorized data egress; relevance: T-EXFIL-001/002/003 (web_fetch theft, message send, credential harvest).
- [Credential Stuffing](../../term_dictionary/term_credential_stuffing.md) — credential-abuse access pattern; relevance: T-ACCESS-003 token theft + T-EXFIL-003 credential harvesting.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — SSRF blocking; relevance: T-EXFIL-001 mitigation is "SSRF blocking for internal networks".
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — third-party-code risk; relevance: T-PERSIST-001/002 are AML.T0010 supply-chain compromise.
- [OWASP LLM Top 10](../../term_dictionary/term_owasp_llm.md) — LLM-app risk taxonomy; relevance: cross-frame for the same threats (prompt injection, insecure output, supply chain) ATLAS catalogs here.
- [Guardrails](../../term_dictionary/term_guardrails.md) — runtime safety filters; relevance: "Current Mitigations" rows (pattern detection, output filtering) are guardrail controls.

**Docs**
- [cc_security_guidance_layers_and_rules](../claude_code/cc_security_guidance_layers_and_rules.md) — layered guidance/guardrail rules; relevance: peer mitigation framing for the execution-tactic threats.
- [cc_hooks_guardrail_and_audit_recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail+audit hook recipes; relevance: peer pattern for the "output validation / confirmation" recommendations.
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — web-tool security limits; relevance: peer of T-EXFIL-001 (web_fetch exfiltration) controls.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command-approval gating; relevance: peer of T-EXEC-004 exec-approval-bypass mitigation.
- [pi_security_model](../pi/pi_security_model.md) — agent threat/mitigation model; relevance: sibling-ecosystem threat coverage for cross-reference.
- [band_a2a_gateway](../band/band_a2a_gateway.md) — A2A gateway threat surface; relevance: another agent platform's exposure to the same tactic set.
- [oc_security_threat_model_architecture](oc_security_threat_model_architecture.md) — architecture/trust-boundaries (planned, this series); relevance: the boundaries each T-* threat targets.
- [oc_security_clawhub_supply_chain](oc_security_clawhub_supply_chain.md) — ClawHub analysis (planned, this series); relevance: deep-dive on the T-PERSIST/T-EVADE supply-chain chain.
- [oc_security_formal_verification](oc_security_formal_verification.md) — TLA+/TLC models (planned, this series); relevance: machine-checks mitigations for several catalogued threats (node-exec, pairing, ingress gating).
- [oc_security_contributing_threat_model](oc_security_contributing_threat_model.md) — contribution process (planned, this series); relevance: how new T-* threats enter this catalog.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec-approvals/ssrf/external-content code; relevance: implements the mitigations cited per threat.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — tool policy + agent loop; relevance: T-EXEC/T-DISC threats target the agent tool surface.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — auth/rate-limit; relevance: T-RECON/T-ACCESS/T-IMPACT-002 target the gateway.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel ingress; relevance: T-ACCESS-002 AllowFrom spoofing + T-RECON-002 channel probing.

**Snippets**
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — XML-wrap + sanitize external content; relevance: T-EXEC-002 indirect-injection mitigation (content wrapping).
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval allowlist/ask; relevance: T-EXEC-003/004 + T-IMPACT-001 control.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec+fs policy; relevance: T-IMPACT-001 unauthorized command execution boundary.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denylist; relevance: blocking for the high-risk tool-invocation threats.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool gating; relevance: T-EXEC-003 tool-argument-injection + T-DISC-001 tool enumeration.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — pairing/AllowFrom; relevance: T-ACCESS-001 pairing interception + T-ACCESS-002 AllowFrom spoofing.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — rate-limit policy; relevance: T-IMPACT-002 DoS recommendation (per-sender rate limits).
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling on calls; relevance: T-ACCESS-003 token theft + T-EXFIL-003 credential harvesting.
- [snippet_openclaw_sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — input provenance tagging; relevance: distinguishing trusted vs injected input (T-EXEC-001/002).
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — static skill analyzer; relevance: T-EVADE-001 moderation-bypass + T-PERSIST-001 malicious-skill control.
- [snippet_openclaw_agents_tool_loop_detectors_circuit](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_circuit.md) — tool-loop circuit breaker; relevance: T-IMPACT-002 resource-exhaustion guard.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: external-content surface for indirect injection (T-EXEC-002).

### oc_security_clawhub_supply_chain (9t · 11s · 11d)

**Terms**
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency/marketplace code risk; relevance: this note is the ClawHub supply-chain analysis.
- [MITRE ATT&CK / ATLAS](../../term_dictionary/term_mitre_attack.md) — adversary taxonomy; relevance: §5.2 attack chains map to AML.T0010 supply-chain techniques.
- [Threat Model](../../term_dictionary/term_threat_model.md) — boundary/asset enumeration; relevance: §5 risk matrix is the quantified threat-model slice for ClawHub.
- [Content Moderation](../../term_dictionary/term_content_moderation.md) — automated policy filtering of user content; relevance: §4.2 `moderation.ts` FLAG_RULES are content-moderation patterns.
- [Sanitization](../../term_dictionary/term_sanitization.md) — neutralizing untrusted input; relevance: §4.1 `sanitizePath()` path-traversal control.
- [Anomaly Detection](../../term_dictionary/term_anomaly_detection.md) — flagging abnormal patterns; relevance: planned VirusTotal Code Insight behavioral analysis vs static regex.
- [Threat Intelligence](../../term_dictionary/term_threat_intelligence.md) — known-bad indicators; relevance: §4.2 known-bad identifier rules + VirusTotal scanning.
- [Attack Simulation](../../term_dictionary/term_attack_simulation.md) — modeling end-to-end attacks; relevance: §5.2 critical-path attack chains (publish→evade→harvest).
- [Adversarial ML](../../term_dictionary/term_adversarial_ml.md) — adversary-aware ML evasion; relevance: T-EVADE-001 homoglyph/encoding evasion of pattern moderation.

**Docs**
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin/extension security guidance; relevance: direct peer of skill-marketplace (plugin) supply-chain controls.
- [cc_create_a_skill](../claude_code/cc_create_a_skill.md) — skill authoring/format; relevance: peer of the SKILL.md-required publishing control.
- [cc_large_codebase_skills_and_plugins](../claude_code/cc_large_codebase_skills_and_plugins.md) — skills+plugins at scale; relevance: peer marketplace distribution surface.
- [hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md) — skill publishing flow; relevance: sibling-ecosystem publish pipeline + validation.
- [hermes_security_skill_memory_settings](../hermes_agent/hermes_security_skill_memory_settings.md) — skill/memory security settings; relevance: peer skill-trust controls.
- [band_environment_variables](../band/band_environment_variables.md) — env/secret surface for extensions; relevance: T-EXFIL-003 skill credential-harvest surface.
- [oc_security_threat_model_architecture](oc_security_threat_model_architecture.md) — Trust Boundary 5 (planned, this series); relevance: the boundary this note analyzes in depth.
- [oc_security_threat_catalog_atlas](oc_security_threat_catalog_atlas.md) — T-PERSIST/T-EVADE/T-EXFIL threats (planned, this series); relevance: the catalogued threats this chain composes.
- [oc_security_formal_verification](oc_security_formal_verification.md) — TLA+/TLC models (planned, this series); relevance: machine-checks adjacent gating; cross-series safety context.
- [oc_security_contributing_threat_model](oc_security_contributing_threat_model.md) — contribution process (planned, this series); relevance: how supply-chain threats/mitigations are submitted.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — `moderation.ts` / skill-scanner / opengrep code; relevance: implements the §4 controls.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill loading/manifest; relevance: the artifact ClawHub distributes and the runtime loads.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension/plugin system; relevance: the broader plugin supply-chain surface.

**Snippets**
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — regex static analyzer + symlink-escape audit; relevance: the §4.1/4.2 moderation control's code.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe execution; relevance: composing skill/workspace trust findings.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: §4.1 plugin/skill trust controls.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolver; relevance: resolving trust level for a published plugin/skill.
- [snippet_openclaw_opengrep_compile_collect](../../code_snippets/snippet_openclaw_opengrep_compile_collect.md) — OpenGrep rulepack collect; relevance: AST-ish behavioral detection beyond regex (the §4.3 improvement direction).
- [snippet_openclaw_opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — rulepack validate + GHSA metadata; relevance: advisory-id-tagged scanning rules for marketplace content.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — SKILL.md manifest; relevance: §4.1 "Required SKILL.md" publishing control.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability gating; relevance: badge/moderation-status gating of distribution.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — skill→tool descriptor contract; relevance: the tool surface a malicious skill could abuse.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content trust gating; relevance: skill-fetched content trust handling.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — remediation of findings; relevance: §4.3 audit-logging / community-reporting remediation flow.

### oc_security_contributing_threat_model (8t · 10s · 13d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — living asset/threat enumeration; relevance: this note is the threat-model contribution guide.
- [MITRE ATT&CK / ATLAS](../../term_dictionary/term_mitre_attack.md) — technique taxonomy; relevance: maintainers map submissions to ATLAS during review.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — injection threat class; relevance: the example threat classes ("prompt injection, tool misuse, agent exploitation") contributors report.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — marketplace/dependency risk; relevance: ClawHub is a named affected component contributors can target.
- [Threat Abuse](../../term_dictionary/term_threat_abuse.md) — abuse-threat enumeration; relevance: the four contribution paths add abuse threats/mitigations.
- [Attack Simulation](../../term_dictionary/term_attack_simulation.md) — attack-chain modeling; relevance: "Propose an attack chain" contribution path.
- [Adversarial Attack](../../term_dictionary/term_adversarial_attack.md) — crafted-input subversion; relevance: contributors describe adversarial attack vectors.
- [CVE-2024-27980](../../term_dictionary/term_cve_2024_27980.md) — a concrete published vulnerability/CVE; relevance: the guide says "links to related research, CVEs, or real-world examples" help a submission.

**Docs**
- [cc_security_guidance_layers_and_rules](../claude_code/cc_security_guidance_layers_and_rules.md) — guidance-rule contribution surface; relevance: peer process for evolving layered security guidance.
- [cc_hook_security_and_debugging](../claude_code/cc_hook_security_and_debugging.md) — security hook debugging; relevance: peer security-finding triage surface.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command-approval policy; relevance: a mitigation class contributors might propose.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook route security; relevance: example affected-component (webhooks) for a contributed threat.
- [pi_security_model](../pi/pi_security_model.md) — sibling threat model; relevance: cross-ecosystem precedent for community threat contribution.
- [oc_security_threat_model_architecture](oc_security_threat_model_architecture.md) — the model being contributed to (planned, this series); relevance: contributions land in its boundaries/scope.
- [oc_security_threat_catalog_atlas](oc_security_threat_catalog_atlas.md) — the T-* catalog (planned, this series); relevance: where new threat IDs get assigned.
- [oc_security_clawhub_supply_chain](oc_security_clawhub_supply_chain.md) — supply-chain section (planned, this series); relevance: a contribution target area.
- [oc_security_formal_verification](oc_security_formal_verification.md) — formal models (planned, this series); relevance: contributors can add bounded models / claims.
- [oc_security_incident_response](oc_security_incident_response.md) — incident runbook (planned, this series); relevance: the contribution guide explicitly separates threat-model PRs from live-vulnerability incident reports routed to this runbook.
- [oc_security_network_proxy_hardening](oc_security_network_proxy_hardening.md) — proxy denylist/hardening (planned, this series); relevance: example affected-component (egress proxy policy) a contributed mitigation can target.
- [cc_security_guidance_plugin](../claude_code/cc_security_guidance_plugin.md) — plugin/extension security guidance; relevance: peer process for evolving plugin/skill (ClawHub) security guidance contributors submit against.
- [cc_hooks_guardrail_and_audit_recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail+audit hook recipes; relevance: a concrete mitigation class (guardrail/audit hooks) a contributor might propose for a reported threat.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security code reviewers verify against; relevance: where proposed mitigations land.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — root repo + issue tracker context; relevance: contributions open issues/PRs on the OpenClaw repos.

**Snippets**
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit finding composition; relevance: how a verified threat becomes a tracked finding.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM-channel audit finding; relevance: example contributed channel-access threat surface.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel-source audit; relevance: example affected-component analysis a contribution refines.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime trust matrix; relevance: exec threat axis contributors enrich.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill scanner; relevance: a moderation mitigation a contributor might extend.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — remediation flow; relevance: the merge/triage path for accepted mitigations.
- [snippet_openclaw_opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — rule validate + GHSA metadata; relevance: links contributed findings to advisory IDs.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denylist; relevance: an actionable mitigation category for submissions.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval; relevance: a frequently-proposed mitigation surface.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: tool-misuse mitigation contributors target.

### oc_security_formal_verification (9t · 11s · 11d)

**Terms**
- [Formal Verification](../../term_dictionary/term_formal_verification.md) — machine-checked proof of system properties; relevance: this note is the TLA+/TLC formal-verification suite.
- [Threat Model](../../term_dictionary/term_threat_model.md) — security properties to enforce; relevance: each model checks a threat-model claim (authz, isolation, gating).
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe operation property; relevance: v1++ pairing/ingress idempotency models (no duplicate rows / no double-processing).
- [Sandbox](../../term_dictionary/term_sandbox.md) — execution isolation; relevance: node-exec-pipeline model checks allowlist + approval before host exec.
- [MITRE ATT&CK / ATLAS](../../term_dictionary/term_mitre_attack.md) — threat technique taxonomy; relevance: models are attacker-driven against the catalogued threats.
- [WebSocket](../../term_dictionary/term_websocket.md) — gateway/ingress transport; relevance: gateway-exposure + ingress-gating claims concern WS exposure.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — egress safety; relevance: gateway-exposure / misconfiguration-safety claims are adjacent egress-safety properties.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: gateway-exposure claim: token/password blocks unauth attackers.
- [Cron](../../term_dictionary/term_cron.md) — scheduled execution; relevance: CI-run models / reproduction workflow scheduling (future hosted runs).

**Docs**
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security guarantee architecture; relevance: peer framing for "what properties are guaranteed vs assumed".
- [cc_sandbox_org_enforcement](../claude_code/cc_sandbox_org_enforcement.md) — org-enforced sandbox policy; relevance: peer of node-exec allowlist+approval enforcement claim.
- [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — managed/enforced config; relevance: peer of "correct configuration inputs" environmental assumption.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation + credentials; relevance: peer of routing/session-key isolation claim.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: peer of gateway-exposure model subject.
- [band_a2a_gateway](../band/band_a2a_gateway.md) — A2A gateway model; relevance: another gateway whose exposure properties matter.
- [oc_security_threat_model_architecture](oc_security_threat_model_architecture.md) — boundaries (planned, this series); relevance: the boundaries these models machine-check.
- [oc_security_threat_catalog_atlas](oc_security_threat_catalog_atlas.md) — T-* threats (planned, this series); relevance: models target the highest-risk catalogued threats.
- [oc_security_contributing_threat_model](oc_security_contributing_threat_model.md) — contribution process (planned, this series); relevance: how new bounded models/claims are contributed.
- [oc_security_network_proxy_routing](oc_security_network_proxy_routing.md) — egress routing (planned, this series); relevance: gateway-exposure / loopback assumptions overlap proxy routing.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway exposure/auth code; relevance: the implementation the gateway-exposure model abstracts.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session key/routing; relevance: routing/session-key isolation model's subject code.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — pairing/ingress; relevance: pairing-store + ingress-gating models' subject code.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec-approval/node-command code; relevance: node-exec pipeline + approvals-token model's subject.

**Snippets**
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — pairing TTL/cap + allowlist; relevance: the pairing-store TTL/MaxPending model's code.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: pairing-cap / node grace-period model subject.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval tokens; relevance: approvals-token (replay-prevention) model's code.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command allowlist; relevance: node-exec-pipeline allowlist+declared-commands claim.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding routing; relevance: ingress-gating / mention bypass model subject.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session key derivation; relevance: routing/session-key isolation claim primitive.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session id resolution + dmScope; relevance: routing dmScope-precedence + identityLinks model.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth modes; relevance: gateway-exposure (token/password-blocks-unauth) claim.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — listen/bind WS server; relevance: gateway-exposure (bind beyond loopback) claim subject.
- [snippet_openclaw_acp_translator_rate_limit](../../code_snippets/snippet_openclaw_acp_translator_rate_limit.md) — rate-limit under interleavings; relevance: concurrency/idempotency property family the v1++ models check.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — exec dedup; relevance: ingress idempotency / dedupe-fallback model's real-world analog.

### oc_security_incident_response (8t · 10s · 13d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — boundary/impact framing; relevance: triage classifies "affected component, version, trust boundary impact".
- [Threat Intelligence](../../term_dictionary/term_threat_intelligence.md) — vulnerability signal sources; relevance: §1 monitors GHSA, Dependabot, CodeQL, secret-scanning signals.
- [Anomaly Detection](../../term_dictionary/term_anomaly_detection.md) — automated abnormal-signal flagging; relevance: §1 automated detection signals.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency/release risk; relevance: §2 critical severity = package/release/repository compromise.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe remediation; relevance: §3 reproduce→patch→validate with regression coverage (re-runnable fix).
- [Attack Simulation](../../term_dictionary/term_attack_simulation.md) — reproduce-the-attack step; relevance: §3 "reproduce on supported releases and latest main".
- [Phishing](../../term_dictionary/term_phishing.md) — a reported incident class; relevance: example external-report category triaged via the runbook.
- [CVE-2024-27980](../../term_dictionary/term_cve_2024_27980.md) — a concrete CVE; relevance: §4 disclosure policy issues CVEs for critical/high incidents.

**Docs**
- [cc_security_guidance_layers_and_rules](../claude_code/cc_security_guidance_layers_and_rules.md) — security guidance baseline; relevance: peer of the SECURITY.md scope/triage rules.
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure deployment principles; relevance: peer of post-incident hardening + recovery follow-up.
- [cc_hook_security_and_debugging](../claude_code/cc_hook_security_and_debugging.md) — security debugging; relevance: peer of reproduce/validate-a-patch step.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — approval-gating control; relevance: a hardening control added in post-incident follow-up.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential exposure handling; relevance: §2 "exposure of OpenClaw-owned sensitive credentials" severity case.
- [oc_security_threat_catalog_atlas](oc_security_threat_catalog_atlas.md) — T-* threats (planned, this series); relevance: incidents instantiate catalogued threats.
- [oc_security_threat_model_architecture](oc_security_threat_model_architecture.md) — trust boundaries (planned, this series); relevance: triage scores trust-boundary impact.
- [oc_security_formal_verification](oc_security_formal_verification.md) — formal models (planned, this series); relevance: post-incident regression coverage can add a bounded model.
- [oc_security_contributing_threat_model](oc_security_contributing_threat_model.md) — contribution vs live-vuln boundary (planned, this series); relevance: distinguishes threat-model PRs from live-vuln incident reports.
- [oc_security_clawhub_supply_chain](oc_security_clawhub_supply_chain.md) — ClawHub supply-chain analysis (planned, this series); relevance: §2 "package/release/repository compromise" critical incidents are supply-chain incidents this note deep-dives.
- [oc_security_network_proxy_hardening](oc_security_network_proxy_hardening.md) — proxy egress hardening (planned, this series); relevance: an egress-policy hardening control added during §5 post-incident follow-up.
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — web-tool security limits; relevance: peer controls for web_fetch exfiltration / abuse incident classes the runbook triages.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook route security; relevance: example affected-component (webhook/ingress route) classified in §2 severity triage.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — patched security code; relevance: where reproduce/patch/validate lands.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — root repo (GHSA/SECURITY.md/release flow); relevance: where advisories, CVEs, and patched releases ship.

**Snippets**
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit finding composition; relevance: triage assembles affected-component findings.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — remediation flow; relevance: §3 response patch + §5 follow-up tasks.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe execution; relevance: verify-remediation-in-CI (§5.1) probe.
- [snippet_openclaw_opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — rule validate + GHSA metadata; relevance: GHSA/CodeQL advisory-id linkage in §1 signals + §4 disclosure.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — scheduled service notifications; relevance: automated-signal / alerting plumbing for detection.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret handling; relevance: §2 credential-exposure incident class containment.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denylist; relevance: hardening control added during follow-up.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime trust matrix; relevance: assess trust-boundary-bypass severity (§2).
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval; relevance: an exec-path hardening fix surface.
- [snippet_openclaw_agents_tool_loop_detectors_circuit](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_circuit.md) — loop/DoS circuit breaker; relevance: narrowly-scoped DoS finding (§2 low severity) remediation.

### oc_security_network_proxy_routing (9t · 10s · 11d)

**Terms**
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy fronting traffic; relevance: contrasts inbound trusted-proxy auth (cross-linked) with this note's outbound forward proxy.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — interpose-a-mediator design; relevance: the forward-proxy interposition for all runtime egress.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — SSRF defense; relevance: the proxy is "stronger SSRF protection" + DNS-rebinding defense.
- [DNS](../../term_dictionary/term_dns.md) — name resolution; relevance: connect-time post-DNS checks + DNS-rebinding gap reduction.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: `http://` vs `https://` proxy endpoint TLS + destination CONNECT TLS.
- [WebSocket](../../term_dictionary/term_websocket.md) — WS egress; relevance: proxy routes "normal HTTP and WebSocket egress".
- [API Gateway](../../term_dictionary/term_api_gateway.md) — central traffic control point; relevance: the proxy is the single egress control point analog.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — outbound throttling; relevance: a listed operator control ("rate limits, outbound allowlists").
- [Authentication](../../term_dictionary/term_authentication.md) — proxy/endpoint auth; relevance: proxy-endpoint TLS verification + credential redaction in output.

**Docs**
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy + gateway config; relevance: closest peer (HTTP(S) proxy config for a coding agent).
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — TLS + network access; relevance: peer of proxy-endpoint TLS + no_proxy/access handling.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — cloud egress access; relevance: peer of central-egress-policy use case.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — gateway egress for LLM calls; relevance: peer of routing client traffic through a managed endpoint.
- [hermes_subscription_proxy](../hermes_agent/hermes_subscription_proxy.md) — provider subscription proxy; relevance: sibling-ecosystem proxy-routing config.
- [hermes_messaging_matrix_proxy_mode](../hermes_agent/hermes_messaging_matrix_proxy_mode.md) — channel proxy mode; relevance: per-transport proxy wiring analog (Telegram custom transport caveat here).
- [oc_security_network_proxy_hardening](oc_security_network_proxy_hardening.md) — proxy requirements/denylist (planned, this series); relevance: the hardening half of this split.
- [oc_security_threat_model_architecture](oc_security_threat_model_architecture.md) — F4 external data-flow (planned, this series); relevance: the boundary this proxy defends.
- [oc_security_threat_catalog_atlas](oc_security_threat_catalog_atlas.md) — T-EXFIL-001 web_fetch SSRF (planned, this series); relevance: the exfiltration threat egress control mitigates.
- [oc_security_formal_verification](oc_security_formal_verification.md) — gateway-exposure/loopback models (planned, this series); relevance: loopbackMode assumptions overlap the gateway-exposure claim.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway client connect + loopback bypass; relevance: control-plane loopback exception the proxy honors.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — `src/infra/net/*` proxy/ssrf wiring; relevance: where Proxyline routing + ssrf parity live.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — Telegram/transport proxy wiring; relevance: plugin-owned custom transports needing explicit proxy env.

**Snippets**
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — managed-proxy + loopback connect flow; relevance: the exact `start()`/loopback-bypass behavior this note documents.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS identity; relevance: proxy-endpoint TLS / `proxy.tls.caFile` trust path.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: proxy/destination TLS verification posture.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — HTTP loopback handling; relevance: loopback control-plane direct-path exception.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection setup; relevance: WebSocket egress routed through the proxy.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listen; relevance: the control-plane loopback WS the `gateway-only` mode bypasses.
- [snippet_openclaw_channels_telegram_transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram undici transport; relevance: the named plugin custom transport honoring `OPENCLAW_PROXY_URL`.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env handling; relevance: `OPENCLAW_PROXY_URL` env-fallback + no_proxy clearing.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama embedding host; relevance: the host-local-loopback embedding bypass exception in loopbackMode.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential redaction; relevance: proxy-URL credentials redacted in text/JSON output.

### oc_security_network_proxy_hardening (9t · 10s · 11d)

**Terms**
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — SSRF blocking via blocked ranges; relevance: the denylist + `ssrf.ts` parity hooks ARE the SSRF guard policy.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy mediation; relevance: contrast with the forward-proxy policy boundary being hardened.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — mediator interposition; relevance: the proxy IS the security boundary ("OpenClaw cannot verify").
- [DNS](../../term_dictionary/term_dns.md) — resolution; relevance: "resolve destinations itself and block destination IPs after DNS resolution".
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: HTTPS CONNECT-tunnel policy + private-CA `proxy.tls.caFile` vs `NODE_EXTRA_CA_CERTS`.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — keep policy under review; relevance: "keep proxy policy under version control and review changes like security-sensitive config".
- [API Gateway](../../term_dictionary/term_api_gateway.md) — central enforcement; relevance: fail-closed central egress enforcement at connect time.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — outbound throttling; relevance: a listed proxy egress control.
- [Encryption](../../term_dictionary/term_encryption.md) — at-transport secret protection; relevance: "do not log authorization headers, cookies, or other secrets" + TLS CONNECT for HTTPS destinations.

**Docs**
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — TLS + access policy; relevance: peer of CA-trust + CONNECT-tunnel hardening.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — cloud egress denylists; relevance: peer of the cloud-metadata (169.254.169.254) blocking guidance.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — network isolation limits; relevance: peer of "not an OS-level network sandbox" limits framing.
- [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — sandbox network modes; relevance: peer of fail-closed-vs-bypass egress modes (loopbackMode block).
- [hermes_subscription_proxy](../hermes_agent/hermes_subscription_proxy.md) — proxy config; relevance: sibling-ecosystem proxy hardening config.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — route/egress security; relevance: peer of validation + denied-destination checks.
- [oc_security_network_proxy_routing](oc_security_network_proxy_routing.md) — routing/config half (planned, this series); relevance: the routing half this hardening completes.
- [oc_security_threat_model_architecture](oc_security_threat_model_architecture.md) — Trust Boundary 3/4 SSRF (planned, this series); relevance: the boundary this denylist enforces.
- [oc_security_threat_catalog_atlas](oc_security_threat_catalog_atlas.md) — T-EXFIL-001 web_fetch SSRF (planned, this series); relevance: the threat the denylist + validation mitigate.
- [oc_security_formal_verification](oc_security_formal_verification.md) — misconfiguration-safety models (planned, this series); relevance: fail-closed-on-misconfig claim overlaps "enabled but no valid URL fails startup".

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — `src/infra/net/ssrf.ts` + `packages/net-policy/src/ip.ts`; relevance: the named parity-hook source for the denylist.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — `openclaw proxy validate` CLI + gateway egress; relevance: where validation + loopbackMode are wired.

**Snippets**
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect-time proxy + loopback; relevance: connect-time policy enforcement the requirements describe.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec+fs deny policy; relevance: parallel deny-policy structure (blocked-by-default boundary).
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool denylist; relevance: peer denylist-as-policy pattern.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS identity; relevance: private-CA proxy-endpoint trust (`proxy.tls.caFile`).
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: proxy-endpoint cert verification vs `NODE_EXTRA_CA_CERTS`.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP path; relevance: the loopback canary + `block` mode behavior.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env; relevance: container `OPENCLAW_PROXY_URL` forwarding + loopback-URL rejection.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — listen/bind; relevance: "bind only to loopback or private trusted interface" requirement.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret redaction; relevance: "do not log authorization headers/cookies/secrets" + redacted validate output.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local embedding host; relevance: the narrow guarded host-local Ollama bypass in the Limits table.

## Undigested Terms Plan

Per master: OpenClaw security vocabulary is the *subject of these doc pages*, so it is digested as `oc_*` documentation concept/argument notes here — NOT promoted to `term_dictionary`. The only `term_dictionary` interaction is **linking existing** terms (verified pool above). Expected **0 new term_dictionary captures**.

| Term (appearing in source) | Disposition |
|---|---|
| MITRE ATLAS / ATT&CK, AML.T0xxx techniques | Link existing `term_mitre_attack`; ATLAS specifics documented inline in notes 1/2/4 as doc prose. |
| Prompt injection (direct / indirect), jailbreak, adversarial data | Link existing `term_prompt_injection`, `term_jailbreak`, `term_adversarial_attack` (note 2). |
| SSRF / server-side request forgery, DNS rebinding, DNS pinning | Link existing `term_ssrf_guard` + `term_dns`; SSRF/rebinding mechanics documented inline in notes 1/7/8 (no `term_ssrf`/`term_dns_rebinding` notes exist; do not create — covered by the doc notes + `term_ssrf_guard`). |
| Trust boundary, session isolation, session key | Documented inline as the note-1 architecture model; link `term_sandbox` for the execution boundary (no `term_trust_boundary`/`term_session_isolation` notes — do not create). |
| ClawHub, skill marketplace, supply-chain compromise, moderation FLAG_RULES, VirusTotal | ClawHub digested by the cw01–cw03 sub-plans; here link existing `term_supply_chain` + cross-link cw notes (planned). No `term_clawhub`/`term_virustotal` capture (OpenClaw product vocab → `oc_*`/`cw_*` doc notes). |
| Exec approvals, command allowlist, tool gating, tool policy | Documented inline (notes 2/5); link `repo_openclaw_security` + `snippet_openclaw_gateway_exec_approval_manager` (no `term_exec_approval`/`term_tool_gating` notes — do not create). |
| Forward proxy, egress filtering, defense-in-depth, Proxyline, loopbackMode, CA trust | Documented inline as the note-7/8 procedure; link existing `term_reverse_proxy`, `term_proxy_pattern`, `term_tls` (no `term_forward_proxy`/`term_egress_filtering`/`term_defense_in_depth` notes — do not create; product/feature vocab → `oc_*`). |
| Formal verification, TLA+, TLC, bounded model checking | Link existing `term_formal_verification`; TLA+/TLC tooling documented inline in note 5 (no `term_tla_plus` note — do not create; the existing `term_formal_verification` covers the concept). |
| Incident response, coordinated disclosure, CVE, GHSA, severity levels | Documented inline as the note-6 runbook; link existing `term_threat_model` + `term_threat_intelligence` (no `term_incident_response`/`term_cve`/`term_coordinated_disclosure` notes — do not create; runbook is the doc note itself). |
| Idempotency, trace correlation, pairing TTL/caps, ingress gating, dmScope | `term_idempotency` exists — link it (note 5); the rest are OpenClaw runtime mechanics documented inline / cross-linked to gateway/channel sibling notes. |

**New-term candidates:** None. No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note — every concept either (a) maps to an existing term, (b) is an OpenClaw product/feature subject digested as an `oc_*`/`cw_*` doc note, or (c) is documented inline. If augment's Step 2d re-scan surfaces one, it would be captured via `/tessellum-capture-term-note` + added to the relevant `acronym_glossary_*.md` (best-fit for the security/AI-threat space: `acronym_glossary_genai_dev.md` or `acronym_glossary_abuse.md`); none expected.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — this sub-plan authors zero `term_dictionary` notes (inherited from master; OpenClaw vocab → `oc_*` doc notes, existing terms linked not redefined). If augment proposes a new term, the master's multi-source-research + glossary-update requirement applies.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit.

| Gate | Check | How |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` per note (YAML field order, `## Overview`/`## Related Notes` present, footer, no forbidden fields). |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/security/<page>.md` — every claim/threat-ID/denylist-range/make-target/config-key traceable to source; no invented mitigations or threat counts. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code fences per note; one BB/note; every source H2/H3 mapped (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected `term_dictionary` terms + sibling `oc_*` + `repo_openclaw*` + other vault, each an indexed `[text](path.md)` link with a relevance statement. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` → 0 broken links after incremental reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | Every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (anti-island), satisfied via `entry_openclaw_docs.md` rows + the inlinks in the Inlinks section; verify `in_degree ≥ 1` in `notes` table. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_security_threat_model_architecture oc_security_threat_catalog_atlas oc_security_clawhub_supply_chain oc_security_contributing_threat_model oc_security_formal_verification oc_security_incident_response oc_security_network_proxy_routing oc_security_network_proxy_hardening"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density (body words excl. frontmatter; fence pairs)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} fences)"
  # sibling cross-ref presence (informational)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING oc_ LINK in $n"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G6 broken links after incremental reindex
bash scripts/update_notes_database.sh
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code fences | Within caps (≤2500w / ≤6 fences / ≤400L / 1 BB)? |
|---|---|---|---:|---:|---|
| 1 | oc_security_threat_model_architecture | model | 600 | 2 (trust-boundary ASCII + data-flow) | Yes |
| 2 | oc_security_threat_catalog_atlas | argument | 750 | 2 (moderation regex pull / attack-chain) | Yes |
| 3 | oc_security_clawhub_supply_chain | argument | 700 | 2 (moderation FLAG_RULES + attack chains) | Yes |
| 4 | oc_security_contributing_threat_model | procedure | 550 | 0 | Yes |
| 5 | oc_security_formal_verification | argument | 650 | 1 (TLC clone/make) | Yes |
| 6 | oc_security_incident_response | procedure | 450 | 0 | Yes |
| 7 | oc_security_network_proxy_routing | procedure | 650 | ≤6 (routing text + proxy yaml + env bash + loopbackMode yaml) | Yes |
| 8 | oc_security_network_proxy_hardening | procedure | 650 | ≤6 (denylist context + validate bash + JSON + curl + CA yaml) | Yes |

No note approaches the 2,500w cap. The two over-cap / code-heavy source pages (THREAT-MODEL-ATLAS 3,660w/5-fence/mixed-BB, network-proxy 2,537w/13-fence) are split so every note stays ≤750w and ≤6 fences (the 13 network-proxy fences distribute ~6/7 across notes 7/8; only load-bearing config/denylist/validation snippets reproduced verbatim).

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` (planned, master pre-step) → all 8 notes (primary anti-island guarantee).
- `repo_openclaw_security.md` → notes 1, 2, 3, 5, 6, 8 (the code-side counterpart links the security doc set).
- `repo_openclaw_gateway.md` → notes 1, 5, 7, 8 (gateway auth / exposure / proxy routing).
- `repo_openclaw_skills.md` + `repo_openclaw_extensions.md` → note 3 (ClawHub skill supply chain).
- `repo_openclaw_sessions.md` → notes 1, 5 (session-key isolation).
- `repo_openclaw_channels.md` → notes 1, 5 (pairing / ingress gating).
- `term_mitre_attack.md` → notes 1, 2, 4; `term_prompt_injection.md` → note 2; `term_ssrf_guard.md` → notes 1, 2, 7, 8; `term_supply_chain.md` → notes 2, 3; `term_formal_verification.md` → note 5; `term_reverse_proxy.md` / `term_proxy_pattern.md` → notes 7, 8.

## Pacing Rules (inherited from master)

One execution phase, 8 notes (well under the ~30-agent fan-out cap). Re-read each source page before authoring; reproduce config/denylist/validation snippets verbatim. One BB per note; ≤6 fences. `git pull --rebase --autostash origin main` before commit; commit+push the wave together (no Claude co-author trailer). Incremental reindex; verify `note_links` populated + 0 broken links + in-degree ≥1 before commit. All 8 gates PASS before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment: per-note mapping locked at ≥8t/≥10s/≥10d)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 checkpoints PASS)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Per-note locked counts (Terms · Snippets · Docs · Repos — all floors met):**

| Note | Terms | Snippets | Docs | Repos | Floors (≥8t/≥10s/≥10d)? |
|---|---:|---:|---:|---:|---|
| oc_security_threat_model_architecture | 10 | 11 | 11 | 5 | MET |
| oc_security_threat_catalog_atlas | 10 | 12 | 11 | 4 | MET |
| oc_security_clawhub_supply_chain | 9 | 11 | 11 | 3 | MET |
| oc_security_contributing_threat_model | 8 | 10 | 10 | 2 | MET |
| oc_security_formal_verification | 9 | 11 | 11 | 4 | MET |
| oc_security_incident_response | 8 | 10 | 10 | 2 | MET |
| oc_security_network_proxy_routing | 9 | 10 | 11 | 3 | MET |
| oc_security_network_proxy_hardening | 9 | 10 | 11 | 2 | MET |


**Ghost verification (G5):** all 269 cited `.md` link targets in the locked mapping resolved deterministically — every EXISTING note_id present in the DB (terms, repos, snippets, cc/hermes/pi/band docs); the only non-resolving targets are the intentional planned `oc_*` siblings (8 of them) and the planned `entry_openclaw_docs.md`. 0 true ghosts. The PLAN-stage MISSING stems (`term_ssrf`, `term_trust_boundary`, `term_session_isolation`, `term_dns_rebinding`, `term_incident_response`, `term_defense_in_depth`, `term_forward_proxy`, `term_clawhub`, `term_virustotal`, `term_exec_approval`, …) were re-confirmed absent and are NOT cited; concepts mapped to nearest verified term (SSRF→`term_ssrf_guard`; session isolation→`term_sandbox`+`snippet_..._session_key_utils`; supply-chain attack→`term_supply_chain`) or documented inline.

**New-term candidates:** **None.** Per master decision (mirrors `claude_code`/`pi` precedent), OpenClaw security vocabulary is the *subject* of these doc pages and is digested as `oc_*` documentation concept/argument notes — NOT promoted to `term_dictionary`. The Step-2d re-read of all 5 pages surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note. Every concept either (a) maps to an existing verified term, (b) is OpenClaw product/feature vocab → `oc_*`/`cw_*` doc note, or (c) is documented inline. Expected **0 new `term_dictionary` captures** stands. (If a future re-scan surfaces one, best-fit glossary for this AI-threat/security space: `acronym_glossary_genai_dev.md` or `acronym_glossary_abuse.md`, captured via `/tessellum-capture-term-note`.)

**Collision/dedup audit (all planned notes, term_dictionary AND documentation/):** no planned `oc_security_*` note duplicates an existing term or doc note — they are OpenClaw-product-specific documentation (threat model, ClawHub supply chain, formal-verification suite, incident runbook, network-proxy feature) with no substantive existing vault counterpart on the *docs* side (code-side `repo_openclaw_security` + `snippet_openclaw_security_*` are LINKED, not recreated). 0 removals/renames required.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only verification of the augmented plan against the 9 mandatory checkpoints.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance-selected, per-link relevance) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED …)` present; all 8 notes ≥8 terms / ≥10 snippets / ≥10 docs (counts table above); every link carries a `— what; relevance: why` statement. Bare-link check: none. |
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link fix, G7/G8 discoverability/in-degree≥1. Single execution phase (8 notes). |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)`: contributes 8 rows to `entry_openclaw_docs.md` (CREATE'd master W1 pre-step); parent-hub wiring (W2/W3) is master-level. Size rule: master-level >30-note series ⇒ dedicated entry point already required. |
| CP4 | Size | **PASS** | 8 planned notes (≤30); single phase, well under the ~30-agent fan-out cap. |
| CP5 | Format derived (not invented) | **PASS** | Format Definition inherited verbatim from master, which derived it from existing `claude_code/` `cc_*` + `pi/` `pi_*` doc corpora (`## Overview` opener, `## Related Notes` reference section, bold `**Source**/**Last Updated**/**Status**` footer, fixed YAML field order, forbidden-field list). Matches existing target-type notes. |
| CP6 | Density / BB atomicity | **PASS** | `## Density Re-Assessment`: every note ≤750w / ≤6 fences / 1 BB. Two over-cap source pages split (THREAT-MODEL-ATLAS 3,660w→notes 1/2/3 by BB; network-proxy 2,537w/13-fence→notes 7/8). No borderline note unaddressed. |
| CP7 | Sources measured (not guessed) | **PASS** | Source table word counts re-verified against `inbox/openclaw_docs/security/*.md` at this augment pass: CONTRIBUTING 690w, THREAT-MODEL-ATLAS 3,660w (5 fences, 9 H2/26 H3), formal-verification 783w, incident-response 341w, network-proxy 2,537w (13 fences). Measured, consistent with plan; no >1.5× under-estimate. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new term captures, dispositions per term row = link-existing/inline/cross-series); `## Term-Note Authoring Requirements` present (N/A — 0 new terms — with the master multi-source+glossary fallback if augment proposes one). |
| CP8f | Slug specificity / collision | **PASS** | All-notes dedup audit (term_dictionary AND documentation/) recorded in Augmentation Report: 0 doc notes duplicate an existing term/doc note; code-side `repo_openclaw_security`/`snippet_openclaw_security_*` LINKED not recreated. 0 renames/removals. No `term_*` slugs created (no specificity audit needed). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-`documentation/openclaw/` inbound link (`entry_openclaw_docs` → all 8; `repo_openclaw_*` + `term_*` reciprocals); G7/G8 in-degree≥1 is a gated check in the G1–G8 phase table + Pacing Rules verify step. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
