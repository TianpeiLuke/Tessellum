---
tags:
  - resource
  - terminology
  - system_design
  - api_design
  - web_architecture
  - distributed_systems
keywords:
  - REST
  - Representational State Transfer
  - RESTful API
  - Roy Fielding
  - HTTP methods
  - stateless
  - HATEOAS
  - Richardson Maturity Model
  - resource-oriented design
  - API design
  - uniform interface
  - content negotiation
topics:
  - System Design
  - API Architecture
  - Web Architecture
  - Distributed Systems
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# REST (Representational State Transfer)

## Definition

**REST (Representational State Transfer)** is an architectural style for distributed hypermedia systems, defined by **Roy Fielding** in his 2000 doctoral dissertation *"Architectural Styles and the Design of Network-based Software Architectures"* at UC Irvine. Fielding, a principal author of the HTTP/1.0 and HTTP/1.1 specifications, derived REST by analyzing the constraints that made the World Wide Web successful at Internet scale. REST defines **six constraints** — client-server, stateless, cacheable, uniform interface, layered system, and code-on-demand (optional) — that, when followed, produce scalable, loosely-coupled, independently evolvable web services. A service that adheres to these constraints is called **RESTful**. REST is not a protocol or a standard; it is a set of architectural constraints that guide the design of networked applications.

## Context

REST is the **dominant API paradigm for web services**. The vast majority of public-facing APIs (e.g., GitHub, Stripe, Twitter/X, AWS) expose RESTful interfaces. Within system design, REST is constantly compared against two other major API paradigms:

- **gRPC** — Google's high-performance RPC framework using Protocol Buffers and HTTP/2; preferred for internal microservice-to-microservice communication where latency and type safety matter
- **GraphQL** — Facebook's query language for APIs that lets clients request exactly the data they need; preferred for complex client-facing UIs with diverse data requirements

REST remains the default choice for **public APIs** due to its simplicity, universal HTTP support, excellent cacheability (CDNs, browser caches), and the ubiquity of tooling. The SDDD podcast series discusses REST in the context of system design fundamentals and API architecture decisions.

## Key Characteristics

### The Six REST Constraints

| # | Constraint | Description | Consequence |
|---|-----------|-------------|-------------|
| 1 | **Client-Server** | Separation of concerns between UI (client) and data storage (server) | Independent evolution of client and server; portability of client across platforms |
| 2 | **Stateless** | Each request from client to server must contain all information needed to understand the request; no session state stored on server | Scalability (any server can handle any request); reliability; visibility for monitoring |
| 3 | **Cacheable** | Responses must explicitly or implicitly label themselves as cacheable or non-cacheable | Reduces client-server interactions; improves scalability and performance via CDNs and browser caches |
| 4 | **Uniform Interface** | A standardized way to communicate between client and server (see sub-constraints below) | Simplicity; decoupling; independent evolvability of components |
| 5 | **Layered System** | Architecture can be composed of hierarchical layers; each component cannot "see" beyond its immediate layer | Load balancers, proxies, gateways, and caches can be inserted transparently; security enforcement at layer boundaries |
| 6 | **Code-on-Demand** *(optional)* | Servers can extend client functionality by transferring executable code (e.g., JavaScript) | Reduces pre-implemented client features; the only optional constraint |

### Uniform Interface Sub-Constraints

The uniform interface is the **defining feature** of REST, distinguishing it from other network-based styles. It comprises four sub-constraints:

1. **Identification of resources** — Each resource is identified by a URI (e.g., `/orders/123`)
2. **Manipulation of resources through representations** — Clients hold representations (JSON, XML) of resources and can modify the resource by sending modified representations back to the server
3. **Self-descriptive messages** — Each message contains enough information to describe how to process it (Content-Type, status codes, cache headers)
4. **Hypermedia as the Engine of Application State (HATEOAS)** — Clients discover available actions through hyperlinks embedded in responses, rather than relying on out-of-band documentation

### Resource-Oriented Design

REST is fundamentally **resource-oriented**, not action-oriented:

