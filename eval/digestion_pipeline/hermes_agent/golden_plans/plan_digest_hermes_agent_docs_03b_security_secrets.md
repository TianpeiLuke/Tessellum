---
title: Hermes Agent Docs Digestion — Sub-Plan 03b — Security, Secrets & Checkpoints
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/
pages:
  - user-guide/security.md
  - user-guide/checkpoints-and-rollback.md
  - user-guide/secrets/bitwarden.md
  - user-guide/secrets/index.md
  - user-guide/managed-scope.md
---

# Sub-Plan 03b: Security, Secrets & Checkpoints

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Part **b** of the
> SP03 deploy/security split (SP03a = Docker/Windows/Desktop/Worktrees deployment; SP03b = this file).
> Inherits shared Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP03b's note
> filenames/BBs/coverage are defined.

## Scope

The security + secrets + filesystem-safety surface of Hermes Agent: the defense-in-depth security model
(dangerous-command approval, YOLO + hardline blocklist, Tirith pre-exec scanning, gateway user
authorization + DM pairing, container isolation, env/credential filtering, MCP credential handling, SSRF,
website blocklist, supply-chain advisories, production deployment checklist), the opt-in checkpoint/rollback
shadow-git safety net, the Bitwarden Secrets Manager backend, and the administrator-pinned **managed scope**
config/secrets governance layer. Source = 5 mirrored pages in
`inbox/hermes_agent_docs/` (4 substantive + 1 stub). **P1 / foundational** — the security concepts here are
referenced by SP02 config notes (`hermes_security_skill_memory_settings`, `hermes_terminal_backends`), the
SP03a Docker note, and the SP06 cron/hooks notes. SP03b OWNS the new term captures `term_tirith` and
`term_shadow_git_checkpoint`.

## Content Strategy

- **One BB per note.** `security.md` (4577w, 26 code) is a single defense-in-depth procedure page but exceeds
  the 2500w cap → split into 2 procedure notes by security boundary (see Split Decisions). `checkpoints-and-rollback.md`
  → 1 procedure note. `secrets/bitwarden.md` → 1 procedure note. `managed-scope.md` (870w, 6 code)
  → 1 procedure note (small, no split). `secrets/index.md` (97w) is a 2-link
  redirect stub → **NOT digested** (recorded in coverage map).
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the terminal
  backend model + Docker hardening detail (SP02 `hermes_terminal_backends`, SP03a `hermes_docker`), the
  config-block reference for `security:`/`approvals:`/`checkpoints:` (SP02 `hermes_security_skill_memory_settings`),
  cron headless approval behavior (SP06), the messaging-platform allowlist/threading detail (SP11-13), the
  MCP feature page (SP09), website-blocklist config reference (SP02).
  Hermes' "credential pool / credential filtering"** — a master-caution LIKE false-positive; do NOT link it
  from the credential-filtering note. `term_secrets_manager.md` (active) is the generic concept (AWS Secrets
  Manager / generic secret-store) — LINK it from the Bitwarden note, do not recreate; the planned
  `hermes_secrets_bitwarden` is the Hermes-specific Bitwarden-backend procedure, a different BB scope.
- **Collision: `term_regular_checkpointing.md` (active)** covers the generic ML/training-checkpoint concept —
  the planned `hermes_checkpoints_rollback` documents Hermes' user-facing shadow-git filesystem rollback
  procedure; the new owned `term_shadow_git_checkpoint` is the Hermes-specific concept → LINK both, do not dup.

