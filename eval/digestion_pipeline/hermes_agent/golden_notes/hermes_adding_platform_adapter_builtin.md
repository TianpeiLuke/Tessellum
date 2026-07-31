---
tags:
  - resource
  - documentation
  - hermes_agent
  - gateway
  - platform_adapter
keywords:
  - built-in platform adapter
  - Platform enum gateway/config.py
  - BasePlatformAdapter subclass
  - gateway runner _create_adapter
  - 20+ file checklist
  - parity audit
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters
access_control_group: ["general"]
---

# Adding a Platform Adapter — Built-in (Core) Path

## Overview

This is the **core-contributor procedure** for adding a messaging platform directly into the Hermes Agent codebase — the path used for officially supported platforms (Telegram, Discord, Slack, WeCom, etc.) rather than community drop-in plugins. Where the [plugin path](hermes_adding_platform_adapter_plugin.md) drops a directory into `~/.hermes/plugins/` with zero core changes, the built-in path touches **20+ files** across gateway code, config, CLI, tools, toolsets, the prompt builder, tests, and an 8-file documentation set. Every adapter — plugin or built-in — extends `BasePlatformAdapter` from `gateway/platforms/base.py` and implements `connect()` / `disconnect()` / `send()`, forwarding inbound messages via `self.handle_message(event)` into the gateway runner that hands off to `AIAgent`.

The page frames the built-in path as an explicit **11-step checklist**: add the `Platform` enum member, create the adapter file, wire three `gateway/config.py` touchpoints and six `gateway/run.py` runner touchpoints, register cross-platform + cron delivery, integrate six `hermes_cli/*` modules, register the send/cronjob tools and the per-platform toolset, add an optional `_PLATFORM_HINTS` entry, write tests, and update eight docs files. It closes with a **parity audit** (search-files diff against an established platform to catch missed touchpoints), three **common transport patterns** (long-poll, callback/webhook, token locks), and a **reference-implementation table** mapping established adapters to the patterns they exemplify.

Because the built-in path is a contributor discipline rather than an everyday task, the recommendation is unambiguous: community / third-party platforms should use the plugin path; only core-supported platforms justify editing 20+ files. The architecture the runner, config bridge, cron scheduler, CLI, prompt builder, and tools implement is documented in the gateway-internals notes; this note is the *authoring checklist* on top of that runtime.

## Architecture Overview

Every adapter sits in a fixed inbound/outbound chain: `User ↔ Messaging Platform ↔ Platform Adapter ↔ Gateway Runner ↔ AIAgent`. The adapter extends `BasePlatformAdapter` and implements `connect()` (establish a WebSocket, long-poll, or HTTP-server connection — abstract), `disconnect()` (clean shutdown — abstract), and `send()` (send text to a chat — abstract), with `send_typing()` and `get_chat_info()` as optional overrides. Inbound messages are received by the adapter and forwarded via `self.handle_message(event)`, which the base class routes to the gateway runner. The built-in checklist below is what wires a new subclass of this contract into every place core Hermes enumerates or dispatches platforms.

## Step-by-Step Checklist (Built-in Path)

> This checklist is for adding a platform directly to the Hermes core codebase — typically done by core contributors for officially supported platforms. Community/third-party platforms should use the [plugin path](hermes_adding_platform_adapter_plugin.md).

**1. Platform Enum** — add your platform to the `Platform` enum in `gateway/config.py`:

```python
class Platform(str, Enum):
    # ... existing platforms ...
    NEWPLAT = "newplat"
```

**2. Adapter File** — create `gateway/platforms/newplat.py` with a `check_newplat_requirements()` dependency probe and a `NewPlatAdapter(BasePlatformAdapter)` subclass implementing `connect`/`disconnect`/`send`/`get_chat_info`:

```python
from gateway.config import Platform, PlatformConfig
from gateway.platforms.base import (
    BasePlatformAdapter, MessageEvent, MessageType, SendResult,
)

def check_newplat_requirements() -> bool:
    """Return True if dependencies are available."""
    return SOME_SDK_AVAILABLE

class NewPlatAdapter(BasePlatformAdapter):
    def __init__(self, config: PlatformConfig):
        super().__init__(config, Platform.NEWPLAT)
        # Read config from config.extra dict
        extra = config.extra or {}
        self._api_key = extra.get("api_key") or os.getenv("NEWPLAT_API_KEY", "")

    async def connect(self) -> bool:
        # Set up connection, start polling/webhook
        self._mark_connected()
        return True

    async def disconnect(self) -> None:
        self._running = False
        self._mark_disconnected()

    async def send(self, chat_id, content, reply_to=None, metadata=None):
        # Send message via platform API
        return SendResult(success=True, message_id="...")

    async def get_chat_info(self, chat_id):
        return {"name": chat_id, "type": "dm"}
```

For inbound messages, build a `MessageEvent` (via `self.build_source(...)`) and call `self.handle_message(event)`.

**3. Gateway Config (`gateway/config.py`)** — three touchpoints: add a credential check to `get_connected_platforms()`; add the token env-map entry `Platform.NEWPLAT: "NEWPLAT_TOKEN"` in `load_gateway_config()`; and map all `NEWPLAT_*` env vars in `_apply_env_overrides()`.

**4. Gateway Runner (`gateway/run.py`)** — six touchpoints: an `elif platform == Platform.NEWPLAT:` branch in `_create_adapter()`; the `Platform.NEWPLAT: "NEWPLAT_ALLOWED_USERS"` and `Platform.NEWPLAT: "NEWPLAT_ALLOW_ALL_USERS"` entries in the `_is_user_authorized()` allowed-users / allow-all maps; the matching `"NEWPLAT_ALLOWED_USERS"` / `"NEWPLAT_ALLOW_ALL_USERS"` strings in the early `_any_allowlist` and `_allow_all` env tuples; and `Platform.NEWPLAT` in the `_UPDATE_ALLOWED_PLATFORMS` frozenset.

