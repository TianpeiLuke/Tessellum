---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - openclaw codex harness setup
  - bundled codex plugin enable
  - codex app-server quickstart
  - openai/gpt-5.5 model ref
  - openclaw models auth login --provider openai
  - auth.order.openai subscription-first
  - agentRuntime.id codex
  - verify codex runtime /status
  - routing and model selection
topics:
  - OpenClaw
  - Codex Harness
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/codex-harness
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Setup (Enable, Configure, Verify, Route)

## Overview

This note is the setup procedure for the bundled `codex` plugin, which lets OpenClaw run embedded OpenAI agent turns through **Codex app-server** instead of the built-in OpenClaw harness. It covers the intro ownership boundary (what OpenClaw owns vs what Codex owns), requirements, the OAuth quickstart, the configuration-table options, runtime verification, and the routing/model-selection rules that keep `openai/gpt-*` provider refs separate from runtime policy — the first six sections of the `plugins/codex-harness` source page. Deployment patterns, app-server policy, commands/diagnostics, native Codex plugins, Computer Use, the full runtime-boundaries contract, and troubleshooting live in the sibling notes (see Related Notes). Full option lists, defaults, enums, discovery, environment isolation, and timeouts live in the Codex harness reference notes.

## What the Codex harness owns vs OpenClaw

Use the Codex harness when you want Codex to own the low-level agent session: native thread resume, native tool continuation, native compaction, and app-server execution. OpenClaw still owns chat channels, session files, model selection, OpenClaw dynamic tools, approvals, media delivery, and the visible transcript mirror. The normal setup uses canonical OpenAI model refs such as `openai/gpt-5.5` — do not configure legacy Codex GPT refs. Put OpenAI agent auth order under `auth.order.openai`; older legacy Codex auth profile ids and legacy Codex auth order entries are legacy state repaired by `openclaw doctor --fix`.

When no OpenClaw sandbox is active, OpenClaw starts Codex app-server threads with Codex native code mode enabled while leaving code-mode-only off by default, keeping Codex native workspace and code capabilities available while OpenClaw dynamic tools continue through the app-server `item/tool/call` bridge. Active OpenClaw sandboxing and restricted tool policies disable native code mode entirely unless you opt into the experimental sandbox exec-server path. This Codex-native feature is separate from OpenClaw code mode (the opt-in QuickJS-WASI runtime at `/reference/code-mode` for generic OpenClaw runs with a different `exec` input shape) — link out, not redefined here. The short version of the broader model/provider/runtime split (see Agent runtimes): `openai/gpt-5.5` is the model ref, `codex` is the runtime, and Telegram, Discord, Slack, or another channel remains the communication surface.

## Requirements

The bundled `codex` plugin needs the following available before setup:

- OpenClaw with the bundled `codex` plugin available.
- If your config uses `plugins.allow`, include `codex`.
- Codex app-server `0.125.0` or newer. The bundled plugin manages a compatible Codex app-server binary by default, so local `codex` commands on `PATH` do not affect normal harness startup.
- Codex auth available through `openclaw models auth login --provider openai`, an app-server account in the agent's Codex home, or an explicit Codex API-key auth profile.

For auth precedence, environment isolation, custom app-server commands, model discovery, and all config fields, see the Codex harness reference (`/plugins/codex-harness-reference`).

## Quickstart

Most users who want Codex in OpenClaw want this path: sign in with a ChatGPT/Codex subscription, enable the bundled `codex` plugin, and use a canonical `openai/gpt-*` model ref. First sign in with Codex OAuth:

```bash
openclaw models auth login --provider openai
```

Then enable the bundled `codex` plugin and select an OpenAI agent model:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
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

If your config uses `plugins.allow`, add `codex` there too:

```json5
{
  plugins: {
    allow: ["codex"],
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

Restart the gateway after changing plugin config. If an existing chat already has a session, use `/new` or `/reset` before testing runtime changes so the next turn resolves the harness from current config.

## Configuration

The quickstart config is the minimum viable Codex harness config. Set Codex harness options in OpenClaw config, and use the CLI only for Codex auth. The configuration-decision table maps each need to a setting and where it lives:

| Need | Set | Where |
| --- | --- | --- |
| Enable the harness | `plugins.entries.codex.enabled: true` | OpenClaw config |
| Keep an allowlisted plugin install | Include `codex` in `plugins.allow` | OpenClaw config |
| Route OpenAI agent turns through Codex | `agents.defaults.model` or `agents.list[].model` as `openai/gpt-*` | OpenClaw agent config |
| Sign in with ChatGPT/Codex OAuth | `openclaw models auth login --provider openai` | CLI auth profile |
| Add API-key backup for Codex runs | `openai:*` API-key profile listed after subscription auth in `auth.order.openai` | CLI auth profile + OpenClaw config |
| Fail closed when Codex is unavailable | Provider or model `agentRuntime.id: "codex"` | OpenClaw model/provider config |
| Use direct OpenAI API traffic | Provider or model `agentRuntime.id: "openclaw"` with normal OpenAI auth | OpenClaw model/provider config |
| Tune app-server behavior | `plugins.entries.codex.config.appServer.*` | Codex plugin config |
| Enable native Codex plugin apps | `plugins.entries.codex.config.codexPlugins.*` | Codex plugin config |
| Enable Codex Computer Use | `plugins.entries.codex.config.computerUse.*` | Codex plugin config |

Use `openai/gpt-*` model refs for Codex-backed OpenAI agent turns and prefer `auth.order.openai` for subscription-first/API-key-backup ordering. Existing legacy Codex auth profile ids and legacy Codex auth order are doctor-only legacy state; do not write new legacy Codex GPT refs.

Do not set `compaction.model` or `compaction.provider` on Codex-backed agents. Codex compacts through its native app-server thread state, so OpenClaw ignores those local summarizer overrides at runtime and `openclaw doctor --fix` removes them when the agent uses Codex. Lossless remains supported as a context engine for assembly, ingestion, and maintenance around Codex turns — configure it through `plugins.slots.contextEngine: "lossless-claw"` and `plugins.entries.lossless-claw.config.summaryModel`, not through `agents.defaults.compaction.provider`. `openclaw doctor --fix` migrates the old `compaction.provider: "lossless-claw"` shape to the Lossless context-engine slot when Codex is the active runtime, but native Codex still owns compaction. The native Codex app-server harness supports context engines that require pre-prompt assembly; generic CLI backends, including `codex-cli`, do not provide that host capability. For Codex-backed agents, `/compact` starts native Codex app-server compaction on the bound thread — OpenClaw does not wait for completion, impose an OpenClaw timeout, restart the shared app-server, or fall back to a context-engine or public OpenAI summarizer, and if the native Codex thread binding is missing or stale the command fails closed so the operator sees the real runtime boundary instead of silently switching compaction backends.

The subscription-first / API-key-backup auth order is configured as:

```json5
{
  auth: {
    order: {
      openai: ["openai:user@example.com", "openai:api-key-backup"],
    },
  },
}
```

In that shape, both profiles still run through Codex for `openai/gpt-*` agent turns — the API key is only an auth fallback, not a request to switch to OpenClaw or plain OpenAI Responses. The rest of the harness surface covers common variants users must choose between (deployment shape, fail-closed routing, guardian approval policy, native Codex plugins, and Computer Use); for full option lists, defaults, enums, discovery, environment isolation, timeouts, and app-server transport fields, see the Codex harness reference.

## Verify Codex runtime

Use `/status` in the chat where you expect Codex. A Codex-backed OpenAI agent turn shows:

```text
Runtime: OpenAI Codex
```

Then check Codex app-server state with `/codex status` and `/codex models`. `/codex status` reports app-server connectivity, account, rate limits, MCP servers, and skills. `/codex models` lists the live Codex app-server catalog for the harness and account. If `/status` is surprising, see the troubleshooting section of the source page (digested in the diagnostics sibling note).

## Routing and model selection

Keep provider refs and runtime policy separate:

- Use `openai/gpt-*` for OpenAI agent turns through Codex.
- Do not use legacy Codex GPT refs in config. Run `openclaw doctor --fix` to repair legacy refs and stale session route pins.
- `agentRuntime.id: "codex"` is optional for normal OpenAI auto mode, but useful when a deployment should fail closed if Codex is unavailable.
- `agentRuntime.id: "openclaw"` opts a provider or model into the OpenClaw embedded runtime when that is intentional.
- `/codex ...` controls native Codex app-server conversations from chat.
- ACP/acpx is a separate external harness path. Use it only when the user asks for ACP/acpx or an external harness adapter.

The common command-routing table maps a user intent to the chat command to use:

| User intent | Use |
| --- | --- |
| Attach the current chat | `/codex bind [--cwd <path>]` |
| Resume an existing Codex thread | `/codex resume <thread-id>` |
| List or filter Codex threads | `/codex threads [filter]` |
| List native Codex plugins | `/codex plugins list` |
| Enable or disable a configured native Codex plugin | `/codex plugins enable <name>`, `/codex plugins disable <name>` |
| Attach an existing Codex CLI session on a paired node | `/codex sessions --host <node> [filter]`, then `/codex resume <session-id> --host <node> --bind here` |
| Send Codex feedback only | `/codex diagnostics [note]` |
| Start an ACP/acpx task | ACP/acpx session commands, not `/codex` |

The use-case routing table maps a deployment goal to its config, verification, and notes:

| Use case | Configure | Verify | Notes |
| --- | --- | --- | --- |
| ChatGPT/Codex subscription with native Codex runtime | `openai/gpt-*` plus enabled `codex` plugin | `/status` shows `Runtime: OpenAI Codex` | Recommended path |
| Fail closed if Codex is unavailable | Provider or model `agentRuntime.id: "codex"` | Turn fails instead of embedded fallback | Use for Codex-only deployments |
| Direct OpenAI API-key traffic through OpenClaw | Provider or model `agentRuntime.id: "openclaw"` and normal OpenAI auth | `/status` shows OpenClaw runtime | Use only when OpenClaw is intentional |
| Legacy config | legacy Codex GPT refs | `openclaw doctor --fix` rewrites it | Do not write new config this way |
| ACP/acpx Codex adapter | ACP `sessions_spawn({ runtime: "acp" })` | ACP task/session status | Separate from native Codex harness |

`agents.defaults.imageModel` follows the same prefix split: use `openai/gpt-*` for the normal OpenAI route and `codex/gpt-*` only when image understanding should run through a bounded Codex app-server turn. Do not use legacy Codex GPT refs; doctor rewrites that legacy prefix to `openai/gpt-*`.

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — self-hosted gateway; relevance: the bundled `codex` plugin lets OpenClaw run embedded OpenAI turns through Codex app-server.
- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — runtime executing agent turns; relevance: this note enables/configures the Codex app-server harness vs OpenClaw's built-in harness.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — agentic coding tools; relevance: Codex is the OpenAI coding-agent runtime being enabled.
- **[OAuth Token](../../term_dictionary/term_oauth_token.md)** — OAuth credential; relevance: quickstart signs in with ChatGPT/Codex OAuth via `openclaw models auth login --provider openai`.
- **[Authentication](../../term_dictionary/term_authentication.md)** — identity/credential verification; relevance: `auth.order.openai` subscription-first/API-key-backup ordering.
- **[LLM](../../term_dictionary/term_llm.md)** — large language model; relevance: `openai/gpt-*` is the model ref routed through Codex.
- **[Claude](../../term_dictionary/term_claude.md)** — Anthropic's model family; relevance: contrasted as the non-Codex default in mixed deployments; provider/model names documented as config not terms.
- **[Provider Plugin](../../term_dictionary/term_provider_plugin.md)** — provider/plugin abstraction; relevance: `plugins.entries.codex` is the provider-plugin enabling Codex runtime.

**Docs**

- **[pi_provider_auth](../pi/pi_provider_auth.md)** — subscription-vs-key provider auth; relevance: direct analog for the OAuth-subscription-first / API-key-backup auth ordering.
- **[cc_model_selection](../claude_code/cc_model_selection.md)** — selecting model refs; relevance: analog for `agents.defaults.model: "openai/gpt-5.5"` model-ref selection.
- **[hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md)** — Hermes Codex runtime setup; relevance: the closest sibling-gateway Codex-runtime enable-and-verify quickstart.
- **[cc_amazon_bedrock_model_config](../claude_code/cc_amazon_bedrock_model_config.md)** — provider/model config; relevance: analog for the provider-backed model-config quickstart pattern.
- **[pi_cloud_providers](../pi/pi_cloud_providers.md)** — cloud provider config; relevance: analog for routing model refs to a specific provider runtime.
- **[cc_fallback_models](../claude_code/cc_fallback_models.md)** — fallback model config; relevance: analog for the API-key-backup auth fallback (not a runtime switch).
- **[oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md)** — full config-field reference for the fields introduced in setup.
- **[oc_plugins_codex_harness_deployment](oc_plugins_codex_harness_deployment.md)** — deployment patterns building on the quickstart config.
- **[oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md)** — the runtime contract that the verified harness obeys.
- **[oc_plugins_codex_harness_diagnostics](oc_plugins_codex_harness_diagnostics.md)** — `/codex status`/`/status` verification commands continue here.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent/Codex runtime code; relevance: the runtime-resolution code that maps `openai/gpt-*` to the Codex harness.
- **[repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md)** — CLI/setup wizard; relevance: `openclaw models auth login` + `openclaw doctor --fix` live on the CLI side.

**Snippets**

- **[snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md)** — OpenAI provider; relevance: the provider whose `openai/gpt-*` refs resolve to Codex.
- **[snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md)** — agent runtime config; relevance: how `agentRuntime.id`/`plugins.entries.codex.enabled` resolve the harness.
- **[snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md)** — auth-profile ordering; relevance: implements `auth.order.openai` subscription-first/API-key-backup.
- **[snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md)** — OAuth profile portability; relevance: the ChatGPT/Codex OAuth profile the quickstart creates.
- **[snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md)** — external-CLI auth profiles; relevance: Codex app-server account vs OpenClaw auth-profile precedence.
- **[snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md)** — model catalog; relevance: `openai/gpt-*` model availability for agent config.
- **[snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md)** — model discovery normalize; relevance: `/codex models` live catalog the setup verifies.
- **[snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md)** — Anthropic provider; relevance: the Claude default in mixed-provider setups.
- **[snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md)** — gateway runtime env; relevance: gateway restart after plugin config change.
- **[snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md)** — setup-wizard config write; relevance: how `plugins.entries.codex` config is authored.
- **[snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md)** — Hermes Codex runtime; relevance: sibling impl of resolving and running a Codex runtime.
- **[snippet_hermes_agent_cli_codex_switch](../../code_snippets/snippet_hermes_agent_cli_codex_switch.md)** — Codex CLI switch; relevance: analog for switching an agent to the Codex runtime.

## References

- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Codex harness reference](https://docs.openclaw.ai/plugins/codex-harness-reference)
- [OpenClaw Docs — Agent runtimes](https://docs.openclaw.ai/concepts/agent-runtimes)
- [OpenClaw Docs — Model providers](https://docs.openclaw.ai/concepts/model-providers)
- [OpenClaw Docs — OpenAI provider](https://docs.openclaw.ai/providers/openai)
- [OpenClaw Docs — OpenClaw code mode](https://docs.openclaw.ai/reference/code-mode)
- [OpenClaw Docs — Status](https://docs.openclaw.ai/cli/status)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)

**Source**: OpenClaw documentation — `plugins/codex-harness` (intro, Requirements, Quickstart, Configuration, Verify Codex runtime, Routing and model selection; mirror `inbox/openclaw_docs/plugins/codex-harness.md`)
**Last Updated**: 2026-06-22
**Status**: Active
