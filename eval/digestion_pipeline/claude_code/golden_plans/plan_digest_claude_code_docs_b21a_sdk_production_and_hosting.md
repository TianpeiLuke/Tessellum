---
title: Sub-Plan B21A — Claude Code Docs: SDK Production & Hosting
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/hosting", "agent-sdk/secure-deployment", "agent-sdk/observability", "agent-sdk/cost-tracking"]
---

# Sub-Plan B21A: SDK Production & Hosting

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 Agent SDK operations pages that cover taking an SDK agent to production: how to host the
subprocess-based runtime, how to harden it (isolation, credentials, network), how to instrument it with
OpenTelemetry, and how to track token cost. P3 (Phase C) — this is specialized SDK-operations material
built on the SDK cores (B19/B20); it references but does not redefine the agent-loop, sessions, MCP,
subagents, and permissions vocabulary.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 9,512 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the production-operations decisions a team makes when deploying the SDK — session
  lifecycle pattern, container provisioning/scaling, isolation strength, credential-proxy pattern, OTEL
  telemetry, and token-cost accounting. These are the load-bearing "how do I run this in prod" answers.
- **Group**: split the two large pages by BB. `hosting` (2.6Kw, 6 H2) splits into subprocess-model
  (concept) / session-patterns (concept) / provisioning+production+isolation (procedure). `secure-deployment`
  (3.0Kw, 7 H2) splits into security-principles (argument) / isolation-technologies (concept) /
  credential+filesystem-controls (procedure). `observability` and `cost-tracking` each map to one procedure
  note.
- **Skip / link-out (own other sub-plans)**: `SessionStore`/session storage → B19B (`session-storage.md`);
  Sessions/resume/fork API → B19B (`sessions.md`); subagents/Task tool → B20B; hooks → B20C; MCP → B20A;
  permissions system → B05A/B20C; sandboxing built-in → B05B (`sandboxing.md`); prompt caching feature →
  B02A (`prompt-caching.md`); Monitoring reference (metric/event catalog) → B15B (`monitoring-usage.md`);
  Bedrock/Vertex/Foundry providers → B14A. Referenced via links, never duplicated.
