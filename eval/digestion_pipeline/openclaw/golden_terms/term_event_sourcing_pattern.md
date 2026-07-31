---
tags:
  - resource
  - terminology
  - distributed_systems
  - cloud_design_pattern
  - microservices
  - event_driven
keywords:
  - Event Sourcing
  - event store
  - event log
  - append-only events
  - state reconstruction
  - replay
  - projection
  - materialized view
  - temporal query
  - time-travel debugging
  - audit trail
  - CQRS
  - Martin Fowler
  - Greg Young
  - EventStoreDB
topics:
  - Distributed Systems
  - Cloud Design Patterns
  - Microservices
  - Data Persistence
  - Event-Driven Architecture
language: markdown
date of note: 2026-07-27
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Event Sourcing Pattern

## Definition

**Event Sourcing** is a data-persistence pattern in which the state of an application is captured not as the current values of its entities but as the full, ordered sequence of **immutable events** that describe every change those entities have undergone. Rather than storing "account balance = $80" and overwriting it on each transaction, an event-sourced system appends events such as `Deposited $100`, `Withdrew $20`, and derives the current balance by **replaying** them in order. The event log — the **event store** — is the single, authoritative source of truth, and it is strictly append-only: events are facts about the past and are never updated or deleted ([Fowler, "Event Sourcing"](https://martinfowler.com/eaaDev/EventSourcing.html)).

The pattern solves problems that arise when a system only keeps its latest state: lost history, weak auditability, and the inability to answer "how did we get here?" or "what did this look like last Tuesday?". Because every state transition is retained, an event-sourced system gains a complete **audit trail**, **temporal queries** and time-travel debugging, the ability to **rebuild** current state or entirely new read views (**projections**) by re-processing the log, and a natural integration point for other services that subscribe to the event stream. The pattern was popularized by Martin Fowler and elaborated by Greg Young alongside CQRS; it is implemented by purpose-built stores such as **EventStoreDB/Kurrent** and described in the [Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) and [AWS prescriptive guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/service-per-team.html). A familiar everyday analogue is **Git**, whose repository is an append-only chain of commits (change events) from which any working-tree state can be reconstructed.

## Context

Event Sourcing appears most often in event-driven microservices, domain-driven design (DDD), and cloud architectures where auditability, integration, and independent scaling of reads and writes matter. It is the canonical partner of **CQRS**: commands append events to the write-side event store, and the read side builds materialized projections optimized for querying by consuming that event stream — the two patterns are so frequently combined that they are usually discussed together as "CQRS/ES". Event Sourcing also pairs naturally with the **Saga** pattern (long-running distributed transactions coordinated through events) and with **idempotent** event handlers, since consumers must tolerate the same event being redelivered during replay or recovery.

Within a knowledge-management or agentic system, the same shape recurs: an append-only log of discrete change events replayed to reconstruct state. This general pattern is instantiated concretely by **term_event_ledger** (an OpenClaw-specific event ledger) and generalized by **term_append_only_state**; both are specializations or mechanisms of the pattern described here rather than duplicates of it. The write-ahead log (WAL) used by databases for crash recovery is a lower-level storage analogue of the same append-then-derive discipline.

## Key Characteristics

- **Append-only event store**: state changes are recorded as immutable, ordered events; the log is never mutated in place, only extended.
- **State as a derivation**: current state is a left-fold (replay) over the event stream, not a directly stored value.
- **Complete audit history**: every transition is retained with its cause and ordering, giving provenance "for free".
- **Temporal queries / time-travel**: any historical state can be reconstructed by replaying up to a chosen point, enabling debugging and retroactive analysis.
- **Rebuildable projections**: new read models or corrected views can be created at any time by re-projecting the existing events.
- **Snapshots for performance**: periodic snapshots (checkpoints) bound replay cost so long-lived aggregates need not replay from the beginning.
- **Natural integration point**: other services subscribe to the event stream, making Event Sourcing a strong fit for event-driven and pub/sub architectures.
- **Trade-offs**: eventual consistency between write log and read projections, event-schema versioning/migration challenges, replay latency without snapshots, and unbounded log growth requiring retention or compaction strategy.

## Related Terms


## References

- [Martin Fowler — "Event Sourcing"](https://martinfowler.com/eaaDev/EventSourcing.html) — the canonical article defining the pattern and its replay/audit properties.
- [Microsoft Learn — Azure Architecture Center: Event Sourcing pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) — production implementation guidance, benefits, trade-offs, and CQRS pairing.
- [AWS Prescriptive Guidance — Event sourcing / data persistence in microservices](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/service-per-team.html) — event store as source of truth in service-per-team modernization.
- [Kurrent (EventStoreDB) — What is Event Sourcing?](https://www.kurrent.io/event-sourcing) — purpose-built event store vendor's explanation of stores, streams, and projections.
- [Greg Young — CQRS Documents (PDF)](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf) — foundational long-form treatment of CQRS and event sourcing by their popularizer.
