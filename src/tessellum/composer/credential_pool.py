"""Credential pool + run-level budgets.

Composer v4, Phase 5. Two orthogonal spend-control mechanisms:

1. **Credential pool** (:class:`CredentialPool`). A same-provider pool of
   API keys. Where the retry ladder answers *when* to retry,
   the pool answers *which key* to use. It supports ``least_used``
   selection, per-worker leasing under a lock (so parallel waves never
   double-rotate a key), **error-class rotation** (a transient 429 →
   retry the same key once; a hard rate-limit/quota → rotate immediately),
   and **differentiated cooldowns** (a 429-benched key rests 1h; a 402
   quota-exhausted key rests 24h). Cooldowns are expressed as absolute
   "available at" timestamps so they survive a restart when persisted.

2. **Run-level budgets** (:class:`RunBudget`). A global cap on total
   invocations (the runaway-fan-out breaker a static compile gate can't
   catch) and on total token/cost spend. When either is exhausted the
   caller halts with a typed ``BUDGET_EXHAUSTED`` outcome.

No LLM, no network — pure bookkeeping (IDENT-3). Timestamps are passed in
(``now: float``) so the transition logic is deterministic + unit-testable
(mirrors :mod:`tessellum.composer.manifest`).
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Literal

from tessellum.composer.error_taxonomy import (
    REASON_TO_ROTATION_CAUSE,
    classify_reason,
)

# Cooldown lengths, in seconds. A soft 429 benches a key for an hour; a
# hard quota/billing (402) benches it for a day.
COOLDOWN_RATE_LIMIT_SECS: float = 3600.0
COOLDOWN_QUOTA_SECS: float = 86400.0

RotationCause = Literal["transient", "rate_limit", "quota", "auth"]
"""Why a key is being rotated/benched (maps from the retry ladder's
error classes; ``quota`` is the hard 402 variant of ``rate_limit``)."""


def classify_rotation_cause(error_msg: str) -> RotationCause:
    """Classify a backend error message into a key-rotation cause.

    P18 (FZ 20k9c1a1a1b7c2f): thin projection of the canonical
    :func:`~tessellum.composer.error_taxonomy.classify_reason` — the single
    token-heuristic source the executor, this pool, and the llm auth-retry all
    share, so the three no longer disagree. The pool cares only about the three
    key-affecting causes; every non-key reason (stall/validation/truncated/…)
    projects to ``transient`` (keep the key, let the retry ladder retry it).

    Causes and their cooldowns: ``quota`` (hard billing/quota → long bench),
    ``rate_limit`` (soft throttle → brief bench), ``auth`` (bad/expired
    credential → bench, won't recover soon), ``transient`` (keep the key).
    A ``None``/empty message is ``transient`` (a blip, not a key fault).
    """
    return REASON_TO_ROTATION_CAUSE[classify_reason(error_msg)]  # type: ignore[return-value]


class CredentialPoolError(Exception):
    """Raised when no key can be leased (all benched / none configured)."""


@dataclass
class _KeyState:
    """Per-key bookkeeping inside the pool."""

    key_id: str
    use_count: int = 0
    leased_by: str | None = None  # run/worker id holding the lease
    available_at: float = 0.0  # epoch seconds; benched until this time


@dataclass
class CredentialPool:
    """A lockable, cooldown-aware pool of same-provider API keys.

    Not frozen — this is live mutable state that parallel workers lease
    from under ``_lock``. Construct with the *key ids* (never the secrets
    themselves — the caller maps id → secret out of band, so this module
    never holds a credential).
    """

    key_ids: tuple[str, ...] = ()
    _states: dict[str, _KeyState] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def __post_init__(self) -> None:
        for kid in self.key_ids:
            self._states.setdefault(kid, _KeyState(key_id=kid))

    # ── Leasing ──────────────────────────────────────────────────────────

    def lease(self, worker_id: str, now: float) -> str:
        """Lease the least-used, available, unleased key to ``worker_id``.

        Selection: among keys that are **not leased** and **past their
        cooldown** (``available_at <= now``), pick the one with the lowest
        ``use_count`` (ties broken by key-id order for determinism).
        Increments its ``use_count`` and marks it leased. This is the
        single choke point that stops two workers from both driving the
        same key (which would double its effective rate and trip a shared
        429 wall).

        Raises:
            CredentialPoolError: If no key is currently available.
        """
        with self._lock:
            candidates = [
                s
                for s in self._states.values()
                if s.leased_by is None and s.available_at <= now
            ]
            if not candidates:
                raise CredentialPoolError(
                    "no credential available (all leased or in cooldown)"
                )
            chosen = min(candidates, key=lambda s: (s.use_count, s.key_id))
            chosen.leased_by = worker_id
            chosen.use_count += 1
            return chosen.key_id

    def release(self, key_id: str, worker_id: str) -> bool:
        """Release a lease held by ``worker_id``. Returns ``False`` if the
        lease wasn't held by that worker (a no-op guard)."""
        with self._lock:
            st = self._states.get(key_id)
            if st is None or st.leased_by != worker_id:
                return False
            st.leased_by = None
            return True

    # ── Error-class rotation + cooldowns ─────────────────────────────────

    def report_failure(
        self, key_id: str, worker_id: str, cause: RotationCause, now: float
    ) -> bool:
        """Record a failure against a leased key; bench + release on a hard one.

        - ``transient`` — a soft/first 429: the key is **not** benched
          (the retry ladder retries it once); the lease is kept so the
          same worker can retry the same key.
        - ``rate_limit`` — a persistent rate-limit: bench the key for
          :data:`COOLDOWN_RATE_LIMIT_SECS` and release the lease so the
          worker rotates to another key.
        - ``quota`` — a hard 402/billing exhaustion: bench for
          :data:`COOLDOWN_QUOTA_SECS` (much longer) and release.
        - ``auth`` — a bad/expired key: bench for the quota duration (it
          won't recover soon) and release.

        Returns:
            ``True`` iff the key was benched (and thus the lease released);
            ``False`` for the ``transient`` keep-the-lease case.
        """
        with self._lock:
            st = self._states.get(key_id)
            if st is None or st.leased_by != worker_id:
                return False
            if cause == "transient":
                return False  # keep the lease; retry ladder handles it
            if cause == "rate_limit":
                st.available_at = now + COOLDOWN_RATE_LIMIT_SECS
            else:  # quota / auth — long bench
                st.available_at = now + COOLDOWN_QUOTA_SECS
            st.leased_by = None
            return True

    def available_count(self, now: float) -> int:
        """How many keys are usable right now (not leased, past cooldown)."""
        with self._lock:
            return sum(
                1
                for s in self._states.values()
                if s.leased_by is None and s.available_at <= now
            )

    # ── Persistence (survives a restart) ─────────────────────────────────

    def to_cooldowns(self) -> dict[str, float]:
        """Export ``{key_id: available_at}`` for keys still in cooldown.

        Persist this (e.g. in the manifest) so a benched key stays benched
        across a restart — a key 402'd 10 minutes ago shouldn't be retried
        the instant the process comes back.
        """
        with self._lock:
            return {
                kid: s.available_at
                for kid, s in self._states.items()
                if s.available_at > 0.0
            }

    def load_cooldowns(self, cooldowns: dict[str, float]) -> None:
        """Restore ``available_at`` timestamps from :meth:`to_cooldowns`."""
        with self._lock:
            for kid, avail in cooldowns.items():
                st = self._states.get(kid)
                if st is not None:
                    st.available_at = avail


# ── Run-level budgets ───────────────────────────────────────────────────────


class BudgetExhausted(Exception):
    """Raised (or signalled) when a run-level budget is exhausted."""


@dataclass
class RunBudget:
    """A global cap on invocations and token/cost spend for one run.

    ``None`` on a limit means unbounded. :meth:`try_spend` is the single
    gate every dispatch passes: it atomically checks + charges, returning
    ``False`` (and charging nothing) when the spend would breach a cap —
    the caller then halts that leaf with a typed ``BUDGET_EXHAUSTED``.
    The invocation cap is the runaway-fan-out breaker a static plan gate
    can't catch (a pathological ``plan_doc`` that explodes at runtime).
    """

    max_invocations: int | None = None
    max_cost: float | None = None
    _invocations: int = 0
    _cost: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def invocations(self) -> int:
        return self._invocations

    @property
    def cost(self) -> float:
        return self._cost

    def try_spend(self, cost: float = 0.0) -> bool:
        """Atomically charge one invocation + ``cost``; refuse if over cap.

        Returns ``True`` and records the spend when both caps still hold
        *after* the charge; returns ``False`` and records **nothing** when
        the invocation or cost cap would be breached. All-or-nothing so a
        refused dispatch doesn't half-count.
        """
        with self._lock:
            next_inv = self._invocations + 1
            next_cost = self._cost + cost
            if self.max_invocations is not None and next_inv > self.max_invocations:
                return False
            if self.max_cost is not None and next_cost > self.max_cost:
                return False
            self._invocations = next_inv
            self._cost = next_cost
            return True

    def remaining_invocations(self) -> int | float:
        if self.max_invocations is None:
            return float("inf")
        return max(0, self.max_invocations - self._invocations)

    def remaining_cost(self) -> float:
        if self.max_cost is None:
            return float("inf")
        return max(0.0, self.max_cost - self._cost)

    def is_exhausted(self) -> bool:
        """True iff either cap has been reached (no headroom for one more)."""
        if self.max_invocations is not None and self._invocations >= self.max_invocations:
            return True
        if self.max_cost is not None and self._cost >= self.max_cost:
            return True
        return False


# ── Run-level error-class circuit breaker (P17; FZ 20k9c1a1a1b7c2f) ──────────


# The error classes that indicate a SYSTEMIC wall worth aborting the whole wave
# for — an expired key pool or a marketplace-wide throttle makes EVERY leaf fail
# the same way, so retrying more leaves just burns budget against the same wall.
# Keyed on the executor's ``error_class`` vocabulary (P18 unified taxonomy);
# ``quota`` folds into ``rate_limit`` at that layer, so both are covered by
# ``rate_limit``. ``validation``/``truncated``/``crash``/``missing_consumed`` are
# per-leaf logic/size faults, NOT systemic — they must never trip the breaker.
DEFAULT_TRIPPING_CLASSES: frozenset[str] = frozenset({"auth", "rate_limit"})

# Conservative defaults (the operator's call): only abort once a MAJORITY of a
# non-trivial number of dispatched leaves have failed the same systemic way. A
# healthy wave with scattered transient/validation failures never trips.
DEFAULT_BREAKER_MIN_DISPATCHED: int = 3
DEFAULT_BREAKER_PROPORTION: float = 0.8


@dataclass
class ErrorClassBreaker:
    """A run-level circuit breaker that aborts a wave when a *proportional*
    share of its dispatched leaves fail with the same systemic error class.

    Where :class:`RunBudget` caps *how much* a run may spend, this caps *how
    long a run keeps trying against a wall it cannot get past*. It aggregates
    the per-leaf ``error_class`` verdicts (which nothing did before P17): once
    ``min_dispatched`` leaves have run AND at least ``proportion`` of them failed
    with a class in ``tripping_classes`` (default ``{auth, rate_limit}``), it
    latches tripped and the scheduler short-circuits the remaining leaves with a
    typed ``BREAKER_TRIPPED`` outcome — mirroring the ``BUDGET_EXHAUSTED`` seam.

    ``None`` / disabled reproduces today's behaviour exactly (never aborts), so
    the param is safe to default off on every dispatch path (IDENT).

    Args:
        proportion: Trip when ``tripping_failures / dispatched >= proportion``
            (once ``min_dispatched`` is met). ``None`` disables the proportional
            rule (then only ``error_threshold`` can trip).
        error_threshold: Absolute count of tripping-class failures that trips
            regardless of proportion. ``None`` disables the absolute rule.
        min_dispatched: Floor on dispatched leaves before the proportional rule
            can trip — stops a 1-of-1 unlucky failure from aborting a wave.
        tripping_classes: The error classes that count toward tripping.

    A breaker with both ``proportion`` and ``error_threshold`` ``None`` is
    inert (never trips) — the disabled state.
    """

    proportion: float | None = DEFAULT_BREAKER_PROPORTION
    error_threshold: int | None = None
    min_dispatched: int = DEFAULT_BREAKER_MIN_DISPATCHED
    tripping_classes: frozenset[str] = DEFAULT_TRIPPING_CLASSES
    _dispatched: int = 0
    _class_counts: dict[str, int] = field(default_factory=dict)
    _tripped: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def dispatched(self) -> int:
        return self._dispatched

    @property
    def tripping_total(self) -> int:
        """Total failures across all tripping classes seen so far."""
        return sum(self._class_counts.get(c, 0) for c in self.tripping_classes)

    def record(self, error_class: str | None) -> None:
        """Record one completed leaf. ``error_class`` is the leaf's
        :attr:`StepResult.error_class` (``None`` on success). Counts every
        dispatched leaf (successes included) so ``proportion`` is measured
        against the whole wave, not just its failures."""
        with self._lock:
            self._dispatched += 1
            if error_class in self.tripping_classes:
                self._class_counts[error_class] = self._class_counts.get(error_class, 0) + 1

    def should_abort(self) -> bool:
        """True once a systemic wall is confirmed — latches, so a later success
        cannot un-trip a wave already being torn down."""
        with self._lock:
            if self._tripped:
                return True
            if self.proportion is None and self.error_threshold is None:
                return False  # inert / disabled
            tripping = sum(self._class_counts.get(c, 0) for c in self.tripping_classes)
            if self.error_threshold is not None and tripping >= self.error_threshold:
                self._tripped = True
                return True
            if (
                self.proportion is not None
                and self._dispatched >= self.min_dispatched
                and tripping / self._dispatched >= self.proportion
            ):
                self._tripped = True
                return True
            return False

    def with_tripping_classes(self, classes: frozenset[str]) -> "ErrorClassBreaker":
        """Return a FRESH breaker with the same threshold config but a different
        set of tripping classes (fresh counts + fresh lock — no shared mutable
        state with ``self``). Used to apply an execute skill's declared
        ``fallback_strategy`` posture at wave start (P17): a ``degrade`` posture
        narrows the set to ``{auth}`` so a soft throttle is tolerated while a
        hard credential wall still aborts."""
        return ErrorClassBreaker(
            proportion=self.proportion,
            error_threshold=self.error_threshold,
            min_dispatched=self.min_dispatched,
            tripping_classes=classes,
        )

    def dominant_class(self) -> str | None:
        """The tripping class with the most failures (ties broken by sorted
        order for determinism); ``None`` if no tripping failure seen."""
        with self._lock:
            counts = {
                c: n for c, n in self._class_counts.items()
                if c in self.tripping_classes and n > 0
            }
        if not counts:
            return None
        return max(sorted(counts), key=lambda c: counts[c])

    def terminal_cause(self) -> str:
        """An actionable terminal-cause message. Contains the substring
        ``"circuit breaker"`` — the marker ``classify_outcome`` matches on to
        map it to the ``BREAKER_TRIPPED`` outcome kind (mirrors the
        ``"run budget exhausted"`` convention)."""
        dom = self.dominant_class() or "systemic"
        with self._lock:
            tripping = sum(self._class_counts.get(c, 0) for c in self.tripping_classes)
            dispatched = self._dispatched
        return (
            f"error-class circuit breaker tripped: {tripping}/{dispatched} dispatched "
            f"leaves failed with a systemic class (dominant: {dom}). Aborting the wave "
            f"instead of burning budget against the same wall — check credentials / "
            f"rate limits and re-run."
        )


# ── Per-stage effort ────────────────────────────────────────────────────────


EffortLevel = Literal["low", "medium", "high"]
"""Per-stage model/effort tier (cheap model for validate/format, high for
enrich/capture, medium for fix) — the caller maps this onto a concrete
model + reasoning budget."""

# Sensible defaults per stage kind; a deployment overrides as needed.
DEFAULT_STAGE_EFFORT: dict[str, EffortLevel] = {
    "validate": "low",
    "format": "low",
    "capture": "high",
    "enrich": "high",
    "fix": "medium",
}


def effort_for_stage(stage: str) -> EffortLevel:
    """Return the default :data:`EffortLevel` for a stage kind (``high`` if
    unknown — an unrecognized stage errs toward capability, not thrift)."""
    return DEFAULT_STAGE_EFFORT.get(stage, "high")


__all__ = [
    "COOLDOWN_RATE_LIMIT_SECS",
    "COOLDOWN_QUOTA_SECS",
    "RotationCause",
    "classify_rotation_cause",
    "CredentialPoolError",
    "CredentialPool",
    "BudgetExhausted",
    "RunBudget",
    "ErrorClassBreaker",
    "DEFAULT_TRIPPING_CLASSES",
    "DEFAULT_BREAKER_MIN_DISPATCHED",
    "DEFAULT_BREAKER_PROPORTION",
    "EffortLevel",
    "DEFAULT_STAGE_EFFORT",
    "effort_for_stage",
]
