---
tags:
  - resource
  - terminology
  - system_design
  - reliability
  - monitoring
  - distributed_systems
  - infrastructure
keywords:
  - health check
  - health checking
  - liveness probe
  - readiness probe
  - startup probe
  - active health check
  - passive health check
  - deep health check
  - shallow health check
  - load balancer health check
  - service health
topics:
  - System Design
  - Load Balancing
  - Service Reliability
  - Container Orchestration
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# Health Check - Service Health Monitoring

## Definition

A **health check** is a mechanism for monitoring the operational status of services, servers, or infrastructure components. Load balancers use health checks to determine which backend servers can receive traffic — an unhealthy server is removed from the rotation until it recovers. Health checks are the nervous system of high-availability infrastructure, providing the feedback loop that enables automated failover, self-healing, and traffic management. Without health checks, a load balancer would blindly route requests to crashed or overloaded servers, turning a single-node failure into a system-wide outage.

## Context

Health checks are a critical component of load balancing, service mesh infrastructure, container orchestration (Kubernetes liveness/readiness probes), and cloud-native architecture. They appear at every layer of a distributed system: load balancers (ALB, NLB, ELB) check backend targets, Kubernetes checks pod containers, service meshes (Istio, Envoy) check sidecar proxies, and monitoring systems (Prometheus, Datadog) check service endpoints. In the SDDD podcast series (Episode 5 - Load Balancing), health checks are presented as the mechanism that transforms a load balancer from a simple traffic distributor into an intelligent traffic router that can react to real-time server state.

## Key Characteristics

- **Active health checks**: The load balancer or orchestrator proactively sends periodic probe requests (HTTP GET, TCP connect, gRPC) to each backend server and evaluates the response; the checker initiates the check, not the server
- **Passive health checks**: The system monitors real traffic responses (e.g., 5xx error rates, connection failures, timeouts) to infer server health without dedicated probe requests; lower overhead but slower detection
- **TCP health checks**: Verify that a server is accepting TCP connections on a given port — confirms the process is running but not that it can serve requests correctly
- **HTTP health checks**: Send an HTTP request to a specific endpoint (e.g., `/health`, `/ready`) and expect a 200 OK response; can verify application-level functionality, not just network connectivity
- **Custom/gRPC health checks**: Application-specific probes that verify business logic, database connectivity, or downstream dependency availability
- **Health check intervals and thresholds**: Defined by `interval` (how often to check, e.g., 10s), `timeout` (max wait for response, e.g., 5s), `healthy threshold` (consecutive successes to mark healthy, e.g., 2), and `unhealthy threshold` (consecutive failures to mark unhealthy, e.g., 3)
- **Kubernetes liveness probe**: Determines if a container is running; failure triggers a container restart — answers "is the process alive?"
- **Kubernetes readiness probe**: Determines if a container can accept traffic; failure removes the pod from Service endpoints without restarting — answers "is the process ready for requests?"
- **Kubernetes startup probe**: Runs only during container startup, disabling liveness and readiness probes until it succeeds — prevents slow-starting containers from being killed prematurely
- **Deep health checks**: Verify not just the service itself but also its critical dependencies (database connections, downstream services, cache availability); more accurate but risk cascading failures if a shared dependency is down
- **Shallow health checks**: Return healthy if the service process is running and can respond, regardless of dependency status; faster and simpler but may route traffic to a server that will fail on actual requests
- **Load balancer health checks (ELB/ALB/NLB)**: AWS ELB performs active health checks on registered targets; ALB supports HTTP/HTTPS checks with path-based routing, NLB supports TCP/HTTP/HTTPS checks; unhealthy targets are deregistered from the target group
- **Cascading health checks**: A service reports itself unhealthy because its downstream dependency is unhealthy, potentially causing an entire chain of services to mark themselves down — must be carefully designed to avoid amplifying partial failures
- **Health check endpoint design patterns**: `/health` (overall service health), `/ready` (readiness for traffic), `/live` (liveness/process alive), `/startup` (initialization complete); best practice is to separate these concerns into distinct endpoints

## Health Check Decision Matrix

| Check Type | What It Validates | When to Use | Risk |
|------------|-------------------|-------------|------|
| **TCP** | Port is open | Basic connectivity | False positive — process may be deadlocked |
| **HTTP shallow** | Service responds 200 | General availability | May miss dependency failures |
| **HTTP deep** | Service + dependencies OK | Critical path services | Cascading failures if dependency down |
| **Liveness** | Process is alive | Container restart decision | Too aggressive = restart loops |
| **Readiness** | Can serve traffic | Load balancer routing | Too strict = no healthy targets |
| **Startup** | Initialization complete | Slow-starting apps | Too short = premature kills |

