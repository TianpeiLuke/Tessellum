---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex
keywords:
  - openclaw native codex plugins
  - codexPlugins config
  - openclaw migrate codex
  - codex plugins chat command
  - openai-curated plugin migration
  - thread app config destructive_enabled
  - allow_destructive_actions policy
  - app inventory ownership mapping
topics:
  - OpenClaw
  - Codex Native Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/codex-native-plugins
access_control_group: ["general"]
---

# OpenClaw — Configuring Native Codex Plugins from Chat

## Overview

This note is the procedure for enabling and managing **native Codex plugins** on a Codex-mode OpenClaw agent — letting that agent use Codex app-server's own app and plugin capabilities inside the same Codex thread that handles the OpenClaw turn. It mirrors the `plugins/codex-native-plugins` source page and covers requirements, the `openclaw migrate codex` quickstart, `/codex plugins` chat management, how native setup works (the installed/enabled/accessible state machine), the V1 support boundary, app inventory and ownership mapping, the restrictive thread app config, the destructive-action policy, and troubleshooting. It assumes the base [Codex harness](oc_plugins_codex_harness_setup.md) is already working; native plugins build on that harness, they do not replace it.

OpenClaw does **not** translate Codex plugins into synthetic `codex_plugin_*` OpenClaw dynamic tools. Plugin calls stay in the native Codex transcript, and Codex app-server owns the app-backed MCP execution.

## Requirements

Before native Codex plugins work, all of the following must hold:

- The selected OpenClaw agent runtime must be the native Codex harness.
- `plugins.entries.codex.enabled` must be true.
- `plugins.entries.codex.config.codexPlugins.enabled` must be true.
- V1 supports only `openai-curated` plugins that migration observed as source-installed in the source Codex home.
- The target Codex app-server must be able to see the expected marketplace, plugin, and app inventory.

`codexPlugins` has **no effect** on OpenClaw runs, normal OpenAI provider runs, ACP conversation bindings, or other harnesses, because those paths do not create Codex app-server threads with native `apps` config. OpenAI-side Codex access, app availability, and workspace app/plugin controls all come from the signed-in Codex account (the OpenAI account and admin model are documented externally under "Using Codex with your ChatGPT plan").

## Quickstart

Migration is the durable install/eligibility step. Preview the migration from the source Codex home before applying anything:

```bash
openclaw migrate codex --dry-run
```

Use strict source app verification when you want migration to check source app accessibility before planning native plugin activation:

```bash
openclaw migrate codex --dry-run --verify-plugin-apps
```

Apply the migration when the plan looks right:

```bash
openclaw migrate apply codex --yes
```