## Source Pages (Measured 2026-06-15; re-measured 2026-06-19 — mirror c253b07, BODY-only words / `^```//2`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/security.md | 4577 | 26 | procedure (defense-in-depth) | 2 (split) |
| user-guide/checkpoints-and-rollback.md | 1321 | 15 | procedure | 1 |
| user-guide/secrets/bitwarden.md | 1256 | 4 | procedure | 1 |
| user-guide/managed-scope.md | 870 | 6 | procedure (config governance) | 1 |
| user-guide/secrets/index.md | 97 | 0 | — (stub) | 0 (skip) |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **5 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_security_command_approval.md` | procedure | security §Overview (7 layers), §Dangerous Command Approval (Approval Modes, YOLO Mode, Hardline Blocklist, Approval Timeout, What Triggers Approval, Approval Flow CLI, Approval Flow Gateway/Messaging, Permanent Allowlist), §User Authorization Gateway (Check Order, Platform Allowlists, DM Pairing System), §Tirith Pre-Exec Security Scanning, §Context File Injection Protection | ~1700 | The "who and what may run" boundary: the 7-layer model, three approval modes (manual/smart/off), `--yolo`/`/yolo`/`HERMES_YOLO_MODE` and the always-on hardline blocklist floor, approval-trigger patterns + CLI/messaging approval flows + permanent allowlist, gateway user-authorization check order + per-platform allowlists + the code-based DM pairing system, Tirith content-level pre-exec scanning, and AGENTS.md/SOUL.md prompt-injection scanning. |
| 2 | `hermes_security_isolation_credentials.md` | procedure | security §Container Isolation (Docker Security Flags, Resource Limits, Filesystem Persistence), §Terminal Backend Security Comparison, §Environment Variable Passthrough (Skill-scoped, Config-based, Credential File Passthrough, What Each Sandbox Filters, Security Considerations), §MCP Credential Handling (Safe Env Vars, Credential Redaction, Website Access Policy, SSRF Protection), §Best Practices for Production Deployment (Gateway Checklist, Securing API Keys, Network Isolation), §Supply-chain advisory checking (+Lazy install) | ~1900 | The isolation + credential-containment boundary: Docker hardening flags + resource limits + persistence modes, the 6-backend security comparison, env-var passthrough (skill-scoped + config + credential-file mounting) + per-sandbox filter matrix, MCP filtered-env + credential redaction, SSRF private-address blocking + `allow_private_urls`, website blocklist, the 10-step production gateway checklist + SSH network isolation, and the supply-chain advisory scanner + lazy-install guarantees. |
| 3 | `hermes_checkpoints_rollback.md` | procedure | checkpoints-and-rollback §(intro/enable), §What Triggers a Checkpoint, §Quick Reference, §How Checkpoints Work, §Configuration, §Listing Checkpoints, §Inspecting the Store, §Previewing with /rollback diff, §Restoring with /rollback, §Single-File Restore, §Safety and Performance Guards, §Where Checkpoints Live (+Migration from v1), §Best Practices | ~1100 | The opt-in filesystem safety net: enable per-session (`--checkpoints`) or globally, the shared shadow-git store at `~/.hermes/checkpoints/store/`, what triggers an auto-snapshot, the `/rollback` slash + `hermes checkpoints` CLI surface, config knobs (max_snapshots/size/retention/auto_prune), restore + single-file restore + pre-rollback snapshot, safety guards (git-availability, dir-scope, size caps, real GC pruning), store layout + v1→v2 migration. |
| 4 | `hermes_secrets_bitwarden.md` | procedure | bitwarden §(intro), §How it works, §Why machine accounts, §Setup (create machine account/token, run wizard, confirm), §CLI, §Configuration, §Failure modes, §Security notes, §When NOT to use this | ~1000 | Pulling provider keys from Bitwarden Secrets Manager at startup: the machine-account + `BWS_ACCESS_TOKEN` bootstrap model, the auto-downloaded checksum-verified `bws` binary, the `hermes secrets bitwarden setup/status/sync/install/disable` CLI, the `secrets.bitwarden.*` config (override_existing, cache_ttl, server_url regions), fail-open failure modes, bootstrap-token security notes, and when NOT to use it. |
| 5 | `hermes_managed_scope.md` | procedure | managed-scope §(intro/what it is + distinction from package-manager lock), §Where it lives (incl. §§Relocating the directory), §Precedence, §Seeing what's managed, §Setting up a managed scope (administrators), §Security model and limitations (v1) | ~750 | Administrator-pinned, user-immutable config + secrets layer: a system-level `/etc/hermes` directory (`config.yaml` + `.env`, root-owned `0755`/`0644`, filesystem-permission enforcement) whose pinned keys win over `~/.hermes/config.yaml`, `~/.hermes/.env`, and even the shell — leaf-level merge so only pinned keys freeze. Covers `HERMES_MANAGED_DIR` relocation (and its bypass caveat), the 3-tier precedence table (the one place managed config inverts the env-over-config rule), the `hermes config`/`hermes doctor` "what's managed" surface + the refusal message on `hermes config set`, the admin setup recipe, and the v1 security model + limitations (out-of-scope: hard agent boundary, macOS/Windows, `managed.d/`, signing, MDM, group-scoped perms). |

**SP03b totals:** 5 notes · procedure 5 · concept 0 (concepts owned by existing/new term notes).
4 source pages digested (substantive), 1 skipped (secrets/index stub), 0 routed-to-enrich.

## Summary Statistics & Building Block Distribution

- Notes: 5 · procedure 5 · concept 0 (security/secrets/checkpoint concepts are existing or owned term notes).
- Source: 4 digested pages (~8.0K words) → ~6.4K words of notes (compression via link-outs to config + backend notes).
- BB mix: procedure 100% (the entire scope is operational security/secrets/rollback/config-governance procedure).
- New term notes OWNED by SP03b: 2 (`term_tirith`, `term_shadow_git_checkpoint`).

## Section Coverage Map

```
security.md (4577w)
├── # Security / ## Overview (7 security layers) ───────────── → Note 1
├── ## Dangerous Command Approval
│   ├── Approval Modes (manual/smart/off + config keys table) → Note 1
│   ├── YOLO Mode (CLI/slash/env, banner+status reminders) ── → Note 1
│   ├── Hardline Blocklist (Always-On Floor) ──────────────── → Note 1
│   ├── Approval Timeout / What Triggers Approval (patterns) ─ → Note 1 (container bypass→Note 2 backend cmp)
│   ├── Approval Flow CLI / Approval Flow Gateway/Messaging ── → Note 1
│   └── Permanent Allowlist ───────────────────────────────── → Note 1 (config block→SP02)
├── ## User Authorization (Gateway)
│   ├── Authorization Check Order / Platform Allowlists ───── → Note 1 (per-platform setup→SP11-13)
│   └── DM Pairing System (flow, security features, CLI, storage) → Note 1
├── ## Container Isolation (Docker flags, Resource Limits, Persistence) → Note 2 (backend model→SP02; docker deep→SP03a)
├── ## Terminal Backend Security Comparison ────────────────── → Note 2 (6-backend model→SP02 hermes_terminal_backends)
├── ## Environment Variable Passthrough (skill/config/cred-file/filter matrix/considerations) → Note 2
├── ## MCP Credential Handling (safe env, redaction, website policy, SSRF) → Note 2 (mcp feature→SP09; blocklist cfg→SP02)
├── ## Tirith Pre-Exec Security Scanning ───────────────────── → Note 1 (OWNS term_tirith)
├── ## Context File Injection Protection ───────────────────── → Note 1 (SOUL/AGENTS→SP05)
├── ## Best Practices for Production Deployment (checklist, API keys, network isolation) → Note 2 (ssh backend→SP02)
└── ## Supply-chain advisory checking (+Lazy install of optional deps) → Note 2
checkpoints-and-rollback.md (1321w) ── ALL sections ────────── → Note 3 (OWNS term_shadow_git_checkpoint; worktrees→SP03a)
secrets/bitwarden.md (1256w) ──────── ALL sections ─────────── → Note 4 (secret-store concept→term_secrets_manager)
managed-scope.md (870w)
├── # Managed Scope / (intro: what it IS + distinction from package-manager-locked install) → Note 5
├── ## Where it lives (/etc/hermes layout, root 0755/0644 perm enforcement) → Note 5 (config blocks→SP02)
│   └── ### Relocating the directory (HERMES_MANAGED_DIR + bypass caveat + hermes doctor) → Note 5 (HERMES_HOME→core_hermes_home)
├── ## Precedence (3-tier table; leaf-level merge; env-inversion note) → Note 5 (config precedence→SP02 hermes_config_files_precedence)
├── ## Seeing what's managed (hermes config / hermes doctor; refusal on hermes config set) → Note 5
├── ## Setting up a managed scope (administrators) (sudo recipe) → Note 5
└── ## Security model and limitations (v1) (filesystem-only enforcement; world-readable .env; out-of-scope list) → Note 5
secrets/index.md (97w) ────────────── 2-link redirect stub ─── → SKIP (recorded; not a note)
```

No source H2/H3 orphaned. `secrets/index.md`'s two link lines are covered by the entry point + Note 4.
Feature-page detail (backend model, config blocks, MCP feature) intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| security.md (4577w, 26 code) | Note 1 (command-approval + user-authorization + Tirith + context-file scanning) + Note 2 (container isolation + env/credential filtering + MCP cred + SSRF + production checklist + supply-chain advisories) | >4000w → ≥2 notes (plan-digestion Step 3c). Both halves are procedure, but they are two distinct security boundaries: "who/what may run a command" (approval + authorization + scanning) vs "how execution is isolated + how credentials are contained" (sandboxing + env-filtering + network). Split keeps each ≤2500w and ≤6 curated code blocks. This matches the master ledger's `[SPLIT]` annotation for security.md. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; search term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_security_command_approval` | `term_prompt_injection` (active), `term_human_in_the_loop` (active), `term_attack_simulation`, `term_adversarial_attack` | **NOT a dup** — those are component concepts the note USES (injection scanning, human-in-the-loop approval) | CREATE; LINK them as related. |
| `hermes_checkpoints_rollback` | `term_regular_checkpointing.md` (active, generic ML/training checkpoint), `term_git_filter_branch` | **NOT a dup** — generic checkpoint concept ≠ Hermes shadow-git filesystem rollback; new `term_shadow_git_checkpoint` is the Hermes concept | CREATE; LINK `term_regular_checkpointing` + new `term_shadow_git_checkpoint`. |
| `hermes_secrets_bitwarden` | `term_secrets_manager.md` (active, generic secret-store), `term_aws_sdk_credential_chain`, `term_encryption` | **NOT a dup** — generic secret-manager concept ≠ Hermes' Bitwarden-backend setup procedure | CREATE; LINK `term_secrets_manager` (do not recreate). |
| `hermes_managed_scope` | `term_configuration_model.md` (active, generic config layering), `term_posix_permissions.md` (active), `term_access_control.md` (active), `term_fleet.md` (active) | **NEW — NOT a dup** — no existing term/doc note covers the Hermes-specific administrator-pinned `/etc/hermes` managed config+secrets layer + its precedence inversion; the LIKE hits are component concepts (config-layering model, the POSIX `0755`/`0644` enforcement primitive, the access-control boundary, the fleet/org deployment context) | CREATE; LINK `term_configuration_model`/`term_posix_permissions`/`term_access_control`/`term_fleet` as related; do not recreate. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords; **0 substantive
same-concept duplicates** (the LIKE hits are component concepts to LINK, or the confirmed `term_credential_stuffing`
false-positive). New `hermes_agent/` folder → no doc-doc collisions (SP03a/SP03 siblings not yet executed;
intra-series links resolve at finalization, verified by G5/G8).

