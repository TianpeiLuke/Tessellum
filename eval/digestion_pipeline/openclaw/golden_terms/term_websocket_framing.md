---
tags:
  - resource
  - terminology
  - websocket-framing
  - rfc-6455
  - wire-protocol
  - openclaw
keywords:
  - WebSocket framing
  - RFC 6455 frame
  - opcode FIN mask
  - control frame
  - fragmentation continuation
  - maximumMessageSize
topics:
  - WebSocket protocol
  - Wire framing
  - Network transport
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/WebSocket
access_control_group: ["general"]
---

# WebSocket Framing

## Definition

**WebSocket Framing** is the message-framing layer of RFC 6455 — the wire-format rules that govern how every byte travels over an established WebSocket connection. While the parent term [WebSocket](term_websocket.md) names the protocol as a whole (handshake, full-duplex semantics, URI schemes, lifecycle), *framing* refers specifically to how each application message is encoded into one or more frames on the wire: the 2-to-14-byte header that carries the FIN bit, the four reserved bits, the 4-bit opcode, the mask bit, the 7/16/64-bit payload-length encoding, the optional 32-bit masking key, and the payload data itself. Every conforming implementation — whether a server library (Node.js `ws`, Python `websockets`, Go `gorilla/websocket`), a high-level browser API, or a low-level transport like Apple's `URLSessionWebSocketTask` — speaks this same frame grammar underneath.

Most application developers never see frames directly because their library lifts them into message-shaped APIs (`onmessage`, `send`, `receive` returning a `Message` enum). The framing layer becomes load-bearing only when (a) implementing a custom WebSocket client/server, (b) tuning a library's frame-level parameters (e.g., bumping `maximumMessageSize` so continuation-bridged messages do not error out), or (c) reasoning about why something at the byte level went wrong — an unmasked client frame, a control frame larger than 125 bytes, or a stuck fragmented message waiting on a missing continuation. OpenClawKit's `GatewayChannel.swift` sits in exactly this zone: it wraps `URLSessionWebSocketTask` (which speaks framing internally) but has to make explicit decisions about message-size limits and ping/pong wiring that only make sense at the framing level.

## Context

WebSocket framing details matter in three settings: **custom protocol implementers** (anyone building a WS server or client from sockets up, as in pusher's "WebSockets from Scratch" tutorial); **library configurators** (developers tuning `ws`, `gorilla/websocket`, OkHttp's WebSocket, `URLSessionWebSocketTask`); and **agent-runtime authors** like OpenClaw, where the wire-level cost model dictates higher-level design. OpenClawKit's Gateway channel is the canonical example: the `WebSocketSessioning` factory bumps `URLSessionWebSocketTask.maximumMessageSize` to 16 MB so that ACP [Event Ledger](term_event_ledger.md) replays and large snapshot payloads do not trip the default cap (Apple's docs note that the bound is the sum of all bytes across continuation frames — i.e., it is a *fragmented-message* limit, not a single-frame limit, which is exactly where the cap bites for any ledger replay). The same channel wraps `URLSessionWebSocketTask.sendPing` in a continuation-bridged async surface for its keep-alive loop — under the hood, that call emits an RFC 6455 ping opcode (0x9) frame and resolves the continuation when the matching pong (0xA) returns, NAT-keepalive without the actor having to think about framing.

The Android counterpart ([Android Gateway Session WS](../code_snippets/snippet_openclaw_android_gateway_session_ws.md)) uses OkHttp's `WebSocket`, which similarly hides framing but exposes `pingInterval`. The gateway server side ([Gateway HTTP listen WS](../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md)) handles the RFC 6455 upgrade handshake and then speaks frames via the `ws` Node.js library. In all three, JSON-RPC envelopes ride inside text-opcode (0x1) frames carrying UTF-8 — see [JSON-RPC](term_json_rpc.md) — and the framing layer's main job is to deliver each envelope intact, in order, without an application-visible split.

## Key Characteristics

