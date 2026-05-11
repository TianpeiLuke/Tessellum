---
tags:
  - resource
  - terminology
  - infrastructure
  - load_balancing
  - networking
keywords:
  - HAProxy
  - high availability proxy
  - load balancer
  - reverse proxy
  - Layer 4
  - Layer 7
  - TCP proxy
  - HTTP proxy
  - ACL routing
  - health check
  - sticky session
  - session persistence
  - SSL termination
  - round robin
  - least connections
  - failover
  - backend server
  - frontend
topics:
  - Infrastructure
  - Load Balancing
  - Networking
  - Distributed Systems
  - High Availability
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: HAProxy (High Availability Proxy)

## Definition

**HAProxy** (**H**igh **A**vailability **Proxy**) is a free, open-source load balancer and reverse proxy for TCP and HTTP applications. Originally written by Willy Tarreau in 2000, HAProxy has become the industry-standard software load balancer, used by organizations including GitHub, Airbnb, Alibaba, and Twitter to distribute traffic across backend servers, ensure high availability, and improve application performance. HAProxy operates at both **Layer 4 (Transport — TCP)** and **Layer 7 (Application — HTTP)** of the OSI model, enabling flexible traffic management strategies ranging from simple TCP forwarding to content-aware HTTP routing.

## Context

In distributed systems and microservices architectures, no single server can handle all incoming traffic or guarantee uninterrupted uptime. HAProxy sits between clients and backend servers as a reverse proxy, distributing requests according to configurable algorithms and automatically removing unhealthy servers from the rotation. For abuse prevention infrastructure, HAProxy is relevant as the traffic entry point where rate limiting, connection throttling, and ACL-based access control can be enforced before requests reach application servers. Understanding HAProxy is also essential for comprehending how services like API gateways, CDNs, and service meshes manage request routing and availability at scale.

## Key Characteristics

### Layer 4 vs. Layer 7 Load Balancing

| Aspect | Layer 4 (TCP Mode) | Layer 7 (HTTP Mode) |
|--------|-------------------|---------------------|
| **OSI Layer** | Transport | Application |
| **Routing basis** | IP address and TCP port | HTTP headers, paths, cookies, query strings |
| **Inspection depth** | Does not read message content | Full HTTP request/response inspection |
| **Performance** | Faster — fewer processing steps | Slightly slower — parses HTTP protocol |
| **Use cases** | Database proxying, mail servers, generic TCP services | Web applications, APIs, multi-app routing under one domain |
| **Benefits** | Health checks, connection queuing, rate limiting connections, hiding internal topology | Content-based routing, HTTP header manipulation, cookie-based persistence, request-level rate limiting |

### Configuration Architecture

HAProxy configuration is organized into four major sections:

| Section | Purpose |
|---------|---------|
| **global** | Process-wide settings: logging, max connections, chroot, user/group |
| **defaults** | Default parameters inherited by frontend and backend sections |
| **frontend** | Defines the listening socket (bind address/port), accepts client connections, applies ACL rules, routes to backends |
| **backend** | Defines the pool of servers that fulfill requests, specifies load balancing algorithm, health checks, and persistence |

A **listen** section can combine frontend and backend into a single block for simpler configurations.

### Load Balancing Algorithms

| Algorithm | Behavior | Best For |
|-----------|----------|----------|
| **roundrobin** | Cycles through servers sequentially (default) | Equal-capacity servers, stateless applications |
| **leastconn** | Routes to server with fewest active connections | Long-lived connections (WebSocket, database) |
| **source** | Hashes client IP for consistent server mapping | Simple session persistence without cookies |
| **uri** | Hashes the request URI | Cache optimization — same URI always hits same cache server |
| **hdr(name)** | Hashes a specified HTTP header value | Routing by custom application headers |
| **first** | Fills servers sequentially to capacity before using next | Minimizing active server count for cost savings |

### ACL-Based Routing

Access Control Lists (ACLs) are conditional expressions evaluated against request attributes (path, host header, source IP, HTTP method). ACLs enable content-aware routing decisions in the frontend:

```
frontend http_front
    bind *:80
    acl is_api path_beg /api
    acl is_static path_end .css .js .png .jpg
    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend web_servers
```

ACLs can also enforce access control by blocking or allowing traffic based on source IP ranges, request rate, or header values — directly relevant to abuse prevention at the infrastructure layer.

### Health Checks

HAProxy performs proactive health checks to detect unhealthy backend servers before routing traffic to them:

| Check Type | Mechanism |
|-----------|-----------|
| **TCP check** (default) | Attempts TCP connection to the server |
| **HTTP check** | Sends an HTTP request and validates response status code |
| **Agent check** | Queries an external agent on the server that reports health and load |
| **Custom check** | Sends arbitrary data and validates the response |

Failed servers are automatically removed from the rotation and re-added when they recover, enabling seamless failover without manual intervention.

### Session Persistence (Sticky Sessions)

Session persistence ensures that subsequent requests from the same client are routed to the same backend server, which is essential for applications that store session state locally:

| Method | Mechanism | Trade-off |
|--------|-----------|-----------|
| **Cookie insertion** | HAProxy inserts a cookie identifying the backend server; subsequent requests include this cookie | Most reliable; requires HTTP mode |
| **Cookie prefix** | HAProxy prepends server ID to an existing application cookie | Transparent to application |
| **Source IP (stick-table)** | Stores client IP-to-server mapping in a stick table | Works at Layer 4; breaks when clients share IPs (NAT) |
| **URL parameter** | Routes based on a session ID in the URL query string | Useful when cookies are unavailable |

### SSL/TLS Termination

HAProxy can terminate SSL/TLS connections at the proxy layer, decrypting incoming HTTPS traffic and forwarding plain HTTP to backend servers. This offloads CPU-intensive cryptographic operations from application servers and centralizes certificate management. HAProxy also supports SSL passthrough (forwarding encrypted traffic without decryption) and SSL re-encryption (decrypting, inspecting, then re-encrypting to backends).

### HAProxy vs. NGINX

| Dimension | HAProxy | NGINX |
|-----------|---------|-------|
| **Primary design** | Purpose-built load balancer and proxy | Web server with reverse proxy capabilities |
| **Layer 4 support** | Native, first-class TCP proxying | Added later; functional but not primary focus |
| **Load balancing algorithms** | Extensive built-in set (roundrobin, leastconn, source, uri, hdr, first, etc.) | Fewer built-in; advanced algorithms require NGINX Plus (commercial) |
| **Health checks** | Active health checks in open-source version | Active health checks only in NGINX Plus |
| **Connection handling** | Event-driven, single-process, multi-threaded | Event-driven, multi-process (worker processes) |
| **Static content** | Not a web server — cannot serve files directly | Excellent static file serving |
| **Configuration reload** | Hot reload with zero downtime | Graceful reload via signal |
| **Typical deployment** | Dedicated load balancer tier | Combined web server + reverse proxy |

In practice, HAProxy and NGINX are often deployed together: NGINX serves static content and handles application logic, while HAProxy sits in front as the dedicated load balancer managing traffic distribution and high availability.

## Related Terms