## Per-Note Related Notes Mapping (FINALIZED — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note — FOUR FLOORS, all counted)

> **Four-floor standard set 2026-06-19** (current user directive — supersedes the prior 2026-06-19
> three-floor wording and the 2026-06-14 floor): each note's `## Related Notes` carries **≥8 term notes
> that IMPLEMENT what this doc note documents), ≥10 snippet notes (`../../code_snippets/snippet_hermes_agent_*`,
> notes (`../../documentation/`, sibling `hermes_*` in this series + analogous `claude_code/cc_*` agent-tool
> docs + other relevant existing doc notes)** — all relevancy-selected, each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`. The **snippet group
> (`snippet_hermes_agent_*`) is now a COUNTED floor (≥10), promoted from its prior "bonus" status** — it is
> the implementation layer this doc note describes and is selected by the planned note's content. **All term +
> `config.DB_PATH_STR`). The 2 owned terms (`term_tirith`, `term_shadow_git_checkpoint`) are captured in
> Phase 0 BEFORE the notes that use them, so by write time they exist — they ARE counted to the ≥8 floor for
> their owning note. Intra-series doc links (sibling `hermes_*`) resolve at finalization (G5/G8) and are
> allowed un-verified. Other-SP not-yet-existing terms are marked `[own]` in a `(+fin ...)` tail and are
> EXCLUDED from the ≥8 floor.

**Note 1 `hermes_security_command_approval`**
- Docs (10): [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md) — sibling Note 2; relevance: the other half of the security.md split (container-bypass of approval checks links the two boundaries). [hermes_checkpoints_rollback](hermes_checkpoints_rollback.md) — sibling Note 3; relevance: checkpoints snapshot before the destructive commands this approval layer gates. [hermes_secrets_bitwarden](hermes_secrets_bitwarden.md) — sibling Note 4; relevance: pinning `security.*` and gateway tokens relates to the approval/authorization posture. [hermes_managed_scope](hermes_managed_scope.md) — sibling Note 5; relevance: an admin can pin `security.redact_secrets`/approval config via managed scope. [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — SP02 sibling; relevance: the `approvals:`/`security:`/`command_allowlist` config blocks referenced here are defined there. [hermes_terminal_backends](hermes_terminal_backends.md) — SP02 sibling; relevance: container backends skip the dangerous-command check (the container is the boundary). [cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md) — Claude Code tool-approval analogue; relevance: closest external-agent parallel to Hermes' approve/deny/always flow. [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — CC permission rules analogue; relevance: allowlist/denylist command rules mirror Hermes' `command_allowlist` + dangerous-pattern list. [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — CC permission modes analogue; relevance: manual/smart/off modes parallel CC's permission-mode spectrum (incl. an auto/yolo-style mode). [cc_security_architecture](../claude_code/cc_security_architecture.md) — CC defense-in-depth analogue; relevance: layered security model parallels Hermes' 7-layer overview.

**Note 2 `hermes_security_isolation_credentials`**
- Docs (10): [hermes_security_command_approval](hermes_security_command_approval.md) — sibling Note 1; relevance: the other security.md half (container backends skip the approval check Note 1 documents). [hermes_checkpoints_rollback](hermes_checkpoints_rollback.md) — sibling Note 3; relevance: shares the filesystem-safety surface and per-file size guards. [hermes_secrets_bitwarden](hermes_secrets_bitwarden.md) — sibling Note 4; relevance: the credential-containment story (env filtering) vs centralized secret injection. [hermes_managed_scope](hermes_managed_scope.md) — sibling Note 5; relevance: a world-readable managed `.env` interacts with this credential-containment boundary. [hermes_terminal_backends](hermes_terminal_backends.md) — SP02 sibling; relevance: the 6-backend model + `terminal.backend`/`docker_image`/resource keys live there. [hermes_docker](hermes_docker.md) — SP03a sibling; relevance: deep Docker deployment + image build detail that this note links out to. [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — SP02 sibling; relevance: `security.website_blocklist`/`allow_private_urls`/`tirith_*`/`allow_lazy_installs` config blocks defined there. [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — CC sandbox isolation analogue; relevance: filesystem + network egress isolation closely parallels Hermes' container + SSRF model. [cc_sandbox_environments_comparison](../claude_code/cc_sandbox_environments_comparison.md) — CC sandbox comparison analogue; relevance: per-backend isolation comparison mirrors Hermes' Terminal Backend Security Comparison table. [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — CC web-tool security analogue; relevance: web-fetch SSRF/domain restrictions parallel Hermes' website blocklist + SSRF protection.

**Note 3 `hermes_checkpoints_rollback`**
- Docs (10): [hermes_security_command_approval](hermes_security_command_approval.md) — sibling Note 1; relevance: checkpoints snapshot before the destructive commands the approval layer gates. [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md) — sibling Note 2; relevance: shares the filesystem-safety + per-file size-cap surface. [hermes_secrets_bitwarden](hermes_secrets_bitwarden.md) — sibling Note 4; relevance: both are opt-in subsystems configured under `~/.hermes/config.yaml`. [hermes_managed_scope](hermes_managed_scope.md) — sibling Note 5; relevance: an admin could pin `checkpoints.enabled`/retention via managed scope. [hermes_git_worktrees](hermes_git_worktrees.md) — SP03a sibling; relevance: the page explicitly recommends combining checkpoints with worktree isolation for parallel agents. [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — SP02 sibling; relevance: the `checkpoints:` config block (max_snapshots/size/retention/auto_prune) is defined in the config notes. [hermes_sessions](hermes_sessions.md) — SP-sessions sibling; relevance: a restore undoes the last conversation turn, tying checkpoints to session state. [cc_file_tool_behavior](../claude_code/cc_file_tool_behavior.md) — CC file-edit behavior analogue; relevance: closest external parallel to the write/patch file mutations that trigger Hermes checkpoints. [cc_worktree_isolation](../claude_code/cc_worktree_isolation.md) — CC worktree isolation analogue; relevance: parallels the git-worktree-as-extra-safety-layer recommendation. [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — CC command-execution analogue; relevance: parallels the destructive-terminal-command set (rm/dd/sed -i/redirects) that fires a pre-mutate snapshot.

**Note 4 `hermes_secrets_bitwarden`**
- Docs (10): [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md) — sibling Note 2; relevance: the credential-containment boundary (env filtering) the injected secrets pass through. [hermes_security_command_approval](hermes_security_command_approval.md) — sibling Note 1; relevance: gateway tokens / secret handling tie into the security posture. [hermes_checkpoints_rollback](hermes_checkpoints_rollback.md) — sibling Note 3; relevance: both are opt-in subsystems toggled in `~/.hermes/config.yaml`. [hermes_managed_scope](hermes_managed_scope.md) — sibling Note 5; relevance: managed scope governs the same secrets surface (a pinned `.env` env key cannot be user-overridden). [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — SP02 sibling; relevance: the `secrets.bitwarden.*` config block is part of the config reference. [hermes_config_files_precedence](hermes_config_files_precedence.md) — SP02 sibling; relevance: Bitwarden runs after `~/.hermes/.env` loads and its `override_existing` decides who wins in the precedence chain. [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — SP02 sibling; relevance: the provider API keys Bitwarden resolves are what the model/provider config consumes. [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — CC credential-controls analogue; relevance: closest external parallel to externalized credential handling + filesystem credential scoping. [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — CC token/auth analogue; relevance: bearer-token + OAuth credential handling parallels Hermes' bootstrap-token model. [cc_managed_settings](../claude_code/cc_managed_settings.md) — CC managed-settings analogue; relevance: parallels org-level externalized/pinned secret + config delivery (ties Bitwarden to the managed-scope story).

**Note 5 `hermes_managed_scope`**
- Docs (10): [hermes_config_files_precedence](hermes_config_files_precedence.md) — SP02 sibling; relevance: managed scope sits ATOP the config-files precedence chain and is the one place env-over-config inverts for pinned keys. [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — SP02 sibling; relevance: managed scope pins `security:`/`model:` config-block keys defined in the settings reference. [hermes_secrets_bitwarden](hermes_secrets_bitwarden.md) — sibling Note 4; relevance: governs the same secrets surface — a managed `.env` pins env keys a user/setup cannot override. [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md) — sibling Note 2; relevance: a world-readable managed `.env` interacts with the credential-containment boundary (use only for non-sensitive shared values). [hermes_security_command_approval](hermes_security_command_approval.md) — sibling Note 1; relevance: pinning `security.redact_secrets`/approval keys ties managed scope into the command-approval/security posture. [hermes_docker](hermes_docker.md) — SP03a sibling; relevance: `HERMES_MANAGED_DIR` is a container/deployment bootstrap knob baked into the service unit / container image. [cc_managed_settings](../claude_code/cc_managed_settings.md) — CC managed-settings analogue; relevance: closest external parallel — admin-enforced settings a user cannot override. [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — CC managed-precedence analogue; relevance: parallels the highest-tier managed layer winning over user/project settings. [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — CC admin-enforcement analogue; relevance: parallels org/IT-pushed enforced config baselines for a fleet. [cc_settings_scopes_and_precedence](../claude_code/cc_settings_scopes_and_precedence.md) — CC settings-precedence analogue; relevance: parallels the multi-tier (managed → user → defaults) precedence resolution and leaf-level merge.

All 5 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc (FOUR FLOORS, all counted). Actual counts per
note: terms 10/10/9/10/10, code-repos 6/6/5/5/5, snippets 10/12/10/10/10, docs 10/10/10/10/10 (min 8 term /
5 repo / 10 snippet / 10 doc). Code-repo IDs are under `areas/code_repos/` with the `repo_hermes_agent_` prefix
implementation corpus whose code each note documents; this is now a COUNTED floor (≥10), promoted from the prior
doc links resolve in `resources/documentation/hermes_agent/` (intra-series links land at finalization, verified
by G5/G8). The 2 owned terms (`term_tirith`, `term_shadow_git_checkpoint`) are Phase-0 captures and count to the

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15; re-measured 2026-06-19, mirror c253b07)

Re-read all 4 substantive source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 security-command-approval | procedure | 1700 | ≤6 (curate from approval-modes YAML + blocklist + tirith + pairing blocks; tables in prose) | ✓ |
| 2 security-isolation-credentials | procedure | 1900 | ≤6 (curate from docker-flags + resource-limits + passthrough + ssrf + lazy-deps blocks) | ✓ |
| 3 checkpoints-rollback | procedure | 1100 | ≤6 (curate from enable/config/store-layout blocks; mermaid kept) | ✓ |
| 4 secrets-bitwarden | procedure | 1000 | 4 | ✓ |
| 5 managed-scope | procedure | 750 | ≤6 (keep all 6: /etc/hermes tree, HERMES_MANAGED_DIR export, managed config.yaml example, precedence table is prose, the refusal-message block, admin sudo recipe) | ✓ |

No further splits needed — all 5 notes ≤2500w (Note 5 is the smallest at ~750w from an 870w page — one cohesive
config-governance procedure, no split). The security.md split (→ Notes 1+2) keeps each half a single
topically-cohesive procedure boundary ≤1900w. The 26 source code blocks across security.md are curated to ≤6
load-bearing examples per note (verbatim for kept blocks: approval YAML, Docker `_BASE_SECURITY_ARGS`, SSRF
ranges, env-filter matrix), the rest summarized in prose. Checkpoints' mermaid + store-layout block kept.
Borderline check: Note 2 at ~1900w is one cohesive isolation/credential boundary with no BB mixing → KEEP
(review CP6 default-to-keep justification). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** (FOUR
FLOORS, all counted — set 2026-06-19) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP03b)

**SP03b owns 2 new term captures** (per the master corpus-wide ownership sweep): `term_tirith` and
`term_shadow_git_checkpoint`. Both DB-confirmed ABSENT 2026-06-15 (no existing note). Each is captured via
`/tessellum-capture-term-note <term>` in **Phase 0**, BEFORE the digest notes that reference them, so their
notes are real link targets from the start. Specificity + collision audit run on each owned slug below.

| Term Slug | Concept | Best-Fit Glossary | Capture Phase | Stub or Full | Source Page | Notes |
|---|---|---|---|---|---|---|

### Renamed (general → specific)

| Original (would-be) slug | Renamed to | Reason (specificity audit) |
|---|---|---|
| `term_checkpoint` / `term_rollback` | `term_shadow_git_checkpoint` | bare `checkpoint`/`rollback` is a one-word common noun that collides with the generic `term_regular_checkpointing` (ML training-checkpoint) and any git-revert concept. Scope-qualified to the Hermes shadow-git filesystem mechanism. |
| `term_security_scanner` | `term_tirith` | bare `security_scanner` is too general (collides with SAST/vuln-scanner concepts). Use the literature's/project's standard proper name — the `tirith` tool. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_secrets_manager` (Bitwarden note) | `term_secrets_manager.md` (active, generic secret-store) | Not captured — LINK the existing term from `hermes_secrets_bitwarden`; the doc note holds the Hermes-specific Bitwarden procedure. |
| `term_credential_pool` (env/cred filtering) | none substantive in SP03b scope (owned by SP09 credential-pools) | Not captured by SP03b — forward-ref `[own SP09]`, linked at finalization. |
| `term_prompt_injection` (context-file scanning) | `term_prompt_injection.md` (active) | Not captured — LINK existing from `hermes_security_command_approval`. |
| `term_ssrf` / `term_command_injection` (would-be) | none substantive | Treated as link-only references inside Note 2 prose (low standalone value; not recurring conceptual use across the corpus per master guidance). Not captured. |

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

Both owned terms (`term_tirith`, `term_shadow_git_checkpoint`) are authored via **`/tessellum-capture-term-note <term>`**
(interactive or via ENRICHER_INPUTS), NOT inline-authored within a digest note. The capture skill enforces the
requirements below; this plan invokes them and does not reduce them.

- **YAML frontmatter**: `tags` (resource, terminology, + domain tags e.g. `security`/`systems`), `keywords`,
  `topics`, `language: markdown`, `date of note`, `status: active`, `building_block: concept`,
  `access_control_group: ["general"]`, `related_wiki: <url or null>`. No forbidden fields.
- **H1**: `# Tirith - Pre-Exec Security Scanner` / `# Shadow Git Checkpoint - Filesystem Rollback Store`.
- **Required H2 in order**: `## Definition` → `## Context` → `## Key Characteristics` → `## Performance / Metrics`
  (OMIT — no metrics) → `## Related Terms` (**8-15 links min**, in-domain + cross-domain) → `## References`
  (external URLs only: the Hermes docs page + e.g. github.com/sheeki03/tirith; NO `term_*.md` links here).
  author MUST also research ≥2 external sources (Tirith: the upstream GitHub repo + OWASP homograph/pipe-to-shell
  references; shadow-git checkpoint: git content-addressable-store + worktree references) AND run vault
  cross-reference (`/tessellum-search-notes` + DB) for in-domain + cross-domain related terms. Internal
  external-tool terms → use the Research Dry-Fall Fallback: cite the docs page + external sources, do NOT emit
  a digest-doc-only stub).
