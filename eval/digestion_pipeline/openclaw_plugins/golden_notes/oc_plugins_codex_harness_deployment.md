---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - codex_harness
keywords:
  - codex harness deployment patterns
  - basic codex deployment
  - mixed provider deployment
  - fail-closed codex agentRuntime
  - app-server policy approval sandbox
  - tools.exec.mode auto guardian
  - danger-full-access workspace-write
  - openclaw codex deployment
topics:
  - OpenClaw
  - Codex Harness Deployment
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/codex-harness
access_control_group: ["general"]
---

# OpenClaw — Codex Harness Deployment Patterns and App-Server Policy

## Overview

This note is the deployment-shape procedure for the bundled `codex` plugin: the three deployment patterns OpenClaw documents — **Basic Codex**, **Mixed provider**, and **Fail-closed Codex** — plus the **app-server policy** that controls approvals, sandbox, and exec behavior per deployment. It mirrors the `plugins/codex-harness` source page sections "Deployment patterns" (Basic / Mixed provider / Fail-closed) and "App-server policy." Enabling, OAuth quickstart, and routing/model selection are covered in the setup note; the full declarative `appServer.*` field reference (transport, timeouts, discovery, env isolation) lives in the harness reference notes. Use this note when choosing how a deployment routes OpenAI agent turns through Codex and what approval/sandbox posture each shape gets.

## Deployment Patterns

The Codex harness supports three deployment shapes you choose between. All three assume the bundled `codex` plugin is enabled and (where `plugins.allow` is configured) allowlisted. The shapes differ in whether Codex is the default runtime, one named agent among several, or a forced fail-closed requirement.

### Basic Codex deployment

Use the quickstart config when all OpenAI agent turns should use Codex by default. This is the minimum viable shape — enable the plugin and point the default agent model at a canonical `openai/gpt-*` ref:

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

### Mixed provider deployment

This shape keeps Claude as the default agent and adds a named Codex agent. The `main` agent uses its normal provider path and the `codex` agent uses Codex app-server:

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
      model: "anthropic/claude-opus-4-6",
    },
    list: [
      {
        id: "main",
        default: true,
        model: "anthropic/claude-opus-4-6",
      },
      {
        id: "codex",
        name: "Codex",
        model: "openai/gpt-5.5",
      },
    ],
  },
}
```

With this config, the `main` agent uses its normal provider path and the `codex` agent uses Codex app-server.

### Fail-closed Codex deployment

For OpenAI agent turns, `openai/gpt-*` already resolves to Codex when the bundled plugin is available. Add explicit runtime policy when you want a written fail-closed rule via provider- (or model-) level `agentRuntime.id: "codex"`:

```json5
{
  models: {
    providers: {
      openai: {
        agentRuntime: {
          id: "codex",
        },
      },
    },
  },
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
    },
  },
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

With Codex forced, OpenClaw fails early if the Codex plugin is disabled, the app-server is too old, or the app-server cannot start — instead of silently falling back to the OpenClaw embedded runtime. Use this shape for Codex-only deployments.

## App-Server Policy

By default, the plugin starts OpenClaw's managed Codex binary locally with stdio transport. Set `appServer.command` only when you intentionally want to run a different executable. Use WebSocket transport only when an app-server is already running elsewhere:

```json5
{
  plugins: {
    entries: {
      codex: {
        enabled: true,
        config: {
          appServer: {
            transport: "websocket",
            url: "ws://gateway-host:39175",
            authToken: "${CODEX_APP_SERVER_TOKEN}",
          },
        },
      },
    },
  },
}
```

Local stdio app-server sessions default to the trusted local operator posture: `approvalPolicy: "never"`, `approvalsReviewer: "user"`, and `sandbox: "danger-full-access"`. If local Codex requirements disallow that implicit YOLO posture, OpenClaw selects allowed guardian permissions instead. When an OpenClaw sandbox is active for the session, OpenClaw disables Codex native Code Mode, user MCP servers, and app-backed plugin execution for that turn instead of relying on Codex host-side sandboxing. Shell access is exposed through OpenClaw sandbox-backed dynamic tools such as `sandbox_exec` and `sandbox_process` when the normal exec/process tools are available.

### Guardian-reviewed exec mode

Use normalized OpenClaw exec mode when you want Codex native auto-review before sandbox escapes or extra permissions:

```json5
{
  tools: {
    exec: {
      mode: "auto",
    },
  },
  plugins: {
    entries: {
      codex: {
        enabled: true,
      },
    },
  },
}
```

