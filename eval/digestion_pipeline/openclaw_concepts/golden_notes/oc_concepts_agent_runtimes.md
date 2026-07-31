---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - agent_runtimes
keywords:
  - openclaw agent runtime
  - provider model runtime harness channel
  - embedded harness vs cli backend
  - codex surfaces app-server acp
  - runtime selection precedence
  - agentruntime.id model-scoped policy
  - github copilot runtime
  - execution runtime status labels
topics:
  - OpenClaw
  - Agent Runtimes
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/agent-runtimes
access_control_group: ["general"]
---

# OpenClaw — Agent Runtimes (Provider vs Model vs Runtime vs Harness vs Channel)

## Overview

This note captures the OpenClaw **agent runtime** taxonomy from the `concepts/agent-runtimes` source page: the four configuration layers that are easy to confuse (provider, model, agent runtime, channel), what a **harness** is, the two runtime families (embedded harnesses vs CLI backends), the five surfaces that share the "Codex" name, the loop-ownership split between the OpenClaw embedded runtime and the Codex app-server, the runtime-selection precedence order, the opt-in GitHub Copilot runtime, the compatibility-contract questionnaire, and how to read the `Execution` / `Runtime` status labels.

## What an Agent Runtime Is

An **agent runtime** is the component that owns one prepared model loop: it receives the prompt, drives model output, handles native tool calls, and returns the finished turn to OpenClaw. Runtimes are easy to confuse with providers because both show up near model configuration, but they are different layers:

| Layer | Examples | What it means |
|---|---|---|
| Provider | `openai`, `anthropic`, `github-copilot` | How OpenClaw authenticates, discovers models, and names model refs. |
| Model | `gpt-5.5`, `claude-opus-4-6` | The model selected for the agent turn. |
| Agent runtime | `openclaw`, `codex`, `copilot`, `claude-cli` | The low level loop or backend that executes the prepared turn. |
| Channel | Telegram, Discord, Slack, WhatsApp | Where messages enter and leave OpenClaw. |

A **harness** is the term seen in code: the implementation that provides an agent runtime. For example, the bundled Codex harness implements the `codex` runtime. Public config uses `agentRuntime.id` on provider or model entries; whole-agent runtime keys are legacy and ignored. `openclaw doctor --fix` removes old whole-agent runtime pins and rewrites legacy runtime model refs to canonical provider/model refs plus model-scoped runtime policy where needed.

## Runtime Families: Embedded Harnesses vs CLI Backends

There are two runtime families. **Embedded harnesses** run inside OpenClaw's prepared agent loop; today this is the built-in `openclaw` runtime plus registered plugin harnesses such as `codex` and `copilot`. **CLI backends** run a local CLI process while keeping the model ref canonical — for example, `anthropic/claude-opus-4-8` with a model-scoped `agentRuntime.id: "claude-cli"` means "select the Anthropic model, execute through Claude CLI." Critically, `claude-cli` is not an embedded harness id and must not be passed to AgentHarness selection. The `copilot` harness is a separate, opt-in external plugin harness for the GitHub Copilot CLI; the user-facing decision between PI, Codex, and GitHub Copilot agent runtime is documented on its own page.

## Codex Surfaces

Most confusion comes from several different surfaces sharing the Codex name. The page lists five intentionally independent surfaces:

| Surface | OpenClaw name/config | What it does |
|---|---|---|
| Native Codex app-server runtime | `openai/*` model refs | Runs OpenAI embedded agent turns through Codex app-server. This is the usual ChatGPT/Codex subscription setup. |
| Codex OAuth auth profiles | `openai` OAuth profiles | Stores ChatGPT/Codex subscription auth that the Codex app-server harness consumes. |
| Codex ACP adapter | `runtime: "acp"`, `agentId: "codex"` | Runs Codex through the external ACP/acpx control plane. Use only when ACP/acpx is explicitly asked. |
| Native Codex chat-control command set | `/codex ...` | Binds, resumes, steers, stops, and inspects Codex app-server threads from chat. |
| OpenAI Platform API route for non-agent surfaces | `openai/*` plus API-key auth | Used for direct OpenAI APIs such as images, embeddings, speech, and realtime. |

