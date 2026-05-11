---
tags:
  - resource
  - terminology
  - system_design
  - microservices
  - networking
keywords:
  - API Gateway
  - API management
  - request routing
  - authentication
  - rate limiting
  - service mesh
  - Kong
  - AWS API Gateway
topics:
  - System Design
  - Microservices Architecture
  - API Management
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# API Gateway

## Definition

An **API Gateway** is an infrastructure component that serves as the **single entry point** for all client requests in a microservices architecture. It sits between external clients and the internal service ecosystem, accepting all incoming API calls, routing them to the appropriate backend services, aggregating results, and returning consolidated responses. The gateway decouples clients from the internal service topology — clients interact with one endpoint rather than discovering and communicating with dozens of individual services directly.

The concept is analogous to the **Facade pattern** applied at the network level: just as a facade provides a simplified interface to a complex subsystem, an API Gateway presents a unified API surface while hiding the internal decomposition of services, their protocols, and their locations. Without a gateway, clients must know about every service endpoint, handle multiple authentication schemes, and manage cross-cutting concerns themselves — leading to tight coupling and duplicated logic across client applications.

## Context

In a monolithic architecture a single server handles all requests, making a gateway unnecessary. As systems decompose into microservices, the number of independently deployed services grows rapidly, and the API Gateway becomes **operationally essential** for managing the surface area. Major cloud providers offer managed gateway services (AWS API Gateway, Azure API Management, Google Cloud Endpoints), while open-source solutions like Kong, Tyk, and Express Gateway provide self-hosted alternatives.

The API Gateway pattern is documented in Chris Richardson's *Microservices Patterns* (2018) and is a core component in the microservices infrastructure stack described by Sam Newman in *Building Microservices* (2021).

## Key Characteristics

### Core Responsibilities

| Responsibility | Description |
|---------------|-------------|
| **Request Routing** | Maps incoming requests to backend services based on URL path, HTTP method, headers, and query parameters |
| **Authentication & Authorization** | Centralizes identity verification (OAuth, JWT, API keys) so individual services do not each implement auth logic |
| **Rate Limiting & Throttling** | Enforces usage quotas and request-per-second limits to protect backend services from overload and abuse |
| **Protocol Translation** | Converts between client-facing protocols (REST/HTTP) and internal protocols (gRPC, WebSocket, AMQP) transparently |
| **Load Balancing** | Distributes requests across multiple instances of a backend service for high availability and horizontal scalability |
| **Response Aggregation** | Combines data from multiple backend services into a single response, reducing client-side round trips |
| **Caching** | Stores frequently accessed, non-user-specific responses to reduce backend load and improve latency |
| **SSL/TLS Termination** | Handles encryption at the edge so internal service-to-service traffic can use lighter protocols |
| **Logging & Monitoring** | Centralizes request metrics, latency tracking, error rates, and distributed tracing correlation |
| **Circuit Breaking** | Detects failing backend services and short-circuits requests to prevent cascade failures across the system |

### API Gateway vs Reverse Proxy vs Load Balancer

These three components overlap in functionality but differ in scope and intent:

| Component | Primary Purpose | Operates At | API Awareness |
|-----------|----------------|-------------|---------------|
| **Load Balancer** | Distribute traffic across identical server instances | L4 (TCP/UDP) or L7 (HTTP) | None — treats servers as interchangeable |
| **Reverse Proxy** | Forward requests on behalf of clients, add caching and SSL termination | L7 (HTTP) | Minimal — URL-based routing |
| **API Gateway** | Full API lifecycle management: routing, auth, rate limiting, transformation, aggregation | L7 (HTTP/gRPC/WebSocket) | Deep — understands API schemas, versioning, and contracts |

A reverse proxy forwards requests; a load balancer distributes them; an **API Gateway understands them**. In practice, modern API Gateways incorporate both reverse-proxy and load-balancing capabilities, but add API-aware features (request/response transformation, developer portal, API key management, usage analytics) that neither a pure proxy nor a pure load balancer provides.

### Common Implementations

| Category | Solutions | Notes |
|----------|----------|-------|
| **Managed Cloud** | AWS API Gateway, Azure API Management, Google Cloud Endpoints | Serverless scaling, native cloud integration, pay-per-request |
| **Open Source** | Kong (NGINX-based), Tyk, Express Gateway, KrakenD | Self-hosted, extensible via plugins, full control |
| **Service Mesh Ingress** | Istio Gateway, Envoy, Linkerd | Gateway as the ingress layer of a broader service mesh |

### Design Considerations

- **Single point of failure** — the gateway must be deployed with high availability (multiple instances behind a load balancer) to avoid becoming a bottleneck or SPOF
- **Backend for Frontend (BFF)** — a pattern variant where separate gateways serve different client types (mobile, web, third-party), each tailored to its client's data and protocol needs
- **Gateway bloat** — resist the temptation to push business logic into the gateway; it should handle cross-cutting infrastructure concerns only
- **Latency overhead** — every request passes through an additional network hop; minimize processing in the gateway to keep added latency under a few milliseconds

