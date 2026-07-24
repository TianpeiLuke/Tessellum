"""Composer v4, Phase 5 — credential pool + run-level budgets.

Covers:
  - CredentialPool: least-used lease, no double-lease under concurrency,
    error-class rotation (transient keeps lease; rate_limit/quota/auth
    bench + release), differentiated cooldowns, cooldown persistence.
  - RunBudget: invocation + cost caps, all-or-nothing try_spend,
    remaining/is_exhausted.
  - effort_for_stage tiers.
  - run_pipeline_dynamic budget integration: a runaway leaf-set halts with
    typed BUDGET_EXHAUSTED outcomes + blocked manifest rows; no budget =
    parity.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from tessellum.composer import (
    CredentialPool,
    CredentialPoolError,
    Manifest,
    MockBackend,
    RunBudget,
    classify_outcome,
    compile_skill,
    effort_for_stage,
    run_pipeline_dynamic,
)
from tessellum.composer.credential_pool import (
    COOLDOWN_QUOTA_SECS,
    COOLDOWN_RATE_LIMIT_SECS,
    DEFAULT_STAGE_EFFORT,
)
from tessellum.composer.llm import LLMRequest, LLMResponse


# ── CredentialPool ──────────────────────────────────────────────────────────


def test_pool_leases_least_used_first() -> None:
    p = CredentialPool(key_ids=("k1", "k2"))
    # First two leases hand out both distinct keys (both use_count 0 → tie
    # broken by id order → k1, then k2).
    a = p.lease("w1", now=0.0)
    b = p.lease("w2", now=0.0)
    assert {a, b} == {"k1", "k2"}


def test_pool_no_double_lease() -> None:
    p = CredentialPool(key_ids=("k1",))
    p.lease("w1", now=0.0)
    try:
        p.lease("w2", now=0.0)
        raise AssertionError("expected CredentialPoolError")
    except CredentialPoolError:
        pass


def test_pool_release_returns_key_to_the_pool() -> None:
    p = CredentialPool(key_ids=("k1",))
    k = p.lease("w1", now=0.0)
    assert p.release(k, "w1") is True
    # Now leasable again.
    assert p.lease("w2", now=0.0) == "k1"


def test_pool_release_guards_wrong_owner() -> None:
    p = CredentialPool(key_ids=("k1",))
    p.lease("w1", now=0.0)
    assert p.release("k1", "someone_else") is False


def test_pool_transient_keeps_lease() -> None:
    p = CredentialPool(key_ids=("k1", "k2"))
    k = p.lease("w1", now=0.0)
    # Transient (soft 429) → retry the same key; lease NOT released, key
    # NOT benched.
    assert p.report_failure(k, "w1", "transient", now=1.0) is False
    assert p.available_count(now=1.0) == 1  # the other key


def test_pool_rate_limit_benches_one_hour() -> None:
    p = CredentialPool(key_ids=("k1",))
    k = p.lease("w1", now=0.0)
    assert p.report_failure(k, "w1", "rate_limit", now=100.0) is True
    # Benched for COOLDOWN_RATE_LIMIT_SECS.
    assert p.available_count(now=100.0) == 0
    assert p.available_count(now=100.0 + COOLDOWN_RATE_LIMIT_SECS - 1) == 0
    assert p.available_count(now=100.0 + COOLDOWN_RATE_LIMIT_SECS + 1) == 1


def test_pool_quota_benches_one_day() -> None:
    p = CredentialPool(key_ids=("k1",))
    k = p.lease("w1", now=0.0)
    assert p.report_failure(k, "w1", "quota", now=0.0) is True
    assert p.available_count(now=COOLDOWN_RATE_LIMIT_SECS + 1) == 0  # still benched
    assert p.available_count(now=COOLDOWN_QUOTA_SECS + 1) == 1


def test_pool_auth_benches_long() -> None:
    p = CredentialPool(key_ids=("k1",))
    k = p.lease("w1", now=0.0)
    assert p.report_failure(k, "w1", "auth", now=0.0) is True
    assert p.available_count(now=COOLDOWN_QUOTA_SECS - 1) == 0


def test_pool_cooldown_persistence_round_trip() -> None:
    p = CredentialPool(key_ids=("k1", "k2"))
    k = p.lease("w1", now=0.0)
    p.report_failure(k, "w1", "rate_limit", now=50.0)
    cooldowns = p.to_cooldowns()
    assert k in cooldowns

    restored = CredentialPool(key_ids=("k1", "k2"))
    restored.load_cooldowns(cooldowns)
    # The benched key is still benched after a "restart".
    assert restored.available_count(now=50.0) == 1  # only the un-benched key


def test_pool_report_failure_wrong_owner_is_noop() -> None:
    p = CredentialPool(key_ids=("k1",))
    p.lease("w1", now=0.0)
    assert p.report_failure("k1", "intruder", "rate_limit", now=0.0) is False


# ── RunBudget ───────────────────────────────────────────────────────────────


def test_budget_invocation_cap() -> None:
    b = RunBudget(max_invocations=2)
    assert b.try_spend()
    assert b.try_spend()
    assert not b.try_spend()  # third refused
    assert b.invocations == 2
    assert b.is_exhausted()


def test_budget_cost_cap_all_or_nothing() -> None:
    b = RunBudget(max_cost=5.0)
    assert b.try_spend(4.0)
    assert not b.try_spend(2.0)  # would exceed → refused, nothing charged
    assert b.cost == 4.0
    assert b.invocations == 1  # the refused spend didn't count


def test_budget_unbounded_by_default() -> None:
    b = RunBudget()
    for _ in range(100):
        assert b.try_spend(1.0)
    assert not b.is_exhausted()
    assert b.remaining_invocations() == float("inf")
    assert b.remaining_cost() == float("inf")


def test_budget_remaining() -> None:
    b = RunBudget(max_invocations=5, max_cost=10.0)
    b.try_spend(3.0)
    assert b.remaining_invocations() == 4
    assert b.remaining_cost() == 7.0


# ── effort tiers ────────────────────────────────────────────────────────────


def test_effort_tiers() -> None:
    assert effort_for_stage("validate") == "low"
    assert effort_for_stage("format") == "low"
    assert effort_for_stage("capture") == "high"
    assert effort_for_stage("fix") == "medium"


def test_effort_unknown_defaults_high() -> None:
    assert effort_for_stage("mystery_stage") == "high"
    assert "capture" in DEFAULT_STAGE_EFFORT


# ── run_pipeline_dynamic budget integration ─────────────────────────────────


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


def test_dynamic_budget_halts_runaway(tmp_path: Path) -> None:
    compiled = _compile(tmp_path)
    manifest = Manifest(path=tmp_path / "m.json")
    budget = RunBudget(max_invocations=2)
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": c} for c in "abcd"],
        backend=MockBackend(default="{}"), vault_root=tmp_path / "v",
        budget=budget, manifest=manifest, run_id="r1", max_workers=1,
    )
    kinds = sorted(classify_outcome(r).kind for r in run.step_results)
    assert kinds.count("BUDGET_EXHAUSTED") == 2
    assert kinds.count("SUCCESS") == 2
    # The budget-halted sessions are blocked in the manifest.
    blocked = [e for e in manifest.entries.values() if e.status == "blocked"]
    assert len(blocked) == 2


def test_dynamic_budget_charges_each_retry_backend_call(tmp_path: Path) -> None:
    class _CrashThenSuccessBackend:
        backend_id = "crash-then-success"

        def __init__(self) -> None:
            self.calls = 0

        def call(self, request: LLMRequest) -> LLMResponse:
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("transient disconnect")
            return LLMResponse(
                content="{}",
                elapsed_ms=1.0,
                backend_id=self.backend_id,
            )

    compiled = _compile(tmp_path)
    backend = _CrashThenSuccessBackend()
    budget = RunBudget(max_invocations=1)

    run = run_pipeline_dynamic(
        compiled,
        leaves=[{"id": "a"}],
        backend=backend,
        vault_root=tmp_path / "v",
        budget=budget,
        max_workers=1,
    )

    assert backend.calls == 1
    assert budget.invocations == 1
    assert run.step_results[0].error == "run budget exhausted"
    assert run.step_results[0].attempts == 1


def test_dynamic_no_budget_runs_all(tmp_path: Path) -> None:
    compiled = _compile(tmp_path)
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": c} for c in "abcd"],
        backend=MockBackend(default="{}"), vault_root=tmp_path / "v",
        budget=None,
    )
    assert run.error_count == 0
    assert len(run.step_results) == 4


def test_dynamic_budget_generous_runs_all(tmp_path: Path) -> None:
    compiled = _compile(tmp_path)
    run = run_pipeline_dynamic(
        compiled, leaves=[{"id": c} for c in "abc"],
        backend=MockBackend(default="{}"), vault_root=tmp_path / "v",
        budget=RunBudget(max_invocations=100, max_cost=1000.0),
    )
    assert run.error_count == 0
