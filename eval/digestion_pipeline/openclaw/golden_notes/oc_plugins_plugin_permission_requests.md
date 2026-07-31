---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - permissions
keywords:
  - openclaw plugin permission requests
  - plugin.approval flow
  - before_tool_call requireApproval
  - allowedDecisions allow-once allow-always deny
  - approvals.plugin routing
  - codex native permissions mcp elicitation
  - choose the right gate
topics:
  - OpenClaw
  - Plugin Permissions
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/plugin-permission-requests
access_control_group: ["general"]
---

# OpenClaw — Plugin Permission Requests (`plugin.approval.*` Gate)

## Overview

This note is the procedure for **plugin permission requests** in OpenClaw: how plugin code pauses a tool call or plugin-owned operation until a user approves or denies it, using the Gateway `plugin.approval.*` flow and the same approval UI surfaces that handle chat approval buttons and `/approve` commands. It mirrors the `plugins/plugin-permission-requests` source page: choosing the right gate among five decision points, requesting approval before a tool call via a `before_tool_call` hook, the decision-behavior table, routing prompts with `approvals.plugin`, how Codex native permissions travel through plugin approvals, and troubleshooting. Plugin permission requests are for plugin/app permissions; they do **not** replace host exec approvals, optional tool allowlists, or Codex's native permission review.

## Choose the Right Gate

OpenClaw has five distinct permission gates; pick the one matching the decision point you need. **Optional tools** gate **tool exposure through `tools.allow`** — use them when a tool should not be visible to the model until the user opts in (a discovery-time gate). **Plugin permission requests** gate **runtime approval through `plugin.approval.*`** — use them when a plugin hook or plugin-owned operation must ask before one action runs (a per-call gate). **Exec approvals** gate **host exec policy and durable exec allowlists** — use them when a host command or shell-like tool needs operator approval. **Codex native permission requests** gate **Codex app-server or native hook approval handling, routed through plugin approvals when OpenClaw owns the prompt** — use them when Codex asks before native shell, file, MCP, or app-server actions. **MCP approval elicitations** gate **MCP approval responses bridged through OpenClaw plugin approvals** — use them when a Codex MCP server requests approval for a tool call.

Optional tools and plugin permission requests are complementary, not exclusive: optional tools are a discovery-time gate while plugin permission requests are a per-call gate. Use both when a sensitive tool should require explicit opt-in before the model can see it AND approval before the action runs.

## Request Approval Before a Tool Call

