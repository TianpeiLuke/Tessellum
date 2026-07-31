---
tags:
  - resource
  - documentation
  - openclaw
  - clawhub
  - http_api
keywords:
  - clawhub public read endpoints
  - api/v1/search skills packages
  - skill detail moderation scan verify
  - package security trust blockedfromdownload
  - npm packument tarball passthrough
  - resolve download read endpoints
  - security-verdicts collection endpoint
topics:
  - OpenClaw
  - ClawHub HTTP API
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/clawhub/http-api
access_control_group: ["general"]
---

# OpenClaw — ClawHub HTTP API Public Read Endpoints

## Overview

This note models the **public (no-auth) read surface** of the ClawHub HTTP API — the catalog, version, scan, verification, security-verdict, moderation-visibility, artifact, npm-mirror, resolve, and download endpoints that third-party directories, the `clawhub` CLI, OpenClaw install clients, and self-hosters consume. It mirrors the "Public endpoints (no auth)" section of the `clawhub/http-api` source page, modeling each endpoint's request parameters, response shapes, and status codes. The base URL is `https://clawhub.ai` and all v1 paths live under `/api/v1/...`. The rate-limit/error conventions and the Bearer-token write/admin endpoints are documented in sibling notes (see Related Notes); a few routes here require an API token despite sitting in the public catalog (the report POSTs, scan submit/poll/download, plugin export, and the moderator/admin intake/queue routes), noted per endpoint.

## Search and Skill Catalog

`GET /api/v1/search` is the skill search endpoint. Params: `q` (required), `limit` (optional integer), `highlightedOnly` (`true` to filter to highlighted skills), `nonSuspiciousOnly` (`true` to hide `flagged.suspicious` skills), and `nonSuspicious` (legacy alias). Results are returned in relevance order (embedding similarity + exact slug/name token boosts + a small popularity prior), where relevance is stronger than popularity — a precise slug/display-name token match can outrank a looser, higher-engagement match (popularity is log-scaled and capped, and suspicious/hidden moderation state can remove a skill from public search depending on caller filters). The response is `{ "results": [ … ] }` where each result carries `score`, `slug`, `displayName`, `summary`, `version`, `updatedAt`, `ownerHandle`, and a nested `owner` (`handle`, `displayName`, `image`).

`GET /api/v1/skills` lists skills. Params: `limit` (1–200), `cursor` (for any non-`trending` sort), `sort` (`updated` default, `recommended` alias `default`, `createdAt` alias `newest`, `stars` alias `rating`, `installsCurrent` alias `installs`, `installsAllTime`, `trending`), plus `nonSuspiciousOnly`/`nonSuspicious`; invalid `sort` returns `400`. `trending` ranks by installs in the last 7 days (telemetry-based), `createdAt` is stable for new-skill crawls while `updated` changes on republish, and when `nonSuspiciousOnly=true` a cursor page may return fewer than `limit` items (filtered after retrieval), so `nextCursor` (not a short page) signals continuation. The response is `{ "items": [ … ], "nextCursor": null }` where each item carries `slug`, `displayName`, `summary`, `tags`, `stats`, `createdAt`, `updatedAt`, `latestVersion`, and `metadata`.

`GET /api/v1/skills/{slug}` returns skill detail; old slugs from owner rename/merge flows resolve to the canonical skill. The response nests `skill`, `latestVersion`, `metadata`, `owner`, and `moderation`. `metadata.os` = OS restrictions from skill frontmatter (e.g. `["macos"]`, `null` if undeclared); `metadata.systems` = Nix system targets (e.g. `["aarch64-darwin", "x86_64-linux"]`, `null` if undeclared); `metadata` itself is `null` with no platform metadata. The `moderation` block (`isSuspicious`, `isMalwareBlocked`, `verdict`, `reasonCodes`, `summary`, `engineVersion`, `updatedAt`) is included only when the skill is flagged or the owner is viewing it.

`GET /api/v1/skills/{slug}/moderation` returns the structured moderation state, adding `legacyReason` and an `evidence[]` array of `{ code, severity, file, line, message, evidence }`. Owners/moderators can access details for hidden skills; public callers only get `200` for already-flagged visible skills, with evidence redacted (raw snippets only for owners/moderators).


`GET /api/v1/skills/{slug}/versions` lists version history (`limit`, `cursor`); `GET /api/v1/skills/{slug}/versions/{version}` returns version metadata plus a files list, where `version.security` includes normalized scan verification status + scanner details (VirusTotal + LLM) when available. `GET /api/v1/skills/{slug}/file` returns raw text content (`path` required, `version`/`tag` optional, latest by default, 200KB limit).

## Skill Reports, Scan, and Verification

