---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugins
  - llm_access
keywords:
  - ctx.llm plugin lane
  - complete and complete_structured
  - PluginLlm host-owned credentials
  - fail-closed trust gate
  - PluginLlmTrustError override gating
  - structured output json_schema
topics:
  - Hermes Agent
  - Plugin System
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access
access_control_group: ["general"]
---

# Hermes Agent — Plugin LLM Access (`ctx.llm`)

## Overview

`ctx.llm` is the supported way for a Hermes plugin to make a one-shot LLM call from *outside* the agent's conversation — chat or structured, sync or async, with or without images, all behind the same surface, the same trust gate, and the same host-owned credentials. It exists for the plugin jobs the agent shouldn't be in the loop on: a hook that rewrites a tool error into something a non-engineer can read, a gateway adapter that translates an inbound message before queuing, a slash command that summarises a long paste, a scheduled job that scores yesterday's activity, or a pre-filter that decides whether a message is even worth waking the agent for. These want one LLM call, a typed answer, and to be done.

As a **subsystem-behavior model**, the lane has four shapes — `complete()`, `complete_structured()`, and their async twins `acomplete()` / `acomplete_structured()` — all sharing arguments and result objects. The *host* owns everything risky: provider resolution, auth (OAuth tokens, refresh flows, the credential pool), vision routing, the fallback chain, timeouts, JSON shaping, schema validation, and the audit log. The *plugin* owns only the request shape, its schema, error handling, and token cost. Guarding all of it is a **fail-closed trust gate**: with no config, a plugin runs only against the user's active provider and model; `provider=`, `model=`, `agent_id=`, and `profile=` overrides each raise `PluginLlmTrustError` until an operator independently opts in via `plugins.entries`. Under the hood it runs on the same auxiliary client documented in [Provider Runtime](hermes_provider_runtime.md).

## The smallest possible call

```python
result = ctx.llm.complete(messages=[{"role": "user", "content": "ping"}])
return result.text
```

That is the whole API in one line — no keys, no provider config, no SDK initialisation. The plugin runs against whatever provider and model the user is currently using; when they switch providers, the plugin follows them automatically. A more complete chat call adds a system message plus request-shaping arguments, and a `purpose` audit string that surfaces in `agent.log` and `result.audit` so operators can see which plugin made which call (optional but recommended for anything that fires often).

## Structured output

When the plugin needs a typed answer, it switches to the structured lane:

```python
result = ctx.llm.complete_structured(
    instructions="Score this support reply for urgency (0–1) and pick a category.",
    input=[{"type": "text", "text": message_body}],
    json_schema=TRIAGE_SCHEMA,
    purpose="support.triage",
    temperature=0.0,
    max_tokens=128,
)

if result.parsed["urgency"] > 0.8:
    await dispatch_to_oncall(result.parsed["category"], message_body)
```

The host requests JSON output from the provider, parses it locally as a fallback, validates against your schema if `jsonschema` is installed, and hands back a Python object on `result.parsed`. If the model couldn't produce valid JSON, `result.parsed` is `None` and `result.text` carries the raw response.

## What this lane gives you

The lane's value is four properties. **One call, four shapes** — `complete()` / `complete_structured()` / `acomplete()` / `acomplete_structured()`, all sharing arguments and result objects. **Host-owned credentials** — OAuth tokens, refresh flows, the credential pool, and per-task aux overrides all apply; the plugin never sees a token, and the host attributes the call through `result.audit`. **Bounded** — a single sync/async call, no streaming, no tool loops, no conversation state. **Fail-closed trust** — an unconfigured plugin cannot pick its own provider, model, agent, or stored credential; the default is "use what the user is using," and operators opt in to overrides per plugin in `config.yaml`.

## Quick start

