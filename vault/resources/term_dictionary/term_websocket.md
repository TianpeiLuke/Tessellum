---
tags:
  - resource
  - terminology
  - system_design
  - networking
  - real_time
keywords:
  - WebSocket
  - RFC 6455
  - full-duplex
  - bidirectional communication
  - persistent connection
  - ws://
  - wss://
  - real-time
  - HTTP upgrade
  - Socket.IO
  - handshake
  - ping-pong
topics:
  - system design
  - networking protocols
  - real-time communication
  - web architecture
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: WebSocket

## Definition

**WebSocket** is a communication protocol that provides **full-duplex, bidirectional communication** over a single persistent TCP connection. Defined in **RFC 6455** (IETF, 2011), WebSocket enables real-time data exchange between client and server without the overhead of repeated HTTP request-response cycles. Unlike HTTP, where the client must initiate every exchange, WebSocket allows either side to send messages independently at any time after the initial handshake. The protocol uses `ws://` (unencrypted, port 80) and `wss://` (TLS-encrypted, port 443) URI schemes. WebSocket is the foundational protocol for interactive web applications requiring low-latency, high-frequency data updates -- chat applications, live dashboards, multiplayer games, collaborative editors, and financial tickers.

## Context

### The Problem WebSocket Solves

HTTP was designed as a request-response protocol: the client asks, the server answers, the connection closes. This model breaks down when the server needs to push data to the client in real time. Before WebSocket, developers relied on workarounds:

- **HTTP Short Polling**: Client repeatedly sends requests at fixed intervals (e.g., every 2 seconds). Simple but wasteful -- most responses are empty "nothing new" replies, consuming bandwidth and server resources.
- **HTTP Long Polling**: Client sends a request; the server holds the connection open until new data is available, then responds. Reduces empty responses but still requires re-establishing connections after each message and carries full HTTP header overhead each time.
- **Server-Sent Events (SSE)**: Server pushes updates to the client over a persistent HTTP connection. Simpler than WebSocket but **unidirectional** (server-to-client only) and limited to text-based data.

WebSocket was created to provide a standardized, efficient, truly bidirectional channel that operates over existing web infrastructure (ports 80/443, compatible with proxies and firewalls).

### Where WebSocket Is Used

- **Chat and messaging applications** (Slack, Discord, WhatsApp Web)
- **Live dashboards and monitoring** (real-time metrics, server health)
- **Multiplayer online gaming** (game state synchronization)
- **Collaborative editing** (Google Docs, Figma)
- **Financial tickers** (stock prices, cryptocurrency exchanges)
- **IoT telemetry** (sensor data streaming)
- **Live sports scores and notifications**
- **Auction and bidding systems** (real-time bid updates)

## Key Characteristics

### 1. The WebSocket Handshake (HTTP Upgrade)

WebSocket connections start as a standard HTTP request with an `Upgrade` header. If the server supports WebSocket, it responds with HTTP `101 Switching Protocols`, and the connection is upgraded from HTTP to WebSocket.

```
Client Request:
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

Server Response:
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

After this handshake, the connection is no longer HTTP -- it is a persistent, full-duplex WebSocket connection.

### 2. Full-Duplex Communication

Once established, either side can send messages independently and simultaneously. There is no request-response coupling -- the server can push data without the client asking, and the client can send data without waiting for a server response.

```
┌──────────┐                         ┌──────────┐
│  Client  │ ── HTTP Upgrade Req ──► │  Server  │
│          │ ◄─ 101 Switching ─────  │          │
│          │                         │          │
│          │ ◄═══ Data Frame ══════  │          │
│          │ ═══ Data Frame ══════►  │          │
│          │ ◄═══ Data Frame ══════  │          │
│          │ ═══ Data Frame ══════►  │          │
│          │ ◄═══ Data Frame ══════  │          │
│          │         ...             │          │
│          │ ── Close Frame ──────►  │          │
│          │ ◄─ Close Frame ───────  │          │
└──────────┘                         └──────────┘
     Bidirectional, independent messaging
```

### 3. Frame-Based Protocol

WebSocket transmits data in **frames** rather than continuous byte streams. Each frame has a minimal header (as low as 2 bytes for small payloads), making it extremely lightweight compared to HTTP headers (typically hundreds of bytes per request).

| Frame Type | Opcode | Purpose |
|------------|--------|---------|
| **Text** | 0x1 | UTF-8 text data |
| **Binary** | 0x2 | Binary data (images, protobuf, etc.) |
| **Ping** | 0x9 | Heartbeat check (sent by either side) |
| **Pong** | 0xA | Heartbeat response (automatic) |
| **Close** | 0x8 | Graceful connection termination |
| **Continuation** | 0x0 | Continuation of a fragmented message |

### 4. URI Schemes: ws:// and wss://

| Scheme | Encryption | Default Port | Usage |
|--------|-----------|-------------|-------|
| `ws://` | None | 80 | Development, internal networks |
| `wss://` | TLS (same as HTTPS) | 443 | Production -- always use wss:// in production |

