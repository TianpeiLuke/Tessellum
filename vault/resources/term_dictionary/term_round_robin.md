---
tags:
  - resource
  - terminology
  - system_design
  - load_balancing
  - algorithms
  - distributed_systems
  - networking
keywords:
  - round robin
  - load balancing algorithm
  - weighted round robin
  - smooth weighted round robin
  - DNS round robin
  - traffic distribution
  - NGINX
  - HAProxy
  - server rotation
  - sequential distribution
topics:
  - system design
  - load balancing
  - distributed systems
  - infrastructure
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: Round Robin

## Definition

**Round Robin** is a load distribution algorithm that cycles through available servers sequentially, sending each new request to the next server in a circular list. It is the simplest and most widely used load balancing algorithm. When a request arrives, the load balancer assigns it to the next server in a fixed rotation order. After reaching the last server in the pool, the algorithm wraps around to the first server, forming an endless cycle. Round Robin assumes all servers have equal capacity and all requests impose equal cost -- making it a **static**, **stateless** algorithm that requires no runtime metrics collection.

## Full Name

**Round Robin** = Round-Robin Scheduling / Cyclic Distribution Algorithm

## Key Characteristics

### Basic Round Robin

The simplest form: distribute requests sequentially across N servers in a repeating 1 -> 2 -> 3 -> ... -> N -> 1 cycle. No state is maintained beyond a single counter (the index of the last server used).

```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A   ← wraps around
Request 5 → Server B
Request 6 → Server C
...
```

- **Time complexity**: O(1) per routing decision
- **Space complexity**: O(1) -- only stores the current index
- **Stateless**: No connection tracking, no latency measurement, no server health awareness (beyond health-check-based removal)

### Weighted Round Robin

An extension where each server receives a **weight** proportional to its capacity. A server with weight 3 receives three times as many requests as a server with weight 1. Weights are assigned statically based on known capacity differences (e.g., CPU cores, RAM).

```
Weights: A=5, B=1, C=1
Sequence: A, A, A, A, A, B, C, A, A, A, A, A, B, C, ...
```

- **Use case**: Heterogeneous backends (e.g., a mix of 4-core and 8-core servers)
- **Limitation**: Weights are static and do not adapt to runtime load or degradation

### Smooth Weighted Round Robin (NGINX)

NGINX's improvement on Weighted Round Robin that prevents request bursts to high-weight servers. Instead of sending all weight-5 requests consecutively to Server A, it **interleaves** requests so each server appears at roughly even intervals proportional to its weight.

```
Weights: A=5, B=1, C=1
Naive WRR:  A, A, A, A, A, B, C       ← 5 consecutive to A (burst)
Smooth WRR: A, A, B, A, A, C, A       ← spread evenly (no burst)
```

This is the default algorithm in NGINX's `upstream` directive and is the reason NGINX's round robin feels "smarter" than textbook implementations.

### DNS Round Robin

A variant where the DNS server itself rotates the order of A records returned for a domain name. Each DNS query returns the same set of IP addresses but in a different order, and clients typically connect to the first IP listed.

```
Query 1 → [10.0.0.1, 10.0.0.2, 10.0.0.3]
Query 2 → [10.0.0.2, 10.0.0.3, 10.0.0.1]
Query 3 → [10.0.0.3, 10.0.0.1, 10.0.0.2]
```

- **Advantage**: No dedicated load balancer hardware/software required
- **Limitations**: No health checks (DNS keeps returning IPs of dead servers), DNS TTL caching causes uneven distribution, no awareness of server load or capacity

## Algorithm Comparison

| Algorithm | Tracks State | Adapts to Load | Best For | Weakness |
|-----------|-------------|----------------|----------|----------|
| **Round Robin** | Nothing (single counter) | No | Homogeneous backends, stateless requests | Ignores server capacity and load |
| **Weighted Round Robin** | Server weights (static) | No (static weights) | Heterogeneous backends | Doesn't adapt to runtime conditions |
| **Least Connections** | Active connection count | Yes | Variable-duration requests, WebSocket/SSE | Connection count != actual CPU/memory load |
| **Least Response Time** | Per-server latency | Yes | Performance-sensitive APIs | Requires latency measurement; outlier-sensitive |
| **IP Hash** | Nothing (hash is stateless) | No | Session affinity without cookies | Uneven distribution; reshuffles on topology change |
| **Consistent Hashing** | Hash ring topology | Partially | Distributed caches, stateful services | More complex; requires virtual nodes |

## When to Use Round Robin

**Use Round Robin when:**
- Backends are homogeneous (same hardware, same capacity)
- Requests are roughly uniform in cost (stateless, short-lived)
- Simplicity is prioritized over optimal load distribution
- The system is a stateless service (no session affinity needed)

**Upgrade from Round Robin when:**
- Backends have different capacities -> **Weighted Round Robin**
- Requests have variable duration (long-lived connections) -> **Least Connections**
- Session affinity is needed -> **IP Hash** or **cookie-based stickiness**
- Distributed caching with minimal redistribution -> **Consistent Hashing**
- Latency-sensitive workloads -> **Least Response Time**

## Limitations

1. **Ignores server load**: A server processing a CPU-intensive request gets the next request just the same
2. **Ignores server capacity**: All servers treated equally regardless of hardware differences (unless using weighted variant)
3. **No session affinity**: Consecutive requests from the same client go to different servers (problematic for stateful applications)
4. **Blind to request cost**: A lightweight health-check ping and a heavy database query are treated identically
5. **DNS Round Robin has no health checks**: Dead servers continue receiving traffic until DNS records are manually updated

## Implementations