`POST /api/v1/skills/{slug}/report` reports a skill for moderator review (requires an API token); reports are skill-level, optionally version-linked, and feed the skill report queue. Request `{ "reason": "Suspicious install step", "version": "1.2.3" }`; response `{ "ok": true, "reported": true, "alreadyReported": false, "reportId": "skillReports:…", "skillId": "skills:…", "reportCount": 1 }`. `GET /api/v1/skills/-/reports` is the moderator/admin skill-report intake (`status` = `open` default/`confirmed`/`dismissed`/`all`, `limit` 1–200, `cursor`); `POST /api/v1/skills/-/reports/{reportId}/triage` resolves or reopens reports — `note` is required for `confirmed`/`dismissed` (optional when reopening to `open`), and `finalAction: "hide"` with a triaged report hides the skill in the same auditable workflow.

`POST /api/v1/skills/-/scan` is the authenticated submit endpoint for new ClawScan jobs. Local upload scans are unsupported (`multipart/form-data` or `{ "source": { "kind": "upload" } }` return `410`). Published scans use JSON `{ "source": { "kind": "published", "slug": "gifgrep", "version": "1.2.3" }, "update": false }`, require owner/publisher management (or moderator/admin) authority, write back only when `update: true` and the scan succeeds, and respond `202` with `{ "ok": true, "scanId": …, "jobId": …, "status": "queued", … "queue": { … } }`; jobs are async, manual requests prioritized ahead of backfill. `GET /api/v1/skills/-/scan/{scanId}` polls a scan (queued/running/succeeded/failed; `queue.queuedAhead`/`queue.position` while queued, bounded with `queuedAheadIsEstimate: true`; a `report` with `clawscan`/`skillspector`/`staticAnalysis`/`virustotal` sections when available; failed jobs return `status: "failed"` + `lastError`). `GET /api/v1/skills/-/scan/{scanId}/download` returns the report archive (requires a succeeded scan — non-terminal returns `409` — as a ZIP with `manifest.json`, `clawscan.json`, `skillspector.json`, `static-analysis.json`, `virustotal.json`, `README.md`). `GET /api/v1/skills/-/scan/download/{name}?version=<version>&kind=skill|plugin` returns the stored report archive for submitted versions (owner/publisher management or moderator/admin authority; exact-version results including blocked/hidden versions; `kind` defaults to `skill`, use `kind=plugin` for plugin scans). `POST /api/v1/skills/-/scan/batch` and `POST /api/v1/skills/-/scan/batch/status` (admin-only canonical batch rescan/status, same payloads/counters as legacy `POST /api/v1/skills/-/rescan-batch[/status]`, the latter taking `{ "jobIds": ["…"] }`) complete the scan routes.

`GET /api/v1/skills/{slug}/scan` returns scan verification details for a version (`version`/`tag`, latest if neither given; `security.hasScanResult` is `true` only when a scanner produced a definitive verdict — `clean`/`suspicious`/`malicious`; `moderation` is a current skill-level snapshot from the latest version, so for historical versions check `moderation.matchesRequestedVersion` and `moderation.sourceVersion`). `GET /api/v1/skills/{slug}/verify` returns the Skill Card verification envelope used by `clawhub skill verify` (`version`/`tag`); `ok` is `true` only when the selected version has a generated Skill Card, is not malware-blocked, and ClawScan verification is clean. Identity/version metadata are top-level fields (`slug`, `displayName`, `publisherHandle`, `version`, `resolvedFrom`, `tag`, `createdAt`); `security` is the top-level verdict (automation keys off `ok`/`decision`/`reasons`/`security.status`) with `security.signals` holding `staticScan`/`virusTotal`/`skillSpector` evidence (`dependencyRegistry` always `null`); `provenance` is `server-resolved-github-import` only when ClawHub resolved+stored a GitHub repo/ref/commit/path, else `unavailable`.

`POST /api/v1/skills/-/security-verdicts` returns compact security verdicts for exact skill versions, for clients that already know which installed versions to display (e.g. OpenClaw Control UI). Request `{ "items": [{ "slug": "gifgrep", "version": "1.2.3" }] }` — `items` must hold 1–100 unique `{ slug, version }` pairs, results are per item (one missing skill/version does not fail the whole response), and the response is security-only (no Skill Card data, file lists, or detailed scanner payloads). Schema `clawhub.skill.security-verdicts.v1` carries per-item `ok`, `decision`, `reasons`, identity fields, and a `security` block; failed items include `error` and a `null` `security`:

```json
{
  "schema": "clawhub.skill.security-verdicts.v1",
  "items": [
    { "ok": true, "decision": "pass", "reasons": [], "slug": "gifgrep", "version": "1.2.3",
      "security": { "status": "clean", "passed": true,
        "signals": { "staticScan": { "status": "clean", "reasonCodes": [] }, "virusTotal": null, "skillSpector": null, "dependencyRegistry": null } } },
    { "ok": false, "decision": "fail", "reasons": ["version.not_found"], "error": { "code": "version_not_found" }, "security": null }
  ]
}
```

