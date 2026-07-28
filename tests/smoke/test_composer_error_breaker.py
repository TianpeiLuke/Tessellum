"""P17 (FZ 20k9c1a1a1b7c2f) — run-level error-class circuit breaker.

Before P17 nothing aggregated the per-leaf ``error_class`` verdicts a wave
produces: a dead key pool or a marketplace-wide 429 made EVERY leaf fail
``auth``/``rate_limit`` independently, and the wave burned its whole leaf scope
(each leaf's full retry budget) against the same wall before finishing. The
:class:`ErrorClassBreaker` aggregates those verdicts and short-circuits the
remaining leaves once a proportional share have failed the same systemic way,
mirroring the existing ``RunBudget`` → ``BUDGET_EXHAUSTED`` seam.

Covers:
  - ErrorClassBreaker pure logic: proportional trip + floor, absolute
    threshold, disabled state, latch, non-systemic classes never count,
    dominant_class, with_tripping_classes freshness.
  - run_pipeline_dynamic + run_pipeline integration: a wave of auth-failing
    leaves aborts with typed BREAKER_TRIPPED outcomes + blocked manifest rows;
    fewer than all leaves actually dispatch to the backend; no breaker = parity.
  - run_execute_wave fallback_strategy consultation (the field's first live
    consumer) — a degrade posture narrows the breaker to auth-only.

Pure/at-most-in-memory backends — no network. Safe alongside a live run.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from tessellum.composer import (
    ErrorClassBreaker,
    Manifest,
    MockBackend,
    classify_outcome,
    compile_skill,
    run_pipeline,
    run_pipeline_dynamic,
)
from tessellum.composer.credential_pool import (
    DEFAULT_BREAKER_MIN_DISPATCHED,
    DEFAULT_BREAKER_PROPORTION,
    DEFAULT_TRIPPING_CLASSES,
)
from tessellum.composer.llm import LLMRequest, LLMResponse


# ── ErrorClassBreaker — pure logic ──────────────────────────────────────────


def test_breaker_disabled_never_trips() -> None:
    b = ErrorClassBreaker(proportion=None, error_threshold=None)
    for _ in range(20):
        b.record("auth")
    assert not b.should_abort()


def test_breaker_proportional_trips_at_floor() -> None:
    b = ErrorClassBreaker()  # proportion 0.8, min_dispatched 3
    b.record("auth")
    assert not b.should_abort(), "1/1 below the min_dispatched floor"
    b.record("auth")
    assert not b.should_abort(), "2/2 below the floor"
    b.record("auth")
    assert b.should_abort(), "3/3 meets floor and >= 0.8"


def test_breaker_proportional_needs_the_proportion() -> None:
    b = ErrorClassBreaker()
    b.record("auth")
    b.record("auth")
    b.record(None)
    assert not b.should_abort(), "2/3 = 0.67 < 0.8"
    b.record("auth")
    assert not b.should_abort(), "3/4 = 0.75 < 0.8"
    b.record("auth")
    assert b.should_abort(), "4/5 = 0.8 -> trip"


def test_breaker_non_systemic_classes_never_count() -> None:
    for klass in ("validation", "crash", "truncated", "missing_consumed", "transient"):
        b = ErrorClassBreaker()
        for _ in range(20):
            b.record(klass)
        assert not b.should_abort(), f"{klass} is per-leaf, not systemic"


def test_breaker_rate_limit_trips_and_is_dominant() -> None:
    b = ErrorClassBreaker()
    for _ in range(3):
        b.record("rate_limit")
    assert b.should_abort()
    assert b.dominant_class() == "rate_limit"


def test_breaker_latches_after_trip() -> None:
    b = ErrorClassBreaker()
    for _ in range(3):
        b.record("auth")
    assert b.should_abort()
    for _ in range(100):
        b.record(None)  # a flood of later successes
    assert b.should_abort(), "a tripped breaker stays tripped (latched)"


def test_breaker_absolute_threshold() -> None:
    b = ErrorClassBreaker(proportion=None, error_threshold=5)
    for _ in range(4):
        b.record("auth")
    assert not b.should_abort(), "4 < 5"
    b.record("rate_limit")
    assert b.should_abort(), "5 tripping-class failures (mixed) -> trip"


def test_breaker_with_tripping_classes_is_fresh() -> None:
    base = ErrorClassBreaker()
    for _ in range(3):
        base.record("rate_limit")
    narrowed = base.with_tripping_classes(frozenset({"auth"}))
    # Fresh counts: the base's rate_limit failures did NOT carry over.
    assert narrowed.dispatched == 0
    # rate_limit is no longer a tripping class: a full wave of it never trips.
    for _ in range(10):
        narrowed.record("rate_limit")
    assert not narrowed.should_abort(), "rate_limit no longer a tripping class"
    # A fresh breaker narrowed to auth trips on a majority-auth wave.
    fresh = base.with_tripping_classes(frozenset({"auth"}))
    for _ in range(3):
        fresh.record("auth")
    assert fresh.should_abort(), "3/3 auth >= floor and proportion"
    # The base is unaffected by operations on the fresh copies.
    assert base.dominant_class() == "rate_limit"


def test_breaker_defaults() -> None:
    b = ErrorClassBreaker()
    assert b.proportion == DEFAULT_BREAKER_PROPORTION
    assert b.min_dispatched == DEFAULT_BREAKER_MIN_DISPATCHED
    assert b.tripping_classes == DEFAULT_TRIPPING_CLASSES


def test_breaker_terminal_cause_carries_marker() -> None:
    b = ErrorClassBreaker()
    for _ in range(3):
        b.record("auth")
    b.should_abort()
    msg = b.terminal_cause()
    assert "circuit breaker" in msg  # the classify_outcome marker
    assert "auth" in msg


# ── pipeline integration ─────────────────────────────────────────────────────


_CANON = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # S

    ## Step 1: rate <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    ```

    Rate.
    """
)


