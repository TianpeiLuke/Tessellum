---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - smart_home
keywords:
  - home assistant integration
  - gateway platform websocket
  - ha_list_entities ha_get_state
  - ha_call_service smart home tools
  - long-lived access token
  - state_changed event filtering
  - blocked service domains
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant
access_control_group: ["general"]
---

# Hermes Agent — Home Assistant Integration

## Overview

The Home Assistant integration connects Hermes Agent to a [Home Assistant](https://www.home-assistant.io/) smart-home instance in **two simultaneous ways**, both activated by a single Long-Lived Access Token:

1. **Gateway platform** — subscribes to real-time state changes via WebSocket and forwards filtered `state_changed` events to the agent as messages.
2. **Smart home tools** — four LLM-callable tools (`ha_list_entities`, `ha_get_state`, `ha_list_services`, `ha_call_service`) for querying and controlling devices via the HA REST API.

Setting `HASS_TOKEN` auto-enables the `homeassistant` toolset and the gateway platform together. The integration ships security restrictions — a blocked-service-domain denylist (to prevent arbitrary code execution on the HA host) and an entity-ID validation pattern — and delivers the agent's outbound replies as Home Assistant **persistent notifications**. This page is the procedural setup and operating reference; the shared messaging-gateway core (pairing, ACL, delivery, session-keying) is documented in the gateway-platform notes.

## Setup

### 1. Create a Long-Lived Access Token

In the Home Assistant UI, open your **Profile** (click your name in the sidebar), scroll to **Long-Lived Access Tokens**, click **Create Token**, give it a name like "Hermes Agent", and copy the token.

### 2. Configure Environment Variables

```bash
# Add to ~/.hermes/.env

# Required: your Long-Lived Access Token
HASS_TOKEN=your-long-lived-access-token

# Optional: HA URL (default: http://homeassistant.local:8123)
HASS_URL=http://192.168.1.100:8123
```

The `homeassistant` toolset is automatically enabled when `HASS_TOKEN` is set — both the gateway platform and the device-control tools activate from this single token.

### 3. Start the Gateway

```bash
hermes gateway
```

Home Assistant appears as a connected platform alongside any other messaging platforms (Telegram, Discord, etc.).

## Available Tools

Hermes Agent registers four tools for smart-home control:

- **`ha_list_entities`** — List HA entities, optionally filtered by `domain` (`light`, `switch`, `climate`, `sensor`, `binary_sensor`, `cover`, `fan`, `media_player`, etc.) or `area` (room name matched against friendly names: `living room`, `kitchen`, `bedroom`). Returns entity IDs, states, and friendly names.
- **`ha_get_state`** — Get the detailed state of a single entity via the required `entity_id` parameter (e.g., `light.living_room`, `climate.thermostat`, `sensor.temperature`). Returns state, all attributes (brightness, color, temperature setpoint, sensor readings), and last changed/updated timestamps.
- **`ha_list_services`** — List available services (actions) for device control, optionally filtered by `domain`. Shows what actions can be performed on each device type and what parameters they accept.
- **`ha_call_service`** — Call an HA service to control a device. Parameters: `domain` *(required)* (`light`, `switch`, `climate`, `cover`, `media_player`, `fan`, `scene`, `script`), `service` *(required)* (`turn_on`, `turn_off`, `toggle`, `set_temperature`, `set_hvac_mode`, `open_cover`, `close_cover`, `set_volume_level`), `entity_id` *(optional)*, and `data` *(optional)* JSON object for additional parameters.

Representative `ha_call_service` calls (natural-language request → tool invocation):

```
Turn on the living room lights
→ ha_call_service(domain="light", service="turn_on", entity_id="light.living_room")

Set the thermostat to 22 degrees in heat mode
→ ha_call_service(domain="climate", service="set_temperature",
    entity_id="climate.thermostat", data={"temperature": 22, "hvac_mode": "heat"})

Set living room lights to blue at 50% brightness
→ ha_call_service(domain="light", service="turn_on",
    entity_id="light.living_room", data={"brightness": 128, "color_name": "blue"})
```

## Gateway Platform: Real-Time Events

The HA gateway adapter connects via WebSocket and subscribes to `state_changed` events. When a device state changes and matches your filters, it is forwarded to the agent as a message.

### Event Filtering

By default, **no events are forwarded**. You must configure at least one of `watch_domains`, `watch_entities`, or `watch_all` to receive events — without filters, a warning is logged at startup and all state changes are silently dropped. Configure filters in `~/.hermes/config.yaml` under the Home Assistant platform's `extra` section:

```yaml
platforms:
  homeassistant:
    enabled: true
    extra:
      watch_domains:
        - climate
        - binary_sensor
        - alarm_control_panel
        - light
      watch_entities:
        - sensor.front_door_battery
      ignore_entities:
        - sensor.uptime
        - sensor.cpu_usage
        - sensor.memory_usage
      cooldown_seconds: 30
```

| Setting | Default | Description |
|---------|---------|-------------|
| `watch_domains` | *(none)* | Only watch these entity domains (e.g., `climate`, `light`, `binary_sensor`) |
| `watch_entities` | *(none)* | Only watch these specific entity IDs |
| `watch_all` | `false` | Set to `true` to receive **all** state changes (not recommended for most setups) |
| `ignore_entities` | *(none)* | Always ignore these entities (applied before domain/entity filters) |
| `cooldown_seconds` | `30` | Minimum seconds between events for the same entity |

The source recommends starting with a focused set of domains — `climate`, `binary_sensor`, and `alarm_control_panel` cover the most useful automations — and using `ignore_entities` to suppress noisy sensors like CPU temperature or uptime counters.

### Event Formatting

State changes are formatted as human-readable messages based on domain:

| Domain | Format |
|--------|--------|
| `climate` | "HVAC mode changed from 'off' to 'heat' (current: 21, target: 23)" |
| `sensor` | "changed from 21°C to 22°C" |
| `binary_sensor` | "triggered" / "cleared" |
| `light`, `switch`, `fan` | "turned on" / "turned off" |
| `alarm_control_panel` | "alarm state changed from 'armed_away' to 'triggered'" |
| *(other)* | "changed from 'old' to 'new'" |

### Agent Responses

Outbound messages from the agent are delivered as **Home Assistant persistent notifications** (via `persistent_notification.create`). These appear in the HA notification panel with the title "Hermes Agent".

### Connection Management

- **WebSocket** with a 30-second heartbeat for real-time events.
- **Automatic reconnection** with backoff: 5s → 10s → 30s → 60s.
- **REST API** for outbound notifications (a separate session to avoid WebSocket conflicts).
- **Authorization** — HA events are always authorized (no user allowlist needed, since the `HASS_TOKEN` authenticates the connection).

## Security

The Home Assistant tools enforce security restrictions. The following service domains are **blocked** to prevent arbitrary code execution on the HA host (calling a service in these domains returns an error):

- `shell_command` — arbitrary shell commands
- `command_line` — sensors/switches that execute commands
- `python_script` — scripted Python execution
- `pyscript` — broader scripting integration
- `hassio` — addon control, host shutdown/reboot
- `rest_command` — HTTP requests from the HA server (SSRF vector)

Entity IDs are validated against the pattern `^[a-z_][a-z0-9_]*\.[a-z0-9_]+$` to prevent injection attacks.

## Example Automations

- **Morning Routine** — "Start my morning routine" → the agent chains `ha_call_service` calls: `light.turn_on` on `light.bedroom` (`brightness: 128`), `climate.set_temperature` on `climate.thermostat` (`temperature: 22`), and `media_player.turn_on` on `media_player.kitchen_speaker`.
- **Security Check** — "Is the house secure?" → `ha_list_entities(domain="binary_sensor")` checks door/window sensors, `ha_get_state(entity_id="alarm_control_panel.home")` checks alarm status, `ha_list_entities(domain="lock")` checks lock states, then reports: "All doors closed, alarm is armed_away, all locks engaged."
- **Reactive Automation (via Gateway Events)** — on `[Home Assistant] Front Door: triggered (was cleared)`, the agent automatically `ha_get_state(entity_id="binary_sensor.front_door")`, `ha_call_service(domain="light", service="turn_on", entity_id="light.hallway")`, and sends a notification: "Front door opened. Hallway lights turned on."

## Troubleshooting

- **Environment variables not picked up.** The adapter reads credentials from `~/.hermes/.env` (auto-merged at startup) or from `config.yaml`. Confirm the file lives under the active Hermes profile home and that there's no stray quoting around the URL/token. Restart the gateway after editing — env changes are applied only on process start.
- **`conversation entity not found` / agent never replies.** Home Assistant's conversation API requires a configured *Assist* conversation agent. In HA, open **Settings → Voice assistants → Add assistant** and note the resulting entity id (e.g., `conversation.home_assistant` or `conversation.openai_<name>`). Set that entity id in the adapter's `conversation_entity` setting; the default may not exist on your instance.
- **REST auth failing (`401 Unauthorized`).** The token must be a *Long-Lived Access Token* created from your HA user profile page (**Profile → Security → Long-lived access tokens**) — short-lived UI session tokens won't work. Verify the base URL includes the scheme and port (e.g., `http://homeassistant.local:8123`) and is reachable from the host running Hermes; `curl -H "Authorization: Bearer <token>" <url>/api/` should return `{"message": "API running."}`.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/homeassistant.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant
**Last Updated**: 2026-06-19
**Status**: Active