- **Glossary**: not re-digested into `cc_` notes — terms route to existing term notes / their home
  sub-plan (Pattern B; see Undigested Terms Plan). No new `term_dictionary` captures.

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).
Code-fence counts are top-level ```` ``` ```` pairs; `<CodeGroup>` TS/Python pairs in `hosting`,
`observability`, and `cost-tracking` add further inline examples (kept ≤6 per digest note).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| hosting | /agent-sdk/hosting | 2,635 | 3 (+3 CodeGroup) | 6 | 15 | concept + procedure |
| secure-deployment | /agent-sdk/secure-deployment | 3,050 | 8 | 7 | 14 | argument + concept + procedure |
| observability | /agent-sdk/observability | 2,002 | 0 (6 CodeGroup) | 8 | 1 | procedure |
| cost-tracking | /agent-sdk/cost-tracking | 1,825 | 2 (+3 CodeGroup) | 6 | 6 | procedure |

> **H2 lists (document order):**
> - **hosting**: The subprocess model (H3 State that lives on local disk) · Choose a session pattern (H3 Ephemeral / Long-running / Hybrid / Multi-agent container) · Provision the container (H3 Container-based sandboxing, Runtime dependencies, Resources, Network) · Handle production concerns (H3 Session and state persistence, Observability, Auth and secrets, Scaling and concurrency, Cost, Multi-tenant isolation) · Known limitations · Next steps
> - **secure-deployment**: Threat model · Built-in security features · Security principles (H3 Security boundaries, Least privilege, Defense in depth) · Isolation technologies (H3 Sandbox runtime, Containers, gVisor, Virtual machines, Cloud deployments) · Credential management (H3 The proxy pattern, Configuring Claude Code to use a proxy, Implementing a proxy, Credentials for other services) · Filesystem configuration (H3 Read-only code mounting, Writable locations) · Further reading
> - **observability**: How telemetry flows from the SDK · Enable telemetry export (H3 Flush telemetry from short-lived calls) · Read agent traces · Link traces to your application · Tag telemetry from your agent · Attribute actions to your end users · Control sensitive data in exports · Related documentation
> - **cost-tracking**: Understand token usage · Get the total cost of a query · Track per-step and per-model usage (H3 Track per-step usage, Break down usage per model) · Accumulate costs across multiple calls · Handle errors, caching, and token discrepancies (H3 Resolve output token discrepancies, Track costs on failed conversations, Track cache tokens, Extend the prompt cache TTL to one hour) · Related documentation

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Prefix `cc_`, target
`resources/documentation/claude_code/`. **8 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_sdk_subprocess_model.md` | concept | hosting: The subprocess model, State that lives on local disk | 500 | One agent session = one `claude` CLI subprocess over stdio owning shell/cwd/JSONL transcripts; `cwd` per `query()`; the three local-disk state kinds (transcripts, CLAUDE.md, working-dir artifacts) lost on restart → persist via `SessionStore` (link B19B). |
| 2 | `cc_sdk_session_patterns.md` | concept | hosting: Choose a session pattern (Ephemeral / Long-running / Hybrid / Multi-agent) | 600 | The four container-lifecycle patterns vs session lifetime, with example workloads and the SDK primitive each uses (`streamInput`/`startup`, `ClaudeSDKClient`, `resume`+`sessionStore`, per-agent cwd). |
| 3 | `cc_sdk_hosting_provisioning_and_scaling.md` | procedure | hosting: Provision the container, Handle production concerns, Known limitations | 700 | Provisioning (sandboxed container, runtime deps, 1GiB/5GiB/1CPU floor, network egress/inbound) + production decisions (state persistence, observability hook-in, auth/secrets, the agents-per-host RAM formula + consistent-hashing pin, cost, multi-tenant isolation summary) + the 4 known limitations. |
| 4 | `cc_sdk_secure_deployment_principles.md` | argument | secure-deployment: intro, Threat model, Built-in security features, Security principles | 550 | Why agents need isolation/least-privilege/defense-in-depth (dynamic actions influenced by processed content → prompt-injection risk); the built-in features (permissions, command AST parsing, web-search summarization, sandbox mode); the security-boundary + least-privilege table + layering principles. |
| 5 | `cc_sdk_isolation_technologies.md` | concept | secure-deployment: Isolation technologies (Sandbox runtime, Containers, gVisor, VMs, Cloud) | 650 | The isolation strength/overhead/complexity tradeoff table; sandbox-runtime (bubblewrap/Seatbelt + proxy, no TLS inspection); hardened Docker flags + Unix-socket-only egress; gVisor userspace syscall interception + perf table; Firecracker microVM + vsock; cloud private-subnet + Envoy proxy. |
| 6 | `cc_sdk_credential_and_filesystem_controls.md` | procedure | secure-deployment: Credential management, Filesystem configuration | 650 | The credential-proxy pattern (agent never sees the key); `ANTHROPIC_BASE_URL` vs `HTTP_PROXY`/`HTTPS_PROXY`; custom-tool vs TLS-terminating-proxy routing for non-Claude services; read-only code mounts + sensitive-file exclusion list; tmpfs/overlay/volume writable options. |
| 7 | `cc_sdk_observability_opentelemetry.md` | procedure | observability: all 7 content H2 | 700 | OTEL flow (CLI emits, SDK passes env through); the 3-signal switch table; `CLAUDE_CODE_ENABLE_TELEMETRY` + OTLP exporter config + flush-interval tuning; the four `claude_code.*` span names + nesting; W3C trace-context propagation; `OTEL_SERVICE_NAME`/resource attrs + end-user attribution; the content opt-in flags. |
| 8 | `cc_sdk_cost_and_usage_tracking.md` | procedure | cost-tracking: all 5 content H2 | 700 | `total_cost_usd`/`costUSD` are client-side estimates (not billing); query/step/session scoping; read total from the result message; dedup per-step usage by message ID; per-model `modelUsage`; accumulate across calls yourself; cache-token fields + `ENABLE_PROMPT_CACHING_1H` TTL. |

