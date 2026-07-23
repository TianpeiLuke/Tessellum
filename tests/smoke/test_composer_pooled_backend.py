"""PooledBackend + classify_rotation_cause — the credential pool wired into
the LLM dispatch layer (the *which-key* dimension).

Covers: cause classification; lease-per-call + key tagging; rotate-and-bench
on a hard cause (rate_limit/quota/auth) then re-raise for the retry ladder;
transient keep-the-lease; multi-key exhaustion; composition with
execute_step_with_retry (a 429'd key benches, the retry lands on a fresh
key and succeeds).

No network — a scripted fake inner backend drives every branch.
"""

from __future__ import annotations

import pytest

from tessellum.composer import (
    CredentialPool,
    LLMRequest,
    LLMResponse,
    PooledBackend,
    classify_rotation_cause,
)
from tessellum.composer.credential_pool import (
    COOLDOWN_QUOTA_SECS,
    COOLDOWN_RATE_LIMIT_SECS,
    CredentialPoolError,
)


# ── classify_rotation_cause ─────────────────────────────────────────────────


@pytest.mark.parametrize(
    "msg,expected",
    [
        ("Error 429: rate limit exceeded", "rate_limit"),
        ("too many requests", "rate_limit"),
        ("ThrottlingException", "rate_limit"),
        ("HTTP 402 quota exhausted", "quota"),
        ("insufficient_quota", "quota"),
        ("billing hard limit reached", "quota"),
        ("401 Unauthorized", "auth"),
        ("403 Forbidden", "auth"),
        ("AccessDeniedException", "auth"),
        ("token expired", "auth"),
        ("some random blip", "transient"),
        ("", "transient"),
    ],
)
def test_classify_rotation_cause(msg, expected) -> None:
    assert classify_rotation_cause(msg) == expected


def test_classify_precedence_quota_before_rate_limit() -> None:
    # A message with both "429" and "quota" → quota wins (the harder cause).
    assert classify_rotation_cause("429 ... quota exceeded") == "quota"


# ── A scripted fake inner backend ───────────────────────────────────────────


class _FakeInner:
    backend_id = "fake"

    def __init__(self, fail_keys: dict[str, str] | None = None) -> None:
        # {key_id: error_message} → raise that error when that key is applied.
        self.fail_keys = fail_keys or {}
        self.key: str | None = None
        self.applied: list[str] = []

    def call(self, request: LLMRequest) -> LLMResponse:
        self.applied.append(self.key or "")
        if self.key in self.fail_keys:
            raise RuntimeError(self.fail_keys[self.key])
        return LLMResponse(content='{"ok": true}', elapsed_ms=1.0, backend_id="fake")


def _clock():
    t = {"v": 0.0}

    def now() -> float:
        return t["v"]

    return now, t


def _apply(inner, key_id):
    inner.key = key_id


# ── PooledBackend ───────────────────────────────────────────────────────────


def test_pooled_backend_id() -> None:
    b = PooledBackend(_FakeInner(), CredentialPool(key_ids=("k1",)), _apply)
    assert b.backend_id == "pooled:fake"


def test_pooled_tags_credential_key_on_success() -> None:
    now, _ = _clock()
    inner = _FakeInner()
    b = PooledBackend(inner, CredentialPool(key_ids=("k1",)), _apply, clock=now)
    resp = b.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert resp.metadata["credential_key"] == "k1"
    assert resp.backend_id == "pooled:fake"
    assert inner.applied == ["k1"]


def test_pooled_releases_key_on_success() -> None:
    now, _ = _clock()
    pool = CredentialPool(key_ids=("k1",))
    b = PooledBackend(_FakeInner(), pool, _apply, clock=now)
    b.call(LLMRequest(system_prompt="s", user_prompt="u"))
    # Released → still leasable (would raise if it stayed leased on 1-key pool).
    assert pool.available_count(now()) == 1


