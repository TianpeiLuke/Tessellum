---
title: Sub-Plan B14B — Claude Code Docs: Admin, Network & Auth
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["admin-setup", "third-party-integrations", "network-config", "server-managed-settings", "authentication"]
---

# Sub-Plan B14B: Admin, Network & Auth

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md),
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 5 enterprise-administration pages that cover how an organization deploys, configures, secures the
network for, and authenticates Claude Code: the admin decision map, deployment-option comparison and
provider best practices, corporate proxy / TLS / firewall network configuration, server-delivered
managed settings, and login / credential / token authentication. P3 (Phase C) — enterprise/specialized
material that references the foundational vocabulary (settings, permissions, MCP, sandboxing) defined by
Phase A sub-plans, so it links those rather than re-defining them.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 5 pages, 7,016 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the administrator decision flow (provider → delivery mechanism → enforcement →
  visibility → data handling), the managed-settings precedence/delivery model, the network allowlist +
  TLS/mTLS surface, and the authentication precedence ladder — the operational facts an admin needs.
- **Group**: split `admin-setup` (decision map concept vs the enforcement/visibility/data control catalog
  which is procedural); keep `third-party-integrations` split into the deployment-option comparison
  (concept) vs the org best-practices (argument); merge the proxy/gateway env-var material from
  `third-party-integrations` with `network-config`'s proxy section into one procedure note, and keep the
  TLS/CA/mTLS/firewall-allowlist material as a second network procedure note.
- **Skip / link-out (own other sub-plans)**: provider-specific Bedrock/Vertex/Foundry setup → B14A;
  Permissions detail → B05A; Sandboxing → B05B; managed MCP → B08A; plugin-marketplace restrictions →
  B09B; hooks → B07A/B07B; settings keys / precedence reference → B03A; env-vars reference → B03A;
  Analytics/Monitoring/Costs → B15B/B02A; Data usage / ZDR / Security / Legal → B16; agent-view →
  B10A; memory / org-wide CLAUDE.md → B02B; LLM gateway → B14A; model pinning → B03B. These are
  referenced via links, never duplicated.
- **Glossary / terms**: no new `cc_` term re-digestion — undigested terms route to existing term notes or
  their home sub-plan (Pattern B; see Undigested Terms Plan). `Managed settings` is the one glossary term
  whose home page is in this sub-plan → digested as `cc_server_managed_settings` (doc concept), not a term note.

## Source Pages (Measured 2026-06-13, re-read)

All 5 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| admin-setup | /admin-setup | 1,609 | 0 | 7 | 0 | concept/procedure |
| third-party-integrations | /third-party-integrations | 1,559 | 0 | 4 | 9 | concept/argument |
| network-config | /network-config | 744 | 6 | 6 | 2 | procedure |
| server-managed-settings | /server-managed-settings | 1,774 | 1 | 8 | 9 | procedure |
| authentication | /authentication | 1,330 | 2 | 3 | 5 | procedure |

> **H2 lists (document order):**
> - **admin-setup**: Choose your API provider · Decide how settings reach devices · Decide what to enforce · Set up usage visibility · Review data handling · Verify and onboard · Next steps
> - **third-party-integrations**: Compare deployment options · Configure proxies and gateways (H3 Amazon Bedrock, Microsoft Foundry, Google Vertex AI) · Best practices for organizations (H3 Invest in documentation and memory, Simplify deployment, Start with guided usage, Pin model versions for cloud providers, Configure security policies, Leverage MCP for integrations) · Next steps
> - **network-config**: Proxy configuration (H3 Environment variables, Basic authentication) · CA certificate store · Custom CA certificates · mTLS authentication · Network access requirements · Additional resources
> - **server-managed-settings**: Requirements · Choose between server-managed and endpoint-managed settings · Configure server-managed settings (H3 Verify settings delivery, Access control, Managed-only settings, Current limitations) · Settings delivery (H3 Settings precedence, Fetch and caching behavior, Invalid entries in delivered settings, Enforce fail-closed startup, Security approval dialogs) · Platform availability · Audit logging · Security considerations · See also
> - **authentication**: Log in to Claude Code · Set up team authentication (H3 Claude for Teams or Enterprise, Claude Console authentication, Cloud provider authentication) · Credential management (H3 Authentication precedence, Generate a long-lived token)

