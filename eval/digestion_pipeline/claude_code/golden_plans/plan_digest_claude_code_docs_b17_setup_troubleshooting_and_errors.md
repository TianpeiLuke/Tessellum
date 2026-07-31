---
title: Sub-Plan B17 — Claude Code Docs: Setup, Troubleshooting & Errors
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["setup", "troubleshoot-install", "troubleshooting", "errors"]
---

# Sub-Plan B17: Setup, Troubleshooting & Errors

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT `plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 operational lifecycle pages that cover how to install/update/uninstall Claude Code, how to fix
install-and-login failures, how to fix runtime performance/stability problems, and how to look up and
recover from runtime error messages. P2 (Phase B) — these are operational references built on the cores
(permissions B05A, context window B02A, MCP B08A, subagents B10A, settings B03A), which they link rather
than redefine. Procedure-heavy and code-block-dense, so density caps drive the split count.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 16,370 measured words. **Planned: 11 notes.**

## Content Strategy

- **Prioritize**: the recovery procedures (PATH fix, auth reset, retry/limit recovery, compaction recovery) operators reach for daily; the error-message → cause → fix mapping that makes `errors.md` a lookup table.
- **Group**: split each page by lifecycle stage and density. `setup` → install vs update vs advanced-install vs uninstall (50 code fences far exceed the ≤6 cap as one note). `troubleshoot-install` → diagnostics vs install-failures vs login/auth. `errors` → server/usage-limit vs auth vs network vs request/quality (36 fences, 9 H2, 38 sections).
- **Skip / link-out (own other sub-plans)**: settings.json keys → B03A; env-vars (`DISABLE_AUTOUPDATER`, `API_TIMEOUT_MS`, `CLAUDE_CODE_MAX_RETRIES`, `NODE_EXTRA_CA_CERTS`) → B03A; `claude doctor` / `/doctor` / debug-config → B03B; auto/permission modes → B05A; sandboxing → B05B; context window → B02A; compaction/checkpointing/`/rewind` → B02B; cloud-provider credential setup → B14A; network-config/proxy/CA → B14B; CLI flags → B03B. Referenced via links, never duplicated.
- **Glossary / new terms**: no new `cc_` glossary notes here (Pattern B); install/error vocabulary routes to existing term notes or its home sub-plan (see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| setup | /setup | 3,179 | 25 | 7 | 18 | procedure |
| troubleshoot-install | /troubleshoot-install | 5,473 | 37 | 5 | 31 | procedure |
| troubleshooting | /troubleshooting | 989 | 5 | 2 | 6 | procedure |
| errors | /errors | 6,729 | 18 | 9 | 34 | procedure/concept |

> Code column = paired ``` fences (opening fences ÷ 2: setup 50→25, troubleshoot-install 75→37, troubleshooting 5, errors 36→18). H4 sub-headers (setup `#### Verify the manifest signature`, `#### Platform code signatures`) folded under their H3.

