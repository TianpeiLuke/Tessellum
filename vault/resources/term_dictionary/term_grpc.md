---
tags:
  - resource
  - terminology
  - system_design
  - networking
  - microservices
keywords:
  - gRPC
  - Remote Procedure Call
  - Protocol Buffers
  - protobuf
  - HTTP/2
  - bidirectional streaming
  - service definition
  - IDL
topics:
  - System Design
  - API Design
  - Microservices Communication
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# gRPC

## Definition

**gRPC** (gRPC Remote Procedure Calls) is a high-performance, open-source RPC framework originally developed by Google and now a Cloud Native Computing Foundation (CNCF) project. It uses **Protocol Buffers** (protobuf) as its Interface Definition Language (IDL) and binary serialization format, and **HTTP/2** as its transport protocol. gRPC enables a client application to directly call methods on a server application on a different machine as if it were a local object, making it straightforward to build distributed services. It supports code generation for over a dozen languages, allowing polyglot microservice architectures where services written in different languages communicate seamlessly through strongly typed contracts.

## Context

In modern distributed systems and microservices architectures, services must communicate efficiently across network boundaries. Traditional REST APIs using JSON over HTTP/1.1 introduce overhead from text-based serialization, lack of streaming, and the absence of a formal contract. gRPC addresses these limitations by combining binary serialization (smaller payloads, faster parsing), HTTP/2 transport (multiplexing, header compression, bidirectional streaming), and schema-first design (compile-time type safety, automated code generation). It has become the de facto standard for **internal service-to-service communication** in high-performance distributed systems, while REST remains dominant for external-facing and browser-based APIs.

## Key Characteristics

### Protocol Buffers (Protobuf)

- **Schema-first contract** — services are defined in `.proto` files that specify message types and RPC methods; the schema serves as the single source of truth and the API contract
- **Binary serialization** — messages are encoded in a compact binary format, resulting in payloads that are **3-10x smaller** than equivalent JSON and significantly faster to serialize/deserialize
- **Backward and forward compatibility** — field numbering allows schema evolution without breaking existing clients; fields can be added or deprecated without coordinated rollouts
- **Code generation** — the `protoc` compiler generates client stubs and server skeletons in multiple languages (Go, Java, Python, C++, Rust, etc.), eliminating manual serialization code

### HTTP/2 Transport

- **Multiplexing** — multiple RPC calls can be sent over a single TCP connection simultaneously without head-of-line blocking, reducing connection overhead
- **Header compression (HPACK)** — repeated headers are compressed, reducing per-request overhead for high-frequency calls
- **Bidirectional streaming** — both client and server can send data independently over the same connection
- **Flow control** — built-in backpressure mechanisms prevent fast producers from overwhelming slow consumers

### Four Communication Patterns

| Pattern | Client | Server | Use Cases |
|---------|--------|--------|-----------|
| **Unary** | 1 request | 1 response | CRUD operations, authentication checks, simple queries |
| **Server Streaming** | 1 request | stream of responses | Real-time updates, large dataset downloads, log tailing |
| **Client Streaming** | stream of requests | 1 response | File uploads, batch processing, sensor data aggregation |
| **Bidirectional Streaming** | stream of requests | stream of responses | Chat applications, real-time collaboration, gaming backends |

Unary calls represent the majority of gRPC usage in practice. Server streaming is the next most common pattern, used for real-time feeds and event notifications. Bidirectional streaming enables the most sophisticated interaction model where both sides can read and write independently in any order.

### gRPC vs REST Comparison

| Dimension | gRPC | REST |
|-----------|------|------|
| **Data format** | Binary (Protocol Buffers) | Text (JSON/XML) |
| **Contract** | Strict schema (`.proto` files) | Schema-optional (OpenAPI is optional) |
| **Transport** | HTTP/2 | HTTP/1.1 or HTTP/2 |
| **Communication** | Unary + streaming | Request-response only |
| **Code generation** | Built-in, multi-language | Third-party tools (OpenAPI Generator) |
| **Browser support** | Not native (requires gRPC-Web proxy) | Native |
| **Human readability** | Binary, not human-readable | Text, human-readable |
| **Performance** | Up to 7x faster in microservice benchmarks | Adequate for most external APIs |
| **Tooling maturity** | Growing but smaller ecosystem | Extensive, mature ecosystem |
| **Best for** | Internal service-to-service, real-time streaming, polyglot systems | External APIs, browser clients, public APIs |

