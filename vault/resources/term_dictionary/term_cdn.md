---
tags:
  - resource
  - terminology
  - system_design
  - networking
  - caching
keywords:
  - CDN
  - Content Delivery Network
  - edge caching
  - PoP
  - origin server
  - edge server
  - CloudFront
  - Akamai
topics:
  - System Design
  - Network Architecture
  - Web Performance
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
---

# Term: CDN (Content Delivery Network)

## Definition

A **Content Delivery Network (CDN)** is a geographically distributed network of proxy servers and data centers designed to deliver web content and services to users with high availability and high performance by serving content from locations physically closer to the requesting user. CDNs cache static assets (images, CSS, JavaScript, video, HTML pages) at **edge servers** deployed across dozens to hundreds of **Points of Presence (PoPs)** worldwide. When a user requests content, DNS resolution directs the request to the nearest edge server rather than the distant **origin server**, reducing round-trip latency, offloading origin bandwidth, and improving fault tolerance. Modern CDNs extend beyond static caching to include dynamic content acceleration, DDoS mitigation, Web Application Firewall (WAF) capabilities, edge compute (e.g., Cloudflare Workers, Lambda@Edge), TLS termination, and real-time video streaming.

## Context

CDNs emerged in the late 1990s to address the fundamental performance limitation of centralized hosting: the speed of light imposes a physical lower bound on network latency, and every additional network hop introduces delay and potential packet loss. Akamai Technologies, founded in 1998 by MIT researchers, pioneered the commercial CDN model by distributing content across a global network of edge servers. Today, CDNs serve the majority of global internet traffic, with providers such as **Amazon CloudFront**, **Cloudflare**, **Akamai**, **Fastly**, **Google Cloud CDN**, and **Azure CDN** operating thousands of PoPs across every continent. In a system design context, the CDN is a critical component of any internet-facing architecture that must serve users across multiple geographic regions with low latency and high reliability.

## Key Characteristics

### How a CDN Works

```
User Request Flow:

1. User requests https://example.com/image.png
2. DNS resolves to the CDN's nearest PoP (via Anycast or GeoDNS)
3. Edge server at the PoP checks its local cache
   ├── Cache HIT  → Return cached content immediately (low latency)
   └── Cache MISS → Fetch from origin server, cache it, then return to user

┌──────────┐       ┌─────────────────────┐       ┌──────────────┐
│  Client   │──────►│  CDN Edge Server     │──────►│ Origin Server │
│ (Browser) │◄──────│  (Nearest PoP)       │◄──────│ (Your Server) │
└──────────┘       └─────────────────────┘       └──────────────┘
   Low latency         Cached content              Source of truth
```

### Points of Presence (PoPs)

A **Point of Presence (PoP)** is a physical data center location where CDN edge servers are deployed. Each PoP contains one or more caching servers that store and serve content to users in the surrounding geographic region. CDNs strategically place PoPs at internet exchange points (IXPs) and major metropolitan areas to minimize the number of network hops between users and content. Some CDN providers implement a **multi-tier PoP hierarchy**:

- **Tier 1 (Edge PoPs)**: Small, numerous, close to end users -- serve cached content directly
- **Tier 2 (Regional PoPs / Mid-tier caches)**: Larger, fewer, aggregate cache misses from multiple edge PoPs before reaching origin -- reduces origin load
- **Origin Shield**: A single designated PoP that sits in front of the origin server, consolidating all cache misses to minimize origin requests

### Edge Servers vs. Origin Server

| Component | Role | Location | Content |
|-----------|------|----------|---------|
| **Origin server** | Source of truth; hosts the canonical version of all content | Centralized (one or few regions) | Complete, authoritative content |
| **Edge server** | Cached proxy; serves content on behalf of origin | Distributed across PoPs worldwide | Cached subset, governed by TTL |
| **Mid-tier cache** | Intermediate cache between edge and origin | Regional hubs | Aggregated cache for multiple edge PoPs |

### Origin Pull vs. Origin Push

CDNs use two fundamental models for populating content at edge servers:

**Pull CDN (Origin Pull)**:
- The edge server fetches content from the origin **on demand** -- only when a user requests it and the cache does not have it (cache miss)
- After fetching, the content is cached at the edge server with a configurable TTL (Time-To-Live)
- Subsequent requests for the same content are served from cache until the TTL expires
- **Advantages**: Simple configuration; no need to proactively manage what is cached; storage-efficient because only requested content is cached
- **Disadvantages**: First request to each PoP experiences full origin latency (cold start / cache miss penalty); unpredictable origin load during traffic spikes on uncached content
- **Best for**: Dynamic websites, frequently updated content, long-tail content where not every asset is accessed at every PoP

**Push CDN**:
- The content owner proactively uploads (pushes) content to CDN edge servers **before** any user requests it
- Content is pre-positioned at all or selected PoPs, eliminating the cold-start cache miss
- Requires the content owner to manage uploads, often via API or automated CI/CD pipelines (e.g., cron jobs, deploy hooks)
- **Advantages**: Zero cache-miss latency for users; predictable origin load; full control over which content is distributed where
- **Disadvantages**: Higher storage costs (content replicated everywhere regardless of demand); operational overhead of managing push workflows; not suitable for frequently changing content
- **Best for**: Large static assets (video, software binaries, firmware updates), content that must be available immediately with zero cold-start, media distribution platforms

**Hybrid Approach**: Most production CDN configurations use a hybrid model -- push for critical static assets (hero images, JS bundles, video segments) and pull for long-tail or infrequently accessed content.

### Cache Invalidation at the CDN Layer

Cache invalidation is the process of removing or updating stale content from CDN edge caches so users receive the most current version. This is one of the most operationally challenging aspects of CDN management, since content is replicated across many edge servers worldwide.

**Invalidation Strategies**:

| Strategy | Mechanism | Trade-off |
|----------|-----------|-----------|
| **TTL expiration** | Content expires after a configured Time-To-Live (e.g., `Cache-Control: max-age=86400`). After expiry, edge re-fetches from origin | Simple but coarse -- cannot force immediate updates; must wait for TTL |
| **Purge / Invalidation API** | Explicitly request removal of specific URLs or path patterns via CDN provider API (e.g., CloudFront `CreateInvalidation`, Fastly `Purge`) | Immediate but costly at scale; some providers charge per invalidation request |
| **Cache tags / Surrogate keys** | Tag cached objects with metadata keys (e.g., `product-123`, `category-shoes`); purge all objects matching a tag | Precise, surgical invalidation; avoids over-purging; supported by Fastly, Cloudflare, Google Cloud CDN |
| **Versioned URLs / Fingerprinting** | Embed a content hash or version in the filename (e.g., `app.9a7f3e.js`, `style.v2.css`). New version = new URL = new cache key | Zero invalidation overhead; old cached versions are simply never requested again; best practice for static assets |
| **Stale-while-revalidate** | Serve stale content immediately while asynchronously fetching a fresh copy from origin (`Cache-Control: stale-while-revalidate=60`) | Users get fast responses; content freshness is eventual; good for non-critical content |

**Best Practice**: Use **versioned URLs / fingerprinting** for static assets (CSS, JS, images) to eliminate the need for invalidation entirely. Use **cache tags** for dynamic content that must be surgically invalidated. Reserve **purge APIs** for emergency invalidation of incorrect or sensitive content.

### CDN Performance Optimizations

Beyond simple caching, modern CDNs provide several performance optimizations:

- **Connection reuse and keep-alive**: CDN maintains persistent connections to both clients and origin, reducing TCP/TLS handshake overhead
- **HTTP/2 and HTTP/3 (QUIC)**: CDN edge servers support modern protocols for multiplexed, low-latency delivery
- **TLS termination at the edge**: SSL/TLS handshake happens at the nearby edge server rather than the distant origin, reducing connection setup latency
- **Image optimization**: On-the-fly image compression, format conversion (WebP, AVIF), and responsive resizing at the edge
- **Compression**: Gzip/Brotli compression applied at the edge for text-based assets
- **Edge compute**: Run application logic at the edge (Cloudflare Workers, Lambda@Edge, Fastly Compute@Edge) for personalization, A/B testing, authentication, and request routing without round-tripping to origin
- **Prefetching and predictive loading**: CDN can preemptively fetch and cache content that is likely to be requested next

