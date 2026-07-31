---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - http_api
keywords:
  - clawhub auth endpoints
  - bearer clh_ token
  - post api v1 skills
  - post api v1 packages
  - clawpack tarball publish
  - soft delete undelete skill
  - users publisher recovery
  - transfer ownership skills
  - ban unban reclassify role
  - official channel eligibility
topics:
  - OpenClaw
  - ClawHub HTTP API
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/clawhub/http-api
access_control_group: ["general"]
---

# OpenClaw — ClawHub HTTP API Authenticated (Bearer) Write/Admin Endpoints

## Overview

This note is the procedure for the **authenticated (Bearer-token) write and admin surface** of the ClawHub HTTP API, mirroring the `## Auth endpoints (Bearer token)` section of the `clawhub/http-api` source page. Every endpoint here requires the header `Authorization: Bearer clh_...`. It covers token validation (`whoami`), publishing skills and code/bundle-plugin packages, soft-delete / undelete, org-publisher creation and recovery, name reservation, owner-slug management (rename/merge), ownership transfer, ban / unban / reclassify-ban / role moderation actions, the admin user list, and stars. The unauthenticated public read surface (search, catalog, scan, download) and the shared rate-limit / error conventions live in the sibling notes `oc_clawhub_http_api_public_endpoints` and `oc_clawhub_http_api_conventions`; only the auth section is documented here.

## Authentication header (required on every endpoint)

All endpoints in this section require the Bearer header exactly:

```
Authorization: Bearer clh_...
```

Per the source conventions, authenticated write endpoints should return actionable text rather than a bare `Unauthorized` when the server knows the reason — missing tokens, invalid/revoked tokens, and deleted/banned/disabled accounts each get distinct, human-readable messaging so CLI clients can tell users what blocked them. A valid Bearer token also moves rate-limit enforcement from per-IP to the per-user bucket.

## `GET /api/v1/whoami`

Validates the token and returns the user handle. This is the canonical pre-flight check for a CLI client to confirm a `clh_` token is live and to surface the actor's identity before any write.

## Publishing endpoints

### `POST /api/v1/skills` — publish a new skill version

Publishes a new version of a skill. The preferred request is `multipart/form-data` with a `payload` JSON part plus repeated `files[]` blobs; a JSON body with `files` (storageId-based) is also accepted. Two optional payload fields control ownership:

- `ownerHandle`: when present, the API resolves that publisher server-side and requires the actor to have publisher access.
- `migrateOwner`: when `true` together with `ownerHandle`, an existing skill may move to that owner — but only if the actor is an admin/owner on BOTH the current and target publishers. Without this explicit opt-in, owner changes are rejected.

### `POST /api/v1/packages` — publish a code-plugin or bundle-plugin release

Publishes a `code-plugin` or `bundle-plugin` release. It requires Bearer auth and `multipart/form-data`. The allowed form fields are `payload`, repeated `files` blobs, OR one `clawpack` tarball reference (`clawpack` may be a `.tgz` blob or a storage id returned by the upload-url flow). Use either `files` or `clawpack`, never both in the same request. Staged storage-id publishes must also include the `clawpackUploadTicket` returned with that upload URL. JSON bodies and caller-supplied `payload.files` / `payload.artifact` metadata are rejected. Direct multipart publish requests are capped at 18MB; ClawPack tarballs may use the upload-url flow up to the 120MB tarball cap. An optional `ownerHandle` payload field is honored, but only admins may publish on behalf of that owner.

```json
{
  "family": "code-plugin",
  "ownerHandle": "openclaw"
}
```

Validation highlights enforced at publish:

- `family` must be `code-plugin` or `bundle-plugin`.
- Plugin packages require `openclaw.plugin.json`; ClawPack `.tgz` uploads must contain it at `package/openclaw.plugin.json`.
- Code plugins additionally require `package.json`, source repo metadata, source commit metadata, config schema metadata, `openclaw.compat.pluginApi`, and `openclaw.build.openclawVersion`.
- `openclaw.hostTargets` and `openclaw.environment` are optional metadata.
- Only the `openclaw` org publisher and current `openclaw` org members' personal publishers may publish to the `official` channel; on-behalf publishes still validate official-channel eligibility against the target owner account.

