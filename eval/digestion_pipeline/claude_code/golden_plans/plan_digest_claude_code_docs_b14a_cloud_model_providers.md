---
title: Sub-Plan B14A — Claude Code Docs: Cloud Model Providers
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["amazon-bedrock", "google-vertex-ai", "microsoft-foundry", "claude-platform-on-aws", "llm-gateway"]
---

# Sub-Plan B14A: Cloud Model Providers

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 5 enterprise deployment pages that document how to point Claude Code at a third-party / cloud
inference backend instead of the default Anthropic API: **Amazon Bedrock**, **Google Vertex AI**,
**Microsoft Foundry**, **Claude Platform on AWS** (Anthropic-operated API with AWS auth/billing), and a
centralized **LLM gateway / proxy** layer (incl. LiteLLM). P3 (Phase C) — enterprise/specialized; runs
after the P1 vocabulary cores are in place so it can link `term_mcp`, `term_prompt_caching`,
`term_context_window`, and the model-config / settings sibling notes.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 5 pages, 9,424 measured words. **Planned: 10 notes.**

## Content Strategy

- **Prioritize**: the per-provider *enable + authenticate + pin-models* procedure (the operational core every team deploying Claude Code at scale needs), plus the cross-provider gateway/proxy routing pattern.
- **Group / split**: `amazon-bedrock` (3.2Kw, 19 code blocks — far over caps) splits 4 ways by BB (setup procedure / model-config procedure / Bedrock-specific feature concepts / the separate Mantle endpoint procedure). `claude-platform-on-aws` (8 code) splits 2 ways (setup+auth vs proxy+SDK). `llm-gateway` splits 2 ways (gateway-requirements concept vs LiteLLM config procedure). Vertex and Foundry each stay a single procedure note (within caps after trivial-block consolidation).
- **Skip / link-out (own other sub-plans)**: the full env-var catalog → `env-vars` (B14B? no — `env-vars` is B03A); model aliases/`modelOverrides`/`availableModels` reference → `model-config` (B03B); settings-file mechanics → `settings` (B03A); MCP tool search behavior → `mcp` (B08A); prompt-caching mechanism + cache lifetime → `prompt-caching` (B02A); WebSearch tool behavior → `tools-reference` (B03B); network/proxy enterprise config → `network-config` (B14B). These are referenced via links, never duplicated.
- **Terms**: no new `term_dictionary` captures — every concept maps to an existing term note (link) or is a Claude-Code-specific doc concept owned by this sub-plan (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 5 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).
Code-block / word counts exclude the shared `ContactSalesCard` / `Experiment` JSX export boilerplate at the top of each page.

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| amazon-bedrock | /amazon-bedrock | 3,242 | 19 | 11 | 12 | procedure (+ concept for features) |
| google-vertex-ai | /google-vertex-ai | 2,017 | 5 | 9 | 5 | procedure |
| microsoft-foundry | /microsoft-foundry | 1,006 | 7 | 5 | 5 | procedure |
| claude-platform-on-aws | /claude-platform-on-aws | 2,005 | 8 | 6 | 6 | procedure |
| llm-gateway | /llm-gateway | 1,154 | 9 | 4 | 3 | concept (+ procedure for LiteLLM) |