- **Cross-domain Related Terms diversity** (≥3 in-domain + ≥3 cross-domain): Tirith → in-domain
  `term_prompt_injection`, `term_adversarial_attack`, `term_attack_simulation`, `term_human_in_the_loop`;
  cross-domain `term_autonomous_coding_agents` (Application), `term_blocklist` (Component/Contrast — pattern
  matching vs content scanning). Shadow-git checkpoint → in-domain `term_regular_checkpointing`,
  `term_git_filter_branch`, `term_session_persistence`; cross-domain `term_idempotency` (Component — the
  auto-prune marker), `term_self_evolving_agent` (Application — safety net for self-modifying agents).
- **Math notation**: N/A (no formulas in these terms); if any appear, MathJax `$...$`/`$$...$$` only.
- **Fleeting-content guard**: no person aliases (use "Nous Research" / team), no bare ETAs/headcounts; pinned
  versions like `bws v2.0.0` get a temporal qualifier ("pinned version as of the docs").
- **Glossary entry** (4-5 sentence Description, no metrics, bold the single most distinguishing fact): append
  to `acronym_glossary_security.md` (Tirith) and `acronym_glossary_systems.md` (shadow-git checkpoint) using
  the exact `**Full Name** / **Description** / **Documentation** / **Wiki** / **Related**` template.
