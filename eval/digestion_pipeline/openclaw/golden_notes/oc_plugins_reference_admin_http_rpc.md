---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - reference
keywords:
  - openclaw admin http rpc plugin
  - admin-http-rpc plugin
  - gatewaymethoddispatch contract
  - gateway method dispatch
  - admin http rpc endpoint
  - included in openclaw
  - plugin reference descriptor
  - openclaw gateway admin rpc
topics:
  - OpenClaw
  - Plugins Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/admin-http-rpc
access_control_group: ["general"]
---

# OpenClaw — Admin Http Rpc Plugin (Reference Descriptor)

## Overview

This note is the faithful reference descriptor for the **`@openclaw/admin-http-rpc`** plugin — OpenClaw's **admin HTTP RPC endpoint** — mirroring the auto-generated `plugins/reference/admin-http-rpc` catalog page. Like every page in OpenClaw's generated plugin reference, it is emitted from the plugin's `extensions/*/package.json` + `openclaw.plugin.json` metadata and carries exactly three facts: a one-line summary, a **Distribution** block (the npm package id + install route), and a **Surface** block (the contracts/providers/skills the plugin registers). This descriptor records that the plugin's one-line summary is "OpenClaw admin HTTP RPC endpoint", that it ships **included in OpenClaw** (package `@openclaw/admin-http-rpc`), and that its registered Surface is the single contract **`gatewayMethodDispatch`** — the gateway method-dispatch contract through which admin RPC methods are routed. The substantive behavior (how the dispatch contract works, how it is auth-gated, the transport it rides) lives in the linked gateway/RPC docs and `repo_openclaw_gateway`; this page is the catalog entry, not the implementation.

## Distribution

The catalog page records two Distribution facts verbatim:

- **Package**: `@openclaw/admin-http-rpc`
- **Install route**: included in OpenClaw

"Included in OpenClaw" means the plugin ships bundled with the OpenClaw distribution rather than being fetched separately from npm / ClawHub — no separate install step is documented on this page. The plugin lives in the OpenClaw `extensions/*` tree (`repo_openclaw_extensions`); the generator parses that package's `package.json` + `openclaw.plugin.json` to emit this Distribution block. *(No version, no configuration keys, and no install command are stated on this source page; "Not specified in source".)*

## Surface

The Surface block records the single contract this plugin registers:

```
contracts: gatewayMethodDispatch
```

The plugin exposes **`contracts: gatewayMethodDispatch`** — and only that. It registers no `providers:` and no `skills:` (those Surface keys are absent from the page). `gatewayMethodDispatch` is the gateway's method-dispatch contract: the surface through which gateway RPC methods are routed to their handlers, making this plugin an HTTP RPC entry point for admin/operator method calls against the OpenClaw gateway. The contract identifier `gatewayMethodDispatch` is an implementation-specific contract id documented inline here as the plugin's Surface — it is not a separate term note. The actual dispatch mechanics, the JSON-RPC envelope/error semantics, and the authentication that gates admin methods are defined in the gateway protocol/auth docs and implemented in `repo_openclaw_gateway`; this descriptor only names the contract the plugin contributes.

**Source**: OpenClaw documentation — `plugins/reference/admin-http-rpc` (mirror `inbox/openclaw_docs/plugins/reference/admin-http-rpc.md`)
**Last Updated**: 2026-06-22
**Status**: Active
