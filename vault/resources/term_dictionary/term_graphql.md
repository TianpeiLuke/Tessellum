---
tags:
  - resource
  - terminology
  - system_design
  - api_design
  - networking
keywords:
  - GraphQL
  - query language
  - API
  - single endpoint
  - schema definition language
  - SDL
  - resolver
  - type system
  - over-fetching
  - under-fetching
  - Apollo
  - Relay
  - introspection
  - DataLoader
  - N+1 problem
  - fragment
  - mutation
  - subscription
topics:
  - System Design
  - API Design
  - Networking
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: GraphQL

## Definition

**GraphQL** is a **query language for APIs** and a server-side runtime for executing those queries, developed internally at Facebook in 2012 and open-sourced in 2015. Unlike REST, where the server defines the shape and size of each resource response, GraphQL lets **clients specify exactly what data they need** in a single request. A GraphQL service is defined by a **strongly typed schema** -- types and their fields -- backed by **resolver functions** that produce data for each field. This schema-first, client-driven approach solves the chronic REST problems of **over-fetching** (receiving more data than needed) and **under-fetching** (requiring multiple round-trips to assemble a complete view). GraphQL operates through a **single endpoint**, supports queries (reads), mutations (writes), and subscriptions (real-time push), and provides built-in **introspection** so clients can discover the API's capabilities programmatically.

## Context

GraphQL emerged from Facebook's need to efficiently power its mobile News Feed, where bandwidth constraints and diverse client requirements made REST endpoints impractical. The 2015 open-source release, accompanied by a formal specification, catalyzed rapid adoption by GitHub (2016), Shopify, Airbnb, Twitter, and the broader industry. Today GraphQL is governed by the GraphQL Foundation under the Linux Foundation, with implementations available in every major programming language and mature client libraries such as Apollo Client and Relay. In system design, GraphQL occupies the API layer between clients and backend services, often sitting in front of microservices, databases, or legacy REST APIs as a unified data-fetching interface.

## Key Characteristics

### Core Operations

| Operation | Purpose | Example |
|-----------|---------|---------|
| **Query** | Read data; clients select fields and nesting depth | `{ user(id: "1") { name, email } }` |
| **Mutation** | Write data; create, update, or delete resources | `mutation { createUser(name: "Ada") { id } }` |
| **Subscription** | Real-time push; server streams updates over WebSocket | `subscription { orderStatusChanged { id, status } }` |

### Type System and Schema

GraphQL enforces a **strong, static type system** defined in the Schema Definition Language (SDL). Every field has a declared type, and the schema serves as the contract between client and server.

```graphql
type Query {
  user(id: ID!): User
  orders(buyerId: ID!, limit: Int = 10): [Order!]!
}

type User {
  id: ID!
  name: String!
  email: String
  orders: [Order!]!
}

type Order {
  id: ID!
  total: Float!
  status: OrderStatus!
  items: [Item!]!
}

enum OrderStatus {
  PENDING
  SHIPPED
  DELIVERED
  CANCELLED
}
```

### Resolvers

Resolvers are functions that produce the value for each field in the schema. The GraphQL execution engine walks the query tree and invokes the appropriate resolver for every field, assembling the result into a JSON response that mirrors the query shape.

```javascript
const resolvers = {
  Query: {
    user: (_, { id }, context) => context.db.getUserById(id),
    orders: (_, { buyerId, limit }, context) =>
      context.db.getOrdersByBuyer(buyerId, limit),
  },
  User: {
    orders: (user, _, context) =>
      context.db.getOrdersByBuyer(user.id),
  },
};
```

### Over-Fetching vs Under-Fetching

| Problem | REST Behavior | GraphQL Solution |
|---------|--------------|-----------------|
| **Over-fetching** | `GET /users/1` returns all 30 fields even when client needs only `name` | Client selects `{ user { name } }` -- only `name` is returned |
| **Under-fetching** | Need user + orders + items requires 3 sequential requests | Single query nests `user { orders { items } }` in one round-trip |

### Introspection

GraphQL schemas are self-documenting. Clients can query the `__schema` and `__type` meta-fields to discover available types, fields, arguments, and deprecation status at runtime. This powers tooling such as GraphiQL, Apollo Studio, and automatic SDK generation.

```graphql
{
  __schema {
    types { name, kind }
    queryType { name }
  }
}
```

### Versionless Evolution

New fields and types can be added without breaking existing clients. Deprecated fields are annotated with `@deprecated(reason: "...")` and gradually removed, eliminating the need for versioned endpoints (`/v1/`, `/v2/`).

## The N+1 Query Problem

Because GraphQL resolves each field independently, a naive implementation can produce **N+1 database queries** -- one query to fetch a list of N items, then N additional queries to resolve a related field for each item. For example, fetching 20 orders and then resolving the buyer for each order triggers 21 database calls.