`wss://` uses TLS encryption identical to HTTPS, ensuring data confidentiality and integrity in transit. Modern browsers and load balancers expect `wss://` for production WebSocket traffic.

### 5. Connection Lifecycle

```
1. CONNECTING    Client sends HTTP Upgrade request
       │
       ▼
2. OPEN          Handshake complete; bidirectional messaging active
       │
       ▼
3. CLOSING       Either side sends a Close frame
       │
       ▼
4. CLOSED        Connection fully terminated; resources released
```

The connection remains open indefinitely until either side initiates a close or a network failure occurs. Applications must handle reconnection logic for dropped connections.

### 6. Heartbeat / Ping-Pong Mechanism

WebSocket includes a built-in keep-alive mechanism via **Ping** and **Pong** control frames:

- Either side can send a Ping frame at any time
- The receiving side must respond with a Pong frame automatically
- This detects dead connections, prevents idle timeouts from proxies/load balancers, and ensures both parties are still reachable
- Typical heartbeat intervals: 15-30 seconds

### 7. Scaling Challenges

WebSocket connections are **stateful and persistent**, which introduces scaling complexity compared to stateless HTTP:

| Challenge | Description | Mitigation |
|-----------|-------------|------------|
| **Sticky sessions** | Each connection is bound to a specific server; load balancers must route subsequent frames to the same backend | Use Layer 7 load balancers with WebSocket-aware routing; consistent hashing |
| **Connection state** | Each open connection consumes server memory (file descriptors, buffers) | Optimize per-connection memory; use event-loop-based servers (Node.js, Go, Nginx) |
| **Horizontal scaling** | Broadcasting messages to all connected clients across multiple servers requires cross-server coordination | Use a pub-sub backbone (Redis Pub/Sub, Kafka) to fan out messages across server instances |
| **Connection limits** | OS-level limits on open file descriptors; single server may cap at ~65K connections per IP | Tune OS limits (`ulimit`); distribute across multiple server IPs |
| **Reconnection storms** | Server restart causes all clients to reconnect simultaneously | Implement exponential backoff with jitter on client reconnection |

### 8. Comparison: WebSocket vs. Alternatives

| Dimension | WebSocket | HTTP Short Polling | HTTP Long Polling | Server-Sent Events (SSE) |
|-----------|-----------|-------------------|------------------|--------------------------|
| **Direction** | Bidirectional (full-duplex) | Client-to-server only | Client-to-server only | Server-to-client only |
| **Connection** | Single persistent TCP | New connection per poll | Held open, re-established per message | Single persistent HTTP |
| **Overhead per message** | ~2 bytes frame header | Full HTTP headers (~800 bytes) | Full HTTP headers (~800 bytes) | ~5 bytes per event |
| **Latency** | Sub-millisecond (after handshake) | Poll interval (seconds) | Near-real-time (held connection) | Near-real-time |
| **Server push** | Native | No (client initiates) | Simulated (delayed response) | Native |
| **Binary data** | Yes (binary frames) | Yes (via HTTP body) | Yes (via HTTP body) | No (text only, needs Base64) |
| **Browser support** | All modern browsers | Universal | Universal | All modern (no IE) |
| **Scaling complexity** | High (stateful) | Low (stateless) | Medium (held connections) | Medium (persistent HTTP) |
| **Best for** | Chat, gaming, collaboration | Legacy APIs, simple checks | Moderate real-time needs | Live feeds, notifications |

### 9. Socket.IO and Abstraction Libraries

**Socket.IO** is the most popular WebSocket abstraction library. It provides:

- **Automatic fallback**: Falls back to HTTP long polling if WebSocket is unavailable (corporate proxies, old browsers)
- **Rooms and namespaces**: Built-in logical grouping of connections for broadcasting
- **Auto-reconnection**: Handles dropped connections with configurable retry logic
- **Acknowledgements**: Request-response semantics on top of WebSocket
- **Binary support**: Seamless binary data transfer

**Important**: Socket.IO is **not** a WebSocket implementation -- it is a higher-level protocol built on top of WebSocket (and other transports). A Socket.IO client cannot connect to a plain WebSocket server, and vice versa.

Other libraries: `ws` (Node.js), `websockets` (Python), `gorilla/websocket` (Go), Spring WebSocket (Java).

## Related Terms

### Networking and Protocols
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- WebSocket enables event-driven real-time communication between client and server; events pushed without polling
- **[Term: Apache Kafka](term_kafka.md)** -- Used as a pub-sub backbone to fan out WebSocket messages across horizontally scaled server instances
- **[Term: Observer Pattern](term_observer_pattern.md)** -- WebSocket implements the observer pattern at the network level: server notifies subscribed clients of state changes
- **[Term: Stream Processing](term_stream_processing.md)** -- WebSocket provides the real-time transport layer that feeds stream processing pipelines

