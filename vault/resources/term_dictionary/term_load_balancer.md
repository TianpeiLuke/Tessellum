---
tags:
  - resource
  - terminology
  - system_design
  - distributed_systems
  - networking
keywords:
  - Load Balancer
  - load balancing
  - traffic distribution
  - Layer 4
  - Layer 7
  - reverse proxy
  - horizontal scaling
  - round robin
  - least connections
  - health check
  - high availability
  - active-passive
  - active-active
  - fault tolerance
topics:
  - System Design
  - Distributed Systems
  - Network Architecture
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# Load Balancer

## Definition

A **load balancer** is a networking component — implemented as dedicated hardware, software, or a cloud-managed service — that distributes incoming client requests across a pool of backend servers to optimize resource utilization, maximize throughput, minimize response latency, and ensure no single server becomes a bottleneck. By acting as a transparent intermediary between clients and servers, the load balancer decouples the client from the specific server handling its request, enabling horizontal scaling (adding more servers) rather than vertical scaling (upgrading a single server). Load balancers operate at different layers of the OSI model: **Layer 4 (L4) load balancers** route at the transport layer based on TCP/UDP connection metadata (source/destination IP and port) without inspecting packet payloads, achieving very high throughput with minimal latency; **Layer 7 (L7) load balancers** operate at the application layer, parsing HTTP headers, URLs, cookies, and request bodies to make content-aware routing decisions such as directing API calls to one server pool and static assets to another.

In the context of the *System Design Deep Dive* (SDDD) podcast series, load balancers are a foundational building block that appears in virtually every large-scale system design — from web application architectures and microservices deployments to database read-replica fan-out and global traffic management. Understanding load balancer placement, algorithm selection, and high-availability configuration is essential for reasoning about system scalability, fault tolerance, and the practical implications of the CAP theorem's availability guarantee. Modern cloud providers offer managed load balancers (AWS ALB/NLB/ELB, GCP Cloud Load Balancing, Azure Load Balancer) that abstract away much of the operational complexity while providing auto-scaling, health checking, and TLS termination out of the box.

## Context

Load balancers sit at critical junctures in system architecture. The most common placement is between clients and web/application servers (the "front door"), but load balancers also appear between application servers and caches, between application servers and databases (especially read replicas), and between internal microservices. In a typical three-tier architecture, at least two load balancer tiers exist: one facing the internet (public) and one or more internal load balancers managing service-to-service traffic. Global Server Load Balancing (GSLB) extends the concept across data centers, using DNS-based routing to direct users to the geographically nearest or healthiest region. In microservices architectures, client-side load balancing (e.g., via service mesh sidecars like Envoy in Istio) complements traditional server-side load balancers by distributing traffic decisions to each service instance.

## Key Characteristics

- **L4 vs L7 distinction**: L4 load balancers are faster and cheaper (no payload inspection) but cannot make content-aware decisions; L7 load balancers can route based on URL path, HTTP headers, cookies, or request body but consume more CPU for parsing and TLS termination
- **Common algorithms**:
  - *Round Robin* — distributes requests sequentially across servers; simple but ignores server load differences
  - *Weighted Round Robin* — assigns weights to servers based on capacity; higher-weight servers receive proportionally more traffic
  - *Least Connections* — routes to the server with the fewest active connections; ideal for long-lived or variable-duration requests
  - *Weighted Least Connections* — combines connection count with server capacity weights
  - *IP Hash / Consistent Hashing* — hashes client IP (or another key) to deterministically route to the same server; provides session affinity without cookies
  - *Least Response Time* — routes to the server with the lowest average response time and fewest active connections
  - *Random / Power of Two Choices (P2C)* — picks two random servers and routes to the one with fewer connections; surprisingly effective at scale
