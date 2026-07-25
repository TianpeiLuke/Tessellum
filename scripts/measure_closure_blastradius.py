#!/usr/bin/env python3
"""Measure the reverse-closure blast radius over a real vault index (P4, A4.1).

The plan calibrates P4's VALIDATION fan-out bound + spill threshold from data,
not a guess: over a random sample of seed notes, report the depth-limited
reverse-reachability set size distribution (mean / median / p90 / p99 / max, as
a %% of the corpus) under a given :class:`ClosurePolicy`. The measured p99 is
what should set ``ClosurePolicy.spill_fraction`` / ``spill_abs``.

This is a diagnostic harness — it never mutates the vault or the index. It reads
the shipped ``notes`` + ``note_links`` index (the same one retrieval uses).

Usage:
    python scripts/measure_closure_blastradius.py <index.db> [--sample N]
        [--depth D] [--hub-threshold H] [--seed S]

Example:
    python scripts/measure_closure_blastradius.py data/tessellum.db --sample 500
"""

from __future__ import annotations

import argparse
import random
import sqlite3
import statistics
import sys
from pathlib import Path

# Allow running from a source checkout without install.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tessellum.composer.write_closure import ClosurePolicy, validation_set  # noqa: E402


def _load(conn: sqlite3.Connection):
    """Return (note_ids, note_category_of, reverse_adj, in_degree_of)."""
    note_category_of: dict[str, str] = {}
    note_ids: list[str] = []
    for row in conn.execute("SELECT note_id, note_category FROM notes"):
        note_ids.append(row[0])
        if row[1] is not None:
            note_category_of[row[0]] = row[1]

    reverse_adj: dict[str, list[str]] = {}  # target -> [sources] (predecessors)
    in_degree_of: dict[str, int] = {}
    for src, tgt in conn.execute(
        "SELECT source_note_id, target_note_id FROM note_links"
    ):
        reverse_adj.setdefault(tgt, []).append(src)
        in_degree_of[tgt] = in_degree_of.get(tgt, 0) + 1
    return note_ids, note_category_of, reverse_adj, in_degree_of


def _pct(sorted_vals: list[float], q: float) -> float:
    if not sorted_vals:
        return 0.0
    k = max(0, min(len(sorted_vals) - 1, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[k]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("index_db", type=Path)
    ap.add_argument("--sample", type=int, default=500)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--hub-threshold", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)  # explicit → reproducible
    args = ap.parse_args()

    conn = sqlite3.connect(str(args.index_db))
    try:
        note_ids, note_category_of, reverse_adj, in_degree_of = _load(conn)
    finally:
        conn.close()

    corpus = len(note_ids)
    if corpus == 0:
        print("empty index — nothing to measure")
        return 1

    rng = random.Random(args.seed)
    sample_ids = (
        note_ids if args.sample >= corpus else rng.sample(note_ids, args.sample)
    )
    policy = ClosurePolicy(
        hub_threshold=args.hub_threshold,
        validation_depth=args.depth,
        spill_fraction=1.0,  # measuring — never trip spill here
    )

    sizes: list[int] = []
    for nid in sample_ids:
        res = validation_set(
            frozenset({nid}),
            reverse_adj=reverse_adj,
            corpus_size=corpus,
            note_category_of=note_category_of,
            in_degree_of=in_degree_of,
            policy=policy,
        )
        sizes.append(res.size)

    sizes.sort()
    pct_of = lambda v: 100.0 * v / corpus  # noqa: E731
    mean = statistics.mean(sizes) if sizes else 0.0
    median = statistics.median(sizes) if sizes else 0.0
    p90, p99, mx = _pct(sizes, 0.90), _pct(sizes, 0.99), (sizes[-1] if sizes else 0)

    print(f"corpus notes         : {corpus}")
    print(f"sample seeds         : {len(sample_ids)}")
    print(f"depth / hub_threshold: {args.depth} / {args.hub_threshold}")
    print(f"reverse-closure size (nodes | %% corpus):")
    print(f"  mean   : {mean:8.2f} | {pct_of(mean):6.3f}%")
    print(f"  median : {median:8.2f} | {pct_of(median):6.3f}%")
    print(f"  p90    : {p90:8.2f} | {pct_of(p90):6.3f}%")
    print(f"  p99    : {p99:8.2f} | {pct_of(p99):6.3f}%")
    print(f"  max    : {mx:8.2f} | {pct_of(mx):6.3f}%")
    print()
    print(f"suggested spill bound: p99 = {p99} nodes "
          f"(spill_fraction ~= {pct_of(p99) / 100:.4f}); "
          f"set ClosurePolicy.spill_abs above this + a margin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