## Related Terms

- **[Microservices Architecture](term_microservices_architecture.md)** — the architectural style that necessitates an API Gateway as its single client-facing entry point
- **[Facade Pattern](term_facade_pattern.md)** — the GoF structural pattern that the API Gateway embodies at the network level: a simplified interface to a complex subsystem
- **[Proxy Pattern](term_proxy_pattern.md)** — the API Gateway acts as a network-level proxy, intercepting and forwarding requests with additional control logic
- **[Adapter Pattern](term_adapter_pattern.md)** — the gateway performs protocol adaptation (REST to gRPC), analogous to the Adapter pattern's interface translation
- **[Decorator Pattern](term_decorator_pattern.md)** — cross-cutting concerns (auth, logging, rate limiting) layered onto requests mirror the Decorator's compositional enrichment
- **[Event-Driven Architecture](term_event_driven_architecture.md)** — often paired with API Gateways; synchronous gateway calls may trigger asynchronous event flows internally
- **[Service-Based Architecture](term_service_based_architecture.md)** — coarser-grained alternative to microservices that may use a simpler gateway or none at all
- **[CAP Theorem](term_cap_theorem.md)** — gateway routing decisions interact with consistency-availability trade-offs across partitioned services
- **[Availability](term_availability.md)** — the gateway's own availability directly bounds the system's overall availability
- **[Cache-Aside](term_cache_aside.md)**: Caching pattern used by API gateways to cache frequently requested responses; the gateway checks the cache before routing to backend services
- **[Cache Invalidation](term_cache_invalidation.md)**: API gateways must invalidate cached responses when backend data changes; TTL-based and event-driven invalidation strategies prevent serving stale data
- **[SSL](term_ssl.md)** — TLS/SSL termination is a core gateway responsibility, offloading encryption from backend services
- **[Kafka](term_kafka.md)** — API Gateways may publish request events to Kafka topics for asynchronous processing and audit logging
- **[Consistency](term_consistency.md)** — response aggregation across services requires the gateway to handle inconsistent or partial responses
- **[Architectural Quantum](term_architectural_quantum.md)** — the gateway sits at the boundary between quanta, mediating independently deployable units
- **[Observability in Agent Systems](term_observability_agent_systems.md)** — centralized gateway logging feeds observability pipelines for monitoring distributed systems
- **[Data Observability](term_data_observability.md)** — API traffic metrics collected at the gateway contribute to data quality and system health monitoring
- **[GraphQL](term_graphql.md)**: GraphQL frequently serves as a Backend for Frontend layer behind an API gateway, aggregating data from multiple microservices into a single client-tailored endpoint
- **[SSL Termination](term_ssl_termination.md)**: API Gateways handle TLS termination at the edge, decrypting incoming HTTPS traffic so internal service-to-service communication uses lighter protocols
- **[WebSocket](term_websocket.md)**: API Gateways must support WebSocket protocol upgrades for real-time bidirectional communication, requiring special handling for persistent connection routing
- **[Rate Limiting](term_rate_limiting.md)**: Rate limiting is a core API Gateway responsibility -- the gateway enforces per-client, per-endpoint, and per-tier request quotas to protect backend services from overload and abuse
- **[Redis](term_redis.md)**: In-memory data store commonly used by API gateways for rate limiting state, response caching, and session management; provides the fast state layer that gateways need for per-request decisions
- **[REST](term_rest.md)**: REST is the dominant API paradigm that API Gateways route and manage -- most gateway configurations involve routing RESTful HTTP requests to backend services
- **[Reverse Proxy](term_reverse_proxy.md)**: An API Gateway is architecturally a reverse proxy with API-specific features layered on top -- both sit between clients and backend servers, forwarding requests
- **[gRPC](term_grpc.md)**: API Gateways perform protocol translation between client-facing REST/HTTP and internal gRPC services, enabling browser clients to access high-performance RPC backends transparently

## References

### External Sources
- Richardson, C. (2018). *Microservices Patterns*. Manning Publications. Chapter 8: External API Patterns.
- Newman, S. (2021). *Building Microservices* (2nd ed.). O'Reilly Media. — gateway as infrastructure concern
- [Microservices Pattern: API Gateway / Backends for Frontends](https://microservices.io/patterns/apigateway.html) — Chris Richardson's pattern catalog
- [API Gateway Deep Dive — Hello Interview](https://www.hellointerview.com/learn/system-design/deep-dives/api-gateway)
- [API Gateway — Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway)
- [Building Microservices: Using an API Gateway — NGINX / F5](https://www.f5.com/company/blog/nginx/building-microservices-using-an-api-gateway)
- [Wikipedia: API Management](https://en.wikipedia.org/wiki/API_management)
