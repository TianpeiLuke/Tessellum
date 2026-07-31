---
tags:
  - resource
  - terminology
  - discriminated-union
  - tagged-union
  - typescript-pattern
  - type-narrowing
keywords:
  - Discriminated union
  - tagged union
  - sum type
  - type narrowing
  - ADT
  - sealed class
topics:
  - Type systems
  - Functional programming patterns
  - TypeScript
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Tagged_union
access_control_group: ["general"]
---

# Discriminated Union

## Definition

A **discriminated union** (also called **tagged union**, **sum type**, **variant**, **choice type**, or **algebraic data type / ADT**) is a composite type whose value is exactly one of a fixed set of alternative shapes, where each alternative carries a distinguishing **tag** (the discriminant) that lets code identify which shape is in use and access only the fields valid for that shape. In TypeScript specifically, the pattern is realised at the type level: each member of a union type declares a common property typed as a **literal type** (e.g. `kind: "fork"`), and the compiler uses ordinary control-flow analysis on that property — typically a `switch (x.kind)` — to **narrow** the union to the single matching member inside each branch.

The same idea appears under different names across paradigms: ML and Haskell call them **algebraic data types** (introduced via `data` declarations); Rust and Swift call them **enums** with associated data; F# calls them **discriminated unions** outright; Scala and Kotlin model them as **sealed classes / sealed interfaces** with case classes / `data class` arms; C# 15 introduces a `union` keyword. The Wikipedia article lists them all as the same construct — a sum type, dual to the product type (record / tuple), in the algebra of data types.

## Context

Discriminated unions appear wherever a value has a fixed, mutually exclusive set of shapes — state machines, result envelopes, parsed message types, AST nodes, command/event types. Functional languages have used them as the primary structural device since ML in the 1970s; systems languages adopted them via Rust's `enum`; the OO world reached them later via Scala/Kotlin sealed hierarchies and now C#15 `union`. TypeScript's version is unusual in that it is purely a **type-level** construct — at runtime the value is just a plain JavaScript object with a string tag field, so the pattern has **zero runtime cost** beyond the tag itself.

OpenClaw — the TypeScript codebase backing the BTW agent harness — uses discriminated unions extensively for result envelopes and state classification. Representative examples:

- **`PreparedSpawnContext`** (subagent-spawn): three arms `ok+isolated`, `ok+fork`, `error`, with a `?: never` exclusion that forbids `forkFallbackNote` on the success-fork arm so a constructor cannot accidentally include it.
- **`CooldownDecision`** (model-failover): classifies whether the failover cool-down has expired, is still active, or short-circuited.
- **`ExternalContentSource`** (security/external-content): identifies the provenance of injected content (user-supplied, fetched, tool-emitted) so policy can branch on origin.
- **`ChannelMatchSource`** (channels): tags how a channel route was resolved (alias, prefix, fallback).
- **`LedgerSession`** event types (ACP event-ledger): a closed union over every event variant the ledger persists.

In every case the tag is a literal-typed string field (`kind`, `status`, `mode`, `source`) and consumers dispatch on it through `switch` with an exhaustiveness check.

## Key Characteristics

- **Literal-type discriminator**: each union member declares a common field (often `kind`, `type`, `status`, `tag`) typed as a single string literal (`"circle"`, not `string`). The literal type is what makes narrowing precise.
- **Switch narrowing**: inside `case "circle":`, TypeScript narrows the value to the member whose tag equals `"circle"`, so member-specific fields become accessible without casts or `?.` guards.
- **Exhaustiveness via `: never`**: a `default:` branch that assigns the discriminated value to `const _: never = x;` becomes a compile-time error the moment a new arm is added without updating the switch — a load-bearing safety net for evolving codebases.
- **`?: never` field exclusion**: a field can be explicitly forbidden on certain arms (e.g. `forkFallbackNote?: never` on the `ok+fork` arm of `PreparedSpawnContext`), so a single-shape escape from one arm cannot leak into another.
- **Zero runtime cost in TypeScript**: at runtime the value is a plain object with a tag field; there is no class hierarchy, no `instanceof`, no boxing. All the safety lives in the type checker.
- **Closed-world by design**: unlike inheritance (open for extension), a discriminated union is closed — the compiler knows every arm, which is what makes exhaustiveness checks possible. Adding an arm is a deliberate, breaking change.
- **Tag-first, not nullable**: prefer `{ kind: "ok"; value: T } | { kind: "err"; error: E }` over `T | null` or `T | undefined` whenever the failure mode carries information; the tag forces callers to acknowledge the error case.
- **Cross-language equivalents**: Rust `enum`, Haskell `data`, F# `type X =`, Scala `sealed trait` + case classes, Kotlin `sealed class`, Swift `enum` with associated values, C#15 `union`.

## Related Terms


## Related Code Snippets

- (code snippet) `snippet_openclaw_agents_subagent_spawn_caps.md` — defines `PreparedSpawnContext` with `ok+isolated` / `ok+fork` / `error` arms and the `forkFallbackNote?: never` exclusion.
- (code snippet) `snippet_openclaw_agents_model_fallback_cooldown.md` — `CooldownDecision` discriminated union over cool-down classification states.
- (code snippet) `snippet_openclaw_security_external_content.md` — `ExternalContentSource` union tagging the provenance of injected content.
- (code snippet) `snippet_openclaw_channels_match_resolver.md` — `ChannelMatchSource` union tagging how a channel route was resolved.
- (code snippet) `snippet_openclaw_acp_event_ledger.md` — `LedgerSession` event-type union persisted by the ACP event ledger.

## References

- [TypeScript Handbook — Narrowing: Discriminated Unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)
- [Tagged union — Wikipedia](https://en.wikipedia.org/wiki/Tagged_union)
- [Tagged Union Types in TypeScript — Marius Schulz](https://mariusschulz.com/blog/tagged-union-types-in-typescript)
- [Discriminated Unions — F# for fun and profit](https://fsharpforfunandprofit.com/posts/discriminated-unions/)
- [TypeScript discriminated unions, and trying to mimic Rust enums — P. Burris](https://www.pburris.me/blog/ts-discriminated-union-rust-enums)
