---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - audit
keywords:
  - openclaw security audit checkid
  - audit findings catalog
  - checkid severity fix key
  - gateway audit reference
  - sandbox docker bind findings
  - tools exec audit findings
  - plugins code safety scan
  - security exposure findings
  - auto-fix audit checks
topics:
  - OpenClaw
  - Security Audit
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/security/audit-checks
access_control_group: ["general"]
---

# OpenClaw — Security Audit checkId Reference Catalog

## Overview

This note models the structured-finding catalog that `openclaw security audit` emits: every audit result is keyed by a `checkId`, and this catalog (mirroring the `gateway/security/audit-checks` source page) records each high-signal `checkId`'s **severity**, **why it matters**, **primary fix key/path**, and whether it supports **auto-fix**. The source lists this as the reference for IDs you see in audit output — for the high-level threat model and hardening guidance it points to the gateway **[Security threat model](oc_gateway_security_threat_model.md)** (source page `gateway/security`). The page notes the listed IDs are the values "you will most likely see in real deployments (not exhaustive)." This note groups those findings by the surface (config-tree prefix) they describe — `fs.*`, `gateway.*`, `discovery.*`, `config.*`, `security.*`, `hooks.*`, `logging.*`, `browser.*`, `sandbox.*`, `tools.exec.*`, `skills.*`, `plugins.*`, `models.*`, and the `summary.*` roll-up — reproducing each `checkId`, its severity, and its config fix path verbatim from source. Only `fs.*` findings and `logging.redact_off` carry `Auto-fix: yes`; every other listed finding is `Auto-fix: no` (manual remediation), which is the catalog's most load-bearing structural fact.

## checkId Catalog Model

Each catalog row is the tuple `(checkId, severity, why-it-matters, primary fix key/path, auto-fix)`. Severity values seen in source are `critical`, `warn`, `info`, and compound bands `warn/critical` and `critical/info` (the band means the audit raises severity based on additional context, e.g. exposure or model size). The "primary fix key/path" is the `openclaw.json` config key, filesystem path, or remediation action that resolves the finding. Auto-fix is `yes` only where the audit can safely apply the change non-interactively (filesystem permission tightening and log redaction); all policy/exposure/trust findings are `no` and require operator review. The groupings below are by config-tree prefix, not a separate field in source.

### `fs.*` — Filesystem permissions and layout

Filesystem findings cover permission drift and unsafe layout for OpenClaw's on-disk state. World-writable state (`fs.state_dir.perms_world_writable`, **critical**) and writable config (`fs.config.perms_writable`, **critical**) are auto-fixed by tightening perms on `~/.openclaw` and `~/.openclaw/openclaw.json`. World-readable config (`fs.config.perms_world_readable`, **critical**) and writable auth profiles (`fs.auth_profiles.perms_writable`, **critical** — others can inject/replace stored model credentials at `agents/<agentId>/agent/auth-profiles.json`) and writable credentials dir (`fs.credentials_dir.perms_writable`, **critical**) are also auto-fixed. Warn-level readable variants exist for state dir, config (`perms_group_readable`), auth profiles, credentials dir, sessions store, and the gateway log file — all `Auto-fix: yes`. Two layout findings are **not** auto-fixed: `fs.config.symlink` (**warn** — symlinked config files are unsupported for writes; fix: replace with a regular config file or point `OPENCLAW_CONFIG_PATH` at the real file) and `fs.synced_dir` (**warn** — state/config in iCloud/Dropbox/Drive broadens token/transcript exposure; fix: move config/state off synced folders). `fs.state_dir.symlink` (**warn**) is likewise no-auto-fix. `fs.config_include.*` mirrors the config findings for include files referenced from `openclaw.json`.

| `checkId` | Severity | Primary fix key/path | Auto-fix |
| --- | --- | --- | --- |
| `fs.state_dir.perms_world_writable` | critical | filesystem perms on `~/.openclaw` | yes |
| `fs.config.perms_writable` | critical | filesystem perms on `~/.openclaw/openclaw.json` | yes |
| `fs.config.perms_world_readable` | critical | filesystem perms on config file | yes |
| `fs.auth_profiles.perms_writable` | critical | `agents/<agentId>/agent/auth-profiles.json` perms | yes |
| `fs.credentials_dir.perms_writable` | critical | filesystem perms on `~/.openclaw/credentials` | yes |
| `fs.config.symlink` | warn | replace with regular config file or set `OPENCLAW_CONFIG_PATH` | no |
| `fs.synced_dir` | warn | move config/state off synced folders | no |

### `gateway.*` — Bind, auth, proxy, Control UI, nodes, Tailscale