## Planned Notes (LOCKED)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_admin_setup_decision_map.md` | concept | admin-setup: intro + decision table, Choose your API provider, Verify and onboard, Next steps | 450 | The admin deployment decision flow (provider → delivery → enforcement → visibility → data); provider selection table (Teams/Enterprise default, Console, Bedrock/Vertex/Foundry → B14A); `/status` Setting-sources verification; login-troubleshoot pointers (→ B17). |
| 2 | `cc_admin_enforcement_controls.md` | procedure | admin-setup: Decide what to enforce, Set up usage visibility, Review data handling | 500 | The managed-settings control catalog (permission rules/lockdown, sandbox, org CLAUDE.md, MCP/plugin/customization lockdown, hook restrictions, disable agent-view, version floor); the permission-vs-sandbox layering note; usage-visibility + data-handling matrices (each row links its home sub-plan: B05A/B05B/B08A/B09B/B07/B10A/B15B/B16). |
| 3 | `cc_enterprise_deployment_options.md` | concept | third-party-integrations: intro, Compare deployment options | 500 | Deploy through Anthropic vs a cloud provider; Teams vs Enterprise distinction; the 6-column option comparison (best-for/billing/regions/caching/auth/cost-tracking/web-included/enterprise-features) summarized; setup links → B14A / authentication note 8. |
| 4 | `cc_enterprise_best_practices.md` | argument | third-party-integrations: Best practices for organizations, Next steps | 450 | The six org-adoption recommendations (invest in docs/memory, simplify install, guided usage ramp, pin model versions, managed security policies, central MCP via `.mcp.json`) + the 3-step rollout; links B02B/B03B/B05A/B08A. |
| 5 | `cc_proxy_and_gateway_config.md` | procedure | network-config: Proxy configuration (Environment variables, Basic authentication); third-party-integrations: Configure proxies and gateways (+ per-provider tabs) | 550 | Corporate proxy vs LLM gateway (different, combinable); `HTTPS_PROXY`/`HTTP_PROXY`/`NO_PROXY` (no SOCKS); proxy basic auth + no-hardcode warning; per-provider proxy/gateway env-var recipes (Bedrock/Foundry/Vertex `*_BASE_URL` + `SKIP_*_AUTH`); `/status` verify. Full gateway → B14A. |
| 6 | `cc_network_tls_and_access.md` | procedure | network-config: CA certificate store, Custom CA certificates, mTLS authentication, Network access requirements, Additional resources | 550 | TLS trust: `CLAUDE_CODE_CERT_STORE` (bundled/system), `NODE_EXTRA_CA_CERTS`, TLS-inspection proxies (Zscaler/CrowdStrike); mTLS client cert/key/passphrase env vars; the network-access allowlist URL table + cloud-provider/GitHub-IP caveats (telemetry disable → B16). |
| 7 | `cc_server_managed_settings.md` | procedure | server-managed-settings: full page (Requirements, Choose between, Configure, Settings delivery, Platform availability, Audit logging, Security considerations) | 700 | Server-delivered managed policy from the Claude.ai admin console (no MDM); server- vs endpoint-managed choice; configure JSON (permissions/hooks/autoMode examples) + security-approval dialogs; precedence (managed tier, no merge across managed sources, array-merge within); fetch/caching + fail-closed `forceRemoteSettingsRefresh`; platform availability (not on 3p providers); audit logging; client-side-control caveats. |
| 8 | `cc_authentication.md` | procedure | authentication: full page (Log in, Set up team authentication, Credential management, Authentication precedence, Generate a long-lived token) | 650 | First-launch browser login + paste-code fallback (WSL2/SSH/containers); account types; team auth paths (Teams/Enterprise, Console roles, cloud provider) → B14A; credential storage per OS (Keychain / `0600` `.credentials.json`); `apiKeyHelper` + TTL; the 6-tier authentication precedence ladder; `claude setup-token` long-lived `CLAUDE_CODE_OAUTH_TOKEN` for CI. |