- **Health checks**: Active health checks (load balancer periodically sends synthetic probes — TCP connect, HTTP GET `/health`) detect failures proactively; passive health checks (monitoring real traffic for errors/timeouts) detect degradation under actual load; both are typically combined with configurable thresholds (healthy/unhealthy counts, intervals, timeouts)
- **High availability patterns**:
  - *Active-Passive (failover)* — a standby load balancer monitors the primary via heartbeat and takes over using a floating/virtual IP (VIP) if the primary fails; simpler but wastes standby resources
  - *Active-Active* — multiple load balancers serve traffic simultaneously, sharing the load; provides better utilization and throughput but requires coordination (e.g., via DNS round robin or BGP Anycast)
- **Session persistence (sticky sessions)**: Some applications require that a client's requests consistently reach the same backend (e.g., for in-memory session state); L7 load balancers achieve this via cookies or header injection, while L4 uses source IP affinity — though sticky sessions reduce the effectiveness of load distribution
- **TLS/SSL termination**: L7 load balancers commonly terminate TLS connections, decrypting traffic before forwarding to backends over plain HTTP internally, offloading cryptographic overhead from application servers
- **Software vs hardware**: Hardware load balancers (F5 BIG-IP, Citrix ADC) offer very high throughput via specialized ASICs but are expensive and inflexible; software load balancers (NGINX, HAProxy, Envoy, Traefik) run on commodity hardware and are more adaptable, with modern software solutions handling millions of concurrent connections
- **Connection draining**: When a backend is being removed (for deployment or failure), the load balancer stops sending new connections but allows existing connections to complete gracefully
- **Single point of failure risk**: The load balancer itself can become a single point of failure if not deployed in an HA configuration — this is why production deployments always use redundant load balancers

## Related Terms

