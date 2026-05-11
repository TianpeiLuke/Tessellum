---
tags:
  - resource
  - terminology
  - system_design
  - networking
  - infrastructure
keywords:
  - reverse proxy
  - forward proxy
  - NGINX
  - HAProxy
  - Envoy
  - load balancing
  - SSL termination
  - caching
  - API gateway
  - Layer 7
  - Layer 4
  - web application firewall
  - rate limiting
topics:
  - system design fundamentals
  - networking infrastructure
  - web architecture
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: Reverse Proxy

## Definition

A **reverse proxy** is a server that sits between clients and one or more backend (origin) servers, intercepting client requests and forwarding them to the appropriate backend. The backend servers' responses flow back through the reverse proxy to the client. Crucially, clients interact only with the reverse proxy and have no direct knowledge of the backend servers behind it.

The key distinction is directionality:
- A **forward proxy** acts on behalf of **clients** -- it sits in front of clients and forwards their requests to the internet, hiding client identity from external servers (e.g., corporate proxies, VPNs).
- A **reverse proxy** acts on behalf of **servers** -- it sits in front of backend servers and forwards client requests to them, hiding server identity and topology from clients.

```
Forward Proxy:                    Reverse Proxy:

Client ──► [Forward Proxy] ──► Internet     Internet ──► [Reverse Proxy] ──► Backend Server A
Client ──►                  ──► Internet     Internet ──►                 ──► Backend Server B
                                             Internet ──►                 ──► Backend Server C
```

## Context

The reverse proxy is a foundational building block of modern web architecture. Nearly every production web system uses at least one reverse proxy layer. NGINX, HAProxy, Envoy, AWS ALB/ELB, Cloudflare, and Traefik are all implementations of the reverse proxy pattern. Understanding reverse proxies is essential for system design because they are the entry point through which most other infrastructure concerns (load balancing, TLS, caching, security) are implemented.

This term originates from the **SDDD Podcast Series -- Episode 2: Fundamentals**, which covers the core infrastructure primitives that appear repeatedly in system design discussions and interviews.

## Key Characteristics

### Forward Proxy vs Reverse Proxy

| Property | Forward Proxy | Reverse Proxy |
|----------|--------------|---------------|
| **Acts on behalf of** | Clients | Servers |
| **Hides** | Client identity from servers | Server identity/topology from clients |
| **Typical placement** | Client-side network edge | Server-side network edge |
| **Use cases** | Content filtering, anonymity, bypassing geo-restrictions | Load balancing, SSL termination, caching, security |
| **Examples** | Squid, corporate HTTP proxies, VPNs | NGINX, HAProxy, Envoy, AWS ALB |

### Core Functions of a Reverse Proxy

1. **Load Balancing**: Distributes incoming requests across multiple backend servers using algorithms such as round-robin, least connections, weighted distribution, or IP hash. This prevents any single server from becoming a bottleneck and enables horizontal scaling.

2. **SSL/TLS Termination**: Handles the computationally expensive TLS handshake and encryption/decryption at the proxy layer, forwarding unencrypted traffic to backend servers over a trusted internal network. This offloads CPU-intensive cryptographic operations from application servers.

3. **Caching**: Stores frequently requested responses (static assets, API responses) and serves them directly without forwarding to the backend, reducing latency and backend load.

4. **Compression**: Compresses responses (e.g., gzip, Brotli) before sending them to clients, reducing bandwidth usage.

5. **Security / Web Application Firewall (WAF)**: Shields backend servers from direct internet exposure. Can filter malicious requests, block IP ranges, enforce rate limits, and act as a WAF to mitigate common attacks (SQL injection, XSS, DDoS).

6. **Rate Limiting**: Throttles excessive requests from individual clients or IP addresses, protecting backend services from overload and abuse.

7. **Request Routing**: Routes requests to different backend services based on URL path, headers, or other request attributes -- enabling a single entry point for a microservices architecture.

### Implementations

| Software | Type | Notable Features |
|----------|------|-----------------|
| **NGINX** | Web server / reverse proxy | Event-driven architecture, high concurrency, low memory footprint |
| **HAProxy** | TCP/HTTP load balancer / proxy | Advanced health checking, connection draining, high availability |
| **Envoy** | Service mesh proxy | gRPC-native, observability, dynamic configuration via xDS API |
| **Traefik** | Cloud-native reverse proxy | Auto-discovery of services, Let's Encrypt integration |
| **AWS ALB/NLB** | Managed cloud load balancer | ALB (Layer 7), NLB (Layer 4), integrated with AWS ecosystem |
| **Cloudflare** | CDN / reverse proxy | Global edge network, DDoS protection, DNS integration |

### Reverse Proxy vs API Gateway vs Load Balancer

These terms overlap significantly but have distinct emphases:

| Component | Primary Concern | Additional Capabilities |
|-----------|----------------|------------------------|
| **Reverse Proxy** | Request forwarding and backend shielding | SSL termination, caching, compression |
| **Load Balancer** | Traffic distribution across backends | Health checking, session affinity, failover |
| **API Gateway** | API lifecycle management | Authentication, rate limiting, request transformation, API versioning, analytics |