## Package Catalog and Plugins

`GET /api/v1/packages` is the unified catalog for skills, code plugins, and bundle plugins. Params: `limit` (1–100), `cursor`, `family` (`skill`/`code-plugin`/`bundle-plugin`), `channel` (`official`/`community`/`private`), `isOfficial`, `sort` (`updated` default, `recommended`, `installs`), and `category` (only when scoped to plugin packages). Invalid `family`/`channel`/`isOfficial`/`featured`/`highlightedOnly`/`sort` return `400`; unknown params are ignored. `GET /api/v1/code-plugins`/`GET /api/v1/bundle-plugins` are fixed-family aliases; skills can only be published via `POST /api/v1/skills` while `POST /api/v1/packages` is only for code-plugin/bundle-plugin releases. Anonymous callers see only public channels; authenticated callers also see private packages for their publishers (`channel=private` returns only packages the caller can read). `GET /api/v1/packages/search` is the unified search across skills + plugin packages (`q` required, plus `limit`/`family`/`channel`/`isOfficial`/`category`, same `400`/visibility rules).

`GET /api/v1/plugins` browses code-plugin + bundle-plugin packages (params `limit` 1–100, `cursor`, `isOfficial`, `sort` = `recommended` default/`installs`/`updated`, `category`). Current `category` values: `channels`, `models`, `memory`, `context`, `voice`, `media`, `web`, `tools`, `runtime`, `gateway`, `security`, `other`. Legacy v1 read-endpoint aliases stay accepted (`mcp-tooling`/`data`/`automation` → `tools`; `observability`/`deployment` → `gateway`; `dev-tools` → `runtime`) but not as stored/author-declared values. `GET /api/v1/plugins/search` is the plugin-only search (`q` required, `limit`, `isOfficial`, `category`); category filtering is a real API filter backed by plugin category digest rows (not a query rewrite), and results return in relevance order without pagination. `GET /api/v1/plugins/export` bulk-exports latest public plugin releases for offline analysis — requires an API token; params `startDate`/`endDate` (required, Unix ms bounds on `updatedAt`), `limit` (1–250, default 250), `cursor`, `family` (`code-plugin`/`bundle-plugin`, omitted means both). Body is a ZIP (each plugin rooted at `{family}/{packageName}/`, latest-release files, per-plugin metadata at `__clawhub_export/{family}/{packageName}/plugin_meta.json`, always `_manifest.json` at root, `_errors.json` on partial failure) returning `X-Next-Cursor`, `X-Has-More`, `X-Total-Returned`, `X-Date-Range`, `X-Export-Errors` headers.

`GET /api/v1/packages/{name}` returns package detail metadata (skills can also resolve here; private packages return `404` unless the caller can read the owning publisher). `GET /api/v1/packages/{name}/versions` returns version history (`limit` 1–100, `cursor`). `GET /api/v1/packages/{name}/versions/{version}` returns one version including file metadata, compatibility, verification, artifact metadata, and scan data: `version.artifact.kind` is `legacy-zip` or `npm-pack` (ClawPack-backed, with `npmIntegrity`/`npmShasum`/`npmTarballName`); `version.sha256hash` is deprecated (hashes the ZIP bytes from `/download`) so modern clients use `version.artifact.sha256`; `version.vtAnalysis`/`version.llmAnalysis`/`version.staticScan` appear when scan data exists. `GET /api/v1/packages/{name}/file` returns raw text content (`path` required, `version`/`tag` optional, latest by default, read bucket not download bucket, binary files `415`, 200KB limit).

## Package Security, Artifact, Readiness, and Moderation Visibility

`GET /api/v1/packages/{name}/versions/{version}/security` is a **public** read endpoint (no token required) returning the exact package-release security/trust summary — the OpenClaw install-decision surface, called after resolving the target version. The `trust` block is the decision: `trust.blockedFromDownload` is the install block signal (block when `true` rather than re-deriving rules), `trust.scanStatus` is the effective status from scanner inputs + manual moderation, `trust.moderationState` is nullable (`null` with no manual moderation), `trust.reasons` is the stable audit list (`manual:quarantined`, `scan:malicious`, `package:malicious`), and `trust.pending`/`trust.stale` flag still-completing or outdated inputs:

```json
{
  "package": { "name": "@openclaw/example-plugin", "displayName": "Example Plugin", "family": "code-plugin" },
  "release": { "releaseId": "packageReleases:…", "version": "1.2.3", "artifactKind": "npm-pack",
    "artifactSha256": "0123…", "npmIntegrity": "sha512-…", "npmShasum": "0123…", "npmTarballName": "example-plugin-1.2.3.tgz", "createdAt": 1730000000000 },
  "trust": { "scanStatus": "malicious", "moderationState": "quarantined", "blockedFromDownload": true,
    "reasons": ["manual:quarantined", "scan:malicious"], "pending": false, "stale": false }
}
```