For Codex app-server sessions, OpenClaw maps `tools.exec.mode: "auto"` to Codex Guardian-reviewed approvals, usually `approvalPolicy: "on-request"`, `approvalsReviewer: "auto_review"`, and `sandbox: "workspace-write"` when the local requirements allow those values. In `tools.exec.mode: "auto"`, OpenClaw does not preserve legacy unsafe Codex `approvalPolicy: "never"` or `sandbox: "danger-full-access"` overrides; use `tools.exec.mode: "full"` for an intentional no-approval Codex posture. The legacy `plugins.entries.codex.config.appServer.mode: "guardian"` preset still works, but `tools.exec.mode: "auto"` is the normalized OpenClaw surface. For the mode-level comparison with host exec approvals and ACPX permissions, see [Permission modes](https://docs.openclaw.ai/tools/permission-modes).

For every app-server field, auth order, environment isolation, discovery, and timeout behavior, see [Codex harness reference](https://docs.openclaw.ai/plugins/codex-harness-reference).

## Related Notes

**Terms**

- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — agent-turn runtime; relevance: deployments choose whether Codex or OpenClaw owns the harness.
- **[Sandbox](../../term_dictionary/term_sandbox.md)** — execution isolation; relevance: app-server policy sets `sandbox: danger-full-access`/`workspace-write`/`read-only` per deployment.
- **[Model Router](../../term_dictionary/term_model_router.md)** — routes refs to providers/runtimes; relevance: mixed-provider deployment routes `anthropic/*` and `openai/*` to different runtimes.
- **[Model Failover](../../term_dictionary/term_model_failover.md)** — fallback across models; relevance: fail-closed vs auto-fallback runtime policy (`agentRuntime.id: "codex"`).
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — coding-agent runtimes; relevance: per-agent Codex vs Claude assignment.
- **[Provider Plugin](../../term_dictionary/term_provider_plugin.md)** — provider abstraction; relevance: `models.providers.openai.agentRuntime` provider-level policy.
- **[Guardian](../../term_dictionary/term_guardian.md)** — review/approval gate; relevance: app-server policy maps `tools.exec.mode: "auto"` to Codex guardian-reviewed approvals.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway; relevance: subject — fail-closed means OpenClaw errors instead of embedded fallback.

**Docs**

- **[cc_model_selection](../claude_code/cc_model_selection.md)** — model-ref selection; relevance: analog for per-agent model assignment in mixed deployments.
- **[pi_cloud_providers](../pi/pi_cloud_providers.md)** — cloud-provider config; relevance: mixed-provider deployment config analog.
- **[cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md)** — permission/approval modes; relevance: analog for the app-server approval-policy posture per deployment.
- **[cc_sandbox_modes](../claude_code/cc_sandbox_modes.md)** — sandbox modes; relevance: analog for `danger-full-access`/`workspace-write` sandbox selection.
- **[cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md)** — sandbox vs permission policy; relevance: the approval-policy-vs-sandbox split the app-server policy section makes.
- **[hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md)** — Hermes Codex runtime; relevance: sibling deployment of a Codex runtime alongside other providers.
- **[oc_plugins_codex_harness_setup](oc_plugins_codex_harness_setup.md)** — the base config these deployment shapes extend.
- **[oc_plugins_codex_harness_reference_config](oc_plugins_codex_harness_reference_config.md)** — `appServer.mode`/`approvalPolicy`/`sandbox` field reference.
- **[oc_plugins_codex_harness_reference_runtime](oc_plugins_codex_harness_reference_runtime.md)** — sandboxed-native-exec behavior under each deployment.
- **[oc_plugins_codex_harness_runtime](oc_plugins_codex_harness_runtime.md)** — runtime contract these deployments operate under.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent runtime; relevance: per-agent runtime assignment and fail-closed resolution code.
- **[repo_ecosystem_acp_providers](../../../areas/code_repos/repo_ecosystem_acp_providers.md)** — multi-provider ACP routing; relevance: sibling multi-provider deployment pattern.

**Snippets**

- **[snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md)** — runtime config resolution; relevance: implements `agentRuntime.id` fail-closed vs auto.
- **[snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md)** — per-agent scope; relevance: mixed-provider per-agent (`main` Claude, `codex` GPT) config.
- **[snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md)** — model fallback ladder; relevance: contrast with fail-closed (no fallback) Codex deployment.
- **[snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md)** — fallback cooldown; relevance: usage-limit reset/cooldown handling per auth profile.
- **[snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md)** — failover error path; relevance: the fail-closed error surfaced when Codex is unavailable.
- **[snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md)** — exec approval manager; relevance: app-server policy maps `tools.exec.mode` to approval behavior.
- **[snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md)** — exec/filesystem policy; relevance: sandbox modes (`workspace-write`/`read-only`) the policy section selects.
- **[snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md)** — Anthropic provider; relevance: the Claude default in mixed-provider deployment.
- **[snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md)** — OpenAI provider; relevance: the Codex-routed `openai/*` provider.
- **[snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md)** — tool policy gating; relevance: sandbox-active turns disable native code mode / route through `sandbox_exec`.
- **[snippet_hermes_agent_cli_codex_switch](../../code_snippets/snippet_hermes_agent_cli_codex_switch.md)** — Codex runtime switch; relevance: analog for selecting the Codex runtime for an agent.

## References

- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Codex harness reference](https://docs.openclaw.ai/plugins/codex-harness-reference)
- [OpenClaw Docs — Permission modes](https://docs.openclaw.ai/tools/permission-modes)
- [OpenClaw Docs — Agent runtimes](https://docs.openclaw.ai/concepts/agent-runtimes)

**Source**: OpenClaw documentation — `plugins/codex-harness` (mirror `inbox/openclaw_docs/plugins/codex-harness.md`), sections "Deployment patterns" + "App-server policy"
**Last Updated**: 2026-06-22
**Status**: Active
