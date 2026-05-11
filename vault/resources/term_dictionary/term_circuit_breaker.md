---
tags:
  - resource
  - terminology
  - system_design
  - resilience
  - design_patterns
keywords:
  - Circuit Breaker
  - fault tolerance
  - cascading failure
  - resilience pattern
  - Hystrix
  - state machine
  - closed-open-half-open
topics:
  - System Design
  - Resilience Patterns
  - Distributed Systems
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Circuit Breaker

## Definition

The **Circuit Breaker** is a stability pattern in distributed systems that prevents an application from repeatedly invoking a remote service or resource that is likely to fail. Named by analogy with electrical circuit breakers -- which interrupt current flow when a fault is detected to prevent damage to the wider circuit -- the software circuit breaker wraps a potentially failing call in a proxy object that monitors failures and, once a threshold is exceeded, short-circuits subsequent calls by failing them immediately without contacting the remote service. This prevents cascading failures, conserves system resources (threads, connections, memory), and gives the failing dependency time to recover.

The pattern was popularized by Michael Nygard in *Release It!* (2007) and became widely adopted through Netflix's **Hystrix** library (2012), which implemented circuit breakers as a core resilience primitive in Netflix's microservices architecture. The Circuit Breaker pattern is now a standard component of resilience engineering in distributed systems, implemented across all major platforms and languages.

## Context

The Circuit Breaker pattern addresses a fundamental problem in distributed architectures: when a downstream service becomes slow or unresponsive, the calling service can exhaust its own resources (thread pools, connection pools, memory) waiting for responses that will never arrive. Without protection, this resource exhaustion propagates upstream through the call chain, producing a **cascading failure** that can bring down an entire system from a single point of degradation. The circuit breaker acts as a fail-fast mechanism that isolates the failure, returns control to the caller immediately, and enables graceful degradation rather than total system collapse.

In modern cloud-native and microservices environments, circuit breakers are essential because: (1) services depend on many remote calls, any of which can fail independently; (2) network partitions, latency spikes, and capacity exhaustion are normal operating conditions, not exceptions; and (3) the blast radius of a single failing dependency must be contained to preserve overall system availability. Circuit breakers are often combined with other resilience patterns -- retries (with backoff), bulkheads, timeouts, and fallbacks -- to form a layered defense against distributed system failures.

## Key Characteristics

### Three-State Model

The circuit breaker operates as a finite state machine with three states:

```
                    failure threshold
                       exceeded
    ┌─────────┐    ─────────────────►    ┌─────────┐
    │  CLOSED  │                         │  OPEN    │
    │ (normal) │    ◄────────────────    │ (trips)  │
    └─────────┘     half-open fails      └─────────┘
         ▲                                    │
         │          timeout expires           │
         │                                    ▼
         │                              ┌──────────┐
         └──────── success threshold ───│HALF-OPEN │
                      reached           │ (probes) │
                                        └──────────┘
```

- **Closed** (normal operation): Requests pass through to the downstream service. The circuit breaker maintains a failure counter. If a call succeeds, the counter resets (or decrements). If a call fails, the counter increments. When the failure count (or failure rate) exceeds a configured threshold within a rolling time window, the circuit breaker transitions to the **Open** state
- **Open** (circuit tripped): All requests fail immediately with a predefined error or fallback response -- no call is made to the downstream service. This prevents resource exhaustion and gives the failing service time to recover. The circuit breaker starts a timeout timer. When the timer expires, the circuit breaker transitions to the **Half-Open** state
- **Half-Open** (probing recovery): A limited number of trial requests are allowed through to the downstream service. If these succeed (reaching a configurable success threshold), the circuit breaker transitions back to **Closed**, resuming normal operation. If any trial request fails, the circuit breaker returns to **Open** and the timeout timer restarts. The Half-Open state prevents a recovering service from being flooded with full traffic before it is ready

### Configuration Parameters

| Parameter | Description | Typical Default |
|-----------|-------------|-----------------|
| **Failure threshold** | Number of failures (or failure rate %) that trips the breaker | 5 failures or 50% failure rate |
| **Rolling window** | Time window over which failures are counted | 10 seconds |
| **Timeout duration** | How long the breaker stays Open before transitioning to Half-Open | 30-60 seconds |
| **Success threshold** | Number of consecutive successes in Half-Open to transition to Closed | 3-5 successes |
| **Trial request count** | Number of requests allowed through in Half-Open state | 1-10 requests |
| **Monitored exceptions** | Which failure types count toward the threshold (vs. ignored) | Configurable per implementation |
| **Slow call threshold** | Response time above which a call is counted as slow/failed | Implementation-dependent |