- **Opcodes (4 bits)**: `0x0` continuation, `0x1` text (UTF-8), `0x2` binary, `0x8` close, `0x9` ping, `0xA` pong; `0x3-0x7` reserved non-control; `0xB-0xF` reserved control.
- **FIN bit + fragmentation**: a logical message can span multiple frames — the first carries the type opcode with FIN=0, zero or more continuation (`0x0`) frames follow with FIN=0, and the final continuation frame sets FIN=1. The library reassembles them before surfacing the message.
- **Mask bit (client→server mandatory)**: all client-sent frames must be masked with a 32-bit key XOR-applied to the payload; the server must close the connection on receiving an unmasked frame, and the server itself must never mask. The reason is cache-poisoning defense at intermediaries that confuse WS traffic for HTTP.
- **Payload length encoding**: 7 bits inline (0-125 bytes), 7+16 bits (extended, up to 65,535), or 7+64 bits (jumbo, up to 2^63-1 bytes); most production frames use the inline or 16-bit form, with the 64-bit form gated by intermediaries' per-frame limits.
- **Control frames are bounded**: close (`0x8`), ping (`0x9`), pong (`0xA`) must carry ≤125 bytes and must never be fragmented (FIN=1 always). This is what lets a control frame interrupt a long fragmented message — the receiver can interleave a ping reply mid-stream.
- **Keepalive via ping/pong**: either side may send a ping; the receiver must echo a pong with the same payload, automatically. Most libraries (URLSession, OkHttp, `ws`) expose this as a high-level "ping interval" knob.
- **Close-status codes**: the close frame's first 2 payload bytes encode a code (1000 normal, 1001 going-away, 1002 protocol-error, 1003 unsupported-data, 1006 abnormal-no-close, 1008 policy-violation, 1009 message-too-big, 1011 internal-error); the rest is a human-readable reason.
- **Contrast with HTTP/2 framing**: both are framed binary protocols over a single TCP connection, but HTTP/2 frames are multiplexed across many *streams* on one connection with explicit stream IDs, whereas a WebSocket connection carries one logical bidirectional message channel — no stream multiplexing, much simpler header, no priority/flow-control machinery beyond TCP itself.

## Related Terms

- **OpenClawKit** (pending — `term_openclawkit.md` not yet authored): Swift client library whose `GatewayChannel` is the immediate consumer of `URLSessionWebSocketTask`'s framing primitives.
- [Band WebSocket Agent Event Payloads](../documentation/band/band_websocket_agent_events.md) — documents Band's application-level agent event schemas (Phoenix-envelope payload model) delivered over a persistent socket; relevance: this term covers the RFC 6455 wire-framing layer that carries application messages, and JSON-RPC/text-opcode envelopes ride inside those frames — a reader moving from the byte-level framing concept to a real protocol's event schemas riding on top would want this concrete payload model.

## Related Code Snippets

- **[OpenClawKit GatewayChannel WS](../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md)**: the 3-way-split documenting `WebSocketTasking` protocol, `WebSocketTaskBox` Sendable wrapper, `WebSocketSessioning` factory's 16 MB `maximumMessageSize` bump, and the continuation-bridged `sendPing` keep-alive loop — the load-bearing example of framing-level decisions in OpenClaw.
- **[OpenClaw Gateway HTTP listen WS](../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md)**: gateway-side WS upgrade handler — where the framing layer is entered on the server.
- **[OpenClaw Android Gateway Session WS](../code_snippets/snippet_openclaw_android_gateway_session_ws.md)**: Android counterpart using OkHttp's WebSocket, whose `pingInterval` and frame-size knobs mirror URLSession's.

## References

- [RFC 6455 — The WebSocket Protocol (IETF Datatracker)](https://datatracker.ietf.org/doc/html/rfc6455)
- [RFC 6455 — The WebSocket Protocol (RFC Editor)](https://www.rfc-editor.org/rfc/rfc6455.html)
- [WebSocket (Wikipedia)](https://en.wikipedia.org/wiki/WebSocket)
- [URLSessionWebSocketTask.maximumMessageSize (Apple Developer Documentation)](https://developer.apple.com/documentation/foundation/urlsessionwebsockettask/maximummessagesize)
- [Writing WebSocket servers (MDN Web Docs)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers)