```
Resources (nouns), not actions (verbs):

  Good:    GET    /orders/123
  Bad:     GET    /getOrder?id=123

  Good:    POST   /orders
  Bad:     POST   /createOrder

  Good:    DELETE /orders/123/items/456
  Bad:     POST   /deleteOrderItem
```

### HTTP Methods and Their Semantics

| Method | CRUD | Idempotent | Safe | Request Body | Typical Use |
|--------|------|-----------|------|-------------|-------------|
| **GET** | Read | Yes | Yes | No | Retrieve a resource or collection |
| **POST** | Create | No | No | Yes | Create a new resource; trigger processing |
| **PUT** | Update (full) | Yes | No | Yes | Replace a resource entirely |
| **PATCH** | Update (partial) | No* | No | Yes | Modify specific fields of a resource |
| **DELETE** | Delete | Yes | No | No | Remove a resource |
| **HEAD** | Read metadata | Yes | Yes | No | Retrieve headers only (no body) |
| **OPTIONS** | Discovery | Yes | Yes | No | Discover allowed methods on a resource |

*PATCH can be made idempotent depending on the patch format used.

### HTTP Status Codes

| Range | Category | Common Codes |
|-------|----------|-------------|
| **2xx** | Success | `200 OK`, `201 Created`, `204 No Content` |
| **3xx** | Redirection | `301 Moved Permanently`, `304 Not Modified` |
| **4xx** | Client Error | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `429 Too Many Requests` |
| **5xx** | Server Error | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

### Richardson Maturity Model

Leonard Richardson (2008) defined four maturity levels for RESTful APIs:

```
Level 3: Hypermedia Controls (HATEOAS)        ← "Glory of REST"
         Responses contain links to related resources
         and available actions — self-documenting API
         ┆
Level 2: HTTP Verbs
         Proper use of GET, POST, PUT, DELETE,
         status codes, and HTTP semantics
         ┆
Level 1: Resources
         Individual URIs for distinct resources
         (e.g., /orders/123 vs. /orders/456)
         ┆
Level 0: The Swamp of POX (Plain Old XML)
         Single endpoint, single HTTP method (POST),
         RPC-style tunneling (e.g., SOAP)
```

Most production REST APIs operate at **Level 2**. True Level 3 (HATEOAS) adoption remains rare in practice, though it represents Fielding's original vision of RESTful design.

### Content Negotiation

Clients and servers negotiate representation formats via HTTP headers:

| Header | Direction | Purpose | Example |
|--------|-----------|---------|---------|
| `Accept` | Request | Client's preferred response format | `Accept: application/json` |
| `Content-Type` | Both | Format of the message body | `Content-Type: application/json` |
| `Accept-Language` | Request | Preferred language | `Accept-Language: en-US` |
| `Accept-Encoding` | Request | Preferred compression | `Accept-Encoding: gzip` |

### REST vs. gRPC vs. GraphQL

| Dimension | REST | gRPC | GraphQL |
|-----------|------|------|---------|
| **Protocol** | HTTP/1.1 (also HTTP/2) | HTTP/2 | HTTP (single endpoint) |
| **Data format** | JSON (text-based) | Protocol Buffers (binary) | JSON |
| **Contract** | OpenAPI/Swagger (optional) | `.proto` files (required) | Schema + SDL (required) |
| **Performance** | Baseline | 5-10x faster than REST | Slightly slower than REST |
| **Caching** | Excellent (CDN, browser, HTTP caching) | No native HTTP caching | Difficult (single endpoint) |
| **Browser support** | Native | Requires gRPC-Web proxy | Native |
| **Streaming** | Limited (SSE, WebSocket) | Native bidirectional streaming | Subscriptions |
| **Over/under-fetching** | Common problem | Fixed by contract | Solved (client specifies fields) |
| **Tooling maturity** | Highest | Growing | High |
| **Best for** | Public APIs, CRUD, cacheable resources | Internal microservices, low-latency RPC | Complex client UIs, mobile apps |
| **Adoption** | Universal default | De facto for internal microservices | 50%+ enterprise adoption (2026) |