**Estimate: 8 notes** — concept ×2 (notes 1, 3), argument ×1 (note 4), procedure ×5 (notes 2, 5, 6, 7, 8). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 5 (7,016 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,350 (avg ~545/note). Code blocks: ≤4/note (env-var/JSON recipes, all verbatim) — every note within the ≤6 cap.
- **Building Block Distribution**: concept ×2 (notes 1, 3) · argument ×1 (note 4) · procedure ×5 (notes 2, 5, 6, 7, 8). No model/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_admin_setup_decision_map` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the administrator deployment decision map for Claude Code itself, so the product term is its canonical definitional anchor (what is being deployed org-wide).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The deployment decisions (which tools, commands, servers, network destinations Claude can reach) configure the harness layer that wraps the model with tools and policy across every developer machine.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The "Decide what to enforce" row of the decision table is about managed permission rules and lockdown that scope how much Claude can execute without asking — the progressive-permission concept this term defines.
- [Bedrock](../../term_dictionary/term_bedrock.md) — Amazon Bedrock is one of the API-provider options in the decision map's provider-selection table (inherit AWS compliance/billing), so the term grounds that provider row.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The decision map's enforcement row includes restricting which MCP servers users can add or connect to, making MCP a first-class control surface this admin flow governs.
- [Data Governance](../../term_dictionary/term_data_governance.md) — The "Review data handling" decision row covers retention and compliance posture inherited from the chosen provider — the data-governance posture this term defines for an enterprise deployment.

### 2. `cc_admin_enforcement_controls` (7 term notes)
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The first control rows (permission rules, permission lockdown, disable `--dangerously-skip-permissions`) are exactly the scoped-allowlist / progressive-permission mechanism this term defines, applied as non-overridable managed policy.
- [Sandbox](../../term_dictionary/term_sandbox.md) — The sandboxing control row enables OS-level filesystem and network isolation with domain allowlists; the note's permission-vs-sandbox layering point centers on the sandbox term.
- [Deny-First](../../term_dictionary/term_deny_first.md) — The enforcement catalog is built on managed deny lists (`permissions.deny`, `deniedMcpServers`, `blockedMarketplaces`) that developers can extend but not remove from — the deny-by-default posture this term names.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — One control row restricts which MCP servers users can add/connect or deploys a fixed set (`allowedMcpServers`/`deniedMcpServers`), making MCP-server lockdown one of the catalog's enforcement surfaces.
- [Skills](../../term_dictionary/term_skills.md) — The customization-lockdown row (`strictPluginOnlyCustomization`) blocks skills, agents, hooks, and MCP servers from user/project sources, so the skills term is one of the things this control governs.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note enumerates the managed-settings control surfaces of Claude Code itself (tools, commands, servers, version floor), so the product term anchors what is being locked down.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — The note's key layering example — denying WebFetch still leaves Bash `curl`/`wget` able to reach any URL until a sandbox network allowlist closes the gap — is the server-side-request-forgery exposure this guard concept addresses at the network layer.

### 3. `cc_enterprise_deployment_options` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note compares the deployment configurations of Claude Code itself (Teams/Enterprise vs Console vs cloud providers), so the product term is the subject being deployed.
- [Bedrock](../../term_dictionary/term_bedrock.md) — Amazon Bedrock is a column in the deployment-comparison table (AWS-native, IAM/CloudTrail, AWS Cost Explorer), so the term grounds that deployment option.
- [AWS](../../term_dictionary/term_aws.md) — Two columns (Amazon Bedrock and Claude Platform on AWS) are AWS-native deployments with AWS Marketplace billing and AWS compliance controls — the cloud platform this term defines.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — Each provider deployment exposes Claude through that provider's model catalog/regions with provider-specific availability, the model-catalog concept differentiating the options.
- [IAM (Identity and Access Management)](../../term_dictionary/term_iam.md) — The comparison table's enterprise-features row lists IAM policies / IAM roles / RBAC as the access-control mechanism each cloud deployment inherits, the access-management concept this term defines.
- [CloudTrail](../../term_dictionary/term_cloudtrail.md) — The AWS deployment columns cite CloudTrail for audit logging in the enterprise-features row, the AWS audit-trail service this term documents.

### 4. `cc_enterprise_best_practices` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the organizational best-practices guide for adopting Claude Code, so the product term anchors the deployment whose adoption is being optimized.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — The "Leverage MCP for integrations" recommendation is to have one central team configure MCP servers and check a `.mcp.json` into the codebase so all users benefit — MCP integration is a core best-practice axis.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — The "Invest in documentation and memory" recommendation is about deploying CLAUDE.md at org/repo levels so Claude persists project context — the agentic-memory mechanism this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The "Start with guided usage" recommendation ramps users from Q&A/small fixes to letting Claude run more agentically over time, and "Configure security policies" sets managed permissions — the graduated-trust adoption pattern.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — The "Pin model versions for cloud providers" recommendation uses `ANTHROPIC_DEFAULT_*_MODEL` to control which catalog model resolves, preventing aliases from lagging — a model-catalog management practice.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The guided-usage ramp ("as users understand this paradigm they'll let Claude Code run more agentically") describes scaling toward the autonomous-coding-agent operating mode this term defines.

### 5. `cc_proxy_and_gateway_config` (7 term notes)
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — The note configures Claude Code to route all outbound traffic through a corporate HTTP/HTTPS proxy via `HTTPS_PROXY`/`HTTP_PROXY` — the proxy-fronting pattern this term defines.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — The LLM-gateway option (`ANTHROPIC_BASE_URL`/`ANTHROPIC_*_BASE_URL`) places a service between Claude Code and the provider for centralized auth/routing/rate-limiting — the gateway concept this term defines.
- [SSL Termination](../../term_dictionary/term_ssl_termination.md) — Corporate proxies and LLM gateways that intercept HTTPS terminate and re-originate TLS, the SSL-termination mechanism that governs how proxy traffic is decrypted/inspected before reaching the provider.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — The note warns against hardcoding proxy basic-auth passwords in scripts and recommends environment variables or secure credential storage — the secrets-management practice this term defines.
- [Bedrock](../../term_dictionary/term_bedrock.md) — The per-provider proxy/gateway recipes include the Bedrock tab (`CLAUDE_CODE_USE_BEDROCK`, `ANTHROPIC_BEDROCK_BASE_URL`, `CLAUDE_CODE_SKIP_BEDROCK_AUTH`), so the term grounds that recipe.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's own proxy/gateway environment variables and `/status` verification, so the product term anchors the configuration target.
- [VPC (Virtual Private Cloud)](../../term_dictionary/term_vpc.md) — Routing all Claude Code outbound traffic through a corporate proxy is a network-egress-control pattern typical of VPC/restricted-network deployments, the isolated-network context this term defines.

### 6. `cc_network_tls_and_access` (7 term notes)
- [SSL Termination](../../term_dictionary/term_ssl_termination.md) — The note's CA-store and custom-CA configuration (`CLAUDE_CODE_CERT_STORE`, `NODE_EXTRA_CA_CERTS`) exists so Claude Code trusts the certs that TLS-inspection proxies (Zscaler/CrowdStrike) present after terminating TLS, the SSL-termination scenario this term defines.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — Trusting a custom CA or bundled-vs-system cert store is exactly the certificate-trust-anchor decision that TLS pinning governs; the note's `CLAUDE_CODE_CERT_STORE=bundled` option narrows trust to a pinned set.
- [mTLS / Client Certificate](../../term_dictionary/term_ssh.md) — The note's mTLS section configures client certificate authentication (`CLAUDE_CODE_CLIENT_CERT`/`_KEY`/`_KEY_PASSPHRASE`) — the same key-pair client-authentication primitive this term documents, applied to TLS rather than shell.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — TLS-inspection appliances (Zscaler/CrowdStrike Falcon) named in the CA-store section operate as intercepting proxies in front of Claude Code's egress, the proxy-fronting pattern this term defines.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — The network-access allowlist (api.anthropic.com, claude.ai, downloads.claude.ai, etc.) is an egress allowlist that constrains which destinations Claude Code may reach, the request-destination control this guard concept addresses.
- [VPC (Virtual Private Cloud)](../../term_dictionary/term_vpc.md) — The note's allowlist + firewall guidance targets containerized or restricted-network (VPC) environments where outbound destinations must be explicitly permitted, the isolated-network context this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's own TLS/CA/mTLS env vars and required-URL allowlist, so the product term anchors what is being network-configured.

### 7. `cc_server_managed_settings` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents how Claude Code itself receives centrally-delivered managed policy from the Claude.ai admin console, so the product term is the subject being centrally configured.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The canonical server-managed example enforces a `permissions.deny` list, blocks bypass-permissions mode, and restricts permission rules to managed ones (`allowManagedPermissionRulesOnly`) — the scoped-permission enforcement this term defines, delivered as non-overridable policy.
- [Deny-First](../../term_dictionary/term_deny_first.md) — Managed settings occupy the highest precedence tier and array keys (`permissions.deny`) merge so developers can extend but not remove — the deny-by-default, can't-loosen posture this term names.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — A documented limitation is that a `managed-mcp.json` file can't be distributed server-side; admins deliver `allowedMcpServers`/`deniedMcpServers` policy keys instead — MCP-server policy is one of the settings this delivery mechanism governs.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — The security-approval dialog gates custom environment variables not on the known-safe allowlist (a path for delivering secrets/tokens), the secrets-handling concern this term addresses in centrally-pushed config.
- [Bedrock](../../term_dictionary/term_bedrock.md) — Platform availability states server-managed settings are bypassed on third-party providers including Bedrock (`CLAUDE_CODE_USE_BEDROCK`), so the term grounds the key exclusion this note documents.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — The audit-logging section emits events (action type, account, device, previous/new values) via the compliance API, and `ConfigChange` hooks detect runtime config changes — the agent-system observability/audit concept this term defines.

### 8. `cc_authentication` (7 term notes)
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — The note's `claude setup-token` flow generates a long-lived OAuth token (`CLAUDE_CODE_OAUTH_TOKEN`) for CI, and subscription login uses OAuth credentials — the OAuth-token credential this term defines.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — The note documents the credential set Claude Code stores and selects per account type (Claude.ai, Console, Bedrock/Vertex/Azure auth), the per-account authentication-profile concept this term defines.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — The `apiKeyHelper` script returns API keys from a vault for dynamic/rotating credentials and credentials are stored at `0600`/Keychain — the secrets-storage-and-rotation practice this term defines.
- [Cloudauth](../../term_dictionary/term_cloudauth.md) — The cloud-provider authentication path (set `CLAUDE_CODE_USE_BEDROCK`/`_VERTEX`/`_FOUNDRY`, no browser login) inherits the provider's cloud credential/auth flow, the cloud-authentication concept this term defines.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — The precedence ladder's `ANTHROPIC_AUTH_TOKEN` (Bearer) tier is for routing through an LLM gateway/proxy that authenticates with bearer tokens — the gateway-fronted auth this term defines.
- [Bedrock](../../term_dictionary/term_bedrock.md) — Cloud-provider credentials sit at the top of the authentication-precedence ladder when `CLAUDE_CODE_USE_BEDROCK` is set, so the term grounds that precedence tier and the cloud-auth setup path.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents how a user logs in to Claude Code itself and how it manages credentials, so the product term anchors the authentication target.

## Section Coverage Map

```
admin-setup.md
├── intro + decision table ────────────── → note 1 (cc_admin_setup_decision_map)
├── Choose your API provider ──────────── → note 1 (provider table; Bedrock/Vertex/Foundry → B14A)
├── Decide how settings reach devices ─── → note 7 (cc_server_managed_settings: precedence/mechanisms)
├── Decide what to enforce ────────────── → note 2 (cc_admin_enforcement_controls)
├── Set up usage visibility ───────────── → note 2 (matrix; Analytics/Monitoring/Costs → B15B/B02A)
├── Review data handling ──────────────── → note 2 (matrix; Data usage/ZDR/Security → B16)
├── Verify and onboard ────────────────── → note 1 (/status sources; login-troubleshoot → B17)
└── Next steps ───────────────────────── → note 1 (links)
third-party-integrations.md
├── intro + ContactSales card ─────────── → note 3 (intro only; card is JSX chrome, dropped)
├── Compare deployment options ────────── → note 3 (cc_enterprise_deployment_options)
├── Configure proxies and gateways ────── → note 5 (cc_proxy_and_gateway_config)
│   ├── Amazon Bedrock (tabs) ─────────── → note 5
│   ├── Microsoft Foundry (tabs) ──────── → note 5
│   └── Google Vertex AI (tabs) ───────── → note 5
├── Best practices for organizations ──── → note 4 (cc_enterprise_best_practices)
│   ├── Invest in documentation/memory ── → note 4 (→ B02B memory)
│   ├── Simplify deployment ───────────── → note 4
│   ├── Start with guided usage ───────── → note 4
│   ├── Pin model versions ────────────── → note 4 (→ B03B model-config)
│   ├── Configure security policies ───── → note 4 (→ B05A/B16)
│   └── Leverage MCP for integrations ─── → note 4 (→ B08A mcp)
└── Next steps ───────────────────────── → note 4 (3-step rollout)
network-config.md
├── Proxy configuration ───────────────── → note 5
│   ├── Environment variables ─────────── → note 5
│   └── Basic authentication ──────────── → note 5
├── CA certificate store ──────────────── → note 6 (cc_network_tls_and_access)
├── Custom CA certificates ────────────── → note 6
├── mTLS authentication ───────────────── → note 6
├── Network access requirements ───────── → note 6 (allowlist table; telemetry → B16)
└── Additional resources ──────────────── → note 6 (links → B03A settings/env-vars, B17)
server-managed-settings.md
├── Requirements ──────────────────────── → note 7
├── Choose server vs endpoint-managed ─── → note 7
├── Configure server-managed settings ─── → note 7
│   ├── Verify settings delivery ──────── → note 7
│   ├── Access control ────────────────── → note 7
│   ├── Managed-only settings ─────────── → note 7 (full list → B05A permissions)
│   └── Current limitations ───────────── → note 7
├── Settings delivery ─────────────────── → note 7
│   ├── Settings precedence ───────────── → note 7 (full hierarchy → B03A settings)
│   ├── Fetch and caching behavior ───── → note 7
│   ├── Invalid entries in delivered ──── → note 7
│   ├── Enforce fail-closed startup ───── → note 7
│   └── Security approval dialogs ─────── → note 7
├── Platform availability ─────────────── → note 7
├── Audit logging ─────────────────────── → note 7 (→ B16)
├── Security considerations ───────────── → note 7
└── See also ──────────────────────────── → note 7 (links)
authentication.md
├── Log in to Claude Code ─────────────── → note 8 (cc_authentication)
├── Set up team authentication ────────── → note 8
│   ├── Claude for Teams or Enterprise ── → note 8
│   ├── Claude Console authentication ─── → note 8
│   └── Cloud provider authentication ─── → note 8 (→ B14A)
├── Credential management ─────────────── → note 8
│   ├── Authentication precedence ─────── → note 8
│   └── Generate a long-lived token ───── → note 8 (→ B11 headless/bare mode)
```
No orphaned sections. (The `third-party-integrations` `ContactSalesCard` JSX/CSS block is presentational chrome, not content — intentionally dropped per G2 faithfulness.)

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| admin-setup (1.6Kw, 7 H2 mixed) | notes 1, 2 + link-outs | distinct BB: the decision-map/provider framing is concept (note 1); the enforcement/visibility/data control catalog is procedure (note 2). "Decide how settings reach devices" precedence content is owned by note 7 (server-managed-settings) to avoid duplication. |
| third-party-integrations (1.6Kw, 4 H2) | notes 3, 4, 5 | deployment-option comparison (concept, note 3) vs org best-practices (argument, note 4) vs proxy/gateway env-var recipes (procedure, note 5) differ in BB and topic. |
| network-config (744w) + third-party proxy section | notes 5, 6 | proxy/gateway env-var config (note 5) is one coherent procedure shared with third-party's proxy tabs; TLS/CA/mTLS + firewall allowlist (note 6) is a distinct network-security procedure. Merging the two pages' proxy material avoids a split-brain proxy note. |
| server-managed-settings (1.8Kw, 8 H2 / 9 H3) | note 7 (single) | one coherent procedure (deliver managed policy from the admin console) — ~700 digest words, within caps; sub-sections become H2/H3 within the one note. No split needed. |
| authentication (1.3Kw, 3 H2 / 5 H3) | note 8 (single) | one coherent procedure (log in + manage credentials) — ~650 digest words, within caps. |

## Density Re-Assessment (LOCKED)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_admin_setup_decision_map | concept | 450 | 0 | ✅ |
| 2 | cc_admin_enforcement_controls | procedure | 500 | 0 | ✅ |
| 3 | cc_enterprise_deployment_options | concept | 500 | 0 | ✅ |
| 4 | cc_enterprise_best_practices | argument | 450 | 0 | ✅ |
| 5 | cc_proxy_and_gateway_config | procedure | 550 | 4 | ✅ |
| 6 | cc_network_tls_and_access | procedure | 550 | 4 | ✅ |
| 7 | cc_server_managed_settings | procedure | 700 | 3 | ✅ |
| 8 | cc_authentication | procedure | 650 | 2 | ✅ |

No note approaches the caps (≤400 lines, ≤2,500 words, ≤6 code blocks). Notes 5/6 carry the most code (env-var recipes, all verbatim ≤4 blocks each). Note 7 is the densest at ~700 words — comfortably under 2,500. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_admin_setup_decision_map cc_admin_enforcement_controls cc_enterprise_deployment_options cc_enterprise_best_practices cc_proxy_and_gateway_config cc_network_tls_and_access cc_server_managed_settings cc_authentication"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (8 notes, all P3). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (JSX chrome dropped) | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes receives ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed, DB in-degree ≥1) | DB in-degree query at finalization |
| G8-Discoverability(inbound) | corpus-level: no `cc_` island — every note reachable from `entry_claude_code_docs.md` + ≥1 term/doc inbound | DB in-degree ≥1 at finalization |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 8 rows** under an "Admin, network & auth" (enterprise) cluster + increments the
BB-distribution counts (concept ×2, procedure ×5, argument ×1). The entry-point back-link is added to each
note's `## Related Notes` at finalization.

## Undigested Terms Plan (Step 2d)

B14B creates **0 new `term_dictionary` captures**. Step 2d scan re-read all 5 pages (emphasis/tables/captions/
code-comments) for newly-surfaced terms; each routes to an existing term note, a B14B `cc_` doc note, or its
home sub-plan (Pattern B). Dedup checked across **both** `term_dictionary/` AND `resources/documentation/`
(no existing `claude_code/` folder yet; no `cc_` doc note duplicates a term note).

| Surfaced term | Disposition |
|---|---|
| Managed settings / Server-managed settings | note 7 `cc_server_managed_settings` (doc concept; glossary home page is in this sub-plan) |
| Endpoint-managed settings (plist/registry/MDM) | note 7 (folded); full settings-files reference → B03A |
| Corporate proxy / LLM gateway | note 5 `cc_proxy_and_gateway_config`; full gateway → B14A `llm-gateway` |
| Custom CA / mTLS / CA certificate store | note 6 `cc_network_tls_and_access` (doc procedure) |
| `apiKeyHelper` / `CLAUDE_CODE_OAUTH_TOKEN` / authentication precedence | note 8 `cc_authentication` (doc procedure) |
| MCP / Sandboxing / Permission rule / Hook / Plugin marketplace / Agent view | existing term notes (`term_mcp`, `term_sandbox`) or home sub-plan (B05A/B05B/B07/B09B/B10A) — captured/linked there, not B14B |
| OAuth / API key / bearer token | existing term notes (`term_oauth_token`, `term_auth_profile`) — linked, not recreated |
| Proxy / reverse proxy / TLS / SSL termination / API gateway / VPC / secrets manager | existing term notes (linked in Per-Note Mapping above) — not recreated |
| ZDR / Data usage / Audit logging / Compliance API | owned by B16 (security/data/compliance) — linked, not B14B |

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B14B authors zero term notes, so there are no
new slugs to audit. The collision check that matters here (do the surfaced concepts duplicate existing
`term_auth_profile`, `term_reverse_proxy`, `term_api_gateway`, `term_ssl_termination`, `term_tls_pinning`,
`term_secrets_manager`, `term_iam`, `term_cloudtrail`, `term_bedrock`, `term_aws`, `term_vpc`,
`term_observability_agent_systems` all exist → linked, not recreated. **0 new B14B `term_dictionary` captures.**

## Term-Note Authoring Requirements

**N/A for B14B** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (env-var/JSON recipes copied exactly from source). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Reindex incrementally after the phase; verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 in-degree ≥1 each):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 7, 8 | product term → CC admin decision map / managed settings / authentication |
| `term_dictionary/term_oauth_token.md` | note 8 | OAuth-token term → CC `setup-token` long-lived token + login flow |
| `term_dictionary/term_reverse_proxy.md` | note 5 | proxy term → CC corporate-proxy configuration |
| `term_dictionary/term_api_gateway.md` | notes 5, 8 | gateway term → CC LLM-gateway env vars + bearer-token auth tier |
| `term_dictionary/term_ssl_termination.md` | note 6 | TLS-termination term → CC custom-CA / TLS-inspection-proxy trust |
| `term_dictionary/term_graduated_trust.md` | notes 2, 7 | permission-scope term → CC enforcement controls + managed permission rules |
| `term_dictionary/term_bedrock.md` | note 3 | Bedrock term → CC enterprise deployment-option comparison |
| `term_dictionary/term_observability_agent_systems.md` | note 7 | observability term → CC audit logging / ConfigChange hooks |

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 8 rows for `entry_claude_code_docs.md` (Admin/network/auth cluster); `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`; verify each note's in-degree ≥1 (G7/G8).
- Add a "Related Entry Points" cross-link from `entry_claude_code_docs.md` to `entry_infosec.md` (this cluster is the security/compliance face of the CC docs).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B14B, 2026-06-13)

