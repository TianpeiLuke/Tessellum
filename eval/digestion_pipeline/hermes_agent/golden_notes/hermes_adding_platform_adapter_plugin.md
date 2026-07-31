---
tags:
  - resource
  - documentation
  - hermes_agent
  - developer_guide
  - messaging
keywords:
  - platform adapter plugin
  - BasePlatformAdapter
  - register_platform
  - plugin.yaml manifest
  - env-driven auto-configuration
  - standalone_sender_fn cron delivery
  - slow-LLM keep_typing override
topics:
  - Hermes Agent
  - Developer Guide
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters
access_control_group: ["general"]
---

# Adding a Platform Adapter — Plugin Path

## Overview

This is the **recommended path for adding a new messaging platform to Hermes** (Telegram-, Discord-, WeCom-style services that let users talk to the agent through an external chat). A platform adapter is a plugin directory dropped into `~/.hermes/plugins/` with **zero core code changes** — the opposite of the built-in path, which touches 20+ files (sibling note `hermes_adding_platform_adapter_builtin`).

The data flow is `User ↔ Messaging Platform ↔ Platform Adapter ↔ Gateway Runner ↔ AIAgent`. Every adapter subclasses `BasePlatformAdapter` from `gateway/platforms/base.py` and implements the abstract contract: `connect()` (open a WebSocket / long-poll / HTTP-server connection), `disconnect()`, and `send()`; `send_typing()` and `get_chat_info()` are optional overrides. Inbound messages are forwarded via `self.handle_message(event)`, which the base class routes to the gateway runner. A single `register(ctx)` entry point wires the adapter into roughly **20 integration points automatically** (adapter creation, config parsing, authorization, cron delivery, CLI menus, prompt hints, chunking), so the plugin author writes only platform-specific I/O.

The sections below follow the source's plugin-path arc: the two-file layout, what `register_platform()` handles for free, env-driven auto-config + the YAML→env bridge, cron delivery (incl. out-of-process `standalone_sender_fn`), surfacing env vars in `hermes config`, and the slow-LLM UX overrides (`_keep_typing` / `send`) for hard-time-window platforms like LINE.

## Architecture Overview

The flow is `User ↔ Messaging Platform ↔ Platform Adapter ↔ Gateway Runner ↔ AIAgent`. `BasePlatformAdapter` defines three abstract methods every adapter implements — `connect()`, `disconnect()`, `send()` — plus optional `send_typing()` and `get_chat_info()` overrides. Inbound traffic flows back up through `self.handle_message(event)`, which the base routes to the runner; the adapter never talks to the `AIAgent` directly.

## Plugin Path (Recommended)

The plugin is a directory with two files — `plugin.yaml` (metadata) and `adapter.py` (the adapter class plus the `register()` entry point):

```
~/.hermes/plugins/my-platform/
  plugin.yaml      # Plugin metadata
  adapter.py       # Adapter class + register() entry point
```