- **Depth-scaled Related Terms minimum**: both expected Simple-to-Moderate (40-150 lines) → **8-10** links min.
- **Backlink expansion** (Step 6e — REVERSE): add the new term to 5-10 existing in/cross-domain term notes'
  `## Related Terms` (e.g. `term_prompt_injection`, `term_sandbox_backend`, `term_regular_checkpointing`).
- **>200-line decomposition**: if either note exceeds 200 lines, decompose (procedure→`sop_*`, model/argument→`thought_*`).
- **Pre-flight outcome**: both DB-confirmed ABSENT → `Stub or Full: full`, create (no overwrite risk).

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (owned-term capture — runs FIRST):** `/tessellum-capture-term-note term_tirith` →
  `acronym_glossary_security.md`; `/tessellum-capture-term-note term_shadow_git_checkpoint` →
  `acronym_glossary_systems.md`. Reindex so the digest notes have real link targets. GATE G1 (term format),
  G5 (related-term DB-verify), G6, G8 (backlink expansion gives in-degree ≥1).
- **Phase 1 (security pilot + isolation):** Pilot Note 1 (`hermes_security_command_approval`) first → reindex
  → verify format/ghost/in-degree BEFORE Note 2. Then Note 2 (`hermes_security_isolation_credentials`). GATE G1–G8.