**Estimate: 8 notes** — concept ×3 (notes 1,2,5), argument ×1 (note 4), procedure ×4 (notes 3,6,7,8). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (9,512 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,050 (avg ~630/note). Code blocks: verbatim SDK snippets kept where
  load-bearing (subprocess `cwd`, hybrid `resume`, multi-tenant `env`, OTEL `.env`, docker hardening,
  cost dedup loop), ≤6 per note.
- **Building Block Distribution**: concept ×3 (notes 1,2,5) · argument ×1 (note 4) · procedure ×4
  (notes 3,6,7,8). No model/empirical_observation in this sub-plan.
- Cross-refs: **≥6 relevancy-selected term notes per note** (56 term-note links, 34 distinct
  entry-point back-link at finalization.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> e.g. `term_trace` = "TRACE post-bypass analysis", not OTEL tracing — excluded).

### 1. `cc_sdk_subprocess_model` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents how the SDK spawns and supervises the `claude` CLI as a child process, so the Claude Code term is the runtime being hosted.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The subprocess that owns the shell, working directory, and transcripts IS the agent harness wrapping the model; this note describes that harness's process/state footprint.
- [Docker](../../term_dictionary/term_docker.md) — The note frames all subprocess state (transcripts, CLAUDE.md, working-dir artifacts) as living on the container filesystem and lost on container restart, the Docker container lifecycle this term defines.
- [Session Persistence (Sticky Sessions)](../../term_dictionary/term_session_persistence.md) — The note's core problem is that local-disk session transcripts do not survive a restart/scale-down, requiring a persistence strategy — exactly the session-persistence concern this term covers.
- [Context Window](../../term_dictionary/term_context_window.md) — The JSONL transcripts the subprocess writes are the on-disk record of the conversation/context the harness holds in its window, linking the disk state to the context the agent reasons over.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — `CLAUDE.md` memory files are one of the three local-disk state kinds the note enumerates; auto memory is the concrete agentic-memory mechanism that persists across sessions and must be storage-planned.

### 2. `cc_sdk_session_patterns` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note's four lifecycle patterns are all ways to host the Claude Code SDK runtime, so the product term grounds the subject being deployed.
- [Session Persistence (Sticky Sessions)](../../term_dictionary/term_session_persistence.md) — The hybrid pattern hydrates from and persists back to a SessionStore and the long-running pattern pins sessions in memory — both are session-persistence strategies this term defines.
- [Serverless](../../term_dictionary/term_serverless.md) — The ephemeral and hybrid patterns spin a container up per task and tear it down on idle, the spin-up/spin-down-on-demand execution model serverless describes.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — The multi-agent-container pattern runs multiple SDK subprocesses that collaborate in a shared environment, the multi-agent-system pattern this term defines.
- [Docker](../../term_dictionary/term_docker.md) — Every pattern is expressed in terms of container lifetime relative to session lifetime (one-shot entrypoint, persistent instance, idle-timeout spin-down), the container-lifecycle decisions Docker governs.
- [Microservices Architecture](../../term_dictionary/term_microservices_architecture.md) — The long-running pattern exposes an HTTP/WebSocket endpoint mapping each session to a held-open query behind it, the request-handling-service decomposition this term frames.

### 3. `cc_sdk_hosting_provisioning_and_scaling` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note provisions and scales the Claude Code SDK runtime in production, so the product term anchors what is being hosted.
- [Docker](../../term_dictionary/term_docker.md) — Provisioning is expressed in container terms (sandboxed container, runtime deps, RAM/disk/CPU floor, exposed ports), the container platform this term defines.
- [Consistent Hashing](../../term_dictionary/term_consistent_hashing.md) — The horizontal-scaling section pins each session to one container via consistent hashing on `sessionId` so it keeps hitting the same running subprocess — the routing technique this term defines.
- [Session Persistence (Sticky Sessions)](../../term_dictionary/term_session_persistence.md) — The pinned-session routing and the SessionStore-mirror persistence decision are both sticky-session/session-persistence patterns this term covers.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — A documented known limitation is that large parallel-subagent fanouts can hit API rate limits, mitigated by batching — the rate-limit constraint this term defines.
- [Health Check](../../term_dictionary/term_health_check.md) — Sizing a host with the agents-per-host RAM formula, recycling subprocesses on memory growth, and bounding sessions with `maxTurns` are the operational-health controls this term frames for long-lived services.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — The auth-and-secrets concern routes `ANTHROPIC_API_KEY` from a secret manager (or via a key-injecting proxy), the managed-secret-distribution pattern this term defines.

### 4. `cc_sdk_secure_deployment_principles` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note is the security-principles guide for deploying Claude Code / the Agent SDK, so the product term names the tool whose actions are being constrained.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — Built-in features (permissions, command AST parsing, web-search summarization, sandbox mode) plus the layered controls are the AI/LLM guardrails this term defines applied to an agent runtime.
- [Blast Radius - Failure Impact Scope](../../term_dictionary/term_blast_radius.md) — The security-boundary principle places credentials outside the agent's boundary so a compromise inside it stays contained — exactly the blast-radius-limiting design this term defines.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — The threat model's defense-in-depth example (network controls block an agent tricked into POSTing customer data to an external server) is the server-side-request-forgery class this term guards against.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The note's threat premise is that the harness generates actions dynamically from processed content rather than following fixed code paths, the property of an agent harness this term defines.
- [Sandbox Environment](../../term_dictionary/term_sandbox.md) — Sandbox mode is one of the built-in features and the security-principles frame "running semi-trusted code" — the OS-level isolation this term defines.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — The recurring boundary example runs a proxy outside the agent that injects credentials so the agent makes calls without seeing the key, the request-intermediary role this term defines.

### 5. `cc_sdk_isolation_technologies` (7 term notes)
- [Docker](../../term_dictionary/term_docker.md) — The note's central isolation tier is hardened Docker containers (cap-drop, seccomp, read-only, `--network none`, user namespaces), the container platform this term defines.
- [Sandbox Environment](../../term_dictionary/term_sandbox.md) — The sandbox-runtime row uses bubblewrap/Seatbelt to enforce filesystem/network restrictions at the OS level — the lightweight-sandbox isolation this term defines.
- [OCI - Open Container Initiative](../../term_dictionary/term_oci.md) — The gVisor section swaps the container runtime (`runsc`) via daemon config and `--runtime=runsc`, the OCI-runtime-interface swap this term standardizes.
- [Blast Radius - Failure Impact Scope](../../term_dictionary/term_blast_radius.md) — Each technology is ranked by how much it shrinks the impact of a compromise (userspace syscall interception, hardware VM boundary), the failure-impact-scope this term measures.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — The Unix-socket-only / vsock egress and proxy-allowlist architecture exists so a compromised agent cannot exfiltrate to arbitrary hosts, the SSRF/egress-control concern this term covers.
- [ECS - Elastic Container Service](../../term_dictionary/term_ecs.md) — The cloud-deployment recipe runs agent containers in a private subnet with firewall egress rules and minimal IAM, the managed-container-orchestration setting this term provides.
- [Microservices Architecture](../../term_dictionary/term_microservices_architecture.md) — The proxy-outside-the-boundary plus agent-container topology is a multi-component service decomposition with explicit trust boundaries, the architecture style this term frames.

### 6. `cc_sdk_credential_and_filesystem_controls` (7 term notes)
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — The note's recommended pattern routes outgoing requests through a proxy outside the agent that injects credentials and enforces an endpoint allowlist, the reverse-proxy role this term defines.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — Keeping credentials in one secure location and injecting them at the proxy rather than distributing them to each agent is the centralized-secret-management pattern this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note configures Claude Code's `ANTHROPIC_BASE_URL` and `HTTP_PROXY`/`HTTPS_PROXY` routing and trust store, so the product term anchors the runtime being configured.
- [SSRF Guard](../../term_dictionary/term_ssrf_guard.md) — The proxy enforces an allowlist of permitted endpoints and the TLS-terminating-proxy section controls which hosts the agent can reach, the egress/SSRF-control concern this term covers.
- [PII (Personally Identifiable Information)](../../term_dictionary/term_pii.md) — The read-only-mount warning lists sensitive files (`.env`, `~/.aws/credentials`, `*.pem`) to exclude before mounting, the secret/PII-exposure risk this term frames.
- [Docker](../../term_dictionary/term_docker.md) — Filesystem controls are expressed as Docker mount flags (`-v ...:ro`, `--tmpfs`, overlay, dedicated volume), the container mount mechanics this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The custom-tool credential approach routes authenticated requests through an MCP server / custom tool outside the boundary so the agent never sees the credential, the tool-server pattern this term defines.

### 7. `cc_sdk_observability_opentelemetry` (8 term notes)
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — The note IS the agent-SDK observability guide (traces/metrics/logs for long-lived tool-calling agents), the exact discipline this term defines.
- [Context Propagation - Distributed Request Context Passing](../../term_dictionary/term_context_propagation.md) — The "Link traces to your application" section propagates W3C `TRACEPARENT`/`TRACESTATE` into the CLI subprocess so the agent run nests under your span — the distributed-context-propagation mechanism this term defines.
- [X-Ray - AWS Distributed Tracing Service](../../term_dictionary/term_xray.md) — The four `claude_code.*` spans nesting into one delegation-chain trace are exactly the distributed traces X-Ray collects and visualizes, a concrete OTLP-compatible backend.
- [CloudWatch - AWS Monitoring & Observability Platform](../../term_dictionary/term_cloudwatch.md) — The exported metrics (token/cost/session counters) and log events land in a monitoring backend; CloudWatch is a representative metrics+logs destination of the kind this note targets.
- [EMF - Embedded Metric Format](../../term_dictionary/term_emf.md) — The metrics signal emits counters for tokens, cost, sessions, and tool decisions as structured records, the structured-metric-emission concern EMF addresses.
- [SLI - Service Level Indicator](../../term_dictionary/term_sli.md) — Tracking which tools ran, request latency, and where sessions stalled produces the latency/error/throughput signals that define SLIs for an agent service.
- [Langfuse - LLM Observability & Analytics Platform](../../term_dictionary/term_langfuse.md) — The note lists Langfuse as one of the OTLP backends the SDK exports to, an LLM-specific observability platform for the emitted spans and token metrics.
- [PII (Personally Identifiable Information)](../../term_dictionary/term_pii.md) — The "Control sensitive data in exports" section gates prompt text, tool inputs, and raw API bodies behind opt-in flags precisely because they may contain PII the pipeline must be approved to store.

### 8. `cc_sdk_cost_and_usage_tracking` (7 term notes)
- [Prompt Caching - Bedrock Cached Prompt Prefix Optimization](../../term_dictionary/term_prompt_caching.md) — The note's cache-token section tracks `cache_creation_input_tokens`/`cache_read_input_tokens` and the `ENABLE_PROMPT_CACHING_1H` TTL knob, the cached-prefix optimization this term defines.
- [KV Cache - Key-Value Cache](../../term_dictionary/term_kv_cache.md) — Cache reads charged at a reduced rate and cache writes at a higher rate are the price mechanics of the underlying KV-cache reuse this term explains.
- [Inference Scaling Law](../../term_dictionary/term_inference_scaling_law.md) — The note frames cost as token-driven (a single long agent session spends dollars in tokens, dwarfing container cost), the token-to-cost relationship this term quantifies.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The `total_cost_usd`/`modelUsage` fields are emitted by the Claude Code SDK result message this note reads, so the product term anchors the runtime being measured.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — The per-model `modelUsage` breakdown is motivated by mixed-model runs (Haiku for subagents, Opus for the main agent), the multi-agent token-attribution case this term frames.
- [Gist Token](../../term_dictionary/term_gist_token.md) — The note's per-step input/output/cache token accounting and dedup-by-message-ID is token-economy bookkeeping, the token-compression/accounting space this term sits in.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — Tracking accumulated cost/usage across calls is the budgeting half of the same token-budget control that rate limiting enforces on the request side.

## Section Coverage Map

```
hosting.md
├── The subprocess model ──────────────── → note 1 (cc_sdk_subprocess_model)
│   └── State that lives on local disk ── → note 1 (→ B19B session-storage for SessionStore)
├── Choose a session pattern ──────────── → note 2 (cc_sdk_session_patterns)
│   ├── Ephemeral / Long-running ──────── → note 2
│   ├── Hybrid ────────────────────────── → note 2 (→ B19B session-storage)
│   └── Multi-agent container ─────────── → note 2 (→ note 4 multi-tenant isolation)
├── Provision the container ───────────── → note 3 (cc_sdk_hosting_provisioning_and_scaling)
│   ├── Container-based sandboxing ────── → note 3 (→ note 5 isolation technologies)
│   ├── Runtime dependencies / Resources → note 3
│   └── Network ───────────────────────── → note 3 (→ note 6 credential proxy)
├── Handle production concerns ────────── → note 3
│   ├── Session and state persistence ─── → note 3 (→ B19B session-storage)
│   ├── Observability ─────────────────── → note 3 (→ note 7 observability)
│   ├── Auth and secrets ──────────────── → note 3 (→ note 6 credential mgmt)
│   ├── Scaling and concurrency ───────── → note 3
│   ├── Cost ──────────────────────────── → note 3 (→ note 8 cost tracking)
│   └── Multi-tenant isolation ────────── → note 3 (cwd / settingSources / config dir / auto-memory)
├── Known limitations ─────────────────── → note 3
└── Next steps (cards) ────────────────── → notes 1/3/7/8 (links)
secure-deployment.md
├── (intro) / Threat model ────────────── → note 4 (cc_sdk_secure_deployment_principles)
├── Built-in security features ────────── → note 4 (→ B05A permissions / B05B sandboxing)
├── Security principles ───────────────── → note 4
│   ├── Security boundaries ───────────── → note 4
│   ├── Least privilege ───────────────── → note 4
│   └── Defense in depth ──────────────── → note 4
├── Isolation technologies ────────────── → note 5 (cc_sdk_isolation_technologies)
│   ├── Sandbox runtime ───────────────── → note 5
│   ├── Containers ────────────────────── → note 5
│   ├── gVisor ────────────────────────── → note 5
│   ├── Virtual machines ──────────────── → note 5
│   └── Cloud deployments ─────────────── → note 5
├── Credential management ─────────────── → note 6 (cc_sdk_credential_and_filesystem_controls)
│   ├── The proxy pattern ─────────────── → note 6
│   ├── Configuring CC to use a proxy ─── → note 6
│   ├── Implementing a proxy ──────────── → note 6
│   └── Credentials for other services ── → note 6
├── Filesystem configuration ──────────── → note 6
│   ├── Read-only code mounting ───────── → note 6
│   └── Writable locations ────────────── → note 6
└── Further reading (links) ───────────── → notes 4/5/6 (links)
observability.md
├── How telemetry flows from the SDK ──── → note 7 (cc_sdk_observability_opentelemetry)
├── Enable telemetry export ───────────── → note 7
│   └── Flush telemetry (short-lived) ─── → note 7
├── Read agent traces ─────────────────── → note 7
├── Link traces to your application ───── → note 7
├── Tag telemetry from your agent ─────── → note 7
├── Attribute actions to your end users ─ → note 7 (→ B15B monitoring-usage for event catalog)
├── Control sensitive data in exports ─── → note 7
└── Related documentation (links) ─────── → notes 7/8 (links; → B15B monitoring-usage)
cost-tracking.md
├── Understand token usage ────────────── → note 8 (cc_sdk_cost_and_usage_tracking)
├── Get the total cost of a query ─────── → note 8
├── Track per-step and per-model usage ── → note 8
│   ├── Track per-step usage ──────────── → note 8
│   └── Break down usage per model ────── → note 8
├── Accumulate costs across multiple calls → note 8
├── Handle errors, caching, discrepancies → note 8
│   ├── Resolve output token discrepancies → note 8
│   ├── Track costs on failed conversations → note 8
│   ├── Track cache tokens ────────────── → note 8 (→ B02A prompt-caching)
│   └── Extend prompt cache TTL to 1h ─── → note 8 (→ B14A providers for Bedrock/Vertex)
└── Related documentation (links) ─────── → note 8 (→ B21B/B21C SDK refs)
```
No orphaned sections. Sections owned by other sub-plans (SessionStore/sessions → B19B; sandboxing built-in
→ B05B; permissions → B05A; monitoring metric/event catalog → B15B; prompt-caching feature → B02A; cloud
providers → B14A; SDK language refs → B21B/B21C) are LINKED, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| hosting (2,635w, 6 H2 mixed) | notes 1,2,3 + link-outs | distinct BBs: subprocess model (concept) / session-lifecycle patterns (concept) / provisioning+production+limits (procedure). SessionStore + sessions API owned by B19B. |
| secure-deployment (3,050w >2500, 7 H2) | notes 4,5,6 + link-outs | exceeds density cap AND mixes BBs: principles/threat-model (argument) vs isolation-technology catalog (concept) vs credential+filesystem how-to (procedure). Built-in sandbox/permissions owned by B05A/B05B. |
| observability (2,002w, 8 H2) | note 7 (single) | one cohesive procedure (configure OTEL export); within caps; no BB mix. Metric/event catalog link-out to B15B. |
| cost-tracking (1,825w, 6 H2) | note 8 (single) | one cohesive procedure (read token/cost from the stream); within caps; no BB mix. Prompt-caching feature link-out to B02A. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_sdk_subprocess_model | concept | 500 | 1 | ✅ |
| 2 | cc_sdk_session_patterns | concept | 600 | 3 | ✅ |
| 3 | cc_sdk_hosting_provisioning_and_scaling | procedure | 700 | 3 | ✅ |
| 4 | cc_sdk_secure_deployment_principles | argument | 550 | 0 | ✅ |
| 5 | cc_sdk_isolation_technologies | concept | 650 | 4 | ✅ |
| 6 | cc_sdk_credential_and_filesystem_controls | procedure | 650 | 5 | ✅ |
| 7 | cc_sdk_observability_opentelemetry | procedure | 700 | 4 | ✅ |
| 8 | cc_sdk_cost_and_usage_tracking | procedure | 700 | 5 | ✅ |

No note approaches the caps (≤2,500w / ≤6 code / ≤400 lines). The two large source pages (hosting,
secure-deployment) are split into 3 notes each so no digest note exceeds ~700w. Every H2/H3 maps to a note
or an explicit link-out — no over-compression.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_sdk_subprocess_model cc_sdk_session_patterns cc_sdk_hosting_provisioning_and_scaling cc_sdk_secure_deployment_principles cc_sdk_isolation_technologies cc_sdk_credential_and_filesystem_controls cc_sdk_observability_opentelemetry cc_sdk_cost_and_usage_tracking"
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
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability (inbound) | each of the 8 notes RECEIVES ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (outbound/entry) | each note links to its siblings + the entry point; entry-point rows added | DB query + `entry_claude_code_docs.md` row check |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets
`0_entry_points/entry_claude_code_docs.md`; this sub-plan **contributes its 8 rows** under an "SDK —
Production & Hosting" cluster and increments the BB-distribution counts (concept +3, argument +1,
procedure +4). The entry-point back-link is added to each note at finalization (G8).