> **H2 lists (document order):**
> - **amazon-bedrock**: Prerequisites · Sign in with Bedrock · Set up manually (H3 1. Submit use case details, 2. Configure AWS credentials, 3. Configure Claude Code, 4. Pin model versions) · Startup model checks · IAM configuration · 1M token context window · Service tiers · AWS Guardrails · Use the Mantle endpoint (H3 Enable Mantle, Select a Mantle model, Run Mantle alongside the Invoke API, Route Mantle through a gateway, Mantle environment variables) · Troubleshooting (H3 Authentication loop with SSO and corporate proxies, Region issues, Mantle endpoint errors) · Additional resources
> - **google-vertex-ai**: Prerequisites · Sign in with Vertex AI · Region configuration · Set up manually (H3 1. Enable Vertex AI API, 2. Request model access, 3. Configure GCP credentials, 4. Configure Claude Code, 5. Pin model versions) · Startup model checks · IAM configuration · 1M token context window · Troubleshooting · Additional resources
> - **microsoft-foundry**: Prerequisites · Setup (H3 1. Provision Microsoft Foundry resource, 2. Configure Azure credentials, 3. Configure Claude Code, 4. Pin model versions, 5. Run Claude Code) · Azure RBAC configuration · Troubleshooting · Additional resources
> - **claude-platform-on-aws**: (intro) · Prerequisites · Setup (H3 1. Configure AWS credentials, 2. Configure Claude Code, 3. Pin model versions) · Use the Agent SDK · Route through a corporate proxy · Troubleshooting (H3 403 Forbidden, missing-workspace error, requests still go to api.anthropic.com) · Additional resources
> - **llm-gateway**: (intro: what a gateway provides) · Gateway requirements (API format, request headers) · Configuration (H3 Model selection) · LiteLLM configuration (H3 Prerequisites, Basic LiteLLM setup with auth methods + endpoints) · Additional resources

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **10 notes** (master estimate 8; raised to 10 during augment because amazon-bedrock at 19 code blocks forces a 4-way split and claude-platform-on-aws / llm-gateway each exceed the 6-code cap → 2-way splits). All prefixed `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_amazon_bedrock_setup.md` | procedure | bedrock: Prerequisites, Sign in with Bedrock, Set up manually 1-3 (use case, AWS credentials A-E, advanced refresh, configure CC env) | 650 | How to enable Bedrock: prereqs, the `/setup-bedrock` sign-in wizard, manual env-var path, AWS credential chain (options A-E consolidated), `awsAuthRefresh`/`awsCredentialExport`, `CLAUDE_CODE_USE_BEDROCK`, region resolution order. Pin step → note 2; IAM/features → note 3; Mantle → note 4. |
| 2 | `cc_amazon_bedrock_model_config.md` | procedure | bedrock: 4. Pin model versions, Map each model version to an inference profile, Startup model checks | 600 | Pinning `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` to Bedrock inference-profile IDs (`us.` prefix; `us-gov.` for GovCloud), default model table, `modelOverrides` ARN map, small/fast-model fallback to primary, startup model-check prompt/fallback behavior. Full env-var list → `model-config` (B03B). |
| 3 | `cc_amazon_bedrock_features.md` | concept | bedrock: IAM configuration, 1M token context window, Service tiers, AWS Guardrails, Troubleshooting (auth loop, region) | 600 | Bedrock-specific server-side concerns: the IAM policy (Invoke/InferenceProfile/Marketplace actions), `[1m]` 1M context, `ANTHROPIC_BEDROCK_SERVICE_TIER`, AWS Guardrails headers, Invoke-API-only / no-Converse / no-WebSearch constraints, SSO-loop + region troubleshooting. Prompt-caching mechanism → `prompt-caching` (B02A). |
| 4 | `cc_amazon_bedrock_mantle_endpoint.md` | procedure | bedrock: Use the Mantle endpoint (Enable, Select model, Run alongside Invoke, Route through gateway, env vars), Mantle endpoint errors | 600 | The Mantle endpoint (native Anthropic API shape on Bedrock): `CLAUDE_CODE_USE_MANTLE`, `anthropic.`-prefixed model IDs, running Mantle + Invoke API together, `availableModels` picker, `CLAUDE_CODE_SKIP_MANTLE_AUTH` for gateways, the 4-row Mantle env-var table, 403/400 troubleshooting. |
| 5 | `cc_google_vertex_ai.md` | procedure | vertex: all (Prereqs, Sign in, Region config, manual 1-5, Startup checks, IAM, 1M, Troubleshooting) | 750 | Full Vertex AI deployment: `/setup-vertex` wizard, `gcloud` API enable + Model Garden access, ADC / service-account / X.509 WIF credentials, `gcpAuthRefresh`, `CLAUDE_CODE_USE_VERTEX` + `CLOUD_ML_REGION` (global/multi-region/regional) + `ANTHROPIC_VERTEX_PROJECT_ID`, `VERTEX_REGION_CLAUDE_*` overrides, tool-search default-off, `roles/aiplatform.user` IAM, 1M context, 404/429/quota troubleshooting. |
| 6 | `cc_microsoft_foundry.md` | procedure | foundry: all (Prereqs, Setup 1-5, Azure RBAC, Troubleshooting) | 550 | Full Foundry deployment: provision Azure resource + Claude deployments, API-key vs Microsoft Entra ID (`ANTHROPIC_FOUNDRY_API_KEY` / Azure default credential chain), `CLAUDE_CODE_USE_FOUNDRY` + `ANTHROPIC_FOUNDRY_RESOURCE`/`_BASE_URL`, pin-models (no startup check — requests fail if default unavailable), no setup wizard, `Azure AI User`/`Cognitive Services User` RBAC, Entra token troubleshooting. |
| 7 | `cc_claude_platform_on_aws_setup.md` | procedure | claude-platform-on-aws: intro, Prerequisites, Setup 1-3 (AWS creds + SigV4 / workspace API key, configure, pin) | 650 | Claude Platform on AWS = Anthropic-operated Claude API with AWS auth + Marketplace billing (separate org). Auth: SigV4 via AWS credential chain OR `ANTHROPIC_AWS_API_KEY` (x-api-key, precedence over SigV4). `CLAUDE_CODE_USE_ANTHROPIC_AWS` + required `ANTHROPIC_AWS_WORKSPACE_ID` (anthropic-workspace-id header) + region-derived base URL; opt-in even with AWS creds (Bedrock/Foundry take precedence); pin same model IDs as direct API. |
| 8 | `cc_claude_platform_on_aws_proxy_and_sdk.md` | procedure | claude-platform-on-aws: Use the Agent SDK, Route through a corporate proxy, Troubleshooting | 450 | Targeting Claude Platform on AWS from the Agent SDK (same env vars as CLI) and through a corporate proxy / LLM gateway: `ANTHROPIC_AWS_BASE_URL` override, `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH` (gateway signs SigV4), `ANTHROPIC_AUTH_TOKEN` for gateway tokens; `/status` provider check; 403/missing-workspace/wrong-endpoint troubleshooting. |
| 9 | `cc_llm_gateway.md` | concept | llm-gateway: intro, Gateway requirements (API format, request headers), Configuration / Model selection | 600 | What an LLM gateway provides (centralized auth, usage/cost/audit, model routing); the 3 supported API formats (Anthropic Messages / Bedrock InvokeModel / Vertex rawPredict) + header-forwarding requirements; `X-Claude-Code-{Session,Agent,Parent-Agent}-Id` attribution headers; attribution block + `CLAUDE_CODE_ATTRIBUTION_HEADER`; gateway model discovery (`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY`, `/v1/models`). |
| 10 | `cc_llm_gateway_litellm.md` | procedure | llm-gateway: LiteLLM configuration (Prerequisites, auth methods, unified + pass-through endpoints) | 600 | Configuring LiteLLM as the gateway: the malware version warning, static-key (`ANTHROPIC_AUTH_TOKEN`) vs dynamic `apiKeyHelper` (+ `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`), the recommended unified Anthropic-format endpoint vs provider-specific pass-through endpoints (Claude API / Bedrock / Vertex / Claude Platform on AWS, each with its `CLAUDE_CODE_SKIP_*_AUTH`). |

