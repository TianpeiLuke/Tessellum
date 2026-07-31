---
title: Sub-Plan gw06 — OpenClaw Docs: Gateway Security (Threat Model, Audit, Hardening, Exposure, Secrets Contract, fs-safe, Shrinkwrap, Tailscale)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["gateway/secrets-plan-contract", "gateway/security", "gateway/security/audit-checks", "gateway/security/exposure-runbook", "gateway/security/secure-file-operations", "gateway/security/shrinkwrap", "gateway/tailscale"]
---

<!-- status: pending -> ready (xref-augment + review 9/9 PASS, 2026-06-21) -->


# Sub-Plan gw06: Gateway

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing
> (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, body H2 structure, density caps), dedup
> (3-way: term_dictionary AND documentation/ AND repo_openclaw*), 9-GATE validation, cross-references, and entry-point
> wiring are ALL inherited from the master. This file re-measures its 7 assigned pages and locks the planned notes,
> coverage map, split decisions, and Candidate Cross-References (per-note locked mapping is deferred to augment).

## Scope

The OpenClaw Gateway **security cluster** — the operational core for safely running a shell-capable AI gateway:

- **Threat model + trust boundaries** (`security.md`): the personal-assistant trust model, Gateway/node trust domain,
  trust-boundary matrix, "not vulnerabilities by design", command/access-control model, prompt injection.
- **Security audit** (`security.md` quick-check sections + `security/audit-checks.md`): `openclaw security audit`,
  the findings priority order, the structured `checkId` reference catalog (severity, fix key, auto-fix).
- **Hardening recipes** (`security.md`): hardened baselines, network/bind/firewall, Docker+UFW, mDNS/Bonjour,
  Gateway WebSocket auth + rotation, secrets-on-disk, workspace `.env` blocking, logs/redaction, sandboxing,
  browser-control + SSRF, per-agent access profiles, incident response.
- **Exposure runbook** (`security/exposure-runbook.md`): pre-flight/rollback checklist before exposing beyond loopback.
- **Secrets apply plan contract** (`secrets-plan-contract.md`): the strict `openclaw secrets apply` plan schema/validation.
- **Secure file operations** (`security/secure-file-operations.md`): `@openclaw/fs-safe`, optional Python helper.
- **npm shrinkwrap** (`security/shrinkwrap.md`): supply-chain / release-reproducibility lockfile boundary.
- **Tailscale** (`tailscale.md`): Serve/Funnel auto-config for the Gateway dashboard + WS.

**Priority: P1 (Phase A).** Security is the gating concern for every Gateway/CLI/channel doc; the rest of the corpus
links here. The code-side counterparts (`repo_openclaw_security`, `repo_openclaw_gateway`, the `snippet_openclaw_security_*`
snippets) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **15,211 measured words**. **Planned: 12 notes.** (Master estimate was 11; raised to
12 because `security.md` alone is 9,250 words and splits into 6 notes.)

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Security | gateway/security | 9,250 | 19 | 35 | 49 | mixed (argument threat-model + procedure hardening) — SPLIT into 6 |
| Security audit checks | gateway/security/audit-checks | 2,082 | 0 | 1 | 0 | model (checkId reference catalog) |
| Gateway exposure runbook | gateway/security/exposure-runbook | 1,168 | 4 | 10 | 0 | procedure |
| Tailscale | gateway/tailscale | 938 | 5 | 9 | 3 | procedure |
| Secrets apply plan contract | gateway/secrets-plan-contract | 654 | 4 | 10 | 0 | model (plan schema/contract) |
| npm shrinkwrap | gateway/security/shrinkwrap | 560 | 4 | 3 | 0 | concept (supply-chain) |
| Secure file operations | gateway/security/secure-file-operations | 559 | 2 | 4 | 0 | concept (fs-safe guardrail) |

Total: 15,211 words. Code counts = raw ```` ``` ```` fence count / 2 (raw fence counts: 38/0/8/10/8/8/4 respectively).
Note: `security.md`, `secure-file-operations.md`, and `secrets-plan-contract.md` contain `# ...` lines that are **bash
comments inside code fences** (e.g. `# /etc/ufw/after.rules`, `# Validate plan without writes`), NOT markdown H1 headers.

## Content Strategy

- **Prioritize**: the threat model + trust boundaries (the conceptual frame everything cites), the `security audit` + the
  `checkId` catalog (the operator's diagnostic), and the network/auth/sandbox hardening recipes (the highest-blast-radius
  config). The exposure runbook is the operator checklist that ties them together.
- **Split** `security.md` (9,250w, 35 H2 / 49 H3, spans argument + procedure BBs) into **6 BB-atomic notes** clustered by
  task: (1) threat model + trust boundaries [argument], (2) audit quick-check + findings priority [procedure], (3) network
  /bind/firewall/mDNS/WS-auth hardening [procedure], (4) tool/exec/sandbox/browser/per-agent access profiles [procedure],
  (5) prompt injection + untrusted-content defenses [argument], (6) secrets-on-disk + credential map + logs/redaction +
  incident response [procedure]. See Split Decisions.
- **Link-out (do not redefine)**: pairing details → `gateway/pairing` (gw04), channels → `channels/*`, sandboxing deep
  doc → `gateway/sandboxing` (gw05), secrets management → `gateway/secrets` (gw05), trusted-proxy auth → `gateway/trusted-proxy-auth`
  (gw07), operator scopes → `gateway/operator-scopes` (gw04), logging → `gateway/logging` (gw03), configuration →
  `gateway/configuration*` (gw02), authentication → `gateway/authentication` (gw01), SecretRef surface → `reference/secretref-credential-surface`
  (rf03), formal verification / network-proxy → `security/*` (se01), exec approvals → `tools/exec-approvals` (to03),
  elevated → `tools/elevated` (to03), browser tool → `tools/browser` (to01). All are sibling planned/other-sub-plan
  `oc_*` notes (cite "(planned)" where in this series; otherwise reference by slug, not duplicated).
