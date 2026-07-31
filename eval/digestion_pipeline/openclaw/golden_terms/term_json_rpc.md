---
tags:
  - resource
  - terminology
  - json-rpc
  - rpc-protocol
  - protocol-spec
keywords:
  - JSON-RPC
  - JSON-RPC 2.0
  - jsonrpc
  - method id params result error
  - notifications batch
topics:
  - RPC protocols
  - Wire protocols
  - Agent transport
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/JSON-RPC
access_control_group: ["general"]
---

# JSON-RPC

## Definition

**JSON-RPC** is a stateless, lightweight remote-procedure-call wire protocol that encodes requests, responses, and notifications as JSON objects. The protocol originated in 2005 as a JSON-flavored simplification of XML-RPC and was finalized as **JSON-RPC 2.0** on 2010-03-26 (with editorial cleanups in 2013). Where REST models *resources* and gRPC models *binary-typed services over HTTP/2*, JSON-RPC models *named method calls* with a tiny envelope: `{"jsonrpc": "2.0", "method": "...", "params": ..., "id": ...}` going one way and `{"jsonrpc": "2.0", "result": ... | "error": {...}, "id": ...}` coming back. It is deliberately **transport-agnostic** — the spec explicitly notes the protocol works "within the same process, over sockets, over http, or in many various message passing environments."

## Context

JSON-RPC is the dominant **agent-transport** wire format in 2025-2026: **MCP** (Anthropic, Nov 2024) chose it as the basis for stdio + Streamable-HTTP transports, **ACP** (Zed Industries, Aug 2025) chose it for editor ↔ agent stdio, and earlier protocols including **LSP** (Microsoft Language Server Protocol) and **DAP** (Debug Adapter Protocol) had already established JSON-RPC 2.0 as the standard for IDE ↔ tooling. Outside the agent space, **Ethereum** and most blockchain node APIs (Geth, Besu) expose JSON-RPC over HTTP and WebSocket, and **TrueNAS**, **OpenRPC**, **Hyperledger Besu**, and many home-automation / IoT control planes use it as their primary control protocol.

## Key Characteristics

- **Tiny envelope, five fields**: `jsonrpc` (always `"2.0"`), `method` (string), `params` (array or object), `id` (string / number / null), and on responses `result` *xor* `error`. Anything outside this is application-level.
- **Notifications = no `id`**: a request without an `id` member is a fire-and-forget notification; the server MUST NOT reply, even inside a batch.
- **Batch requests**: a client MAY send an array of request objects; the server returns an array of responses in arbitrary order, omitting entries for notifications. A batch of pure notifications produces no reply at all.
- **ID correlation for async**: because responses can return out of order, every request `id` is echoed on its response, letting the client multiplex many in-flight calls on one connection — essential for stdio and WebSocket carriers that cannot use HTTP's per-request socket pairing.
- **Reserved error-code band**: `-32700` parse error, `-32600` invalid request, `-32601` method not found, `-32602` invalid params, `-32603` internal error, and `-32000..-32099` for implementation-defined server errors. Application errors must live outside `-32768..-32000`.
- **Transport-agnostic by design**: spec is silent on framing. Common carriers are HTTP POST (one request per body), stdio with newline-delimited JSON (LSP, ACP, MCP-stdio), WebSocket (Ethereum), TCP, and Unix domain sockets.
- **JSON-only payloads — no binary, no streaming primitives**: blobs must be base64-encoded inside `params`, and there is no spec-level chunked-response or server-push concept. This is exactly why MCP pairs JSON-RPC with WebSocket (for bidirectional push) or SSE (for streaming text), rather than using bare HTTP.
- **Stateless on the wire, session-ful in the application**: the spec defines no session, auth, or capability negotiation; protocols like MCP and ACP layer those on top as the first method (`initialize`) of every connection.

## Related Terms

## References

- [JSON-RPC 2.0 Specification (jsonrpc.org)](https://www.jsonrpc.org/specification)
- [JSON-RPC — Wikipedia](https://en.wikipedia.org/wiki/JSON-RPC)
- [MCP Architecture Overview (Anthropic)](https://modelcontextprotocol.io/docs/learn/architecture)
- [Agent Client Protocol — Introduction (Zed)](https://agentclientprotocol.com/get-started/introduction)
- [Why MCP Uses JSON-RPC Instead of REST or gRPC (Glama)](https://glama.ai/blog/2025-08-13-why-mcp-uses-json-rpc-instead-of-rest-or-g-rpc)
- [JSON-RPC over WebSocket — rpc-websockets (GitHub)](https://github.com/elpheria/rpc-websockets)
