---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_computer_use
keywords:
  - codex computer use openclaw
  - computer-use mcp plugin
  - /codex computer-use commands
  - computeruse autoinstall config
  - codex marketplace install
  - macos accessibility screen recording permissions
  - fail closed computer use
  - cua-driver mcp
topics:
  - OpenClaw
  - Codex Computer Use
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/codex-computer-use
access_control_group: ["general"]
---

# OpenClaw — Setting Up Codex Computer Use

## Overview

This note is the procedure for enabling **Codex Computer Use**, the Codex-native MCP plugin for local desktop control, on a Codex-mode OpenClaw agent — mirroring the `plugins/codex-computer-use` source page. OpenClaw does **not** vendor the desktop app, execute desktop actions itself, or bypass Codex permissions; the bundled `codex` plugin only *prepares* Codex app-server by enabling Codex plugin support, finding or installing the configured Computer Use plugin, checking that the `computer-use` MCP server is available, and then letting Codex own the native MCP tool calls during Codex-mode turns. Use this procedure only when OpenClaw is already running the native Codex harness (see the setup note); it covers what Computer Use is NOT (Peekaboo, iOS app, direct cua-driver MCP), the `computerUse` config, the `/codex computer-use` commands, marketplace/catalog choices, the setup-reason status machine, and macOS permission + troubleshooting flows.

## When NOT to use this — adjacent paths

Three adjacent desktop/mobile-control paths are explicitly **separate** from Codex Computer Use:

- **OpenClaw.app + Peekaboo** — The macOS app can host a PeekabooBridge socket so the `peekaboo` CLI can reuse the app's local Accessibility and Screen Recording grants for Peekaboo's own automation tools. That bridge does **not** install or proxy Codex Computer Use, and Codex Computer Use does **not** call through the PeekabooBridge socket. Use the Peekaboo bridge when you want OpenClaw.app to be a permission-aware host for Peekaboo CLI automation.
- **iOS app** — The iOS app does not install or proxy the Codex `computer-use` MCP server and is not a desktop-control backend. Instead it connects as an OpenClaw **node** and exposes mobile capabilities through node commands such as `canvas.*`, `camera.*`, `screen.*`, `location.*`, and `talk.*`. Use the iOS path to drive an iPhone node through the gateway.
- **Direct cua-driver MCP** — Codex Computer Use is not the only way to expose desktop control. To let OpenClaw-managed runtimes call TryCua's driver directly, use the upstream `cua-driver mcp` server through OpenClaw's MCP registry instead of the Codex-specific marketplace flow. After installing `cua-driver`, either ask it for the OpenClaw command (`cua-driver mcp-config --client openclaw`) or register the stdio server yourself:

```bash
openclaw mcp set cua-driver '{"command":"cua-driver","args":["mcp"]}'
```

The cua-driver path keeps the upstream MCP tool surface intact (driver schemas and structured MCP responses) — use it when you want the CUA driver available as a normal OpenClaw MCP server. Use the Codex Computer Use setup on this page when Codex app-server should own plugin installation, MCP reloads, and native tool calls inside Codex-mode turns. CUA's driver is macOS-specific and still requires the local macOS permissions its app prompts for (Accessibility and Screen Recording); OpenClaw does not install `cua-driver`, grant those permissions, or bypass the upstream driver's safety model.

## Quick setup