def test_pooled_rate_limit_benches_and_rotates() -> None:
    now, t = _clock()
    inner = _FakeInner(fail_keys={"k1": "429 rate limit"})
    pool = CredentialPool(key_ids=("k1", "k2"))
    b = PooledBackend(inner, pool, _apply, worker_id="w1", clock=now)

    # Call 1 leases k1 (id order, use_count 0) → 429 → benched + re-raised.
    with pytest.raises(RuntimeError, match="429"):
        b.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert inner.applied[-1] == "k1"
    # k1 benched for the rate-limit cooldown; only k2 is available now.
    assert pool.available_count(now()) == 1
    assert pool.available_count(now() + COOLDOWN_RATE_LIMIT_SECS + 1) == 2

    # Call 2 leases k2 (k1 benched) → success.
    resp = b.call(LLMRequest(system_prompt="s", user_prompt="u"))
    assert inner.applied[-1] == "k2"
    assert resp.metadata["credential_key"] == "k2"


def test_pooled_quota_benches_long() -> None:
    now, _ = _clock()
    inner = _FakeInner(fail_keys={"k1": "402 insufficient_quota"})
    pool = CredentialPool(key_ids=("k1", "k2"))
    b = PooledBackend(inner, pool, _apply, clock=now)
    with pytest.raises(RuntimeError):
        b.call(LLMRequest(system_prompt="s", user_prompt="u"))
    # Quota cooldown is the long one — still benched after the rate-limit window.
    assert pool.available_count(now() + COOLDOWN_RATE_LIMIT_SECS + 1) == 1
    assert pool.available_count(now() + COOLDOWN_QUOTA_SECS + 1) == 2


def test_pooled_transient_keeps_key_available() -> None:
    now, _ = _clock()
    inner = _FakeInner(fail_keys={"k1": "some transient blip"})
    pool = CredentialPool(key_ids=("k1",))
    b = PooledBackend(inner, pool, _apply, clock=now)
    with pytest.raises(RuntimeError):
        b.call(LLMRequest(system_prompt="s", user_prompt="u"))
    # Transient → NOT benched, lease released → still available for retry.
    assert pool.available_count(now()) == 1


def test_pooled_all_keys_benched_raises_pool_error() -> None:
    now, _ = _clock()
    inner = _FakeInner(fail_keys={"k1": "429", "k2": "429"})
    pool = CredentialPool(key_ids=("k1", "k2"))
    b = PooledBackend(inner, pool, _apply, clock=now)
    # Bench both keys.
    for _ in range(2):
        with pytest.raises(RuntimeError):
            b.call(LLMRequest(system_prompt="s", user_prompt="u"))
    # Now every key is in cooldown → the next lease fails closed.
    with pytest.raises(CredentialPoolError):
        b.call(LLMRequest(system_prompt="s", user_prompt="u"))


def test_pooled_composes_with_retry_ladder() -> None:
    """The whole point: a 429'd key benches, and the executor's crash-retry
    re-dispatches through the pool onto a FRESH key that succeeds."""
    from tessellum.composer.executor import execute_step_with_retry

    # Build a minimal compiled step via the compiler (real, not faked).
    import textwrap
    import tempfile
    from pathlib import Path
    from tessellum.composer import compile_skill

    canon = textwrap.dedent(
        """\
        ---
        tags: [resource, skill]
        keywords: [alpha, beta, gamma]
        topics: [X]
        language: markdown
        date of note: 2026-05-10
        status: active
        building_block: procedure
        ---

        # S

        ## Step 1: go <!-- :: section_id = step_1 :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        ```

        Go.
        """
    )
    with tempfile.TemporaryDirectory() as d:
        tp = Path(d)
        (tp / "s.md").write_text(canon)
        compiled = compile_skill(tp / "s.md")

        now, _ = _clock()
        inner = _FakeInner(fail_keys={"k1": "429 rate limit"})
        pool = CredentialPool(key_ids=("k1", "k2"))
        pooled = PooledBackend(inner, pool, _apply, worker_id="w1", clock=now)

        # The retry ladder sees the k1 429 as a crash, recovers, and the
        # second attempt leases k2 (k1 benched) → clean success.
        result = execute_step_with_retry(
            compiled.steps[0],
            leaf={"_id": "corpus"},
            upstream={},
            backend=pooled,
            vault_root=tp / "v",
            max_crash_recoveries=2,
        )
        assert result.error is None
        assert result.attempts == 2  # first attempt (k1) failed, second (k2) won
        assert result.response.metadata["credential_key"] == "k2"