## Best Practices

- **Separate liveness from readiness**: A service can be alive (liveness = OK) but not ready (readiness = FAIL) — e.g., warming caches or loading models; conflating them causes unnecessary restarts
- **Avoid deep checks in liveness probes**: A database outage should not restart your application container; use deep checks only in readiness probes
- **Set conservative thresholds**: Require 3+ consecutive failures before marking unhealthy to avoid flapping caused by transient network issues
- **Health check interval tuning**: 10-30 seconds is typical; too frequent (1s) adds load, too infrequent (60s) delays failure detection; target a 30-60 second detection window
- **Dedicated health endpoints**: Use `/health`, `/ready`, `/live` rather than production API routes to prevent false positives from normal load variations
- **Include version/metadata**: Health endpoints can return build version, uptime, and dependency status in the response body for debugging

## Related Terms

- **[SAR](term_sar.md)** - Scalability, Availability, Reliability framework; health checks are the operational mechanism for achieving the availability component of SAR
- **[Availability](term_availability.md)** - Health checks are the primary mechanism for maintaining high availability by detecting and routing around failures
- **[SLA](term_sla.md)** - Service Level Agreements define uptime targets that health checks help enforce through automated failover
- **[Microservices Architecture](term_microservices_architecture.md)** - Health checks are essential in microservices where each service must independently report its status to the service mesh and load balancer
- **[CAP Theorem](term_cap_theorem.md)** - Health checks interact with CAP trade-offs: during a partition, a health check timeout may incorrectly mark a consistent (CP) node as unhealthy
- **[Proxy Pattern](term_proxy_pattern.md)** - Load balancers and reverse proxies use health checks to decide which backend to forward requests to
- **[Event-Driven Architecture](term_event_driven_architecture.md)** - Health check failures often trigger events (alerts, auto-scaling, failover) in event-driven infrastructure
- **[Space-Based Architecture](term_space_based_architecture.md)** - Processing units in space-based architecture use health checks for in-memory data grid replication and failover
- **[Observability (Agent Systems)](term_observability_agent_systems.md)** - Health checks are one pillar of observability alongside metrics, logs, and traces
- **[Data Observability](term_data_observability.md)** - Data pipeline health checks monitor freshness, volume, and schema consistency of data flows
- **[Partition Tolerance](term_partition_tolerance.md)** - Network partitions can cause health check probes to timeout, creating false-negative health assessments
- **[MTBF](term_mtbf.md)**: Mean Time Between Failures -- health checks detect failures that start the MTTR clock; faster detection directly improves the MTTR component of the availability formula `A = MTBF / (MTBF + MTTR)`
- **[SLI](term_sli.md)**: Service Level Indicator -- health checks are a simple availability SLI implementation; periodic health-check signals feed into availability SLO calculations
- **[SLO](term_slo.md)**: Service Level Objective -- health check failures trigger SLO-based alerting by signaling availability degradation that consumes error budget
- **[Chaos Engineering](term_chaos_engineering.md)**: Chaos engineering tests health check infrastructure by injecting failures and verifying that health checks correctly detect degraded services and trigger automated responses
- **[Failover](term_failover.md)**: Health checks are the detection mechanism that triggers failover -- heartbeat signals and external probes identify when the primary has failed, initiating the switch to standby
- **[gRPC](term_grpc.md)**: gRPC defines a standard health checking protocol (grpc.health.v1) that load balancers and orchestrators use for active health probing of gRPC services

## References

- [Health Check API Pattern — Microservices.io](https://microservices.io/patterns/observability/health-check-api.html)
- [Configure Liveness, Readiness and Startup Probes — Kubernetes Documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Liveness, Readiness, and Startup Probes — Kubernetes Concepts](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [Health Check Concepts — Google Cloud Load Balancing](https://docs.cloud.google.com/load-balancing/docs/health-check-concepts)
- [Configure Probes and Load Balancer Health Checks — AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/ha-resiliency-amazon-eks-apps/probes-checks.html)
- [Load Balancing Monitor Groups — Cloudflare Blog](https://blog.cloudflare.com/load-balancing-monitor-groups-multi-service-health-checks-for-resilient/)
- [The Instance Is Up. Or Is It? — Health Checking in Client-Side vs Server-Side Load Balancing](https://singh-sanjay.com/2026/01/12/health-checks-client-vs-server-side-lb.html)

---

**Last Updated**: April 19, 2026
**Status**: Active
**Source**: SDDD Podcast Series - Episode 5 (Load Balancing)
**Related Terms**: [SAR](term_sar.md), [Availability](term_availability.md), [Microservices Architecture](term_microservices_architecture.md), [CAP Theorem](term_cap_theorem.md)
