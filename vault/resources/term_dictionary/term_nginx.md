---
tags:
  - resource
  - terminology
  - infrastructure
  - web_server
  - load_balancing
keywords:
  - NGINX
  - web server
  - reverse proxy
  - load balancer
  - HTTP cache
  - event-driven architecture
  - upstream
  - proxy_pass
  - worker processes
  - SSL termination
  - HTTP/2
  - gRPC proxy
  - C10K problem
  - epoll
  - non-blocking I/O
topics:
  - Infrastructure
  - Web Server Architecture
  - System Design
  - Load Balancing
  - Reverse Proxy
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: NGINX

## Definition

**NGINX** (pronounced "engine-x") is a high-performance, open-source web server, reverse proxy, load balancer, and HTTP cache originally created by Igor Sysoev in 2004 to solve the **C10K problem** -- handling 10,000+ concurrent connections efficiently on commodity hardware. Unlike traditional web servers such as Apache that use a thread-per-connection (or process-per-connection) model, NGINX employs an **asynchronous, event-driven, non-blocking architecture** that allows a small number of worker processes to handle tens of thousands of simultaneous connections with minimal memory overhead. As of 2026, NGINX powers over 34% of all active websites and is the most widely deployed web server and reverse proxy on the internet.

NGINX is often deployed as the entry point in modern distributed systems, sitting in front of application servers (Python/Gunicorn, Node.js, Java/Tomcat) to handle SSL termination, static file serving, request routing, rate limiting, and load balancing -- effectively acting as the infrastructure layer between clients and backend services.

## Full Name

**NGINX** (no official expansion; stylized as "nginx" in documentation)

**Also Known As**: nginx, Engine-X

## Context

NGINX occupies a central role in modern system design and infrastructure:

- **Web server**: Serves static content (HTML, CSS, JS, images) directly from disk with high concurrency and low memory footprint.
- **Reverse proxy**: Sits between clients and backend application servers, forwarding requests and returning responses while providing SSL termination, caching, compression, and request buffering.
- **Load balancer**: Distributes incoming traffic across multiple upstream servers using configurable algorithms (round robin, least connections, IP hash, consistent hashing).
- **HTTP cache**: Caches responses from upstream servers to reduce backend load and improve response latency.
- **API gateway**: In microservices architectures, NGINX (especially NGINX Plus) functions as an API gateway handling routing, authentication, rate limiting, and protocol translation (HTTP/2, gRPC, WebSocket).

NGINX is a foundational component in the infrastructure stack for abuse detection systems, serving as the front door for API endpoints that receive buyer/seller interactions, enforce rate limits against automated abuse, and route requests to downstream ML scoring services.

## Key Characteristics

### Event-Driven Architecture

NGINX uses a **master-worker process model**:

```
                ┌──────────────────────┐
                │    Master Process    │
                │  (config, signals,   │
                │   worker lifecycle)  │
                └──────┬───────────────┘
           ┌───────────┼───────────────┐
           ▼           ▼               ▼
    ┌────────────┐ ┌────────────┐ ┌────────────┐
    │  Worker 1  │ │  Worker 2  │ │  Worker N  │
    │ event loop │ │ event loop │ │ event loop │
    │  (epoll/   │ │  (epoll/   │ │  (epoll/   │
    │   kqueue)  │ │   kqueue)  │ │   kqueue)  │
    └────────────┘ └────────────┘ └────────────┘
```

- The **master process** reads configuration, binds to ports, and manages worker process lifecycle.
- Each **worker process** is single-threaded and runs an event loop using OS-level mechanisms (`epoll` on Linux, `kqueue` on BSD/macOS) to multiplex thousands of connections without spawning threads per connection.
- **Non-blocking I/O**: Workers never block on network or disk operations; they register interest in events and process them when ready, minimizing context switches and memory overhead.
- Theoretical max connections = `worker_processes` x `worker_connections` (commonly configured as `auto` x `10240`).

### Reverse Proxy and Upstream Configuration

NGINX forwards client requests to backend servers via the `proxy_pass` directive and manages pools of upstream servers:

```nginx
upstream backend_pool {
    least_conn;                    # Load balancing algorithm
    server 10.0.0.1:8080 weight=3;
    server 10.0.0.2:8080 weight=2;
    server 10.0.0.3:8080 backup;   # Failover only
    keepalive 32;                  # Persistent connections to backends
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate     /etc/ssl/certs/api.crt;
    ssl_certificate_key /etc/ssl/private/api.key;

    location /api/ {
        proxy_pass http://backend_pool;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Load Balancing Algorithms

| Algorithm | Directive | Behavior |
|-----------|-----------|----------|
| **Round Robin** | (default) | Distributes requests sequentially across upstream servers |
| **Least Connections** | `least_conn` | Routes to the server with fewest active connections |
| **IP Hash** | `ip_hash` | Hashes client IP for session persistence (sticky sessions) |
| **Generic Hash** | `hash $key` | Hashes arbitrary key (e.g., `$request_uri`) for consistent routing |
| **Random** | `random two least_conn` | Randomly picks two servers, selects the one with fewer connections |

### Health Checks and Failover

- **Passive health checks** (open-source): NGINX monitors backend responses; if a server returns errors, it is temporarily marked as failed (`max_fails`, `fail_timeout` parameters).
- **Active health checks** (NGINX Plus): Periodically sends health probe requests to upstream servers independent of client traffic.
- **Backup servers**: Servers marked with `backup` receive traffic only when all primary servers are unavailable.

### SSL/TLS Termination

NGINX handles TLS handshakes at the edge, offloading cryptographic operations from application servers:

- Supports TLS 1.2/1.3, OCSP stapling, session resumption, and HTTP Strict Transport Security (HSTS).
- Reduces backend complexity -- application servers communicate with NGINX over plain HTTP on internal networks.
- Enables centralized certificate management and renewal (often via Let's Encrypt / certbot).

### Protocol Support

| Protocol | Use Case |
|----------|----------|
| **HTTP/1.1** | Standard web traffic |
| **HTTP/2** | Multiplexed streams, header compression, server push |
| **gRPC** | Proxying gRPC services via `grpc_pass` directive |
| **WebSocket** | Real-time bidirectional communication via `proxy_http_version 1.1` + `Upgrade` headers |
| **TCP/UDP** | Layer 4 (stream) proxying for databases, mail, DNS |

### NGINX in System Design

```
┌──────────┐     ┌───────────────┐     ┌─────────────────────┐
│  Clients │────►│    NGINX       │────►│  Application Tier    │
│ (browser,│     │ - SSL termn.  │     │ ┌─────┐ ┌─────┐     │
│  mobile, │     │ - Static files│     │ │App 1│ │App 2│ ... │
│  API)    │     │ - Load balance│     │ └──┬──┘ └──┬──┘     │
└──────────┘     │ - Rate limit  │     │    │       │         │
                 │ - Caching     │     │ ┌──▼───────▼──┐      │
                 │ - Compression │     │ │  Database    │      │
                 └───────────────┘     │ └─────────────┘      │
                                       └─────────────────────┘