### System Design and Architecture
- **[Term: Microservices Architecture](term_microservices_architecture.md)** -- WebSocket gateways in microservices require special handling for connection routing and service discovery
- **[Term: CAP Theorem](term_cap_theorem.md)** -- WebSocket-based systems face CAP trade-offs: connection state is partitioned across servers, requiring consistency vs. availability decisions
- **[Term: Consistency](term_consistency.md)** -- Real-time systems using WebSocket must choose between strong and eventual consistency for message delivery and ordering
- **[Term: Proxy Pattern](term_proxy_pattern.md)** -- Reverse proxies (Nginx, HAProxy) must be configured for WebSocket pass-through via HTTP Upgrade support
- **[Term: Hexagonal Architecture](term_hexagonal_architecture.md)** -- WebSocket adapters serve as inbound ports in hexagonal architecture for real-time interfaces

### API Paradigms
- **[GraphQL](term_graphql.md)**: GraphQL subscriptions use WebSocket as the transport protocol for real-time server-to-client data push in client-driven APIs
- **[API Gateway](term_api_gateway.md)**: API Gateways handle WebSocket protocol translation and connection management, routing persistent WebSocket connections to appropriate backend services
- **[REST](term_rest.md)**: REST's request-response model cannot natively push data from server to client -- WebSocket solves this limitation by providing full-duplex, bidirectional communication after an HTTP Upgrade handshake

### Messaging Patterns
- **[Pub/Sub](term_pub_sub.md)**: WebSocket scaling across multiple server instances requires a pub/sub backbone (Redis Pub/Sub, Kafka) to fan out messages to all connected clients regardless of which server holds their connection

### Data and Infrastructure
- **[Term: Elasticsearch](term_elasticsearch.md)** -- Often paired with WebSocket for real-time search-as-you-type and live log streaming dashboards
- **[Term: Clickstream](term_clickstream.md)** -- WebSocket can transport clickstream events in real time from browser to analytics pipeline
- **[Term: Kinesis](term_kinesis.md)** -- AWS managed streaming service that can ingest data from WebSocket-connected clients at scale
- **[gRPC](term_grpc.md)**: gRPC's bidirectional streaming over HTTP/2 provides an alternative to WebSocket for real-time server-to-server communication -- gRPC is preferred for structured RPC with type safety, WebSocket for browser-based real-time apps

## References

### Vault References
- SDDD Podcast Series, Episode 2 -- Fundamentals of System Design: WebSocket as a core real-time communication primitive

### External References
- IETF RFC 6455 -- The WebSocket Protocol: https://www.rfc-editor.org/rfc/rfc6455.html
- MDN Web Docs -- WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- WebSocket.org -- Protocol Guide: https://websocket.org/guides/websocket-protocol/
- Socket.IO Documentation: https://socket.io/docs/v4/
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. -- Chapter 11 on stream processing and messaging protocols
- ByteByteGo -- Short/Long Polling, SSE, WebSocket: https://bytebytego.com/guides/shortlong-polling-sse-websocket/
- AlgoMaster -- Polling vs Long Polling vs SSE vs WebSockets vs Webhooks: https://blog.algomaster.io/p/polling-vs-long-polling-vs-sse-vs-websockets-webhooks

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Communication protocol (application layer) |
| **RFC** | RFC 6455 (IETF, December 2011) |
| **Communication** | Full-duplex, bidirectional over single TCP connection |
| **Handshake** | HTTP Upgrade (GET with `Upgrade: websocket` header, server responds 101) |
| **URI schemes** | `ws://` (unencrypted), `wss://` (TLS-encrypted) |
| **Frame overhead** | As low as 2 bytes per frame (vs. hundreds of bytes for HTTP headers) |
| **Keep-alive** | Built-in Ping/Pong control frames |
| **Key use cases** | Chat, gaming, dashboards, collaborative editing, financial tickers, IoT |
| **Scaling challenge** | Stateful persistent connections require sticky sessions and cross-server pub-sub |
| **Popular libraries** | Socket.IO, `ws` (Node.js), `websockets` (Python), `gorilla/websocket` (Go) |

**Key Insight**: WebSocket's fundamental contribution is eliminating the impedance mismatch between HTTP's request-response model and the reality of interactive, real-time applications. By upgrading a single HTTP connection into a persistent, full-duplex channel, WebSocket removes the need for polling hacks that waste bandwidth and add latency. However, this benefit comes with an architectural cost: **statefulness**. Every open WebSocket connection is a piece of server-side state that must be managed, load-balanced, and coordinated across horizontally scaled instances. This is why production WebSocket systems almost always require a pub-sub backbone (Redis, Kafka) behind the WebSocket servers -- the persistent connections handle the last-mile delivery to clients, while the pub-sub layer handles the fan-out across servers. The design decision is not "WebSocket vs. HTTP" but rather understanding where in the communication spectrum your application falls: if the server rarely pushes data, SSE or long polling may suffice; if bidirectional, high-frequency interaction is required, WebSocket is the right primitive.

---

**Last Updated**: April 19, 2026
**Status**: Active - foundational real-time communication protocol in system design