Migration writes explicit `codexPlugins` entries for eligible plugins and calls Codex app-server `plugin/install` for selected plugins. A typical migrated config looks like this:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          codexPlugins: {
            enabled: true,
            allow_destructive_actions: true,
            plugins: {
              "google-calendar": {
                enabled: true,
                marketplaceName: "openai-curated",
                pluginName: "google-calendar",
              },
            },
          },
        },
      },
    },
  },
}
```

After changing `codexPlugins`, new Codex conversations pick up the updated app set automatically. Use `/new` or `/reset` to refresh the current conversation. A gateway restart is **not** required for plugin enable or disable changes.

## Manage plugins from chat

Use `/codex plugins` when you want to inspect or change configured native Codex plugins from the same chat where you operate the Codex harness:

```text
/codex plugins
/codex plugins list
/codex plugins disable google-calendar
/codex plugins enable google-calendar
```

`/codex plugins` is an alias for `/codex plugins list`. The list output shows the configured plugin keys, on/off state, Codex plugin name, and marketplace from `plugins.entries.codex.config.codexPlugins.plugins`.

`enable` and `disable` write only to OpenClaw config at `~/.openclaw/openclaw.json`; they do **not** edit `~/.codex/config.toml` or install new Codex plugins. Only the owner or a gateway client with the `operator.admin` scope can change plugin state. Enabling a configured plugin also turns on the global `codexPlugins.enabled` switch. If the plugin was written disabled because migration returned `auth_required`, reauthorize the app in Codex before enabling it in OpenClaw.

## How native plugin setup works

The integration has three separate states:

- **Installed** — Codex has the local plugin bundle in the target app-server runtime.
- **Enabled** — OpenClaw config is willing to make the plugin available to Codex harness turns.
- **Accessible** — Codex app-server confirms the plugin's app entries are available for the active account and can be mapped to the migrated plugin identity.

Migration is the durable install/eligibility step. During planning, OpenClaw reads source Codex `plugin/read` details and checks that the source Codex app-server account response is a ChatGPT subscription account. Non-ChatGPT or missing account responses skip app-backed plugins with `codex_subscription_required`. By default, migration does **not** call source `app/list`; app-backed source plugins that pass the account gate are planned without source app accessibility verification, and account lookup transport failures skip with `codex_account_unavailable`. With `--verify-plugin-apps`, migration takes a fresh source `app/list` snapshot and requires every owned app to be present, enabled, and accessible before planning native activation; in that mode, account lookup transport failures fall through to the source app-inventory gate. Runtime app inventory is the target-session accessibility check after migration, and Codex harness session setup then computes a restrictive thread app config for the enabled and accessible plugin apps.

Thread app config is computed when OpenClaw establishes a Codex harness session or replaces a stale Codex thread binding. It is **not** recomputed on every turn, so `/codex plugins enable` and `/codex plugins disable` affect new Codex conversations. Use `/new` or `/reset` when the current conversation should pick up the updated app set.

## V1 support boundary

V1 is intentionally narrow:

- Only `openai-curated` plugins that were already installed in the source Codex app-server inventory are migration-eligible.
- App-backed source plugins must pass the migration-time subscription gate. `--verify-plugin-apps` adds the source app-inventory gate. Subscription-gated accounts plus, in verification mode, inaccessible, disabled, or missing source apps or source app-inventory refresh failures are reported as skipped manual items instead of enabled config entries. Unreadable plugin details are skipped before the source app-inventory gate.
- Migration writes explicit plugin identities with `marketplaceName` and `pluginName`; it does **not** write local `marketplacePath` cache paths.
- `codexPlugins.enabled` is the global enablement switch.
- There is no `plugins["*"]` wildcard and no config key that grants arbitrary install authority.
- Unsupported marketplaces, cached plugin bundles, hooks, and Codex config files are preserved in the migration report for manual review.

## App inventory and ownership

OpenClaw reads Codex app inventory through app-server `app/list`, caches it for **one hour**, and refreshes stale or missing entries asynchronously. The cache is in memory only; restarting the CLI or gateway drops it, and OpenClaw rebuilds it from the next `app/list` read.

Migration and runtime use separate cache keys. Source migration verification uses the source Codex home and source app-server start options — it runs only when `--verify-plugin-apps` is set, and it forces a fresh source `app/list` traversal for that planning run. Target runtime setup uses the target agent's Codex app-server identity when it builds the Codex thread app config; plugin activation invalidates that target cache key and then force-refreshes it after `plugin/install`.

A plugin app is exposed only when OpenClaw can map it back to the migrated plugin through stable ownership — one of: exact app id from plugin detail; known MCP server name; or unique stable metadata. Display-name-only or ambiguous ownership is excluded until the next inventory refresh proves ownership.

## Thread app config

OpenClaw injects a restrictive `config.apps` patch for the Codex thread: `_default` is disabled and only apps owned by enabled migrated plugins are enabled. OpenClaw sets app-level `destructive_enabled` from the effective global or per-plugin `allow_destructive_actions` policy and lets Codex enforce destructive tool metadata from its native app tool annotations. `true` and `"auto"` both set `destructive_enabled: true`; `false` sets it false. The `_default` app config is disabled with `open_world_enabled: false`. Enabled plugin apps are emitted with `open_world_enabled: true`; OpenClaw does not expose a separate plugin open-world policy knob and does not maintain per-plugin destructive tool-name deny lists.

Tool approval mode is automatic by default for plugin apps so non-destructive read tools can run without a same-thread approval UI. Destructive tools remain controlled by each app's `destructive_enabled` policy.

## Destructive action policy

Destructive plugin elicitations are allowed by default for migrated Codex plugins, while unsafe schemas and ambiguous ownership still fail closed:

- Global `allow_destructive_actions` defaults to `true`.
- Per-plugin `allow_destructive_actions` overrides the global policy for that plugin.
- When policy is `false`, OpenClaw returns a deterministic decline.
- When policy is `true`, OpenClaw auto-accepts only safe schemas it can map to an approval response, such as a boolean approve field.
- When policy is `"auto"`, OpenClaw exposes destructive plugin actions to Codex but turns ownership-proven MCP approval elicitations into OpenClaw plugin approvals before returning the Codex approval response.
- Missing plugin identity, ambiguous ownership, a missing turn id, a wrong turn id, or an unsafe elicitation schema declines instead of prompting.

## Troubleshooting

- **`auth_required`** — migration installed the plugin, but one of its apps still needs authentication; the explicit plugin entry is written disabled until you reauthorize and enable it.
- **`app_inaccessible`, `app_disabled`, or `app_missing`** — migration did not install the plugin because the source Codex app inventory did not show all owned apps as present, enabled, and accessible while `--verify-plugin-apps` was set; reauthorize or enable the app in Codex, then rerun migration with `--verify-plugin-apps`.
- **`app_inventory_unavailable`** — migration did not install the plugin because strict source app verification was requested and source Codex app inventory refresh failed; fix source Codex app-server access or retry without `--verify-plugin-apps` if you accept the faster account-gated plan.
- **`codex_subscription_required`** — migration did not install the app-backed plugin because the source Codex app-server account was not logged in with a ChatGPT subscription account; log in to the Codex app with subscription auth, then rerun migration.
- **`codex_account_unavailable`** — migration did not install the app-backed plugin because the source Codex app-server account could not be read; fix source Codex app-server auth or rerun with `--verify-plugin-apps` if you want source app inventory to decide eligibility when account lookup fails.
- **`marketplace_missing` or `plugin_missing`** — the target Codex app-server cannot see the expected `openai-curated` marketplace or plugin; rerun migration against the target runtime or inspect Codex app-server plugin status.
- **`app_inventory_missing` or `app_inventory_stale`** — app readiness came from an empty or stale cache; OpenClaw schedules an async refresh and excludes plugin apps until ownership and readiness are known.
- **`app_ownership_ambiguous`** — app inventory only matched by display name, so the app is not exposed to the Codex thread.
- **Config changed but the agent cannot see the plugin** — use `/codex plugins list` to confirm the configured state, then use `/new` or `/reset`; existing Codex thread bindings keep the app config they started with until OpenClaw establishes a new harness session or replaces a stale binding.
- **Destructive action is declined** — check the global and per-plugin `allow_destructive_actions` values; even when policy is true or `"auto"`, unsafe elicitation schemas and ambiguous plugin identity still fail closed.

## Related Notes

**Terms**

- **[MCP](../../term_dictionary/term_mcp.md)** — MCP execution; relevance: Codex app-server owns the app-backed MCP execution for native plugins.
- **[Plugin Manifest](../../term_dictionary/term_plugin_manifest.md)** — plugin identity/manifest; relevance: migration writes explicit `marketplaceName`/`pluginName` plugin identities.
- **[Plugin SDK](../../term_dictionary/term_plugin_sdk.md)** — plugin framework; relevance: native Codex plugin/app capabilities vs OpenClaw plugin SDK.
- **[Provider Plugin](../../term_dictionary/term_provider_plugin.md)** — provider/plugin abstraction; relevance: `codexPlugins` is the native-plugin enablement surface inside `plugins.entries.codex`.
- **[Tool Registry](../../term_dictionary/term_tool_registry.md)** — tool catalog; relevance: thread app config (`config.apps`) controls which plugin app tools are exposed.
- **[Guardian](../../term_dictionary/term_guardian.md)** — approval gate; relevance: destructive-action policy + ownership-proven MCP approval elicitations.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway; relevance: subject — managing native Codex plugins from OpenClaw chat (`/codex plugins`).
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — coding-agent runtime; relevance: native plugins run inside the same Codex thread as the OpenClaw turn.

**Docs**

- **[cc_sdk_plugins](../claude_code/cc_sdk_plugins.md)** — SDK plugins; relevance: analog for enabling/configuring plugins for an agent runtime.
- **[cc_plugin_components](../claude_code/cc_plugin_components.md)** — plugin components; relevance: analog for plugin/app inventory and ownership mapping.
- **[cc_managed_plugin_policy_settings](../claude_code/cc_managed_plugin_policy_settings.md)** — managed plugin policy; relevance: analog for enable/disable + destructive-action policy.
- **[hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md)** — built-in plugins; relevance: sibling native-plugin enablement model.
- **[hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md)** — plugin tutorial; relevance: analog for plugin install/eligibility flow.
- **[cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md)** — marketplace install; relevance: analog for `openai-curated` marketplace install/migration.
- **[oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md)** — the base harness this builds on; relevance: native plugins require the working Codex harness first.
- **[oc_plugins_codex_computer_use](oc_plugins_codex_computer_use.md)** — Computer Use uses the same Codex plugin-install machinery; relevance: a sibling Codex-native plugin class.
- **[oc_plugins_community](oc_plugins_community.md)** — community/marketplace plugin discovery counterpart; relevance: the discovery side of the plugin ecosystem.
- **[oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md)** — plugin approval elicitations route through the runtime contract; relevance: the ownership-boundary runtime this policy operates under.

**Repos**

- **[repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md)** — plugin/extension framework; relevance: the `codexPlugins` config + migration code lives here.
- **[repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md)** — app inventory/packaging; relevance: `app/list` inventory, ownership mapping, app config patches.

**Snippets**

- **[snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md)** — plugin lifecycle; relevance: installed/enabled/accessible state machine.
- **[snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md)** — package contract; relevance: plugin identity (`marketplaceName`/`pluginName`).
- **[snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md)** — plugin SDK entries; relevance: `codexPlugins.plugins.*` config entries.
- **[snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md)** — plugin runtime load; relevance: thread-app-config computation at session establish.
- **[snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md)** — plugin config impl; relevance: `/codex plugins enable/disable` writes to OpenClaw config only.
- **[snippet_openclaw_security_plugins_trust_resolver](../../code_snippets/snippet_openclaw_security_plugins_trust_resolver.md)** — plugin trust resolver; relevance: ownership-proven mapping (exact app id / MCP server name).
- **[snippet_openclaw_security_plugins_trust_findings](../../code_snippets/snippet_openclaw_security_plugins_trust_findings.md)** — trust findings; relevance: ambiguous-ownership exclusion until inventory refresh.
- **[snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md)** — approval manager; relevance: destructive-action elicitation → OpenClaw plugin approval.
- **[snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md)** — migration import; relevance: `openclaw migrate codex` plugin-eligibility migration.
- **[snippet_hermes_agent_cli_codex_migrate](../../code_snippets/snippet_hermes_agent_cli_codex_migrate.md)** — Codex migrate CLI; relevance: analog for the migrate-plugins-from-Codex-home flow.
- **[snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md)** — command catalog; relevance: `/codex plugins` chat-command registration.

## References

- [OpenClaw Docs — Native Codex plugins](https://docs.openclaw.ai/plugins/codex-native-plugins)
- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Codex harness reference](https://docs.openclaw.ai/plugins/codex-harness-reference)
- [OpenClaw Docs — Codex harness runtime](https://docs.openclaw.ai/plugins/codex-harness-runtime)
- [OpenClaw Docs — Configuration reference (Codex harness plugin config)](https://docs.openclaw.ai/gateway/configuration-reference#codex-harness-plugin-config)
- [OpenClaw Docs — Migrate CLI](https://docs.openclaw.ai/cli/migrate)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)

**Source**: OpenClaw documentation — `plugins/codex-native-plugins` (mirror `inbox/openclaw_docs/plugins/codex-native-plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
