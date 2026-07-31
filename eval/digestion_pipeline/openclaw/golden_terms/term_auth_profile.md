---
tags:
  - resource
  - terminology
  - openclaw
  - agent_framework
  - auth-profile
  - credential-management
  - oauth
  - round-robin
  - identity
keywords:
  - auth profile
  - per-agent credential
  - round-robin order pipeline
  - credential expiry state machine
  - external CLI sync
  - identity-match gate
  - OAuth refresh queue
  - portability decision
  - secret-ref sanitizer
  - locked refresh
topics:
  - Credential management
  - Multi-provider authentication
  - OpenClaw architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/tree/main/src/agents/auth-profiles
access_control_group: ["general"]
---

# Auth Profile

## Definition

An **auth profile** is a named credential record — `(profileId, provider, type ∈ {api_key, token, oauth, aws-sdk}, secret-or-secretRef, optional accountId/email, optional expires)` — that an agent runtime selects, validates, rotates, and persists on behalf of a single provider account. The pattern generalises the multi-credential management problem that every multi-provider LLM client now faces: industry frameworks address it differently — **LiteLLM** routes across model deployments with per-deployment fallback chains, automatic cooldown on 429s, and round-robin/latency/weighted strategies (LiteLLM Router); **Auth0 Token Vault** stores per-user external tokens and silently refreshes them via OAuth 2.0 Token Exchange (RFC 8693) so the application code never sees a refresh token; **LangChain** keeps the simplest model — one provider, one env var (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, …) — and delegates rotation to external secret managers. "Auth profile" is the OpenClaw name for a credential-record-plus-policy-state object that sits between the simple env-var model and the full token-vault service.

In **OpenClaw** the term refers concretely to the `src/agents/auth-profiles/` cluster: a persisted `AuthProfileStore` (`{version, profiles, order, usageStats}`) merged with the runtime `OpenClawConfig.auth.profiles` config, plus the order pipeline (`order.ts`), credential-state machine (`credential-state.ts`), OAuth secret-ref policy gate (`policy.ts`), external-CLI sync (`external-cli-sync.ts`), persisted-store normaliser (`persisted.ts`), locked OAuth refresh (`oauth.ts` + `oauth-manager.ts`), and portability decision record (`portability.ts`). Together these implement **per-key round-robin rotation with cooldown** (the LiteLLM analog), **secret-ref sanitisation** so OAuth credentials (which mutate at runtime) cannot be backed by an immutable secret reference, **identity-match safety gates** so a Codex CLI re-auth on the host machine cannot silently overwrite the agent's locally-refreshed token, and **portability decisions** so single-use OAuth refresh tokens are excluded from agent-fork copies unless the credential opts in.

## Context