- **[CAP Theorem](term_cap_theorem.md)**: Load balancers are a primary mechanism for achieving the "A" (Availability) in CAP — by distributing traffic and rerouting around failures, they keep systems available even when individual nodes fail
- **[Availability](term_availability.md)**: Load balancers directly improve system availability by detecting unhealthy backends via health checks and redistributing traffic to healthy nodes
- **[Consistency](term_consistency.md)**: Sticky sessions and routing algorithms affect consistency guarantees — stateless backends behind a load balancer simplify consistency, while stateful routing introduces session-consistency trade-offs
- **[Partition Tolerance](term_partition_tolerance.md)**: Load balancers help systems tolerate network partitions by routing traffic only to reachable, healthy nodes within a partition
- **[Microservices Architecture](term_microservices_architecture.md)**: Microservices rely heavily on load balancers (both external and internal/service mesh) for inter-service communication, scaling individual services, and fault isolation
- **[Proxy Pattern](term_proxy_pattern.md)**: A load balancer is architecturally a reverse proxy — it implements the proxy pattern by intercepting client requests and forwarding them to backend servers, adding routing and health-check logic
- **[SSL](term_ssl.md)**: L7 load balancers perform SSL/TLS termination, decrypting incoming HTTPS traffic and forwarding plain HTTP to backends, offloading cryptographic processing from application servers
- **[DNS](term_dns.md)**: DNS-based load balancing (GSLB) uses DNS responses to distribute traffic across data centers or regions; DNS round robin is the simplest form of global load balancing
- **[SAR](term_sar.md)**: Scalability, Availability, Reliability — load balancers are a core enabler of all three SAR dimensions, enabling horizontal scalability and improving availability and reliability through redundancy
- **[Space-Based Architecture](term_space_based_architecture.md)**: Uses a messaging grid and processing units that rely on load balancing to distribute work across in-memory data grid nodes
- **[Event-Driven Architecture](term_event_driven_architecture.md)**: Message brokers in event-driven systems perform a form of load balancing by distributing events across consumer groups (e.g., Kafka consumer group rebalancing)
- **[Kafka](term_kafka.md)**: Kafka's consumer group protocol performs partition-level load balancing across consumers — conceptually analogous to a load balancer distributing requests across servers
- **[Architecture Characteristics](term_architecture_characteristics.md)**: Load balancers directly support the scalability, availability, fault tolerance, and performance architecture characteristics
- **[FLP Impossibility](term_flp_impossibility.md)**: Active-active load balancer coordination faces the same consensus limitations described by FLP in asynchronous systems with faults
- **[Scalability](term_scalability.md)**: The load balancer is the infrastructure component that makes horizontal scaling possible by distributing requests across a pool of backend servers
- **[API Gateway](term_api_gateway.md)**: API Gateways incorporate load balancing as one of their core responsibilities, distributing requests across backend microservice instances alongside API-aware features like auth and rate limiting
- **[Database Replication](term_database_replication.md)**: Load balancers distribute read traffic across database read replicas, making read-replica scaling effective by routing queries to healthy replicas
- **[Session Persistence](term_session_persistence.md)**: Sticky sessions ensure client requests consistently reach the same backend server — essential for stateful applications but reduces load distribution effectiveness
- **[SSL Termination](term_ssl_termination.md)**: L7 load balancers commonly terminate TLS connections at the edge, offloading cryptographic operations from backend servers and centralizing certificate management
- **[HAProxy](term_haproxy.md)**: Industry-standard open-source software load balancer operating at Layer 4 and Layer 7, offering extensive load balancing algorithms, active health checks, and session persistence
- **[NGINX](term_nginx.md)**: High-performance web server and reverse proxy commonly deployed as a Layer 7 load balancer with event-driven architecture for high concurrency
- **[Health Check](term_health_check.md)**: Mechanism load balancers use to detect unhealthy backend servers and remove them from the rotation, enabling automated failover
- **[Reverse Proxy](term_reverse_proxy.md)**: A load balancer is architecturally a reverse proxy -- it intercepts client requests and forwards them to backend servers, with load distribution as its primary concern
- **[Round Robin](term_round_robin.md)**: Round robin is the simplest and most widely used load balancing algorithm -- it distributes requests sequentially across servers in a circular rotation, serving as the default in NGINX, HAProxy, and AWS ALB
- **[Failover](term_failover.md)**: Load balancers implement failover by detecting unhealthy backends via health checks and redirecting traffic to healthy nodes -- active-passive and active-active HA patterns for the load balancer itself prevent it from becoming a single point of failure
- **[gRPC](term_grpc.md)**: Load balancers must support HTTP/2 to properly route gRPC traffic; L7 load balancers can perform gRPC-aware routing and health checking for RPC services
- **[Sharding](term_sharding.md)**: In sharded database architectures, load balancers or shard-aware proxies route queries to the correct shard based on the shard key
- **[Redundancy](term_redundancy.md)**: Load balancers distribute traffic across redundant server instances -- without redundant backends, load balancing has no pool to distribute across; the load balancer itself must also be redundant (active-passive or active-active)
- **[Fault Tolerance](term_fault_tolerance.md)**: Load balancers provide fault tolerance via health checks and automatic failover — detecting unhealthy backends and redirecting traffic to healthy nodes ensures continued service despite individual server failures
- **[Latency](term_latency.md)**: Load balancers reduce latency by distributing requests to avoid overloaded servers
- **[Throughput](term_throughput.md)**: Load balancers maximize aggregate throughput by distributing requests across a server pool
- **[TPS](term_tps.md)**: Load balancers distribute TPS across backend instances for even utilization and higher aggregate throughput

## References

- [What is Load Balancing? — AWS](https://aws.amazon.com/what-is/load-balancing/)
- [Load Balancing — Wikipedia](https://en.wikipedia.org/wiki/Load_balancing_(computing))
- [Design a Load Balancer — AlgoMaster](https://algomaster.io/learn/system-design-interviews/design-load-balancer)
- [NGINX Load Balancing Documentation](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [Layer 4 vs Layer 7 Load Balancers — GeeksforGeeks](https://www.geeksforgeeks.org/system-design/layer-4l4-layer-7l7-and-gslb-load-balancers/)