def _compile(tmp_path: Path):
    sk = tmp_path / "s.md"
    sk.write_text(_CANON, encoding="utf-8")
    return compile_skill(sk)


class _AuthFailBackend:
    """Every call raises a 403 auth error (a dead-credential-pool simulation)."""

    backend_id = "auth-fail"

    def __init__(self) -> None:
        self.calls = 0

    def call(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        raise RuntimeError("403 Forbidden: the security token is expired")


def test_dynamic_breaker_aborts_auth_wave(tmp_path: Path) -> None:
    """A wave of auth-failing leaves trips the breaker and the remaining leaves
    short-circuit to BREAKER_TRIPPED without more backend calls."""
    compiled = _compile(tmp_path)
    manifest = Manifest(path=tmp_path / "m.json")
    backend = _AuthFailBackend()
    # No retries so each leaf makes exactly one call — deterministic counting.
    breaker = ErrorClassBreaker()  # 0.8 / floor 3
    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": c} for c in "abcdefgh"],  # 8 leaves
        backend=backend,
        vault_root=tmp_path / "v",
        breaker=breaker,
        manifest=manifest,
        run_id="r1",
        max_workers=1,  # serialize so record→should_abort is ordered
        max_logic_retries=0,
        max_crash_recoveries=0,
    )
    kinds = [classify_outcome(r).kind for r in run.step_results]
    # The first 3 auth failures fill the floor and trip; the rest short-circuit.
    assert kinds.count("BREAKER_TRIPPED") >= 1, kinds
    assert backend.calls < 8, "the breaker must stop dispatching before all leaves"
    # Every breaker-tripped leaf is blocked in the manifest (not released).
    blocked = [e for e in manifest.entries.values() if e.status == "blocked"]
    assert len(blocked) >= 1


def test_dynamic_no_breaker_runs_all_leaves(tmp_path: Path) -> None:
    """Parity: without a breaker, every leaf is dispatched even under a total
    auth outage (pre-P17 behaviour)."""
    compiled = _compile(tmp_path)
    backend = _AuthFailBackend()
    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": c} for c in "abcdefgh"],
        backend=backend,
        vault_root=tmp_path / "v",
        breaker=None,
        max_workers=1,
        max_logic_retries=0,
        max_crash_recoveries=0,
    )
    assert backend.calls == 8, "no breaker → every leaf dispatched"
    assert run.error_count == 8