Auth profiles sit at the seam between the agent's model-failover layer and the cloud LLM/provider APIs. Every time the failover ladder reaches for a credential — Anthropic, OpenAI, Google, Codex CLI, Claude CLI, MiniMax, Amazon Bedrock — `resolveAuthProfileOrder` produces an ordered list of profile IDs to try, the model layer iterates it until one succeeds, and the chosen profile's `usageStats.lastUsed` is updated so the next call round-robins to a sibling. Failures bump the per-profile error counter; sufficient errors trip a cooldown window so the deployment is skipped without being removed (LiteLLM's deployment-isolation pattern). The same store also holds OAuth credentials for cross-run refresh — the OAuth refresh queue is the most-cited concurrency-hazard module in the auth-profiles cluster (issues #29257 / #12447 / #26322 in the Claude Code and OpenClaw repos are all multi-instance refresh races).

OpenClaw's auth-profiles also coordinate with external **non-OpenClaw credential sources**: the Claude CLI's keychain credential, the OpenAI Codex CLI's filesystem-backed credential, and the MiniMax CLI all surface OAuth tokens that OpenClaw can adopt as a bootstrap value for an empty profile slot. The `external-cli-sync.ts` module wraps this with an **identity-match gate** (`accountId` or normalized `email` must match) so that a host-machine re-auth as a different user cannot silently replace the agent's stored credential. Codex specifically is marked `bootstrapOnly` — once OpenClaw has refreshed the token locally, the CLI's potentially-stale token must not shadow it.

## Key Characteristics

- **Round-robin order pipeline (`resolveAuthProfileOrder`)** — sweeps expired cooldowns, resolves a base order from stored/configured/discovered profile IDs, filters by eligibility, repairs config/store drift (when configured IDs no longer exist, fall back to provider-scoped store scan), de-duplicates, then sorts by mode (round-robin) or honours an explicit order.
- **Type+lastUsed sorter (`orderProfilesByMode`)** — partitions into available vs in-cooldown, then primary-sorts available by `typeScore` (oauth=0, token=1, api_key=2 — prefer OAuth identity over raw keys), secondary-sorts by `lastUsed` oldest-first (round-robin within type), appends cooldown-sorted profiles at the tail.
- **Credential expiry state machine (`resolveTokenExpiryState`)** — five-state classifier over `expires` (epoch-ms) → `missing` | `valid` | `expiring` | `expired` | `invalid_expires` with a configurable `expiringWithinMs` margin (default 5 min for OAuth refresh).
- **Credential eligibility evaluator (`evaluateStoredCredentialEligibility`)** — branches by `type`: `api_key` needs `key` OR `keyRef`; `token` adds an expiry check; `oauth` needs `access` OR `refresh`. Returns `{eligible, reasonCode}` so the order pipeline can report `missing_credential` / `invalid_expires` / `expired` / `unresolved_ref` upstream.
- **OAuth secret-ref policy gate (`assertNoOAuthSecretRefPolicyViolations`)** — throws if any profile with `type="oauth"` OR `mode="oauth"` carries a `SecretRef`, because OAuth credentials are runtime-mutable (refresh-token rotation overwrites them) and cannot be backed by an immutable reference.
- **Identity-match safety gate (`isSafeToUseExternalCliCredential`)** — for external CLI sync: provider must match; if both sides have `accountId` or `email`, they must be equal; if existing has any identity and imported has none, refuse.
- **Provider registry & runtime bootstrap** — the `EXTERNAL_CLI_SYNC_PROVIDERS` list registers Codex (`bootstrapOnly`), Claude CLI, and MiniMax as adoption sources; the runtime bootstrap hook adopts an external credential only when the local slot is empty AND identity-safe.
- **Two-store merge (`persisted.ts`)** — the persisted JSON store and the live runtime config are merged by `overlayRuntimeExternalOAuthProfiles`; the persisted entry wins for static fields, the runtime entry wins for refreshed OAuth tokens.
- **Secret-ref sanitiser (`normalizeRawCredentialEntry` + `coerceSecretRef`)** — legacy entries with `apiKey`/`mode` fields are normalised to `key`/`type`; raw object values are promoted to `keyRef`/`tokenRef`; rejected entries get a typed reason (`non_object` / `invalid_type` / `missing_provider`).
- **Locked OAuth refresh + token rotation (`oauth-manager.ts`)** — `refreshOAuthTokenWithLock` chains in-process callers through a per-`(provider, profileId)` `Promise` queue; the inner `doRefreshOAuthTokenWithLock` acquires a global file lock plus an auth-store lock, re-checks usability under the lock, dispatches the adapter refresh (plugin → Chutes → pi-ai OAuth), spreads `{...credentialToRefresh, ...refreshed, type: "oauth"}` so rotated refresh tokens land atomically, persists, and returns.
- **Per-key refresh queue + failure cascade** — keyed by `(provider, profileId)` so different identities still parallelise; on failure, re-read the store (a peer process may have refreshed), detect `refresh_token_reused`, load-fresh-or-retry once, then fall back to inheriting from the main agent's store if identity-safe (`isSafeToAdoptMainStoreOAuthIdentity`).
- **Portability decision record (`resolveAuthProfilePortability`)** — returns `{portable, reason}` ∈ {`portable-static-credential`, `non-portable-oauth-refresh-token`, `credential-opted-out`, `oauth-provider-opted-in`}. OAuth defaults to non-portable because refresh tokens are single-use; static credentials default to portable; `credential.copyToAgents` is an explicit override in either direction.

## Related Terms

- **[Band register-agent (one-time API key) endpoint](../documentation/band/band_human_api_profile_agents.md)**: band note covering the human/API profile-agents endpoints (`POST /me/agents/register` and owned-agents management); relevance: that endpoint mints exactly the kind of per-agent credential this concept describes — a one-time API key the remote agent carries — making it the concrete issuance/scoping point for an auth-profile-style credential.

### Related Code Snippets

- [Auth Profiles — Order + Credential State + OAuth Policy (snippet #589)](../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md): `resolveAuthProfileOrder` round-robin pipeline, the type+lastUsed sorter, the five-state expiry classifier, the eligibility evaluator, and the OAuth SecretRef policy gate.
- [Auth Profiles — External CLI Sync (snippet #590)](../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md): `EXTERNAL_CLI_SYNC_PROVIDERS` registry, identity-match safety gate, and the Codex `bootstrapOnly` rule.
- [Auth Profiles — OAuth Refresh + Portability (snippet #591)](../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md): locked refresh + per-key queue, refresh-failure recovery cascade, and the portability decision record.

## References

- [Authentication — Wikipedia](https://en.wikipedia.org/wiki/Authentication)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [Router — Load Balancing | LiteLLM Docs](https://docs.litellm.ai/docs/routing)
- [Router Architecture (Fallbacks / Retries) | LiteLLM Docs](https://docs.litellm.ai/docs/router_architecture)
- [Auth0 Token Vault for AI Agents](https://auth0.com/ai/docs/intro/token-vault)
- [Configure Token Vault — Auth0 Docs](https://auth0.com/docs/secure/call-apis-on-users-behalf/token-vault/configure-token-vault)
- [OpenClaw `src/agents/auth-profiles/`](https://github.com/openclaw/openclaw/tree/main/src/agents/auth-profiles)