**Solution -- DataLoader**: The DataLoader pattern (originated by Facebook) batches and deduplicates resolver calls within a single request tick. Instead of N individual lookups, DataLoader collects all requested keys and issues a single batched query, reducing 21 queries to 2.

```javascript
// Without DataLoader: 21 queries
// With DataLoader: 2 queries (1 for orders, 1 batched for buyers)
const buyerLoader = new DataLoader(ids =>
  db.getBuyersByIds(ids)  // single SELECT ... WHERE id IN (...)
);
```

## GraphQL vs REST vs gRPC

| Dimension | GraphQL | REST | gRPC |
|-----------|---------|------|------|
| **Data fetching** | Client specifies exact fields | Server defines fixed response shape | Server defines via Protobuf messages |
| **Endpoints** | Single endpoint (`/graphql`) | Multiple resource endpoints | Multiple service methods |
| **Transport** | HTTP (typically POST) | HTTP (GET, POST, PUT, DELETE) | HTTP/2 with Protocol Buffers |
| **Typing** | Strong schema (SDL) | Informal (OpenAPI optional) | Strong (Protobuf IDL) |
| **Over/under-fetching** | Eliminated by design | Common problem | Less common (designed per RPC) |
| **Real-time** | Subscriptions (WebSocket) | Polling or SSE | Bidirectional streaming |
| **Caching** | Complex (single endpoint breaks HTTP caching) | Native HTTP caching (ETags, Cache-Control) | Custom caching required |
| **Performance** | Good for complex nested reads | Good for simple CRUD | Best for high-throughput internal RPC |
| **Browser support** | Native | Native | Requires gRPC-Web proxy |
| **Best for** | Client-driven UIs, mobile, BFF | Public APIs, simple CRUD, broad ecosystem | Internal microservice communication |

## Architecture Patterns

### Backend for Frontend (BFF)

GraphQL frequently serves as a **Backend for Frontend** layer, aggregating data from multiple microservices into a single, client-tailored API. Each frontend (web, mobile, IoT) queries the same GraphQL endpoint but requests different field subsets.

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│  Web    │  │ Mobile  │  │   IoT   │
│ Client  │  │ Client  │  │ Client  │
└────┬────┘  └────┬────┘  └────┬────┘
     └────────────┼────────────┘
            ┌─────┴──────┐
            │  GraphQL   │
            │  Gateway   │
            └─────┬──────┘
     ┌────────────┼────────────┐