Skill entries are published only through `POST /api/v1/skills`; `POST /api/v1/packages` is only for code-plugin and bundle-plugin releases.

## Delete and undelete

### `DELETE /api/v1/skills/{slug}` / `POST /api/v1/skills/{slug}/undelete`

Soft-delete or restore a skill — permitted to the owner, a moderator, or an admin. An optional JSON body carries a moderation reason:

```json
{ "reason": "Held for moderation pending legal review." }
```

When present, `reason` is stored as the skill moderation note and copied into the audit log. Owner-initiated soft deletes reserve the slug for 30 days, after which the slug can be claimed by another publisher; the delete response includes `slugReservedUntil` when this expiry applies. Moderator/admin hides and security removals do NOT expire this way. The delete response is:

```json
{ "ok": true, "slugReservedUntil": 1730000000000 }
```

Status codes: `200` ok, `401` unauthorized, `403` forbidden, `404` skill/user not found, `500` internal server error.

## Publisher and account provisioning

### `POST /api/v1/users/publisher` (admin-only)

Ensures an org publisher exists for a handle. If the handle still points at a legacy shared user/personal publisher, the endpoint first migrates it into an org publisher. For a newly-created org, provide `memberHandle` — the acting admin is NOT added as a member — and `memberRole` defaults to `owner`. Body: `{ "handle": "openclaw", "displayName": "OpenClaw", "memberHandle": "alice", "memberRole": "owner", "trusted": true }`. Response: `{ "ok": true, "publisherId": "...", "handle": "openclaw", "created": true, "migrated": false, "trusted": true, "member": { "userId": "...", "handle": "alice", "role": "owner" } }`.

### `POST /api/v1/publishers` (authenticated self-serve)

Self-serve org publisher creation: creates a new org publisher and adds the caller as owner. It does NOT migrate existing user/personal handles and does NOT mark the publisher trusted/official. Body: `{ "handle": "opik", "displayName": "Opik" }`. Response: `{ "ok": true, "publisherId": "...", "handle": "opik", "created": true, "trusted": false }`. Returns `409` when the handle is already used by a publisher, user, or personal publisher.

### `POST /api/v1/users/reserve` (admin-only)

Reserves root slugs and package names for a rightful owner without publishing a release. Reserved package names become private placeholder packages with no release rows, so the same owner can later publish the real code-plugin or bundle-plugin release into that name. Body: `{ "handle": "openclaw", "slugs": ["diffs"], "packageNames": ["@openclaw/diffs"], "reason": "reserved for official OpenClaw plugin" }`. Response: `{ "ok": true, "succeeded": 2, "failed": 0, "results": [{ "kind": "slug", "name": "diffs", "ok": true, "action": "reserved" }] }`.

### `POST /api/v1/users/publisher-recovery` (admin-only)

Recovers a personal publisher for a verified replacement GitHub OAuth principal without editing Convex Auth account rows. The request must name BOTH immutable GitHub provider account ids; mutable handles are only an operator-facing guard. The endpoint defaults to dry-run — applying recovery requires `dryRun: false` AND `confirmIdentityVerified: true` after staff independently verify continuity between both GitHub principals. Recovery fails closed when the destination user's current personal publisher already has skills, packages, or GitHub skill sources. Recovery also migrates legacy `ownerUserId` fields for the recovered publisher's skills, skill slug aliases, packages, package inspector warnings, and derived search digest rows so direct-owner paths agree with the new publisher authority; an active protected-handle reservation for the recovered handle is reassigned to the replacement user so later profile synchronization cannot restore the former user's competing authority. Each primary table is bounded to 100 rows per apply transaction, and larger recoveries must first use a resumable owner migration. GitHub skill sources are publisher-scoped and reported as checked rather than rewritten. Body: `{ "handle": "gingiris", "nextUserHandle": "gingiris-1031", "previousGitHubProviderAccountId": "123", "nextGitHubProviderAccountId": "456", "reason": "Verified account continuity for issue #2555", "confirmIdentityVerified": true, "dryRun": false }`.

## Owner slug management and ownership transfer