### RESTful API Design Best Practices

1. **Use nouns, not verbs** — Resources are nouns (`/users`, `/orders`); HTTP methods provide the verbs
2. **Use plural resource names** — `/users/123` not `/user/123`
3. **Nest for relationships** — `/users/123/orders` for user's orders
4. **Version your API** — `/v1/users` or `Accept: application/vnd.api.v1+json`
5. **Use query parameters for filtering** — `GET /orders?status=pending&sort=-created_at`
6. **Return proper status codes** — `201` for creation, `204` for deletion, `404` for not found
7. **Paginate collections** — `GET /orders?page=2&per_page=25` with `Link` headers
8. **Support partial responses** — `GET /users/123?fields=name,email`
9. **Use HATEOAS links** — Include `_links` or `links` in responses for discoverability
10. **Idempotency keys** — For `POST` requests, accept client-generated idempotency keys to enable safe retries

### Limitations of REST

| Limitation | Description | Mitigation |
|-----------|-------------|------------|
| **Over-fetching** | API returns more data than the client needs (e.g., full user object when only the name is needed) | Field selection (`?fields=`), GraphQL for complex cases |
| **Under-fetching** | Client must make multiple requests to assemble needed data (e.g., user + orders + payments) | Compound documents, embedded resources, GraphQL |
| **Chatty APIs** | Fine-grained resources lead to many round-trips; N+1 request problem | Backend-for-Frontend (BFF) pattern, batch endpoints |
| **No native real-time** | HTTP request-response is inherently pull-based | Server-Sent Events (SSE), WebSockets, long polling |
| **Versioning complexity** | Breaking changes require API versioning strategies | URL versioning, header versioning, or careful evolution |
| **Lack of contract enforcement** | OpenAPI specs are optional; drift between docs and implementation is common | Code-generated clients, contract testing |

## Related Terms

### API Architecture and Communication
- **[Microservices Architecture](term_microservices_architecture.md)** — REST is the most common inter-service communication protocol in microservices; API gateways route REST calls to individual services
- **[Event-Driven Architecture](term_event_driven_architecture.md)** — Asynchronous alternative to REST's synchronous request-response pattern; often combined with REST for different interaction types
- **[Proxy Pattern](term_proxy_pattern.md)** — REST APIs are commonly fronted by reverse proxies, API gateways, and load balancers that operate transparently within REST's layered system constraint
- **[Service-Based Architecture](term_service_based_architecture.md)** — Coarser-grained architecture style where services communicate via REST APIs over a shared database

### Software Architecture Principles
- **[Hexagonal Architecture](term_hexagonal_architecture.md)** — REST controllers are driving adapters that plug into application-core ports; REST is an interchangeable delivery mechanism
- **[SOLID](term_solid.md)** — Interface Segregation Principle (ISP) maps to well-designed REST resource interfaces; Dependency Inversion keeps REST controllers as thin adapters
- **[Deep Modules](term_deep_modules.md)** — Well-designed REST endpoints are deep modules: simple URI interface hiding complex server-side logic
- **[Information Hiding](term_information_hiding.md)** — REST's uniform interface hides server implementation details; clients interact only with resource representations

### Distributed Systems
- **[CAP Theorem](term_cap_theorem.md)** — REST's statelessness constraint simplifies horizontal scaling but pushes consistency challenges to the data layer
- **[Availability](term_availability.md)** — REST's layered system and statelessness enable high availability through load balancing and redundancy
- **[Kafka](term_kafka.md)** — REST APIs often produce events to Kafka topics; REST for synchronous queries, Kafka for asynchronous event streaming

### Data and Caching
- **[KV Cache](term_kv_cache.md)** — REST responses are commonly cached in key-value stores (Redis, Memcached) keyed by URI + query parameters
- **[LRU Cache](term_lru_cache.md)** — HTTP caching (Cache-Control, ETag, Last-Modified) enables LRU-style eviction in CDNs and browser caches
- **[Schema Evolution](term_schema_evolution.md)** — REST API versioning is a form of schema evolution; backward-compatible changes avoid breaking clients