The largest family. Remote bind without a shared secret is `gateway.bind_no_auth` (**critical**; fix `gateway.bind`, `gateway.auth.*`); a reverse-proxied loopback that may become unauthenticated is `gateway.loopback_no_auth` (**critical**). Trusted-proxy auth has a dedicated cluster: `gateway.trusted_proxy_auth` (**critical** — proxy identity becomes the auth boundary), `gateway.trusted_proxy_no_proxies` (**critical**, fix `gateway.trustedProxies`), `gateway.trusted_proxy_no_user_header` (**critical**, fix `gateway.auth.trustedProxy.userHeader`), `gateway.trusted_proxy_no_allowlist` (**warn**, `gateway.auth.trustedProxy.allowUsers`), `gateway.trusted_proxy_allow_loopback` (**warn**), and `gateway.trusted_proxies_missing` (**warn**, headers present but not trusted). HTTP-API findings: `gateway.http.no_auth` (**warn/critical**, `gateway.auth.mode="none"`), `gateway.http.session_key_override_enabled` (**info**, `gateway.http.allowSessionKeyOverride`), and `gateway.tools_invoke_http.dangerous_allow` (**warn/critical**, `gateway.tools.allow`). Control UI: `gateway.control_ui.allowed_origins_required` (**critical**), `_allowed_origins_wildcard` (**warn/critical**, `allowedOrigins=["*"]`), `_host_header_origin_fallback` (**warn/critical**, DNS-rebinding hardening downgrade via `dangerouslyAllowHostHeaderOriginFallback`), `_insecure_auth` (**warn**, `allowInsecureAuth`), and `_device_auth_disabled` (**critical**, `dangerouslyDisableDeviceAuth`). Token hygiene: `gateway.token_too_short` (**warn**, `gateway.auth.token`) and `gateway.auth_no_rate_limit` (**warn**, `gateway.auth.rateLimit`). Source-IP: `gateway.real_ip_fallback_enabled` (**warn/critical**, `gateway.allowRealIpFallback`). Node commands: `gateway.nodes.allow_commands_dangerous` (**warn/critical** — enables camera/screen/contacts/calendar/SMS; `gateway.nodes.allowCommands`) and `gateway.nodes.deny_commands_ineffective` (**warn**, `gateway.nodes.denyCommands`). Tailscale exposure: `gateway.tailscale_funnel` (**critical** — public internet exposure) and `gateway.tailscale_serve` (**info** — tailnet exposure), both fixed via `gateway.tailscale.mode`. Deep-probe findings: `gateway.probe_failed` (**warn/critical**) and `gateway.probe_auth_secretref_unavailable` (**warn**). Every `gateway.*` finding is `Auto-fix: no`.

### `discovery.*`, `config.*`, `security.*` — mDNS, debug flags, exposure roll-ups

`discovery.mdns_full_mode` (**warn/critical**) flags mDNS full mode advertising `cliPath`/`sshPort` metadata on the local network (fix `discovery.mdns.mode`, `gateway.bind`). `config.insecure_or_dangerous_flags` (**warn**) fires when one insecure/dangerous debug flag is enabled (fix: the key named in the finding detail). `config.secrets.gateway_password_in_config` and `config.secrets.hooks_token_in_config` (both **warn**) flag credentials stored directly in config. `security.audit.suppressions.active` (**info**) signals the audit output is filtered by configured `security.audit.suppressions`. The `security.exposure.*` cluster captures the highest-blast-radius combinations: `open_channels_with_exec` (**warn/critical** — shared/public rooms reach exec-enabled agents), `open_groups_with_elevated` (**critical** — open DMs/groups + elevated tools create high-impact prompt-injection paths), and `open_groups_with_runtime_or_fs` (**critical/warn** — open DMs/groups reach command/file tools without sandbox/workspace guards). `security.trust_model.multi_user_heuristic` (**warn**) flags config that looks multi-user while the trust model is personal-assistant.

### `hooks.*` — Ingress token, routing, install records

Hook ingress findings: `hooks.token_reuse_gateway_token` (**critical** — hook ingress token also unlocks Gateway auth), `hooks.token_too_short` (**warn**), `hooks.path_root` (**critical** — hook path is `/`), `hooks.default_session_key_unset` (**warn**), `hooks.allowed_agent_ids_unrestricted` (**warn/critical**, `hooks.allowedAgentIds`), `hooks.request_session_key_enabled` (**warn/critical**, `hooks.allowRequestSessionKey`), and `hooks.request_session_key_prefixes_missing` (**warn/critical**, `hooks.allowedSessionKeyPrefixes`). Install-record hygiene mirrors the plugin family: `hooks.installs_unpinned_npm_specs`, `hooks.installs_missing_integrity`, and `hooks.installs_version_drift` (all **warn**). All `Auto-fix: no`.

