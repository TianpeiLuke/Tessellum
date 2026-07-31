---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - clawhub
keywords:
  - openclaw community plugins
  - clawhub plugin discovery
  - openclaw plugins search
  - openclaw plugins install
  - clawhub package publish
  - community plugin publish workflow
  - clawhub source prefix
  - plugin publish checklist
topics:
  - OpenClaw
  - Community Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/community
access_control_group: ["general"]
---

# OpenClaw — Finding and Publishing Community Plugins

## Overview

This procedure covers how to **discover and publish community-maintained OpenClaw plugins** through ClawHub, mirroring the `plugins/community` source page. Community plugins are third-party packages that extend OpenClaw with channels, tools, providers, hooks, or other capabilities, and **ClawHub is the primary discovery surface for public community plugins**. The page documents two task flows: finding (and installing) a plugin from the CLI using explicit source prefixes, and the publish workflow for sharing your own plugin — including the pre-publish checklist and what ClawHub validates before creating a release. The docs intentionally do **not** maintain a static third-party plugin catalog; ClawHub owns the live package listing, release history, scan status, and install hints.

## Find plugins

Search ClawHub from the CLI:

```bash
openclaw plugins search "calendar"
```

Install a ClawHub plugin with an **explicit source prefix**:

```bash
openclaw plugins install clawhub:<package-name>
```

**npm** remains a supported direct-install path during the launch cutover:

```bash
openclaw plugins install npm:<package-name>
```

For common install, update, inspect, and uninstall examples, the source page points to the **Manage plugins** page (`/plugins/manage-plugins`). For the full command reference and source-selection rules, it points to the **`openclaw plugins`** CLI reference (`/cli/plugins`).

## Publish plugins

Publish public community plugins on ClawHub when you want OpenClaw users to discover and install them. **ClawHub owns the live package listing, release history, scan status, and install hints; the docs do not maintain a static third-party plugin catalog.** Publishing uses the `clawhub package publish` command, run first as a dry run and then for real:

```bash
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
```

Before publishing, make sure the plugin has **package metadata, a plugin manifest, setup docs, and a clear maintenance owner.** ClawHub **validates owner scope, package name, version, file limits, and source metadata** before it creates a release, then keeps new releases **hidden from normal install and download surfaces until review and verification finish.**

### Pre-publish checklist

The source page provides this checklist to satisfy before you publish:

| Requirement          | Why                                                 |
| -------------------- | --------------------------------------------------- |
| Published on ClawHub | Users need `openclaw plugins install` hints to work |
| Public GitHub repo   | Source review, issue tracking, transparency         |
| Setup and usage docs | Users need to know how to configure it              |
| Active maintenance   | Recent updates or responsive issue handling         |

### Full publishing contract

The source page directs you to three pages for the full publishing contract: **ClawHub publishing** (`/clawhub/publishing`) explains owners, scopes, releases, review, package validation, and package transfer; **Building plugins** (`/plugins/building-plugins`) shows the plugin package shape and first publish workflow; and **Plugin manifest** (`/plugins/manifest`) defines native plugin manifest fields.

## Related Notes

**Terms**

- **[Plugin Manifest](../../term_dictionary/term_plugin_manifest.md)** — plugin manifest; relevance: publishing requires package metadata + a plugin manifest.
- **[Plugin SDK](../../term_dictionary/term_plugin_sdk.md)** — plugin framework; relevance: community plugins are built on the plugin SDK / building-plugins workflow.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway; relevance: subject — community plugins extend OpenClaw with channels/tools/providers/hooks.
- **[Downstream Ecosystem](../../term_dictionary/term_downstream_ecosystem.md)** — downstream ecosystem; relevance: the OpenClaw plugin ecosystem this discovery surface feeds.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — coding-agent runtime; relevance: plugins extend the coding-agent gateway's capability set.
- **[Provider Plugin](../../term_dictionary/term_provider_plugin.md)** — provider/plugin abstraction; relevance: community plugins can add providers/channels/tools.
- **[Skill Manifest](../../term_dictionary/term_skill_manifest.md)** — package/skill manifest; relevance: ClawHub validates owner scope, package name, version, file limits, source metadata.
- **[Deprecation](../../term_dictionary/term_deprecation.md)** — lifecycle policy; relevance: ClawHub release review/verification gating before public install.

**Docs**

- **[cc_sdk_plugins](../claude_code/cc_sdk_plugins.md)** — SDK plugins; relevance: analog for the plugin packaging/build workflow.
- **[cc_plugin_components](../claude_code/cc_plugin_components.md)** — plugin components; relevance: analog for the package shape (manifest, metadata, docs).
- **[cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md)** — marketplace install; relevance: analog for ClawHub `install`/`search` discovery surface.
- **[cc_plugin_sources](../claude_code/cc_plugin_sources.md)** — plugin source selection; relevance: analog for `clawhub:`/`npm:` install source prefixes.
- **[hermes_creating_skill_publish](../hermes_agent/hermes_creating_skill_publish.md)** — publishing skills/packages; relevance: sibling publish-workflow contract (owner, review, release).
- **[hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md)** — build plugin tutorial; relevance: analog for the build-before-publish plugin workflow.
- **[oc_plugins_compatibility](oc_plugins_compatibility.md)** — the compatibility/inspector gate published plugins must pass.
- **[oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md)** — native-plugin install counterpart.
- **[oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md)** — bundled-plugin enablement context for community plugins.
- **[oc_plugins_compatibility_areas](oc_plugins_compatibility_areas.md)** — concrete compatibility shims published plugins must honor.

**Repos**

- **[repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md)** — plugin/extension framework; relevance: the SDK/package shape community plugins build against.

**Snippets**

- **[snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md)** — package contract; relevance: the package metadata/manifest a publish requires.
- **[snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md)** — plugin lifecycle; relevance: install/enable/uninstall after discovery.
- **[snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md)** — plugin SDK entries; relevance: the SDK entrypoints a community plugin implements.
- **[snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md)** — command catalog; relevance: `openclaw plugins search/install` CLI commands.
- **[snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md)** — CLI routing; relevance: routing of `plugins`/source-prefixed install subcommands.
- **[snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md)** — plugin runtime load; relevance: loading an installed community plugin into the gateway.
- **[snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md)** — skill/package scanner; relevance: ClawHub scan status / review-before-publish gating.
- **[snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md)** — plugin trust; relevance: source/owner trust validation for installed plugins.
- **[snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md)** — setup imports; relevance: importing/registering an installed plugin during setup.
- **[snippet_ecosystem_llm_provider](../../code_snippets/snippet_ecosystem_llm_provider.md)** — provider plugin; relevance: example of a provider-class plugin in the ecosystem.

## References

- [OpenClaw Docs — Community plugins](https://docs.openclaw.ai/plugins/community)
- [OpenClaw Docs — ClawHub](https://docs.openclaw.ai/clawhub)
- [OpenClaw Docs — Manage plugins](https://docs.openclaw.ai/plugins/manage-plugins)
- [OpenClaw Docs — openclaw plugins CLI](https://docs.openclaw.ai/cli/plugins)
- [OpenClaw Docs — ClawHub publishing](https://docs.openclaw.ai/clawhub/publishing)
- [OpenClaw Docs — Building plugins](https://docs.openclaw.ai/plugins/building-plugins)
- [OpenClaw Docs — Plugin manifest](https://docs.openclaw.ai/plugins/manifest)

**Source**: OpenClaw documentation — `plugins/community` (mirror `inbox/openclaw_docs/plugins/community.md`)
**Last Updated**: 2026-06-22
**Status**: Active