- **[GraphQL](term_graphql.md)**: Client-driven query language for APIs that solves REST's over-fetching and under-fetching problems by letting clients specify exactly the data they need
- **[API Gateway](term_api_gateway.md)**: REST APIs are commonly fronted by API Gateways that handle authentication, rate limiting, and request routing, operating within REST's layered system constraint

### Amazon Internal REST Services
- **[Dryad](term_dryad.md)**: DryadService — Cradle's REST API for programmatic job management; example of internal REST service with AAA authentication over VPC endpoints
- **[WebSocket](term_websocket.md)**: WebSocket provides the real-time bidirectional communication that REST's request-response model cannot — REST applications use WebSocket for live updates, chat, and streaming
- **[gRPC](term_grpc.md)**: High-performance RPC framework using Protocol Buffers and HTTP/2 -- gRPC is the primary alternative to REST for internal microservice communication, offering 5-10x faster serialization and native bidirectional streaming

## References

### Vault Sources
- [Digest: SDDD Fundamentals Podcast](../digest/digest_sddd_fundamentals_podcast.md) — System design fundamentals including API design paradigms and REST principles
- [Digest: SDDD Series](../digest/digest_sddd_series.md) — System Design Deep Dive podcast series covering REST in the context of distributed system architecture
- [Digest: Fundamentals of Software Architecture (Richards & Ford)](../digest/digest_fundamentals_software_architecture_richards.md) — Architecture styles and communication patterns including REST

### External Sources
- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. Doctoral dissertation, University of California, Irvine. Chapter 5: Representational State Transfer (REST). — [https://roy.gbiv.com/pubs/dissertation/rest_arch_style.htm](https://roy.gbiv.com/pubs/dissertation/rest_arch_style.htm)
- Richardson, L. (2008). *Richardson Maturity Model*. — [https://martinfowler.com/articles/richardsonMaturityModel.html](https://martinfowler.com/articles/richardsonMaturityModel.html)
- [REST API Tutorial](https://restfulapi.net/) — Comprehensive reference for RESTful API design principles and constraints
- [Wikipedia: Representational State Transfer](https://en.wikipedia.org/wiki/Representational_state_transfer) — Encyclopedic overview of REST's history, constraints, and adoption
- Masse, M. (2011). *REST API Design Rulebook*. O'Reilly Media. — Practical design rules for RESTful APIs
- Richardson, L. & Amundsen, M. (2013). *RESTful Web APIs*. O'Reilly Media. — Resource-oriented design and hypermedia patterns

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Architectural style for distributed hypermedia systems |
| **Originator** | Roy Fielding (2000 doctoral dissertation) |
| **Core principle** | Six constraints that produce scalable, loosely-coupled web services |
| **Communication** | Synchronous HTTP request-response with resource-oriented URIs |
| **Data format** | JSON (de facto standard), XML, or any negotiated representation |
| **Key strength** | Simplicity, cacheability, universal tooling, browser-native |
| **Key weakness** | Over-fetching, under-fetching, chatty APIs, no native streaming |
| **Maturity model** | Richardson Maturity Model: Level 0 (POX) through Level 3 (HATEOAS) |
| **Alternatives** | gRPC (performance), GraphQL (flexible queries) |

**Key Insight**: REST's power lies not in any specific technology but in its *constraints*. Each constraint trades a degree of implementation freedom for a specific architectural property: statelessness yields horizontal scalability, cacheability yields performance, uniform interface yields simplicity and independent evolvability, and layered system yields operational flexibility. Fielding did not invent REST as a theoretical exercise — he *derived* it by studying what made the existing Web architecture successful. This means REST is less a design to be implemented and more a set of constraints to be *honored*. The most common mistake in "RESTful" API design is adopting REST's surface vocabulary (URIs, JSON, HTTP methods) while violating its deeper constraints (statelessness, HATEOAS, self-descriptive messages) — producing Level 2 APIs that work well enough in practice but miss the full architectural benefits Fielding described.

---

**Last Updated**: April 19, 2026
**Status**: Active — foundational API architecture paradigm for system design