Two complete plugins ship inside a single `register(ctx)` function and need zero outside configuration to run against whatever model the user has active. The chat plugin `/tldr` registers a command whose handler calls `ctx.llm.complete(...)` with a summarise system prompt and returns `result.text`; `result.usage` carries token counts and `result.provider` / `result.model` carry attribution. The structured plugin `/paste-to-tasks` registers a command that calls `complete_structured(instructions=..., input=[{"type": "text", "text": raw_args}], json_schema=_TASKS_SCHEMA, schema_name="meeting.tasks", ...)`, then formats `result.parsed["tasks"]` (or returns the raw `result.text` when `result.parsed is None`). A third worked example with image input lives in the companion `hermes-example-plugins` repo (`plugin-llm-example`), and an async example using `asyncio.gather()` lives in `plugin-llm-async-example` in the same repo.

## When to use which

Provider selection, model resolution, auth, fallback, timeout, and vision routing are identical across all four methods; only the shape differs:

- Free-form text response (translation, summary, rewrite, generation) → `complete()`.
- Multi-turn prompt (system + few-shot examples + user) → `complete()`.
- A typed dict back, validated against a schema → `complete_structured()`.
- Image-or-text input with a typed dict back → `complete_structured()`.
- The same call from async code (gateway adapters, async hooks) → `acomplete()` / `acomplete_structured()`.

## API surface

`ctx.llm` is an instance of `agent.plugin_llm.PluginLlm`. The two primary methods are `complete()` and `complete_structured()`, each with sync and async forms.

```python
result = ctx.llm.complete(
    messages=[{"role": "user", "content": "Hi"}],
    provider=None,         # optional, gated — Hermes provider id (e.g. "openrouter")
    model=None,            # optional, gated — whatever string that provider expects
    temperature=None,
    max_tokens=None,
    timeout=None,          # seconds
    agent_id=None,         # optional, gated
    profile=None,          # optional, gated — explicit auth-profile name
    purpose="optional-audit-string",
)
# → PluginLlmCompleteResult(text, provider, model, agent_id, usage, audit)
```

`messages` is the standard OpenAI shape — a list of `{"role": "...", "content": "..."}` dicts — so multi-turn prompts work exactly as with the OpenAI SDK. `provider=` and `model=` are independent and follow the host's main config shape (`model.provider` + `model.model`): set just `model=` to use the user's active provider with a different model, set both to switch providers entirely; either without operator opt-in raises `PluginLlmTrustError`.

`complete_structured()` takes `instructions` plus typed `input` blocks (`{"type": "text", ...}` or `{"type": "image", "data"/"url": ...}` — raw bytes are base64-encoded as a `data:` URL automatically), an optional `json_schema` (triggers parsed result + validation), `json_mode=False` (set `True` without a schema to ask for JSON anyway), and an optional `schema_name`. When `result.content_type == "json"`, `result.parsed` matches your schema; when `== "text"`, parsing or validation failed and `result.text` holds the raw response. The async forms (`acomplete` / `acomplete_structured`) share arguments and result types with their sync counterparts.

### Result attributes

```python
@dataclass
class PluginLlmCompleteResult:
    text: str                    # the assistant's response
    provider: str                # e.g. "openrouter", "anthropic"
    model: str                   # whatever the provider returned for this call
    agent_id: str                # whose model/auth was used
    usage: PluginLlmUsage        # tokens + cache + cost estimate
    audit: Dict[str, Any]        # plugin_id, purpose, profile

@dataclass
class PluginLlmStructuredResult(PluginLlmCompleteResult):
    parsed: Optional[Any]        # JSON object when content_type == "json"
    content_type: str            # "json" or "text"
    # audit also carries schema_name when supplied
```

`usage` carries `input_tokens`, `output_tokens`, `total_tokens`, `cache_read_tokens`, `cache_write_tokens`, and `cost_usd` when the provider returns those fields.

## Trust gate

The default behaviour is fail-closed. With no `plugins.entries` config block, a plugin can run any of the four methods against the user's active provider and model, and set request-shaping arguments (`temperature`, `max_tokens`, `timeout`, `system_prompt`, `purpose`, `messages`, `instructions`, `input`, `json_schema`) — and that is it. `provider=`, `model=`, `agent_id=`, and `profile=` raise `PluginLlmTrustError` until an operator opts in. Most plugins never need this: a plugin that just calls `ctx.llm.complete(messages=...)` runs zero-config against whatever the user has active. The opt-in block pins a plugin to a different model/provider:

```yaml
plugins:
  entries:
    my-plugin:
      llm:
        allow_provider_override: true     # choose a different known Hermes provider
        allowed_providers:                # optionally restrict; ["*"] for any
          - openrouter
          - anthropic
        allow_model_override: true        # ask for a specific model
        allowed_models:                   # matched literally; ["*"] for any
          - openai/gpt-4o-mini
          - anthropic/claude-3-5-haiku
        allow_agent_id_override: false    # cross-agent calls (rare)
        allow_profile_override: false     # request a specific stored auth profile
```

The plugin id is the manifest `name:` field for flat plugins, or the path-derived key for nested plugins (`image_gen/openai`, `memory/honcho`). Each override is **independently gated** — granting `allow_model_override` does *not* also grant `allow_provider_override`:

| Override        | Default | Config key                       |
| --------------- | ------- | -------------------------------- |
| `provider=`     | denied  | `allow_provider_override: true`  |
| ↳ allowlist     | —       | `allowed_providers: [...]`       |
| `model=`        | denied  | `allow_model_override: true`     |
| ↳ allowlist     | —       | `allowed_models: [...]`          |
| `agent_id=`     | denied  | `allow_agent_id_override: true`  |
| `profile=`      | denied  | `allow_profile_override: true`   |

The gate does **not** need to enforce request-shaping arguments (`temperature`, `max_tokens`, `timeout`, `system_prompt`, `purpose`, `messages`, `instructions`, `input`, `json_schema`, `schema_name`, `json_mode`) — they pick neither credentials nor routes and are always allowed. The default-deny posture still lets an unconfigured plugin do useful work against the active provider and model; operators only think about `plugins.entries` for plugins that want finer routing.

## What the host owns vs the plugin owns

What `ctx.llm` does so the plugin doesn't have to: **provider resolution** (`model.provider` + `model.model`, or trusted overrides); **auth** (API keys, OAuth/refresh tokens from `~/.hermes/auth.json` / env, plus the credential pool — the plugin never sees them); **vision routing** (falls back to the configured vision model when image input meets a text-only active model); **fallback chain** (the usual aggregator-aware fallback on 5xx/429); **timeout** (honours `timeout=`, else `auxiliary.<task>.timeout` or the global aux default); **JSON shaping** (sends `response_format`, re-parses locally from a code-fenced response); **schema validation** (against `json_schema` when `jsonschema` is installed, else skips with a debug line); and the **audit log** (one INFO line per call to `agent.log` with plugin id, provider/model, purpose, token totals).

The plugin owns: the **request shape** (`messages` for chat, `instructions` + `input` for structured — it builds the prompt, the host runs it); the **schema** (the host doesn't infer it); **error handling** (`complete_structured()` raises `ValueError` on empty inputs and validation failure, `PluginLlmTrustError` on a denied override, and anything else — provider 5xx, no credentials, timeout — raises whatever `auxiliary_client.call_llm()` raises); and **cost** (every call hits the user's paid provider, so don't loop `complete()` on every gateway message).

## Where this fits in the plugin surface

Existing `ctx.register_*` methods each extend a Hermes subsystem — `register_tool` adds an agent-callable tool, `register_platform` wires a gateway adapter, `register_image_gen_provider` replaces an image-gen backend, `register_memory_provider` the memory backend, `register_context_engine` the context compressor, and `register_hook` observes a lifecycle event. `ctx.llm` is the first surface that lets a plugin run *the same model the user is talking to, out of band*, without registering anything — that is its only job. Need a tool the agent invokes? `register_tool`. React to a lifecycle event? `register_hook`. Make its own model call, structured or not? `ctx.llm`.

**Source**: https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access
**Last Updated**: 2026-06-19
**Status**: Active