### When to Use gRPC

- **Internal microservice communication** — where performance, type safety, and streaming matter more than browser compatibility
- **Real-time streaming** — analytics pipelines, live feeds, event-driven systems where server streaming or bidirectional streaming is required
- **Polyglot environments** — where services are written in different languages and need a shared, strongly typed contract
- **High-throughput, low-latency paths** — payment processing, fraud detection, real-time scoring where every millisecond counts

### When REST is Preferred

- **Public-facing APIs** — where broad client compatibility, browser support, and human readability are priorities
- **Simple CRUD applications** — where the overhead of protobuf schema management is not justified
- **Third-party integrations** — where consumers expect standard HTTP semantics and JSON payloads

## Related Terms

- **[Microservices Architecture](term_microservices_architecture.md)** — gRPC is a primary communication protocol for inter-service calls in microservices architectures
- **[Event-Driven Architecture](term_event_driven_architecture.md)** — complementary pattern; gRPC handles synchronous RPC while event-driven handles asynchronous communication
- **[Kafka](term_kafka.md)** — common event backbone for asynchronous messaging between microservices; gRPC handles synchronous paths, Kafka handles event streams
- **[SSL](term_ssl.md)** — gRPC uses TLS (successor to SSL) for transport-layer encryption; mutual TLS (mTLS) is the standard for securing gRPC channels in production
- **[Service-Based Architecture](term_service_based_architecture.md)** — coarser-grained alternative to microservices; may use gRPC or REST for inter-service communication
- **[Architectural Quantum](term_architectural_quantum.md)** — each gRPC service boundary defines an independently deployable quantum
- **[CAP Theorem](term_cap_theorem.md)** — distributed gRPC services must make consistency vs availability trade-offs at partition boundaries
- **[Availability](term_availability.md)** — gRPC services require health checking, load balancing, and retry policies to maintain availability targets
- **[A2A Protocol](term_a2a.md)** — Google's Agent-to-Agent protocol; distinct from gRPC but shares the principle of structured inter-service communication
- **[Change Data Capture](term_change_data_capture.md)** — CDC events can trigger gRPC calls or be consumed alongside gRPC-based synchronous communication
- **[NGINX](term_nginx.md)**: NGINX natively supports gRPC proxying and load balancing via the `grpc_pass` directive, enabling HTTP/2-based RPC routing through the reverse proxy layer
- **[GraphQL](term_graphql.md)**: Alternative API paradigm to gRPC; GraphQL excels at client-facing flexible queries while gRPC dominates internal high-throughput microservice communication
- **[API Gateway](term_api_gateway.md)**: API Gateways perform protocol translation between client-facing REST/HTTP and internal gRPC services, enabling gRPC microservices to serve browser clients transparently
- **[REST](term_rest.md)**: REST is gRPC's primary alternative -- REST uses text-based JSON over HTTP/1.1 for public APIs with universal browser support, while gRPC uses binary Protobuf over HTTP/2 for high-performance internal microservice communication

## References

### External Sources
- [gRPC Official Documentation](https://grpc.io/docs/) — authoritative reference for gRPC concepts, guides, and API documentation
- [gRPC Core Concepts, Architecture and Lifecycle](https://grpc.io/docs/what-is-grpc/core-concepts/) — official guide covering the four communication patterns
- [Protocol Buffers Documentation](https://protobuf.dev/) — official protobuf language guide and best practices
- [gRPC vs REST — AWS](https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/) — comprehensive comparison of gRPC and REST design patterns
- [gRPC vs REST — Google Cloud Blog](https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them) — guidance on choosing between gRPC, OpenAPI, and REST
- [gRPC HTTP/2 Protocol Specification](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) — low-level protocol details for gRPC over HTTP/2
- [Wikipedia: gRPC](https://en.wikipedia.org/wiki/GRPC)
