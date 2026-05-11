---
tags:
  - resource
  - terminology
  - system_design
  - distributed_systems
  - algorithms
keywords:
  - Consistent Hashing
  - hash ring
  - virtual nodes
  - vnodes
  - data partitioning
  - distributed caching
  - minimal disruption
topics:
  - System Design
  - Distributed Systems
  - Data Partitioning
language: markdown
date of note: 2026-04-19
status: active
building_block: concept
related_wiki: null
---

# Consistent Hashing

## Definition

Consistent hashing is a distributed hashing technique that maps both data keys and server nodes onto a circular hash space (the "hash ring"), so that each key is assigned to the nearest node in the clockwise direction on the ring. Introduced by David Karger et al. at MIT in their 1997 paper "Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web," the technique was originally designed to balance load across web caches. Its defining property is **minimal disruption**: when a node is added or removed, only K/N keys on average need to be redistributed (where K is the total number of keys and N is the number of nodes), compared to traditional modular hashing where nearly all keys must be remapped.

In practice, naive consistent hashing with one point per physical node produces uneven load distribution because hash functions do not guarantee uniform spacing. The standard solution is **virtual nodes (vnodes)**: each physical node is assigned V points on the ring (typically 100-256 per node), which dramatically smooths the load distribution. For example, with 150 vnodes per node, the range of keys held by any single node narrows to approximately 18-22% variance from the ideal, versus 28% or more with physical nodes alone. Virtual nodes also simplify heterogeneous clusters, since higher-capacity machines can be assigned more vnodes proportionally. This combination of the hash ring structure and virtual nodes is the foundation of data partitioning in systems such as Amazon DynamoDB, Apache Cassandra, and Akamai's CDN infrastructure.

## Context

Consistent hashing is a foundational concept in system design interviews and distributed systems architecture (featured in the "System Design Deep Dive" podcast, Episodes 2, 4, and 5). It appears whenever a system must distribute data or requests across a dynamic set of nodes without requiring a full remapping on topology changes. The most influential real-world adoption was Amazon's Dynamo paper (2007), which demonstrated how consistent hashing with virtual nodes could partition petabytes of data across a key-value store while prioritizing availability. Today, consistent hashing underpins distributed caching layers (e.g., Memcached ring-based pools), distributed databases (Cassandra, DynamoDB, ScyllaDB, Riak), content delivery networks (Akamai, where co-inventor F. Thomson Leighton co-founded the company), and load balancers that need sticky session routing. In ML infrastructure, consistent hashing is relevant for partitioning feature stores, distributing embedding lookups, and sharding inference requests across GPU clusters.

## Key Characteristics

- **Hash ring topology**: Both keys and nodes are hashed onto a circular space (0 to 2^m - 1); each key is assigned to the first node encountered clockwise from its position
- **Minimal key redistribution**: Adding or removing a node only affects keys in the arc between the changed node and its predecessor, yielding O(K/N) key movements on average
- **Virtual nodes (vnodes)**: Each physical node maps to multiple positions on the ring (typically 100-256), ensuring even load distribution and supporting heterogeneous hardware by assigning more vnodes to higher-capacity machines
- **O(log N) lookup**: Using a sorted ring of node positions, key-to-node mapping requires O(log N) time via binary search
- **Replication-friendly**: Data can be replicated to the next R nodes clockwise on the ring, providing fault tolerance with minimal coordination overhead
- **Monotonicity**: When new nodes join, keys only move toward the new node — they never move between existing nodes, preserving cache validity
- **Decentralized**: No central directory is required; each node can independently compute key ownership given the ring membership, enabling peer-to-peer architectures
- **Hot spot mitigation**: Originally designed to relieve hot spots in web caching, the ring distributes popular keys across multiple physical nodes via vnodes
- **Comparison with rendezvous hashing**: An alternative approach (highest random weight hashing) achieves similar minimal-disruption properties but with O(N) lookup per key rather than O(log N)

## Related Terms