**`plugin.yaml`** declares `name`, `label`, `kind: platform`, `version`, `description`, `author`, and `requires_env` / `optional_env` blocks. Each env entry is a bare string (`- MY_PLATFORM_TOKEN`) or a rich dict (`name`, `description`, `prompt`, `password`) for better setup-UI text; these blocks auto-populate `hermes config` (see [Surfacing Env Vars](#surfacing-env-vars-in-hermes-config)).

**`adapter.py`** subclasses `BasePlatformAdapter`, reads its token from env-or-`config.extra`, and exposes the `register(ctx)` entry point the plugin system calls:

```python
import os
from gateway.platforms.base import (
    BasePlatformAdapter, SendResult, MessageEvent, MessageType,
)
from gateway.config import Platform, PlatformConfig


class MyPlatformAdapter(BasePlatformAdapter):
    def __init__(self, config: PlatformConfig):
        super().__init__(config, Platform("my_platform"))
        extra = config.extra or {}
        self.token = os.getenv("MY_PLATFORM_TOKEN") or extra.get("token", "")

    async def connect(self) -> bool:
        # Connect to the platform API, start listeners
        self._mark_connected()
        return True

    async def disconnect(self) -> None:
        self._mark_disconnected()

    async def send(self, chat_id, content, reply_to=None, metadata=None):
        return SendResult(success=True, message_id="...")

    async def get_chat_info(self, chat_id):
        return {"name": chat_id, "type": "dm"}


def register(ctx):
    """Plugin entry point — called by the Hermes plugin system."""
    ctx.register_platform(
        name="my_platform",
        label="My Platform",
        adapter_factory=lambda cfg: MyPlatformAdapter(cfg),
        check_fn=check_requirements,        # deps available?
        validate_config=validate_config,    # minimally configured?
        required_env=["MY_PLATFORM_TOKEN"],
        install_hint="pip install my-platform-sdk",
        env_enablement_fn=_env_enablement,        # seed extras from env
        cron_deliver_env_var="MY_PLATFORM_HOME_CHANNEL",  # deliver= target
        allowed_users_env="MY_PLATFORM_ALLOWED_USERS",
        allow_all_env="MY_PLATFORM_ALLOW_ALL_USERS",
        max_message_length=4000,    # 0 = no limit (smart chunking)
        platform_hint="You are chatting via My Platform. It supports markdown.",
        emoji="💬",
    )
    # Optional: register platform-specific tools
    ctx.register_tool(name="my_platform_search", toolset="my_platform",
                      schema={...}, handler=my_search_handler)
```

`check_fn` returns `True` when SDK deps are importable; `validate_config` returns `True` when the platform is minimally configured. Users enable the platform in `config.yaml` under `gateway.platforms.my_platform` (`enabled: true` + an `extra` dict), or purely via env vars read in `__init__`.

## What the Plugin System Handles Automatically

Calling `ctx.register_platform()` wires ~20 integration points with no core edits — the registry is checked **before** the built-in if/elif chain, making a plugin platform a first-class peer of built-in platforms:

| Integration point | How it works |
|---|---|
| Gateway adapter creation | Registry checked before built-in if/elif chain |
| Config parsing | `Platform._missing_()` accepts any platform name |
| Connected-platform validation | Registry `validate_config()` called |
| User authorization | `allowed_users_env` / `allow_all_env` checked |
| Env-only auto-enable | `env_enablement_fn` seeds `PlatformConfig.extra` + `home_channel` |
| YAML config bridge | `apply_yaml_config_fn` translates `config.yaml` keys into env/extras |
| Cron delivery | `cron_deliver_env_var` makes `deliver=<name>` work |
| `hermes config` UI entries | `requires_env` / `optional_env` in `plugin.yaml` auto-populate |
| send_message tool | Routes through the live gateway adapter |
| Webhook cross-platform delivery | Registry checked for known platforms |
| `/update` command access | `allow_update_command` flag |
| Channel directory | Plugin platforms included in enumeration |
| System-prompt hints | `platform_hint` injected into LLM context |
| Message chunking | `max_message_length` for smart splitting |
| PII redaction | `pii_safe` flag |
| `hermes status` | Shows plugin platforms with `(plugin)` tag |
| `hermes gateway setup` | Plugin platforms appear in the setup menu |
| `hermes tools` / `hermes skills` | Plugin platforms in per-platform config |
| Token lock (multi-profile) | Use `acquire_scoped_lock()` in `connect()` |
| Orphaned-config warning | Descriptive log when a plugin is missing |

## Env-Driven Auto-Configuration

Most users configure a platform by dropping env vars into `~/.hermes/.env` rather than editing `config.yaml`. The `env_enablement_fn` hook lets the plugin pick those env vars up **before** the adapter is constructed, so `hermes gateway status`, `get_connected_platforms()`, and cron delivery see correct state without instantiating the SDK. It is called by the registry during `load_gateway_config()`; return `None` when the platform is not minimally configured (caller skips auto-enable), or a dict to seed extras. The special `home_channel` key becomes a `HomeChannel` dataclass on the `PlatformConfig`; every other key merges into `PlatformConfig.extra`.

```python
def _env_enablement() -> dict | None:
    """Seed PlatformConfig.extra from env vars (called during load_gateway_config())."""
    token = os.getenv("MY_PLATFORM_TOKEN", "").strip()
    channel = os.getenv("MY_PLATFORM_CHANNEL", "").strip()
    if not (token and channel):
        return None  # not minimally configured → skip auto-enable
    seed = {"token": token, "channel": channel}
    home = os.getenv("MY_PLATFORM_HOME_CHANNEL")
    if home:
        seed["home_channel"] = {
            "chat_id": home,
            "name": os.getenv("MY_PLATFORM_HOME_CHANNEL_NAME", "Home"),
        }
    return seed
```

## YAML→env Config Bridge

Some users prefer setting `config.yaml` keys (e.g. `my_platform.require_mention`, `my_platform.allowed_channels`) over env vars. The `apply_yaml_config_fn` hook lets the plugin own that translation instead of forcing core `gateway/config.py` to know the platform's YAML schema. It receives the full parsed `config.yaml` plus the platform's own sub-dict; it may mutate `os.environ` (use `not os.getenv(...)` guards to preserve **env > YAML** precedence) and/or return a dict merged into `PlatformConfig.extra`.

The hook runs during `load_gateway_config()` — **after** the generic shared-key loop (common keys like `reply_prefix`, `require_mention`) and **before** `_apply_env_overrides()` — so the plugin only bridges **platform-specific** keys. Exceptions are swallowed and logged at debug level, so a misbehaving plugin never aborts gateway config load.

## Cron Delivery

To let `deliver=my_platform` cron jobs route to a configured home channel, set `cron_deliver_env_var` to the env-var name holding the default chat/room/channel ID. The scheduler reads it when resolving the home target and treats the platform as a valid cron target (`_KNOWN_DELIVERY_PLATFORMS`-style checks). A `home_channel` dict seeded by `env_enablement_fn` takes precedence; `cron_deliver_env_var` is the fallback for jobs running before env seeding.

### Out-of-process cron delivery

`cron_deliver_env_var` makes the platform a recognized `deliver=` target, but the actual send must still succeed when the cron job runs in a **separate process** from the gateway (`hermes cron run` vs `hermes gateway`). Built-in platforms ship direct REST helpers in `tools/send_message_tool.py`; plugin platforms historically used `_gateway_runner_ref()`, which returns `None` outside the gateway process, so the cron-side send fails with `No live adapter for platform '<name>'`. Register a `standalone_sender_fn` to fix this:

```python
async def _standalone_send(
    pconfig, chat_id, message, *,
    thread_id=None, media_files=None, force_document=False,
):
    """Open an ephemeral connection / fresh token, send, close."""
    # ... open connection, send message ...
    return {"success": True, "message_id": "..."}   # or {"error": "..."}

ctx.register_platform(
    name="my_platform", ...,
    cron_deliver_env_var="MY_PLATFORM_HOME_CHANNEL",
    standalone_sender_fn=_standalone_send,
)
```

The function gets the same `pconfig` and `chat_id` the live adapter would, plus optional `thread_id`, `media_files`, `force_document`. `{"success": True, "message_id": ...}` is a successful delivery; `{"error": "..."}` surfaces in cron's `delivery_errors`; an exception is reported as `Plugin standalone send failed: <reason>`. References: `plugins/platforms/{irc,teams,google_chat}/adapter.py`.

## Surfacing Env Vars in `hermes config`

`hermes_cli/config.py` scans `plugins/platforms/*/plugin.yaml` at import time and auto-populates `OPTIONAL_ENV_VARS` from `requires_env` and (optional) `optional_env`. Use the rich-dict form to contribute descriptions, prompts, password flags, and URLs — the CLI setup UI picks them up for free. Supported dict keys: `name` (required), `description`, `prompt`, `url`, `password` (bool — auto-detected from a `*_TOKEN`/`*_SECRET`/`*_KEY`/`*_PASSWORD`/`*_JSON` suffix when omitted), and `category` (defaults to `"messaging"`).

```yaml
# plugins/platforms/my_platform/plugin.yaml
requires_env:
  - name: MY_PLATFORM_TOKEN
    description: "Bot API token from the My Platform console"
    prompt: "My Platform bot token"
    url: "https://my-platform.example.com/bots"
    password: true
  - name: MY_PLATFORM_CHANNEL
    description: "Channel to join (e.g. #hermes)"
    prompt: "Channel"
    password: false
optional_env:
  - name: MY_PLATFORM_HOME_CHANNEL
    description: "Default channel for cron delivery"
    prompt: "Home channel (or empty)"
    password: false
```

Bare-string entries still work (generic description derived from `label`). If a hardcoded entry for the same var already exists in `OPTIONAL_ENV_VARS`, it wins (back-compat); the `plugin.yaml` form is the fallback.

## Platform-Specific Slow-LLM UX

Some platforms constrain how a *slow* LLM response can be presented: **LINE** issues a single-use reply token that expires ~60s after the inbound event (free to use; the metered Push API is not); **WhatsApp** goes template-only after 24h of inactivity; **SMS** has no typing indicators, so long responses look like the bot is offline. The base `BasePlatformAdapter` can't anticipate these, so the plugin surface leaves room to layer platform-specific UX on the base typing loop without expanding the kwarg list.

**Pattern — subclass `_keep_typing` to layer mid-flight UX.** `_keep_typing` is the typing-indicator heartbeat: a background task that runs while the LLM generates and is cancelled on delivery. To fire something at a threshold (e.g. a "still thinking" bubble at 45s), override it, schedule a side task **alongside** `super()._keep_typing()`, and tear it down in `finally`:

```python
class LineAdapter(BasePlatformAdapter):
    async def _keep_typing(self, chat_id: str, *args, **kwargs) -> None:
        if self.slow_response_threshold <= 0:
            await super()._keep_typing(chat_id, *args, **kwargs)
            return

        async def _fire_at_threshold() -> None:
            try:
                await asyncio.sleep(self.slow_response_threshold)
            except asyncio.CancelledError:
                raise
            # LINE: send a Template Buttons "Get answer" bubble using the
            # cached reply token so the user can fetch the cached response
            # later via a fresh (free) reply token from a postback callback.
            await self._send_slow_response_button(chat_id)

        side_task = asyncio.create_task(_fire_at_threshold())
        try:
            await super()._keep_typing(chat_id, *args, **kwargs)
        finally:
            if not side_task.done():
                side_task.cancel()
                try:
                    await side_task
                except (asyncio.CancelledError, Exception):
                    pass
```

Key points: always `await super()._keep_typing(...)` (the heartbeat is independently useful — layer, don't replace); tear the side task down in `finally` so it observes cancellation when the LLM finishes or `/stop` runs; and pair with `interrupt_session_activity` to resolve orphan UX state on `/stop` (LINE flips the postback cache entry to `ERROR`).

**Pattern — subclass `send` to route through a cache.** If the slow-response UX caches the answer for later retrieval (LINE's postback flow), the `send` override recognizes three modes: (1) pending postback for this chat → cache the response under its `request_id`, send nothing visible; (2) a system busy-ack (`⚡`, `⏳`, `⏩`, `💾`) → bypass the cache, send visibly; (3) normal response → send via reply-token-or-push. The `_SYSTEM_BYPASS_PREFIXES` always pass through visibly regardless of cached UX state.

**When this is appropriate.** Use the typing-loop override when the platform's outbound API has a hard time-window (single-use reply token, expiring session) **and** a visible mid-flight bubble is acceptable; use the simpler always-Push path (`slow_response_threshold = 0`) when there is no free-vs-paid distinction. LINE supports both: the threshold defaults to 45s for free postback fetch, and `LINE_SLOW_RESPONSE_THRESHOLD=0` reverts to always-Push.

## Reference Implementations (Plugin Path)

| Adapter | Pattern | Good reference for |
|---------|---------|-------------------|
| `plugins/platforms/irc/` | Async IRC, zero external deps | Complete working minimal example |
| `plugins/platforms/teams/` | Bot Framework / Adaptive Cards | Rich-card messaging |
| `plugins/platforms/google_chat/` | OAuth-based REST APIs | OAuth + REST integration |
| `plugins/platforms/line/` | Webhook-driven Messaging API | Slow-LLM postback UX — `RequestCache` `PENDING → READY → DELIVERED`/`ERROR` state machine + `_keep_typing`/`send`/`interrupt_session_activity` overrides |

**Source**: `inbox/hermes_agent_docs/developer-guide/adding-platform-adapters.md`
**Last Updated**: 2026-06-19
**Status**: Active