- **Phase 2 (checkpoints + secrets + managed scope):** Notes 3 (`hermes_checkpoints_rollback`),
  4 (`hermes_secrets_bitwarden`), 5 (`hermes_managed_scope`). GATE G1–G8.
- **Phase 2b (inlinks — EXECUTED, G8):** add the inlinks in the Inlinks table to existing notes. Runs after
  Notes 1-5 pass GATEs.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

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
for n in hermes_security_command_approval hermes_security_isolation_credentials hermes_checkpoints_rollback hermes_secrets_bitwarden hermes_managed_scope; do
# Phase-0 term existence (after capture)
for t in term_tirith term_shadow_git_checkpoint; do
```

## Entry Point Decision (inherited)

Contributes 5 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Security, Secrets & Checkpoints" section (within the Deployment & Security group
shared with SP03a). Parent hub back-link in `entry_research_and_ai_hub.md` is handled at master level. SP03b
does NOT create a separate entry point — the >30-note corpus shares the single master-created
`entry_hermes_agent_docs.md` (matches the >30 threshold). The 2 owned term notes also get glossary rows in
`acronym_glossary_security.md` / `acronym_glossary_systems.md` (term-capture skill Step 5).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_tools.md` | → `hermes_security_command_approval`, `hermes_checkpoints_rollback` | `tools/approval.py` + `tools/checkpoint*` repo ↔ approval/rollback usage docs |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_security_command_approval` | gateway repo ↔ user-authorization/DM-pairing usage doc |
| `repo_hermes_agent_agent_core.md` | → `hermes_security_isolation_credentials`, `hermes_secrets_bitwarden` | agent core (credential sources, env filtering) ↔ isolation/secrets docs |
| `repo_hermes_agent.md` | → `hermes_security_isolation_credentials`, `hermes_managed_scope` | implementation ↔ container-isolation/production-deploy + managed-config-layer usage |
| `repo_hermes_agent_cli.md` | → `hermes_secrets_bitwarden`, `hermes_checkpoints_rollback`, `hermes_managed_scope` | CLI repo (`hermes secrets`, `hermes checkpoints`, `hermes config`/`hermes doctor` managed-scope reporting) ↔ command usage docs |
| `term_configuration_model.md` | → `hermes_managed_scope` | generic config-layering term → Hermes admin-pinned managed-scope precedence doc |
| `term_posix_permissions.md` | → `hermes_managed_scope` | POSIX `0755`/`0644` permission term → the doc whose enforcement mechanism IS those file perms |
| `term_prompt_injection.md` | → `hermes_security_command_approval` | concept term → context-file injection scanning doc |
| `term_sandbox_backend.md` | → `hermes_security_isolation_credentials` | concept term → backend-isolation security doc |
| `term_secrets_manager.md` | → `hermes_secrets_bitwarden` | generic secret-store term → Hermes Bitwarden backend doc |
| `term_regular_checkpointing.md` | → `hermes_checkpoints_rollback` | generic checkpoint term → Hermes shadow-git rollback doc |
| `term_tirith.md` (new, Phase 0) | → `hermes_security_command_approval` | owned term → the doc that documents Tirith in the approval flow |
| `term_shadow_git_checkpoint.md` (new, Phase 0) | → `hermes_checkpoints_rollback` | owned term → the rollback procedure doc |
| `entry_code_snippets_hermes_agent.md` | → `hermes_security_command_approval`, `hermes_secrets_bitwarden`, `hermes_managed_scope` | code layer ↔ docs layer (managed-scope ↔ `snippet_hermes_agent_cli_config_*`) |
| `entry_hermes_agent_docs.md` (new, master) | → all 5 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 2b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 1 (`hermes_security_command_approval`) → reindex → verify format/ghost/in-degree BEFORE authoring
the rest. Phase 0 owned-term captures run FIRST (so Notes 1/3 have real link targets). Commit per phase
(per-wave commits for multi-agent runs). Re-read the source page before writing each note — do NOT work from
memory. Code blocks verbatim for kept blocks; curate code-heavy notes (security.md 26 blocks) to ≤6
load-bearing examples per note, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP
and split. If multi-agent: agents return note content, master writes serially where there is write-contention;
≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP03b lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 5 rows to the
  master-created entry point + the 2 glossary rows; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8);
  run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1 wave: bidirectionally cross-link the security notes with the SP02 config cluster
  (`hermes_security_skill_memory_settings`, `hermes_terminal_backends`) and the SP03a `hermes_docker` note
  once those land — the config blocks here are configured in SP02, the container hardening detailed in SP03a.
- Consider one `thought_` note comparing Hermes' docs-stated security model vs the code-digestion findings in
  `snippet_hermes_agent_tools_approval_*` / `snippet_hermes_agent_tools_environments_docker`.

## Augmentation Report

- **Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  code-repo / ≥10 doc, snippets bonus) and the prior ≥8 term / ≥8 snippet / ≥5 doc floor. Per-Note Mapping
  source-code modules, a COUNTED Snippets (≥10) line of `snippet_hermes_agent_*` implementation notes (promoted
  from bonus and raised from 8), and Docs (≥10) (sibling `hermes_*` + analogous `claude_code/cc_*` + SP02/SP03a
  siblings). Actual per-note counts: terms 10/10/9/10/10, repos 6/6/5/5/5, snippets 10/12/10/10/10, docs
  10/10/10/10/10. All term + code-repo + snippet + cc-doc IDs re-verified active 2026-06-19.
- Sections added/updated: Collision&Dedup Audit (1 confirmed LIKE false-positive `term_credential_stuffing`;
  3 LINK-not-dup component/generic terms), finalized Per-Note Mapping (≥8 term + ≥5 code-repo + ≥10 snippet +
  confirmed), Undigested Terms Plan + Term-Note Authoring Requirements (2 owned captures), G5 ghost + G8
  scripts, Inlinks.
- Density re-read: counts match measured (security 4577, checkpoints 1321, bitwarden 1256, managed-scope 870,
  secrets/index 97); **1 split** (security.md → Notes 1+2, matching the master ledger `[SPLIT]`). All 5 notes
  ≤2500w; code-heavy security note curated to ≤6 blocks per half; managed-scope keeps all 6 code blocks.
  `term_secrets_manager`/`term_regular_checkpointing` (generic concepts) are LINK-not-dup; no doc note
  duplicates an existing term/doc note. 2 would-be term slugs renamed for specificity
  (`term_checkpoint`→`term_shadow_git_checkpoint`, `term_security_scanner`→`term_tirith`); 1 would-be term
  removed (`term_secrets_manager` already substantive → link).
- Owned-term existence: `term_tirith` + `term_shadow_git_checkpoint` DB-confirmed ABSENT → `full`, captured Phase 0.
- Undigested terms surfaced at augment: **2 owned** (both in the master sweep, no new ones beyond it).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans, stub
skipped) ✓ Split Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note
G5/G6/G8 ✓ Note Format Def (derived from `cc_*.md`) ✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment
(re-read) ✓ Follow-up ✓ Undigested Terms Plan (2 owned) ✓ Capture Phase per term (Phase 0) ✓ best-fit
invokes capture-term-note ✓ Entry-Point Decision ✓ matches size threshold (>30 shares master entry point) ✓
Slug Specificity (2 renames documented) ✓ Slug Collision (1 false-positive confirmed + audit on owned slugs +
1 removed) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in
every phase + inlinks EXECUTED (Phase 2b) ✓ Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass). Re-reviewed 2026-06-19 (FOUR-FLOOR
standard, independent) — READY FOR EXECUTION (9/9 checkpoints pass).**

### Independent Re-Review 2026-06-19 (four-floor standard)

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP1 | Related Notes — FOUR-FLOOR | PASS | Counted per note: terms 10/10/9/10/10 (all ≥8), code-repos 6/6/5/5/5 (all ≥5), snippets 10/12/10/10/10 (all ≥10), docs 10/10/10/10/10 (all ≥10). 178 links / 178 `relevance:` clauses — no bare links. Anti-fabrication DB sweep (`.venv/bin/python` → `config.DB_PATH_STR`): ALL 35 cited existing term slugs + 10 repo slugs + 41 snippet slugs + 16 `cc_*` doc slugs verified ACTIVE; the only 2 not-in-DB term IDs are the SP03b Phase-0 OWNED captures `term_tirith`/`term_shadow_git_checkpoint` (legitimately counted; even excluding them Note 1=9 and Note 3=8 active terms still meet ≥8). 12 sibling `hermes_*` doc IDs correctly not-yet-created (G5/G8 finalization-exempt; folder has 0 notes). |
| CP2 | 8-GATE per batch (G1-G8) | PASS | Phases 0/1/2/2b each list G1-G8 incl G5-ghost (Script 4 DB-verify) + G6-broken + G8-discoverability. |
| CP4 | Plan size manageable | PASS | 5 notes ≤30; SP03 a/b split keeps under the 15-note heuristic. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (field order verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); four-floor minimum embedded. |
| CP6 | Borderline density → split | PASS | security.md→2 (master `[SPLIT]`); all 5 notes ≤2500w; Note 2 (~1900w) single-BB KEEP justified; Note 5 (~750w) no split. |
| CP7 | Source counts measured | PASS | Re-measured 2026-06-19 from `inbox/hermes_agent_docs/` (BODY-only words, fences/2): security 4577/26, checkpoints 1321/15, bitwarden 1256/4, managed-scope 870/6, secrets/index 97/0 — EXACT match to Source Pages table (ratio 1.00). |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision&Dedup Audit covers all 5 doc notes (term_dictionary AND documentation/); 1 LIKE false-positive confirmed (`term_credential_stuffing`, NOT linked); 2 renames + 1 removal sub-tables present. |
| CP9 | Discoverability — inbound (G8) | PASS | Inlinks table covers all 5 notes from `repo_*`/`term_*`/`entry_*` outside the folder; owned terms also get inlinks; inlink addition is gated Phase 2b. |

**RE-REVIEW RESULT: 9/9 → READY FOR EXECUTION (four-floor standard met).**

### Original Review 2026-06-15

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phases 0/1/2/2b, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (5 rows under a Security/Secrets/Checkpoints section); + 2 glossary rows; parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 5 notes ≤30; master holds the corpus-level split; SP03 a/b split keeps this under the 15-note heuristic. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | security.md→2 (matches master ledger `[SPLIT]`); checkpoints→1, bitwarden→1, managed-scope→1; all notes ≤2500w; code-heavy security halves curated ≤6; Note 2 (~1900w) cohesive single-BB → KEEP justified; Note 5 (~750w) small → no split. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15; re-measured 2026-06-19 (mirror c253b07): security 4577, checkpoints 1321, bitwarden 1256, managed-scope 870/6c, secrets/index 97 — measured == plan (ratio 1.00). |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 5 notes from repo_*/term_*/entry_* outside the folder (managed-scope ← repo_hermes_agent/repo_hermes_agent_cli/term_configuration_model/term_posix_permissions/entry hub); the 2 owned terms get inlinks too; inlink addition is gated Phase 2b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-downloaded from upstream `main` HEAD and is byte-identical
to it; the pin moved **95715dc → c253b07**. That re-sync surfaced **1 NEW rendered doc page**,
`user-guide/managed-scope.md` (re-measured **870w / 6 code**, BODY-only words / `^```//2` convention), which
routes to SP03b (Security, Secrets & Checkpoints) as a config-governance / fleet-security procedure. It is now
planned as the new BB-atomic note **`hermes_managed_scope.md`** (BB = procedure, ~750w, ≤6 code, no split).

