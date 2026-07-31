---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - permissions
keywords:
  - macos tcc permissions
  - openclaw permission persistence
  - accessibility grant node
  - tccutil reset accessibility
  - stable permission requirements
  - desktop documents downloads gating
  - openclaw workspace workaround
  - ad-hoc signing permission loss
topics:
  - OpenClaw
  - macOS Permissions
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/mac/permissions
access_control_group: ["general"]
---

# OpenClaw — Keeping macOS TCC Permission Grants Stable

## Overview

This note is the procedure for keeping macOS permission grants for the OpenClaw.app stable, recovering them when prompts disappear, and reasoning about which process identity should hold them — mirroring the `platforms/mac/permissions` source page. macOS permission grants are fragile because TCC (the macOS Transparency, Consent, and Control subsystem) associates a permission grant with the app's **code signature, bundle identifier, and on-disk path**; if any of those change, macOS treats the app as new and may drop or hide prompts. The page covers the four requirements for stable permissions, why you should not grant Accessibility to a generic `node` runtime, the `tccutil` recovery checklist when prompts disappear, and the Desktop/Documents/Downloads file-access gating with its workspace workaround.

## Requirements for stable permissions

TCC ties a grant to a triple of identity signals, so a grant survives a rebuild only if all three stay the same. Meet every requirement below for grants to persist:

- **Same path** — run the app from a fixed location (for OpenClaw, `dist/OpenClaw.app`).
- **Same bundle identifier** — changing the bundle ID creates a new permission identity.
- **Signed app** — unsigned or ad-hoc signed builds do not persist permissions.
- **Consistent signature** — use a real Apple Development or Developer ID certificate so the signature stays stable across rebuilds.

Ad-hoc signatures generate a new identity every build, so macOS will forget previous grants, and prompts can disappear entirely until the stale entries are cleared. (Signing is the prerequisite that makes grants stick — see the signing procedure linked under Related Notes.)

## Accessibility grants for Node and CLI runtimes

Prefer granting Accessibility to OpenClaw.app, Peekaboo.app, or another signed helper with its own bundle identifier instead of a generic `node` binary. macOS TCC grants Accessibility to the code identity of the process it sees, so if a Homebrew, nvm, pnpm, or npm workflow causes a shared `node` executable to receive Accessibility, any JavaScript package launched through that same executable may inherit GUI automation privileges.

Treat a `node` entry in System Settings as broad permission for that Node runtime, not as permission for one npm package. Avoid granting Accessibility to `node` unless you trust every script and package launched through that exact Node install. If you accidentally granted Accessibility to `node`, remove that entry from System Settings -> Privacy & Security -> Accessibility, then grant the signed app or helper that should own UI automation.

## Recovery checklist when prompts disappear

When permission prompts disappear, work through this checklist in order:

1. Quit the app.
2. Remove the app entry in System Settings -> Privacy & Security.
3. Relaunch the app from the same path and re-grant permissions.
4. If the prompt still does not appear, reset TCC entries with `tccutil` and try again.
5. Some permissions only reappear after a full macOS restart.

Example resets (replace the bundle ID as needed):

```bash
sudo tccutil reset Accessibility ai.openclaw.mac
sudo tccutil reset ScreenCapture ai.openclaw.mac
sudo tccutil reset AppleEvents
```

## Files and folders permissions (Desktop/Documents/Downloads)

macOS may also gate Desktop, Documents, and Downloads for terminal/background processes. If file reads or directory listings hang, grant access to the same process context that performs file operations (for example Terminal/iTerm, a LaunchAgent-launched app, or an SSH process) — each process context has its own TCC identity that macOS evaluates separately.

**Workaround:** move files into the OpenClaw workspace (`~/.openclaw/workspace`) if you want to avoid per-folder grants. If you are testing permissions, always sign with a real certificate; ad-hoc builds are only acceptable for quick local runs where permissions do not matter.

**Source**: OpenClaw documentation — `platforms/mac/permissions` (mirror `inbox/openclaw_docs/platforms/mac/permissions.md`)
**Last Updated**: 2026-06-22
**Status**: Active