## Undigested Terms Plan (Step 2d)

B21A creates **0 new `term_dictionary` captures**. The 4 pages introduce production/security/observability
vocabulary, but every term either (a) has an existing substantive term note to link, (b) is a Claude Code
doc-concept owned by a `cc_` note here or in another sub-plan (Pattern B), or (c) is owned by another
sub-plan's home page. **Dedup performed across `term_dictionary/` AND `resources/documentation/`** (no
observability docs are different-product, not same-sense duplicates).

**Step 2d re-scan (2026-06-13)** — re-read all 4 pages scanning emphasis/tables/captions for newly-surfaced terms:

| Surfaced term | Disposition |
|---|---|
| Subprocess / stdio / JSONL transcript | note 1 `cc_sdk_subprocess_model` (doc concept) |
| Session pattern (ephemeral/long-running/hybrid/multi-agent) | note 2 `cc_sdk_session_patterns` (doc concept) |
| `SessionStore` / session storage | owned by B19B (`session-storage.md`) — link, not capture |
| Multi-tenant isolation / `settingSources` / `CLAUDE_CONFIG_DIR` | note 3 (folded) + B19A/B20C (settingSources) — link |
| Threat model / prompt injection | argument framed in note 4; **Prompt injection term owned by B16** (master) — link there when it exists, not captured here |
| Security boundary / least privilege / defense in depth | note 4 (doc concepts); link existing `term_blast_radius`, `term_guardrails` |
| Sandbox runtime / gVisor / Firecracker / vsock / seccomp / cap-drop | note 5 (doc concepts); link existing `term_sandbox`, `term_docker`, `term_oci` |
| Credential proxy / TLS-terminating proxy / transparent proxy | note 6 (doc concepts); link existing `term_reverse_proxy`, `term_secrets_manager` |
| OpenTelemetry / OTLP / span / trace context / SIEM | note 7 (doc concepts); link existing `term_observability_agent_systems`, `term_context_propagation`, `term_xray`, `term_cloudwatch`, `term_langfuse` |
| `total_cost_usd` / `modelUsage` / cache tokens / 1h TTL | note 8 (doc concepts); link existing `term_prompt_caching`, `term_kv_cache` |