### Owner slug management endpoints

Both endpoints require API token auth and only work for the skill owner:

- `POST /api/v1/skills/{slug}/rename` — Body `{ "newSlug": "new-canonical-slug" }`; Response `{ "ok": true, "slug": "new-canonical-slug", "previousSlug": "old-slug" }`. `rename` preserves the previous slug as a redirect alias.
- `POST /api/v1/skills/{slug}/merge` — Body `{ "targetSlug": "canonical-target-slug" }`; Response `{ "ok": true, "sourceSlug": "old-slug", "targetSlug": "canonical-target-slug" }`. `merge` hides the source listing and redirects the source slug to the target listing.

### Transfer ownership endpoints

- `POST /api/v1/skills/{slug}/transfer` — Body `{ "toUserHandle": "target_handle", "message": "optional" }`; Response `{ "ok": true, "transferId": "skillOwnershipTransfers:...", "toUserHandle": "target_handle", "expiresAt": 1730000000000 }`.
- `POST /api/v1/skills/{slug}/transfer/accept`, `POST /api/v1/skills/{slug}/transfer/reject`, `POST /api/v1/skills/{slug}/transfer/cancel` — Response (accept/reject/cancel): `{ "ok": true, "skillSlug": "demo-skill?" }`.
- `GET /api/v1/transfers/incoming`, `GET /api/v1/transfers/outgoing` — Response shape: `{ "transfers": [{ "_id": "...", "skill": { "slug": "demo", "displayName": "Demo" }, "fromUser"|"toUser": { "handle": "..." }, "message": "...", "requestedAt": 0, "expiresAt": 0 }] }`.

## Moderation and account-standing actions

### `POST /api/v1/users/ban` (moderator/admin only)

Bans a user and hard-deletes owned skills. The body identifies the target by `handle` or `userId`, with an optional `reason` — `{ "handle": "user_handle", "reason": "optional ban reason" }` or `{ "userId": "users_...", "reason": "optional ban reason" }`. Response: `{ "ok": true, "alreadyBanned": false, "deletedSkills": 3 }`.

### `POST /api/v1/users/unban` (admin only)

Unbans a user and restores eligible skills. Body identifies by `handle` or `userId` with an optional `reason`. Response: `{ "ok": true, "alreadyUnbanned": false, "restoredSkills": 3 }`.

### `POST /api/v1/users/reclassify-ban` (admin only)

Changes the stored reason for an existing ban WITHOUT unbanning or restoring content. It defaults to dry-run unless `dryRun` is `false`. Body: `{ "handle": "user_handle", "reason": "bulk publishing spam", "dryRun": true }` (or by `userId` with `dryRun: false`). Response:

```json
{
  "ok": true,
  "dryRun": false,
  "userId": "users_...",
  "handle": "user_handle",
  "previousReason": "malware auto-ban",
  "nextReason": "bulk publishing spam",
  "changed": true
}
```

### `POST /api/v1/users/role` (admin only)

Changes a user role. Body identifies by `handle` or `userId` and names the new role — `{ "handle": "user_handle", "role": "moderator" }` or `{ "userId": "users_...", "role": "admin" }`. Response: `{ "ok": true, "role": "moderator" }`.

### `GET /api/v1/users` (admin only)

Lists or searches users. Query params: `q` (optional search query), `query` (optional alias for `q`), and `limit` (optional, default 20, max 200). Response: `{ "items": [{ "userId": "users_...", "handle": "user_handle", "displayName": "User", "name": "User", "role": "moderator" }], "total": 1 }`.

## Stars

### `POST /api/v1/stars/{slug}` / `DELETE /api/v1/stars/{slug}`

Add or remove a star (highlights). Both endpoints are idempotent. Responses: `{ "ok": true, "starred": true, "alreadyStarred": false }` (POST) and `{ "ok": true, "unstarred": true, "alreadyUnstarred": false }` (DELETE).

**Source**: OpenClaw documentation — `clawhub/http-api` (mirror `inbox/openclaw_docs/clawhub/http-api.md`), `## Auth endpoints (Bearer token)` section
**Last Updated**: 2026-06-22
**Status**: Active
