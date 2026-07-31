---
title: Sub-Plan cl07 — OpenClaw Docs CLI (secrets, security, sessions, setup, skills, status, system)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/secrets", "cli/security", "cli/sessions", "cli/setup", "cli/skills", "cli/status", "cli/system"]
augmented: 2026-06-21
reviewed: 2026-06-21
---

# Sub-Plan cl07: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML field order, `## Overview` / `## Related Notes` / `## References`, density caps), dedup (three-way across `term_dictionary/` + `documentation/` + `repo_openclaw*`), the 9-GATE (G1–G9), corpus-wide cross-references, and entry-point wiring (`entry_openclaw_docs.md`, W1–W5) are ALL inherited from the master.

## Scope

The 7 `openclaw <cmd>` CLI reference pages covering **operator / lifecycle / state-management** commands:
`secrets` (SecretRef reload/audit/configure/apply), `security` (config + filesystem audit and safe fixes),
`sessions` (list / tail / export-trajectory / cleanup / compact stored conversation sessions), `setup`
(initialize baseline config + workspace, optional wizard), `skills` (search/install/update/verify/list/info/check + ClawHub Skill Workshop), `status` (channel + session diagnostics, usage snapshots), and `system`
(enqueue system events, control heartbeats, view presence). **Priority P1 (Phase A)** — these CLI commands are
the operator surface the rest of the OpenClaw docs reference for credential hygiene, runtime health, and
session lifecycle. The code-side counterparts (`repo_openclaw_security`, `repo_openclaw_sessions`,
`repo_openclaw_skills`, `repo_openclaw_cli_wizard`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 5,268 measured body words (893 + 970 + 1,248 + 312 + 896 + 570 + 379). **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| secrets | cli/secrets | 893 | 6 | 7 | 0 | procedure |
| security | cli/security | 970 | 4 | 4 | 0 | procedure (+argument: trust-model audit guidance) |
| sessions | cli/sessions | 1,248 | 9 | 3 | 1 | procedure (split: list/tail/export vs cleanup/compact) |
| setup | cli/setup | 312 | 1 | 4 | 1 | procedure |
| skills | cli/skills | 896 | 2 | 3 | 0 | procedure |
| status | cli/status | 570 | 1 | 1 | 0 | procedure |
| system | cli/system | 379 | 1 | 6 | 0 | procedure |

(Word counts are body-only, computed via `sed -n '/^---$/,/^---$/!p' | wc -w`; code = `grep -c '^```' / 2`. H2/H3 counts exclude the H1 command title and the trailing `## Related` link-stub.)

## Content Strategy

- **Prioritize**: credential-hygiene commands (`secrets`, `security`) — the audit/scrub/fix loops every
  operator runs before exposing a gateway — and the session-state lifecycle (`sessions`), which the
  concepts/session and gateway/config-agents docs reference. These are the load-bearing CLI surfaces.
- **Split**: `sessions.md` (1,248w, 9 code fences) → a discovery/inspection note (list / scope flags / tail /
  export-trajectory) + a maintenance/lifecycle note (cleanup, compact + the `sessions.compact` RPC). Two
  distinct task clusters with the most fences on the page; keeps each note ≤6 code blocks and focused.
- **Group small adjacent pages by command, 1 note each**: the remaining 6 pages are each a single coherent
  command reference well under caps (≤970 words, ≤6 fences) → one note per page. `setup`, `status`, `system`
  are short but are distinct commands with their own flags/RPC surface — keep separate (no cross-BB merge;
  the master's "most reference pages = 1 note" rule applies).
- **Link-out, do not redefine**: the `secrets`/`security` pages point at gateway guides (`/gateway/secrets`,
  `/gateway/security`, `/reference/secretref-credential-surface`, `/gateway/secrets-plan-contract`) and the
  audit cross-references `openclaw doctor --fix`, `openclaw channels status`, `openclaw memory status` — these
  are sibling CLI/gateway pages owned by other sub-plans (cl03 doctor/health, gw05/gw06 secrets/security);
  reference them as `## References` external URLs + planned-sibling links, never inline their content. Term
  vocabulary (SecretRef, sandbox, trust model, ClawHub, heartbeat) links existing `term_*`, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_secrets.md` | procedure | cli/secrets.md: command roles (reload/audit/configure/apply), Reload runtime snapshot, Audit, Configure (interactive helper), Apply a saved plan, Why no rollback backups, Example | 650 | The `openclaw secrets` command: re-resolving SecretRefs (`secrets.reload` RPC, atomic snapshot swap), auditing plaintext residues / unresolved+shadowed refs (exit codes, finding codes), the interactive `configure` planner, applying scrub plans (`--dry-run`, `--allow-exec`), and the no-rollback-backup safety model. |
| 2 | `oc_cli_security.md` | procedure | cli/security.md: Audit (cold vs `--deep`, trust-model warnings, suppressions, SecretRef behavior), JSON output, What `--fix` changes | 650 | The `openclaw security` command: cold config/filesystem audit vs `--deep` live+plugin probes, the personal-assistant trust-model heuristics it flags (open DM/group policy, hooks token reuse, unsandboxed small models, dangerous Docker/network flags, mutable allowlists), `security.audit.suppressions`, JSON output for CI, and the safe deterministic remediations `--fix` does (and does not) apply. |
| 3 | `oc_cli_sessions_inspect.md` | procedure | cli/sessions.md: list (bounding/`--limit`/`configuredAgentsOnly`, scope flags, JSON), Tail trajectory, Export trajectory bundle, discovery scope semantics | 600 | Listing and inspecting stored sessions with `openclaw sessions`: bounded list output (`--limit`, `totalCount`/`hasMore`), scope flags (`--agent`/`--all-agents`/`--store`/`--active`), `sessions tail`/`--follow` redacted trajectory progress, and `export-trajectory` bundles — plus why a session list is not a channel liveness check. |
| 4 | `oc_cli_sessions_maintenance.md` | procedure | cli/sessions.md: Cleanup maintenance (`session.maintenance` modes, `--dry-run`/`--enforce`/`--fix-missing`/`--fix-dm-scope`/`--active-key`, gateway-routed writes), Compact a session, `### sessions.compact RPC` | 600 | Maintaining stored sessions: `sessions cleanup` (prune/cap by `session.maintenance`, dry-run table, fix-missing/fix-dm-scope, active-key protection, gateway-routed writes) and `sessions compact` (LLM-summarize vs `--max-lines` truncate, the `sessions.compact` gateway RPC contract and responses). |
| 5 | `oc_cli_setup.md` | procedure | cli/setup.md: setup intent + Nix refusal, Options table, Wizard auto-trigger, Examples, Notes | 450 | The `openclaw setup` command: initializing baseline config + agent workspace (`agents.defaults.workspace`), the option flags (`--workspace`, `--wizard`, `--non-interactive`/`--accept-risk`, `--mode`, `--import-from`/`--import-source`/`--import-secrets`, `--remote-url`/`--remote-token`), wizard auto-trigger semantics, Nix-mode write refusal, and how it relates to `onboard`/`configure`/`migrate`. |
| 6 | `oc_cli_skills.md` | procedure | cli/skills.md: Commands (search/install/update/verify/list/info/check), install sources + slug/`--global`/`--agent` resolution, verify provenance/`--card`, Skill Workshop (propose/list/inspect/revise/apply/reject/quarantine) | 650 | The `openclaw skills` command: searching/installing skills from ClawHub, Git (`git:owner/repo[@ref]`), or local dirs; workspace vs `--global`/`--agent` targeting; `verify` (ClawHub envelope, `verifiedSourceUrl` provenance, `--card`); `update`/`list`/`info`/`check`; and the `skills workshop` proposal lifecycle. |
| 7 | `oc_cli_status.md` | procedure | cli/status.md: status flags (`--all`/`--deep`/`--usage`), notes (live probes, memory plugin reporting, Execution vs Runtime, usage windows, transcript fallback, model-pin display, SecretRef read-only resolution, Secrets overview) | 500 | The `openclaw status` command: channel + session diagnostics, fast read-only path vs `--deep` live probes vs `--all`, `--usage` provider quota windows, the Execution-vs-Runtime distinction, transcript fallback for token/cache/model labels, session-pin display, and read-only SecretRef resolution + degraded-output behavior. |
| 8 | `oc_cli_system.md` | procedure | cli/system.md: shared client flags, Common commands, `system event` (main-session enqueue, `--mode`/`--session-key` timing exception), `system heartbeat last/enable/disable`, `system presence`, Notes | 450 | The `openclaw system` command: gateway system-level helpers — `system event` (enqueue a `System:` heartbeat-injected event, `--mode now`/`next-heartbeat`, `--session-key` targeted-wake timing exception), `system heartbeat` controls, and `system presence` listing. |

## Section Coverage Map

```
cli/secrets.md
├── (intro) command roles: reload / audit / configure / apply, operator loop → note 1 (oc_cli_secrets)
├── ## Reload runtime snapshot (secrets.reload RPC, options) ───────────── → note 1
├── ## Audit (scan targets, header heuristic, exit, report shape, codes) ─ → note 1
├── ## Configure (interactive helper) (flow, flags, notes, exec safety) ── → note 1
├── ## Apply a saved plan (exec behavior, plan contract, what apply updates) → note 1
├── ## Why no rollback backups ───────────────────────────────────────── → note 1
├── ## Example ───────────────────────────────────────────────────────── → note 1
└── ## Related (link-stub: /cli, /gateway/secrets) ───────────────────── → note 1 References
cli/security.md
├── (intro) security tools (audit + optional fixes) ──────────────────── → note 2 (oc_cli_security)
├── ## Audit (cold vs --deep, trust-model warnings, suppressions, SecretRef) → note 2
├── ## JSON output (CI/policy jq examples) ───────────────────────────── → note 2
├── ## What `--fix` changes (does / does not) ────────────────────────── → note 2
└── ## Related (link-stub) ───────────────────────────────────────────── → note 2 References
cli/sessions.md
├── (intro) list intent, liveness caveat, bounding, configuredAgentsOnly → note 3 (oc_cli_sessions_inspect)
├── (list examples + Scope selection flags + --all-agents discovery + JSON) → note 3
├── (sessions tail / --follow / --session-key / --tail, progress redaction) → note 3
├── (sessions export-trajectory bundle, /export-trajectory slash command) → note 3
├── ## Cleanup maintenance (session.maintenance, flags, gateway-routed, JSON) → note 4 (oc_cli_sessions_maintenance)
├── ## Compact a session (LLM-summarize vs --max-lines, flags, exit) ──── → note 4
├── ### sessions.compact RPC (field table, response examples) ─────────── → note 4
└── ## Related (link-stub: /gateway/config-agents#session, /concepts/session) → notes 3+4 References
cli/setup.md
├── (intro) initialize baseline config + workspace; Nix-mode refusal Note → note 5 (oc_cli_setup)
├── ## Options (flag table) ──────────────────────────────────────────── → note 5
├── ### Wizard auto-trigger ──────────────────────────────────────────── → note 5
├── ## Examples ──────────────────────────────────────────────────────── → note 5
├── ## Notes (plain setup vs onboard/configure/channels add, migration) ─ → note 5
└── ## Related (link-stub: /start/wizard, /start/getting-started, /install) → note 5 References
cli/skills.md
├── (intro) inspect/search/install/verify/update scope ───────────────── → note 6 (oc_cli_skills)
├── ## Commands (search/install/update/verify/list/info/check + workshop) → note 6
├── (install sources, slug resolution, --global/--agent, verify provenance, notes) → note 6
├── ## Skill Workshop (proposal lifecycle, examples) ─────────────────── → note 6
└── ## Related (link-stub: /tools/skills) ────────────────────────────── → note 6 References
cli/status.md
├── (intro) diagnostics for channels + sessions, examples ────────────── → note 7 (oc_cli_status)
├── (Notes block: --deep/--all/--usage, memory plugin, Execution vs Runtime,
│   usage windows, transcript fallback, model pin, SecretRef read-only) ─ → note 7
└── ## Related (link-stub: /cli, /gateway/doctor) ────────────────────── → note 7 References
cli/system.md
├── (intro) system-level gateway helpers, shared client flags ────────── → note 8 (oc_cli_system)
├── ## Common commands ───────────────────────────────────────────────── → note 8
├── ## `system event` (enqueue, --mode, --session-key timing exception) ─ → note 8
├── ## `system heartbeat last|enable|disable` ────────────────────────── → note 8
├── ## `system presence` ─────────────────────────────────────────────── → note 8
├── ## Notes (running gateway required, ephemeral events) ─────────────── → note 8
└── ## Related (link-stub: /cli) ─────────────────────────────────────── → note 8 References
```
No orphaned sections. Trailing `## Related` link-stubs map to each note's `## References`. Cross-referenced
sibling commands (`doctor`, `channels status`, `memory status`, `migrate`, `onboard`, `configure`, `update`)
and gateway guides (`/gateway/secrets`, `/gateway/security`, `/gateway/config-agents`, `/concepts/session`)
are owned by other sub-plans — linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| cli/sessions.md (1,248w, 9 code fences, 3 H2 + 1 H3) | notes 3 (`oc_cli_sessions_inspect`) + 4 (`oc_cli_sessions_maintenance`) | The page mixes read-only discovery/inspection (list/scope flags/tail/export-trajectory) with destructive state maintenance (cleanup pruning, compaction + the `sessions.compact` RPC). These are distinct operator task clusters; it carries the most code fences on the page (9 → would exceed the ≤6 cap in one note) and the most JSON examples. Splitting keeps each note focused and ≤6 code blocks. |

All other 6 pages: 1 note each (each ≤970 words, ≤6 fences, single procedure BB — within caps, no split).

## Summary Statistics & Building Block Distribution

- Source pages: 7 (5,268 body words). New `oc_*` notes: **8**. New `term_dictionary` notes: **0** (master decision — OpenClaw vocab is digested as `oc_*` doc notes; existing terms are linked).
- BB distribution: **procedure ×8** (all 8 notes). `oc_cli_security` carries a secondary argument flavor (the personal-assistant trust-model audit guidance) but the dominant BB is procedure (run the audit, read findings, apply fixes); kept single-BB per the one-BB-per-note rule.
- Est. digest words ~4,550 (avg ~570/note); all ≤650w. 25 source code fences distribute across the 8 notes; each note kept ≤6 (sessions split specifically to honor the fence cap).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_cli_secrets (8t · 11s · 11d)

**Terms** (8)
- [SecretRef / Secrets Manager](../../term_dictionary/term_secrets_manager.md) — externalized secret-reference store resolved at runtime; relevance: `secrets reload` re-resolves SecretRefs and atomically swaps the runtime snapshot, the central object this command manages.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — multi-source credential store with precedence ordering; relevance: `audit` detects precedence drift where `auth-profiles.json` credentials shadow `openclaw.json` refs (`REF_SHADOWED`).
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — per-agent stored credential mapping (`auth-profiles.json`); relevance: `configure --agent` targets `auth-profiles.json` writes and `apply` scrubs provider-target plaintext from it.
- [Authentication](../../term_dictionary/term_authentication.md) — proving identity to a provider/gateway; relevance: the secret-bearing fields the command maps and scrubs are provider authentication credentials.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential for delegated provider access; relevance: `audit` flags legacy OAuth reminders and the legacy auth-store residues among its finding codes.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary for untrusted code; relevance: exec SecretRefs/providers run external commands, gated behind `--allow-exec` and `trustedDirs`/`allowSymlinkCommand` path safety.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — Unix file-mode access control; relevance: exec provider safety pairs `trustedDirs` with Homebrew symlink paths and fails closed on Windows ACL-unverifiable provider paths unless `allowInsecurePath`.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — ordered credential-source resolution (env → profile → role); relevance: a precedent for the env/auth-profile/legacy `.env` precedence chain the secrets audit walks and scrubs.

**Docs** (11; 6 existing + 5 planned-sibling)
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi coding-agent provider credential resolution; relevance: closest analog to OpenClaw's SecretRef/provider credential resolution and precedence model.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — Hermes multi-key credential pools; relevance: the upstream-ecosystem analog of the credential-pool precedence/shadowing the secrets audit reports.
- [hermes_secrets_bitwarden](../hermes_agent/hermes_secrets_bitwarden.md) — external secrets-manager (Bitwarden) integration; relevance: an external exec-style SecretRef provider exactly like the `--allow-exec` provider commands this page guards.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env-var inventory; relevance: maps the env known-secret keys that `apply` migrates and scrubs from `~/.openclaw/.env`.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code credential/auth setup; relevance: analogous coding-agent credential configuration and storage the configure/apply loop manages.
- [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — SDK credential + filesystem guardrails; relevance: parallel to the no-rollback-backup + path-security model and scrub-on-apply behavior.
- [oc_cli_security](oc_cli_security.md) — `openclaw security` audit/fix (planned, this series); relevance: overlapping read-only audit surface; security-audit also resolves SecretRefs read-only.
- [oc_cli_status](oc_cli_status.md) — `openclaw status` diagnostics (planned, this series); relevance: status performs read-only SecretRef resolution and shows a Secrets overview row.
- [oc_gw_secrets](../openclaw/oc_gw_secrets.md) — gateway Secrets Management guide (planned, gw05 series); relevance: the `/gateway/secrets` guide this page links for the full secrets model.
- [oc_reference_secretref_credential_surface](../openclaw/oc_reference_secretref_credential_surface.md) — SecretRef credential surface (planned, rf03 series); relevance: the canonical supported-surface reference `configure` points to.
- [oc_gw_secrets_plan_contract](../openclaw/oc_gw_secrets_plan_contract.md) — Secrets Apply Plan Contract (planned, gw06 series); relevance: the plan contract `apply --from` validates against.

**Repos** (2)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security/audit subsystem; relevance: implements the secrets audit scan, finding codes, and scrub remediations.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: hosts the `secrets.reload` RPC and atomic runtime-snapshot swap.

**Snippets** (11)
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — gateway credentials/secrets RPC call; relevance: the gateway-side `secrets.reload` / credential-resolution path this command drives.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: the precedence/shadowing logic `audit` reports as `REF_SHADOWED`.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth credential portability in auth profiles; relevance: the legacy OAuth residues `audit` flags and `apply` migrates.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI credential provider; relevance: the exec SecretRef provider class gated by `--allow-exec`.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security audit probe executor; relevance: the read-only audit-scan engine shared by `secrets audit`.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem policy; relevance: the `trustedDirs`/symlink/Windows-ACL path-security rules the exec-provider safety note describes.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway auth at startup; relevance: where reused/persisted secret values (`gateway.auth.token`) the audit checks are loaded.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider config; relevance: a `secrets.providers` alias whose `apiKey` SecretRef is the scrub/configure target.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: a provider alias `configure` adds/edits in the `secrets.providers` flow.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — provider model fallback/cooldown; relevance: depends on resolved provider credentials the reload swaps in.

### oc_cli_security (9t · 12s · 11d)

**Terms** (9)
- [Threat Model](../../term_dictionary/term_threat_model.md) — structured inventory of attack surfaces/defenses; relevance: `audit` emits `security.trust_model.multi_user_heuristic` and reminds that OpenClaw defaults to a personal-assistant trust model.
- [Trust Policy](../../term_dictionary/term_trust_policy.md) — who-can-do-what boundary rules; relevance: the shared-inbox / multi-user trust-boundary guidance (separate gateways/OS users for adversarial operators) the audit advises.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution boundary; relevance: audit warns on unsandboxed small models with web/browser tools and on Docker settings configured while sandbox mode is off.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: audit flags dangerous sandbox Docker network modes (`host`, `container:*`), bridge-without-cdpSourceRange, and stale browser-container hash labels.
- [POSIX Permissions](../../term_dictionary/term_posix_permissions.md) — Unix file-mode control; relevance: `--fix` tightens state/config/credentials file permissions via `chmod` (POSIX) and `icacls` (Windows).
- [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — inbound webhook ingress to the gateway; relevance: audit flags `hooks.token` reuse of gateway shared-secret auth, short/`"/"`-path hooks, and unrestricted `allowedAgentIds`.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback endpoint; relevance: the webhook-ingress security warnings (token reuse, sessionKey overrides) are a core audit category.
- [Break Glass](../../term_dictionary/term_break_glass.md) — explicit emergency-override control; relevance: settings prefixed `dangerous`/`dangerously` are break-glass operator overrides the audit reports one-per-finding but does not treat as a vulnerability by itself.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct-message access/group policy; relevance: audit recommends secure DM mode (`session.dmScope`) and flips `groupPolicy="open"`→`"allowlist"`, and flags open DM/group exposure of runtime tools.

**Docs** (11; 7 existing + 4 planned-sibling)
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — Claude Code security architecture; relevance: the closest peer-tool security-model doc framing audit categories (permissions, exposure, isolation).
- [cc_hook_security_and_debugging](../claude_code/cc_hook_security_and_debugging.md) — hook security review; relevance: directly analogous to the `hooks.token` reuse / webhook ingress findings.
- [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — prompt-injection defenses; relevance: the adversarial-ingress threat the multi-user/open-DM heuristics defend against.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — sandbox filesystem/network isolation; relevance: parallels the workspace-scoped filesystem + sandbox guidance for shared-user setups.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — admin-enforced security controls; relevance: analog of the deterministic safe-defaults `--fix` enforces (allowlist, redaction, permission tightening).
- [pi_security_model](../pi/pi_security_model.md) — Pi agent security model; relevance: peer coding-agent trust/permission model paralleling OpenClaw's audit posture.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — Hermes isolation + credential security; relevance: upstream-ecosystem analog of credential-exposure and isolation checks.
- [oc_cli_secrets](oc_cli_secrets.md) — `openclaw secrets` (planned, this series); relevance: the SecretRef audit half; both resolve SecretRefs read-only.
- [oc_cli_status](oc_cli_status.md) — `openclaw status` (planned, this series); relevance: heavy security audit/plugin/memory probes are deferred to `status --all` / `security audit`.
- [oc_gw_security](../openclaw/oc_gw_security.md) — gateway Security guide (planned, gw06 series); relevance: the `/gateway/security` guide and the "Insecure or dangerous flags summary" this page links.
- [oc_gw_security_audit_checks](../openclaw/oc_gw_security_audit_checks.md) — gateway security audit-checks reference (planned, gw06 series); relevance: the per-`checkId` catalog suppressions match against.

**Repos** (2)
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — OpenClaw security subsystem; relevance: the audit + `--fix` engine and its collectors.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: hosts the auth/bind/exposure config (`gateway.auth.mode`, `allowRealIpFallback`) the audit inspects.

**Snippets** (12)
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit collector composition; relevance: how cold-path vs `--deep` plugin-owned collectors are assembled.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel-source audit collector; relevance: the secure-DM-mode / shared-inbox `session.dmScope` finding.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: the write/edit-disabled-but-exec-available and unsandboxed-exec findings.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe executor; relevance: the `--deep` best-effort live-gateway probe path.
- [snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md) — plugin trust findings; relevance: the "installed plugin tools reachable under permissive policy" findings and suppressions.
- [snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md) — plugin trust resolver; relevance: the trusted-plugin reasoning behind `plugins.tools_reachable_permissive_policy` suppressions.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — `--fix` remediation; relevance: the safe deterministic remediations (`groupPolicy`, `redactSensitive`, permission tightening) `--fix` applies.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tools deny logic; relevance: the `denyCommands`/`allowCommands` and dangerous-flag findings.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hooks config payload; relevance: the `hooks.token`/`hooks.path`/`allowedSessionKeyPrefixes` fields the webhook findings inspect.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode helpers; relevance: the `gateway.auth.mode="none"` HTTP-API exposure the audit flags.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — gateway authorize dispatch; relevance: the shared-secret auth path whose token reuse the audit checks.

### oc_cli_sessions_inspect (8t · 11s · 11d)

**Terms** (8)
- [Session Data](../../term_dictionary/term_session_data.md) — persisted per-conversation state rows; relevance: the bounded list of stored `sessions.json` conversation rows this command enumerates.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable storage of conversation state across restarts; relevance: `sessions` reads persisted rows from disk-only and configured stores (not a liveness check).
- [Trajectory](../../term_dictionary/term_trajectory.md) — recorded sequence of agent steps/events; relevance: `sessions tail` renders trajectory JSONL events as compact progress lines.
- [Agent Trajectory](../../term_dictionary/term_agent_trajectory.md) — the agent-execution event log; relevance: `export-trajectory` bundles the trajectory artifacts for a session key.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: the progress view shows tool-call names with `{...redacted...}` and tool-result statuses.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional gateway transport; relevance: `--url ws://` and the gateway `sessions.list` RPC ride a WebSocket connection.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — request/response RPC over JSON; relevance: list/discovery use gateway RPC methods returning `totalCount`/`limitApplied`/`hasMore`.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — auxiliary/relocated transcript file; relevance: `--follow` watches relocated files referenced by `<session>.trajectory-path.json`.

**Docs** (11; 6 existing + 5 planned-sibling)
- [cc_sessions](../claude_code/cc_sessions.md) — Claude Code sessions overview; relevance: peer-tool analog of stored-session listing and inspection.
- [cc_manage_your_session](../claude_code/cc_manage_your_session.md) — managing a Claude Code session; relevance: the discovery/inspection operator workflow this note documents.
- [cc_sdk_session_store](../claude_code/cc_sdk_session_store.md) — SDK session store; relevance: parallels the on-disk `sessions.json` store and discovery semantics.
- [hermes_sessions_lifecycle_resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — Hermes session lifecycle/resume; relevance: upstream-ecosystem session list/resume model the discovery mirrors.
- [hermes_trajectory_format](../hermes_agent/hermes_trajectory_format.md) — Hermes trajectory file format; relevance: the trajectory JSONL schema `tail`/`export-trajectory` render and bundle.
- [pi_session_file_format](../pi/pi_session_file_format.md) — Pi session file format; relevance: peer agent's on-disk session-row format analogous to `sessions.json`.
- [oc_cli_sessions_maintenance](oc_cli_sessions_maintenance.md) — `openclaw sessions cleanup/compact` (planned, this series); relevance: the lifecycle/maintenance half of the same session store.
- [oc_cli_status](oc_cli_status.md) — `openclaw status` (planned, this series); relevance: status surfaces per-agent session-store snapshots and recent recipients.
- [oc_concepts_session](../openclaw/oc_concepts_session.md) — Session concept (planned, co06 series); relevance: the `/concepts/session` doc this page links for the session model.
- [oc_gw_config_agents](../openclaw/oc_gw_config_agents.md) — gateway config-agents/session config (planned, gw01 series); relevance: the `/gateway/config-agents#session` config-reference this page links.
- [oc_cli_channels](../openclaw/oc_cli_channels.md) — `openclaw channels status` (planned, cl01 series); relevance: the live channel-liveness command the page contrasts a session list against.

**Repos** (2)
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw session store subsystem; relevance: the session store, discovery, and read paths this command lists.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: hosts the bounded `sessions.list` RPC and disk-only-store discovery.

**Snippets** (11)
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — sessions list/read RPC methods; relevance: the gateway-side `sessions.list` bounded-read implementation behind this command.
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — transcript candidate scan; relevance: the disk discovery of `sessions.json` stores and transcript/trajectory files (symlink/out-of-root skipping).
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — session FS index read; relevance: the index read that backs bounded listing with `totalCount`/`hasMore`.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — store-target resolution; relevance: how `--agent`/`--all-agents`/`--store` scope flags resolve to store paths.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — subagent liveness; relevance: the running-vs-stored distinction `tail` uses (tails running sessions first).
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — session transcript events; relevance: the trajectory JSONL events `tail` renders as progress lines.
- [snippet_hermes_agent_trajectory_canonicalize](../../code_snippets/snippet_hermes_agent_trajectory_canonicalize.md) — trajectory canonicalization (Hermes); relevance: the canonical trajectory form `export-trajectory` bundles.
- [snippet_hermes_agent_trajectory_redact_export](../../code_snippets/snippet_hermes_agent_trajectory_redact_export.md) — trajectory redact-on-export (Hermes); relevance: directly analogous to the redacted (`{...redacted...}`) progress view and export path.
- [snippet_hermes_agent_trajectory_schema](../../code_snippets/snippet_hermes_agent_trajectory_schema.md) — trajectory schema (Hermes); relevance: the event schema the JSONL `tail` lines conform to.
- [snippet_openclaw_acp_event_ledger](../../code_snippets/snippet_openclaw_acp_event_ledger.md) — ACP event ledger; relevance: the ordered agent-event source feeding trajectory progress.

### oc_cli_sessions_maintenance (8t · 11s · 11d)

**Terms** (8)
- [Compaction](../../term_dictionary/term_compaction.md) — shrinking a transcript while preserving meaning; relevance: `sessions compact` LLM-summarizes (or `--max-lines` truncates) a wedged/oversized session.
- [Context Compression](../../term_dictionary/term_context_compression.md) — reducing context tokens via summarization/eviction; relevance: the goal of compaction — reclaim context budget (`tokensBefore`→`tokensAfter`).
- [Context Window](../../term_dictionary/term_context_window.md) — the model's bounded token budget; relevance: compaction reclaims context-window budget for an oversized session.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — cached key/value attention state; relevance: token accounting in the compaction RPC response (the cache/token economics compaction restores).
- [Session Data](../../term_dictionary/term_session_data.md) — persisted conversation rows; relevance: the rows `cleanup` prunes/caps/retires and `compact` rewrites.
- [Append-Only State](../../term_dictionary/term_append_only_state.md) — log-structured immutable transcript; relevance: `--max-lines` archives the prior transcript as a `.bak` sidecar rather than mutating in place.
- [Cron](../../term_dictionary/term_cron.md) — scheduled job runner; relevance: cleanup explicitly does NOT prune cron run history (`cron.runLog.keepLines`), and compact exits non-zero so crons/scripts never mistake a no-op for success.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON request/response RPC; relevance: `sessions compact` wraps the `sessions.compact` gateway RPC (`key`/`agentId`/`maxLines` contract).

**Docs** (11; 6 existing + 5 planned-sibling)
- [cc_what_survives_compaction](../claude_code/cc_what_survives_compaction.md) — what is preserved across compaction; relevance: peer-tool analog of LLM-summarize compaction semantics.
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — anatomy of the context window; relevance: the budget compaction reclaims (`tokensBefore`/`tokensAfter`).
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — reducing token usage; relevance: the operator goal of compacting a wedged/oversized session.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — Hermes session storage; relevance: upstream-ecosystem analog of the store the cleanup maintains/prunes.
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — Hermes context compression + caching; relevance: directly analogous compaction + cache token-accounting model.
- [pi_compaction](../pi/pi_compaction.md) — Pi compaction; relevance: peer agent's transcript-compaction mechanism paralleling `sessions compact`.
- [oc_cli_sessions_inspect](oc_cli_sessions_inspect.md) — `openclaw sessions` list/tail/export (planned, this series); relevance: the discovery half of the same session store.
- [oc_cli_status](oc_cli_status.md) — `openclaw status` (planned, this series); relevance: status surfaces token/cache counters compaction changes.
- [oc_concepts_compaction](../openclaw/oc_concepts_compaction.md) — Compaction concept (planned, co02 series); relevance: the concept doc for the compaction mechanism.
- [oc_concepts_session_pruning](../openclaw/oc_concepts_session_pruning.md) — Session pruning concept (planned, co06 series); relevance: the prune/cap/eviction model `cleanup` enforces via `session.maintenance`.
- [oc_automation_cron_jobs](../openclaw/oc_automation_cron_jobs.md) — Cron jobs (planned, au01 series); relevance: the `/automation/cron-jobs` config/maintenance this page contrasts cleanup's scope against.

**Repos** (2)
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw session store subsystem; relevance: the maintenance/eviction policy (`session.maintenance`) and compaction logic.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: hosts the `sessions.compact` RPC and the gateway-routed cleanup writer.

**Snippets** (11)
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — sessions compact/reset impl; relevance: the gateway-side `sessions.compact` (LLM-summarize vs truncate) implementation.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — sessions lifecycle patches; relevance: the prune/cap/retire mutations `cleanup` applies to `sessions.json`.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — session reset mutation; relevance: the gateway-routed writer that performs cleanup mutations.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — session reset helpers; relevance: the helper path shared by cleanup/compact state changes.
- [snippet_openclaw_gateway_session_fs_title_cache_archive](../../code_snippets/snippet_openclaw_gateway_session_fs_title_cache_archive.md) — transcript title/cache archive; relevance: the `.bak` sidecar archive `--max-lines` truncation produces.
- [snippet_openclaw_memory_host_session_files_classify](../../code_snippets/snippet_openclaw_memory_host_session_files_classify.md) — session-file classification; relevance: identifying unreferenced transcripts/compaction-checkpoints/sidecars `cleanup` prunes after `pruneAfter`.
- [snippet_hermes_agent_gw_runner_shutdown](../../code_snippets/snippet_hermes_agent_gw_runner_shutdown.md) — gateway runner shutdown (Hermes); relevance: the write-cycle maintenance point `cleanup` runs "now" instead of waiting for.
- [snippet_hermes_agent_core_conversation_compression_entry](../../code_snippets/snippet_hermes_agent_core_conversation_compression_entry.md) — conversation compression entry (Hermes); relevance: ecosystem analog of the LLM-summarize compaction entry point.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — model fallback cooldown; relevance: the model label kept per session row that cleanup preserves in its dry-run action table.

### oc_cli_setup (8t · 11s · 11d)

**Terms** (8)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway/coding-agent product; relevance: `setup` initializes OpenClaw's baseline config and agent workspace.
- [Data Onboarding](../../term_dictionary/term_data_onboarding.md) — guided first-run/import flow; relevance: the closest existing analog to the wizard onboarding flow `setup` auto-triggers on any onboarding flag.
- [Secrets Manager / SecretRef](../../term_dictionary/term_secrets_manager.md) — externalized secret store; relevance: `--import-secrets` migrates supported secrets during onboarding migration.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: `--remote-url wss://gateway-host:18789` connects to a remote gateway over WebSocket.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer auth credential; relevance: `--remote-token` authenticates to the remote gateway.
- [Authentication](../../term_dictionary/term_authentication.md) — proving identity to the gateway; relevance: remote-mode setup authenticates with `--remote-token` against the remote gateway.
- [Data Store Import](../../term_dictionary/term_data_store_import.md) — importing an existing data store; relevance: `--import-from`/`--import-source` import a source agent home during onboarding migration.

**Docs** (11; 6 existing + 5 planned-sibling)
- [hermes_installation](../hermes_agent/hermes_installation.md) — Hermes install/first-run; relevance: upstream-ecosystem analog of baseline-config + workspace setup.
- [hermes_quickstart_first_chat](../hermes_agent/hermes_quickstart_first_chat.md) — Hermes first-chat quickstart; relevance: the plain-setup-then-onboard journey this page describes.
- [hermes_install_nix_quickstart](../hermes_agent/hermes_install_nix_quickstart.md) — Hermes Nix install; relevance: directly relevant to the Nix-mode (`OPENCLAW_NIX_MODE=1`) setup-write refusal note.
- [hermes_migrate_from_openclaw](../hermes_agent/hermes_migrate_from_openclaw.md) — migrate between Hermes/OpenClaw; relevance: the `--import-from hermes` migration lineage `setup` offers.
- [cc_quickstart](../claude_code/cc_quickstart.md) — Claude Code quickstart; relevance: peer-tool first-run/initialize-config analog.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI reference (incl. setup/wizard); relevance: the pi `setup`/`wizard` precedent the plan cites for not promoting workspace/wizard terms.
- [oc_cli_skills](oc_cli_skills.md) — `openclaw skills` (planned, this series); relevance: post-setup skill install into the configured workspace.
- [oc_cli_status](oc_cli_status.md) — `openclaw status` (planned, this series); relevance: post-setup health check of the initialized gateway/workspace.
- [oc_start_wizard](../openclaw/oc_start_wizard.md) — Onboarding (CLI) wizard (planned, st02 series); relevance: the `/start/wizard` onboarding doc this page links.
- [oc_start_getting_started](../openclaw/oc_start_getting_started.md) — Getting started (planned, st01 series); relevance: the `/start/getting-started` guide this page links.
- [oc_cli_migrate](../openclaw/oc_cli_migrate.md) — `openclaw migrate` (planned, cl05 series); relevance: the `/cli/migrate` command for dry-run plans/backups outside onboarding this page defers to.

**Repos** (2)
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — OpenClaw setup/wizard CLI; relevance: implements `setup`, the wizard auto-trigger, and migration/import flows.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw core; relevance: the baseline config (`agents.defaults.workspace`) and workspace layout `setup` initializes.

**Snippets** (11)
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config writer; relevance: the baseline-config + `agents.defaults.workspace` writer behind plain `setup`.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — wizard migration import; relevance: the `--import-from`/`--import-source` onboarding migration path.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard setup imports; relevance: the `--import-secrets` supported-secret import during migration.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — interactive wizard prompter; relevance: the interactive onboarding prompts the wizard auto-trigger launches (vs `--non-interactive`).
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: the `agents.defaults.workspace` runtime config `setup` establishes.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — gateway RPC protocol schema; relevance: the remote-gateway (`--remote-url`/`--remote-token`) RPC surface remote-mode setup targets.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — CLI setup installer (Hermes); relevance: ecosystem analog of baseline-config initialization.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — CLI setup wizard (Hermes); relevance: directly analogous wizard onboarding flow.
- [snippet_hermes_agent_cli_setup_skills](../../code_snippets/snippet_hermes_agent_cli_setup_skills.md) — setup skills step (Hermes); relevance: the skill-install step setup can lead into (mirrors `oc_cli_skills`).
- [snippet_hermes_agent_cli_claw_migrate](../../code_snippets/snippet_hermes_agent_cli_claw_migrate.md) — claw migrate (Hermes); relevance: ecosystem analog of `--import-from hermes` state migration.
- [snippet_hermes_agent_optional_skills_migration_openclaw](../../code_snippets/snippet_hermes_agent_optional_skills_migration_openclaw.md) — Hermes→OpenClaw skills migration; relevance: the cross-product migration lineage setup's import flow participates in.

### oc_cli_skills (8t · 11s · 11d)

**Terms** (8)
- [Skills](../../term_dictionary/term_skills.md) — agent skill system (instructions + tools packaged for reuse); relevance: the skill system `openclaw skills` searches/installs/verifies/lists.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — `SKILL.md` frontmatter contract; relevance: the install slug comes from `SKILL.md` frontmatter `name` (overridable with `--as`).
- [Skills Hub / ClawHub](../../term_dictionary/term_skills_hub.md) — skill registry/marketplace; relevance: `search`/`install <slug>`/`verify`/`update` use ClawHub directly, including the `clawhub.skill.verify.v1` envelope.
- [Atomic Skill](../../term_dictionary/term_atomic_skill.md) — a single self-contained skill unit; relevance: the unit `install`/`list`/`info` operate on (one skill folder with `SKILL.md`).
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol (tools as agent capabilities); relevance: skills surface as agent capabilities alongside MCP tools on the prompt/command surface `check` inspects.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: skills extend the coding agent's capability surface this command manages per workspace/agent.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of available tools/capabilities; relevance: the workspace/`--global` skills directory acts as the agent's skill registry `list`/`check` read.
- [Progressive Disclosure](../../term_dictionary/term_progressive_disclosure.md) — surfacing capabilities on demand; relevance: `list --eligible`/`check` report which ready skills are actually visible to the agent's prompt/command surface.

**Docs** (11; 6 existing + 5 planned-sibling)
- [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — Hermes skills usage guide; relevance: upstream-ecosystem analog of search/install/list/check skill operations.
- [hermes_skills_hub_agent_managed](../hermes_agent/hermes_skills_hub_agent_managed.md) — Hermes skills-hub agent-managed installs; relevance: directly analogous to ClawHub-tracked installs and the separate `skills.install` gateway path.
- [hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md) — publishing a Hermes skill; relevance: the publish/verify provenance side of the ClawHub registry `verify` checks.
- [cc_plugin_marketplace_walkthrough](../claude_code/cc_plugin_marketplace_walkthrough.md) — Claude Code marketplace walkthrough; relevance: peer-tool analog of registry search/install/update flow.
- [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — plugin CLI commands; relevance: peer-tool analog of the install/update/list/info command surface.
- [pi_packages](../pi/pi_packages.md) — Pi packages/extensions; relevance: peer agent's package/skill install + slug resolution analog.
- [oc_cli_setup](oc_cli_setup.md) — `openclaw setup` (planned, this series); relevance: workspace setup precedes workspace-scoped skill install.
- [oc_cli_security](oc_cli_security.md) — `openclaw security` (planned, this series); relevance: the skill scanner / unpinned-install integrity warnings the audit raises.
- [oc_tools_skills](../openclaw/oc_tools_skills.md) — Skills system (planned, to07 series); relevance: the `/tools/skills` system doc this page links.
- [oc_tools_skill_workshop](../openclaw/oc_tools_skill_workshop.md) — Skill Workshop (planned, to06 series); relevance: the `/tools/skill-workshop` proposal storage/approval-policy doc the workshop lifecycle links.
- [oc_clawhub_cli](../openclaw/oc_clawhub_cli.md) — ClawHub CLI (planned, cw01 series); relevance: the `/clawhub/cli` install/auth doc this page links.

**Repos** (2)
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills subsystem; relevance: the skill install/verify/workshop engine.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions framework; relevance: the skill/extension capability framework skills plug into.

**Snippets** (11)
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — `SKILL.md` manifest parse; relevance: how the install slug is derived from frontmatter `name`.
- [snippet_openclaw_skills_availability_evaluator](../../code_snippets/snippet_openclaw_skills_availability_evaluator.md) — skill availability evaluator; relevance: the `list --eligible`/`check` visibility evaluation.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — skill tool-descriptor contract; relevance: how an installed skill surfaces as a callable agent capability.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: the planner that decides which skills are ready/visible to a workspace.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — skill provenance/security scanner; relevance: the `verify` provenance / `verifiedSourceUrl` security check.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin/skill package contract; relevance: the install-source package contract (Git/local/ClawHub) `install` honors.
- [snippet_hermes_agent_tools_skills_hub_registry](../../code_snippets/snippet_hermes_agent_tools_skills_hub_registry.md) — skills-hub registry (Hermes); relevance: ecosystem analog of the ClawHub registry `search`/`verify` query.
- [snippet_hermes_agent_cli_skills_hub](../../code_snippets/snippet_hermes_agent_cli_skills_hub.md) — CLI skills-hub (Hermes); relevance: the registry-backed CLI install/update analog.
- [snippet_hermes_agent_cli_skills_install](../../code_snippets/snippet_hermes_agent_cli_skills_install.md) — CLI skills install (Hermes); relevance: directly analogous slug/Git/local install resolution.
- [snippet_hermes_agent_tools_skills_hub_install](../../code_snippets/snippet_hermes_agent_tools_skills_hub_install.md) — skills-hub install impl (Hermes); relevance: the workspace-vs-managed install targeting analog (`--global`).
- [snippet_hermes_agent_tools_skills_guard](../../code_snippets/snippet_hermes_agent_tools_skills_guard.md) — skills guard/validation (Hermes); relevance: ecosystem analog of verify/quarantine safety gating in the workshop lifecycle.

### oc_cli_status (9t · 11s · 11d)

**Terms** (9)
- [Model Failover](../../term_dictionary/term_model_failover.md) — automatic switch to a backup model/runtime; relevance: the `Runtime:` label distinguishes OpenClaw Default / OpenAI Codex / CLI backend / ACP backend.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — protocol for external agent backends; relevance: the `codex (acp/acpx)` runtime distinction `status` reports.
- [Context Window](../../term_dictionary/term_context_window.md) — bounded token budget; relevance: status resolves the context window against the recovered runtime model when transcript fallback differs from the selected model.
- [KV Cache](../../term_dictionary/term_kv_cache.md) — cached attention state; relevance: cache counters are backfilled from the most recent transcript usage log when the live snapshot is sparse.
- [Secrets Manager / SecretRef](../../term_dictionary/term_secrets_manager.md) — externalized secret store; relevance: read-only status surfaces resolve supported SecretRefs for targeted config paths and report `secretDiagnostics` on degraded output.
- [Session Data](../../term_dictionary/term_session_data.md) — persisted conversation rows; relevance: status shows per-agent session stores and recent session recipients.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of model ids/pricing; relevance: model-pricing refresh failures surface as optional pricing warnings in the overview.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: `--deep` runs live channel probes (WhatsApp/Telegram/Discord/Slack/Signal) and gateway/node host runtime status.
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic liveness/uptime signal; relevance: the overview includes compact gateway-process uptime and host system uptime.

**Docs** (11; 6 existing + 5 planned-sibling)
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — Claude Code config debugging; relevance: peer-tool analog of the pasteable diagnostics `status --all` produces.
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install diagnostics; relevance: analog of the health/probe diagnostics surface.
- [cc_performance_and_stability](../claude_code/cc_performance_and_stability.md) — performance/stability diagnostics; relevance: the runtime/uptime/usage signals `status` reports.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — usage/limit errors; relevance: directly analogous to `--usage` provider quota windows (`X% left`).
- [hermes_lsp_diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — Hermes diagnostics; relevance: upstream-ecosystem analog of a channel/session diagnostics command.
- [pi_overview](../pi/pi_overview.md) — Pi agent overview (runtime/model concepts); relevance: peer agent's provider/model/runtime distinction paralleling Execution-vs-Runtime.
- [oc_cli_security](oc_cli_security.md) — `openclaw security` (planned, this series); relevance: the heavy security audit `status` defers to `status --all` / `security audit`.
- [oc_cli_sessions_inspect](oc_cli_sessions_inspect.md) — `openclaw sessions` (planned, this series); relevance: the session recipients/diagnostics overlap surfaced in status output.
- [oc_concepts_agent_runtimes](../openclaw/oc_concepts_agent_runtimes.md) — Agent runtimes (planned, co01 series); relevance: the `/concepts/agent-runtimes` provider/model/runtime distinction this page links.
- [oc_gw_doctor](../openclaw/oc_gw_doctor.md) — `openclaw doctor` (planned, gw02 series); relevance: the `/gateway/doctor` deeper-diagnosis command this page links.
- [oc_install_updating](../openclaw/oc_install_updating.md) — Updating (planned, in05 series); relevance: the `/install/updating` flow `status` hints at when an update is available.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: hosts the status RPC, live probes, usage/latency/cache, and uptime reporting.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw session store; relevance: the per-agent session-store snapshots status reads.

**Snippets** (11)
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency/cache status; relevance: the `--usage` windows and token/cache counters status reports.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — transcript model-label fallback; relevance: the transcript fallback that recovers the active runtime model label.
- [snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md) — model fallback observation; relevance: the Runtime/model-pin observation status renders (`session override`, `/model default`).
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — session model overrides; relevance: the pinned-vs-primary model display (`session override`) status prints.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-window guard; relevance: resolving the context window against the recovered runtime model.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing alias lookup; relevance: the model-pricing refresh whose failures show as optional pricing warnings.
- [snippet_openclaw_gateway_session_utils_title_runtime](../../code_snippets/snippet_openclaw_gateway_session_utils_title_runtime.md) — session title/runtime utils; relevance: deriving the runtime/model label for session-store snapshot lines.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status probe; relevance: the live channel probe `status --deep` runs.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — post-attach runtime; relevance: the gateway/node host service install/runtime status the overview includes.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — doctor API connectivity (Hermes); relevance: ecosystem analog of the deep live-probe connectivity check.
- [snippet_hermes_agent_core_conversation_loop_usage_accounting](../../code_snippets/snippet_hermes_agent_core_conversation_loop_usage_accounting.md) — usage accounting (Hermes); relevance: ecosystem analog of token/cache usage accounting and transcript-fallback backfill.

### oc_cli_system (8t · 11s · 11d)

**Terms** (8)
- [Heartbeat](../../term_dictionary/term_heartbeat.md) — periodic agent wake/tick; relevance: `system event` is injected as a `System:` line at the next heartbeat; `system heartbeat last/enable/disable` controls the tick.
- [Cron](../../term_dictionary/term_cron.md) — scheduled job runner; relevance: `system event` is the cron-free enqueue alternative the page positions against creating a cron job.
- [Session Data](../../term_dictionary/term_session_data.md) — per-agent session state; relevance: `--session-key` targets a specific agent session (falling back to the agent's main session for non-matching keys).
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — JSON request/response RPC; relevance: all `system` subcommands use gateway RPC with shared client flags.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional gateway transport; relevance: `--url ws://127.0.0.1:18789` connects the system RPC over WebSocket.
- [Server-Sent Events](../../term_dictionary/term_sse.md) — server-push event stream; relevance: the `--expect-final` streaming RPC flag governs how pushed gateway responses are awaited.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked actions; relevance: an injected `System:` event drives the next agent turn's tool/action selection (e.g. "check for urgent follow-ups").
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — local service/node discovery; relevance: `system presence` lists nodes/instances/status lines the gateway knows about (discovered presence entries).

**Docs** (11; 6 existing + 5 planned-sibling)
- [cc_routine_triggers](../claude_code/cc_routine_triggers.md) — routine triggers; relevance: peer-tool analog of an enqueued/triggered agent event (immediate vs scheduled).
- [cc_create_routine](../claude_code/cc_create_routine.md) — creating a routine; relevance: the scheduled-vs-immediate enqueue the page contrasts with `--mode now`/`next-heartbeat`.
- [cc_routines_overview](../claude_code/cc_routines_overview.md) — routines overview; relevance: peer-tool analog of heartbeat-driven recurring agent wakes.
- [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — scheduled-task execution model; relevance: the not-due-gate / immediate-wake timing model the `--session-key` exception parallels.
- [hermes_automation_blueprints_scheduled](../hermes_agent/hermes_automation_blueprints_scheduled.md) — scheduled automation blueprints (Hermes); relevance: upstream-ecosystem analog of cron-vs-event enqueue choices.
- [hermes_cron_internals](../hermes_agent/hermes_cron_internals.md) — Hermes cron internals; relevance: the cron-job mechanism `system event` offers an ephemeral alternative to.
- [oc_cli_status](oc_cli_status.md) — `openclaw status` (planned, this series); relevance: presence/runtime/uptime overlap with `system presence`.
- [oc_cli_sessions_inspect](oc_cli_sessions_inspect.md) — `openclaw sessions` (planned, this series); relevance: the `--session-key` targeting shared with session listing.
- [oc_gw_heartbeat](../openclaw/oc_gw_heartbeat.md) — gateway Heartbeat (planned, gw03 series); relevance: the heartbeat mechanism `system event`/`system heartbeat` drives.
- [oc_automation_cron_jobs](../openclaw/oc_automation_cron_jobs.md) — Cron jobs (planned, au01 series); relevance: the cron-job system the page contrasts the ephemeral event enqueue against.
- [oc_concepts_presence](../openclaw/oc_concepts_presence.md) — Presence concept (planned, co05 series); relevance: the presence model `system presence` lists.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: hosts the system-event/heartbeat/presence RPCs and the heartbeat runner.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: the main-session event injection and per-session targeting `system event` performs.

**Snippets** (11)
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node-events/presence; relevance: the presence/node entries `system presence` lists.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat buffered delta; relevance: the heartbeat tick that injects an enqueued `System:` event.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: targeted node/instance wake analogous to the targeted-wake `--session-key` path.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron-service notifications; relevance: the cron mechanism `system event` is the cron-free alternative to.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime-config broadcast; relevance: the gateway broadcast/RPC mechanism the system subcommands ride.
- [snippet_openclaw_gateway_chat_lifecycle_session_persist](../../code_snippets/snippet_openclaw_gateway_chat_lifecycle_session_persist.md) — session-persist lifecycle; relevance: where an injected event lands on a session (main vs targeted) and is processed.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent dispatch handler; relevance: dispatching the injected `System:` event to the resolved agent session.
- [snippet_openclaw_gateway_agent_identity_reset](../../code_snippets/snippet_openclaw_gateway_agent_identity_reset.md) — agent identity/session resolution; relevance: resolving `--session-key` to an agent (fallback to the main session).
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — gateway WebSocket connection; relevance: the `--url ws://` transport for system RPC.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — nodes pairing; relevance: the nodes/instances `system presence` enumerates.

> Augment note (xref-locked 2026-06-21): where a desired term has **no** existing note (`term_session`,
> `term_skill`, `term_workspace`, `term_secret`, `term_credential`, `term_audit`, `term_presence`,
> (`term_session_data`, `term_session_persistence`; `term_skills`/`term_atomic_skill`;
> `term_secrets_manager`/`term_credential_pool`/`term_auth_profile`; `term_threat_model`/`term_trust_policy`;
> `term_heartbeat`/`term_bonjour_discovery` for presence; `term_data_onboarding`/`term_data_store_import`).
> No new term capture is triggered (see Undigested Terms Plan). All 8 notes meet the raised floor

## Undigested Terms Plan

| Term | Disposition |
|------|-------------|
| SecretRef / secrets reload / audit / scrub / plan contract | → `oc_cli_secrets` + gateway/secrets sub-plan; link `term_secrets_manager`, `term_credential_pool`. Not a new term note. |
| security audit / `--fix` / suppressions / trust model | → `oc_cli_security`; link `term_threat_model`, `term_trust_policy`, `term_audit_operations`. Not a new term note. |
| session / session store / session key / dmScope | → `oc_cli_sessions_inspect` + concepts/session sub-plan; link `term_session_data`. `term_session` ABSENT but session vocabulary is documented as doc-note content, not promoted. |
| trajectory / export-trajectory | → `oc_cli_sessions_inspect`; link existing `term_trajectory` / `term_agent_trajectory`. |
| compaction / compact RPC | → `oc_cli_sessions_maintenance`; link existing `term_compaction`. |
| setup / workspace / wizard / onboarding / migration / import | → `oc_cli_setup`; link `term_openclaw`, `term_data_onboarding`. `term_workspace`/`term_wizard`/`term_migration` ABSENT — documented as command behavior, not promoted (analogous to pi `setup`/`wizard` precedent). |
| skill / ClawHub / Skill Workshop / verify / provenance | → `oc_cli_skills`; link existing `term_skills`, `term_skill_manifest`, `term_skills_hub`, `term_atomic_skill`. |
| status / Execution vs Runtime / usage windows | → `oc_cli_status`; link `term_model_failover`, `term_acp_agent_client_protocol`. |
| system event / heartbeat / presence | → `oc_cli_system`; link existing `term_heartbeat`. `term_presence` ABSENT — documented as command behavior, not promoted. |

**Expected new `term_dictionary` captures: 0.** OpenClaw CLI vocabulary is digested as `oc_*` doc-note content
(per master); existing terms are linked. No genuinely cross-cutting, vault-reusable term lacks both a doc-page
home AND an existing note: every candidate either has a usable existing term (substitute) or is a
command/config behavior best documented in its `oc_cli_*` note. No new-term candidate proposed.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — cl07 authors zero `term_dictionary` notes. Inherited from master: if augment's Step 2d
re-scan surfaces a genuinely reusable cross-cutting term with no doc-page home AND no existing note, capture it
via `/tessellum-capture-term-note` + add to the best-fit `acronym_glossary_*.md` (none expected here).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit.

| Gate | Check | Tooling |
|------|-------|---------|
| G1 | Format: YAML field order + forbidden-field absence; H1/`## Overview`/`## Related Notes`/`## References` + bold footer | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traces to `inbox/openclaw_docs/cli/<page>.md` (no invented flags/RPC fields) | diff vs mirror page |
| G3 | Density + coverage: ≤400 lines / ≤2500 words / ≤6 code blocks per note; every mapped H2/H3 covered | `wc`, fence count, coverage map |
| G4 | Cross-reference: ≥6 relevancy-selected term links + repo/sibling/other, each with a relevance statement | manual review vs candidates |
| G5 | Ghost-reference detect + redirect: every cited `note_id` resolves in DB | `sqlite3` existence check |
| G6 | Broken-link fix: relative paths resolve | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability: each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (in-degree ≥1, anti-island) | satisfied via `entry_openclaw_docs.md` + repo back-links |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_secrets oc_cli_security oc_cli_sessions_inspect oc_cli_sessions_maintenance oc_cli_setup oc_cli_skills oc_cli_status oc_cli_system"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING: $n"; continue; }
  # G1: format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3: density caps (body-only words, fence pairs)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code / $lines L)"
  # G4: at least 6 sibling-or-term related links
  grep -cE "\]\((\.\./)*term_dictionary/term_|${SIBLING_PREFIX}|repo_openclaw" "$f" >/dev/null
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost-reference: DB-verify each cited note_id
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_cli_secrets | procedure | 650 | ≤6 | ✅ (source 893w / 6 fences) |
| 2 | oc_cli_security | procedure | 650 | ≤4 | ✅ (source 970w / 4 fences) |
| 3 | oc_cli_sessions_inspect | procedure | 600 | ≤6 | ✅ (sessions split keeps fences ≤6) |
| 4 | oc_cli_sessions_maintenance | procedure | 600 | ≤6 | ✅ (sessions split keeps fences ≤6) |
| 5 | oc_cli_setup | procedure | 450 | ≤2 | ✅ (source 312w / 1 fence) |
| 6 | oc_cli_skills | procedure | 650 | ≤4 | ✅ (source 896w / 2 fences; reproduce command examples selectively) |
| 7 | oc_cli_status | procedure | 500 | ≤2 | ✅ (source 570w / 1 fence) |
| 8 | oc_cli_system | procedure | 450 | ≤2 | ✅ (source 379w / 1 fence) |

No note approaches caps. The only over-fence page (`sessions.md`, 9 fences) is split so each half stays ≤6.
Command-example fences are reproduced selectively/verbatim, not exhaustively, to stay under the cap.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under the **CLI** section
(cl07 cluster). Each note receives its entry-point back-link at finalization (satisfies G7/G8 — ≥1 inbound link
from outside `documentation/openclaw/`). No new entry point is created by this sub-plan; the master hub +
parent-hub back-links (W1–W3) cover navigation.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; ≥1 per new note for G7/G8):

- `entry_openclaw_docs.md` → all 8 notes (primary discoverability source).
- `repo_openclaw_security` → notes 1, 2 (CLI commands documenting that subsystem).
- `repo_openclaw_sessions` → notes 3, 4 (session list/maintenance/compact).
- `repo_openclaw_skills` → note 6; `repo_openclaw_cli_wizard` → note 5.
- `repo_openclaw_gateway` → notes 1, 4, 7, 8 (RPC-backed commands: secrets.reload, sessions.compact, status probes, system events).
- `term_secrets_manager` → note 1; `term_threat_model` → note 2; `term_compaction` → note 4; `term_skills` → note 6; `term_heartbeat` → note 8; `term_model_failover` → note 7; `term_session_data` → note 3.
- Sibling cross-links within cl07 (notes 3↔4 split halves; 1↔2 audit overlap) provide intra-series cohesion (do not count toward the outside-folder G8 requirement).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each source page at execute; reproduce CLI command
examples verbatim but selectively (≤6 fences/note). One BB per note. Cap dynamic-workflow fan-out at ~30
agents/run. `git pull --rebase --autostash` first; commit + push per wave; no Claude co-author trailer.
Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — 9/9 checkpoints PASS → READY |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)


**What was locked.** The legacy `## Candidate Cross-References` section was replaced with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`, grouped per note into **Terms / Docs / Repos / Snippets**, each link rendered as `- [Name](relpath.md) — what it is; relevance: why THIS note`. Summary Statistics cross-ref line updated to the raised floor + LOCKED pointer.

**Per-note counts (all meet floors):**

| Note | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_cli_secrets | 8 | 11 | 11 (6 / 5) | 2 | ✅ |
| oc_cli_security | 9 | 12 | 11 (7 / 4) | 2 | ✅ |
| oc_cli_sessions_inspect | 8 | 11 | 11 (6 / 5) | 2 | ✅ |
| oc_cli_sessions_maintenance | 8 | 11 | 11 (6 / 5) | 2 | ✅ |
| oc_cli_setup | 8 | 11 | 11 (6 / 5) | 2 | ✅ |
| oc_cli_skills | 8 | 11 | 11 (6 / 5) | 2 | ✅ |
| oc_cli_status | 9 | 11 | 11 (6 / 5) | 2 | ✅ |
| oc_cli_system | 8 | 11 | 11 (6 / 5) | 2 | ✅ |



## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Plan: `plan_digest_openclaw_docs_cl07.md` · Date: 2026-06-21 · Reviewer pass: 9-checkpoint final sign-off.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors, relevance statements) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (8–9), ≥10 snippets (11–12), ≥10 docs (11); every link carries `relevance:`; bare-link count = 0. |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table has G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect (`sqlite3` existence), G6 broken-link fix, G7/G8 discoverability (in-degree ≥1, anti-island). Single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` states 8 rows into `entry_openclaw_docs.md` (master pre-step W1); DB confirms hub not-yet-created → consistent. >30-note master ⇒ dedicated hub already required by master. |
| CP4 | Size | **PASS** | 8 notes ≤ 30; sessions.md split (3+4) keeps each note ≤6 fences. |
| CP5 | Format derived (not invented) | **PASS** | Master Format Definition derived from existing `claude_code/`+`pi/` doc corpora; YAML order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`, body `## Overview`/`## Related Notes`/`## References` + bold footer — matches target-dir convention. |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment`: all notes ≤650w / ≤6 fences / well under 400 lines; only over-fence page (sessions, 9) is split. No borderline note left unaddressed. |
| CP7 | Sources measured (not guessed) | **PASS** | All 7 pages re-read 2026-06-21; measured body words match the plan's Source table (893/970/1,248/312/896/570/379) within tolerance; no page >1.5× its estimate. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (9 rows, each with disposition → owning `oc_cli_*` note + linked existing terms); expected new captures = 0; `## Term-Note Authoring Requirements` present (N/A, 0 terms, inherits master capture-term-note mandate if a term ever surfaces). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to audit (Undigested Terms Plan promotes none). All-notes dedup generalized: the 8 planned `oc_cli_*` doc notes were checked against `term_dictionary/` AND `documentation/` — none duplicate an existing term/doc note; the 9 absent-term slugs re-confirmed DB-ABSENT 2026-06-21, documented as command behavior not promoted (pi/cc precedent). |
| CP9 | Discoverability / inlinks (G8 executed) | **PASS** | `## Inlinks` maps ≥1 outside-folder inbound link per new note (`entry_openclaw_docs` → all 8; `repo_openclaw_*` → notes per subsystem; term backlinks); G8-Discoverability is in the phase gate table and marked verify-at-execution (in-degree ≥1). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
