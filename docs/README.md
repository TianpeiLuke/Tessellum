# Tessellum — Engineering Documentation

How the **Tessellum 1.0** code is built, and why.

> **Two surfaces, by audience.** This `docs/` tree is the *engineering* reference. The [`vault/`](../vault/)
> is the *knowledge* documentation — Tessellum dogfoods itself, so its concepts, how-tos, and design
> arguments live as typed atomic notes. Start there at
> [`vault/0_entry_points/entry_master_toc.md`](../vault/0_entry_points/entry_master_toc.md).

Within `docs/`, knowledge is split by type. The **design docs** (`docs/<module>.md`) explain the ideas —
the model each part builds, the procedure it runs, and the decisions behind it — in prose meant to be read
start to finish. The **reference** (`docs/reference/<module>.md`) is the lookup surface: file→role tables,
public signatures, constants, and flags, dense on purpose. Read the design doc to understand a subsystem;
open the reference when you need an exact name.

## Start here

**[architecture.md](architecture.md)** — the whole system as one picture. The CQRS wall between authorship
(System P, the markdown vault) and computation (System D, the SQLite index and retrieval), the operational
runtime that feeds Composer without becoming a knowledge authority, and the invariants that keep each layer
honest.

## Modules

| Module | Design | Reference |
|---|---|---|
| Automatic runtime — durable inbox admission and supervision | [runtime.md](runtime.md) | [reference/runtime.md](reference/runtime.md) |
| Composer — the typed-contract pipeline runtime | [composer.md](composer.md) | [reference/composer.md](reference/composer.md) |
| DKS — the dialectic knowledge engine | [dks.md](dks.md) | [reference/dks.md](reference/dks.md) |
| Retrieval — the five read surfaces | [retrieval.md](retrieval.md) | [reference/retrieval.md](reference/retrieval.md) |
| Indexer — vault → SQLite | [indexer.md](indexer.md) | [reference/indexer.md](reference/indexer.md) |
| BB — the Building Block ontology | [bb.md](bb.md) | [reference/bb.md](reference/bb.md) |
| Format — the note validator | [format.md](format.md) | [reference/format.md](reference/format.md) |
| CLI — the command surface | [cli.md](cli.md) | [reference/cli.md](reference/cli.md) |
| MCP — the agent tool server | [mcp.md](mcp.md) | [reference/mcp.md](reference/mcp.md) |

When code and docs disagree, the **code is truth** — open an issue or a PR against the doc.
