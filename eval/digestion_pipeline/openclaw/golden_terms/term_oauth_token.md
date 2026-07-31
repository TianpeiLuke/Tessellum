---
tags:
  - resource
  - terminology
  - oauth-token
  - oauth-refresh
  - rfc-6749
  - credential-rotation
  - openclaw
keywords:
  - OAuth refresh token
  - OAuth 2.0
  - RFC 6749
  - locked refresh
  - thundering herd
  - per-key refresh queue
  - token rotation
topics:
  - Authentication protocols
  - Credential management
  - OpenClaw auth profiles
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/OAuth
access_control_group: ["general"]
---

# OAuth Token Refresh

## Definition

OAuth 2.0 (RFC 6749) decouples the long-lived **refresh token** from the short-lived **access token**: the access token is the bearer credential a client sends to resource servers, while the refresh token is presented only to the authorization server's token endpoint to mint replacement access tokens via `grant_type=refresh_token` (RFC 6749 § 1.5, § 6). The grammar is asymmetric — RFC 6749 § 6 says the server "issues a new access token (and, optionally, a new refresh token)" — and modern providers exploit the optional clause to perform **refresh-token rotation**: each refresh returns a new refresh token and revokes its predecessor (after a brief grace period in Slack's case), so a stolen refresh token reveals itself the next time the legitimate client tries to use it.

Rotation creates a concurrency hazard known as the **OAuth refresh thundering herd**: if N concurrent in-process callers all observe an expired access token at the same instant and each fires a refresh, only the first wins — the rest race against a refresh token that has already been rotated and get back `refresh_token_reused` errors that some providers escalate to full re-auth. The industry remedy is the **locked-refresh + per-key queue** pattern: a per-`(provider, profileId)` mutex (or a shared `Promise` map) serializes in-process callers so that exactly one refresh fires per key and the rest await its result, while an outer file or distributed lock extends the same guarantee across processes.

## Context

OAuth refresh-token plumbing sits inside every agent runtime that talks to a cloud LLM or messaging provider via OAuth rather than a static API key. Anthropic Claude Code, OpenAI organization auth, Slack/Discord/Telegram channel adapters, and IDP-mediated agent auth flows all issue access tokens with 1-hour to 12-hour TTLs and rely on the refresh path to keep autonomous sessions alive. When concurrency is mishandled the symptoms are visible — issues #29257 and #12447 in `anthropics/claude-code` and #26322 in `openclaw/openclaw` are all reports of multi-instance refresh races causing spurious re-auth prompts.

In the **OpenClaw** agent framework, the `auth-profiles` subsystem is the canonical industry implementation of the locked-refresh + per-key queue pattern. `oauth-manager.ts` owns a `Map<string, Promise<unknown>>` refresh queue keyed by `(provider, profileId)` plus a cross-process file lock; `refreshOAuthTokenWithLock` chains in-process callers through `await prev` and then runs `doRefreshOAuthTokenWithLock` once, spreading `{ ...credentialToRefresh, ...refreshed, type: "oauth" }` so a rotated refresh token replaces the old one in place. The failure path is a four-step cascade — re-read the store in case a peer process refreshed, detect `refresh_token_reused`, load-fresh-or-retry once, then fall back to inheriting from the main agent's store — and the portability rule defaults OAuth credentials to non-portable when an agent forks because the refresh token is single-use.

## Key Characteristics

- **Access token vs refresh token (RFC 6749 § 1.5)**: access tokens are bearer credentials for resource servers; refresh tokens are presented only to the authorization server and never travel to a resource server.
- **Refresh-token rotation**: providers that opt into rotation revoke the old refresh token (Slack: after a short grace period) and return a new one in the same response — single-use refresh tokens shrink the window of compromise to one rotation interval.
- **Thundering-herd hazard**: N concurrent callers seeing an expired token at the same time each fire a refresh; only one survives the rotation, the rest get `refresh_token_reused` and may be force-logged-out.
- **Locked-refresh pattern**: a per-key mutex (in-process) plus a file or distributed lock (cross-process) ensures exactly one refresh fires per `(provider, identity)` key; later callers await the shared `Promise` and read the rotated token from the persisted store.
- **Per-key queue keying**: keyed by `(provider, profileId)` (OpenClaw) or `(connectionId, userId)` (Nango) — finer than a global lock so different identities still parallelize.
- **Hard timeout on the refresh call**: a hung provider must not hold the lock forever; OpenClaw wraps the call in `withRefreshCallTimeout`.
- **Persist-before-return**: the rotated credential is saved to the auth store before the caller receives the new access token, so a peer reader sees consistent state.
- **Failure recovery cascade**: cheapest-first — re-read store, detect-reuse-and-retry-once, inherit-from-main-store, finally wrap and rethrow with snapshot.
- **Grant types (RFC 6749)**: authorization-code (with PKCE for public clients per RFC 7636), client-credentials, resource-owner-password (deprecated), device-code (RFC 8628), and the refresh grant itself.
- **PKCE (RFC 7636)**: code-verifier/code-challenge pair that hardens authorization-code grants against intercepted-code attacks for native and SPA clients.
- **Non-portable refresh tokens**: forks/copies of an agent must NOT carry the refresh token by default — it is bound to the issuing CLI identity and single-use; OpenClaw enforces this via `resolveAuthProfilePortability`.
- **Distinct from sliding session**: a sliding session extends a server-side cookie on every request; OAuth refresh is a client-driven exchange against the token endpoint with a separate credential.

## Related Terms


### Related Code Snippets

- [OpenClaw Agents — auth-profiles — OAuth Refresh, Rotation, Portability (#591)](../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md): the canonical OpenClaw implementation — `refreshOAuthCredential` provider dispatch, `createOAuthManager` factory, `refreshOAuthTokenWithLock` per-key queue, failure-cascade, and the non-portable-refresh-token portability rule.

## References

- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749): the canonical specification; § 1.5 defines refresh tokens, § 6 defines the `grant_type=refresh_token` exchange and the optional new-refresh-token clause that rotation exploits.
- [OAuth 2.0 — oauth.net](https://oauth.net/2/): the OAuth working group's hub with current best-practice references, including the Security BCP and the Browser-Based Apps BCP that codify rotation and PKCE.
- [Wikipedia — OAuth](https://en.wikipedia.org/wiki/OAuth): foundational background, grant-type taxonomy, and historical context for the OAuth 1.0 → 2.0 → 2.1 evolution.
- [Slack — Using token rotation](https://docs.slack.dev/authentication/using-token-rotation/): industry implementation reference — 12-hour access-token TTL, refresh-token revocation after a short grace period, and the 2-active-token limit.
- [Nango — How to handle concurrency with OAuth token refreshes](https://nango.dev/blog/concurrency-with-oauth-token-refreshes/): industry write-up of the locked-refresh + per-connection-key queue pattern with in-memory `Map` and Redis distributed-lock variants — the same shape OpenClaw's `auth-profiles` implements.