- The 6 sub-notes of `security.md` are wired to each other and to the 4 standalone notes (audit-checks ↔ note 2;
  exposure-runbook ↔ notes 2/3/4; secure-file-operations ↔ note 6; shrinkwrap ↔ note 4 plugins; tailscale ↔ note 3).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_gateway_security_threat_model.md` | argument | security.md: Scope (personal-assistant model), Deployment/host trust, Shared/Company-shared agent, Gateway and node trust concept, Trust boundary matrix, Not vulnerabilities by design, The threat model, Core concept (access control before intelligence), Command authorization model, Control plane tools risk | 700 | OpenClaw's personal-assistant security model: one trusted operator boundary per gateway, the Gateway/node trust domain + trust-boundary matrix, "not vulnerabilities by design" triage, and access-control-before-intelligence with control-plane tool risk. |
| 2 | `oc_gateway_security_audit.md` | procedure | security.md: Quick check `openclaw security audit` (--deep/--fix/--json), What the audit checks (high level), Security audit checklist (priority order), Security audit glossary (checkId classes), Insecure or dangerous flags summary | 650 | Running `openclaw security audit` (deep/fix/json modes), what it inspects, the findings priority order, the checkId severity classes, and the insecure/dangerous-flags summary. Pointer to the full catalog (note 7). |
| 3 | `oc_gateway_security_network_hardening.md` | procedure | security.md: Network exposure (bind/port/firewall), Docker port publishing with UFW, mDNS/Bonjour discovery, Lock down the Gateway WebSocket (local auth + auth modes + rotation), Tailscale Serve identity headers, HSTS and origin notes, Reverse proxy configuration, Control UI over HTTP | 750 | Network/transport hardening: bind modes + firewall, Docker+UFW DOCKER-USER rules, mDNS/Bonjour minimal mode, Gateway WebSocket auth + rotation, Tailscale Serve identity-header rules, reverse-proxy `trustedProxies`, HSTS/origin, and Control-UI-over-HTTP. |
| 4 | `oc_gateway_security_tool_sandbox_hardening.md` | procedure | security.md: Hardened baseline in 60 seconds, Secure baseline (copy/paste), Sandboxing (recommended) + sub-agent delegation guardrail, Browser control risks + Browser SSRF policy, Per-agent access profiles (full/read-only/no-access examples), Read-only mode, Plugins, Dynamic skills, Node execution (system.run) | 750 | Tool/exec/sandbox blast-radius hardening: the hardened/secure baselines, tool sandboxing + sub-agent guardrail, browser control + strict SSRF policy, per-agent access profiles, read-only mode, plugin trust, dynamic skills, and node `system.run`. |
| 5 | `oc_gateway_security_prompt_injection.md` | argument | security.md: Prompt injection (what it is, why it matters), Prompt injection does not require public DMs, External content special-token sanitization, Self-hosted LLM backends, Unsafe external content bypass flags, Model strength, Reasoning/verbose output in groups, Context visibility model, External-content special-token sanitization | 700 | Prompt-injection threat + defenses: why system prompts are soft guidance, untrusted-content risk even with private DMs, external-content special-token sanitization, self-hosted-backend tokenizer risk, unsafe-bypass flags, model-strength guidance, contextVisibility, and verbose-output exposure. |
| 6 | `oc_gateway_security_data_protection.md` | procedure | security.md: Credential storage map, Secrets on disk, Workspace `.env` files, Logs and transcripts (redaction/retention), Local session logs live on disk, File permissions, Separate numbers, DM access model / DM session isolation / Secure DM mode / Allowlists, Shared inbox quick rule, Incident response, Secret scanning, Reporting security issues | 700 | On-disk data protection + incident response: the credential storage map, securing `~/.openclaw` secrets, workspace `.env` credential blocking, log/transcript redaction, DM access/isolation + allowlists, file permissions, and the contain/rotate/audit incident-response runbook. |
| 7 | `oc_gateway_security_audit_checks.md` | model | gateway/security/audit-checks.md: the full `checkId` reference catalog table (fs.* / gateway.* / hooks.* / browser.* / sandbox.* / tools.exec.* / skills.* / plugins.* / security.exposure.* / config.* / models.*), Related | 700 | The structured `checkId` reference catalog emitted by `openclaw security audit`: each finding's severity, why-it-matters, primary fix key/config path, and auto-fix support, grouped by surface (fs / gateway / hooks / browser / sandbox / exec / plugins / exposure / models). |
| 8 | `oc_gateway_security_exposure_runbook.md` | procedure | gateway/security/exposure-runbook.md: Choose the exposure pattern, Pre-flight inventory, Baseline checks, Minimum safe baseline, DM/group exposure, Reverse proxy checks, Tool and sandbox review, Post-change validation, Rollback plan, Review checklist | 600 | The pre-flight + rollback operator runbook for exposing the Gateway beyond loopback: choose the narrowest exposure pattern, inventory + baseline checks, the minimum-safe-baseline config, per-surface review (DM/proxy/tool), post-change validation, and the rollback checklist. |
| 9 | `oc_gateway_tailscale.md` | procedure | gateway/tailscale.md: Modes (serve/funnel/off), Auth (none/token/password/trusted-proxy + allowTailscale identity headers), Config examples (Serve, named Service, Tailnet IP bind, Funnel+password), CLI examples, Notes, Browser control, Tailscale prerequisites + limits, Learn more, Related | 600 | Integrated Tailscale Serve (tailnet) / Funnel (public) for the Gateway dashboard + WebSocket: modes, auth + identity-header behavior, Serve/Service/Tailnet-bind/Funnel config examples, CLI, prerequisites/limits, and remote-Gateway browser control. |
| 10 | `oc_gateway_secrets_plan_contract.md` | model | gateway/secrets-plan-contract.md: Plan file shape, Provider upserts and deletes, Supported target scope, Target type behavior, Path validation rules, Failure behavior, Exec provider consent behavior, Runtime and audit scope notes, Operator checks, Related docs | 600 | The strict contract for `openclaw secrets apply` plans: the `targets` plan-file schema, `providerUpserts`/`providerDeletes`, target-type/path validation rules, fail-before-mutate behavior, exec-provider `--allow-exec` consent, and operator dry-run/apply commands. |
| 11 | `oc_gateway_security_secure_file_operations.md` | concept | gateway/security/secure-file-operations.md: Default no Python helper, What stays protected without Python, What Python adds, Plugin and core guidance | 450 | OpenClaw's `@openclaw/fs-safe` library guardrail for trusted code handling untrusted path input: why the optional POSIX Python helper is off by default, the Node-only protections that always apply, what the Python helper adds (fd-relative mutation hardening), and plugin/core usage guidance. |
| 12 | `oc_gateway_security_shrinkwrap.md` | concept | gateway/security/shrinkwrap.md: The easy version (lockfile model table), Why OpenClaw uses it, Technical details (generate/check commands, validators, package inspection) | 450 | npm shrinkwrap as OpenClaw's supply-chain / release-reproducibility boundary: `npm-shrinkwrap.json` vs `pnpm-lock.yaml` vs `package-lock.json`, why published packages ship a reviewed transitive graph, and the maintainer generate/check + package-inspection commands. |

## Section Coverage Map

```
gateway/security.md (35 H2 / 49 H3 — SPLIT into notes 1-6)
├── Scope first: personal assistant security model ──────────────── → note 1 (threat_model)
├── Quick check: openclaw security audit ──────────────────────── → note 2 (audit)
│   ├── Published package dependency lock (H3) ─────────────────── → note 12 (shrinkwrap; pointer in note 2)
│   ├── Deployment and host trust (H3) ─────────────────────────── → note 1
│   ├── Secure file operations (H3) ────────────────────────────── → note 11 (secure_file_operations; pointer)
│   ├── Shared Slack workspace: real risk (H3) ─────────────────── → note 1
│   └── Company-shared agent: acceptable pattern (H3) ──────────── → note 1
├── Gateway and node trust concept ────────────────────────────── → note 1
├── Trust boundary matrix ─────────────────────────────────────── → note 1
├── Not vulnerabilities by design ─────────────────────────────── → note 1
├── Hardened baseline in 60 seconds ───────────────────────────── → note 4 (tool_sandbox)
├── Shared inbox quick rule ───────────────────────────────────── → note 6 (data_protection; DM rules)
├── Context visibility model ──────────────────────────────────── → note 5 (prompt_injection)
├── What the audit checks (high level) ────────────────────────── → note 2
├── Credential storage map ────────────────────────────────────── → note 6
├── Security audit checklist ──────────────────────────────────── → note 2
├── Security audit glossary ───────────────────────────────────── → note 2 (→ note 7 full catalog)
├── Control UI over HTTP ──────────────────────────────────────── → note 3 (network_hardening)
├── Insecure or dangerous flags summary ───────────────────────── → note 2
├── Reverse proxy configuration ───────────────────────────────── → note 3
├── HSTS and origin notes ─────────────────────────────────────── → note 3
├── Local session logs live on disk ───────────────────────────── → note 6
├── Node execution (system.run) ───────────────────────────────── → note 4
├── Dynamic skills (watcher / remote nodes) ───────────────────── → note 4
├── The threat model ──────────────────────────────────────────── → note 1
├── Core concept: access control before intelligence ──────────── → note 1
├── Command authorization model ───────────────────────────────── → note 1
├── Control plane tools risk ──────────────────────────────────── → note 1
├── Plugins ───────────────────────────────────────────────────── → note 4
├── DM access model: pairing, allowlist, open, disabled ────────── → note 6
├── DM session isolation (multi-user mode) + Secure DM mode (H3) ─ → note 6
├── Allowlists for DMs and groups ─────────────────────────────── → note 6
├── Prompt injection (what it is, why it matters) ─────────────── → note 5
│   └── Prompt injection does not require public DMs (H3) ──────── → note 5
│   └── Self-hosted LLM backends (H3) ─────────────────────────── → note 5
│   └── Model strength (security note) (H3) ───────────────────── → note 5
├── External content special-token sanitization ──────────────── → note 5
├── Unsafe external content bypass flags ──────────────────────── → note 5
├── Reasoning and verbose output in groups ───────────────────── → note 5
├── Configuration hardening examples (H2) with H3 children:
│   ├── File permissions ──────────────────────────────────────── → note 6
│   ├── Network exposure (bind, port, firewall) ───────────────── → note 3
│   ├── Docker port publishing with UFW ───────────────────────── → note 3
│   ├── mDNS/Bonjour discovery ────────────────────────────────── → note 3
│   ├── Lock down the Gateway WebSocket (local auth) ──────────── → note 3
│   ├── Tailscale Serve identity headers ──────────────────────── → note 3 (→ note 9 full Tailscale)
│   ├── Browser control via node host (recommended) ──────────── → note 4
│   ├── Secrets on disk ───────────────────────────────────────── → note 6
│   ├── Workspace .env files ──────────────────────────────────── → note 6
│   ├── Logs and transcripts (redaction and retention) ────────── → note 6
│   ├── DMs: pairing by default ───────────────────────────────── → note 6
│   ├── Groups: require mention everywhere ────────────────────── → note 6
│   ├── Separate numbers (WhatsApp, Signal, Telegram) ─────────── → note 6
│   ├── Read-only mode (via sandbox and tools) ────────────────── → note 4
│   └── Secure baseline (copy/paste) ──────────────────────────── → note 4
├── Sandboxing (recommended) + Sub-agent delegation guardrail (H3) → note 4
├── Browser control risks + Browser SSRF policy (H3) ──────────── → note 4
├── Per-agent access profiles (multi-agent) + 3 example H3s ────── → note 4
├── Incident response + Contain/Rotate/Audit/Collect (H3) ─────── → note 6
├── Secret scanning ───────────────────────────────────────────── → note 6
└── Reporting security issues ─────────────────────────────────── → note 6 (footer)
gateway/security/audit-checks.md
├── checkId reference catalog (1 H2 + giant table) ────────────── → note 7 (audit_checks)
└── Related ───────────────────────────────────────────────────── → note 7
gateway/security/exposure-runbook.md
├── Choose the exposure pattern ───────────────────────────────── → note 8 (exposure_runbook)
├── Pre-flight inventory / Baseline checks / Minimum safe baseline → note 8
├── DM and group exposure / Reverse proxy checks / Tool+sandbox ── → note 8
├── Post-change validation / Rollback plan / Review checklist ──── → note 8
gateway/tailscale.md
├── Modes / Auth ──────────────────────────────────────────────── → note 9 (tailscale)
├── Config examples (Serve / Service / Tailnet IP / Funnel) (H3) ─ → note 9
├── CLI examples / Notes / Browser control / Prerequisites ─────── → note 9
├── Learn more / Related ──────────────────────────────────────── → note 9
gateway/secrets-plan-contract.md
├── Plan file shape / Provider upserts and deletes ───────────── → note 10 (secrets_plan_contract)
├── Supported target scope / Target type behavior / Path rules ── → note 10
├── Failure behavior / Exec provider consent / Runtime+audit ──── → note 10
├── Operator checks / Related docs ────────────────────────────── → note 10
gateway/security/secure-file-operations.md
├── Default: no Python helper / What stays protected w/o Python ─ → note 11 (secure_file_operations)
├── What Python adds / Plugin and core guidance ──────────────── → note 11
gateway/security/shrinkwrap.md
├── The easy version / Why OpenClaw uses it ──────────────────── → note 12 (shrinkwrap)
└── Technical details ─────────────────────────────────────────── → note 12
```
No orphaned sections. Cross-doc pointers (pairing, sandboxing deep doc, secrets, trusted-proxy, operator-scopes,
logging, configuration, SecretRef surface, exec-approvals, elevated, browser tool) link out to their home sub-plan
notes; not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| gateway/security.md (9,250w, 35 H2 / 49 H3, mixed argument+procedure BB) | notes 1–6 | 3.7× the 2,500w cap and 19 code blocks (>6 cap) and spans two BBs (argument threat-model framing vs procedure hardening recipes). Split by task cluster: 1 threat-model/trust (argument), 2 audit (procedure), 3 network hardening (procedure), 4 tool/exec/sandbox/browser hardening (procedure), 5 prompt injection/untrusted content (argument), 6 on-disk data protection + incident response (procedure). Each ≤750w, ≤6 code blocks, single BB. |
| (others) | 1 note each | secrets-plan-contract (654w), exposure-runbook (1,168w), tailscale (938w), shrinkwrap (560w), secure-file-operations (559w) are each single-BB and ≤2,500w → one note apiece (notes 10, 8, 9, 12, 11). audit-checks (2,082w) is a single reference-catalog table → one model note (note 7), under cap. |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (15,211 words). New `oc_` notes: **12**. New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: procedure ×6 (notes 2, 3, 4, 6, 8, 9) · argument ×2 (notes 1, 5) · model ×2 (notes 7, 10) ·
  concept ×2 (notes 11, 12).
- Est. digest words ~7,650 (avg ~640/note). 38 source code fences distribute across notes; each note kept ≤6 (the
  largest source, security.md @ 19 fences, is split so its hardening config blocks spread across notes 3/4/6, ≤6 each;
  audit-checks @ 0 fences → note 7 is a prose+table note).
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** every note maps **≥8 relevance-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (plus relevant
  for the exact per-note lists; the executor copies them verbatim.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> notes in THIS series do not exist yet → marked `(planned, this series)` and counted toward the 10-doc floor, but each
> `../../term_dictionary/term_Y.md`; sibling oc → `oc_Y.md`; cc doc → `../claude_code/cc_Y.md`; hermes doc →
> `../hermes_agent/hermes_Y.md`; pi doc → `../pi/pi_Y.md`; repo → `../../../areas/code_repos/repo_Y.md`; snippet →
> `../../code_snippets/snippet_Y.md`; entry point → `../../../0_entry_points/entry_openclaw_docs.md`. The executor copies
> the link + description + relevance verbatim into each note's `## Related Notes` section.