- **[Proxy Pattern](term_proxy_pattern.md)**: The structural design pattern underlying HAProxy's architecture — a surrogate that controls access to backend objects/servers
- **[Availability](term_availability.md)**: The system property HAProxy is designed to maximize — ensuring every request receives a response even during server failures
- **[Load Balancing Loss](term_load_balancing_loss.md)**: Load balancing as a concept applied in ML (mixture-of-experts routing); HAProxy applies the same principle at the infrastructure level
- **[Microservices Architecture](term_microservices_architecture.md)**: The distributed architecture style where HAProxy commonly serves as the ingress load balancer or API gateway layer
- **[CAP Theorem](term_cap_theorem.md)**: HAProxy's health checks and failover mechanisms are practical implementations of availability guarantees in the face of partition tolerance
- **[SLA](term_sla.md)**: Service Level Agreements define the uptime and response time targets that HAProxy helps achieve through load balancing and failover
- **[SAR](term_sar.md)**: Scalability, Availability, Reliability — the three operational properties that HAProxy directly supports through horizontal scaling, failover, and health checks
- **[Service-Based Architecture](term_service_based_architecture.md)**: Coarser-grained distributed style where HAProxy routes traffic between domain services
- **[Event-Driven Architecture](term_event_driven_architecture.md)**: Architectural style often combined with load-balanced frontends; HAProxy can proxy event stream connections (WebSocket, SSE)
- **[DevOps](term_devops.md)**: HAProxy configuration, deployment, and monitoring are core DevOps responsibilities in production infrastructure
- **[CI/CD](term_ci_cd.md)**: HAProxy enables zero-downtime deployments through blue-green and canary release strategies with backend weight adjustment
- **[Kafka](term_kafka.md)**: HAProxy can load-balance TCP connections to Kafka brokers; both are infrastructure components in distributed systems
- **[IPs Attack Vectors and Infrastructure](term_ips_attack_vectors_and_infrastructure.md)**: HAProxy's ACL rules and rate limiting serve as a first line of defense against IP-based attack vectors and infrastructure abuse
- **[Session Persistence](term_session_persistence.md)**: HAProxy supports multiple session persistence methods (cookie insertion, source IP stick-tables, URL parameters) to route client requests to the same backend
- **[SSL Termination](term_ssl_termination.md)**: HAProxy terminates SSL/TLS connections at the proxy layer, offloading cryptographic operations and centralizing certificate management
- **[WebSocket](term_websocket.md)**: HAProxy can proxy WebSocket connections using the leastconn algorithm, which is optimal for long-lived persistent connections
- **[Rate Limiting](term_rate_limiting.md)**: HAProxy enforces rate limiting through stick-tables and ACL rules, throttling excessive requests from individual clients or IP addresses at the proxy layer
- **[Reverse Proxy](term_reverse_proxy.md)**: HAProxy is a purpose-built reverse proxy and load balancer that sits between clients and backend servers, forwarding requests and hiding internal topology
- **[Round Robin](term_round_robin.md)**: Round robin (`balance roundrobin`) is HAProxy's default load balancing algorithm, cycling through backend servers sequentially for stateless request distribution
- **[Health Check](term_health_check.md)**: HAProxy performs active TCP, HTTP, and agent-based health checks to detect unhealthy backends and remove them from the rotation before routing traffic
- **[NGINX](term_nginx.md)**: Often deployed alongside HAProxy -- NGINX serving static content and application logic while HAProxy sits in front as the dedicated load balancer managing traffic distribution
- **[Failover](term_failover.md)**: HAProxy implements failover through backup server declarations and health checks -- failed primary servers are removed from rotation and backup servers absorb traffic automatically
- **[gRPC](term_grpc.md)**: HAProxy can proxy gRPC traffic over HTTP/2, load-balancing RPC calls across backend gRPC service instances at Layer 7

## References

### External Sources
- [HAProxy Official Website](https://www.haproxy.org/) — project home with documentation and downloads
- [HAProxy Configuration Manual](https://docs.haproxy.org/3.1/configuration.html) — comprehensive reference for all directives
- [Layer 4 and Layer 7 Proxy Mode — HAProxy Blog](https://www.haproxy.com/blog/layer-4-and-layer-7-proxy-mode) — detailed comparison of L4 vs L7 modes
- [HAProxy — Wikipedia](https://en.wikipedia.org/wiki/HAProxy) — project history and adoption
- [What Is HAProxy — LogicMonitor](https://www.logicmonitor.com/blog/what-is-haproxy-and-what-is-it-used-for) — practical guide with configuration examples
- [Load Balancing, Affinity, Persistence, Sticky Sessions — HAProxy Blog](https://www.haproxy.com/blog/load-balancing-affinity-persistence-sticky-sessions-what-you-need-to-know) — session persistence deep dive