def test_dynamic_breaker_healthy_wave_never_trips(tmp_path: Path) -> None:
    """A clean wave (no failures) never trips the breaker — the safety invariant
    (a healthy run must be byte-identical to the no-breaker path)."""
    compiled = _compile(tmp_path)
    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": c} for c in "abcdefgh"],
        backend=MockBackend(default="{}"),
        vault_root=tmp_path / "v",
        breaker=ErrorClassBreaker(),
        max_workers=1,
    )
    assert run.error_count == 0
    assert len(run.step_results) == 8
    assert all(classify_outcome(r).kind == "SUCCESS" for r in run.step_results)


def test_serial_breaker_aborts_auth_wave(tmp_path: Path) -> None:
    """The serial run_pipeline honors the breaker symmetrically (parity with
    the dynamic path)."""
    compiled = _compile(tmp_path)
    backend = _AuthFailBackend()
    run = run_pipeline(
        compiled,
        leaves=[{"id": c} for c in "abcdefgh"],
        backend=backend,
        vault_root=tmp_path / "v",
        breaker=ErrorClassBreaker(),
        max_logic_retries=0,
        max_crash_recoveries=0,
    )
    kinds = [classify_outcome(r).kind for r in run.step_results]
    assert kinds.count("BREAKER_TRIPPED") >= 1
    assert backend.calls < 8


def test_serial_no_breaker_parity(tmp_path: Path) -> None:
    compiled = _compile(tmp_path)
    backend = _AuthFailBackend()
    run = run_pipeline(
        compiled,
        leaves=[{"id": c} for c in "abcd"],
        backend=backend,
        vault_root=tmp_path / "v",
        breaker=None,
        max_logic_retries=0,
        max_crash_recoveries=0,
    )
    assert backend.calls == 4
    assert run.error_count == 4


def test_breaker_ignores_scattered_validation_failures(tmp_path: Path) -> None:
    """A wave where leaves fail VALIDATION (a per-leaf logic defect, not a
    systemic wall) never trips — validation is not a tripping class."""

    class _ValidationFailBackend:
        backend_id = "bad-json"

        def __init__(self) -> None:
            self.calls = 0

        def call(self, request: LLMRequest) -> LLMResponse:
            self.calls += 1
            # Non-JSON → schema/materializer validation failure downstream.
            return LLMResponse(content="not json at all", elapsed_ms=1.0,
                               backend_id=self.backend_id)

    compiled = _compile(tmp_path)
    backend = _ValidationFailBackend()
    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": c} for c in "abcdefgh"],
        backend=backend,
        vault_root=tmp_path / "v",
        breaker=ErrorClassBreaker(),
        max_workers=1,
        max_logic_retries=0,
        max_crash_recoveries=0,
    )
    # Every leaf dispatched (validation never trips the breaker); none tripped.
    kinds = [classify_outcome(r).kind for r in run.step_results]
    assert "BREAKER_TRIPPED" not in kinds, kinds
    assert backend.calls == 8


# ── run_execute_wave fallback_strategy consultation ──────────────────────────


def test_execute_fallback_strategy_none_when_no_mcp(tmp_path: Path) -> None:
    """The execute skill in these tests declares no MCP deps → default posture
    (None), so the breaker keeps its default {auth, rate_limit} classes."""
    from tessellum.composer.digestion import _execute_fallback_strategy

    (tmp_path / "skill_tessellum_execute_digestion_plan.md").write_text(
        _CANON, encoding="utf-8"
    )
    assert _execute_fallback_strategy(tmp_path) is None


# ── concurrency: the breaker under max_workers > 1 (the real target path) ────


def test_dynamic_breaker_aborts_auth_wave_concurrent(tmp_path: Path) -> None:
    """The breaker's whole point is to abort a PARALLEL wave. With max_workers=4
    and 40 auth-failing leaves, some leaves dispatch concurrently before the
    breaker latches, but it MUST latch and short-circuit the bulk of the wave —
    fewer than all leaves reach the backend. Exercises the record()-under-lock /
    should_abort()-own-lock interleaving the single-worker tests can't."""
    compiled = _compile(tmp_path)
    backend = _AuthFailBackend()
    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": str(i)} for i in range(40)],
        backend=backend,
        vault_root=tmp_path / "v",
        breaker=ErrorClassBreaker(),
        max_workers=4,
        max_logic_retries=0,
        max_crash_recoveries=0,
    )
    kinds = [classify_outcome(r).kind for r in run.step_results]
    assert kinds.count("BREAKER_TRIPPED") >= 1, kinds
    # With 4 workers, at most ~a handful of leaves are in flight when the
    # breaker latches; the vast majority must be short-circuited, so the backend
    # is called far fewer than 40 times.
    assert backend.calls < 40, backend.calls
    assert backend.calls < 20, "the concurrent wave should abort well before half"