### CDN Providers

| Provider | Key Differentiator | Edge Compute | PoPs (approx.) |
|----------|-------------------|--------------|----------------|
| **Amazon CloudFront** | Deep AWS integration, Lambda@Edge, Origin Shield | Lambda@Edge, CloudFront Functions | 600+ |
| **Cloudflare** | Largest network, Workers edge compute, integrated security (WAF, DDoS) | Cloudflare Workers | 310+ |
| **Akamai** | Oldest CDN, largest enterprise customer base, Intelligent Edge Platform | EdgeWorkers | 4,100+ |
| **Fastly** | Real-time purging (<150ms global), Compute@Edge (Wasm), VCL configuration | Compute@Edge | 90+ |
| **Google Cloud CDN** | Integrated with GCP, global load balancing, Media CDN for streaming | Cloud Run integration | 180+ |
| **Azure CDN** | Multi-CDN (Akamai, Verizon profiles), Azure Front Door integration | Azure Functions integration | 180+ |

## Related Terms

### Caching and Data
- **[Term: LRU Cache](term_lru_cache.md)** -- Least Recently Used eviction policy; CDN edge caches typically use LRU or LRU-variant algorithms to manage limited local storage when cache capacity is exceeded
- **[Term: KV Cache](term_kv_cache.md)** -- Key-value caching pattern; CDN edge caches are conceptually key-value stores mapping URL (key) to content (value)
- **[Term: Consistency](term_consistency.md)** -- CDN caching introduces eventual consistency between origin and edge; cache invalidation strategies manage this trade-off
- **[Cache Invalidation](term_cache_invalidation.md)**: CDN cache invalidation is one of the most operationally challenging aspects of CDN management, using strategies like TTL expiration, purge APIs, cache tags, versioned URLs, and stale-while-revalidate
- **[Cache Stampede](term_cache_stampede.md)**: CDNs experience cache stampede at edge PoPs when popular content TTLs expire simultaneously across edge nodes, flooding the origin with concurrent requests
- **[Eviction Policy](term_eviction_policy.md)**: CDN edge caches use eviction policies (typically LRU variants) to manage finite edge storage across millions of cached content objects

### Security and Networking
- **[Term: SSL](term_ssl.md)** -- CDN edge servers terminate SSL/TLS connections, offloading cryptographic overhead from the origin and reducing handshake latency for end users
- **[Term: CAP Theorem](term_cap_theorem.md)** -- CDNs prioritize Availability and Partition Tolerance over strong Consistency; cached content may be stale during the TTL window

### Architecture Patterns
- **[Term: Event-Driven Architecture](term_event_driven_architecture.md)** -- CDN cache invalidation can be triggered by events (e.g., content update event triggers purge); event-driven patterns complement CDN-based architectures
- **[Term: Microservices Architecture](term_microservices_architecture.md)** -- CDNs sit in front of microservices-based backends, caching API responses and serving static assets to reduce load on individual services
- **[Term: Hexagonal Architecture](term_hexagonal_architecture.md)** -- CDN is an infrastructure adapter in hexagonal architecture; the application core remains agnostic to whether content is served via CDN or directly from origin
- **[Term: Deep Modules](term_deep_modules.md)** -- A CDN is an example of a deep module: simple interface (serve content at a URL) hiding enormous internal complexity (global distribution, caching, failover, DDoS mitigation)

### Data Infrastructure
- **[Term: Elasticsearch](term_elasticsearch.md)** -- CDN access logs are commonly indexed in Elasticsearch for real-time analytics, cache hit ratio monitoring, and anomaly detection
- **[Term: Clickstream](term_clickstream.md)** -- CDN edge logs capture clickstream data (user requests, referrers, response codes) used for traffic analysis and user behavior modeling
- **[Term: Stream Processing](term_stream_processing.md)** -- CDN log streams are processed in real-time (via Kafka/Flink) for monitoring cache performance, detecting attacks, and triggering invalidation events