**0 new B21A `term_dictionary` captures.** No genuine cross-cutting vocabulary term with no doc-page home
AND no existing note surfaced. (`term_prompt_injection` is MISSING from the vault and is owned by B16 per
the master — it is NOT created here and NOT listed as a Related Note, to avoid a ghost.)

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B21A authors zero term notes, so there are
no slugs to audit. The collision check that matters here (do the page concepts duplicate existing notes?)
was performed and resolved to *link existing*: `term_observability_agent_systems`, `term_prompt_caching`,
`term_kv_cache`, `term_docker`, `term_sandbox`, `term_reverse_proxy`, `term_secrets_manager`,
`term_ssrf_guard`, `term_blast_radius`, `term_guardrails`, `term_consistent_hashing`, etc. — all exist →
linked, not recreated.

## Term-Note Authoring Requirements

**N/A for B21A** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from the source (SDK snippets, docker/OTEL config). One BB per note. Each note
  ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Cap dynamic-workflow fan-out at ~30 agents/run (8 notes here is well under).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7 — each new note
receives ≥1 inbound link from outside `claude_code/`):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 3 | product term → SDK subprocess runtime + hosting/scaling |
| `term_dictionary/term_observability_agent_systems.md` | note 7 | agent-observability term → SDK OTEL export how-to |
| `term_dictionary/term_prompt_caching.md` | note 8 | prompt-caching term → SDK cache-token cost tracking |
| `term_dictionary/term_sandbox.md` | note 5 | sandbox term → SDK isolation-technology catalog |
| `term_dictionary/term_secrets_manager.md` | note 6 | secrets-manager term → SDK credential-proxy pattern |
| `term_dictionary/term_docker.md` | notes 2, 5 | docker term → SDK session-pattern containers + isolation |
| `term_dictionary/term_consistent_hashing.md` | note 3 | consistent-hashing term → SDK session-pinned scaling |
| `term_dictionary/term_kv_cache.md` | note 8 | kv-cache term → SDK cache-token pricing |

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 8
  rows for `entry_claude_code_docs.md` under "SDK — Production & Hosting"; `/tessellum-check-broken-links`.