In practice, many tools (NGINX, Envoy, AWS ALB) serve all three roles simultaneously. An API gateway is essentially a reverse proxy with API-specific features layered on top.

### Layer 4 vs Layer 7 Proxying

- **Layer 4 (Transport)**: Operates at the TCP/UDP level. Routes based on IP address and port. Faster but no visibility into HTTP content. Example: AWS NLB, HAProxy in TCP mode.
- **Layer 7 (Application)**: Operates at the HTTP/HTTPS level. Can inspect headers, URL paths, cookies, and body content. Enables content-based routing, header manipulation, and URL rewriting. Example: NGINX, AWS ALB, Envoy.

Most reverse proxies operate at Layer 7, which provides the richest routing and manipulation capabilities at the cost of slightly higher latency compared to Layer 4.

## Related Terms

### Infrastructure and Architecture
- **[Proxy Pattern](term_proxy_pattern.md)**: The GoF structural pattern underlying reverse proxies -- provides a surrogate to control access to another object
- **[Microservices Architecture](term_microservices_architecture.md)**: Reverse proxies serve as the unified entry point (ingress) for routing traffic to independently deployed microservices
- **[Event-Driven Architecture](term_event_driven_architecture.md)**: Reverse proxies handle synchronous ingress; EDA handles asynchronous internal communication -- complementary patterns
- **[Facade Pattern](term_facade_pattern.md)**: A reverse proxy acts as an infrastructure-level facade, providing a single simplified entry point to a complex backend topology
- **[CAP Theorem](term_cap_theorem.md)**: Reverse proxies with caching introduce consistency-availability trade-offs (stale cache vs backend availability)
- **[Space-Based Architecture](term_space_based_architecture.md)**: Architecture pattern that uses distributed caching and messaging; reverse proxies serve as the ingress layer
- **[Hexagonal Architecture](term_hexagonal_architecture.md)**: Reverse proxies sit at the infrastructure adapter boundary in ports-and-adapters design

### Design Principles
- **[Deep Modules](term_deep_modules.md)**: A reverse proxy is a deep module -- simple interface (accept HTTP requests) hiding substantial complexity (load balancing, SSL, caching, routing)
- **[Information Hiding](term_information_hiding.md)**: Reverse proxies hide backend topology, server count, and internal routing from clients
- **[Decorator Pattern](term_decorator_pattern.md)**: Reverse proxy layers (caching, compression, SSL) compose like decorators, each adding a cross-cutting concern

### Data and Caching
- **[LRU Cache](term_lru_cache.md)**: Common eviction policy used in reverse proxy caching layers
- **[Elasticsearch](term_elasticsearch.md)**: Distributed search engine often deployed behind a reverse proxy for load distribution and access control

### Security and Access
- **[Singleton](term_singleton.md)**: A reverse proxy is often a single point of entry (though deployed redundantly) -- the singleton gateway pattern for infrastructure
- **[API Gateway](term_api_gateway.md)**: An API Gateway is a reverse proxy extended with API-aware capabilities (authentication, rate limiting, request transformation, analytics) -- the reverse proxy is the foundational pattern upon which API Gateways are built
- **[Session Persistence](term_session_persistence.md)**: Reverse proxies implement session persistence (sticky sessions) via cookies or IP hash to ensure client requests reach the same backend server
- **[SSL Termination](term_ssl_termination.md)**: Reverse proxies handle TLS termination at the edge, decrypting traffic before forwarding to backends — a core function of reverse proxy deployments
- **[HAProxy](term_haproxy.md)**: Purpose-built open-source TCP/HTTP load balancer and reverse proxy with first-class Layer 4 support, active health checks, and extensive routing algorithms
- **[NGINX](term_nginx.md)**: High-performance event-driven web server and reverse proxy that handles SSL termination, static file serving, and Layer 7 load balancing with minimal memory overhead
- **[Rate Limiting](term_rate_limiting.md)**: Reverse proxies enforce rate limiting at the edge, throttling excessive requests before they reach backend services -- a key security and abuse prevention function
- **[Round Robin](term_round_robin.md)**: Round robin is the default load balancing algorithm used by reverse proxies (NGINX, HAProxy) to distribute requests across backend servers in sequential rotation
- **[Load Balancer](term_load_balancer.md)**: A load balancer is a specialized reverse proxy focused on traffic distribution -- in practice, most reverse proxies (NGINX, HAProxy, Envoy) serve both roles simultaneously

## References

- [What Is a Reverse Proxy? -- Cloudflare](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/)
- [NGINX Reverse Proxy Documentation](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Reverse Proxy -- Wikipedia](https://en.wikipedia.org/wiki/Reverse_proxy)
- [What Is a Reverse Proxy Server? -- NGINX](https://www.nginx.com/resources/glossary/reverse-proxy-server/)
- [HAProxy Documentation](https://www.haproxy.org/#desc)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs/envoy/latest/)
- [System Design Primer -- Reverse Proxy](https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server)