### Distributed Systems
- **[Term: Availability](term_availability.md)** -- CDNs improve system availability by serving cached content even when the origin is unreachable; edge redundancy provides geographic fault tolerance
- **[Term: Partition Tolerance](term_partition_tolerance.md)** -- CDN design inherently handles network partitions; edge servers continue serving cached content independently of origin connectivity
- **[Scalability](term_scalability.md)**: CDNs are a key scalability mechanism — they offload static content delivery from origin servers, enabling systems to handle orders-of-magnitude more traffic
- **[SSL Termination](term_ssl_termination.md)**: CDN edge servers perform TLS termination, handling the SSL/TLS handshake near the user to reduce connection latency and offload crypto from origin servers
- **[Cache Stampede](term_cache_stampede.md)**: CDN cache expiration events can trigger origin stampedes when many edge PoPs simultaneously refetch expired content; origin shield and stale-while-revalidate mitigate this
- **[Eviction Policy](term_eviction_policy.md)**: CDN edge caches use LRU or LRU-variant eviction policies to manage limited local storage; eviction of popular content can trigger origin fetches
- **[Reverse Proxy](term_reverse_proxy.md)**: CDN edge servers are geographically distributed reverse proxies -- they intercept client requests and serve cached content on behalf of origin servers, hiding the origin's identity and topology
- **[Latency](term_latency.md)**: CDNs reduce latency by serving content from edge locations closer to users (250ms → 20ms for distant users)

## References

### External References
- Nygren, E., Sitaraman, R., & Sun, J. (2010). "The Akamai Network: A Platform for High-Performance Internet Applications." *ACM SIGOPS Operating Systems Review*, 44(3). -- Foundational paper on commercial CDN architecture
- Dilley, J., et al. (2002). "Globally Distributed Content Delivery." *IEEE Internet Computing*, 6(5). -- Early architectural survey of CDN design
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. -- Chapters on caching, consistency, and distributed systems fundamentals
- AWS. ["What is a CDN?"](https://aws.amazon.com/what-is/cdn/) -- Amazon CloudFront overview and CDN fundamentals
- Cloudflare. ["What is a CDN?"](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) -- Cloudflare CDN educational resource
- Akamai. ["What is a CDN?"](https://www.akamai.com/glossary/what-is-a-cdn) -- Akamai CDN glossary entry
- Google Cloud. ["Cache Invalidation Overview."](https://docs.cloud.google.com/cdn/docs/cache-invalidation-overview) -- Google Cloud CDN cache invalidation strategies and cache tags

## Summary

| Aspect | Details |
|--------|---------|
| **Type** | Distributed network infrastructure |
| **Core principle** | Serve content from the nearest edge location to minimize latency and offload origin |
| **Key components** | Origin server, edge servers, PoPs, mid-tier caches, origin shield |
| **Delivery models** | Pull (on-demand origin fetch) vs. Push (proactive content upload) vs. Hybrid |
| **Cache invalidation** | TTL expiration, purge API, cache tags, versioned URLs, stale-while-revalidate |
| **Key benefit** | Lower latency, higher availability, reduced origin load, DDoS protection |
| **Key challenge** | Cache invalidation complexity, eventual consistency, cold-start cache misses |
| **Major providers** | CloudFront, Cloudflare, Akamai, Fastly, Google Cloud CDN, Azure CDN |

**Key Insight**: A CDN fundamentally trades **consistency** for **latency and availability** -- the same trade-off at the heart of the CAP theorem, applied to content delivery at global scale. By replicating content to edge servers near users, CDNs eliminate the latency penalty of centralized hosting but introduce the operational challenge of keeping distributed caches synchronized with the origin. The evolution of CDNs from simple static-asset caches to full edge-compute platforms (Cloudflare Workers, Lambda@Edge) represents a broader architectural trend: pushing computation to the network edge to reduce round trips, a principle that extends beyond content delivery to API gateways, authentication, personalization, and real-time data processing. In system design interviews and production architectures alike, the CDN is often the first and highest-leverage optimization for any globally distributed application.

---

**Last Updated**: April 19, 2026
**Status**: Active -- foundational infrastructure component in system design and web architecture