- When B16's `term_prompt_injection` is created, add it as a Related Note to note 4 (deferred to avoid a
  ghost now).
- When sibling SDK sub-plans (B19B sessions/storage, B20A MCP, B20B subagents, B20C hooks/permissions)
  land, add cross-`cc_` links from notes 1/2/3/6/7 to those siblings.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13** — see Review Sign-Off below (9/9 → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B21A, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read from `inbox/claude_code_docs/agent-sdk/`; measured words
  match the master's figure (hosting 2,635 · secure-deployment 3,050 · observability 2,002 · cost-tracking
  1,825 = 9,512). No >1.5× under-estimate; the two pages over the 2,500-word cap (secure-deployment 3,050;
  hosting 2,635 mixed-BB) are split into 3 notes each.
- **Notes**: 8 (concept 3, argument 1, procedure 4) — exactly the master estimate. Split decisions: hosting
  → 3 (subprocess / session-patterns / provisioning+scaling), secure-deployment → 3 (principles /
  isolation-technologies / credential+filesystem), observability → 1, cost-tracking → 1.
- **Per-Note Related Notes Mapping (Step 8)**: 6–8 relevancy-selected term notes per note (34 distinct
  `term_prompt_injection` MISSING and owned by B16, excluded). Relpaths `../../term_dictionary/`.