| Software | Default Algorithm | Round Robin Config |
|----------|------------------|-------------------|
| **NGINX** | Smooth Weighted Round Robin | Default (no directive needed); `upstream backend { server s1; server s2; }` |
| **HAProxy** | Round Robin | `balance roundrobin` in backend config |
| **AWS ELB/ALB** | Round Robin | Default for ALB; configurable |
| **Envoy** | Round Robin | `lb_policy: ROUND_ROBIN` in cluster config |
| **Kubernetes** | Round Robin (via kube-proxy iptables) | Default Service load balancing |

## Related Terms

### Load Balancing Algorithms and Infrastructure
- **[Term: Scheduling Algorithms](term_scheduling_algorithms.md)** -- Round Robin originated as a CPU scheduling algorithm (time-slice rotation); the load balancing variant applies the same cyclic principle to request distribution
- **[Term: SAR (Scalability, Availability, Reliability)](term_sar.md)** -- Load balancing with Round Robin directly improves horizontal scalability (add backends to the pool) and availability (remove failed servers via health checks)
- **[Term: CAP Theorem](term_cap_theorem.md)** -- Distributed systems behind a Round Robin load balancer still face CAP trade-offs; consistent hashing addresses the partition tolerance dimension more gracefully than Round Robin
- **[Term: Availability](term_availability.md)** -- Round Robin improves system availability by distributing load; combined with health checks, failed servers are removed from rotation
- **[Term: Partition Tolerance](term_partition_tolerance.md)** -- Round Robin does not handle network partitions between load balancer and backends; health checks serve as the partition detection mechanism
- **[Term: Proxy Pattern](term_proxy_pattern.md)** -- A load balancer is a reverse proxy; Round Robin is the routing logic within the proxy that determines which backend receives each forwarded request
- **[Term: Microservices Architecture](term_microservices_architecture.md)** -- Round Robin is the default algorithm for distributing requests across instances of a microservice behind a Layer 7 load balancer
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- In event-driven systems, Round Robin distributes events across consumer instances in a competing-consumers pattern (e.g., Kafka consumer group partition assignment)
- **[Term: LRU Cache](term_lru_cache.md)** -- Caching and load balancing are complementary; caching reduces the volume of requests that Round Robin must distribute
- **[Term: SSL](term_ssl.md)** -- SSL/TLS termination at the load balancer offloads encryption before Round Robin distributes plaintext requests to backends
- **[Term: Deep Modules](term_deep_modules.md)** -- A load balancer using Round Robin exemplifies a deep module: simple interface (send request), complex internals (health checks, failover, connection management) hidden behind a narrow API
- **[Session Persistence](term_session_persistence.md)** -- Round Robin does not provide session affinity; applications needing sticky sessions must upgrade to IP Hash or cookie-based persistence

### Infrastructure Implementations
- **[HAProxy](term_haproxy.md)**: HAProxy uses `balance roundrobin` as its default load balancing algorithm, distributing requests sequentially across backend server pools
- **[NGINX](term_nginx.md)**: NGINX implements Smooth Weighted Round Robin as its default algorithm, interleaving requests to prevent burst patterns on high-weight servers

### Source Digest
- **[Digest: Understanding Load Balancing Techniques (SDDD Episode 5)](../digest/digest_sddd_load_balancing_podcast.md)** -- Source digest covering Round Robin and five other load balancing algorithms, Layer 4 vs Layer 7, health checks, and high availability patterns

## References

### External References
- [NGINX Load Balancing Documentation](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/) -- official NGINX load balancing guide; Round Robin is the default algorithm
- [HAProxy Configuration Manual — Balance Algorithms](https://docs.haproxy.org/2.8/configuration.html#4.2-balance) -- HAProxy balance roundrobin configuration
- [GeeksforGeeks — Load Balancing Algorithms](https://www.geeksforgeeks.org/system-design/load-balancing-algorithms/) -- overview of static and dynamic load balancing algorithms
- [AlgoMaster — Load Balancing Algorithms Explained with Code](https://blog.algomaster.io/p/load-balancing-algorithms-explained-with-code) -- code implementations of Round Robin and variants
- [Wikipedia — Round-robin scheduling](https://en.wikipedia.org/wiki/Round-robin_scheduling) -- history and variants of Round Robin from CPU scheduling to load balancing

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Static load balancing algorithm |
| **Mechanism** | Cycle through servers sequentially in circular order |
| **Time complexity** | O(1) per routing decision |
| **State required** | Single counter (current server index) |
| **Variants** | Basic, Weighted, Smooth Weighted (NGINX), DNS Round Robin |
| **Default in** | NGINX, HAProxy, AWS ALB, Envoy, Kubernetes |
| **Best for** | Homogeneous backends, stateless requests, uniform request cost |
| **Limitation** | Ignores server load, capacity, and request cost; no session affinity |
| **Source** | SDDD Podcast Episode 5 — Load Balancing |

**Key Insight**: Round Robin's power lies in its simplicity -- O(1) time, no state, no metrics collection, no adaptive logic. For the common case of stateless services behind identical backends, this simplicity is a feature, not a limitation. The algorithm distributes requests evenly over time by construction, and when combined with health checks (removing failed servers from the pool) and horizontal scaling (adding servers to the pool), it provides a robust baseline that handles most production workloads. The upgrade path is clear: when backends become heterogeneous, switch to Weighted Round Robin; when request durations vary, switch to Least Connections; when session affinity is needed, switch to IP Hash or Consistent Hashing. Round Robin is the "start here" algorithm -- the simplest thing that could possibly work, and often the only thing you need.

---

**Last Updated**: April 19, 2026
**Status**: Active -- system design, load balancing algorithms, SDDD podcast series