### Fallback Mechanisms

When the circuit is open, the system must handle requests that cannot reach the downstream service. Common fallback strategies include:

- **Cached responses**: Return the most recently cached successful response
- **Default values**: Return a sensible default (e.g., empty list, default configuration)
- **Degraded functionality**: Disable the feature that depends on the failing service while keeping the rest of the application operational
- **Alternative service**: Route to a secondary or backup service
- **Queue for later**: Buffer the request for asynchronous processing when the service recovers
- **Error with context**: Return a meaningful error that informs the caller of the degradation without exposing internal details

### Relationship to Other Resilience Patterns

The Circuit Breaker is one component in a broader resilience toolkit. These patterns complement each other and are often composed together:

- **Retry with backoff**: Retries handle transient failures (single-request glitches); the circuit breaker handles sustained failures. Retries should be wrapped inside a circuit breaker so that retries stop when the breaker opens. Without this coordination, retries amplify load on an already failing service
- **Bulkhead**: Isolates resources (thread pools, connection pools) per dependency, so that one slow dependency cannot exhaust resources shared by others. While the circuit breaker stops calls to a failing service, the bulkhead prevents a slow service from consuming all available threads. Together, they provide both temporal isolation (circuit breaker) and resource isolation (bulkhead)
- **Timeout**: Sets a maximum duration for a remote call. Timeouts ensure that a single slow call does not block a thread indefinitely. The circuit breaker uses timeout failures as one of its failure signals
- **Rate limiting / throttling**: Controls the rate of outbound requests. Complementary to circuit breakers -- rate limiting prevents overloading a healthy service; circuit breakers stop calling a failing one
- **Fallback**: Provides alternative behavior when the primary path fails. Fallback is not a separate pattern but an integral part of the circuit breaker's open-state behavior
- **Health check endpoint**: The circuit breaker can use a dedicated health endpoint to probe service recovery in the Half-Open state, rather than sending real user requests as probes

### Major Implementations