**Estimate: 10 notes** — procedure ×8 (notes 1,2,4,5,6,7,8,10), concept ×2 (notes 3,9). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 5 (9,424 words). New `cc_` notes: 10. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~6,050 (avg ~605/note). Code blocks: ≤6 per note (verbatim shell/JSON config), well under the ≤6 cap after the bedrock 4-way + claude-platform 2-way + gateway 2-way splits.
- **Building Block Distribution**: procedure ×8 (notes 1,2,4,5,6,7,8,10) · concept ×2 (notes 3,9). No model/argument/empirical_observation in this sub-plan (deployment-config material is overwhelmingly step/procedure; Bedrock features and the gateway abstraction are concept).

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_amazon_bedrock_setup` (7 term notes)
- [AWS — Amazon Web Services](../../term_dictionary/term_aws.md) — what AWS is (the cloud platform, accounts, services, regions); relevance: this note's entire setup runs on an AWS account — Bedrock console, AWS CLI, regions, and the AWS SDK credential chain are all AWS primitives the procedure depends on.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the agentic coding tool being configured; relevance: this note is the Bedrock deployment procedure for Claude Code itself (`claude` login wizard, `CLAUDE_CODE_USE_BEDROCK`, `/setup-bedrock`).
- [SigV4 — AWS Signature Version 4 Authentication](../../term_dictionary/term_sigv4.md) — the AWS request-signing scheme; relevance: Claude Code signs Bedrock Invoke API calls with SigV4 using the resolved AWS credentials this note configures (access key / SSO profile / bearer token).
- [IAM — AWS Identity and Access Management](../../term_dictionary/term_iam.md) — AWS's identity/permission service; relevance: the prereqs require "appropriate IAM permissions" and the use-case-submission step needs `bedrock:PutUseCaseForModelAccess` — IAM is the access-control layer gating every Bedrock call.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — short-lived access tokens minted from long-lived credentials and auto-refreshed; relevance: the `awsAuthRefresh`/`awsCredentialExport` settings this note documents are exactly Claude Code's credential-refresh hooks for expiring AWS SSO/SDK sessions.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's Claude LLM family (Opus/Sonnet/Haiku) on Bedrock; relevance: the procedure's goal is invoking Claude models through Bedrock, and the prereq is enabling "Anthropic models (e.g. Claude Sonnet 4.6)" in the account.
- [Access Control](../../term_dictionary/term_access_control.md) — the general principle of regulating who/what may perform actions on resources; relevance: this note's credential setup + per-account model enablement is access control applied to model invocation, and the docs explicitly recommend a dedicated AWS account "to simplify cost tracking and access control."

### 2. `cc_amazon_bedrock_model_config` (6 term notes)
- [Claude](../../term_dictionary/term_claude.md) — the Opus/Sonnet/Haiku model family and its variants; relevance: this note maps the `opus`/`sonnet`/`haiku` aliases to specific Bedrock model IDs and inference profiles — the whole note is about which Claude version each alias resolves to.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — a runtime registry resolving a (provider, model-id) name to an invocation endpoint, incl. Vertex/Bedrock model gardens and inference-profile lookup; relevance: pinning `ANTHROPIC_DEFAULT_*_MODEL` and `modelOverrides` ARNs is precisely populating Claude Code's runtime model-resolution table for Bedrock.
- [AWS — Amazon Web Services](../../term_dictionary/term_aws.md) — AWS regions, ARNs, and inference profiles; relevance: Bedrock model IDs are cross-region inference-profile IDs (`us.`/`us-gov.` prefix) and application-inference-profile ARNs — AWS-native resource identifiers this note pins.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool whose `/model` picker and model defaults are configured; relevance: this note covers Claude Code's built-in Bedrock defaults, startup model checks, and the `/model` picker behavior driven by `modelOverrides`/`availableModels`.
- [IAM — AWS Identity and Access Management](../../term_dictionary/term_iam.md) — AWS permission policies; relevance: `bedrock:GetInferenceProfile` (an IAM action) lets Claude Code resolve an application-inference-profile ARN to its backing foundation model, affecting which request shape this note's pinned models use.
- [Amazon Nova](../../term_dictionary/term_amazon_nova.md) — AWS's first-party foundation-model family on Bedrock with tiered cost/speed variants; relevance: contextualizes the Bedrock model-catalog landscape — Claude models are configured here alongside (and against) Bedrock's other 1P model families, and the small/fast-vs-primary tiering mirrors Nova's tier design.

### 3. `cc_amazon_bedrock_features` (7 term notes)
- [IAM — AWS Identity and Access Management](../../term_dictionary/term_iam.md) — AWS identity/permission policies; relevance: this note's IAM policy section is the canonical Bedrock permission set (`bedrock:InvokeModel`, `ListInferenceProfiles`, marketplace subscribe) — IAM is the gate on every feature here.
- [Guardrails (AI/LLM)](../../term_dictionary/term_guardrails.md) — runtime safety controls that filter model input/output; relevance: the AWS Guardrails section configures Amazon Bedrock Guardrails (content filtering via `X-Amzn-Bedrock-Guardrail*` headers) — a direct instance of the guardrails concept applied to Claude Code traffic.
- [AWS — Amazon Web Services](../../term_dictionary/term_aws.md) — the AWS platform, service tiers, and provisioned throughput; relevance: service tiers (`default`/`flex`/`priority`), provisioned-throughput ARNs, and cross-region inference are all AWS Bedrock capabilities this note's features expose.
- [Context Window](../../term_dictionary/term_context_window.md) — the token budget a model can attend to in one request; relevance: the "1M token context window" feature extends Claude Code's context window on Bedrock for Opus 4.6+/Sonnet 4.6 via the `[1m]` model-ID suffix — directly the context-window concept.
- [Prompt Caching — Bedrock Cached Prompt Prefix Optimization](../../term_dictionary/term_prompt_caching.md) — caching a stable prompt prefix to cut input-token cost/latency; relevance: this note covers the Bedrock prompt-caching toggles (`DISABLE_PROMPT_CACHING`, `ENABLE_PROMPT_CACHING_1H`) and the region-availability caveat — the term note IS the Bedrock prompt-caching definition.
- [Latency](../../term_dictionary/term_latency.md) — request-to-response time, the responsiveness measure; relevance: Bedrock service tiers explicitly "trade off cost against latency" — the `priority`/`flex`/`default` choice this note documents is a latency-vs-cost knob.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool whose Bedrock-specific behavior is documented; relevance: the Invoke-API-only / no-Converse-API / no-WebSearch constraints and the SSO-loop troubleshooting are Claude-Code-on-Bedrock specifics this note records.

### 4. `cc_amazon_bedrock_mantle_endpoint` (6 term notes)
- [AWS — Amazon Web Services](../../term_dictionary/term_aws.md) — AWS credentials, regions, and Bedrock; relevance: Mantle is an Amazon Bedrock endpoint using the same AWS credentials, IAM permissions, and `awsAuthRefresh` config — the procedure is wholly AWS-anchored.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool being routed to Mantle; relevance: this note documents Claude-Code-specific Mantle switches (`CLAUDE_CODE_USE_MANTLE`, `/status` provider line, `/model` picker integration via `availableModels`).
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — runtime name→endpoint resolution across providers; relevance: running Mantle alongside the Invoke API routes each request by model-ID format (`anthropic.`-prefixed → Mantle, others → Invoke) — a model-catalog routing decision this note configures.
- [SigV4 — AWS Signature Version 4 Authentication](../../term_dictionary/term_sigv4.md) — AWS request signing; relevance: `CLAUDE_CODE_SKIP_MANTLE_AUTH` tells Claude Code to send Mantle requests *without* SigV4 signatures or `x-api-key` headers when a gateway injects credentials server-side — a direct SigV4-skip toggle.
- [Claude](../../term_dictionary/term_claude.md) — the Claude model family and IDs; relevance: Mantle uses its own Claude model lineup with `anthropic.`-prefixed IDs (e.g. `anthropic.claude-haiku-4-5`) separate from the standard Bedrock catalog — model selection is central to this note.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a managed entry point that fronts backend services with auth/routing; relevance: the "Route Mantle through a gateway" section sends Mantle traffic to a centralized gateway that injects AWS credentials — exactly the gateway-fronting pattern.

### 5. `cc_google_vertex_ai` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool being deployed on Vertex; relevance: this note is the end-to-end Claude-Code-on-Vertex procedure (`/setup-vertex` wizard, `CLAUDE_CODE_USE_VERTEX`, region/project env vars, startup model checks).
- [Claude](../../term_dictionary/term_claude.md) — the Claude model family requested in Model Garden; relevance: the procedure requests access to specific Claude models (Sonnet 4.6 etc.) in the Vertex AI Model Garden and pins their Vertex model IDs.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — runtime model resolution and the Vertex AI Model Garden as a discovery surface; relevance: the term note explicitly names Vertex AI Model Garden, and this note's model-access + pinning + `VERTEX_REGION_CLAUDE_*` overrides populate Claude Code's Vertex model resolution.
- [IAM — AWS Identity and Access Management](../../term_dictionary/term_iam.md) — identity/permission management (the cross-cloud access-control concept); relevance: Vertex's IAM section grants `roles/aiplatform.user` (`aiplatform.endpoints.predict`) — the GCP analog of the IAM permission model this term anchors for model-invocation access.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — short-lived credential auto-refresh; relevance: `gcpAuthRefresh` re-runs `gcloud auth application-default login` when GCP credentials expire — Vertex's credential-refresh hook, the same pattern as Bedrock's `awsAuthRefresh`.
- [Context Window](../../term_dictionary/term_context_window.md) — the model's token budget; relevance: this note covers the 1M token context window on Vertex (Opus 4.6+/Sonnet 4.6) enabled via the `[1m]` model-ID suffix or the setup wizard.
- [Access Control](../../term_dictionary/term_access_control.md) — regulating action on resources; relevance: the GCP project enablement, Model Garden approval, and quota allocation this note documents are access control over Vertex model invocation, plus the dedicated-project recommendation for cost/access isolation.

### 6. `cc_microsoft_foundry` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool being deployed on Foundry; relevance: this note is the full Claude-Code-on-Foundry setup (`CLAUDE_CODE_USE_FOUNDRY`, `ANTHROPIC_FOUNDRY_RESOURCE`, no setup wizard, env-var-only path).
- [Claude](../../term_dictionary/term_claude.md) — the Opus/Sonnet/Haiku model family deployed in Azure; relevance: step 1 creates Azure deployments for Claude Opus/Sonnet/Haiku and the pin step maps aliases to those deployment names.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — token-based credential chains; relevance: Microsoft Entra ID auth uses the Azure SDK default credential chain (token providers); the troubleshooting section centers on `azureADTokenProvider` token-acquisition failures.
- [Access Control](../../term_dictionary/term_access_control.md) — regulating who may invoke resources; relevance: Foundry's `Azure AI User` / `Cognitive Services User` RBAC roles (and the custom `Microsoft.CognitiveServices/accounts/providers/*` data action) are the access-control layer this note configures.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a managed endpoint fronting a backend service; relevance: `ANTHROPIC_FOUNDRY_RESOURCE`/`ANTHROPIC_FOUNDRY_BASE_URL` point Claude Code at the Azure-hosted Foundry endpoint (`{resource}.services.ai.azure.com/anthropic`) — the provider endpoint this note targets.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — runtime name→deployment resolution; relevance: Foundry has no startup model check, so pinning `ANTHROPIC_DEFAULT_*_MODEL` to the Azure deployment names is the only model-resolution path — a manual model-catalog binding this note stresses.

### 7. `cc_claude_platform_on_aws_setup` (7 term notes)
- [AWS — Amazon Web Services](../../term_dictionary/term_aws.md) — AWS accounts, credentials, regions, and Marketplace; relevance: Claude Platform on AWS uses AWS authentication, IAM access control, and AWS Marketplace billing — the entire setup runs on AWS primitives this note configures.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool being pointed at the AWS-fronted Anthropic API; relevance: this note configures `CLAUDE_CODE_USE_ANTHROPIC_AWS` + workspace ID and explains provider-routing precedence (Bedrock/Foundry over Claude Platform on AWS).
- [SigV4 — AWS Signature Version 4 Authentication](../../term_dictionary/term_sigv4.md) — AWS request signing; relevance: Option A signs every request with SigV4 using the AWS credential chain — the default auth path this note documents (with API-key precedence as the alternative).
- [IAM — AWS Identity and Access Management](../../term_dictionary/term_iam.md) — AWS identity/permission policies; relevance: the prereq is an IAM principal with permission to invoke the Anthropic service (`aws-external-anthropic` actions) — IAM is what authorizes SigV4 requests here.
- [Claude](../../term_dictionary/term_claude.md) — the Claude model family/IDs; relevance: Claude Platform on AWS uses the same model IDs as the direct Claude API, and this note pins `fable`/`opus`/`sonnet`/`haiku` aliases to specific Claude versions.
- [Access Control](../../term_dictionary/term_access_control.md) — regulating resource access; relevance: the AWS-Marketplace subscription provisions a *separate* Anthropic org with its own workspace ID and keys (credentials don't transfer) — an access-control isolation boundary this note warns about.
- [Prompt Caching — Bedrock Cached Prompt Prefix Optimization](../../term_dictionary/term_prompt_caching.md) — prefix caching to cut input-token cost; relevance: prompt caching is enabled automatically and this note documents the `ENABLE_PROMPT_CACHING_1H` 1-hour-TTL toggle and its higher billing rate.

### 8. `cc_claude_platform_on_aws_proxy_and_sdk` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool whose proxy routing and `/status` provider check are documented; relevance: this note covers Claude-Code-specific proxy switches (`ANTHROPIC_AWS_BASE_URL`, `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH`) and the `/status` troubleshooting flow.
- [SigV4 — AWS Signature Version 4 Authentication](../../term_dictionary/term_sigv4.md) — AWS request signing; relevance: `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH` makes Claude Code send unsigned requests so the gateway adds SigV4 headers before forwarding to AWS — a direct SigV4-delegation toggle.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — a server fronting backends, intercepting and forwarding client requests; relevance: "Route through a corporate proxy" points `ANTHROPIC_AWS_BASE_URL` at a proxy that forwards requests with workspace/auth headers — exactly the reverse-proxy interposition.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a managed front door with auth/routing; relevance: the proxy/LLM-gateway in this note can sign requests itself or require its own token (`ANTHROPIC_AUTH_TOKEN`) — the auth-injecting gateway pattern.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — bearer-token credentials; relevance: when the gateway requires its own token, it is supplied via `ANTHROPIC_AUTH_TOKEN` (a bearer credential) — the token-based gateway-auth path this note documents.
- [AWS — Amazon Web Services](../../term_dictionary/term_aws.md) — AWS credentials and regions; relevance: the Agent SDK example exports the same AWS env vars (`CLAUDE_CODE_USE_ANTHROPIC_AWS`, `ANTHROPIC_AWS_WORKSPACE_ID`, `AWS_REGION`) and relies on the ambient AWS credential chain for SigV4.

### 9. `cc_llm_gateway` (7 term notes)
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a centralized managed entry point fronting backend services with auth/routing/observability; relevance: an LLM gateway IS an API gateway specialized for model providers — this note's centralized-auth / usage-tracking / cost-control / audit-logging / model-routing list maps one-to-one to the API-gateway responsibilities.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — a server intermediating between clients and backends; relevance: the gateway is "a centralized proxy layer between Claude Code and model providers" — the reverse-proxy definition exactly, intercepting requests and forwarding to provider backends.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — a surrogate that implements the same interface as the real subject to control access; relevance: the gateway must expose one of the provider API formats (Anthropic Messages / Bedrock / Vertex) so Claude Code talks to it transparently — the proxy pattern's same-interface surrogate, adding auth/logging before delegating.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the client whose requests the gateway fronts; relevance: this note documents the Claude-Code attribution headers (`X-Claude-Code-Session-Id`, `-Agent-Id`, `-Parent-Agent-Id`), the system-prompt attribution block, and `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` — all Claude-Code-specific gateway contracts.
- [Subagent](../../term_dictionary/term_subagent.md) — a spawned isolated-context agent within a session; relevance: `X-Claude-Code-Agent-Id`/`-Parent-Agent-Id` let a proxy attribute API cost to individual parallel subagents/teammates and across nested agents — the headers are about subagent cost attribution.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — runtime model resolution and discovery (incl. gateway `/v1/models` endpoints); relevance: gateway model discovery queries the gateway's `/v1/models` and adds `claude`/`anthropic` entries to the `/model` picker — populating Claude Code's model catalog from the gateway, exactly the term's gateway-discovery case.
- [Prompt Caching — Bedrock Cached Prompt Prefix Optimization](../../term_dictionary/term_prompt_caching.md) — prefix caching keyed on request content; relevance: the attribution block is stripped by the Anthropic API so it doesn't affect first-party prompt caching, but a gateway with its own request-body-keyed cache should set `CLAUDE_CODE_ATTRIBUTION_HEADER=0` — a caching interaction this note explains.

### 10. `cc_llm_gateway_litellm` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — the client being configured against LiteLLM; relevance: this note sets Claude Code's gateway env vars (`ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, `apiKeyHelper`, the per-provider `CLAUDE_CODE_SKIP_*_AUTH`) to route through LiteLLM.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a managed proxy fronting backends; relevance: LiteLLM Proxy Server is the concrete LLM gateway this note configures — the unified Anthropic-format endpoint vs provider pass-through endpoints are gateway routing modes.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — runtime name→provider resolution (the term note cites LiteLLM's 2,600+ models / 140+ providers); relevance: LiteLLM's unified endpoint resolves model names across providers and load-balances — the canonical model-catalog/router this term references by name.
- [Load Balancer](../../term_dictionary/term_load_balancer.md) — distributes requests across backends for throughput/availability; relevance: the recommended unified endpoint's stated benefits are "load balancing" and "fallbacks" over pass-through endpoints — LiteLLM acting as a model-request load balancer.
- [OAuth Token Refresh](../../term_dictionary/term_oauth_token.md) — rotating/short-lived credentials; relevance: the dynamic `apiKeyHelper` path mints rotating per-user keys (vault fetch / JWT) refreshed on `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` — the rotating-token pattern this note documents.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — an intermediary forwarding client requests to backends; relevance: LiteLLM sits between Claude Code and the upstream providers (Claude API / Bedrock / Vertex / Claude Platform on AWS), forwarding signed or unsigned requests — the reverse-proxy role.

## Section Coverage Map

```
amazon-bedrock.md
├── Prerequisites ───────────────────────── → note 1 (cc_amazon_bedrock_setup)
├── Sign in with Bedrock (wizard) ────────── → note 1
├── Set up manually
│   ├── 1. Submit use case details ───────── → note 1
│   ├── 2. Configure AWS credentials (A-E) ── → note 1
│   │   └── Advanced credential config ───── → note 1 (awsAuthRefresh/awsCredentialExport)
│   ├── 3. Configure Claude Code (env) ────── → note 1
│   └── 4. Pin model versions ────────────── → note 2 (cc_amazon_bedrock_model_config)
│       └── Map each version → inf. profile ─ → note 2 (modelOverrides)
├── Startup model checks ─────────────────── → note 2
├── IAM configuration ────────────────────── → note 3 (cc_amazon_bedrock_features)
├── 1M token context window ──────────────── → note 3
├── Service tiers ────────────────────────── → note 3
├── AWS Guardrails ───────────────────────── → note 3
├── Use the Mantle endpoint (+5 H3) ──────── → note 4 (cc_amazon_bedrock_mantle_endpoint)
├── Troubleshooting
│   ├── Authentication loop (SSO/proxy) ──── → note 3
│   ├── Region issues ────────────────────── → note 3
│   └── Mantle endpoint errors ───────────── → note 4
└── Additional resources ─────────────────── → notes 1/3 (References)
google-vertex-ai.md
├── Prerequisites / Sign in / Region config ─ → note 5 (cc_google_vertex_ai)
├── Set up manually (1-5) ────────────────── → note 5
├── Startup model checks / IAM / 1M ──────── → note 5
├── Troubleshooting ──────────────────────── → note 5
└── Additional resources ─────────────────── → note 5 (References)
microsoft-foundry.md
├── Prerequisites / Setup (1-5) ──────────── → note 6 (cc_microsoft_foundry)
├── Azure RBAC configuration ─────────────── → note 6
├── Troubleshooting ──────────────────────── → note 6
└── Additional resources ─────────────────── → note 6 (References)
claude-platform-on-aws.md
├── (intro: what it is, separate org Note) ─ → note 7 (cc_claude_platform_on_aws_setup)
├── Prerequisites ────────────────────────── → note 7
├── Setup 1-3 (creds, configure, pin) ────── → note 7
├── Use the Agent SDK ────────────────────── → note 8 (cc_claude_platform_on_aws_proxy_and_sdk) (→ B19A/B21 SDK)
├── Route through a corporate proxy ──────── → note 8
├── Troubleshooting (403/workspace/endpoint) → note 8
└── Additional resources ─────────────────── → note 7 (References)
llm-gateway.md
├── (intro: what a gateway provides) ─────── → note 9 (cc_llm_gateway)
├── Gateway requirements (formats, headers) ─ → note 9
├── Configuration / Model selection ──────── → note 9 (gateway model discovery)
├── LiteLLM configuration (auth + endpoints) → note 10 (cc_llm_gateway_litellm)
└── Additional resources ─────────────────── → notes 9/10 (References)
```
Explicit cross-sub-plan link-outs (sections referenced, not duplicated — owned elsewhere):
`env-vars` full catalog → B03A; `model-config` (aliases/`modelOverrides`/`availableModels`) → B03B;
`settings` files → B03A; `prompt-caching` mechanism + cache lifetime → B02A; `mcp` tool search → B08A;
`tools-reference` WebSearch behavior → B03B; `network-config` enterprise proxy → B14B;
`agent-sdk/overview` → B19A. No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| amazon-bedrock (3,242w, 19 code, 11 H2) | notes 1,2,3,4 + link-outs | far over caps (19 code ≫ 6); 4 distinct BB/topic clusters: enable+auth (procedure), model pinning/checks (procedure), Bedrock features IAM/1M/tiers/guardrails (concept), the separate Mantle endpoint (procedure). |
| claude-platform-on-aws (2,005w, 8 code) | notes 7,8 | 8 code > 6 cap; setup+auth+pin (procedure) vs proxy-routing+Agent-SDK targeting (procedure, forward-refs B19/B21). |
| llm-gateway (1,154w, 9 code) | notes 9,10 | 9 code > 6 cap; gateway-abstraction requirements/headers/discovery (concept) vs concrete LiteLLM config (procedure). |
| google-vertex-ai (2,017w, 5 code) | note 5 (single) | within all caps after consolidation; one coherent provider procedure. |
| microsoft-foundry (1,006w, 7 code) | note 6 (single) | 7 code reduced to ≤6 by inlining the trivial `claude` run-command and `az login` one-liners as prose; one coherent provider procedure, small word count. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_amazon_bedrock_setup | procedure | 650 | 6 | ✅ (credential options A-E consolidated to ≤6 blocks) |
| 2 | cc_amazon_bedrock_model_config | procedure | 600 | 4 | ✅ |
| 3 | cc_amazon_bedrock_features | concept | 600 | 4 | ✅ (IAM JSON, tier export, guardrail JSON, caching toggles) |
| 4 | cc_amazon_bedrock_mantle_endpoint | procedure | 600 | 5 | ✅ |
| 5 | cc_google_vertex_ai | procedure | 750 | 5 | ✅ |
| 6 | cc_microsoft_foundry | procedure | 550 | 6 | ✅ (trivial run-command/az-login inlined as prose) |
| 7 | cc_claude_platform_on_aws_setup | procedure | 650 | 5 | ✅ |
| 8 | cc_claude_platform_on_aws_proxy_and_sdk | procedure | 450 | 3 | ✅ |
| 9 | cc_llm_gateway | concept | 600 | 1 | ✅ |
| 10 | cc_llm_gateway_litellm | procedure | 600 | 6 | ✅ (3 pass-through exports consolidated to fit ≤6) |

No note approaches the word/line caps. The two binding constraints were code-block counts on the bedrock,
claude-platform, and gateway pages — resolved by the splits above + consolidating adjacent one-line shell
exports. Every H2/H3 maps to a note or an explicit cross-sub-plan link-out (no over-compression).

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_amazon_bedrock_setup cc_amazon_bedrock_model_config cc_amazon_bedrock_features cc_amazon_bedrock_mantle_endpoint cc_google_vertex_ai cc_microsoft_foundry cc_claude_platform_on_aws_setup cc_claude_platform_on_aws_proxy_and_sdk cc_llm_gateway cc_llm_gateway_litellm"
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

Single phase (10 notes, all P3). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (env-var names/headers/IDs verbatim) | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 10 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 10 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree ≥1 query at finalization |
| G8-Discoverability (sibling) | intra-cluster sibling `cc_*` links present so the provider notes interlink (Bedrock 4-note set, gateway 2-note set, Claude-Platform 2-note set) | DB query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 10 rows** under a "Cloud Model Providers / Enterprise Deployment" cluster +
increments the BB-distribution counts (procedure +8, concept +2).

## Undigested Terms Plan (Step 4e)

B14A creates **0 new `term_dictionary` captures**. Every term these 5 pages introduce maps to an existing
substantive term note (link) or is a Claude-Code-specific doc concept owned by a `cc_` note here (Pattern B).
Dedup checked across **both** `term_dictionary/` AND `resources/documentation/` (the `claude_code/` folder is
empty pre-execution; no `cc_` provider note exists yet — all 10 are net-new, no recreation risk).

| Term surfaced on these pages | Disposition |
|---|---|
| Amazon Bedrock / Bedrock Invoke API / inference profile | doc concept in notes 1-4 (`cc_amazon_bedrock_*`); AWS/IAM/SigV4 grounded by existing term notes (link) |
| Mantle endpoint | doc concept in note 4 `cc_amazon_bedrock_mantle_endpoint` (Claude-Code-specific; no general term) |
| Google Vertex AI / Model Garden / `CLOUD_ML_REGION` | doc concept in note 5; `term_model_catalog` (Model Garden) linked |
| Microsoft Foundry / Entra ID / Azure RBAC | doc concept in note 6; `term_access_control` / `term_oauth_token` linked |
| Claude Platform on AWS / workspace ID / AWS Marketplace | doc concept in notes 7-8; `term_aws`/`term_sigv4`/`term_iam` linked |
| LLM gateway / proxy / LiteLLM / model discovery | doc concept in notes 9-10; `term_api_gateway`/`term_reverse_proxy`/`term_proxy_pattern`/`term_load_balancer`/`term_model_catalog` linked |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 5 pages scanning emphasis/tables/captions/code
comments for newly-surfaced non-glossary terms. Candidates considered and resolved without a new capture:
"inference profile" / "application inference profile ARN" → folded into note 2 (Bedrock model-config doc
concept; grounded by `term_model_catalog`); "Workload Identity Federation (X.509)" → folded into note 5
(Vertex credentials; grounded by `term_iam`/`term_oauth_token`); "service tier" → folded into note 3
(grounded by `term_latency`/`term_aws`); "pass-through endpoint" → folded into note 10 (grounded by
`term_reverse_proxy`/`term_api_gateway`). None is a cross-cutting vocabulary term lacking both a doc-page
home and an existing note. **0 new B14A `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B14A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these provider concepts duplicate existing notes?)
was performed: `term_aws`, `term_sigv4`, `term_iam`, `term_guardrails`, `term_prompt_caching`,
`term_context_window`, `term_model_catalog`, `term_api_gateway`, `term_reverse_proxy`, `term_proxy_pattern`,
`term_load_balancer`, `term_oauth_token`, `term_access_control`, `term_claude`, `term_amazon_nova`,
`term_latency`, `term_subagent`, `term_claude_code` all exist → linked, not recreated. No `cc_` provider doc
note duplicates an existing term note (the P0 failure class) — the `cc_*` notes are provider-deployment
procedures, distinct in scope from the conceptual term notes they link.

## Term-Note Authoring Requirements

**N/A for B14A** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory; copy env-var names, headers, model IDs, and IAM actions **verbatim** (these are load-bearing and error-prone).
- Code blocks verbatim; consolidate only adjacent trivial one-line shell exports to meet the ≤6 cap (documented per note in Density Re-Assessment). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Reindex incrementally after the phase; verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island, G7/G8):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_aws.md` | notes 1, 7 | AWS term → Bedrock setup + Claude Platform on AWS setup (the AWS-native deployment paths) |
| `term_dictionary/term_sigv4.md` | notes 1, 7 | SigV4 term → the two notes where Claude Code signs AWS requests with SigV4 |
| `term_dictionary/term_iam.md` | note 3 | IAM term → the canonical Bedrock IAM policy note |
| `term_dictionary/term_prompt_caching.md` | note 3 | Bedrock prompt-caching term → Bedrock features note (caching toggles) |
| `term_dictionary/term_api_gateway.md` | note 9 | API-gateway term → the LLM gateway concept note |
| `term_dictionary/term_model_catalog.md` | notes 5, 10 | model-catalog term (names Vertex Model Garden + LiteLLM) → Vertex + LiteLLM notes |
| `term_dictionary/term_claude_code.md` | note 1 | Claude Code term → the canonical Bedrock deployment entry note |

## Follow-up Recommendations

- After the 10 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; add intra-cluster sibling links (Bedrock 4-set, gateway 2-set, Claude-Platform 2-set; G8); queue the 10 rows for `entry_claude_code_docs.md`; `/tessellum-check-broken-links`.
- Consider a single shared "third-party provider routing precedence" callout (Bedrock > Foundry > Claude Platform on AWS > default) cross-linked from notes 1, 6, 7 — it recurs across pages.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B14A, 2026-06-13)

- **Source re-read (Step 2)**: all 5 pages re-read from `inbox/claude_code_docs/`; measured words match the master figures (amazon-bedrock 3,242 · google-vertex-ai 2,017 · microsoft-foundry 1,006 · claude-platform-on-aws 2,005 · llm-gateway 1,154 = 9,424). Per-section code-block counts measured to drive the splits (bedrock setup section alone = 11 code blocks → forced the 4-way bedrock split).
- **Notes**: 10 (procedure 8, concept 2) — raised from the master's estimate of 8 because three pages exceed the ≤6 code-block cap and require splitting (bedrock ×4, claude-platform ×2, gateway ×2). Documented in Split Decisions + Density Re-Assessment.
- **Step 2d new-term scan**: 4 candidates considered (inference profile, X.509 WIF, service tier, pass-through endpoint) — all folded into doc notes and grounded by existing term links; **0 new B14A term captures**.
- **Dedup (G-B)**: `claude_code/` doc folder empty pre-execution → no `cc_` recreation risk; 18 existing term notes confirmed present and linked, not recreated; no `cc_` doc note duplicates a term note.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G5 verification note, G8 sibling-discoverability gate.
- **28-item checklist**: PASS (term-note items N/A — B14A authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and self-reviewed; set to `ready` after the 9-checkpoint review below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7 inbound-discoverability + G8 sibling-cluster discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B14A contributes 10 rows under a Cloud Model Providers cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 10 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2 / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | All 10 notes 450–750w, ≤6 code; the 3 over-cap pages were split (bedrock ×4, claude-platform ×2, gateway ×2). None left borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Re-measured 2026-06-13: amazon-bedrock 3,242 / vertex 2,017 / foundry 1,006 / claude-platform 2,005 / gateway 1,154 = 9,424 = master figure (±0%). Per-section code counts also measured. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B14A authors 0 term notes; Undigested Terms Plan routes every surfaced term to an existing link / doc concept; Authoring Requirements inherited from master. |
| CP9 | Discoverability (G7/G8) executable | ✅ PASS | Inlinks table lists 7 concrete existing-note → new-note inbound links (each new note receives ≥1); intra-cluster sibling links specified for the Bedrock/gateway/Claude-Platform sets (G8). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