Set `plugins.entries.codex.config.computerUse` when Codex-mode turns must have Computer Use available before a thread starts. `autoInstall: true` opts Computer Use in and lets OpenClaw install or re-enable it before the turn:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          computerUse: {
            autoInstall: true,
          },
        },
      },
    },
  },
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
    },
  },
}
```

With this config, OpenClaw checks Codex app-server before each Codex-mode turn. If Computer Use is missing but Codex app-server has already discovered an installable marketplace, OpenClaw asks Codex app-server to install or re-enable the plugin and reload MCP servers. On macOS, when no matching marketplace is registered and the standard Codex app bundle exists, OpenClaw also tries to register the bundled Codex marketplace from `/Applications/Codex.app/Contents/Resources/plugins/openai-bundled` before it fails. If setup still cannot make the MCP server available, the turn fails before the thread starts. After changing Computer Use config, use `/new` or `/reset` in the affected chat before testing if an existing Codex thread has already started.

## Commands

Use the `/codex computer-use` commands from any chat surface where the `codex` plugin command surface is available. These are OpenClaw chat/runtime commands, **not** `openclaw codex ...` CLI subcommands:

```text
/codex computer-use status
/codex computer-use install
/codex computer-use install --source <marketplace-source>
/codex computer-use install --marketplace-path <path>
/codex computer-use install --marketplace <name>
```

`status` is read-only: it does not add marketplace sources, install plugins, or enable Codex plugin support. If no config opts Computer Use in, `status` can report disabled even after a one-off install command. `install` enables Codex app-server plugin support, optionally adds a configured marketplace source, installs or re-enables the configured plugin through Codex app-server, reloads MCP servers, and verifies that the MCP server exposes tools.

## Marketplace choices

OpenClaw uses the same app-server API that Codex itself exposes; the marketplace fields choose where Codex should find `computer-use`:

| Field | Use when | Install support |
| --- | --- | --- |
| No marketplace field | You want Codex app-server to use marketplaces it already knows. | Yes, when app-server returns a local marketplace. |
| `marketplaceSource` | You have a Codex marketplace source app-server can add. | Yes, for explicit `/codex computer-use install`. |
| `marketplacePath` | You already know the local marketplace file path on the host. | Yes, for explicit install and turn-start auto-install. |
| `marketplaceName` | You want to select one already registered marketplace by name. | Yes only when the selected marketplace has a local path. |

Fresh Codex homes may need a short moment to seed their official marketplaces. During install, OpenClaw polls `plugin/list` for up to `marketplaceDiscoveryTimeoutMs` milliseconds (default 60 seconds). If multiple known marketplaces contain Computer Use, OpenClaw prefers `openai-bundled`, then `openai-curated`, then `local`. Unknown ambiguous matches fail closed and ask you to set `marketplaceName` or `marketplacePath`.

## Bundled macOS marketplace

Recent Codex desktop builds bundle Computer Use at `/Applications/Codex.app/Contents/Resources/plugins/openai-bundled/plugins/computer-use`. When `computerUse.autoInstall` is true and no marketplace containing `computer-use` is registered, OpenClaw tries to add the standard bundled marketplace root automatically (`/Applications/Codex.app/Contents/Resources/plugins/openai-bundled`). You can also register it explicitly from a shell with Codex:

```bash
codex plugin marketplace add /Applications/Codex.app/Contents/Resources/plugins/openai-bundled
```

If you use a nonstandard Codex app path, run `/codex computer-use install --source <marketplace-root>` once, or set `computerUse.marketplacePath` to a local marketplace file path. Use `--marketplace-path` only when you have the marketplace JSON **file** path, not the bundled marketplace **root**.

## Remote catalog limit

Codex app-server can list and read remote-only catalog entries, but it does **not** currently support remote `plugin/install`. That means `marketplaceName` can select a remote-only marketplace for status checks, but installs and re-enables still need a local marketplace via `marketplaceSource` or `marketplacePath`. If status says the plugin is available in a remote Codex marketplace but remote install is unsupported, run install with a local source or path:

```text
/codex computer-use install --source <marketplace-source>
/codex computer-use install --marketplace-path <path>
```

## Configuration reference

The `computerUse` config fields under `plugins.entries.codex.config.computerUse`:

| Field | Default | Meaning |
| --- | --- | --- |
| `enabled` | inferred | Require Computer Use. Defaults to true when another Computer Use field is set. |
| `autoInstall` | false | Install or re-enable from already discovered marketplaces at turn start. |
| `marketplaceDiscoveryTimeoutMs` | 60000 | How long install waits for Codex app-server marketplace discovery. |
| `marketplaceSource` | unset | Source string passed to Codex app-server `marketplace/add`. |
| `marketplacePath` | unset | Local Codex marketplace file path containing the plugin. |
| `marketplaceName` | unset | Registered Codex marketplace name to select. |
| `pluginName` | `computer-use` | Codex marketplace plugin name. |
| `mcpServerName` | `computer-use` | MCP server name exposed by the installed plugin. |

Turn-start auto-install intentionally **refuses** configured `marketplaceSource` values: adding a new source is an explicit setup operation, so use `/codex computer-use install --source <marketplace-source>` once, then let `autoInstall` handle future re-enables from discovered local marketplaces. Turn-start auto-install **can** use a configured `marketplacePath`, because that is already a local path on the host.

## What OpenClaw checks (setup-reason status machine)

OpenClaw reports a stable setup reason internally and formats a user-facing status for chat. The chat output includes the plugin state, MCP server state, marketplace, tools when available, and the specific message for the failing setup step:

| Reason | Meaning | Next step |
| --- | --- | --- |
| `disabled` | `computerUse.enabled` resolved to false. | Set `enabled` or another Computer Use field. |
| `marketplace_missing` | No matching marketplace was available. | Configure source, path, or marketplace name. |
| `plugin_not_installed` | Marketplace exists, but the plugin is not installed. | Run install or enable `autoInstall`. |
| `plugin_disabled` | Plugin is installed but disabled in Codex config. | Run install to re-enable it. |
| `remote_install_unsupported` | Selected marketplace is remote-only. | Use `marketplaceSource` or `marketplacePath`. |
| `mcp_missing` | Plugin is enabled, but the MCP server is unavailable. | Check Codex Computer Use and OS permissions. |
| `ready` | Plugin and MCP tools are available. | Start the Codex-mode turn. |
| `check_failed` | A Codex app-server request failed during status check. | Check app-server connectivity and logs. |
| `auto_install_blocked` | Turn-start setup would need to add a new source. | Run explicit install first. |

## macOS permissions

Computer Use is macOS-specific. The Codex-owned MCP server may need local OS permissions before it can inspect or control apps. If OpenClaw says Computer Use is installed but the MCP server is unavailable, verify the Codex-side Computer Use setup first:

- Codex app-server is running on the same host where desktop control should happen.
- The Computer Use plugin is enabled in Codex config.
- The `computer-use` MCP server appears in Codex app-server MCP status.
- macOS has granted the required permissions for the desktop-control app.
- The current host session can access the desktop being controlled.

OpenClaw intentionally **fails closed** when `computerUse.enabled` is true: a Codex-mode turn should not silently proceed without the native desktop tools that the config required.

## Troubleshooting

- **Status says not installed.** Run `/codex computer-use install`. If the marketplace is not discovered, pass `--source` or `--marketplace-path`.
- **Status says installed but disabled.** Run `/codex computer-use install` again. Codex app-server install writes the plugin config back to enabled.
- **Status says remote install is unsupported.** Use a local marketplace source or path. Remote-only catalog entries can be inspected but not installed through the current app-server API.
- **Status says the MCP server is unavailable.** Re-run install once so MCP servers reload. If it remains unavailable, fix the Codex Computer Use app, Codex app-server MCP status, or macOS permissions.
- **Status or a probe times out on `computer-use.list_apps`.** The plugin and MCP server are present, but the local Computer Use bridge did not answer. Quit or restart Codex Computer Use, relaunch Codex Desktop if needed, then retry in a fresh OpenClaw session.
- **A Computer Use tool says `Native hook relay unavailable`.** The Codex-native tool hook could not reach an active OpenClaw relay through the local bridge or Gateway fallback. Start a fresh OpenClaw session with `/new` or `/reset`. If it works once and then fails again on a later tool call, `/new` is only clearing the current attempt; restart the Codex app-server or OpenClaw Gateway so old threads and hook registrations are dropped, then retry in a fresh session.
- **Turn-start auto-install refuses a source.** This is intentional. Add the source with explicit `/codex computer-use install --source <marketplace-source>` first, then future turn-start auto-install can use the discovered local marketplace.

## Related Notes

**Terms**

- **[MCP](../../term_dictionary/term_mcp.md)** — Model Context Protocol tool/server interface; relevance: Computer Use is a Codex-native MCP plugin (`computer-use` MCP server) that OpenClaw checks for availability before a turn.
- **[Sandbox](../../term_dictionary/term_sandbox.md)** — isolated execution boundary; relevance: desktop control runs under Codex permissions and the host's macOS permission grants, not OpenClaw's own exec.
- **[Tool Registry](../../term_dictionary/term_tool_registry.md)** — catalog of callable tools; relevance: OpenClaw verifies the MCP server exposes tools (`computer-use.list_apps`) and reloads MCP servers on install.
- **[Function Calling](../../term_dictionary/term_function_calling.md)** — model-issued structured tool calls; relevance: Codex owns the native MCP tool calls during Codex-mode turns; OpenClaw only prepares them.
- **[Multimodal](../../term_dictionary/term_multimodal.md)** — text + image/screen modalities; relevance: desktop control inspects and acts on screen state — a multimodal capability requiring Screen Recording grants.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — agentic coding tools (Codex/Claude Code); relevance: Computer Use extends a Codex-mode OpenClaw agent's action surface to the local desktop.
- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — the runtime executing agent turns; relevance: Computer Use is only available when OpenClaw runs the native Codex harness.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the self-hosted gateway; relevance: subject system — OpenClaw prepares (does not vendor/execute) the plugin and fails closed when `computerUse.enabled` is true.

**Docs**

- **[cc_computer_use](../claude_code/cc_computer_use.md)** — Anthropic's computer-use tool; relevance: closest sibling-tool analog (screenshot/click/type desktop control via a coding agent).
- **[cc_computer_use_safety](../claude_code/cc_computer_use_safety.md)** — computer-use safety/permission guidance; relevance: parallels the macOS Accessibility/Screen-Recording permission + fail-closed posture this note documents.
- **[hermes_computer_use_macos](../hermes_agent/hermes_computer_use_macos.md)** — Hermes macOS computer-use setup; relevance: the macOS-permission-gated desktop-control flow in a sibling coding-agent gateway.
- **[cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md)** — managing MCP server config; relevance: analog for the `marketplaceSource`/`marketplacePath`/`marketplaceName` MCP-install config this note covers.
- **[cc_mcp_server_management](../claude_code/cc_mcp_server_management.md)** — installing/enabling/reloading MCP servers; relevance: mirrors OpenClaw's install/re-enable/reload-MCP-servers status machine (`disabled`/`mcp_missing`/`ready`).
- **[pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md)** — registering custom MCP/agent tools; relevance: analog for the `openclaw mcp set cua-driver` direct-MCP alternative path.
- **[oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md)** `(planned, this series)` — enabling the native Codex harness; relevance: prerequisite — Computer Use needs the harness running first.
- **[oc_plugins_codex_native_plugins](oc_plugins_codex_native_plugins.md)** `(planned, this series)` — native Codex plugin management; relevance: same Codex app-server plugin-install machinery, different plugin class.
- **[oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md)** `(planned, this series)` — the `computerUse` config surface lives in the harness config reference.
- **[oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md)** `(planned, this series)` — `Native hook relay unavailable` troubleshooting ties to the native hook/relay runtime contract.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — Codex/agent runtime code; relevance: the agent-runtime side that drives Codex-mode turns where Computer Use is prepared.
- **[repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md)** — plugin/extension framework; relevance: the bundled `codex` plugin that hosts the `computerUse` setup lives here.

**Snippets**

- **[snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md)** — OpenAI provider wiring; relevance: Computer Use runs on `openai/gpt-*` Codex-mode turns.
- **[snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md)** — tool catalog assembly; relevance: how the `computer-use` MCP tools enter the agent's available-tool set.
- **[snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md)** — tool gating policy; relevance: fail-closed gating when the required MCP server is unavailable.
- **[snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md)** — MCP loopback transport; relevance: the MCP-server transport plane the `computer-use` server attaches to.
- **[snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md)** — plugin enable/install lifecycle; relevance: the install/re-enable/reload steps this note's setup machine performs.
- **[snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md)** — plugin package contract; relevance: marketplace plugin shape that `pluginName`/`mcpServerName` select.
- **[snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md)** — macOS app surface lifecycle; relevance: the macOS host context (permissions, app bundle) Computer Use depends on.
- **[snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md)** — dangerous-tool denial; relevance: the fail-closed safety posture around native desktop-control tools.
- **[snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md)** — registering agent tools; relevance: analog for exposing native plugin tools into the agent turn.
- **[snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md)** — node command policy; relevance: contrasts with the iOS-node `canvas.*/camera.*/screen.*` path this note distinguishes from Computer Use.
- **[snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md)** — iOS node pairing; relevance: the iOS-app-as-node path explicitly contrasted with desktop Computer Use.

## References

- [OpenClaw Docs — Codex Computer Use](https://docs.openclaw.ai/plugins/codex-computer-use)
- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Peekaboo bridge](https://docs.openclaw.ai/platforms/mac/peekaboo)
- [OpenClaw Docs — iOS app](https://docs.openclaw.ai/platforms/ios)

**Source**: OpenClaw documentation — `plugins/codex-computer-use` (mirror `inbox/openclaw_docs/plugins/codex-computer-use.md`)
**Last Updated**: 2026-06-22
**Status**: Active