- **Step 2d new-term scan**: production/security/observability terms surfaced; all route to existing term
  notes (link) or doc-concept `cc_` notes (Pattern B); **0 new B21A term captures**.
- **Dedup (G-B)**: searched `term_dictionary/` AND `resources/documentation/`; no `claude_code/` doc folder
  not same-sense — no merge/delete needed (adversarial dedup-verify trivially N/A).
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G7/G8 gate rows, Inlinks table, Section Coverage Map link-outs.
- **28-item checklist**: PASS (term-note items N/A — B21A authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented, reviewed, and set to `ready` (self-review 9/9 below).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | ALL gates per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (inbound in-degree ≥1 + outbound/entry). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (>30 notes → CREATE required); B21A contributes 8 rows under "SDK — Production & Hosting". |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; the overall corpus is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the inherited Format Definition exactly (`tags`→`access_control_group`); body uses `## Overview` / source-mirrored H2s / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | The two pages over the 2,500-word cap (secure-deployment 3,050; hosting 2,635 mixed-BB) are pre-split into 3 notes each; all 8 notes 500–700w, ≤5 code — none borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: hosting 2,635, secure-deployment 3,050, observability 2,002, cost-tracking 1,825 = 9,512 = master figure. H2/H3/code-fence counts measured via `grep`. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B21A authors 0 term notes; Undigested Terms Plan routes every surfaced term (link existing / doc-concept / other sub-plan); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); page-concept collision check documented (existing observability/security/caching/container terms linked, not recreated); `term_prompt_injection` ghost avoided (owned by B16). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.
