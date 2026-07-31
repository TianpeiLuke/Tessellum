---
tags:
  - resource
  - terminology
  - security
  - oauth
  - rfc-7636
keywords:
  - PKCE
  - Proof Key for Code Exchange
  - code_verifier
  - code_challenge
  - S256
  - RFC 7636
  - OAuth 2.1
  - authorization code interception
topics:
  - Authentication protocols
  - OAuth authorization code flow
  - MCP remote-server auth
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/OAuth#PKCE
access_control_group: ["general"]
---

# PKCE - Proof Key for Code Exchange

## Definition

**PKCE** ("pixie", *Proof Key for Code Exchange*, RFC 7636) is an extension to the OAuth 2.0 authorization-code grant that defends against the **authorization-code interception attack** without requiring the client to hold a pre-registered secret. On each authorization request the client generates a high-entropy random **code verifier**, derives a transformed **code challenge** from it, and sends only the challenge to the authorization endpoint; later, at the token endpoint, it presents the original verifier. Because the verifier travels only over the TLS-protected back-channel, an attacker who intercepts the front-channel authorization code (for example, a malicious app that registered the same custom URI scheme as a legitimate native app) cannot redeem it — they lack the secret that the authorization server re-derives and compares.

PKCE was created for **public clients** (native apps, single-page apps, CLIs) that cannot keep a `client_secret` confidential, but **OAuth 2.1 makes PKCE mandatory for every client using the authorization-code flow** — public *and* confidential — folding RFC 7636 into the core spec and removing the implicit grant in its favor. It is also the linchpin of the **Model Context Protocol (MCP) authorization spec**, which requires MCP clients connecting to remote HTTP MCP servers to implement PKCE per OAuth 2.1 § 7.5.2 alongside dynamic client registration and resource-indicator audience binding.

## Context

PKCE sits inside the authorization-code flow of any system whose clients run outside a trusted server — IDE plugins, desktop agents, mobile apps, and CLIs that open a loopback redirect to capture the callback. In the **Hermes agent**, declaring `auth: oauth` on a remote HTTP `mcp_servers` entry triggers the full OAuth 2.1 handshake — discovery, dynamic client registration (RFC 7591), **PKCE**, token exchange, refresh, and step-up — driven by the MCP Python SDK. Hermes prints an authorize URL, waits for the OAuth callback on a local loopback port, and caches the resulting tokens at `~/.hermes/mcp-tokens/<server>.json` with `0o600` perms; the same machinery seeds OAuth-token credential pools and powers the subscription proxy's Portal login.

Beyond agents, PKCE is the de-facto baseline for OAuth in browser-based apps (OAuth 2.0 for Browser-Based Apps BCP) and native apps (RFC 8252), and is recommended by the OAuth 2.0 Security Best Current Practice for all authorization-code clients. It composes with — but is distinct from — the `state` parameter (CSRF protection) and exact redirect-URI matching: PKCE binds the *token exchange* to the *original requestor*, while `state` binds the *callback* to the *original request*.

## Key Characteristics

- **Code verifier**: a cryptographically random string of 43–128 characters drawn from the unreserved set `[A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"`; RFC 7636 recommends 32 random octets base64url-encoded (a 43-char string, ≥256 bits of entropy).
- **Code challenge transformation** `t(code_verifier)` selected by `code_challenge_method`:
  - `S256` (mandatory to implement, REQUIRED when the client can compute SHA-256): $$\text{code\_challenge} = \text{BASE64URL\text{-}ENCODE}(\text{SHA256}(\text{ASCII}(\text{code\_verifier})))$$
  - `plain`: `code_challenge = code_verifier` — compatibility only; SHOULD NOT be used in new implementations.
- **Token-endpoint verification**: the server re-applies the bound method to the received verifier and checks equality against the stored challenge; on mismatch it returns `invalid_grant`. This is the proof that the redeeming party is the original requestor.
- **No shared secret required**: PKCE replaces the `client_secret` for public clients, so the security does not depend on a credential that a distributable binary cannot protect.
- **Defends authorization-code interception/injection**: the front-channel code alone is useless without the back-channel verifier.
- **Mandatory under OAuth 2.1**: required for all authorization-code clients (public and confidential); the implicit grant is removed, pushing flows to authorization-code + PKCE.
- **Composes with audience binding**: in MCP, PKCE is paired with the RFC 8707 `resource` parameter so tokens are bound to the specific MCP server and cannot be replayed across services.
- **Distinct from `state`**: `state` is a CSRF / request-binding nonce on the callback; PKCE is a cryptographic binding of the *code exchange*. Robust clients use both.

## Related Terms


## References

- [RFC 7636 — Proof Key for Code Exchange by OAuth Public Clients](https://datatracker.ietf.org/doc/html/rfc7636): the canonical specification — defines `code_verifier`/`code_challenge`, the `plain`/`S256` methods, the `S256` transformation, verifier length/charset, and the token-endpoint `t(code_verifier)` comparison.
- [OAuth 2.1 — oauth.net/2.1](https://oauth.net/2.1/): consolidates RFC 7636 into core OAuth and makes PKCE mandatory for all authorization-code clients; removes the implicit grant and ROPC.
- [draft-ietf-oauth-v2-1 — The OAuth 2.1 Authorization Framework](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13): § 7.5.2 mandates PKCE to mitigate authorization-code interception/injection.
- [MCP Authorization Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization): requires MCP clients to implement PKCE per OAuth 2.1 § 7.5.2, with RFC 7591 dynamic client registration and RFC 8707 resource-indicator audience binding.
- [RFC 8252 — OAuth 2.0 for Native Apps](https://datatracker.ietf.org/doc/html/rfc8252): the native-app BCP that mandates PKCE and loopback/redirect handling — the pattern Hermes uses for its loopback OAuth callback.
- [Wikipedia — OAuth (PKCE)](https://en.wikipedia.org/wiki/OAuth#PKCE): background on the authorization-code interception attack and PKCE's verifier/challenge mitigation.
