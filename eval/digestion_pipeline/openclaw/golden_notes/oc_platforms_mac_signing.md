---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - macos
keywords:
  - openclaw macos signing
  - package-mac-app.sh
  - codesign-mac-app.sh
  - stable debug bundle id
  - ad-hoc signing hardened runtime
  - sign_identity allow_adhoc_signing
  - team id audit
  - tcc grant persistence
  - openclaw build metadata about pane
topics:
  - OpenClaw
  - macOS Code Signing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/mac/signing
access_control_group: ["general"]
---

# OpenClaw — Signing macOS Debug Builds

## Overview

This note is the procedure for signing macOS **debug builds** of the OpenClaw.app produced by the packaging script, mirroring the `platforms/mac/signing` source page. It documents what `scripts/package-mac-app.sh` does (stable debug bundle id, Info.plist stamping, the `codesign-mac-app.sh` signing call), the `Usage` invocations for real-cert vs ad-hoc signing, the `Ad-hoc Signing Note` (Hardened Runtime handling for embedded frameworks like Sparkle), the build-metadata keys stamped for the About pane, and the `Why` rationale — a stable bundle id, signature, and fixed path are what keep macOS TCC permission grants persistent across rebuilds.

## What `package-mac-app.sh` Does

The app is usually built from `scripts/package-mac-app.sh`, which now performs the following:

- Sets a **stable debug bundle identifier**: `ai.openclaw.mac.debug`.
- Writes the Info.plist with that bundle id (override via `BUNDLE_ID=...`).
- Calls `scripts/codesign-mac-app.sh` to sign the main binary and the app bundle so macOS treats each rebuild as the same signed bundle and keeps TCC permissions (notifications, accessibility, screen recording, mic, speech). For stable permissions, use a real signing identity; ad-hoc is opt-in and fragile (see the `Why` section and macOS permissions).
- Uses `CODESIGN_TIMESTAMP=auto` by default, which enables trusted timestamps for Developer ID signatures. Set `CODESIGN_TIMESTAMP=off` to skip timestamping (offline debug builds).
- Injects build metadata into Info.plist: `OpenClawBuildTimestamp` (UTC) and `OpenClawGitCommit` (short hash) so the About pane can show build, git, and debug/release channel.
- **Packaging defaults to Node 24**: the script runs TS builds and the Control UI build. Node 22 LTS, currently `22.19+`, remains supported for compatibility.
- Reads `SIGN_IDENTITY` from the environment. Add `export SIGN_IDENTITY="Apple Development: Your Name (TEAMID)"` (or your Developer ID Application cert) to your shell rc to always sign with your cert. Ad-hoc signing requires explicit opt-in via `ALLOW_ADHOC_SIGNING=1` or `SIGN_IDENTITY="-"` (not recommended for permission testing).
- Runs a **Team ID audit** after signing and fails if any Mach-O inside the app bundle is signed by a different Team ID. Set `SKIP_TEAM_ID_CHECK=1` to bypass.

## Usage

Run the packager from the repo root. The first form auto-selects an identity and errors if none is found; the remaining forms select a specific identity or opt into ad-hoc signing:

```bash
# from repo root
scripts/package-mac-app.sh               # auto-selects identity; errors if none found
SIGN_IDENTITY="Developer ID Application: Your Name" scripts/package-mac-app.sh   # real cert
ALLOW_ADHOC_SIGNING=1 scripts/package-mac-app.sh    # ad-hoc (permissions will not stick)
SIGN_IDENTITY="-" scripts/package-mac-app.sh        # explicit ad-hoc (same caveat)
DISABLE_LIBRARY_VALIDATION=1 scripts/package-mac-app.sh   # dev-only Sparkle Team ID mismatch workaround
```

### Ad-hoc Signing Note

When signing with `SIGN_IDENTITY="-"` (ad-hoc), the script automatically disables the **Hardened Runtime** (`--options runtime`). This is necessary to prevent crashes when the app attempts to load embedded frameworks (like Sparkle) that do not share the same Team ID. Ad-hoc signatures also break TCC permission persistence; see macOS permissions for recovery steps.

## Build Metadata for About

`package-mac-app.sh` stamps the bundle with two keys:

- `OpenClawBuildTimestamp`: ISO8601 UTC at package time.
- `OpenClawGitCommit`: short git hash (or `unknown` if unavailable).

The About tab reads these keys to show version, build date, git commit, and whether it is a debug build (via `#if DEBUG`). Run the packager to refresh these values after code changes.

## Why

TCC permissions are tied to the bundle identifier *and* code signature. Unsigned debug builds with changing UUIDs were causing macOS to forget grants after each rebuild. Signing the binaries (ad-hoc by default) and keeping a fixed bundle id/path (`dist/OpenClaw.app`) preserves the grants between builds, matching the VibeTunnel approach.

**Source**: OpenClaw documentation — `platforms/mac/signing` (mirror `inbox/openclaw_docs/platforms/mac/signing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