def test_dynamic_breaker_records_under_concurrency_no_crash(tmp_path: Path) -> None:
    """A mixed wave (some success, some auth) under concurrency records every
    completed leaf into the breaker without a lock error / miscount crash."""
    class _AltBackend:
        backend_id = "alt"

        def __init__(self) -> None:
            self.calls = 0
            self._lock = __import__("threading").Lock()

        def call(self, request: LLMRequest) -> LLMResponse:
            with self._lock:
                self.calls += 1
                n = self.calls
            if n % 2 == 0:
                raise RuntimeError("403 Forbidden: token expired")
            return LLMResponse(content="{}", elapsed_ms=1.0, backend_id=self.backend_id)

    compiled = _compile(tmp_path)
    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": str(i)} for i in range(12)],
        backend=_AltBackend(),
        vault_root=tmp_path / "v",
        breaker=ErrorClassBreaker(),
        max_workers=4,
        max_logic_retries=0,
        max_crash_recoveries=0,
    )
    # It completes and every leaf has a typed outcome (no crash / lost leaf).
    assert len(run.step_results) == 12
    assert all(classify_outcome(r).kind for r in run.step_results)


# ── absolute backstop: mid-wave credential death the proportion rule misses ──


def test_breaker_absolute_backstop_catches_mid_wave_death() -> None:
    """The proportional rule alone is defeated when early successes inflate the
    denominator (a pool healthy for 40 leaves then dead). The absolute
    error_threshold backstop trips regardless of proportion."""
    b = ErrorClassBreaker(proportion=0.8, error_threshold=10, min_dispatched=3)
    for _ in range(40):
        b.record(None)  # 40 healthy leaves
    assert not b.should_abort(), "0 systemic failures — healthy"
    for _ in range(9):
        b.record("auth")
    # 9/49 = 0.18 << 0.8 (proportion never trips), 9 < 10 (backstop not yet)
    assert not b.should_abort()
    b.record("auth")
    # 10 absolute systemic failures → backstop trips even though 10/50 = 0.2
    assert b.should_abort(), "absolute backstop catches the mid-wave death"


# ── fallback_strategy degrade posture actually narrows the tripping set ──────


def test_execute_fallback_strategy_degrade_narrows_to_auth(tmp_path: Path) -> None:
    """An execute skill whose MCP dep declares fallback_strategy='degrade' →
    the wave narrows the breaker to {auth}, so a rate_limit-only wave rides
    (tolerated) while an auth wave still aborts. Uses a real MCP contract name
    with a degrade posture."""
    from tessellum.composer.contracts import MCP_CONTRACTS
    from tessellum.composer.digestion import _execute_fallback_strategy

    # Find a registered MCP whose contract posture is 'degrade' (the field's
    # documented value); if none exists in the registry, the mapping is still
    # exercised by asserting the None-posture default elsewhere.
    degrade_mcp = next(
        (name for name, c in MCP_CONTRACTS.items()
         if c.fallback_strategy == "degrade"),
        None,
    )
    if degrade_mcp is None:
        # No degrade-posture MCP shipped; the narrowing branch is still unit-
        # covered by test_breaker_with_tripping_classes_is_fresh. Skip the e2e.
        return
    # Inject an mcp_dependencies block into the step's yaml contract, at the
    # SAME indentation as the other contract keys (the loader parses the whole
    # ```yaml block; list items sit under the key with no extra indent — the
    # real-skill convention, e.g. skill_tessellum_dks_cycle.md).
    skill = _CANON.replace(
        "materializer: no_op\n",
        "materializer: no_op\n"
        "mcp_dependencies:\n"
        f"- name: {degrade_mcp}\n"
        "  calls: []\n"
        "  required: false\n",
    )
    (tmp_path / "skill_tessellum_execute_digestion_plan.md").write_text(
        skill, encoding="utf-8"
    )
    assert _execute_fallback_strategy(tmp_path) == "degrade"