- **[CAP Theorem](term_cap_theorem.md)**: Consistent hashing is a key mechanism in AP systems (like DynamoDB and Cassandra) that choose availability over strict consistency during partitions
- **[DynamoDB](term_ddb.md)**: Amazon's key-value store that uses consistent hashing with virtual nodes for data partitioning, directly descended from the Dynamo paper
- **[Kafka](term_kafka.md)**: Distributed event streaming platform — uses partitioning strategies for topic distribution across brokers, analogous to hash-ring-based data placement
- **[LRU Cache](term_lru_cache.md)**: Eviction policy used within individual cache nodes; consistent hashing determines which node holds the cache entry, LRU determines what stays in that node
- **[CAP Tools and Systems](term_cap_tools_and_systems.md)**: Classification of distributed systems by their CAP trade-offs — consistent hashing is the partitioning layer enabling both CP and AP system designs
- **[Availability](term_availability.md)**: Consistent hashing improves availability by minimizing disruption during node failures, ensuring only a fraction of keys are affected
- **[Partition Tolerance](term_partition_tolerance.md)**: Consistent hashing supports partition-tolerant designs by enabling each node to independently compute key ownership without a central coordinator
- **[Consistency](term_consistency.md)**: In consistent-hashing-based systems, consistency is achieved through replication and quorum reads/writes across ring neighbors
- **[Microservices Architecture](term_microservices_architecture.md)**: Consistent hashing is used for request routing and session affinity across microservice instances
- **[NoSQL](term_nosql.md)**: NoSQL databases (DynamoDB, Cassandra, Riak) are the primary adopters of consistent hashing for horizontal data partitioning
- **[Space-Based Architecture](term_space_based_architecture.md)**: Distributed architecture pattern that uses data partitioning strategies including consistent hashing for in-memory data grids
- **[MongoDB](term_mongodb.md)**: Uses range-based and hash-based sharding; hash-based sharding is a form of consistent hashing for distributing documents across shards
- **[FLP Impossibility](term_flp_impossibility.md)**: Fundamental impossibility result for consensus in asynchronous systems — consistent hashing sidesteps consensus by enabling decentralized key ownership
- **[Amdahl's Law](term_amdahls_law.md)**: Consistent hashing enables near-linear horizontal scaling for data-parallel workloads, bounded by Amdahl's Law for any serial coordination overhead
- **[Scalability](term_scalability.md)**: Consistent hashing is a key enabler of horizontal scalability — it minimizes data redistribution when nodes are added or removed, enabling smooth scale-out
- **[PACELC](term_pacelc.md)**: Consistent hashing is a key partitioning mechanism in systems classified by PACELC -- PA/EL systems like Cassandra and DynamoDB use consistent hashing to distribute data while favoring availability and low latency
- **[Cache Stampede](term_cache_stampede.md)**: Consistent hashing determines which cache node owns a key; when that node fails, all its keys simultaneously miss, creating a stampede risk on the new owner
- **[Cassandra](term_cassandra.md)**: Apache Cassandra uses consistent hashing with virtual nodes (vnodes) to partition data across its masterless ring architecture, directly descended from the Dynamo paper's design
- **[Eviction Policy](term_eviction_policy.md)**: Consistent hashing routes keys to cache nodes; eviction policies manage what stays within each node when local capacity is exceeded
- **[Sharding](term_sharding.md)**: Consistent hashing is the primary technique for hash-based sharding that minimizes data redistribution when shards are added or removed
- **[Redshift Distribution Key](term_redshift_distribution_key.md)**: Redshift uses hash-based distribution to assign rows to compute node slices by distkey column value; conceptually equivalent to consistent hashing for data warehouse workloads
- **[Round Robin](term_round_robin.md)**: Round robin is the simplest load balancing alternative to consistent hashing -- round robin ignores key affinity and distributes requests sequentially, while consistent hashing provides deterministic key-to-server mapping for stateful workloads
- **[Database Replication](term_database_replication.md)**: Consistent hashing enables replication by placing replicas on the next R nodes clockwise on the ring -- systems like Cassandra and DynamoDB use this to co-locate partition replicas on distinct physical nodes for fault tolerance
- **[Vitess](term_vitess.md)**: MySQL sharding middleware that uses consistent hashing for shard key-to-shard mapping, enabling transparent horizontal scaling of MySQL databases
- **[Citus](term_citus.md)**: PostgreSQL sharding extension that uses hash-based distribution to assign rows to shards, leveraging consistent hashing principles for balanced data placement
- **[Memcached](term_memcached.md)**: Distributed caching system whose clients use consistent hashing for key-to-server distribution across the Memcached pool, ensuring minimal key redistribution when servers are added or removed
- **[Hotspot](term_hotspot.md)**: Consistent hashing mitigates hotspots by distributing keys across virtual nodes, preventing disproportionate load concentration on individual physical servers
- **[Data Partitioning](term_data_partitioning.md)**: Consistent hashing is the algorithm underlying hash-based data partitioning in distributed systems — it maps keys to partitions with minimal redistribution when the partition count changes
- **[Throughput](term_throughput.md)**: Consistent hashing distributes throughput across nodes with minimal redistribution when capacity changes

## References

- [Consistent Hashing -- Wikipedia](https://en.wikipedia.org/wiki/Consistent_hashing)
- Karger, D., Lehman, E., Leighton, T., Panigrahy, R., Levine, M., & Lewin, D. (1997). "Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web." Proceedings of the 29th Annual ACM Symposium on Theory of Computing (STOC), 654-663.
- DeCandia, G. et al. (2007). "Dynamo: Amazon's Highly Available Key-Value Store." Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP), 205-220.
- [Consistent Hashing -- GeeksforGeeks](https://www.geeksforgeeks.org/system-design/consistent-hashing/)
- [Consistent Hashing Explained -- AlgoMaster](https://blog.algomaster.io/p/consistent-hashing-explained)
- [Consistent Hashing -- System Design School](https://systemdesignschool.io/fundamentals/consistent-hashing)