| Library / Framework | Language / Platform | Notes |
|---|---|---|
| **Netflix Hystrix** | Java | Pioneered the pattern at scale (2012); now in maintenance mode |
| **Resilience4j** | Java | Lightweight, modern successor to Hystrix; functional API, supports reactive streams |
| **Polly** | .NET (C#) | Comprehensive resilience library with circuit breaker, retry, bulkhead, timeout policies |
| **gobreaker** | Go | Sony's circuit breaker implementation for Go services |
| **pybreaker** | Python | Circuit breaker for Python applications |
| **Istio / Envoy** | Service mesh (any language) | Infrastructure-level circuit breaking via sidecar proxy; no application code changes |
| **AWS App Mesh** | AWS service mesh | Managed circuit breaking for AWS workloads |
| **Spring Cloud Circuit Breaker** | Java / Spring | Abstraction layer supporting Resilience4j as the default backend |

### Anti-Patterns and Pitfalls

- **Threshold too sensitive**: Setting failure thresholds too low causes the breaker to trip on normal transient errors, creating unnecessary outages
- **Threshold too lenient**: Setting thresholds too high allows cascading failures to propagate before the breaker trips
- **Timeout too short**: Reopening the circuit before the downstream service has recovered causes repeated trip-reset cycling (flapping)
- **Timeout too long**: Keeping the circuit open long after recovery means extended periods of unnecessary degradation
- **No fallback strategy**: Tripping the breaker without a fallback simply converts a slow failure into a fast failure -- the user still gets an error
- **Ignoring partial failures**: Using a single circuit breaker for a service with multiple independent endpoints or partitions can cause healthy endpoints to be blocked when only one is failing
- **No observability**: Circuit breaker state transitions are critical operational signals. Without monitoring and alerting on breaker state changes, operators cannot distinguish between a failing dependency and a tripped breaker

## Related Terms

- **[MTTR](term_mttr.md)**: Circuit breakers reduce effective MTTR by failing fast and enabling automatic recovery probing via the Half-Open state
- **[Rate Limiting](term_rate_limiting.md)**: Rate limiting prevents overloading a healthy service while circuit breakers stop calling a failing one — complementary resilience patterns
- **[Microservices Architecture](term_microservices_architecture.md)**: The architectural style where circuit breakers are most critical -- each service-to-service call is a potential failure point that benefits from circuit breaker protection
- **[Availability](term_availability.md)**: Circuit breakers preserve overall system availability by isolating failing dependencies and enabling graceful degradation rather than total outage
- **[Event-Driven Architecture](term_event_driven_architecture.md)**: Asynchronous, event-driven communication reduces the need for circuit breakers (since producers do not wait for consumer responses), but circuit breakers remain relevant for any synchronous call within an EDA system
- **[CAP Theorem](term_cap_theorem.md)**: Circuit breakers implement an availability-favoring strategy during partition-like conditions -- when a dependency is unreachable, the breaker chooses availability (via fallback) over consistency (waiting for the real response)
- **[Proxy Pattern](term_proxy_pattern.md)**: The circuit breaker is structurally a proxy that intercepts calls to the downstream service and decides whether to forward or short-circuit them
- **[State Pattern](term_state_pattern.md)**: The circuit breaker's three-state model (Closed, Open, Half-Open) is a direct application of the GoF State pattern, where behavior changes based on the current state object
- **[Strategy Pattern](term_strategy_pattern.md)**: Fallback mechanisms in circuit breakers can be modeled as interchangeable strategies, selected based on the failure context
- **[Observer Pattern](term_observer_pattern.md)**: Circuit breaker state transitions (Closed to Open, Open to Half-Open, etc.) are typically broadcast as events for monitoring and alerting, following the Observer pattern
- **[Decorator Pattern](term_decorator_pattern.md)**: Circuit breakers are often implemented as decorators that wrap existing service clients, adding resilience behavior without modifying the original client code
- **[Hexagonal Architecture](term_hexagonal_architecture.md)**: Circuit breakers are naturally placed in the adapter layer of a hexagonal architecture, wrapping driven adapters that communicate with external services
- **[Facade Pattern](term_facade_pattern.md)**: An API gateway or service facade may embed circuit breakers to protect downstream services from cascading call failures
- **[Adapter Pattern](term_adapter_pattern.md)**: Circuit breakers wrap service adapters, adding failure management to the translation layer between the application core and external dependencies
- **[SAR](term_sar.md)**: Scalability, Availability, Reliability -- circuit breakers directly support the Availability and Reliability dimensions of SAR by containing failure blast radius
- **[API Gateway](term_api_gateway.md)**: API Gateways embed circuit breaking as a core responsibility, detecting failing backend services and short-circuiting requests to prevent cascade failures across the microservices ecosystem
- **[MTBF](term_mtbf.md)**: Mean Time Between Failures -- circuit breakers reduce effective MTTR by failing fast, which improves availability in the `A = MTBF / (MTBF + MTTR)` formula
- **[SLI](term_sli.md)**: Service Level Indicator -- circuit breaker state transitions are observable SLI signals; breaker trips indicate availability degradation measurable through error rate SLIs
- **[SLO](term_slo.md)**: Service Level Objective -- circuit breakers protect SLO compliance by failing fast when a downstream dependency degrades, preventing cascading failures from consuming error budget
- **[Rate Limiting](term_rate_limiting.md)**: Complementary resilience pattern -- rate limiting prevents overloading a healthy service by capping inbound request volume, while circuit breakers stop calling a failing service entirely
- **[Chaos Engineering](term_chaos_engineering.md)**: Chaos engineering validates circuit breaker behavior by injecting failures and verifying that breakers trip correctly, fallbacks activate, and the system degrades gracefully
- **[Graceful Degradation](term_graceful_degradation.md)**: Circuit breakers enable graceful degradation by defining fallback behavior when the circuit is open -- the system continues at reduced functionality rather than failing completely
- **[Error Budget](term_error_budget.md)**: Circuit breakers protect error budget by failing fast and preventing cascading failures that would consume budget through prolonged outages
- **[Health Check](term_health_check.md)**: Circuit breakers can use dedicated health check endpoints to probe service recovery in the Half-Open state rather than sending real user requests as probes
- **[Failover](term_failover.md)**: Circuit breakers complement failover by providing application-level failure isolation while failover switches to a standby at the infrastructure level
- **[Fault Tolerance](term_fault_tolerance.md)**: The circuit breaker is a core fault tolerance pattern — it enables systems to continue operating in a degraded mode when downstream dependencies fail, rather than allowing cascading failures
- **[Latency](term_latency.md)**: Circuit breakers protect latency by failing fast when a downstream service is degraded, avoiding cascading timeouts

## References

### Vault References
- [Fundamentals of Software Architecture](../digest/digest_fundamentals_software_architecture_richards.md) -- Richards and Ford cover resilience patterns including circuit breakers in the context of distributed architecture trade-offs
- [Design Patterns (GoF)](../digest/digest_design_patterns_gamma.md) -- The State, Proxy, and Decorator patterns that structurally underpin the circuit breaker implementation
- [Clean Architecture](../digest/digest_clean_architecture_martin.md) -- Circuit breakers reside at the outermost ring (Frameworks & Drivers) as infrastructure-level resilience wrappers around external service calls

### External References
- [Nygard, M. (2007/2018). *Release It! Design and Deploy Production-Ready Software.* Pragmatic Bookshelf](https://pragprog.com/titles/mnee2/release-it-second-edition/) -- The definitive treatment of stability patterns including Circuit Breaker, Bulkhead, and Timeout; the book that named and popularized the pattern for software systems
- [Microsoft Azure Architecture Center. "Circuit Breaker pattern."](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) -- Comprehensive reference with state diagrams, configuration considerations, and Azure-specific implementation guidance
- [Microservices.io. "Pattern: Circuit Breaker."](https://microservices.io/patterns/reliability/circuit-breaker.html) -- Pattern catalog entry with problem-solution format and relationship to other microservices patterns
- [Fowler, M. (2014). "CircuitBreaker." martinfowler.com](https://martinfowler.com/bliki/CircuitBreaker.html) -- Martin Fowler's concise explanation with code examples illustrating the state machine implementation
- [Wikipedia. "Circuit breaker design pattern."](https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern) -- Encyclopedic overview with history and cross-language implementation references
- [Resilience4j Documentation](https://resilience4j.readme.io/docs/circuitbreaker) -- Modern Java circuit breaker library documentation with configuration reference and usage patterns
- [Netflix Hystrix (archived)](https://github.com/Netflix/Hystrix) -- The original Netflix library that brought circuit breakers to mainstream microservices practice; now in maintenance mode, succeeded by Resilience4j

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Stability / resilience pattern for distributed systems |
| **Core mechanism** | Three-state proxy (Closed, Open, Half-Open) that monitors failures and short-circuits calls to failing services |
| **Named after** | Electrical circuit breakers that interrupt current to prevent damage |
| **Problem solved** | Cascading failures caused by repeated calls to unresponsive or failing downstream services |
| **Key benefit** | Fail-fast behavior, resource conservation, graceful degradation, failure isolation |
| **Key trade-off** | During open state, callers receive fallback responses instead of real data -- availability over consistency |
| **Key configurations** | Failure threshold, rolling window, timeout duration, success threshold, fallback strategy |
| **Key implementations** | Resilience4j (Java), Polly (.NET), gobreaker (Go), Istio/Envoy (service mesh) |
| **Complementary patterns** | Retry with backoff, Bulkhead, Timeout, Rate Limiting, Health Check |
| **Popularized by** | Michael Nygard (*Release It!*, 2007), Netflix Hystrix (2012) |

**Key Insight**: The Circuit Breaker pattern embodies a counterintuitive principle: *failing fast is better than failing slow*. When a downstream dependency degrades, the worst outcome is not an immediate error but a slow, resource-draining timeout that propagates up the call chain. The circuit breaker converts slow failures into fast failures, returning control to the caller immediately so it can execute a fallback strategy. This is why the pattern is named after its electrical counterpart -- just as an electrical breaker sacrifices power to one circuit to protect the rest of the system, a software circuit breaker sacrifices one dependency's functionality to preserve overall system health. The critical design challenge is calibrating thresholds and timeouts: too aggressive and the breaker trips on normal variance, causing unnecessary degradation; too lenient and cascading failures propagate before the breaker activates. Modern adaptive approaches use machine learning to dynamically adjust these thresholds based on real-time traffic patterns and historical failure rates.

---

**Last Updated**: April 19, 2026
**Status**: Active - foundational resilience pattern in distributed systems and microservices architecture
