---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - http_api
keywords:
  - clawhub http api conventions
  - clawhub base url api v1
  - clawhub rate limits 429 retry-after
  - clawhub error responses plain text
  - clawhub legacy cli endpoints deprecated
  - well-known clawhub.json discovery
  - cf-connecting-ip trusted forwarding
  - clawhub public catalog reuse
  - per-ip per-key rate buckets
topics:
  - OpenClaw
  - ClawHub HTTP API
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/clawhub/http-api
access_control_group: ["general"]
---

# OpenClaw — ClawHub HTTP API Conventions (Base URL, Rate Limits, Errors, Discovery)

## Overview

This note captures the cross-cutting **conventions** of the ClawHub HTTP API — the rules that apply across every endpoint rather than any single route — mirroring the introductory and shared-policy sections of the `clawhub/http-api` source page. ClawHub is OpenClaw's registry for skills and plugins, and these conventions define the contract that third-party directories, the `clawhub` CLI, and self-hosters all consume: the base URL and API versioning, the public-catalog-reuse policy, the per-IP / per-key rate-limit model (buckets, headers, `429`/`Retry-After` backoff, client-IP source), the plain-text error-response format, the deprecated legacy CLI endpoints, and registry discovery via `/.well-known/clawhub.json`. The per-endpoint request/response catalogs are documented separately in the two sibling notes (public read surface and authenticated write/admin surface).

## Base URL, Versioning, and OpenAPI

The default base URL is `https://clawhub.ai`. All v1 paths live under `/api/v1/...`. Legacy `/api/...` and `/api/cli/...` paths remain for backward compatibility (their removal plan lives in `DEPRECATIONS.md`). A machine-readable schema is served at `/api/v1/openapi.json`. Web slug shortcuts (the human-facing `https://clawhub.ai/<owner>/<slug>` URLs) resolve across registry families, but API clients should use the canonical URLs returned by read endpoints rather than reconstructing route precedence themselves.

## Public Catalog Reuse

Third-party directories may use the public read endpoints to list or search ClawHub skills, subject to a behavioral policy. Reusers should cache results, honor `429`/`Retry-After`, link users back to the canonical ClawHub listing (`https://clawhub.ai/<owner>/<slug>`), and avoid implying ClawHub endorsement of the third-party site. They must not attempt to mirror hidden, private, or moderation-blocked content outside the public API surface.

## Rate Limits

The enforcement model distinguishes anonymous from authenticated callers. Anonymous requests are enforced **per IP**; authenticated requests (a valid Bearer token) are enforced **per user bucket**; if a token is missing or invalid, behavior falls back to IP enforcement. Authenticated write endpoints should not return a bare `Unauthorized` when the server knows the reason: missing tokens, invalid/revoked tokens, and deleted/banned/disabled accounts should each get actionable text so CLI clients can tell users what blocked them.

The configured limits are three distinct buckets, each given as a per-IP and a per-key allowance:

- **Read**: `3000/min` per IP, `12000/min` per key
- **Write**: `300/min` per IP, `3000/min` per key
- **Download**: `1200/min` per IP, `6000/min` per key (download endpoints)

Responses carry both legacy-compatibility headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) and standardized headers (`RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`); on a `429` a `Retry-After` header is also sent. The header time semantics differ and matter for clients: `X-RateLimit-Reset` is an absolute Unix epoch-seconds timestamp, `RateLimit-Reset` is seconds-until-reset (a delay), and `Retry-After` is the number of seconds to wait before retrying on `429`.

A representative `429` response is plain text with both header families populated:

```http
HTTP/2 429
content-type: text/plain; charset=utf-8
x-ratelimit-limit: 20
x-ratelimit-remaining: 0
x-ratelimit-reset: 1771404540
ratelimit-limit: 20
ratelimit-remaining: 0
ratelimit-reset: 34
retry-after: 34

Rate limit exceeded
```

Client backoff guidance follows from those headers: if `Retry-After` exists, wait that many seconds before retrying; use jittered backoff to avoid synchronized retries across clients; and if `Retry-After` is missing, fall back to `RateLimit-Reset` (or compute the delay from the absolute `X-RateLimit-Reset`).

### Client-IP Source for Per-IP Buckets

For per-IP enforcement the API derives the client IP from `cf-connecting-ip` (Cloudflare) by default, and ClawHub uses trusted forwarding headers to identify client IPs at the edge. If no trusted client IP is available, anonymous **download** requests use an endpoint-scoped fallback bucket instead of one global `ip:unknown` bucket; anonymous **read/write** requests still use the shared unknown bucket, so missing-IP routing stays visible and conservative.

## Error Responses

Public v1 error responses are **plain text** with `content-type: text/plain; charset=utf-8`. This format covers validation failures (`400`), missing public resources (`404`), auth and permission failures (`401`/`403`), rate limits (`429`), and blocked downloads. Clients should read the response body as a human-readable string. Unknown query parameters are ignored for compatibility, but a recognized query parameter supplied with an invalid value returns `400`.

## Legacy CLI Endpoints (Deprecated)

A set of `/api/cli/...` endpoints remains supported for older CLI versions, with a removal plan tracked in `DEPRECATIONS.md`. The deprecated routes are `GET /api/cli/whoami`, `POST /api/cli/upload-url`, `POST /api/cli/publish`, `POST /api/cli/telemetry/install`, `POST /api/cli/skill/delete`, and `POST /api/cli/skill/undelete`. The staged-upload helper `POST /api/cli/upload-url` returns `uploadUrl` and `uploadTicket`; a package publish that stages a ClawPack tarball must send the resulting storage id as `clawpack` and the returned ticket as `clawpackUploadTicket`.

## Registry Discovery (`/.well-known/clawhub.json`)

The CLI can discover registry/auth settings directly from a site. The preferred discovery document is `/.well-known/clawhub.json` (JSON); `/.well-known/clawdhub.json` is the legacy fallback. The schema is a small JSON object:

```json
{ "apiBase": "https://clawhub.ai", "authBase": "https://clawhub.ai", "minCliVersion": "0.0.5" }
```

Self-hosters should serve this file so clients can auto-discover the registry, or set `CLAWHUB_REGISTRY` explicitly (the legacy environment variable is `CLAWDHUB_REGISTRY`).

**Source**: OpenClaw documentation — `clawhub/http-api` (mirror `inbox/openclaw_docs/clawhub/http-api.md`), conventions sections only
**Last Updated**: 2026-06-22
**Status**: Active
