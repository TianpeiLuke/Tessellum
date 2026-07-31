---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - rest_api
keywords:
  - clawhub api v1
  - clawhub rest api
  - public catalog reuse
  - bearer clh_ token
  - rate limit buckets retry-after
  - x-ratelimit headers
  - plain text errors
  - public read auth admin endpoints
topics:
  - OpenClaw
  - ClawHub API
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/clawhub/api
access_control_group: ["general"]
---

# OpenClaw — ClawHub Public REST API (v1)

## Overview

This note models the **ClawHub public REST API v1** contract: its base URL and OpenAPI document, the rules for reusing the public catalog, anonymous-vs-Bearer authentication, the auth-aware rate-limit buckets and headers, the plain-text error conventions, and the full endpoint surface (public read, auth required, admin only) plus the legacy aliases. It mirrors the `clawhub/api` source page. The API base is `https://clawhub.ai` and the machine-readable contract is served at `/api/v1/openapi.json`. This is the read/write surface that the `clawhub` CLI, the OpenClaw gateway install/update path, and third-party catalogs all consume; token creation, storage, and revocation are owned by the ClawHub auth note, not redefined here.

## Public Catalog Reuse

You can build a third-party catalog, directory, or search surface on top of ClawHub's public read APIs. Public skill metadata and skill files are published under ClawHub's skill license rules, while the API itself is rate-limited and should be consumed responsibly. The page states the following guidelines: use public read endpoints such as `GET /api/v1/skills`, `GET /api/v1/search`, and `GET /api/v1/skills/{slug}` for catalog listings; cache responses and respect `429`, `Retry-After`, and rate-limit headers instead of polling aggressively; link back to the canonical ClawHub skill URL when displaying listings so users can inspect the source registry record; use canonical page URLs in the form `https://clawhub.ai/<owner>/<slug>`; do not imply that ClawHub endorses, verifies, or operates the third-party site; and do not mirror hidden, private, or moderation-blocked content by bypassing public API filters or auth boundaries.

## Auth

Authentication is a two-tier model. **Public read** requires no token. **Write + account** operations require a Bearer credential: `Authorization: Bearer clh_...`. Token lifecycle (sign-in, creation, per-OS storage, and revocation) is documented separately in the ClawHub auth note and is not duplicated here.

## Rate Limits

Enforcement is **auth-aware** and keyed by identity. Anonymous requests are limited per IP; authenticated requests with a valid Bearer token are limited per user bucket; a missing or invalid token falls back to IP enforcement. The buckets are:

- **Read**: 3000/min per IP, 12000/min per key.
- **Write**: 300/min per IP, 3000/min per key.
- **Download**: 1200/min per IP, 6000/min per key.

Responses carry the rate-limit headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, and `Retry-After` (on `429`). The header semantics are explicit: `X-RateLimit-Reset` is the Unix epoch seconds of the absolute reset time, `RateLimit-Reset` is the delay in seconds until reset, and `Retry-After` is the delay in seconds to wait on a `429`. An example `429` response illustrates the headers:

```http
HTTP/2 429
x-ratelimit-limit: 20
x-ratelimit-remaining: 0
x-ratelimit-reset: 1771404540
ratelimit-limit: 20
ratelimit-remaining: 0
ratelimit-reset: 34
retry-after: 34
```

For client handling the page prescribes: prefer `Retry-After` when present; otherwise use `RateLimit-Reset` or derive the delay from `X-RateLimit-Reset`; and add jitter to retries.

## Errors

v1 errors are returned as plain text (`text/plain; charset=utf-8`), including the `400`, `401`, `403`, `404`, `429`, and blocked-download responses. Unknown query parameters are ignored for compatibility, while known query parameters with invalid values return `400`.

## Endpoints

The endpoint surface is split into three access tiers.

### Public read

These require no token:

- `GET /api/v1/search?q=...` — optional filters `highlightedOnly=true`, `nonSuspiciousOnly=true`; legacy alias `nonSuspicious=true`.
- `GET /api/v1/skills?limit=&cursor=&sort=` — `sort` accepts `updated` (default), `recommended` (`default`), `createdAt` (`newest`), `stars` (`rating`), `installsCurrent` (`installs`), `installsAllTime`, and `trending`; invalid `sort` values return `400`; `cursor` applies to non-`trending` sorts; optional filter `nonSuspiciousOnly=true` with legacy alias `nonSuspicious=true`. With `nonSuspiciousOnly=true`, cursor-based pages may contain fewer than `limit` items, so use `nextCursor` to continue. `recommended` uses engagement and recency signals.
- `GET /api/v1/skills/{slug}` — the registry record for a single skill.
- `GET /api/v1/skills/{slug}/moderation` — moderation state for a skill.
- `GET /api/v1/skills/{slug}/versions?limit=&cursor=` — paginated version listing.
- `GET /api/v1/skills/{slug}/versions/{version}` — a single version record.
- `GET /api/v1/skills/{slug}/scan?version=&tag=` — scan results for a version/tag.
- `GET /api/v1/skills/{slug}/file?path=&version=&tag=` — a file from a skill bundle.
- `GET /api/v1/resolve?slug=&hash=` — resolve a slug + content hash.
- `GET /api/v1/download?slug=&version=&tag=` — download a skill artifact.
- `GET /api/v1/packages?limit=&cursor=&sort=` — `sort` accepts `updated` (default), `recommended`, `installs`; invalid `sort` values return `400`.
- `GET /api/v1/plugins?limit=&cursor=&sort=` — `sort` accepts `recommended` (default), `installs`, `updated`.
- `GET /api/v1/plugins/search?q=...` — plugin search.
- `GET /api/v1/packages/{name}/versions/{version}/artifact` — a package version artifact.
- `GET /api/v1/packages/{name}/versions/{version}/security` — security data for a package version.
- `GET /api/v1/packages/{name}/versions/{version}/artifact/download` — download a package artifact.
- `GET /api/npm/{package}` — npm-compatible package metadata.
- `GET /api/npm/{package}/-/{tarball}.tgz` — npm-compatible tarball fetch.

### Auth required

These require a valid Bearer token:

- `POST /api/v1/skills` — publish (multipart preferred).
- `DELETE /api/v1/skills/{slug}` and `DELETE /api/v1/packages/{name}` — delete a skill / package.
- `POST /api/v1/skills/{slug}/undelete` and `POST /api/v1/packages/{name}/undelete` — undelete.
- `POST /api/v1/skills/{slug}/rename` — rename a skill.
- `POST /api/v1/skills/{slug}/merge` — merge a skill.
- `POST /api/v1/skills/{slug}/transfer` and `POST /api/v1/packages/{name}/transfer` — initiate ownership transfer.
- `POST /api/v1/skills/{slug}/transfer/accept`, `.../transfer/reject`, `.../transfer/cancel` — respond to a transfer.
- `GET /api/v1/plugins/export?startDate=&endDate=&limit=&cursor=&family=` — export plugin install data.
- `GET /api/v1/transfers/incoming` and `GET /api/v1/transfers/outgoing` — list pending transfers.
- `GET /api/v1/whoami` — the authenticated account identity.

### Admin only

- `POST /api/v1/users/reserve` — reserves root slugs and private no-release package placeholders for an owner handle.

## Legacy

The legacy `/api/*` and `/api/cli/*` routes are still available; the page directs readers to `DEPRECATIONS.md` for details.

**Source**: OpenClaw documentation — `clawhub/api` (mirror `inbox/openclaw_docs/clawhub/api.md`)
**Last Updated**: 2026-06-22
**Status**: Active