`GET /api/v1/packages/{name}/versions/{version}/artifact` returns explicit artifact resolver metadata (legacy versions return a `legacy-zip` artifact + legacy ZIP `downloadUrl`; ClawPack versions return an `npm-pack` artifact, npm integrity fields, a `tarballUrl`, and the legacy ZIP URL — the resolver surface that avoids guessing archive format from a shared URL). `GET /api/v1/packages/{name}/versions/{version}/artifact/download` downloads through that resolver path (ClawPack versions stream the exact uploaded npm-pack `.tgz` bytes; legacy ZIP versions redirect to `/api/v1/packages/{name}/download?version=`; download bucket). `GET /api/v1/packages/{name}/readiness` returns computed readiness for future OpenClaw consumption — checks cover official-channel status, latest-version availability, ClawPack npm-pack artifact, artifact digest, source-repo/commit provenance, OpenClaw compatibility metadata, host targets, and scan state — returning `{ "package": { …, "isOfficial", "latestVersion" }, "ready": false, "checks": [{ "id", "label", "status", "message" }], "blockers": [] }`.

`GET /api/v1/packages/migrations` lists official OpenClaw plugin migration rows (moderator/admin token; `phase` = `planned`/`published`/`clawpack-ready`/`legacy-zip-only`/`metadata-ready`/`blocked`/`ready-for-openclaw`/`all` default, `limit` 1–100, `cursor`). `GET /api/v1/packages/moderation/queue` is the moderator/admin package-release review queue (`status` = `open` default/`blocked`/`manual`/`all`; `open` = suspicious/malicious/pending/quarantined/revoked/reported, `blocked` = quarantined/revoked/malicious, `manual` = any manual override). `GET /api/v1/packages/reports` is the moderator/admin package-report intake (`status` = `open`/`confirmed`/`dismissed`/`all`, `limit` 1–100, `cursor`). `GET /api/v1/packages/{name}/moderation` is the owner/moderator visibility endpoint (token for the package owner, publisher member, moderator, or admin) returning a `package` summary and a `latestRelease` with `scanStatus`/`moderationState`/`moderationReason`/`blockedFromDownload`/`reasons`.

`POST /api/v1/packages/{name}/report` reports a package for moderator review (requires an API token); reports are package-level, optionally version-linked, feed the moderation queue, and do not auto-hide or block downloads. Request `{ "reason": "Suspicious native binary", "version": "1.2.3" }`; response mirrors the skill-report shape with `packageId`/`releaseId` in place of `reportId`/`skillId` (`ok`, `reported`, `alreadyReported`, `reportCount`).

## npm Passthrough, Resolve, and Download

`GET /api/npm/{package}` returns an npm-compatible packument for ClawPack-backed package versions (only versions with uploaded ClawPack npm-pack tarballs are listed, legacy ZIP-only versions omitted; `dist.tarball`/`dist.integrity`/`dist.shasum` use npm-compatible fields so users can point npm at the mirror; scoped packuments accept both `/api/npm/@scope/name` and npm's encoded `/api/npm/@scope%2Fname`). `GET /api/npm/{package}/-/{tarball}.tgz` streams the exact uploaded ClawPack tarball bytes for npm mirror clients (download bucket; headers include the ClawHub SHA-256 + npm integrity/shasum metadata; moderation and private-package access checks still apply).

`GET /api/v1/resolve` maps a local fingerprint to a known version for the CLI (`slug` required, `hash` required = 64-char hex sha256 of the bundle fingerprint), returning `{ "slug": "gifgrep", "match": { "version": "1.2.2" }, "latestVersion": { "version": "1.2.3" } }`. `GET /api/v1/download` downloads a zip of a skill version (`slug` required, `version` optional semver, `tag` optional e.g. `latest`, latest if neither given; soft-deleted versions return `410`; download stats counted as unique identities per hour — `userId` with a valid token, otherwise IP). `GET /api/v1/packages/{name}/download` downloads the legacy deterministic ZIP archive for a package release (`version`/`tag` optional, defaults to latest; skills redirect to `GET /api/v1/download`; archives have a `package/` root for old clients; ZIP-only, does not stream ClawPack `.tgz`; responses include `ETag`, `Digest`, `X-ClawHub-Artifact-Type`, `X-ClawHub-Artifact-Sha256` headers; malicious releases return `403`; private packages return `404` unless the caller is the owner).

**Source**: OpenClaw documentation — `clawhub/http-api` (mirror `inbox/openclaw_docs/clawhub/http-api.md`), Public endpoints section
**Last Updated**: 2026-06-22
**Status**: Active
