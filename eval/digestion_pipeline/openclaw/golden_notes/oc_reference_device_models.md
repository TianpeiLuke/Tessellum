---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - device_models
keywords:
  - openclaw device model database
  - apple device identifiers
  - apple-device-identifiers vendored json
  - instances ui device names
  - apps/macos devicemodels resources
  - pin upstream commits notice.md
  - swift build package-path apps/macos
  - update device model mapping procedure
topics:
  - OpenClaw
  - Device Models
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/device-models
access_control_group: ["general"]
---

# OpenClaw — Updating the Device Model Database

## Overview

This note is the maintenance **procedure** for OpenClaw's vendored device-model database — the JSON mapping that lets the macOS companion app render friendly Apple device names (e.g. `iPad16,6`, `Mac16,6` → human-readable names) in the **Instances** UI. It mirrors the entire `reference/device-models` source page: the location of the vendored JSON, the upstream MIT data source, and the three-part update routine (pick + record pinned commits → re-download the JSON with `curl` → re-verify the macOS Swift build). Use this when updating device-model identifier mappings or the accompanying NOTICE/license files, or when changing how the Instances UI displays device names.

## Where the mapping lives

The macOS companion app maps Apple model identifiers to human-readable names so the **Instances** UI can show friendly device names. The mapping is vendored as JSON under:

- `apps/macos/Sources/OpenClaw/Resources/DeviceModels/`

## Data source

The mapping is currently vendored from the MIT-licensed repository `kyle-seongwoo-jun/apple-device-identifiers`. To keep builds deterministic, the JSON files are pinned to specific upstream commits, which are recorded in `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`.

## Updating the database

Follow these steps to refresh the vendored mapping (source page section "Updating the database"):

1. Pick the upstream commits you want to pin to — one for iOS, one for macOS.
2. Update the commit hashes in `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`.
3. Re-download the JSON files, pinned to those commits:

```bash
IOS_COMMIT="<commit sha for ios-device-identifiers.json>"
MAC_COMMIT="<commit sha for mac-device-identifiers.json>"

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${IOS_COMMIT}/ios-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/ios-device-identifiers.json

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${MAC_COMMIT}/mac-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/mac-device-identifiers.json
```

4. Ensure `apps/macos/Sources/OpenClaw/Resources/DeviceModels/LICENSE.apple-device-identifiers.txt` still matches upstream — replace it if the upstream license changes.
5. Verify the macOS app builds cleanly (no warnings):

```bash
swift build --package-path apps/macos
```

**Source**: OpenClaw documentation — `reference/device-models` (mirror `inbox/openclaw_docs/reference/device-models.md`)
**Last Updated**: 2026-06-22
**Status**: Active