```

Common deployment patterns:

1. **Single reverse proxy**: NGINX in front of one or more application servers for SSL, caching, and buffering.
2. **Load balancer tier**: Multiple NGINX instances (active-passive or active-active with keepalived) distributing traffic across server pools.
3. **API gateway**: NGINX routing requests to different microservices based on URL path, headers, or methods.
4. **Sidecar proxy**: In Kubernetes, NGINX Ingress Controller serves as the cluster entry point, routing external traffic to internal services.

## NGINX vs. Apache vs. HAProxy

| Dimension | NGINX | Apache httpd | HAProxy |
|-----------|-------|-------------|---------|
| **Architecture** | Event-driven, non-blocking | Process/thread per connection (prefork/worker MPM) | Event-driven, single-process |
| **Primary strength** | Web server + reverse proxy + cache | Dynamic content (mod_php, .htaccess) | Pure load balancing / TCP proxy |
| **Concurrency** | Very high (C10K+) | Moderate (thread-limited) | Very high |
| **Static content** | Excellent | Good | N/A (not a web server) |
| **Configuration** | Declarative config files | .htaccess per-directory overrides | Declarative config files |
| **Use case** | General-purpose web/proxy tier | Legacy apps, shared hosting | Dedicated L4/L7 load balancer |

## NGINX Open Source vs. NGINX Plus

| Feature | Open Source | NGINX Plus |
|---------|-----------|------------|
| **Load balancing** | Round robin, least_conn, ip_hash, hash | + least_time, session persistence (sticky cookie/route) |
| **Health checks** | Passive only | Active + passive |
| **API gateway** | Basic routing | JWT auth, rate limiting per key, request validation |
| **Monitoring** | Stub status module | Live activity dashboard, JSON API |
| **Support** | Community | Commercial support from F5 |

## Related Terms

- **[Proxy Pattern](term_proxy_pattern.md)**: NGINX implements the proxy structural pattern -- it acts as a surrogate for backend servers, intercepting and forwarding requests while adding control logic (caching, auth, rate limiting)
- **[Event-Driven Architecture](term_event_driven_architecture.md)**: NGINX's internal architecture is event-driven -- worker processes use non-blocking event loops rather than thread-per-connection models, enabling massive concurrency
- **[Microservices Architecture](term_microservices_architecture.md)**: NGINX commonly serves as the API gateway and load balancer in microservices deployments, routing requests to independently deployed services
- **[Self-Supervised Learning (SSL)](term_ssl.md)**: Shares the SSL acronym but is unrelated; in the NGINX context, SSL/TLS refers to the cryptographic protocol for securing HTTP connections
- **[Kafka](term_kafka.md)**: In event-driven microservices stacks, NGINX handles synchronous HTTP/gRPC ingress while Kafka handles asynchronous event streaming between services
- **[CAP Theorem](term_cap_theorem.md)**: NGINX load balancing decisions interact with CAP trade-offs -- IP hash provides session consistency while round robin maximizes availability
- **[gRPC](term_grpc.md)**: NGINX natively supports gRPC proxying and load balancing via the `grpc_pass` directive, enabling HTTP/2-based RPC routing
- **[Service-Based Architecture](term_service_based_architecture.md)**: NGINX serves as the shared infrastructure layer in service-based architectures, providing centralized routing and cross-cutting concerns
- **[LRU Cache](term_lru_cache.md)**: NGINX's proxy cache uses LRU-like eviction policies to manage cached upstream responses within configured memory and disk limits
- **[Availability](term_availability.md)**: NGINX's passive and active health checks, failover to backup servers, and graceful reload (zero-downtime config changes) are availability engineering mechanisms
- **[Layered Architecture](term_layered_architecture.md)**: NGINX typically occupies the presentation/infrastructure layer in layered architectures, handling concerns before requests reach the application layer
- **[KV Cache](term_kv_cache.md)**: NGINX Plus includes an in-memory key-value store for dynamic configuration and session persistence, conceptually similar to external KV caches
- **[API Gateway](term_api_gateway.md)**: NGINX (especially NGINX Plus) functions as an API Gateway in microservices architectures, handling routing, authentication, rate limiting, and protocol translation alongside its reverse proxy capabilities
- **[Session Persistence](term_session_persistence.md)**: NGINX supports session persistence via IP hash and cookie-based sticky sessions, ensuring client requests reach the same backend server
- **[SSL Termination](term_ssl_termination.md)**: NGINX handles TLS termination at the edge, offloading cryptographic operations from application servers and enabling centralized certificate management
- **[WebSocket](term_websocket.md)**: NGINX natively proxies WebSocket connections via HTTP Upgrade headers, enabling real-time bidirectional communication through the reverse proxy layer
- **[HAProxy](term_haproxy.md)**: Often deployed alongside NGINX -- HAProxy as a dedicated Layer 4/7 load balancer in front, NGINX serving static content and application logic behind it
- **[Health Check](term_health_check.md)**: NGINX performs passive health checks in the open-source version and active health checks in NGINX Plus to detect and remove unhealthy upstream servers
- **[Rate Limiting](term_rate_limiting.md)**: NGINX provides built-in rate limiting via the `limit_req` and `limit_conn` directives, enforcing request-per-second and connection thresholds at the reverse proxy layer
- **[Reverse Proxy](term_reverse_proxy.md)**: NGINX is one of the most widely deployed reverse proxy implementations, sitting between clients and backend servers to handle SSL termination, caching, load balancing, and request routing
- **[Round Robin](term_round_robin.md)**: NGINX uses smooth weighted round robin as its default load balancing algorithm, interleaving requests across weighted upstream servers to prevent burst patterns
- **[Failover](term_failover.md)**: NGINX implements failover through backup server declarations in upstream blocks and passive/active health checks that automatically route traffic away from failed backends

## References

### External Sources
- Sysoev, I. (2004). NGINX. https://nginx.org/ -- Official open-source project
- [NGINX Documentation -- Admin Guide](https://docs.nginx.com/nginx/admin-guide/) -- Official configuration and deployment documentation
- [NGINX Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) -- Reverse proxy configuration guide
- [NGINX HTTP Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/) -- Load balancing algorithms and upstream configuration
- [NGINX SSL Termination](https://docs.nginx.com/nginx/admin-guide/security-controls/terminating-ssl-http/) -- SSL/TLS termination setup
- DeJonghe, D. (2019). *NGINX Cookbook*. O'Reilly Media. -- Practical recipes for common NGINX use cases
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. -- System design context for load balancing and reverse proxies
- Richards, M. & Ford, N. (2020). *Fundamentals of Software Architecture*. O'Reilly Media. -- Architectural patterns where NGINX serves as infrastructure glue