**5. Cross-Platform Delivery** — add `"newplat"` to the delivery-type tuple in `gateway/platforms/webhook.py`, and add the platform to the `_KNOWN_DELIVERY_PLATFORMS` frozenset plus the `_deliver_result()` platform map in `cron/scheduler.py`.

**6. CLI Integration** — six `hermes_cli/*` modules: add `NEWPLAT_*` vars to `_EXTRA_ENV_KEYS` in `config.py`; add a `_PLATFORMS` entry (key, label, emoji, token_var, setup_instructions, vars) in `gateway.py`; add a `PlatformInfo` entry (label, default_toolset for the `skills_config`/`tools_config` TUIs) in `platforms.py`; add a `_setup_newplat()` function and a messaging-platforms tuple in `setup.py`; add the detection entry `"NewPlat": ("NEWPLAT_TOKEN", "NEWPLAT_HOME_CHANNEL")` in `status.py`; and add `"newplat": "NEWPLAT_TOKEN"` to the detection dict in `dump.py`.

**7. Tools** — add `"newplat": Platform.NEWPLAT` to the platform map in `tools/send_message_tool.py`, and add `newplat` to the delivery-target description string in `tools/cronjob_tools.py`.

**8. Toolsets** — in `toolsets.py`, add a `"hermes-newplat"` toolset definition with `_HERMES_CORE_TOOLS`, then add `"hermes-newplat"` to the `"hermes-gateway"` includes list.

**9. Optional: Platform Hints** — if the platform has rendering limits, add an entry to the `_PLATFORM_HINTS` dict in `agent/prompt_builder.py`; this injects platform-specific guidance into the system prompt. Only add a hint if the agent's behavior should differ on that platform:

```python
_PLATFORM_HINTS = {
    # ...
    "newplat": (
        "You are chatting via NewPlat. It supports markdown formatting "
        "but has a 4000-character message limit."
    ),
}
```

**10. Tests** — create `tests/gateway/test_newplat.py` covering adapter construction from config, message-event building, the send method (mock the external API), and any platform-specific features (encryption, routing, etc.).

**11. Documentation** — update the eight-file doc set:

| File | What to add |
|------|-------------|
| `website/docs/user-guide/messaging/newplat.md` | Full platform setup page |
| `website/docs/user-guide/messaging/index.md` | Platform comparison table, architecture diagram, toolsets table, security section, next-steps link |
| `website/docs/reference/environment-variables.md` | All NEWPLAT_* env vars |
| `website/docs/reference/toolsets-reference.md` | hermes-newplat toolset |
| `website/docs/integrations/index.md` | Platform link |
| `website/sidebars.ts` | Sidebar entry for the docs page |
| `website/docs/developer-guide/architecture.md` | Adapter count + listing |
| `website/docs/developer-guide/gateway-internals.md` | Adapter file listing |

## Parity Audit

Before marking a new-platform PR complete, run a parity audit against an established platform — search every file mentioning the reference platform, then every file mentioning the new platform; any file in the first set but not the second is a potential gap:

```bash
# Find every .py file mentioning the reference platform
search_files "bluebubbles" output_mode="files_only" file_glob="*.py"

# Find every .py file mentioning the new platform
search_files "newplat" output_mode="files_only" file_glob="*.py"

# Any file in the first set but not the second is a potential gap
```

Repeat for `.md` and `.ts` files. Investigate each gap — is it a platform enumeration (needs updating) or a platform-specific reference (skip)? The parity audit is the modularity discipline that backstops the 20+-file checklist: it catches the touchpoint you forgot to mirror.

## Common Patterns

**Long-Poll Adapters** — for platforms like Telegram or Weixin, run a polling-loop task started from `connect()`:

```python
async def connect(self):
    self._poll_task = asyncio.create_task(self._poll_loop())
    self._mark_connected()

async def _poll_loop(self):
    while self._running:
        messages = await self._fetch_updates()
        for msg in messages:
            await self.handle_message(self._build_event(msg))
```

**Callback/Webhook Adapters** — if the platform pushes messages to your endpoint (e.g. WeCom Callback), run an HTTP server inside `connect()` and acknowledge inbound requests immediately, queuing the event for asynchronous handling. For platforms with tight response deadlines (e.g. WeCom's 5-second limit), always acknowledge immediately and deliver the agent's reply proactively via API later — agent sessions run 3–30 minutes, so inline replies within a callback response window are not feasible.

**Token Locks** — if the adapter holds a persistent connection with a unique credential, acquire a scoped lock in `connect()` (and release it in `disconnect()`) so two profiles never share the same credential:

```python
from gateway.status import acquire_scoped_lock, release_scoped_lock

async def connect(self):
    if not acquire_scoped_lock("newplat", self._token):
        logger.error("Token already in use by another profile")
        return False
    # ... connect

async def disconnect(self):
    release_scoped_lock("newplat", self._token)
```

## Reference Implementations

Mirror an established adapter that matches your transport pattern:

| Adapter | Pattern | Complexity | Good reference for |
|---------|---------|------------|-------------------|
| `bluebubbles.py` | REST + webhook | Medium | Simple REST API integration |
| `weixin.py` | Long-poll + CDN | High | Media handling, encryption |
| `wecom_callback.py` | Callback/webhook | Medium | HTTP server, AES crypto, multi-app |
| `telegram.py` | Long-poll + Bot API | High | Full-featured adapter with groups, threads |

**Source**: `inbox/hermes_agent_docs/developer-guide/adding-platform-adapters.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters
**Last Updated**: 2026-06-19
**Status**: Active