> **H2 lists (document order):**
> - **setup**: System requirements (H3 Additional dependencies) · Install Claude Code (H3 Set up on Windows, Alpine Linux and musl-based distributions) · Verify your installation · Authenticate · Update Claude Code (H3 Auto-updates, Configure release channel, Pin a minimum version, Disable auto-updates, Update manually) · Advanced installation options (H3 Install a specific version, Install with Linux package managers, Install with npm, Binary integrity and code signing) · Uninstall Claude Code (H3 Native installation, Homebrew installation, WinGet installation, apt/dnf/apk, npm, Remove configuration files)
> - **troubleshoot-install**: Find your error · Run diagnostic checks (H3 Check network connectivity, Verify your PATH, Check for conflicting installations, Check directory permissions, Verify the binary works) · Common installation issues (H3 Install script returns HTML, command not found, curl: (56), TLS or SSL connection errors, Failed to fetch version, Wrong install command on Windows, The process cannot access the file, Install killed on low-memory Linux servers, Install hangs in Docker, Claude Desktop overrides claude command, Windows requires Git for Windows or PowerShell, does not support 32-bit Windows, Linux musl or glibc binary mismatch, Illegal instruction, dyld: cannot load on macOS, Exec format error on WSL1, npm install errors in WSL, Permission errors during installation, Native binary not found after npm install) · Login and authentication (H3 Reset your login, OAuth error: Invalid code, 403 Forbidden after login, This organization has been disabled with an active subscription, OAuth login fails in WSL2/SSH/containers, Not logged in or token expired, Bedrock/Vertex/Foundry credentials not loading) · Still stuck
> - **troubleshooting**: Performance and stability (H3 High CPU or memory usage, Auto-compaction stops with a thrashing error, Command hangs or freezes, Garbled or corrupted text in an editor's integrated terminal, Search and discovery issues, Slow or incomplete search results on WSL) · Get more help
> - **errors**: Find your error · Automatic retries · Server errors (H3 API Error: 500, Repeated 529 Overloaded, Request timed out, Auto mode cannot determine the safety of an action) · Usage limits (H3 hit your session limit, Usage credits required for 1M context, Server is temporarily limiting requests, Request rejected (429), Credit balance is too low) · Authentication errors (H3 Not logged in, Could not resolve authentication method, Invalid API key, This organization has been disabled, disabled API key authentication, disabled Claude subscription access, Routines are disabled by policy, OAuth token revoked or expired, OAuth scope requirement) · Network and connection errors (H3 Unable to connect to API, SSL certificate errors, Host not allowed in a cloud session) · Request errors (H3 Prompt is too long, Error during compaction, Request too large, Image was too large, Unable to resize image, PDF errors, Extra inputs are not permitted, There's an issue with the selected model, Claude Opus not available with Pro, thinking.type.enabled not supported, Thinking budget exceeds output limit, Tool use or thinking block mismatch, Usage Policy refusal) · Responses seem lower quality than usual · Report an error

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **11 notes** (matches master estimate). Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_install.md` | procedure | setup: System requirements, Install Claude Code (Windows/Alpine), Verify, Authenticate | 700 | Platform/hardware requirements; native installer (curl/irm/cmd), Homebrew, WinGet; Windows native vs WSL; Alpine musl deps; `claude --version`; auth-account prerequisites (links B14A). ≤6 code blocks (verbatim install one-liners). |
| 2 | `cc_update_and_release_channels.md` | procedure | setup: Update Claude Code (Auto-updates, Configure release channel, Pin a minimum version, Disable auto-updates, Update manually) | 600 | Background auto-update; `autoUpdatesChannel` latest/stable; `minimumVersion` floor + managed `requiredMinimum/MaximumVersion`; `DISABLE_AUTOUPDATER`/`DISABLE_UPDATES`; `claude update`. Settings/env keys → B03A; managed settings → B05A. |
| 3 | `cc_advanced_install_and_verification.md` | procedure | setup: Advanced installation options (specific version, Linux package managers, npm, Binary integrity and code signing) | 700 | Version/channel pinning at install; signed apt/dnf/apk repos + GPG fingerprint; npm global + optional-dep model; manifest GPG verification + per-platform code signatures. ≤6 code blocks (one representative per method). |
| 4 | `cc_uninstall.md` | procedure | setup: Uninstall Claude Code (Native, Homebrew, WinGet, apt/dnf/apk, npm, Remove configuration files) | 450 | Per-install-method removal; conflicting-install caveat (→ note 6); `~/.claude`/`.claude.json`/`.mcp.json` config cleanup + the warning that IDE/Desktop recreate `~/.claude`. |
| 5 | `cc_install_diagnostics.md` | procedure | troubleshoot-install: Run diagnostic checks (network connectivity, Verify your PATH, Check for conflicting installations, Check directory permissions, Verify the binary works) + Still stuck | 600 | The 5 ordered diagnostic checks: reach `downloads.claude.ai`; PATH `~/.local/bin`; `which -a claude` conflict detection; dir-writability; `ldd`/binary executability; escalation (`claude doctor`, `/feedback`, GitHub). |
| 6 | `cc_install_failures_reference.md` | procedure | troubleshoot-install: Find your error + Common installation issues (all 19 H3) | 900 | Symptom→fix lookup for install failures: HTML/403, command-not-found/PATH, curl (56)/(23), TLS/SSL+CA, Failed-to-fetch, wrong-shell-command, file-locked, low-mem `Killed`/swap, Docker WORKDIR, Desktop PATH override, Windows shell missing, 32-bit, musl/glibc, Illegal instruction/AVX, macOS dyld, WSL1 Exec format, npm-in-WSL, perms, native-binary-not-found. ≤6 code blocks. |
| 7 | `cc_login_authentication_troubleshooting.md` | procedure | troubleshoot-install: Login and authentication (Reset login, OAuth Invalid code, 403 Forbidden, org disabled w/ active sub, OAuth in WSL2/SSH/containers, Not logged in / token expired, Bedrock/Vertex/Foundry creds) | 700 | Login/OAuth recovery: `/logout`+relogin; copy-`c` URL fallback; 403 subscription/role check; stale `ANTHROPIC_API_KEY` override; headless-browser code paste; clock/Keychain fixes; cloud-provider CLI re-auth (`aws sts`, `gcloud`, `az`). Provider setup → B14A; precedence → B14B. |
| 8 | `cc_performance_and_stability.md` | procedure | troubleshooting: Performance and stability (High CPU/memory, Auto-compaction thrashing, Command hangs, Garbled terminal text, Search issues, WSL slow search) + Get more help | 600 | Runtime fixes: `/compact`+restart, `--safe-mode` bisect, `/heapdump`; auto-compact thrashing recovery; Ctrl+C/`--resume`; `/terminal-setup` GPU; bundled-ripgrep fallback (`USE_BUILTIN_RIPGREP=0`); WSL filesystem search. Debug-config → B03B; compaction → B02B; subagent offload → B10A. |
| 9 | `cc_server_and_usage_limit_errors.md` | concept | errors: Automatic retries + Server errors (500, 529, Request timed out, Auto mode cannot determine safety) + Usage limits (session/weekly/Opus limit, 1M-context credits, temporary throttle, 429, credit balance) | 850 | Provider-side vs account-side error families: retry-with-backoff model (10×, `CLAUDE_CODE_MAX_RETRIES`/`API_TIMEOUT_MS`); 5xx/529/timeout/auto-mode-classifier recovery; quota limits and `/usage`/`/usage-credits`/`/model` recovery. ≤6 code blocks (error samples). |
| 10 | `cc_authentication_and_network_errors.md` | procedure | errors: Authentication errors (9 H3) + Network and connection errors (Unable to connect, SSL cert, Host not allowed in cloud session) | 850 | Auth-error recovery: `/login`/`/logout`, credential precedence, `ANTHROPIC_API_KEY` overrides, org/policy disables (`oauth_org_not_allowed`); network: `ECONNREFUSED/RESET`, `NODE_EXTRA_CA_CERTS` (never `NODE_TLS_REJECT_UNAUTHORIZED=0`), cloud-session `host_not_allowed` allowlist. Network-config → B14B; precedence → B14B. |
| 11 | `cc_request_and_quality_errors.md` | procedure | errors: Request errors (13 H3) + Responses seem lower quality than usual + Report an error | 950 | Request-content errors: prompt-too-long/compaction-too-long (`/compact`/`/clear`/`/context`), request-too-large/image/PDF, beta-header strip, model-not-found/Opus-not-in-plan, thinking config, tool/thinking-block mismatch (`/rewind`), Usage-Policy refusal; quality triage (`/model`/`/effort`/`/context`/`/doctor`); `/feedback`. ≤6 code blocks. Context window → B02A; checkpointing/`/rewind` → B02B; model-config → B03B. |

**Estimate: 11 notes** — procedure ×10 (notes 1–8, 10, 11), concept ×1 (note 9). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (16,370 words). New `cc_` notes: 11. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~7,900 (avg ~720/note). Code blocks: each note ≤6 representative verbatim snippets (source is fence-dense; full per-platform variants are linked to source, not all inlined — keeps the ≤6 cap).
- **Building Block Distribution**: procedure ×10 (notes 1,2,3,4,5,6,7,8,10,11) · concept ×1 (note 9 — taxonomy of error families + retry model). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_install` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding CLI/tool; relevance: this note IS the install procedure for Claude Code itself, so the product term is its definitional anchor.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the Node.js package manager and registry; relevance: the note documents `npm install -g @anthropic-ai/claude-code` (Node 18+) as one install path and its per-platform optional-dependency model.
- [Docker — Container Platform](../../term_dictionary/term_docker.md) — what-it-is: platform for running apps in isolated containers; relevance: the note's WSL/containerized setup and the install-in-container caveat (WORKDIR scan) tie installation behavior to container runtimes.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated execution environment that restricts an agent's reach; relevance: the note's Windows table marks WSL 2 as "Sandboxing supported" vs native Windows "not supported," making the install choice a sandbox-capability decision.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime that wraps an LLM with tools/context/execution; relevance: installing Claude Code installs the harness binary that launches `claude` and wires the model to the local project.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: the category of tools that plan/edit/run/verify code autonomously; relevance: the note installs precisely such an agent, and the account-prerequisite section (Pro/Max/Team/Enterprise/Console or API provider) gates access to that capability.

### 2. `cc_update_and_release_channels` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding tool being updated; relevance: the note governs how the Claude Code binary stays current across native/Homebrew/WinGet/Linux installs.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the Node package manager; relevance: the note's manual-update guidance covers `npm install -g @anthropic-ai/claude-code@latest` and warns against `npm update -g` respecting the original semver range.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive, settings-scoped control over what an agent may do; relevance: the note's managed-settings enforcement of `requiredMinimum/MaximumVersion` across an org is an admin-imposed trust/governance control over the update path.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the agent runtime binary; relevance: each update replaces the harness binary, and the release-channel choice (latest vs stable) controls how new harness behavior reaches users.
- [Version Set](../../term_dictionary/term_version_set.md) — what-it-is: a single-source-of-truth pin for which version of each dependency builds; relevance: the note's `minimumVersion` floor and channel-vs-pin interaction is the Claude Code analog of pinning a version to avoid regressions, framing the same dependency-version-control problem.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: the autonomous-agent product category; relevance: auto-updates keep the autonomous agent on a model/feature set that matches the docs, and the stable channel exists to skip releases with major regressions in that agent.

### 3. `cc_advanced_install_and_verification` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the tool being installed/verified; relevance: this note covers Claude Code's version-pinned installs, Linux repos, npm, and binary-integrity verification.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the Node package manager and optional-dependency mechanism; relevance: the note details the npm install path, the eight per-platform optional-dependency packages, and the postinstall link step that delivers the native binary.
- [Docker — Container Platform](../../term_dictionary/term_docker.md) — what-it-is: the container platform; relevance: signed apt/dnf/apk repos are the standard way to install Claude Code into Linux container images reproducibly, the install method this note configures.
- [Secure PyPI](../../term_dictionary/term_secure_pypi.md) — what-it-is: a signed/verified package-registry trust model; relevance: the note's GPG-signed apt/dnf/apk repositories and signature verification before trusting the key is the same signed-registry supply-chain-trust pattern this term describes.
- [Idempotency](../../term_dictionary/term_idempotency.md) — what-it-is: an operation that yields the same result however many times it is applied; relevance: the note's manifest-checksum + GPG-signature verification step is an idempotent integrity check that can be re-run safely to re-confirm a binary matches the signed manifest.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — what-it-is: a server forwarding client requests to backends, often doing TLS termination; relevance: the note notes corporate proxies/mirrors must mirror all platform packages and route the signed-repo downloads, making proxy/mirror configuration part of advanced install.

### 4. `cc_uninstall` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the tool being removed; relevance: this note is the per-install-method uninstall procedure for Claude Code itself.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the Node package manager; relevance: the note covers `npm uninstall -g @anthropic-ai/claude-code` and removing the legacy `~/.claude/local` npm install.
- [Docker — Container Platform](../../term_dictionary/term_docker.md) — what-it-is: the container platform; relevance: the note's apt/dnf/apk package + repository-config removal is the cleanup needed to rebuild a clean container image without Claude Code.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — what-it-is: the protocol/config for connecting external tool servers; relevance: the note's config-cleanup step deletes `.mcp.json` and warns that removing `~/.claude` deletes all MCP server configurations.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what-it-is: persisted per-project learnings/preferences across sessions; relevance: the note warns that deleting `~/.claude`/`.claude` removes session history and the memory state Claude accumulated, the agentic-memory store this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the agent runtime binary + its config tree; relevance: the note removes both the harness binary and the `~/.claude` config tree that the harness, VS Code extension, JetBrains plugin, and Desktop app all write to.

### 5. `cc_install_diagnostics` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the tool being diagnosed; relevance: this note is the ordered diagnostic-check procedure for a Claude Code install that won't run.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the Node package manager; relevance: the conflict-detection check distinguishes the native `~/.local/bin` install from `~/.claude/local` legacy npm and `npm -g ls` global installs.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — what-it-is: an intermediary forwarding/terminating client traffic; relevance: the first diagnostic check reaches `downloads.claude.ai` and the note attributes failures to corporate proxies/firewalls intercepting the connection.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — what-it-is: the OAuth access/refresh token mechanism; relevance: the "Still stuck" escalation and binary-works check feed into login diagnosis, where an expired/invalid OAuth token is a common downstream failure after a working binary.
- [Docker — Container Platform](../../term_dictionary/term_docker.md) — what-it-is: the container platform; relevance: the directory-permission and binary-executability checks (`ldd`, ownership) are exactly the failure points seen when diagnosing a containerized or non-root install.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the agent runtime binary; relevance: the "Verify the binary works" check confirms the harness binary exists, is on PATH, is executable, and has its shared libraries resolved before any agent session can start.

### 6. `cc_install_failures_reference` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the tool whose install fails; relevance: this note is the symptom→fix lookup table for every documented Claude Code install failure.
- [NPM (Node Package Manager)](../../term_dictionary/term_npm.md) — what-it-is: the Node package manager + optional-deps; relevance: several rows (native-binary-not-found, npm-in-WSL OS detection, `--omit=optional`, `sudo npm` permission risk) are npm-install-path failures and their fixes.
- [Docker — Container Platform](../../term_dictionary/term_docker.md) — what-it-is: the container platform; relevance: the "Install hangs in Docker" row's root cause (installer scanning `/` from root) and the `WORKDIR`/`--memory` fixes are container-specific install failures.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — what-it-is: a TLS-terminating intermediary; relevance: the TLS/SSL-error and 403/HTML rows are caused by corporate proxies performing TLS inspection, fixed with `--cacert`/`NODE_EXTRA_CA_CERTS`/`HTTPS_PROXY`.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated/restricted execution environment; relevance: the WSL1/WSL2, Docker, and endpoint-security (AppLocker/EDR blocking `cmd.exe`) failure rows are install problems specific to sandboxed/restricted execution contexts.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the native agent binary; relevance: the musl/glibc mismatch, Illegal instruction/AVX, macOS dyld, and Exec-format-error rows are all native-harness-binary compatibility failures the note maps to fixes.

### 7. `cc_login_authentication_troubleshooting` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the tool you sign in to; relevance: this note is the login/OAuth-failure recovery procedure for Claude Code authentication.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — what-it-is: the OAuth access/refresh-token decoupling; relevance: the note's "Invalid code," "token expired," and re-`/login` flows are exactly OAuth-token issuance/refresh failures and their resolution.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — what-it-is: a named credential record (api_key/token/oauth/aws-sdk) an agent runtime selects and validates; relevance: the note's precedence story (stale `ANTHROPIC_API_KEY` overriding subscription OAuth, cloud-provider creds) is the multi-credential selection/validation problem this term formalizes.
- [CloudAuth](../../term_dictionary/term_cloudauth.md) — what-it-is: an authentication protocol for service-to-service credential exchange; relevance: the note's Bedrock/Vertex/Foundry credential-not-loading section depends on the cloud provider CLI being authenticated (`aws sts`, `gcloud auth`, `az login`) in the launching shell, the same provider-auth concern.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated/remote execution context; relevance: the note's WSL2/SSH/container login section addresses how the OAuth browser callback fails inside isolated/remote environments and how to paste the code instead.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the agent runtime; relevance: the note's macOS-Keychain and system-clock fixes are about the harness's ability to persist and validate the credentials it stores for the session.

### 8. `cc_performance_and_stability` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the running agent tool; relevance: this note is the runtime performance/stability fix procedure for a working Claude Code session.
- [Compaction](../../term_dictionary/term_compaction.md) — what-it-is: automatic context-summarization when the window fills; relevance: the note's "auto-compaction stops with a thrashing error" section is a direct compaction-failure-recovery procedure (`/compact` with a focus, smaller reads, `/clear`).
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the fixed token budget holding conversation/files/memory; relevance: the high-CPU/memory and thrashing fixes all reduce context-window pressure (`/compact` regularly, read files in chunks, offload to a subagent).
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a delegated worker with its own isolated context window; relevance: the note recommends moving large-file work to a subagent so it runs in a separate context window and doesn't refill the main one.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the agent runtime process; relevance: the `--safe-mode` bisect, `/heapdump`, and restart-between-tasks steps diagnose and recover the harness process's resource usage and customization-induced slowdowns.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: on-demand packaged knowledge/workflows the agent loads; relevance: the search-and-discovery section notes custom skills (and `@file`/custom agents) rely on `ripgrep`, and `--safe-mode` disables skills/MCP/hooks to isolate which customization causes high usage.

### 9. `cc_server_and_usage_limit_errors` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agent that surfaces these errors; relevance: this note classifies the server-side and account-quota error families Claude Code displays and how each recovers.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — what-it-is: rejecting requests over a per-window threshold; relevance: the note's 429 "Request rejected" and per-key/per-project limits are direct rate-limiting errors with tier/concurrency-reduction fixes.
- [Throttling](../../term_dictionary/term_throttling.md) — what-it-is: deliberate request-rate restriction under load; relevance: the note's "Server is temporarily limiting requests (not your usage limit)" and 529 Overloaded are server-side throttle/capacity signals distinct from account quota.
- [Exponential Backoff](../../term_dictionary/term_exponential_backoff.md) — what-it-is: doubling the wait between retries; relevance: the "Automatic retries" section the note opens with is exactly retry-with-exponential-backoff (10× attempts, tunable via `CLAUDE_CODE_MAX_RETRIES`).
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the model's token budget; relevance: the "Usage credits required for 1M context" and "Auto mode classifier transcript exceeded context window" errors are context-window-capacity/entitlement errors the note covers (`/model`, `/compact`).
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive auto-approval of agent actions; relevance: the "Auto mode cannot determine the safety of an action" server errors come from auto mode's safety classifier failing, the graduated-trust mechanism whose fallback to manual approval the note explains.

### 10. `cc_authentication_and_network_errors` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agent surfacing these errors; relevance: this note maps Claude Code's runtime authentication and network error messages to their recovery commands.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — what-it-is: OAuth access/refresh tokens; relevance: the "OAuth token revoked/expired," "Not logged in," and scope-requirement errors are OAuth-token lifecycle failures the note recovers with `/login`/`/logout`.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — what-it-is: a named credential record an agent selects/validates; relevance: the note's authentication-precedence story (`/status`, `ANTHROPIC_API_KEY` vs OAuth vs `apiKeyHelper` vs cloud creds, "Could not resolve authentication method") is the multi-credential selection problem this term defines.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — what-it-is: per-window request rejection; relevance: the auth section's "Invalid API key"/org-disabled fixes route via `/status` to confirm the active credential, which also resolves 429s caused by a stray low-tier key routing requests.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — what-it-is: a TLS-terminating intermediary; relevance: the "SSL certificate verification failed"/"Self-signed certificate detected" network errors come from a proxy/security appliance intercepting TLS, fixed with `NODE_EXTRA_CA_CERTS`.
- [Sandbox](../../term_dictionary/term_sandbox.md) — what-it-is: an isolated, network-policy-restricted execution environment; relevance: the "Host not allowed in a cloud session" (`x-deny-reason: host_not_allowed`) error is the sandboxed cloud environment's outbound-allowlist blocking a host, fixed by editing the environment's network access.
- [CloudAuth](../../term_dictionary/term_cloudauth.md) — what-it-is: service-to-service auth protocol; relevance: the note's cloud-provider auth errors (and the `host_not_allowed` cloud-session case) depend on provider credential/network setup, the provider-auth concern this term covers.

### 11. `cc_request_and_quality_errors` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agent surfacing these errors; relevance: this note maps request-content errors and response-quality symptoms to recovery commands.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the model's token budget; relevance: "Prompt is too long," "Request too large" vs context-limit distinction, and `/context` triage are all context-window-capacity errors the note resolves.
- [Compaction](../../term_dictionary/term_compaction.md) — what-it-is: automatic context summarization; relevance: "Error during compaction: Conversation too long" is a compaction-failure error, and the note's `/compact`/Esc-twice/`/clear` recovery is the compaction-recovery procedure.
- [Chain-of-Thought Reasoning](../../term_dictionary/term_chain_of_thought.md) — what-it-is: explicit step-by-step model reasoning (extended thinking); relevance: "thinking.type.enabled not supported," "Thinking budget exceeds output limit," and the `/effort` quality check are extended-thinking/effort configuration errors this term grounds.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a delegated isolated-context worker; relevance: the "Prompt is too long" fix notes subagents inherit every MCP tool definition and can fill their context before the first turn, and the quality section ties large subagent definitions to context pressure.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — what-it-is: the protocol for connecting external tool servers; relevance: the note's prompt-too-long fix is to disable unused MCP servers (`/mcp disable`) to drop their tool definitions, and "Extra inputs are not permitted" is a gateway stripping the beta header MCP-adjacent fields ride on.
- [Guardrails](../../term_dictionary/term_guardrails.md) — what-it-is: safety constraints that block disallowed model behavior; relevance: the "Usage Policy refusal" error is a guardrail/policy check declining the request, and the note's rewind/rephrase/new-session recovery is how to work around a triggered guardrail.

> **Term screening note:** `term_secrets_manager` (AWS Secrets Manager) was screened as an Amazon-product
> false positive and dropped (no Claude Code coupling). `term_cloudauth` is kept only where genuinely about
> provider credential exchange (notes 7, 10). `term_version_set` is kept only in note 2, where the
> with no placeholder or commented lines.

## Section Coverage Map

```
setup.md
├── System requirements (+ Additional dependencies) ─ → note 1 (cc_install)
├── Install Claude Code ─────────────────────────────── → note 1
│   ├── Set up on Windows ───────────────────────────── → note 1
│   └── Alpine Linux and musl-based distributions ───── → note 1
├── Verify your installation ────────────────────────── → note 1 (claude doctor → linked B03B)
├── Authenticate ────────────────────────────────────── → note 1 (account types → linked B14A/B14B)
├── Update Claude Code ──────────────────────────────── → note 2 (cc_update_and_release_channels)
│   ├── Auto-updates ────────────────────────────────── → note 2
│   ├── Configure release channel ───────────────────── → note 2
│   ├── Pin a minimum version ───────────────────────── → note 2 (managed settings → linked B05A)
│   ├── Disable auto-updates ────────────────────────── → note 2 (env vars → linked B03A)
│   └── Update manually ─────────────────────────────── → note 2
├── Advanced installation options ───────────────────── → note 3 (cc_advanced_install_and_verification)
│   ├── Install a specific version ──────────────────── → note 3
│   ├── Install with Linux package managers ─────────── → note 3
│   ├── Install with npm ────────────────────────────── → note 3
│   └── Binary integrity and code signing ───────────── → note 3
└── Uninstall Claude Code ───────────────────────────── → note 4 (cc_uninstall)
    ├── Native / Homebrew / WinGet / apt-dnf-apk / npm ─ → note 4
    └── Remove configuration files ──────────────────── → note 4
troubleshoot-install.md
├── Find your error (router table) ──────────────────── → note 6 (cc_install_failures_reference, as lookup)
├── Run diagnostic checks ───────────────────────────── → note 5 (cc_install_diagnostics)
│   ├── Check network connectivity ─────────────────── → note 5
│   ├── Verify your PATH ────────────────────────────── → note 5
│   ├── Check for conflicting installations ─────────── → note 5
│   ├── Check directory permissions ─────────────────── → note 5
│   └── Verify the binary works ─────────────────────── → note 5
├── Common installation issues (19 H3) ──────────────── → note 6
├── Login and authentication (7 H3) ─────────────────── → note 7 (cc_login_authentication_troubleshooting)
│   └── Bedrock/Vertex/Foundry credentials not loading ─ → note 7 (provider setup → linked B14A)
└── Still stuck ─────────────────────────────────────── → note 5 (escalation)
troubleshooting.md
├── Performance and stability ───────────────────────── → note 8 (cc_performance_and_stability)
│   ├── High CPU or memory usage ────────────────────── → note 8
│   ├── Auto-compaction stops with a thrashing error ── → note 8 (compaction → linked B02B)
│   ├── Command hangs or freezes ────────────────────── → note 8
│   ├── Garbled or corrupted text in integrated terminal → note 8 (terminal-config → linked B04A)
│   ├── Search and discovery issues ─────────────────── → note 8
│   └── Slow or incomplete search results on WSL ────── → note 8
└── Get more help ───────────────────────────────────── → note 8 (doctor/feedback → linked B03B)
errors.md
├── Find your error (router table) ──────────────────── → notes 9/10/11 (routes to the matching family)
├── Automatic retries ───────────────────────────────── → note 9 (cc_server_and_usage_limit_errors)
├── Server errors (500, 529, timeout, auto-mode) ────── → note 9
├── Usage limits (session/1M/throttle/429/credit) ───── → note 9 (auto mode → linked B05A; usage → linked B02A)
├── Authentication errors (9 H3) ────────────────────── → note 10 (cc_authentication_and_network_errors)
├── Network and connection errors (3 H3) ────────────── → note 10 (network-config → linked B14B)
├── Request errors (13 H3) ──────────────────────────── → note 11 (cc_request_and_quality_errors)
├── Responses seem lower quality than usual ─────────── → note 11 (model-config → linked B03B)
└── Report an error ─────────────────────────────────── → note 11 (feedback/doctor → linked B03B)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| setup (3.2Kw, 50 code fences, 7 H2) | notes 1,2,3,4 | one note would hold 25 paired code blocks (>>6 cap); install vs update vs advanced-install vs uninstall are distinct lifecycle procedures with no shared body |
| troubleshoot-install (5.5Kw, 37 code fences, 31 H3) | notes 5,6,7 | exceeds word + code caps as one note; diagnostics (ordered procedure) vs install-failure lookup (symptom→fix) vs login/auth differ in shape and BB granularity |
| troubleshooting (989w, 6 H3) | note 8 (single) | small, single topic (performance/stability); no split needed |
| errors (6.7Kw, 36 code fences, 34 H3) | notes 9,10,11 | far exceeds word + code caps; the page's own H2 families (server/usage-limit vs auth/network vs request/quality) are the natural BB-coherent boundaries — note 9 is a concept taxonomy + retry model, 10/11 are recovery procedures |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_install | procedure | 700 | 6 | ✅ |
| 2 | cc_update_and_release_channels | procedure | 600 | 4 | ✅ |
| 3 | cc_advanced_install_and_verification | procedure | 700 | 6 | ✅ |
| 4 | cc_uninstall | procedure | 450 | 5 | ✅ |
| 5 | cc_install_diagnostics | procedure | 600 | 6 | ✅ |
| 6 | cc_install_failures_reference | procedure | 900 | 6 | ✅ |
| 7 | cc_login_authentication_troubleshooting | procedure | 700 | 5 | ✅ |
| 8 | cc_performance_and_stability | procedure | 600 | 4 | ✅ |
| 9 | cc_server_and_usage_limit_errors | concept | 850 | 6 | ✅ |
| 10 | cc_authentication_and_network_errors | procedure | 850 | 6 | ✅ |
| 11 | cc_request_and_quality_errors | procedure | 950 | 6 | ✅ |

All 11 notes are within the ≤2,500 word / ≤6 code / ≤400 line caps. The source is fence-dense, so each note inlines only a representative verbatim snippet per method/error and links the full per-platform variant set to the source page (keeps ≤6 without losing the symptom→fix mapping). No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_install cc_update_and_release_channels cc_advanced_install_and_verification cc_uninstall cc_install_diagnostics cc_install_failures_reference cc_login_authentication_troubleshooting cc_performance_and_stability cc_server_and_usage_limit_errors cc_authentication_and_network_errors cc_request_and_quality_errors"
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

Single phase (11 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucinated commands/error strings | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 11 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability (inbound) | each of the 11 notes RECEIVES ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (entry-point) | each note linked from `entry_claude_code_docs.md` (its B17 rows) | DB query + entry-point review |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`
(created as a pre-step before the first sub-plan executes); this sub-plan **contributes its 11 rows** under a
"Setup, Troubleshooting & Errors" cluster + increments the BB-distribution counts (procedure +10, concept +1).
The hub itself is back-linked from `entry_gen_ai_dev.md` and `term_claude_code.md` (master Entry Points to Update).

## Undigested Terms Plan (Step 4e)

B17 creates **0 new `term_dictionary` notes**. Install/troubleshooting/error vocabulary is either an
operational instruction (not a vocabulary term), an existing substantive term note (link), or owned by a
home sub-plan (Pattern B). Dedup checked across `term_dictionary/` AND `resources/documentation/`.

| Term / phrase in pages | Disposition |
|---|---|
| MCP / Subagent / Sandbox / Compaction / Context window / Skills | existing term notes (link) — not recreated |
| OAuth token / API key precedence / auth profile | link `term_oauth_token` + `term_auth_profile` (exist) |
| Rate limit / 429 / throttle / overloaded / retry backoff | link `term_rate_limiting` + `term_throttling` + `term_exponential_backoff` (exist) |
| Extended thinking / effort level | link `term_chain_of_thought` (exists); effort-level CLI → B03B |
| Permission / auto mode | link `term_graduated_trust` (exists); full treatment → B05A |
| npm / Docker / Node / package managers | link `term_npm` + `term_docker` (exist); Node has no term note and is a runtime dependency mention, not a CC vocabulary term — no capture |
| `claude doctor` / `/doctor` / `--safe-mode` / debug-config | operational commands → owned by B03B (debug-your-config) — linked, not a term |
| env vars (`DISABLE_AUTOUPDATER`, `API_TIMEOUT_MS`, `NODE_EXTRA_CA_CERTS`, `USE_BUILTIN_RIPGREP`, …) | owned by B03A (env-vars) — linked, not captured |
| settings keys (`autoUpdatesChannel`, `minimumVersion`, `apiKeyHelper`) | owned by B03A (settings) — linked, not captured |
| `/rewind` / checkpoint | link `term_regular_checkpointing` (exists); full treatment → B02B |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/error-code
strings/captions for newly-surfaced terms. Candidates considered and rejected as new captures: **"ripgrep"**
(bundled binary / search dependency — operational mention, no standalone vocabulary need; owned by B03B
tools-reference search), **"AVX instruction set"** / **"musl vs glibc"** / **"OOM killer"** (OS/hardware
concepts, not Claude Code vocabulary; explained inline in note 6), **"manifest signature / GPG fingerprint"**
(covered by linking `term_secure_pypi` for the signed-registry pattern; explained inline in note 3),
**"auto mode classifier"** (a Claude Code feature owned by B05A permission-modes / errors note 9). **Dedup
check passed: no candidate duplicates an existing term, and none is a cross-cutting glossary term lacking a
home.** **0 new B17 `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B17 authors zero term notes, so there are no
slugs to audit for specificity or collision. The collision check that matters here (do the install/error
concepts duplicate existing notes?) was performed: `term_npm`, `term_docker`, `term_oauth_token`,
`term_auth_profile`, `term_rate_limiting`, `term_throttling`, `term_exponential_backoff`, `term_idempotency`,
`term_mcp`, `term_subagent`, `term_sandbox`, `term_compaction`, `term_context_window`, `term_skills`,
`term_chain_of_thought`, `term_graduated_trust`, `term_agent_harness`, `term_claude_code`,
`term_autonomous_coding_agents`, `term_agentic_memory`, `term_reverse_proxy`, `term_secure_pypi`,
`term_version_set`, `term_cloudauth`, `term_guardrails` all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for B17** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory; install one-liners, error
  strings, command names, env-var names, and fingerprints must be copied verbatim (G2).
- Code blocks verbatim; inline only a representative snippet per method/error to stay ≤6 per note, link the
  full per-platform variant set to the source. One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 6, 11 | tool note → CC install / install-failure reference / runtime errors |
| `term_dictionary/term_npm.md` | notes 1, 3 | npm term → CC npm install path + optional-dependency model |
| `term_dictionary/term_oauth_token.md` | notes 7, 10 | OAuth-token term → CC login/auth troubleshooting + runtime auth errors |
| `term_dictionary/term_rate_limiting.md` | note 9 | rate-limiting term → CC 429 / usage-limit error recovery |
| `term_dictionary/term_compaction.md` | notes 8, 11 | compaction term → CC thrashing recovery + compaction-too-long error |
| `documentation/tutorials/tutorial_claude_code_getting_started.md` | note 1 | getting-started tutorial → docs install procedure (confirm exact filename at finalization; else use docs overview cc_overview) |
| `0_entry_points/entry_claude_code_docs.md` | all 11 | entry-point hub → every B17 note (G8) |

## Follow-up Recommendations

- After the 11 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 11 rows for `entry_claude_code_docs.md` under a "Setup, Troubleshooting & Errors" cluster; `/tessellum-check-broken-links`; verify in-degree ≥1 for every note (G7) and entry-point linkage (G8) before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B17, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read from `inbox/claude_code_docs/`; measured words match the master's total (setup 3,179 · troubleshoot-install 5,473 · troubleshooting 989 · errors 6,729 = 16,370). Code fences re-counted (setup 25, troubleshoot-install 37, troubleshooting 5, errors 18 paired). No >1.5× under-estimate vs the master's 11-note figure; no re-split forced beyond the four documented.
- **Notes**: 11 (procedure 10, concept 1) — matches master estimate. Split count driven by the ≤6-code / ≤2,500-word caps (setup→4, troubleshoot-install→3, troubleshooting→1, errors→3).
- **Step 2d new-term scan**: candidates ripgrep / AVX / musl-glibc / OOM / manifest-signature / auto-mode-classifier all rejected as captures (operational/OS mentions or owned by B03B/B05A); **0 new B17 term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G5/G7/G8 verification rows, Split Decisions, Density Re-Assessment.
- **28-item checklist**: PASS (term-note items N/A — B17 authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and reviewed; set to `ready` by the Review Sign-Off below.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7 in-degree ≥1 and G8 entry-point linkage. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B17 contributes 11 rows under a Setup/Troubleshooting/Errors cluster; hub back-linked from `entry_gen_ai_dev.md` + `term_claude_code.md`. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 11 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + body (`## Overview` / source-mirrored H2 / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer) match the master Format Definition verbatim, derived from existing `documentation/` notes. |
| CP6 | Borderline density → split | ✅ PASS | Largest note (11) is 950w / 6 code — under caps; the fence-dense pages were split aggressively (4 pages → 11 notes) precisely to avoid borderline code-block density. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Re-measured: setup 3,179 · troubleshoot-install 5,473 · troubleshooting 989 · errors 6,729 = 16,370 = master figure. Code fences re-counted from `grep '^```'`. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B17 authors 0 term notes; Undigested Terms Plan routes all install/error vocabulary (link existing / home sub-plan); Authoring Requirements inherited. Dedup checked across term_dictionary AND documentation/. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented — 25 existing terms linked, not recreated; AWS-specific false positives (secrets_manager) screened out. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.