Those surfaces are intentionally independent. Enabling the `codex` plugin makes the native app-server features available; `openclaw doctor --fix` owns legacy Codex route repair and stale session pin cleanup. Selecting `openai/*` for an agent model now means "run this through Codex" unless a non-agent OpenAI API surface is being used. The common ChatGPT/Codex subscription setup uses Codex OAuth for auth, but keeps the model ref as `openai/*` and selects the `codex` runtime:

```json5
{
  agents: {
    defaults: {
      model: "openai/gpt-5.5",
    },
  },
}
```

That means OpenClaw selects an OpenAI model ref, then asks the Codex app-server runtime to run the embedded agent turn. It does not mean "use API billing," nor that the channel, model provider catalog, or OpenClaw session store becomes Codex. When the bundled `codex` plugin is enabled, natural-language Codex control should use the native `/codex` command surface (`/codex bind`, `/codex threads`, `/codex resume`, `/codex steer`, `/codex stop`) instead of ACP. Use ACP for Codex only when the user explicitly asks for ACP/acpx or is testing the ACP adapter path; Claude Code, Gemini CLI, OpenCode, Cursor, and similar external harnesses still use ACP.

### Codex Decision Tree

The agent-facing decision tree is: (1) if the user asks for **Codex bind/control/thread/resume/steer/stop**, use the native `/codex` command surface when the bundled `codex` plugin is enabled; (2) if the user asks for **Codex as the embedded runtime** or wants the normal subscription-backed Codex agent experience, use `openai/<model>`; (3) if the user explicitly chooses **OpenClaw for an OpenAI model**, keep the model ref as `openai/<model>` and set provider/model runtime policy to `agentRuntime.id: "openclaw"` (a selected `openai` OAuth profile is routed internally through OpenClaw's Codex-auth transport); (4) if legacy config still contains **legacy Codex model refs**, repair it to `openai/<model>` with `openclaw doctor --fix` — doctor keeps the Codex auth route by adding provider/model-scoped `agentRuntime.id: "codex"` where the old model ref implied it, and legacy **`codex-cli/*` model refs** repair to the same `openai/<model>` Codex app-server route because OpenClaw no longer keeps a bundled Codex CLI backend; (5) if the user explicitly says **ACP**, **acpx**, or **Codex ACP adapter**, use ACP with `runtime: "acp"` and `agentId: "codex"`; (6) if the request is for **Claude Code, Gemini CLI, OpenCode, Cursor, Droid, or another external harness**, use ACP/acpx, not the native sub-agent runtime. The page summarizes the intent-to-config mapping:

| You mean... | Use... |
|---|---|
| Codex app-server chat/thread control | `/codex ...` from the bundled `codex` plugin |
| Codex app-server embedded agent runtime | `openai/*` agent model refs |
| OpenAI Codex OAuth | `openai` OAuth profiles |
| Claude Code or other external harness | ACP/acpx |

## Runtime Ownership

Different runtimes own different amounts of the loop. The page contrasts the OpenClaw embedded runner against the Codex app-server across each surface:

| Surface | OpenClaw embedded | Codex app-server |
|---|---|---|
| Model loop owner | OpenClaw through the OpenClaw embedded runner | Codex app-server |
| Canonical thread state | OpenClaw transcript | Codex thread, plus OpenClaw transcript mirror |
| OpenClaw dynamic tools | Native OpenClaw tool loop | Bridged through the Codex adapter |
| Native shell and file tools | OpenClaw path | Codex-native tools, bridged through native hooks where supported |
| Context engine | Native OpenClaw context assembly | OpenClaw projects assembled context into the Codex turn |
| Compaction | OpenClaw or selected context engine | Codex-native compaction, with OpenClaw notifications and mirror maintenance |
| Channel delivery | OpenClaw | OpenClaw |

This ownership split is the main design rule: if OpenClaw owns the surface it can provide normal plugin hook behavior; if the native runtime owns the surface, OpenClaw needs runtime events or native hooks; and if the native runtime owns canonical thread state, OpenClaw should mirror and project context, not rewrite unsupported internals.

## Runtime Selection (Precedence)

OpenClaw chooses an embedded runtime **after** provider and model resolution, following a fixed precedence: (1) **model-scoped runtime policy wins** — this can live in a configured provider model entry or in `agents.defaults.models["provider/model"].agentRuntime` / `agents.list[].models["provider/model"].agentRuntime`, and a provider wildcard such as `agents.defaults.models["vllm/*"].agentRuntime` applies after exact model policy so dynamically discovered provider models can share one runtime without overriding exact per-model exceptions; (2) **provider-scoped runtime policy** comes next at `models.providers.<provider>.agentRuntime`; (3) in `auto` mode, registered plugin runtimes can claim supported provider/model pairs; (4) if no runtime claims a turn in `auto` mode, OpenClaw uses `openclaw` as the compatibility runtime (use an explicit runtime id when the run must be strict).

Whole-session and whole-agent runtime pins are ignored. That includes `OPENCLAW_AGENT_RUNTIME`, session `agentHarnessId`/`agentRuntimeOverride` state, `agents.defaults.agentRuntime`, and `agents.list[].agentRuntime`. Run `openclaw doctor --fix` to remove stale whole-agent runtime config and convert legacy runtime model refs where OpenClaw can preserve the intent. Explicit provider/model plugin runtimes **fail closed**: for example, `agentRuntime.id: "codex"` on a provider or model means Codex or a clear selection/runtime error; it is never silently routed back to OpenClaw. CLI backend aliases are different from embedded harness ids — the preferred Claude CLI form is:

```json5
{
  agents: {
    defaults: {
      model: "anthropic/claude-opus-4-8",
      models: {
        "anthropic/claude-opus-4-8": {
          agentRuntime: { id: "claude-cli" },
        },
      },
    },
  },
}
```

Legacy refs such as `claude-cli/claude-opus-4-7` remain supported for compatibility, but new config should keep the provider/model canonical and put the execution backend in provider/model runtime policy. Legacy `codex-cli/*` refs are different: doctor migrates them to `openai/*` so they run through the Codex app-server harness instead of preserving a Codex CLI backend. `auto` mode is intentionally conservative for most providers — OpenAI agent models are the exception: unset runtime and `auto` both resolve to the Codex harness. Explicit OpenClaw runtime config remains an opt-in compatibility route for `openai/*` agent turns; when paired with a selected `openai` OAuth profile, OpenClaw routes that path internally through the Codex-auth transport while keeping the public model ref as `openai/*`. Stale OpenAI runtime session pins are ignored by runtime selection and can be cleaned with `openclaw doctor --fix`.

## GitHub Copilot Agent Runtime

The external `@openclaw/copilot` plugin registers an opt-in `copilot` runtime backed by the GitHub Copilot CLI (`@github/copilot-sdk`). It claims the canonical subscription `github-copilot` provider and is **never** selected by `auto`. Opt in per-model or per-provider via `agentRuntime.id`:

```json5
{
  agents: {
    defaults: {
      model: "github-copilot/gpt-5.5",
      models: {
        "github-copilot/gpt-5.5": {
          agentRuntime: { id: "copilot" },
        },
      },
    },
  },
}
```

The harness claims its provider, runtime, CLI session key, and auth profile prefix in `extensions/copilot/doctor-contract-api.ts`, which `openclaw doctor` auto-loads. Configuration, auth, transcript mirroring, compaction, the doctor probe surface, and the broader PI vs Codex vs Copilot SDK decision are documented on the GitHub Copilot agent runtime page.

## Compatibility Contract

When a runtime is not OpenClaw, it should document which OpenClaw surfaces it supports. The page prescribes this questionnaire shape:

| Question | Why it matters |
|---|---|
| Who owns the model loop? | Determines where retries, tool continuation, and final answer decisions happen. |
| Who owns canonical thread history? | Determines whether OpenClaw can edit history or only mirror it. |
| Do OpenClaw dynamic tools work? | Messaging, sessions, cron, and OpenClaw-owned tools rely on this. |
| Do dynamic tool hooks work? | Plugins expect `before_tool_call`, `after_tool_call`, and middleware around OpenClaw-owned tools. |
| Do native tool hooks work? | Shell, patch, and runtime-owned tools need native hook support for policy and observation. |
| Does the context engine lifecycle run? | Memory and context plugins depend on assemble, ingest, after-turn, and compaction lifecycle. |
| What compaction data is exposed? | Some plugins only need notifications, while others need kept/dropped metadata. |
| What is intentionally unsupported? | Users should not assume OpenClaw equivalence where the native runtime owns more state. |

The Codex runtime support contract is documented separately under the Codex harness runtime page (its `#v1-support-contract` section).

## Status Labels

Status output may show both `Execution` and `Runtime` labels; read them as diagnostics, not provider names. A model ref such as `openai/gpt-5.5` tells you the selected provider/model, a runtime id such as `codex` tells you which loop is executing the turn, and a channel label such as Telegram or Discord tells you where the conversation is happening. If a run still shows an unexpected runtime, inspect the selected provider/model runtime policy first — legacy session runtime pins no longer decide routing.

## Related Notes

**Terms**

- **[Agent Harness](../../term_dictionary/term_agent_harness.md)** — harness providing a runtime; relevance: this page defines harness vs runtime.
- **[ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md)** — external agent control plane; relevance: the ACP/acpx adapter path for Codex/Claude Code/external harnesses.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — coding agents; relevance: the runtime families (openclaw/codex/copilot/claude-cli) ARE coding agents.
- **[Claude Code](../../term_dictionary/term_claude_code.md)** — Anthropic coding agent; relevance: claude-cli CLI-backend + Claude Code via ACP.
- **[Model Router](../../term_dictionary/term_model_router.md)** — model/runtime selection; relevance: the runtime-selection precedence order this page specifies.
- **[Provider Plugin](../../term_dictionary/term_provider_plugin.md)** — pluggable provider; relevance: provider vs model vs runtime layer distinction.
- **[LLM](../../term_dictionary/term_llm.md)** — large language model; relevance: the model layer the runtime executes.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — gateway product; relevance: `openclaw` is the default embedded runtime.
- **[Pi Agent](../../term_dictionary/term_pi_agent.md)** — Pi coding agent; relevance: PI vs Codex vs Copilot runtime decision referenced here.

**Docs**

- **[oc_concepts_agent](oc_concepts_agent.md)** — embedded runtime contract (planned, this series); relevance: the `openclaw` embedded runtime this taxonomy names.
- **[oc_concepts_agent_loop](oc_concepts_agent_loop.md)** — loop (planned, this series); relevance: the loop a runtime owns.
- **[oc_concepts_model_providers](oc_concepts_model_providers_official.md)** — model providers (planned, co04); relevance: the provider layer disambiguated from runtime.
- **[oc_concepts_models](oc_concepts_models_selection.md)** — models (planned, co04); relevance: the model layer.
- **[oc_concepts_model_failover](oc_concepts_model_failover_auth_rotation.md)** — model failover (planned, co04); relevance: runtime selection interacts with fallback.
- **[hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md)** — Hermes provider runtime; relevance: provider/runtime layering in the OpenClaw-lineage fork.
- **[hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md)** — Hermes Codex runtime; relevance: Codex app-server harness setup analog.
- **[cc_agent_sdk_compare_to_other_tools](../claude_code/cc_agent_sdk_compare_to_other_tools.md)** — Claude SDK vs other tools; relevance: cross-harness comparison framing.
- **[pi_overview](../pi/pi_overview.md)** — Pi harness overview; relevance: the PI runtime in the PI/Codex/Copilot decision.
- **[band_acp_overview](../band/band_acp_overview.md)** — Band ACP; relevance: ACP control-plane analog for external harnesses.
- **[band_adapter_codex](../band/band_adapter_codex.md)** — Band Codex adapter; relevance: Codex-runtime adapter counterpart.
- **[band_coding_agents_deployment](../band/band_coding_agents_deployment.md)** — coding-agent deployment; relevance: cross-platform runtime/harness deployment model.

**Repos**

- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — embedded runtime + harness selection; relevance: AgentHarness selection + runtime registry.
- **[repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md)** — Hermes agent core; relevance: sibling-fork runtime/harness core.

**Snippets**

- **[snippet_openclaw_acp_runtime_contract](../../code_snippets/snippet_openclaw_acp_runtime_contract.md)** — ACP runtime contract; relevance: the external-runtime contract this page describes.
- **[snippet_openclaw_acp_manager_runtime_register](../../code_snippets/snippet_openclaw_acp_manager_runtime_register.md)** — runtime register; relevance: how plugin runtimes claim provider/model pairs.
- **[snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md)** — runtime config; relevance: `agentRuntime.id` model/provider-scoped policy.
- **[snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md)** — fallback ladder; relevance: runtime selection in auto mode + fallback.
- **[snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md)** — ACP sub-agent spawn; relevance: spawning external harnesses via ACP.
- **[snippet_openclaw_acp_manager_controls_apply](../../code_snippets/snippet_openclaw_acp_manager_controls_apply.md)** — ACP controls; relevance: bind/resume/steer/stop control surface (Codex).
- **[snippet_openclaw_acp_spawn_policy](../../code_snippets/snippet_openclaw_acp_spawn_policy.md)** — ACP spawn policy; relevance: when ACP is used vs native runtime.
- **[snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md)** — ACP session init; relevance: ACP adapter session handshake.
- **[snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md)** — external-CLI auth; relevance: claude-cli/Codex OAuth auth profiles.
- **[snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md)** — OpenAI provider; relevance: `openai/*` model refs routed to the Codex runtime.
- **[snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md)** — Anthropic provider; relevance: anthropic model + claude-cli backend example.
- **[snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md)** — model discovery; relevance: provider model discovery feeding runtime selection.

## References

- [OpenClaw Docs — Agent runtimes](https://docs.openclaw.ai/concepts/agent-runtimes)
- [OpenClaw Docs — Codex harness](https://docs.openclaw.ai/plugins/codex-harness)
- [OpenClaw Docs — Codex harness runtime (v1 support contract)](https://docs.openclaw.ai/plugins/codex-harness-runtime#v1-support-contract)
- [OpenClaw Docs — GitHub Copilot agent runtime](https://docs.openclaw.ai/plugins/copilot)
- [OpenClaw Docs — OpenAI](https://docs.openclaw.ai/providers/openai)
- [OpenClaw Docs — Agent harness plugins](https://docs.openclaw.ai/plugins/sdk-agent-harness)
- [OpenClaw Docs — Model providers](https://docs.openclaw.ai/concepts/model-providers)
- [OpenClaw Docs — Agent loop](https://docs.openclaw.ai/concepts/agent-loop)
- [OpenClaw Docs — Models](https://docs.openclaw.ai/concepts/models)
- [OpenClaw Docs — Status](https://docs.openclaw.ai/cli/status)

**Source**: OpenClaw documentation — `concepts/agent-runtimes` (mirror `inbox/openclaw_docs/concepts/agent-runtimes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