Most plugin-authored prompts should start in a `before_tool_call` hook. The hook runs after the model selects a tool and before OpenClaw executes it. The hook returns a `requireApproval` object describing the prompt and the allowed decisions:

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "deploy-policy",
  name: "Deploy Policy",
  register(api) {
    api.on("before_tool_call", async (event) => {
      if (event.toolName !== "deploy_service") {
        return;
      }

      const environment =
        typeof event.params.environment === "string" ? event.params.environment : "unknown";

      return {
        requireApproval: {
          title: "Deploy service",
          description: `Deploy service to ${environment}.`,
          severity: environment === "production" ? "critical" : "warning",
          allowedDecisions:
            environment === "production"
              ? ["allow-once", "deny"]
              : ["allow-once", "allow-always", "deny"],
          timeoutMs: 120_000,
          timeoutBehavior: "deny",
          onResolution(decision) {
            console.log(`deploy approval resolved: ${decision}`);
          },
        },
      };
    });
  },
});
```

### Authoring the Prompt Text

Write the prompt text for the person who will approve the action. Per source, the authoring rules are: keep `title` short and action-focused — the Gateway accepts up to **80 characters**; keep `description` specific and bounded — the Gateway accepts up to **256 characters**; include the action, target, and risk, but do **not** include secrets, tokens, or private payloads that should not appear in chat approval surfaces; use `severity: "critical"` only for actions where the wrong decision could cause production damage or data loss; and use `allowedDecisions: ["allow-once", "deny"]` when persistent trust is unsafe for that action.

## Decision Behavior

OpenClaw creates a pending approval with a `plugin:` ID, delivers it to the available approval surfaces, and waits for a decision. Each possible decision resolves the gated call as follows:

| Decision          | Result                                                                    |
| ----------------- | ------------------------------------------------------------------------- |
| `allow-once`      | The current call continues.                                               |
| `allow-always`    | The current call continues and the decision is passed to the plugin.      |
| `deny`            | The call is blocked with a denied tool result.                            |
| Timeout           | The call is blocked unless `timeoutBehavior` is `"allow"`.                |
| Cancellation      | The call is blocked when the run is aborted.                              |
| No approval route | The call is blocked because no connected approval surface can resolve it. |

`allow-always` is only durable when the requesting plugin or runtime implements that persistence. For ordinary `before_tool_call.requireApproval` hooks, OpenClaw treats `allow-once` and `allow-always` as approval decisions for the current call and passes the resolved value to `onResolution`. If your plugin offers `allow-always`, document and implement exactly what future calls it trusts. If the hook also returns `params`, OpenClaw applies those parameter changes only **after** the approval succeeds, and a lower-priority hook can still block after a higher-priority hook requested approval. `allowedDecisions` limits the buttons and commands shown to the user, and the Gateway rejects a resolve attempt for any decision the request did not offer.

## Route Approval Prompts

Approval prompts can resolve in local UI surfaces or in chat channels that support approval handling. To forward plugin approval prompts to explicit chat targets, configure `approvals.plugin`:

```json5
{
  approvals: {
    plugin: {
      enabled: true,
      mode: "targets",
      agentFilter: ["main"],
      targets: [{ channel: "slack", to: "U12345678" }],
    },
  },
}
```

`approvals.plugin` is independent from `approvals.exec`: enabling exec approval forwarding does **not** route plugin approval prompts, and enabling plugin approval forwarding does **not** change host exec policy. When a prompt includes manual approval text, resolve it with one of the offered decisions:

```text
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

The full forwarding model — same-chat approval behavior, native channel delivery, and channel-specific approver rules — is documented in the source under [Advanced exec approvals](https://docs.openclaw.ai/tools/exec-approvals-advanced#plugin-approval-forwarding).

## Codex Native Permissions

Codex native permission prompts can also travel through plugin approvals, but they have different ownership than plugin-authored hooks. Per source: Codex app-server approval requests route through OpenClaw **after** Codex review; the native hook `permission_request` relay can ask through `plugin.approval.request` when that relay is enabled; and MCP tool approval elicitations route through plugin approvals when Codex marks `_meta.codex_approval_kind` as `"mcp_tool_call"`. The Codex-specific behavior and fallback rules are documented under [Codex harness runtime](https://docs.openclaw.ai/plugins/codex-harness-runtime#native-permissions-and-mcp-elicitations).

## Troubleshooting

The source page lists four common failure modes and their fixes:

- **The tool says plugin approvals are unavailable.** No approval UI or configured approval route accepted the request. Connect an approval-capable client, use a channel that supports same-chat `/approve`, or configure `approvals.plugin`.
- **`allow-always` appears but the next call prompts again.** The generic plugin approval flow does not automatically persist trust for arbitrary hooks. Persist plugin-owned trust in your plugin after `onResolution("allow-always")`, or offer only `allow-once` and `deny`.
- **`/approve` rejects the decision.** The request restricted `allowedDecisions`. Use one of the decisions printed in the prompt.
- **A Slack, Discord, Telegram, or Matrix prompt routes differently from exec approvals.** Plugin approvals and exec approvals use separate config and may use different authorization checks. Verify `approvals.plugin` and the channel's plugin approval support instead of only checking `approvals.exec`.

**Source**: OpenClaw documentation — `plugins/plugin-permission-requests` (mirror `inbox/openclaw_docs/plugins/plugin-permission-requests.md`)
**Last Updated**: 2026-06-22
**Status**: Active