┌────┴────┐ ┌────┴────┐ ┌────┴────┐
│ User    │ │ Order   │ │ Payment │
│ Service │ │ Service │ │ Service │
└─────────┘ └─────────┘ └─────────┘
```

### Schema Federation

**Apollo Federation** enables multiple teams to own independent subgraphs that compose into a single supergraph. Each service defines its portion of the schema, and a gateway (Apollo Router) merges them at runtime -- critical for scaling GraphQL across large organizations with microservices.

### Security Considerations

| Concern | Mitigation |
|---------|-----------|
| **Query complexity attacks** | Query depth limiting, complexity scoring, cost analysis |
| **Introspection in production** | Disable introspection on public-facing endpoints |
| **Denial of service** | Rate limiting, persisted queries (allowlist), timeout enforcement |
| **Authorization** | Field-level authorization in resolvers; never rely solely on schema visibility |
| **Injection** | Parameterized arguments prevent injection; validate input types |

## Key Ecosystem

| Tool / Library | Role |
|---------------|------|
| **Apollo Server / Client** | Most popular full-stack GraphQL framework |
| **Relay** | Facebook's GraphQL client optimized for React |
| **GraphiQL** | In-browser IDE for exploring GraphQL APIs |
| **Hasura** | Instant GraphQL API over PostgreSQL/databases |
| **AWS AppSync** | Managed GraphQL service on AWS |
| **Apollo Federation / Router** | Schema composition for microservices |
| **Prisma** | ORM with GraphQL-friendly data access layer |
| **graphql-codegen** | Generates typed SDKs from schemas |

## Related Terms

### API and System Design
- **[Microservices Architecture](term_microservices_architecture.md)** -- GraphQL often serves as the unified API gateway aggregating data from multiple microservices
- **[Event-Driven Architecture](term_event_driven_architecture.md)** -- GraphQL subscriptions complement EDA by pushing real-time event updates to clients over WebSocket
- **[Facade Pattern](term_facade_pattern.md)** -- GraphQL gateway acts as a facade, presenting a unified interface over heterogeneous backend services
- **[CAP Theorem](term_cap_theorem.md)** -- GraphQL resolvers that aggregate data from distributed services face consistency-vs-availability trade-offs

### Data and Graph Technologies
- **[Knowledge Graph](term_knowledge_graph.md)** -- GraphQL can serve as the query interface for knowledge graph APIs; both use graph-structured thinking but at different layers (API vs data model)
- **[Neptune](term_neptune.md)** -- AWS AppSync can front Neptune graph databases with a GraphQL API, combining graph storage with client-driven querying
- **[MongoDB](term_mongodb.md)** -- Document databases pair naturally with GraphQL resolvers; MongoDB Atlas provides a native GraphQL API
- **[NoSQL](term_nosql.md)** -- GraphQL's flexible query model aligns well with schema-flexible NoSQL backends

### Caching and Performance
- **[LRU Cache](term_lru_cache.md)** -- DataLoader uses per-request caching to deduplicate resolver calls; server-side LRU caches complement GraphQL's lack of native HTTP caching
- **[Schema Evolution](term_schema_evolution.md)** -- GraphQL's versionless API evolution through additive changes and `@deprecated` directives is a form of schema evolution

### API Infrastructure
- **[API Gateway](term_api_gateway.md)**: GraphQL servers often sit behind or function as API Gateways; the gateway handles cross-cutting concerns (auth, rate limiting, SSL) while GraphQL handles query resolution and data aggregation
- **[WebSocket](term_websocket.md)**: GraphQL subscriptions use WebSocket as the transport protocol for real-time, bidirectional push updates from server to client

### Architecture Patterns
- **[Star Schema](term_star_schema.md)** -- Both GraphQL schemas and star schemas model data as a central type with radiating relationships, though at different abstraction levels (API vs warehouse)
- **[Directed Acyclic Graph](term_directed_acyclic_graph.md)** -- GraphQL query execution follows a DAG of resolver invocations from root to leaf fields
- **[REST](term_rest.md)**: REST is GraphQL's primary alternative for API design -- REST uses multiple resource endpoints with server-defined responses, while GraphQL uses a single endpoint with client-specified queries, solving REST's over-fetching and under-fetching problems
- **[gRPC](term_grpc.md)**: gRPC is the third major API paradigm alongside GraphQL and REST -- gRPC excels at high-throughput internal microservice communication while GraphQL excels at flexible client-facing data fetching

## References

### Specification and Documentation
- GraphQL Foundation. *GraphQL Specification*. https://spec.graphql.org/
- GraphQL Foundation. *GraphQL: A query language for your API*. https://graphql.org/
- GraphQL Foundation. *Learn GraphQL*. https://graphql.org/learn/

### External Sources
- Buna, S. (2021). *GraphQL in Action*. Manning Publications.
- Banks, A. & Porcello, E. (2018). *Learning GraphQL*. O'Reilly Media.
- [Apollo GraphQL Documentation](https://www.apollographql.com/docs/) -- Federation, client, server guides
- [Wikipedia: GraphQL](https://en.wikipedia.org/wiki/GraphQL)
- [REST vs. GraphQL vs. gRPC -- Baeldung](https://www.baeldung.com/rest-vs-graphql-vs-grpc)
- [AWS AppSync Developer Guide](https://docs.aws.amazon.com/appsync/) -- Managed GraphQL on AWS

## Summary

| Aspect | Details |
|--------|---------|
| **Full Name** | GraphQL (Graph Query Language) |
| **Type** | API query language and server-side runtime |
| **Created By** | Facebook (2012 internal, 2015 open-source) |
| **Governance** | GraphQL Foundation (Linux Foundation) |
| **Core Idea** | Clients request exactly the data they need via a typed schema |
| **Operations** | Query (read), Mutation (write), Subscription (real-time) |
| **Type System** | Strong, static types defined in SDL; schema is the API contract |
| **Key Advantage** | Eliminates over-fetching and under-fetching; single endpoint |
| **Key Challenge** | N+1 queries (solved by DataLoader), caching complexity, query cost control |
| **vs REST** | More efficient data fetching; harder to cache; single endpoint vs multiple |
| **vs gRPC** | Better for client-facing APIs; gRPC better for internal high-throughput RPC |
| **Key Ecosystem** | Apollo, Relay, Hasura, AWS AppSync, GraphiQL |

**Key Insight**: GraphQL inverts the traditional API power dynamic. In REST, the server dictates what data each endpoint returns, forcing clients to either accept surplus data (over-fetching) or chain multiple requests (under-fetching). GraphQL transfers control to the client: the schema defines what is *possible*, but the query defines what is *returned*. This makes GraphQL exceptionally well-suited for scenarios with diverse clients (web, mobile, IoT) consuming the same backend -- each client queries exactly what it needs without requiring dedicated endpoints. The trade-off is that this flexibility shifts complexity to the server: resolvers must handle arbitrary query shapes, the N+1 problem requires DataLoader-style batching, HTTP caching no longer works out of the box, and unbounded queries can become denial-of-service vectors without depth limiting and complexity analysis. In microservices architectures, GraphQL's role as a unified aggregation layer (via federation or BFF pattern) makes it a natural complement to service meshes and API gateways.

---

**Last Updated**: April 19, 2026
**Status**: Active - foundational API design concept in system design
**Related Concepts**: REST, gRPC, API Gateway, Schema Definition Language, Apollo Federation
