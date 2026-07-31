---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - logging
keywords:
  - openclaw macos logging
  - rolling diagnostics jsonl
  - diagnostics.jsonl debug pane
  - unified logging private data
  - ai.openclaw subsystem plist
  - enable-private-data
  - swift-log unified logging
  - clawlog.sh log capture
  - private payload phone numbers message bodies
topics:
  - OpenClaw
  - macOS Logging
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/mac/logging
access_control_group: ["general"]
---

# OpenClaw — macOS App Logging (Rolling Diagnostics + Unified-Logging Private Data)

## Overview

This procedure note covers how to capture logs from the OpenClaw **macOS app**, mirroring the `platforms/mac/logging` source page. The app routes its logs through swift-log (Apple unified logging by default) and offers two capture surfaces: an off-by-default **rolling JSONL diagnostics file** (toggled from the Debug pane) for a durable on-disk capture, and a **unified-logging private-data override** (an `ai.openclaw` subsystem plist) that unredacts payloads which are normally masked. It walks the enable/clear steps for the diagnostics file, the root-installed plist that opts the `ai.openclaw` subsystem into `Enable-Private-Data`, and the disable/cleanup steps — including the core sensitivity warning that the private surface can include phone numbers and message bodies, so these toggles stay on only while actively debugging (e.g. voice wake / session lifecycle issues).

## Rolling diagnostics file log (Debug pane)

OpenClaw routes macOS app logs through **swift-log** (unified logging by default) and can write a local, rotating file log to disk when you need a durable capture. Drive it from the Debug pane:

- **Verbosity**: Debug pane → Logs → App logging → **Verbosity**.
- **Enable**: Debug pane → Logs → App logging → **"Write rolling diagnostics log (JSONL)"**.
- **Location**: `~/Library/Logs/OpenClaw/diagnostics.jsonl` (rotates automatically; old files are suffixed with `.1`, `.2`, …).
- **Clear**: Debug pane → Logs → App logging → **"Clear"**.

Two notes from the source govern its use: the rolling diagnostics log is **off by default** — enable it only while actively debugging — and the resulting file should be treated as **sensitive**, so do not share it without review.

## Unified logging private data on macOS

Apple **unified logging redacts most payloads** unless a subsystem opts into `privacy -off`. Per the referenced macOS logging-privacy write-up, this opt-in is controlled by a plist in `/Library/Preferences/Logging/Subsystems/`, keyed by the subsystem name. Because the override only takes effect for **new log entries**, you must enable it *before* reproducing the issue you want captured — entries written before the flag was set stay redacted.

## Enable for OpenClaw (`ai.openclaw`)

To unredact the OpenClaw subsystem's private payloads, write the subsystem plist to a temp file first, then install it atomically as root into the unified-logging Subsystems directory:

```bash
cat <<'EOF' >/tmp/ai.openclaw.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DEFAULT-OPTIONS</key>
    <dict>
        <key>Enable-Private-Data</key>
        <true/>
    </dict>
</dict>
</plist>
EOF
sudo install -m 644 -o root -g wheel /tmp/ai.openclaw.plist /Library/Preferences/Logging/Subsystems/ai.openclaw.plist
```

The plist keys the `DEFAULT-OPTIONS` dict's `Enable-Private-Data` to `true`, and `install` places it as `ai.openclaw.plist` (mode `644`, owner `root:wheel`). Per source: **no reboot is required** — `logd` notices the file quickly — but only new log lines will include private payloads. View the richer output with the existing helper, for example: `./scripts/clawlog.sh --category WebChat --last 5m`.

## Disable after debugging

When the debugging session is finished, undo the override:

- **Remove the override**: `sudo rm /Library/Preferences/Logging/Subsystems/ai.openclaw.plist`.
- Optionally run `sudo log config --reload` to force `logd` to drop the override immediately.
- Remember this surface can include **phone numbers and message bodies**; keep the plist in place only while you actively need the extra detail.

**Source**: OpenClaw documentation — `platforms/mac/logging` (mirror `inbox/openclaw_docs/platforms/mac/logging.md`)
**Last Updated**: 2026-06-22
**Status**: Active