### oc_gateway_security_threat_model (8t · 11s · 11d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — structured enumeration of attackers, assets, and trust boundaries; relevance: this page IS OpenClaw's personal-assistant threat model and the trust-boundary matrix.
- [Access Control](../../term_dictionary/term_access_control.md) — mechanisms gating who may do what; relevance: the page's "identity first / access control before intelligence" stance is the core principle.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted shell-capable AI gateway; relevance: subject system being secured.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — the scope of damage a compromise can cause; relevance: "design so manipulation has limited blast radius" is the model-last layer.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: the model recommends sandboxing as the strong boundary when prompts cannot be trusted.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — shell-capable AI agents that act on hosts; relevance: the agent class whose tool authority the trust domain bounds.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple cooperating agents under one gateway; relevance: "one trusted operator boundary, potentially many agents" frames the shared-tool-authority risk.

**Docs**
- [cc: Security Architecture](../claude_code/cc_security_architecture.md) — Claude Code's layered security/trust model; relevance: analogous coding-agent threat-model framing for an external doc viewpoint.
- [cc: Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — trust boundaries for chat-connected agents; relevance: parallels OpenClaw's "who can message the bot" trust boundary.
- [cc: Permission System and Rules](../claude_code/cc_permission_system_and_rules.md) — authorization-before-action rules; relevance: mirrors access-control-before-intelligence.
- [cc: What Claude Can Access](../claude_code/cc_what_claude_can_access.md) — enumerates the agent's reachable surfaces; relevance: parallels "your AI assistant can execute shell / read files / access network."
- [pi: Security Model](../pi/pi_security_model.md) — Pi coding-agent trust model; relevance: independent single-operator coding-agent security posture for orthogonality.
- [hermes: Security Isolation and Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — Hermes trust-boundary + credential isolation; relevance: closest sibling-tool threat model (Hermes is downstream of OpenClaw).
- [OpenClaw — Security Audit](oc_gateway_security_audit.md) (planned, this series) — the diagnostic that scores this model; relevance: the audit checks the boundaries this note defines.
- [OpenClaw — Tool/Sandbox Hardening](oc_gateway_security_tool_sandbox_hardening.md) (planned, this series) — where the model is enforced; relevance: model-last blast-radius controls live here.
- [OpenClaw — Prompt Injection](oc_gateway_security_prompt_injection.md) (planned, this series) — the manipulation surface the model assumes; relevance: "assume the model can be manipulated."
- [OpenClaw — Exposure Runbook](oc_gateway_security_exposure_runbook.md) (planned, this series) — operationalizes the model before exposure; relevance: pre-flight checklist for trust-boundary changes.
- [OpenClaw — Data Protection](oc_gateway_security_data_protection.md) (planned, this series) — host/disk trust boundary; relevance: "treat disk access as the trust boundary."

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — code-side audit/trust implementation; relevance: implements the audit + trust-boundary checks this model frames.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — control-plane/policy surface; relevance: the `gateway.auth` / tool-policy boundary the matrix describes.
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent trust scoping; relevance: where per-agent delegated tool authority is enforced.

**Snippets**
- [snippet: security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — assembles the audit's trust/exposure checks; relevance: encodes the boundaries this model enumerates.
- [snippet: gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — gateway-call authorization dispatch; relevance: "authenticated operator access is a trusted control-plane role."
- [snippet: gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — per-method gating of control-plane RPCs; relevance: enforces the control-plane-tool-risk boundary.
- [snippet: agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — per-agent scope resolution; relevance: realizes "scope next" in the identity/scope/model stack.
- [snippet: security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — denies high-risk tools for untrusted surfaces; relevance: the deny-by-default control-plane-tool list.
- [snippet: gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — coarse global node command policy; relevance: the node-trust execution boundary in the matrix.
- [snippet: sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — sessionKey derivation/handling; relevance: "sessionKey is a routing selector, not an auth token."
- [snippet: gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing/approval/token issuance; relevance: "after pairing, node actions are trusted operator actions."
- [snippet: agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool allow/deny resolution; relevance: the delegated-tool-authority surface the model bounds.
- [snippet: security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — audits exec-runtime drift; relevance: detects when the "intentional default" posture has drifted.
- [snippet: gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity + TLS handling; relevance: device-identity vs shared-token trust distinction.

### oc_gateway_security_audit (8t · 12s · 11d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — attacker/asset/boundary enumeration; relevance: the audit operationalizes the threat model into findings.
- [Access Control](../../term_dictionary/term_access_control.md) — who-can-do-what gating; relevance: "Inbound access" (DM/group/allowlist) is the first audit surface.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — damage scope; relevance: "Tool blast radius" is a core audit dimension.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: the audit flags sandbox-config-vs-mode drift.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller identity; relevance: audit checks Gateway bind/auth and weak/short tokens.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling abusive requests; relevance: `gateway.auth_no_rate_limit` is an audit finding.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — subject gateway; relevance: `openclaw security audit` is the subject CLI.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency/plugin provenance risk; relevance: the audit scans plugins and `--deep` runs code-safety checks.

**Docs**
- [cc: Security Guidance Layers and Rules](../claude_code/cc_security_guidance_layers_and_rules.md) — layered guardrail/rule guidance; relevance: analogous diagnostic-of-guardrails framing.
- [cc: Hooks Guardrail and Audit Recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail/audit recipes; relevance: parallel "audit your guardrails" workflow.
- [cc: Admin Enforcement Controls](../claude_code/cc_admin_enforcement_controls.md) — enforce/verify security config; relevance: analogous to the audit's config-drift checks.
- [cc: Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — distinguishes sandbox vs permission controls; relevance: the audit's exec/sandbox-policy-drift checks.
- [hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — command-approval guardrails; relevance: sibling tool's exec-approval posture the audit also inspects.
- [pi: Security Model](../pi/pi_security_model.md) — coding-agent security posture; relevance: independent checklist analog for orthogonality.
- [OpenClaw — Audit Checks (checkId catalog)](oc_gateway_security_audit_checks.md) (planned, this series) — the full catalog this summarizes; relevance: note 2 → note 7 pointer.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — the model the audit scores; relevance: findings map back to boundaries.
- [OpenClaw — Exposure Runbook](oc_gateway_security_exposure_runbook.md) (planned, this series) — runs the audit as a baseline check; relevance: `openclaw security audit --deep` is a runbook step.
- [OpenClaw — Network Hardening](oc_gateway_security_network_hardening.md) (planned, this series) — fixes network findings; relevance: bind/auth/proxy findings resolve here.
- [OpenClaw — Tool/Sandbox Hardening](oc_gateway_security_tool_sandbox_hardening.md) (planned, this series) — fixes exec/sandbox findings; relevance: exec/sandbox/plugin findings resolve here.

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — implements `security audit` / `--deep` / `--fix`; relevance: the audit's home module.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — bind/auth/exposure surface; relevance: the audit probes gateway config + live gateway.
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent tool/exec policy; relevance: the audit reads per-agent overrides.

**Snippets**
- [snippet: security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — assembles the full audit run; relevance: the top-level audit composition.
- [snippet: security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — audits exec/runtime drift; relevance: "Exec approval drift" + "Runtime expectation drift" checks.
- [snippet: security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — the `--deep` live gateway probe; relevance: "If you run --deep, OpenClaw attempts a best-effort live probe."
- [snippet: security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — audits DM exposure; relevance: "Inbound access" DM-policy checks.
- [snippet: security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — audits channel/group exposure; relevance: open-channel-with-exec exposure checks.
- [snippet: security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — applies `--fix` remediations; relevance: `security audit --fix` narrow auto-fix behavior.
- [snippet: security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem-drift policy; relevance: "Exec filesystem drift" audit dimension.
- [snippet: security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — emits plugin-trust findings; relevance: "Plugins (load without allowlist)" check.
- [snippet: security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — scans skill install material; relevance: `skills.code_safety` deep-scan findings.
- [snippet: gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution; relevance: "Network exposure (bind/auth, weak tokens)" check.
- [snippet: gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth rate-limit + install policy; relevance: `auth_no_rate_limit` + install-policy findings.
- [snippet: opengrep_compile_validate](../../code_snippets/snippet_openclaw_opengrep_compile_validate.md) — compiles/validates code-scan rules; relevance: backs `--deep` plugin/skill code-safety scanning.

### oc_gateway_security_network_hardening (9t · 12s · 11d)

**Terms**
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — intermediary that forwards client traffic; relevance: `gateway.trustedProxies` + X-Forwarded-For handling.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — single network entry point for APIs; relevance: the Gateway multiplexes WS+HTTP on one port.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional connection; relevance: "Lock down the Gateway WebSocket" auth section.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: HSTS, wss/`tlsFingerprint`, secure-context Control UI.
- [VPN](../../term_dictionary/term_vpn.md) — private network overlay; relevance: Tailscale Serve identity headers / prefer-Serve-over-LAN.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: Docker port-publishing + UFW DOCKER-USER rules.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying caller identity; relevance: token/password/trusted-proxy auth modes + rotation.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — throttling abusive requests; relevance: per-Origin browser-auth lockout buckets.
- [Encryption](../../term_dictionary/term_encryption.md) — protecting data in transit/at rest; relevance: HTTPS termination + HSTS hardening.

**Docs**
- [cc: Network, TLS, and Access](../claude_code/cc_network_tls_and_access.md) — network/TLS/access config; relevance: closest external analog for bind/TLS hardening.
- [cc: Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — reverse-proxy/gateway header handling; relevance: parallels `trustedProxies` / X-Forwarded-For.
- [cc: Cloud Network Access](../claude_code/cc_cloud_network_access.md) — network exposure controls; relevance: analogous bind/firewall surface guidance.
- [cc: DevContainer Hardening](../claude_code/cc_devcontainer_hardening.md) — firewall/network hardening for containers; relevance: parallels Docker+UFW firewall recipe.
- [hermes: Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway transport internals; relevance: sibling gateway bind/port architecture.
- [hermes: Dashboard Auth Remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: analogous Control-UI-over-remote auth hardening.
- [OpenClaw — Tailscale](oc_gateway_tailscale.md) (planned, this series) — full Tailscale Serve/Funnel doc; relevance: this note's Tailscale identity-header rules point to it.
- [OpenClaw — Audit](oc_gateway_security_audit.md) (planned, this series) — surfaces network findings; relevance: `gateway.bind_no_auth` etc. drive this note's fixes.
- [OpenClaw — Exposure Runbook](oc_gateway_security_exposure_runbook.md) (planned, this series) — exposure pre-flight; relevance: applies these hardening controls before exposure.
- [OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md) (planned, this series) — `gateway.*` checkId catalog; relevance: the network checkIds this note remediates.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — trust-boundary model; relevance: bind/proxy decisions follow the trust matrix.

**Repos**
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — bind/auth/proxy/WS server surface; relevance: implements bind modes, auth modes, trusted-proxy handling.
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — emits network exposure findings; relevance: the audit checks this note's controls.

**Snippets**
- [snippet: gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token/password/trusted-proxy/Tailscale auth modes; relevance: the auth-mode matrix this note documents.
- [snippet: gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth rate-limit policy; relevance: origin-scoped lockout behavior.
- [snippet: gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize/dispatch on the gateway call; relevance: fail-closed WS auth.
- [snippet: gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener on one port; relevance: "the Gateway multiplexes WS+HTTP on a single port."
- [snippet: gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect-through-proxy; relevance: reverse-proxy/X-Forwarded handling.
- [snippet: gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity + TLS pin; relevance: `gateway.remote.tlsFingerprint` / wss pinning.
- [snippet: kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS-fingerprint pinning in the client kit; relevance: pin remote TLS for wss.
- [snippet: gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: "Control UI over HTTP" secure-context / device-identity rules.
- [snippet: gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection lifecycle; relevance: WS auth/lockdown behavior.
- [snippet: gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback-only MCP HTTP surface; relevance: loopback-first bind hardening.
- [snippet: android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — mobile WS with stricter cleartext rules; relevance: "Mobile pairing routes are stricter" cleartext/TLS rules.
- [snippet: gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — global node command policy; relevance: node-over-WS access via the same endpoint.

### oc_gateway_security_tool_sandbox_hardening (9t · 12s · 11d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: tool sandboxing is the core control of this note.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — damage scope; relevance: per-agent profiles + read-only mode shrink blast radius.
- [Access Control](../../term_dictionary/term_access_control.md) — who-can-do-what gating; relevance: `tools.allow`/`deny`, `elevated.allowFrom` profiles.
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool/function invocation; relevance: tool/exec policy gates the agent's tool calls.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: default sandbox backend + dangerous bind/network checks.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency/plugin provenance; relevance: "treat plugin install like running untrusted code."
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: `openclaw plugins install <package>` install trust.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — shell-capable agents; relevance: node `system.run` is remote code execution.
- [Subagent](../../term_dictionary/term_subagent.md) — delegated child agent run; relevance: sub-agent delegation guardrail (`sessions_spawn`, `sandbox: "require"`).

**Docs**
- [cc: Sandbox Modes](../claude_code/cc_sandbox_modes.md) — sandbox mode selection; relevance: parallels `sandbox.mode` off/all/non-main.
- [cc: Sandbox Filesystem and Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — fs/network isolation; relevance: parallels workspaceAccess + bind-mount validation.
- [cc: Permission Modes Overview](../claude_code/cc_permission_modes_overview.md) — permission/approval modes; relevance: analogous to exec approvals + read-only profiles.
- [cc: Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool allow/deny rules; relevance: parallels per-agent tool allow/deny lists.
- [cc: Computer Use Safety](../claude_code/cc_computer_use_safety.md) — browser/computer-use safety; relevance: parallels browser-control risk + SSRF policy.
- [hermes: Subagent Delegation](../hermes_agent/hermes_subagent_delegation.md) — delegated sub-agent runs; relevance: sibling sub-agent delegation guardrail.
- [hermes: Code Execution](../hermes_agent/hermes_code_execution.md) — sandboxed code execution; relevance: analogous exec/sandbox tool blast-radius control.
- [OpenClaw — Shrinkwrap](oc_gateway_security_shrinkwrap.md) (planned, this series) — plugin supply-chain lockfile; relevance: backs "inspect unpacked plugin code" install trust.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — the model enforced here; relevance: this note is "scope next / model last" enforcement.
- [OpenClaw — Audit](oc_gateway_security_audit.md) (planned, this series) — surfaces tool/sandbox findings; relevance: `tools.exec.*` / `sandbox.*` findings resolve here.
- [OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md) (planned, this series) — `sandbox.*` / `tools.exec.*` catalog; relevance: the checkIds this note remediates.

**Repos**
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent sandbox/tool policy; relevance: where access profiles + tool deny lists resolve.
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — exec filesystem policy + audit; relevance: enforces exec/approval guardrails.
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin host/trust; relevance: "plugins run in-process; treat as trusted code."
- [repo: openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — dynamic skills runtime; relevance: "treat skill folders as trusted code."

**Snippets**
- [snippet: agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool allow/deny resolution; relevance: the per-agent access-profile mechanism.
- [snippet: security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem-drift policy; relevance: read-only-mode + `applyPatch.workspaceOnly` enforcement.
- [snippet: gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval manager; relevance: `security`/`ask`/allowlist approval binding.
- [snippet: gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing + token issuance; relevance: node `system.run` requires pairing.
- [snippet: gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — global node command allow/deny; relevance: coarse node command policy for `system.run`.
- [snippet: agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn policy; relevance: `sessions_spawn` + `sandbox: "require"` guardrail.
- [snippet: agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — caps on sub-agent spawns; relevance: bounds delegated runs.
- [snippet: security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — denies dangerous tools; relevance: the deny `gateway`/`cron`/`sessions_*` baseline.
- [snippet: security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — resolves plugin trust/allowlist; relevance: `plugins.allow` allowlist trust.
- [snippet: plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/load lifecycle; relevance: "restart after plugin changes" + install path.
- [snippet: skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — evaluates skill availability (watcher/node bin probing); relevance: dynamic-skills eligibility.
- [snippet: process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — orchestrates exec/process runs; relevance: the exec surface sandboxing constrains.

### oc_gateway_security_prompt_injection (8t · 11s · 11d)

**Terms**
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — adversarial input that hijacks model instructions; relevance: the subject of this note.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: "prompt injection is not solved; system prompts are soft guidance."
- [Claude](../../term_dictionary/term_claude.md) — instruction-hardened model family; relevance: "use the strongest latest-generation instruction-hardened model."
- [Social Engineering](../../term_dictionary/term_social_engineering.md) — manipulating people/agents into unsafe actions; relevance: "social engineer access to your data."
- [Phishing](../../term_dictionary/term_phishing.md) — deceptive content to extract data/actions; relevance: treat links/attachments/pasted instructions as hostile.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — damage scope; relevance: reader-agent containment + read-only tools reduce blast radius.
- [Access Control](../../term_dictionary/term_access_control.md) — trigger/context gating; relevance: `contextVisibility` + trigger authorization layers.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: injection's typical risk is triggering tool calls.

**Docs**
- [cc: Prompt Injection Defenses](../claude_code/cc_prompt_injection_defenses.md) — defenses against prompt injection; relevance: direct external analog of this note's subject.
- [cc: Security Guidance Layers and Rules](../claude_code/cc_security_guidance_layers_and_rules.md) — layered soft+hard guardrails; relevance: "hard enforcement comes from tool policy, not prompts."
- [cc: Hook Security and Debugging](../claude_code/cc_hook_security_and_debugging.md) — untrusted hook-payload handling; relevance: "hook payloads are untrusted content."
- [cc: What Claude Can Access](../claude_code/cc_what_claude_can_access.md) — agent's reachable data; relevance: injection's exfiltration target surface.
- [cc: Computer Use Safety](../claude_code/cc_computer_use_safety.md) — browser/computer-use injection risk; relevance: web fetch/browser content as injection vector.
- [hermes: Security Isolation and Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolating untrusted-content agents; relevance: sibling reader-agent containment pattern.
- [pi: Security Model](../pi/pi_security_model.md) — coding-agent trust model; relevance: independent prompt-injection posture for orthogonality.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — assumes the model can be manipulated; relevance: the model-last layer.
- [OpenClaw — Tool/Sandbox Hardening](oc_gateway_security_tool_sandbox_hardening.md) (planned, this series) — blast-radius controls; relevance: sandbox + tool deny limit injection impact.
- [OpenClaw — Data Protection](oc_gateway_security_data_protection.md) (planned, this series) — "keep secrets out of prompts"; relevance: injection exfiltration containment.
- [OpenClaw — Network Hardening](oc_gateway_security_network_hardening.md) (planned, this series) — OpenResponses URL allowlists; relevance: untrusted URL-input fetch controls.

**Repos**
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — system-prompt + context injection handling; relevance: external-content wrapping + special-token sanitization.
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — external-content sanitizer + bypass flags; relevance: special-token stripping + `allowUnsafeExternalContent`.
- [repo: openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — inbound content surface; relevance: untrusted inbound message content.

**Snippets**
- [snippet: agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — injects supplemental context into model input; relevance: the `contextVisibility` context-injection surface.
- [snippet: security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — wraps/sanitizes external untrusted content; relevance: `<<<EXTERNAL_UNTRUSTED_CONTENT>>>` boundary markers.
- [snippet: gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — sanitizes attachment/media text; relevance: media-understanding extracted text wrapped as untrusted.
- [snippet: agents_btw_streamSimple_sanitize](../../code_snippets/snippet_openclaw_agents_btw_streamSimple_sanitize.md) — strips leaked runtime scaffolding from replies; relevance: the outbound-response sanitizer counterpart.
- [snippet: gateway_chat_history_inject_handler](../../code_snippets/snippet_openclaw_gateway_chat_history_inject_handler.md) — injects chat/thread history into context; relevance: supplemental-context filtering by `contextVisibility`.
- [snippet: sessions_input_provenance](../../code_snippets/snippet_openclaw_sessions_input_provenance.md) — tracks input provenance/trust; relevance: distinguishing trusted vs external-untrusted input.
- [snippet: gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — handles inbound hook payloads; relevance: hook payloads are untrusted injection vectors.
- [snippet: gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hook config incl. `allowUnsafeExternalContent`; relevance: the unsafe-bypass flag.
- [snippet: agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool deny; relevance: keep web_fetch/web_search/browser off for tool-enabled agents.
- [snippet: gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media/transcript ingest pipeline; relevance: untrusted document text appended to media prompt.
- [snippet: security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny high-risk tools; relevance: limit `exec`/`browser` for untrusted-content agents.

### oc_gateway_security_data_protection (8t · 12s · 11d)

**Terms**
- [PII](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: secrets/private data on disk under `~/.openclaw`.
- [Data Minimization](../../term_dictionary/term_data_minimization.md) — keep/expose only needed data; relevance: log/transcript redaction + retention pruning.
- [Access Control](../../term_dictionary/term_access_control.md) — who-can-trigger/read gating; relevance: DM allowlists, session isolation, file permissions.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored credential token; relevance: `auth-profiles.json` tokens + legacy `oauth.json`.
- [Authentication](../../term_dictionary/term_authentication.md) — caller identity + credential rotation; relevance: incident-response credential rotation.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — damage scope; relevance: incident contain/rotate/audit limits damage.
- [Slack](../../term_dictionary/term_slack.md) — team chat platform; relevance: shared-inbox DM example + DM allowlist controls.
- [Encryption](../../term_dictionary/term_encryption.md) — protect data at rest; relevance: "use full-disk encryption on the gateway host."

**Docs**
- [cc: Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — chat-channel data controls; relevance: parallels DM allowlists + shared-inbox rules.
- [cc: Data Usage and Telemetry](../claude_code/cc_data_usage_and_telemetry.md) — data handling/retention; relevance: parallels log/transcript redaction + retention.
- [cc: Zero Data Retention](../claude_code/cc_zero_data_retention.md) — retention controls; relevance: "prune old transcripts/logs."
- [cc: SDK Credential and Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential + fs scoping; relevance: parallels secrets-on-disk + workspace `.env` blocking.
- [hermes: Security Isolation and Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — credential isolation on disk; relevance: sibling on-disk credential map.
- [hermes: Session Storage](../hermes_agent/hermes_session_storage.md) — session transcripts on disk; relevance: "local session logs live on disk."
- [OpenClaw — Secure File Operations](oc_gateway_security_secure_file_operations.md) (planned, this series) — fs-safe secret-file helpers; relevance: how secret/state files are written safely.
- [OpenClaw — Secrets Plan Contract](oc_gateway_secrets_plan_contract.md) (planned, this series) — credential write contract; relevance: how the credential map is mutated.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — "disk access is the trust boundary"; relevance: the host-trust premise.
- [OpenClaw — Prompt Injection](oc_gateway_security_prompt_injection.md) (planned, this series) — exfiltration risk; relevance: "keep secrets out of the agent's reachable filesystem."
- [OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md) (planned, this series) — `fs.*` / `logging.redact_off` catalog; relevance: the permissions/redaction checkIds.

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — credential/secret handling + secret scanning; relevance: secrets-on-disk + redaction enforcement.
- [repo: openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session transcripts on disk; relevance: `sessions/*.jsonl` storage + retention.
- [repo: openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — DM allowlists + pairing stores; relevance: `<channel>-allowFrom.json` credential state.
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — `auth-profiles.json` per-agent credentials; relevance: model auth profiles on disk.

**Snippets**
- [snippet: gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — resolves call credentials/secrets; relevance: the credential storage map plumbing.
- [snippet: channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing + allowlist store; relevance: DM access model + allowlist files.
- [snippet: agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth-profile credentials; relevance: stored model credentials.
- [snippet: agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: `keyRef`/`tokenRef` resolution + scrubbing.
- [snippet: sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript event records; relevance: transcripts that can contain private messages/output.
- [snippet: gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — reads session-store files; relevance: filesystem-access trust boundary on logs.
- [snippet: sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — DM session send policy; relevance: `dmScope` isolation between users.
- [snippet: sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — sessionKey/scope utilities; relevance: per-channel-peer DM isolation.
- [snippet: gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env/dotenv loading; relevance: workspace `.env` credential blocking.
- [snippet: security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — audits DM exposure; relevance: shared-inbox quick rule enforcement.
- [snippet: gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — applies config changes; relevance: incident-response config tightening (bind/dmPolicy).
- [snippet: security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — auto-fix tightens permissions/redaction; relevance: `--fix` restores redaction + perms.

### oc_gateway_security_audit_checks (8t · 12s · 11d)

**Terms**
- [Threat Model](../../term_dictionary/term_threat_model.md) — boundary enumeration; relevance: the catalog groups findings by trust surface.
- [Access Control](../../term_dictionary/term_access_control.md) — who-can-do-what; relevance: `security.exposure.*` + DM/group policy checks.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: the `sandbox.*` checkId family.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — forwarding intermediary; relevance: `gateway.trusted_proxy_*` checks.
- [Authentication](../../term_dictionary/term_authentication.md) — caller identity; relevance: `gateway.*_no_auth` + `gateway.token_too_short` checks.
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency/plugin provenance; relevance: `plugins.installs_*` + `plugins.code_safety` checks.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — damage scope; relevance: `security.exposure.open_groups_with_elevated` blast-radius checks.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: `gateway.auth_no_rate_limit` check.

**Docs**
- [cc: Hooks Guardrail and Audit Recipes](../claude_code/cc_hooks_guardrail_and_audit_recipes.md) — guardrail/audit reference; relevance: analogous structured audit/finding reference.
- [cc: Admin Enforcement Controls](../claude_code/cc_admin_enforcement_controls.md) — enforce/verify config; relevance: parallels the config-drift checkId classes.
- [cc: Sandbox Org Enforcement](../claude_code/cc_sandbox_org_enforcement.md) — org-level sandbox enforcement; relevance: parallels `sandbox.*` policy-drift findings.
- [cc: Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool rules; relevance: parallels `tools.exec.*` finding catalog.
- [cc: Managed Permission Settings and Precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — settings precedence; relevance: parallels `tools.profile_minimal_overridden`.
- [hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — command-approval reference; relevance: sibling exec-approval finding analog.
- [OpenClaw — Audit](oc_gateway_security_audit.md) (planned, this series) — summarizes this catalog; relevance: note 7 is the full catalog behind note 2.
- [OpenClaw — Network Hardening](oc_gateway_security_network_hardening.md) (planned, this series) — fixes `gateway.*` findings; relevance: network checkIds remediated there.
- [OpenClaw — Tool/Sandbox Hardening](oc_gateway_security_tool_sandbox_hardening.md) (planned, this series) — fixes `sandbox.*`/`tools.exec.*`; relevance: exec/sandbox checkIds remediated there.
- [OpenClaw — Data Protection](oc_gateway_security_data_protection.md) (planned, this series) — fixes `fs.*`/`logging.*`; relevance: permissions/redaction checkIds remediated there.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — the boundaries findings map to; relevance: severity reflects boundary impact.

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — emits the `checkId` findings; relevance: the catalog's source module.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — config surface checked; relevance: `gateway.*` checks read this config tree.
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent config checked; relevance: `tools.exec.*` per-agent + `auth_profiles` checks.

**Snippets**
- [snippet: security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composes the finding set; relevance: how checkIds are aggregated.
- [snippet: security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel/group exposure findings; relevance: `security.exposure.open_channels_*` checks.
- [snippet: security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM exposure findings; relevance: DM-policy checkIds.
- [snippet: security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec/runtime findings; relevance: `tools.exec.*` checkId family.
- [snippet: security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec fs-drift policy; relevance: `tools.exec.fs_tools_disabled_but_exec_enabled`.
- [snippet: security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin-trust findings; relevance: `plugins.*` checkId family.
- [snippet: security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — resolves plugin trust/allowlist; relevance: `plugins.extensions_no_allowlist`.
- [snippet: security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — scans skill code; relevance: `skills.code_safety` findings.
- [snippet: opengrep_compile_collect](../../code_snippets/snippet_openclaw_opengrep_compile_collect.md) — collects code-scan matches; relevance: `plugins.code_safety` deep-scan engine.
- [snippet: gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: `gateway.nodes.allow_commands_dangerous` / `deny_commands_ineffective`.
- [snippet: gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution; relevance: `gateway.trusted_proxy_*` + auth checks.
- [snippet: security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — live gateway probe; relevance: `gateway.probe_failed` / `probe_auth_secretref_unavailable`.

### oc_gateway_security_exposure_runbook (8t · 11s · 11d)

**Terms**
- [Access Control](../../term_dictionary/term_access_control.md) — who-can-reach/trigger gating; relevance: "who can reach it, how authenticated, which agents/tools."
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — forwarding intermediary; relevance: trusted-reverse-proxy exposure pattern + checks.
- [VPN](../../term_dictionary/term_vpn.md) — private network overlay; relevance: Tailscale Serve/tailnet exposure patterns.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: "non-main sessions run in sandbox mode."
- [Authentication](../../term_dictionary/term_authentication.md) — caller identity + token rotation; relevance: auth-mode inventory + rotation on rollback.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — damage scope; relevance: "widen one control at a time" minimizes exposure.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: rate limits as a public-exposure control.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: TLS required for public/identity-aware-proxy exposure.

**Docs**
- [cc: Network, TLS, and Access](../claude_code/cc_network_tls_and_access.md) — network/TLS/access controls; relevance: the exposure surface this runbook gates.
- [cc: Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — reverse-proxy/gateway setup; relevance: the trusted-proxy exposure pattern.
- [cc: Enterprise Deployment Options](../claude_code/cc_enterprise_deployment_options.md) — deployment exposure choices; relevance: analogous "choose the narrowest pattern" decision.
- [cc: DevContainer Hardening](../claude_code/cc_devcontainer_hardening.md) — firewall/isolation hardening; relevance: firewall-allowlist + isolation pre-flight.
- [hermes: Gateway Operations](../hermes_agent/hermes_gateway_operations.md) — operating a messaging gateway; relevance: sibling operator exposure/runbook analog.
- [hermes: Dashboard Auth Remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: remote Control-UI exposure checks.
- [OpenClaw — Audit](oc_gateway_security_audit.md) (planned, this series) — baseline check before/after exposure; relevance: `openclaw security audit --deep` is a runbook step.
- [OpenClaw — Network Hardening](oc_gateway_security_network_hardening.md) (planned, this series) — bind/auth/proxy controls; relevance: the controls applied per exposure step.
- [OpenClaw — Tool/Sandbox Hardening](oc_gateway_security_tool_sandbox_hardening.md) (planned, this series) — tool/sandbox review; relevance: "Tool and sandbox review" section.
- [OpenClaw — Tailscale](oc_gateway_tailscale.md) (planned, this series) — Serve/Funnel exposure; relevance: tailnet/public exposure patterns.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — the model this runbook applies; relevance: "turns Security guidance into an operator checklist."

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — audit/doctor/health checks; relevance: the baseline-check commands the runbook runs.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — bind/expose/probe surface; relevance: `gateway probe` + bind changes.

**Snippets**
- [snippet: security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — live gateway probe; relevance: `openclaw gateway probe --url ... --token ...` baseline check.
- [snippet: security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — full audit run; relevance: "Run these before opening access."
- [snippet: gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution; relevance: minimum-safe-baseline `auth.mode: "token"`.
- [snippet: gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — applies config changes; relevance: rollback config (`bind: "loopback"`, `dmPolicy: "disabled"`).
- [snippet: channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing/allowlist; relevance: "DM and group exposure" pairing/allowlist controls.
- [snippet: security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny dangerous tools; relevance: "avoid browser/canvas/node/cron/gateway tools for open surfaces."
- [snippet: agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool policy; relevance: "route shared channels to agents with minimal tools."
- [snippet: agents_subagent_spawn_policy](../../code_snippets/snippet_openclaw_agents_subagent_spawn_policy.md) — sub-agent spawn gating; relevance: avoid session-spawn tools on open surfaces.
- [snippet: gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize/dispatch; relevance: "test unauthorized sender is denied."
- [snippet: security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel exposure audit; relevance: "confirm DM/group routing reaches only the intended agent."
- [snippet: gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: tool/sandbox review of node command exposure.

### oc_gateway_tailscale (8t · 10s · 11d)

**Terms**
- [VPN](../../term_dictionary/term_vpn.md) — private network overlay; relevance: Tailscale is the WireGuard-based tailnet VPN.
- [TLS](../../term_dictionary/term_tls.md) — transport encryption; relevance: Serve/Funnel provide HTTPS while the gateway stays on loopback.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — identity-forwarding intermediary; relevance: Serve injects identity headers like a trusted proxy.
- [Authentication](../../term_dictionary/term_authentication.md) — caller identity; relevance: `gateway.auth.mode` + `allowTailscale` identity-header auth.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent connection; relevance: Serve/Funnel expose the Gateway Control UI + WS.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — single network entry point; relevance: "Serve/Funnel only expose the Gateway control UI + WS."
- [Access Control](../../term_dictionary/term_access_control.md) — who-can-reach gating; relevance: Funnel requires a shared password; node browser-control trust.
- [Encryption](../../term_dictionary/term_encryption.md) — protect data in transit; relevance: HTTPS-everywhere via Tailscale.

**Docs**
- [cc: Network, TLS, and Access](../claude_code/cc_network_tls_and_access.md) — network/TLS access; relevance: analogous TLS-terminating remote-access path.
- [cc: Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway header handling; relevance: Serve identity-header behavior parallel.
- [cc: Remote Control](../claude_code/cc_remote_control.md) — remote access to the agent; relevance: analogous remote-dashboard exposure.
- [cc: Cloud Network Access](../claude_code/cc_cloud_network_access.md) — network exposure controls; relevance: tailnet vs public exposure decision.
- [hermes: Dashboard Auth Remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote dashboard auth; relevance: sibling remote Control-UI auth analog.
- [hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — tunneled remote access; relevance: alternative to Tailscale for private remote access.
- [OpenClaw — Network Hardening](oc_gateway_security_network_hardening.md) (planned, this series) — Tailscale Serve identity-header rules; relevance: this doc is the full version of that section.
- [OpenClaw — Exposure Runbook](oc_gateway_security_exposure_runbook.md) (planned, this series) — tailnet/public exposure patterns; relevance: Serve/Funnel are runbook exposure rows.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — "tokenless Serve assumes host is trusted"; relevance: the trust assumption behind allowTailscale.
- [OpenClaw — Audit](oc_gateway_security_audit.md) (planned, this series) — flags `gateway.tailscale_funnel`/`_serve`; relevance: audit reports Tailscale exposure.
- [OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md) (planned, this series) — `gateway.tailscale_*` checkIds; relevance: the Tailscale exposure findings.

**Repos**
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Tailscale Serve/Funnel auto-config; relevance: implements `tailscale serve`/`funnel` orchestration.
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — Tailscale identity-header verification; relevance: `tailscale whois` identity check + audit findings.

**Snippets**
- [snippet: gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution incl. allowTailscale; relevance: the Serve/Funnel auth handshake.
- [snippet: gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket/device identity; relevance: Serve path skips device-pairing for browser-identity sessions.
- [snippet: gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity + TLS; relevance: tailnet `*.ts.net` ws/wss handling.
- [snippet: kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning in client kit; relevance: secure tailnet connection from clients.
- [snippet: gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener; relevance: the loopback surface Serve fronts.
- [snippet: gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize/dispatch; relevance: HTTP API endpoints do NOT use Tailscale identity auth.
- [snippet: gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect-through-proxy; relevance: x-forwarded-* header handling for Serve.
- [snippet: gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: "nodes connect over the same Gateway WS endpoint."
- [snippet: gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection lifecycle; relevance: node access over Serve WS.
- [snippet: gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: "treat node pairing like operator access" for remote browser control.

### oc_gateway_secrets_plan_contract (8t · 11s · 11d)

**Terms**
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored credential token; relevance: `auth-profiles.json` `keyRef`/`tokenRef` targets.
- [Authentication](../../term_dictionary/term_authentication.md) — credential management; relevance: the plan writes provider/model API keys.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model/credential provider; relevance: `models.providers.*` + `secrets.providers` upserts.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — structured RPC envelope; relevance: `version`/`protocolVersion` plan-file shape.
- [Function Calling](../../term_dictionary/term_function_calling.md) — structured tool/schema invocation; relevance: the typed `targets` schema validation.
- [Access Control](../../term_dictionary/term_access_control.md) — path/segment gating; relevance: forbidden-segment rejection (`__proto__`/`prototype`/`constructor`).
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — exec/external provider trust; relevance: exec-provider `--allow-exec` consent.
- [Secrets Management](../../term_dictionary/term_oauth.md) — credential lifecycle (OAuth flows); relevance: `secrets apply` mutates credential targets (OAuth import path).

**Docs**
- [cc: Authentication](../claude_code/cc_authentication.md) — credential/auth setup; relevance: analogous credential-write surface.
- [cc: SDK Credential and Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential scoping; relevance: parallels target-path credential validation.
- [cc: Managed MCP Configuration](../claude_code/cc_managed_mcp_configuration.md) — managed provider/credential config; relevance: provider-upsert config-write parallel.
- [cc: Settings Scopes and Precedence](../claude_code/cc_settings_scopes_and_precedence.md) — config path/precedence; relevance: analogous to dot-path target validation.
- [hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — credential provider pools; relevance: sibling provider-credential model.
- [hermes: Secrets Bitwarden](../hermes_agent/hermes_secrets_bitwarden.md) — exec-provider secret sourcing; relevance: parallels exec SecretRef provider (`op read`, etc.).
- [OpenClaw — Data Protection](oc_gateway_security_data_protection.md) (planned, this series) — the credential storage map; relevance: where the written targets live on disk.
- [OpenClaw — Secure File Operations](oc_gateway_security_secure_file_operations.md) (planned, this series) — secret-file helpers; relevance: how secret files are written safely.
- [OpenClaw — Audit](oc_gateway_security_audit.md) (planned, this series) — flags secrets-in-config; relevance: `config.secrets.*` findings on raw credentials.
- [OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md) (planned, this series) — `fs.auth_profiles.*` catalog; relevance: protecting the targets this plan writes.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — config-write trust boundary; relevance: "fail before mutating configuration."

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — `secrets apply` validation; relevance: enforces the plan contract.
- [repo: openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — `config.apply` write path; relevance: applies `openclaw.json` targets.
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — `auth-profiles.json` targets; relevance: per-agent credential targets require `agentId`.

**Snippets**
- [snippet: gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — resolves credentials/SecretRefs; relevance: the `secrets.providers` resolution the plan mutates.
- [snippet: agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — exec/external-CLI SecretRef provider; relevance: exec-provider consent (`--allow-exec`).
- [snippet: agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: `keyRef`/`tokenRef` runtime resolution.
- [snippet: agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: OAuth credential targets.
- [snippet: gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — applies a config change; relevance: `secrets apply` writes supported `openclaw.json` targets.
- [snippet: gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — plans a config reload/diff; relevance: dry-run-before-apply plan validation.
- [snippet: gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope with version; relevance: `version`/`protocolVersion` plan shape.
- [snippet: gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — gates config-mutating calls; relevance: fail-closed write protection.
- [snippet: security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: exec-provider runtime/audit scope notes.
- [snippet: gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — env-source resolution; relevance: `ref.source: "env"` provider targets.
- [snippet: security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny config-mutating tools; relevance: the `gateway` tool refuses to rewrite protected exec paths.

### oc_gateway_security_secure_file_operations (8t · 10s · 11d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: fs-safe is "a library guardrail, not a sandbox."
- [Access Control](../../term_dictionary/term_access_control.md) — bounded file access; relevance: root-bounded reads/writes, reject `..`/absolute escapes.
- [Blast Radius](../../term_dictionary/term_blast_radius.md) — damage scope; relevance: "host perms / OS users / containers / tool policy define the real blast radius."
- [PII](../../term_dictionary/term_pii.md) — sensitive data; relevance: secret/private-state file helpers with private modes.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin-facing API surface; relevance: "plugin file access should go through `openclaw/plugin-sdk/*`."
- [Data Minimization](../../term_dictionary/term_data_minimization.md) — limit data exposure; relevance: byte limits for reads + archive extraction.
- [Encryption](../../term_dictionary/term_encryption.md) — protect at rest; relevance: secret-file private modes complement disk encryption.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: "keeps behavior predictable across desktop/Docker/CI" (Python-helper default).

**Docs**
- [cc: Sandbox Filesystem and Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — fs isolation boundaries; relevance: distinguishes library-guardrail vs sandbox.
- [cc: SDK Credential and Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — fs + credential scoping; relevance: parallels root-bounded fs + secret helpers.
- [cc: File Tool Behavior](../claude_code/cc_file_tool_behavior.md) — file-read/write tool guardrails; relevance: parallels path-escape rejection.
- [cc: DevContainer Hardening](../claude_code/cc_devcontainer_hardening.md) — container fs/network hardening; relevance: "use sandboxing for hostile local-user isolation."
- [hermes: Security Isolation and Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — fs/credential isolation; relevance: sibling secret-file handling analog.
- [pi: Containerization](../pi/pi_containerization.md) — container isolation; relevance: "run separate gateways under separate OS users/hosts."
- [OpenClaw — Data Protection](oc_gateway_security_data_protection.md) (planned, this series) — secrets on disk; relevance: fs-safe writes those secret/state files.
- [OpenClaw — Tool/Sandbox Hardening](oc_gateway_security_tool_sandbox_hardening.md) (planned, this series) — sandbox vs library distinction; relevance: "fs-safe is not a sandbox."
- [OpenClaw — Secrets Plan Contract](oc_gateway_secrets_plan_contract.md) (planned, this series) — secret-file writes; relevance: file SecretRef payloads use fs-safe secret helpers.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — single-operator trust model; relevance: "trusted gateway code handling untrusted path input."
- [OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md) (planned, this series) — `fs.config.symlink` etc.; relevance: fs-safe refuses symlink/hardlink patterns.

**Repos**
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — fs-safe usage under `src/infra/*`; relevance: "core code should use the fs-safe wrappers."
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin-sdk fs helpers; relevance: "plugin file access goes through plugin-sdk helpers."
- [repo: openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent workspace/state files; relevance: agent-state writes go through fs-safe.

**Snippets**
- [snippet: security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — fs bridge for openshell; relevance: root-bounded fs access bridging.
- [snippet: security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem policy; relevance: workspace-only fs guardrails alongside fs-safe.
- [snippet: security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — openshell backend fs handling; relevance: trusted-root file operations.
- [snippet: security_openshell_mirror](../../code_snippets/snippet_openclaw_security_openshell_mirror.md) — mirrors/normalizes fs paths; relevance: canonical-path resolution vs `startsWith` checks.
- [snippet: gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — reads session-store files; relevance: atomic/identity-checked reads.
- [snippet: gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secret-file resolution; relevance: "use OpenClaw secret helpers, not hand-rolled mode checks."
- [snippet: plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-sdk entry surface; relevance: `openclaw/plugin-sdk/*` fs helpers.
- [snippet: process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — spawns/orchestrates child processes; relevance: the optional Python sidecar helper process.
- [snippet: process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — supervises long-lived processes; relevance: "persistent Python process" lifecycle.
- [snippet: gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: `OPENCLAW_FS_SAFE_PYTHON_MODE` env handling.

### oc_gateway_security_shrinkwrap (8t · 10s · 11d)

**Terms**
- [Supply Chain](../../term_dictionary/term_supply_chain.md) — dependency provenance/integrity; relevance: shrinkwrap is "a supply-chain hardening boundary."
- [npm](../../term_dictionary/term_npm.md) — Node package manager; relevance: `npm-shrinkwrap.json` is npm's publishable lockfile.
- [Threat Model](../../term_dictionary/term_threat_model.md) — risk-boundary enumeration; relevance: shrinkwrap defines the release-reproducibility boundary.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: "shrinkwrap is not a sandbox; it doesn't make a dependency safe."
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin packages; relevance: OpenClaw-owned plugin packages carry their own locked graph.
- [Access Control](../../term_dictionary/term_access_control.md) — controlling what installs; relevance: "review these files as security-sensitive."
- [CI/CD](../../term_dictionary/term_ci_cd.md) — automated build/release pipeline; relevance: release validation tests the same graph users install.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — installable provider/plugin package; relevance: plugin tarballs ship `bundledDependencies`.

**Docs**
- [cc: Managed Plugin Policy Settings](../claude_code/cc_managed_plugin_policy_settings.md) — plugin install/policy controls; relevance: analogous plugin supply-chain policy surface.
- [cc: Plugin Dependencies](../claude_code/cc_plugin_dependencies.md) — plugin dependency resolution; relevance: parallels plugin-local locked dependency graph.
- [cc: DevContainer Hardening](../claude_code/cc_devcontainer_hardening.md) — dependency/network hardening; relevance: reproducible-install hardening analog.
- [cc: Update and Release Channels](../claude_code/cc_update_and_release_channels.md) — release/version channels; relevance: "release reproducibility" boundary parallel.
- [hermes: Plugins Management](../hermes_agent/hermes_plugins_management.md) — plugin install/lifecycle; relevance: sibling plugin packaging/supply-chain analog.
- [hermes: Updating Uninstalling](../hermes_agent/hermes_updating_uninstalling.md) — update/version handling; relevance: locked-install update boundary parallel.
- [OpenClaw — Tool/Sandbox Hardening](oc_gateway_security_tool_sandbox_hardening.md) (planned, this series) — plugin install trust; relevance: "inspect unpacked plugin code; prefer pinned versions."
- [OpenClaw — Audit](oc_gateway_security_audit.md) (planned, this series) — `plugins.installs_*` findings; relevance: audit flags unpinned/integrity-missing installs.
- [OpenClaw — Audit Checks](oc_gateway_security_audit_checks.md) (planned, this series) — `plugins.installs_unpinned_npm_specs` etc.; relevance: the supply-chain checkIds.
- [OpenClaw — Threat Model](oc_gateway_security_threat_model.md) (planned, this series) — supply-chain risk boundary; relevance: "supply-chain exposure" in the trust model.
- [OpenClaw — Secure File Operations](oc_gateway_security_secure_file_operations.md) (planned, this series) — "not a sandbox" sibling concept; relevance: both are library/boundary guardrails, not sandboxes.

**Repos**
- [repo: openclaw](../../../areas/code_repos/repo_openclaw.md) — root npm package; relevance: ships `npm-shrinkwrap.json` on publish.
- [repo: openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin packages w/ bundledDependencies; relevance: plugin-local locked graphs.
- [repo: openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — package validators + audit; relevance: rejects `package-lock.json`, requires shrinkwrap.

**Snippets**
- [snippet: security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composes audit incl. install checks; relevance: where plugin install findings surface.
- [snippet: security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin install/trust findings; relevance: unpinned/integrity-missing/version-drift checks.
- [snippet: security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — resolves plugin install trust; relevance: plugin install-source trust decisions.
- [snippet: plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package shape/contract; relevance: what a publishable plugin tarball must include.
- [snippet: plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/load lifecycle; relevance: install-time vs bundled-dependency behavior.
- [snippet: plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-sdk entry surface; relevance: plugin packages' runtime entry/deps.
- [snippet: security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — scans skill/plugin install material; relevance: `--deep` diagnostic scanning of installs.
- [snippet: opengrep_compile_collect](../../code_snippets/snippet_openclaw_opengrep_compile_collect.md) — collects code-scan matches; relevance: package-inspection/code-safety scanning.
- [snippet: gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — install policy hook; relevance: `security.installPolicy` allow/block decisions.
- [snippet: cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command registry; relevance: the `plugins install`/`deps:shrinkwrap:*` command surface.

## Undigested Terms Plan

Per master: OpenClaw vocabulary terms are the subjects of their home doc pages and are digested as `oc_*` doc notes, NOT
new `term_dictionary` entries. The only `term_dictionary` interaction is **linking existing** terms (verified above).
**Expected 0 new `term_dictionary` captures.**

| Term (appears in source) | Disposition |
|---|---|
| security audit / checkId / audit finding | Documented as `oc_gateway_security_audit` (note 2) + `oc_gateway_security_audit_checks` (note 7); not a term note (OpenClaw-specific feature). |
| trust boundary / trust model / personal-assistant model | Concept of `oc_gateway_security_threat_model` (note 1); link existing `term_threat_model`, `term_access_control`. |
| prompt injection / external content / special-token sanitization | Concept of `oc_gateway_security_prompt_injection` (note 5); link existing `term_prompt_injection`. |
| sandboxing / per-agent access profile / tool policy | Concept of note 4; link existing `term_sandbox`, `term_function_calling`. Sandbox deep doc is gw05. |
| secrets apply plan / target / providerUpserts / SecretRef | Schema of `oc_gateway_secrets_plan_contract` (note 10); SecretRef surface is rf03; link `term_oauth_token`, `term_authentication`. No `term_secretref` exists (NOT created — OpenClaw-specific config shape, lives in doc note). |
| fs-safe / fd-relative / atomic write | Concept of `oc_gateway_security_secure_file_operations` (note 11); link existing `term_sandbox`, `term_access_control`. |
| npm shrinkwrap / pnpm-lock / bundledDependencies | Concept of `oc_gateway_security_shrinkwrap` (note 12); link existing `term_supply_chain`, `term_npm`. |
| Tailscale Serve / Funnel / tailnet | Procedure of `oc_gateway_tailscale` (note 9); link existing `term_vpn`, `term_tls`. No `term_tailscale` exists (NOT created — product-specific; the doc note + `term_vpn` cover it). |
| mDNS / Bonjour / SSRF / DNS rebinding / trusted-proxy | Hardening details in notes 3/4; no dedicated term notes exist (`term_mdns`/`term_bonjour`/`term_ssrf`/`term_dns_rebinding` MISSING) and they are inline hardening details, not reusable cross-cutting vault terms → documented in the `oc_*` notes, no new term captures. |
| incident response / rotate / contain | Procedure of note 6; link existing `term_blast_radius`, `term_authentication`. |

**New-term candidates: none.** All cross-cutting security concepts present (threat model, access control, sandbox, blast
radius, prompt injection, supply chain, rate limiting, TLS, VPN, PII, data minimization) already have substantive
Tailscale Serve/Funnel modes, mDNS minimal mode) are product features digested in the `oc_*` notes, not promoted.

## Term-Note Authoring Requirements

(If augment's Step 2d re-scan surfaces a genuinely reusable cross-cutting term with no existing note and no doc-page home,
it would be captured via `/tessellum-capture-term-note` + added to the best-fit `acronym_glossary_*.md` per master W5 —
not expected here.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (12 notes, P1). All gates must pass before commit.

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order/types valid; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; bold `**Source**`/`**Last Updated**`/`**Status**` footer. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/gateway/<page>` | Every claim/config traceable to source; no invented behavior; config snippets reproduced verbatim. |
| G3 | Density + Coverage | word/code/line caps + Section Coverage Map | ≤2500w, ≤6 code blocks, ≤400 lines, single BB; every mapped H2/H3 covered, no orphans. |
| G4 | Cross-Reference | `## Related Notes` floors | ≥6 relevance-selected term_dictionary terms + relevant repo_openclaw*/sibling oc_*/docs/snippets, each with a relevance statement, all indexed `[text](path.md)` links. |
| G5 | Ghost-reference | detect + redirect | 0 links to non-existent notes; sibling oc_* links resolve once all 12 land. |
| G6 | Broken-link | `/tessellum-fix-broken-links` + reindex | 0 broken links after incremental reindex. |
| G7/G8 | Discoverability | in-degree ≥1 from outside `documentation/openclaw/` | Each note RECEIVES ≥1 inbound link from outside the folder (via `entry_openclaw_docs.md` + repo_openclaw*/term_* inlinks); anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_gateway_security_threat_model oc_gateway_security_audit oc_gateway_security_network_hardening \
oc_gateway_security_tool_sandbox_hardening oc_gateway_security_prompt_injection oc_gateway_security_data_protection \
oc_gateway_security_audit_checks oc_gateway_security_exposure_runbook oc_gateway_tailscale \
oc_gateway_secrets_plan_contract oc_gateway_security_secure_file_operations oc_gateway_security_shrinkwrap"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (${words}w ${cb}cb ${lines}L)"
  # sibling-prefix sanity (informational): count oc_ sibling links
  echo "$n sibling oc_ links: $(grep -oE '\]\('"$SIBLING_PREFIX"'[a-z0-9_]+\.md\)' "$f" | wc -l)"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
bash scripts/update_notes_database.sh   # incremental reindex, then verify note_links + 0 broken links
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w/≤6cb/≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_gateway_security_threat_model | argument | 700 | 2 | ✅ |
| 2 | oc_gateway_security_audit | procedure | 650 | 2 | ✅ |
| 3 | oc_gateway_security_network_hardening | procedure | 750 | 5 | ✅ |
| 4 | oc_gateway_security_tool_sandbox_hardening | procedure | 750 | 6 | ✅ (at code cap; trim examples if exceeded) |
| 5 | oc_gateway_security_prompt_injection | argument | 700 | 0 | ✅ |
| 6 | oc_gateway_security_data_protection | procedure | 700 | 4 | ✅ |
| 7 | oc_gateway_security_audit_checks | model | 700 | 0 | ✅ (prose + condensed checkId table; reproduce high-signal rows, link full source) |
| 8 | oc_gateway_security_exposure_runbook | procedure | 600 | 3 | ✅ |
| 9 | oc_gateway_tailscale | procedure | 600 | 5 | ✅ |
| 10 | oc_gateway_secrets_plan_contract | model | 600 | 4 | ✅ |
| 11 | oc_gateway_security_secure_file_operations | concept | 450 | 2 | ✅ |
| 12 | oc_gateway_security_shrinkwrap | concept | 450 | 4 | ✅ |

No note approaches the word cap. The code-heavy split of `security.md` (19 fences) spreads its config blocks across notes
3/4/6 so each stays ≤6; note 4 is at the 6-block cap — reproduce only the most load-bearing access-profile examples and
link the rest. Note 7 (audit-checks, 2,082w / 0 fences) condenses the ~80-row catalog to high-signal rows grouped by
surface with a pointer to the full source, keeping it ≤700w.

## Entry Point Decision (inherited from master)

Contributes **12 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under a **"Gateway — Security"**
cluster (the gw06 section). Each note also gets its entry-point back-link at finalization (satisfies G7/G8). Parent-hub
master-level steps W2/W3, not repeated per sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all targets verified present 2026-06-20):

- `entry_openclaw_docs.md` (planned, master W1) → **all 12** notes (primary anti-island guarantee).
- `repo_openclaw_security.md` → notes 1, 2, 4, 6, 7, 10, 11 (the code-side security module documents these surfaces).
- `repo_openclaw_gateway.md` → notes 1, 3, 8, 9, 10 (bind/auth/proxy/Tailscale control plane).
- `repo_openclaw_agents.md` → notes 4, 5, 6 (per-agent sandbox/tool policy, auth-profiles, system-prompt context).
- `repo_openclaw_sessions.md` → note 6 (session transcripts on disk).
- `repo_openclaw_extensions.md` → notes 4, 11, 12 (plugin trust, plugin-sdk fs helpers, plugin packages).
- `term_threat_model.md` → notes 1, 7; `term_sandbox.md` → notes 4, 11; `term_prompt_injection.md` → note 5;
  `term_supply_chain.md` → note 12; `term_vpn.md` → note 9; `term_reverse_proxy.md` → notes 3, 9; `term_access_control.md`
  → notes 1, 6; `term_npm.md` → note 12.

## Pacing Rules (inherited from master)

Single execution phase; cap dynamic-workflow fan-out at ~30 agents/run (12 notes here, well within cap). Embed the
manifest in the execution script. Re-read each source page before authoring its note(s); reproduce config snippets
verbatim. One BB per note. Reindex incrementally after the wave; verify `note_links` + 0 broken links before commit.
`git pull --rebase --autostash origin main` first; commit + push the sub-plan as one cycle; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment; per-note Related Notes locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** lock the per-note `## Related Notes` mapping at the RAISED floors (≥8 term_dictionary
"Candidate Cross-References" pool. The plan's other 15 augment sections (Section Coverage Map, Split Decisions, Density
Re-Assessment, Pacing Rules, Validation Scripts incl. ghost-detect, Inlink Mapping, Undigested Terms Plan with slug
specificity + collision audit, Term-Note Authoring Requirements [N/A — 0 new terms], Entry Point Decision] were already
present from the initial authoring and were re-verified against the re-read source.

**What was locked.** Re-read all 7 source pages under `inbox/openclaw_docs/gateway/` (measured 2026-06-21:
security.md 9,223w; audit-checks 2,027w; exposure-runbook 1,113w; tailscale 910w; secrets-plan-contract 609w;
shrinkwrap 508w; secure-file-operations 521w — total 15,211w, matches the plan's Source table within tolerance). Built
applied — this is a coding-agent security cluster). Drew snippets from the rich existing openclaw corpus (255 snippets)
and docs from the claude_code (`cc_*`), hermes_agent (`hermes_*`), and pi (`pi_*`) coding-agent doc corpora.

**Per-note locked counts** (terms · snippets · existing docs + planned siblings = total docs · repos):

| # | Note | Terms | Snippets | Docs (existing + sibling) | Repos | Floors met |
|---|---|---:|---:|---|---:|---|
| 1 | oc_gateway_security_threat_model | 8 | 11 | 6 + 5 = 11 | 3 | ✅ |
| 2 | oc_gateway_security_audit | 8 | 12 | 6 + 5 = 11 | 3 | ✅ |
| 3 | oc_gateway_security_network_hardening | 9 | 12 | 6 + 5 = 11 | 2 | ✅ |
| 4 | oc_gateway_security_tool_sandbox_hardening | 9 | 12 | 7 + 4 = 11 | 4 | ✅ |
| 5 | oc_gateway_security_prompt_injection | 8 | 10 | 7 + 4 = 11 | 3 | ✅ |
| 6 | oc_gateway_security_data_protection | 8 | 12 | 6 + 5 = 11 | 4 | ✅ |
| 7 | oc_gateway_security_audit_checks | 8 | 12 | 6 + 5 = 11 | 3 | ✅ |
| 8 | oc_gateway_security_exposure_runbook | 8 | 11 | 6 + 5 = 11 | 2 | ✅ |
| 9 | oc_gateway_tailscale | 8 | 10 | 6 + 5 = 11 | 2 | ✅ |
| 10 | oc_gateway_secrets_plan_contract | 8 | 11 | 6 + 5 = 11 | 3 | ✅ |
| 11 | oc_gateway_security_secure_file_operations | 8 | 10 | 6 + 5 = 11 | 3 | ✅ |
| 12 | oc_gateway_security_shrinkwrap | 8 | 10 | 6 + 5 = 11 | 3 | ✅ |


**New-term candidates: NONE.** Confirmed against the re-read source. All cross-cutting security concepts already have
supply_chain, rate_limiting, tls, vpn, pii, data_minimization, encryption, multi_agent, subagent, +more). The
OpenClaw-specific items surfaced in the re-read (checkId, secrets-plan-contract, fs-safe, npm shrinkwrap, Tailscale
Serve/Funnel modes, mDNS minimal mode, SSRF policy, DNS rebinding, trusted-proxy auth) are product features digested in
the `oc_*` notes, not promoted to `term_dictionary` (consistent with the master's corpus-wide Pattern-B decision and the
claude_code/pi precedents). Existence checks confirmed `term_ssrf`/`term_dns_rebinding`/`term_mdns`/`term_firewall`/
`term_secrets_management` do NOT exist and are correctly left undocumented as inline hardening details (best-fit
glossary if ever promoted: the agentic/LLM-tooling glossary, but **not recommended** — product-specific, doc-note home
exists). **Net: 0 new term captures; best-fit glossary N/A.**

`cc_security_architecture`, `cc_security_guidance_layers_and_rules`, `cc_security_guidance_plugin`,
`cc_prompt_injection_defenses`, `cc_what_claude_can_access`, `cc_zero_data_retention`, `cc_data_usage_and_telemetry`,
`cc_hooks_guardrail_and_audit_recipes`, `cc_sandbox_vs_permissions`, `cc_sandbox_org_enforcement`,
`cc_tool_specific_permission_rules`, `cc_managed_permission_settings_and_precedence`, `cc_settings_scopes_and_precedence`,
`cc_computer_use_safety`, `cc_cloud_network_access`, `cc_remote_control`, `cc_enterprise_deployment_options`,
`cc_file_tool_behavior`, `cc_plugin_dependencies`, `cc_update_and_release_channels`,
`cc_sdk_credential_and_filesystem_controls`, `cc_admin_enforcement_controls`, `cc_managed_mcp_configuration`,
`cc_authentication`; hermes — `hermes_security_isolation_credentials`, `hermes_security_command_approval`,
`hermes_gateway_internals`, `hermes_gateway_operations`, `hermes_dashboard_auth_remote`, `hermes_subagent_delegation`,
`hermes_code_execution`, `hermes_credential_pools`, `hermes_secrets_bitwarden`, `hermes_oauth_over_ssh`,
`hermes_session_storage`, `hermes_plugins_management`, `hermes_updating_uninstalling`; pi — `pi_security_model`,
`pi_containerization`. Terms added beyond the pool: `term_encryption`, `term_multi_agent`, `term_subagent`,
`term_ci_cd`. Snippets added (from the existing openclaw corpus): `snippet_openclaw_security_dangerous_tools_deny`,
`_security_external_content`, `_security_fix_remediation`, `_security_openshell_backend`/`_mirror`,
`_security_plugins_trust_findings`/`_resolver`, `_security_skill_scanner`, `_gateway_node_command_policy`,
`_gateway_auth_authorize_dispatch`, `_gateway_call_method_gating`, `_gateway_server_http_listen_ws`,
`_gateway_client_identity_tls`/`_connect_proxy`, `_gateway_control_ui_auth_ticket`, `_gateway_ws_connection`,
`_gateway_mcp_http_loopback`, `_gateway_hooks_request_handler`/`_config_payload`, `_gateway_runtime_env`,
`_gateway_config_reload_plan`, `_gateway_rpc_protocol_envelope`, `_gateway_chat_history_inject_handler`,
`_gateway_chat_transcript_media_pipeline`, `_gateway_session_fs_index_read`, `_agents_scope`/`_tool_catalog`,
`_agents_subagent_spawn_policy`/`_caps`, `_agents_auth_profiles_oauth_portability`/`_order_credential`,
`_agents_btw_streamSimple_sanitize`, `_sessions_input_provenance`/`_send_policy`/`_session_key_utils`/`_transcript_events`,
`_channels_dm_pairing_allowlist`, `_plugin_lifecycle`/`_package_contract`/`_sdk_entries`,
`_opengrep_compile_collect`/`_validate`, `_process_exec_orchestrator`/`_supervisor`, `_skills_availability_evaluator`,
`_kit_gateway_tls_pinning`, `_android_gateway_session_ws`, `_cli_command_catalog`.

**Issues / flags:** none blocking. (a) The original Candidate pool listed `cc_managed_plugin_policy_settings` with a
"verify at augment" caveat — CONFIRMED present (used in note 12). (b) Note 10 reuses `term_oauth.md` with display text
relevance framing. (c) No source section is orphaned; the Section Coverage Map remains accurate after re-read.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review of the augmented plan against the 9 checkpoints. CP7 page-read spot-check performed live (re-read
security.md, audit-checks.md, exposure-runbook.md; word counts within ±2% of plan estimates).

| CP | Checkpoint | Result | Evidence |
|----|------------|--------|----------|
| CP1 | Related Notes step (≥8 terms + raised floors, relevance-stated) | **PASS** | Per-Note Related Notes Mapping (LOCKED) present; all 12 notes ≥8 terms · ≥10 snippets · ≥10 docs; every link carries a relevance statement; floors auto-counted (see Augmentation Report table). |
| CP2 | 9-GATE present per batch (G1-G6 + G7/G8 + G9) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table covers G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost-reference, G6 Broken-link, G7/G8 Discoverability; single execution phase. |
| CP4 | Plan size manageable | **PASS** | 12 notes — well under the 30 cap; single execution phase; fan-out ≤30. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from the master's Format Definition, which was derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora (`## Overview` / `## Related Notes`, fixed YAML field order, bold footer). G1 table re-asserts it. |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: all 12 notes ≤750w / ≤6 code blocks / ≤400L; security.md (9,223w/19 fences) split into 6 BB-atomic notes; note 4 at the 6-block cap with a documented trim-rule; note 7 condenses the catalog. No note approaches caps. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Live re-read 2026-06-21: security.md 9,223w (plan 9,250), audit-checks 2,027w (plan 2,082), exposure-runbook 1,113w (plan 1,168). All within ±5% — measured, not estimated. |
| CP8 | Undigested Terms + Term-Note Authoring Reqs | **PASS** | Undigested Terms Plan present with per-row disposition; Term-Note Authoring Requirements section present (marked N/A — 0 new terms, with the conditional capture path documented). Master Pattern-B (OpenClaw vocab → doc notes, link existing terms) respected. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