### `logging.*`, `browser.*` — Redaction and browser control

`logging.redact_off` (**warn**, `logging.redactSensitive`) is the only non-`fs.*` finding with `Auto-fix: yes` — sensitive values leak to logs/status until redaction is restored. Browser control: `browser.control_invalid_config` (**warn**), `browser.control_no_auth` (**critical** — browser control exposed without token/password auth, fix `gateway.auth.*`), `browser.remote_cdp_http` (**warn** — remote CDP over plain HTTP), and `browser.remote_cdp_private_host` (**warn** — remote CDP targets a private/internal host; fix browser profile `cdpUrl`, `browser.ssrfPolicy.*`).

### `sandbox.*`, `tools.exec.*` — Docker isolation and exec policy

Sandbox findings target Docker isolation drift: `sandbox.docker_config_mode_off` (**warn**), `sandbox.bind_mount_non_absolute` (**warn**), `sandbox.dangerous_bind_mount` (**critical** — bind mount targets blocked system/credential/Docker-socket paths), `sandbox.dangerous_network_mode` (**critical** — `host` or `container:*` namespace-join), `sandbox.dangerous_seccomp_profile` and `sandbox.dangerous_apparmor_profile` (both **critical** — weaken container isolation via `securityOpt`), plus browser-bridge/container findings (`sandbox.browser_cdp_bridge_unrestricted` warn, `sandbox.browser_container.non_loopback_publish` critical, and two hash-label staleness warns fixed by `openclaw sandbox recreate --browser --all`). The `tools.exec.*` cluster (all **warn** except where noted) covers exec policy drift: `host_sandbox_no_sandbox_defaults` / `_agents` (exec `host=sandbox` fails closed when sandbox is off), `security_full_configured` (**warn/critical** — host exec running with `security="full"`), `fs_tools_disabled_but_exec_enabled` (filesystem tool policy does not make shell read-only), `auto_allow_skills_enabled`, `allowlist_interpreter_without_strict_inline_eval`, `safe_bins_interpreter_unprofiled`, `safe_bins_broad_behavior`, and `safe_bin_trusted_dirs_risky`. All `sandbox.*`/`tools.exec.*` findings are `Auto-fix: no`.

| `checkId` | Severity | Primary fix key/path | Auto-fix |
| --- | --- | --- | --- |
| `sandbox.dangerous_bind_mount` | critical | `agents.*.sandbox.docker.binds[]` | no |
| `sandbox.dangerous_network_mode` | critical | `agents.*.sandbox.docker.network` | no |
| `tools.exec.security_full_configured` | warn/critical | `tools.exec.security`, `agents.list[].tools.exec.security` | no |
| `tools.exec.fs_tools_disabled_but_exec_enabled` | warn | `tools.deny`, `agents.*.sandbox.workspaceAccess` | no |

### `skills.*`, `plugins.*`, `models.*`, `summary.*`

Skills: `skills.workspace.symlink_escape` (**warn** — `skills/**/SKILL.md` resolves outside workspace root), `skills.code_safety` (**warn/critical** — installer metadata/code contains suspicious/dangerous patterns), and `skills.code_safety.scan_failed` (**warn**). Plugins (supply-chain): `plugins.extensions_no_allowlist` (**warn**, `plugins.allowlist`), the three install-record warns (`installs_unpinned_npm_specs`, `installs_missing_integrity`, `installs_version_drift`), `plugins.code_safety` (**warn/critical** — code scan found suspicious patterns), `plugins.code_safety.entry_path` (**warn** — hidden/`node_modules` entry), `plugins.code_safety.entry_escape` (**critical** — entry escapes the plugin directory), `plugins.code_safety.scan_failed` (**warn**), `plugins.tools_reachable_permissive_policy` (**warn**), and `tools.profile_minimal_overridden` (**warn** — agent overrides bypass global minimal profile). Models: `models.legacy` (**warn**), `models.weak_tier` (**warn**), and `models.small_params` (**critical/info** — small models + unsafe tool surfaces raise injection risk). Finally `summary.attack_surface` (**info**) is a roll-up of auth, channel, tool, and exposure posture (fix: multiple keys, see finding detail). All `Auto-fix: no`.

**Source**: OpenClaw documentation — `gateway/security/audit-checks` (mirror `inbox/openclaw_docs/gateway/security/audit-checks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