- **Source re-read (Step 2)**: all 5 pages re-read from `inbox/claude_code_docs/`; measured words (admin-setup 1,609 · third-party-integrations 1,559 · network-config 744 · server-managed-settings 1,774 · authentication 1,330 = 7,016) match the master figure exactly. No >1.5× under-estimate; no re-split forced.
- **Notes**: 8 (concept 2, procedure 5, argument 1) — matches master estimate. Splits documented: admin-setup → 2 notes, third-party-integrations → 3 notes, network-config proxy material merged with third-party proxy tabs into note 5 (avoiding a split-brain proxy note), TLS/access → note 6; server-managed-settings and authentication kept single (within caps).
- **Step 2d new-term scan**: surfaced terms (managed settings, corporate proxy, LLM gateway, custom CA, mTLS, apiKeyHelper, OAuth token) all route to an existing term note, a B14B `cc_` doc note, or a home sub-plan; **0 new B14B term captures**.
- **Dedup (G-B)**: no existing `resources/documentation/claude_code/` folder yet; no `cc_` doc note duplicates an existing term note; all 16 colliding concepts (MCP, sandbox, OAuth, proxy, gateway, TLS, etc.) link existing notes rather than recreate.
- **Sections present**: Scope, Content Strategy, Source Pages (measured), Planned Notes (LOCKED), Summary Statistics & BB Distribution, Per-Note Related Notes Mapping (LOCKED), Section Coverage Map, Split Decisions, Density Re-Assessment (LOCKED), Validation Scripts, Per-Phase Validation Gate (G1–G8), Entry Point Decision, Undigested Terms Plan, Term-Note Authoring Requirements, Pacing Rules, Inlinks, Follow-up Recommendations, Pipeline Status, Augmentation Report, Review Sign-Off.
- **Status**: augmented and self-reviewed → set to `ready` (all 9 review checkpoints PASS below).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B14B contributes 8 rows under the Admin/network/auth cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2 / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | All 8 notes 450–700w, ≤4 code each — none borderline (densest is note 7 at 700w / 3 code, well under 2,500w / 6-code caps). |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: admin-setup 1,609 · third-party-integrations 1,559 · network-config 744 · server-managed-settings 1,774 · authentication 1,330 = 7,016 = master figure (±0%). |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B14B authors 0 term notes; Undigested Terms Plan routes every surfaced term; Authoring Requirements inherited from master. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status: `ready`.

**Source**: https://code.claude.com/docs/en
**Last Updated**: 2026-06-13
**Status**: Active