- **Note count: 4 → 5** (procedure 4 → 5; concept still 0). Source pages digested: 3 → 4 (stub skip unchanged).
- **All existing SP03b pages were re-measured** under the BODY-only convention against mirror c253b07 and are
  **unchanged**: security.md 4577w/26c, checkpoints-and-rollback.md 1321w/15c, secrets/bitwarden.md 1256w/4c,
  secrets/index.md 97w (stub). No coverage, split, or routing change to Notes 1–4.
- **Cross-ref four-floor met for the new note** (re-augmented to the 2026-06-19 four-floor standard): Note 5
  `term_access_control`, `term_fleet`, `term_secrets_manager`, `term_trusted_system`, `term_appconfig`,
  (`repo_hermes_agent_cli`, `repo_hermes_agent_agent_core`, `repo_hermes_agent`, `repo_hermes_agent_plugins`,
  (`{cli_config_load, cli_config_loading, cli_config_schema, cli_config_set, cli_config_validate,
  cli_config_migrate, core_hermes_home, cli_doctor_auth_dirs, core_credential_sources, core_redact_patterns}`),
  and 10 doc notes (sibling `hermes_*` + analogous `claude_code/cc_managed_settings`,
  `cc_managed_permission_settings_and_precedence`, `cc_admin_enforcement_controls`,
  `cc_settings_scopes_and_precedence`) — meeting the
  ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc four-floor standard. Collision verdict: **NEW** (no existing
  term/doc note covers the Hermes admin-pinned `/etc/hermes` managed config+secrets layer). G8 satisfied: ≥1
  inbound link from outside the folder (`repo_hermes_agent`, `repo_hermes_agent_cli`, `term_configuration_model`,
  `term_posix_permissions`, `entry_code_snippets_hermes_agent`, the new `entry_hermes_agent_docs` hub).
- **Plan remains READY** (no gate weakened; structure, ordering preserved; cross-ref floor set
  2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note, all counted).

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented 2026-06-19 to four-floor) · Review: **DONE** (2026-06-15, 9/9 READY; re-reviewed 2026-06-19 four-floor, 9/9 READY) · Execute: pending · Re-synced 2026-06-19 (+1 note)

**Source**: `inbox/hermes_agent_docs/user-guide/{security,checkpoints-and-rollback,managed-scope}.md`, `inbox/hermes_agent_docs/user-guide/secrets/{bitwarden,index}.md`
**Last Updated**: 2026-06-15 (revised 2026-06-19, mirror c253b07 — +1 note from re-sync)
**Status**: Ready (augmented + reviewed)
