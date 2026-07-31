---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw voice-call plugin
  - "@openclaw/voice-call"
  - twilio telnyx plivo phone calls
  - contracts tools surface
  - telephony tool plugin
  - npm clawhub install
  - voice call plugin descriptor
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/voice-call
access_control_group: ["general"]
---

# OpenClaw — voice-call Plugin (`@openclaw/voice-call`)

## Overview

This note is the plugin descriptor card for the OpenClaw **voice-call** plugin, mirroring the `plugins/reference/voice-call` reference page. It captures the plugin's three load-bearing identity facts: its npm package name (`@openclaw/voice-call`), its install route (npm; ClawHub), and the contract surface it registers (`contracts: tools`) for Twilio, Telnyx, and Plivo phone calls. As the source page states, this is the "OpenClaw voice-call plugin for Twilio, Telnyx, and Plivo phone calls." This card states only the package + surface; the deeper voice-call telephony behavior is documented by the dedicated voice-call plugin doc, which this card links rather than redefines.

## Distribution

- **Package:** `@openclaw/voice-call`
- **Install route:** npm; ClawHub

The voice-call plugin is distributed via npm and the ClawHub plugin marketplace (it is NOT bundled "included in OpenClaw" — it must be installed). This is the same npm + ClawHub install route used by other add-on plugin cards in this reference series.

## Surface

The plugin registers the contract surface:

```
contracts: tools
```

Registering under the `tools` contract means the voice-call plugin exposes its telephony capability (placing/receiving Twilio, Telnyx, and Plivo phone calls) as agent **tools** — invoked through the agent's function-calling / tool-execution path rather than as a standalone channel or model provider. The carrier names enumerated by the source are Twilio, Telnyx, and Plivo.

**Source**: OpenClaw documentation — `plugins/reference/voice-call` (mirror `inbox/openclaw_docs/plugins/reference/voice-call.md`)
**Last Updated**: 2026-06-22
**Status**: Active
