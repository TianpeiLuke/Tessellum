# Tessellum Runtime Traces

Top-level home for **session-scoped run artifacts**: capture-pipeline traces, retrieval-evaluation outputs, composer (DKS) chain run records.

## What lives here

| Subdirectory | Holds | Written by |
|---|---|---|
| `capture/` | Capture-pipeline traces (digest, distill, decompose runs) | Capture skills + future `tessellum capture <bb>` |
| `retrieval/` | Retrieval evaluation + benchmark traces | Future `tessellum search --eval` |
| `composer/` | DKS chain run traces (LLM calls + intermediate JSON) | Future `tessellum compose <chain>` |

## Lifecycle

**Gitignored.** Run artifacts are session-scoped and regenerable in principle; they don't ship in the wheel or the sdist. The directory structure is preserved in git via `.gitkeep` files in each subdirectory; this `README.md` is also tracked.

## Filename convention

`<YYYY-MM-DDThh-mm-ss>_<task-or-chain>.<ext>` — ISO-8601-ish timestamps for chronological ordering. Hyphens (not colons) in the time portion so the filename is portable across filesystems.

Examples:

- `runs/composer/2026-05-10T14-30-22_chain_decompose-paper-abc.json`
- `runs/retrieval/2026-05-10T09-15-00_bench_query-recall.json`
- `runs/capture/2026-05-10T11-02-44_digest_paper-foo.log`

## See also

- [`../plans/plan_cqrs_repo_layout.md`](../plans/plan_cqrs_repo_layout.md) — the architectural decision that put `runs/` here, including the System × lifecycle matrix.
