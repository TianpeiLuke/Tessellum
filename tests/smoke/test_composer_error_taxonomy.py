"""P18 (FZ 20k9c1a1a1b7c2f) — the canonical error taxonomy the three composer
classifiers project from.

Before P18, ``executor.classify_error``, ``credential_pool.classify_rotation_cause``,
and ``llm._is_auth_error`` hand-mirrored overlapping token lists and DISAGREED —
a bare ``AccessDenied`` was ``crash`` in the executor, ``auth`` in the pool, and
**not-auth** for the P1 credential-refresh, so the refresh never fired on the
exact failure it targets. These tests pin:

  1. ``classify_reason`` maps each canonical reason correctly, with precedence.
  2. The two projection tables + ``is_auth`` reproduce every mapping the three
     consumers previously asserted (no behavioural regression).
  3. THE AGREEMENT INVARIANT: over a shared error-string corpus, the three
     consumers never contradict each other (an ``auth`` string is auth
     everywhere; a rate/quota string benches the key AND is rate_limit in the
     executor class; a validation string touches no key).

Pure functions — no LLM, no I/O, no backend. Safe alongside a live run.
"""

from __future__ import annotations

import pytest

from tessellum.composer.credential_pool import classify_rotation_cause
from tessellum.composer.error_taxonomy import (
    REASON_TO_ERROR_CLASS,
    REASON_TO_ROTATION_CAUSE,
    classify_reason,
    is_auth,
)
from tessellum.composer.executor import classify_error
from tessellum.composer.llm import _is_auth_error


# ── classify_reason — canonical reasons + precedence ─────────────────────────


@pytest.mark.parametrize(
    "msg,expected",
    [
        ("stalled after 120.0s", "stall"),
        ("STALLED AFTER 5s", "stall"),
        ("missing required consumed input: upstream.plan_doc", "missing_consumed"),
        ("truncated at max_tokens after 3 attempts", "truncated"),
        ("response failed schema validation", "validation"),
        ("materializer failed: no such key", "validation"),
        ("contract violation: missing field", "validation"),
        ("response is not valid JSON: Expecting value", "validation"),
        ("HTTP 402 quota exhausted", "quota"),
        ("insufficient_quota", "quota"),
        ("billing hard limit reached", "quota"),
        ("HTTP 429 Too Many Requests", "rate_limit"),
        ("rate limit exceeded", "rate_limit"),
        ("ThrottlingException", "rate_limit"),
        ("401 Unauthorized", "auth"),
        ("403 Forbidden", "auth"),
        ("AccessDeniedException", "auth"),
        ("token expired", "auth"),
        ("invalid credential", "auth"),
        ("RuntimeError: connection reset by peer", "unknown"),
        ("some unexpected explosion", "unknown"),
        ("", "unknown"),
        (None, "unknown"),
    ],
)
def test_classify_reason_maps_each(msg, expected) -> None:
    assert classify_reason(msg) == expected


def test_precedence_stall_beats_status_tokens() -> None:
    assert classify_reason("stalled after 30s (429 upstream)") == "stall"


def test_precedence_truncated_beats_validation() -> None:
    # A truncated payload also fails JSON parse; the size diagnosis wins.
    assert classify_reason("truncated at max_tokens (not valid json)") == "truncated"


def test_precedence_quota_beats_rate_limit() -> None:
    assert classify_reason("429 ... quota exceeded") == "quota"


def test_precedence_validation_beats_auth() -> None:
    # A logic-class message that merely MENTIONS a status token stays validation.
    assert classify_reason("schema validation failed (403 in example)") == "validation"


def test_bare_auth_substring_is_not_auth() -> None:
    # 'non-auth failure' must NOT classify as auth — else the P1 refresh fires on
    # a non-auth error. The bare 'auth' token was deliberately dropped.
    assert classify_reason("ValueError: some non-auth failure") == "unknown"
    assert not is_auth("ValueError: some non-auth failure")


# ── projections reproduce the pre-P18 consumer contracts ─────────────────────


@pytest.mark.parametrize(
    "msg,expected",
    [
        ("stalled after 120.0s", "transient"),
        ("response failed schema validation", "validation"),
        ("materializer failed", "validation"),
        ("contract violation", "validation"),
        ("response is not valid JSON", "validation"),
        ("HTTP 429 Too Many Requests", "rate_limit"),
        ("monthly quota exhausted", "rate_limit"),  # quota folds into rate_limit here
        ("request was throttled", "rate_limit"),
        ("401 Unauthorized", "auth"),
        ("403 Forbidden", "auth"),
        ("authentication token expired, please login again", "auth"),
        ("invalid credential", "auth"),
        ("RuntimeError: connection reset", "crash"),
        ("", "crash"),
        ("truncated at max_tokens", "truncated"),
        ("missing required consumed input: x", "missing_consumed"),
    ],
)
def test_classify_error_projection_matches_legacy(msg, expected) -> None:
    assert classify_error(msg) == expected


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
def test_classify_rotation_cause_projection_matches_legacy(msg, expected) -> None:
    assert classify_rotation_cause(msg) == expected


def test_is_auth_error_matches_legacy_and_fixes_access_denied() -> None:
    # Pre-P18 asserted case (403 + expired security token).
    assert _is_auth_error(
        Exception(
            "PermissionDeniedError: Error code: 403 - "
            "The security token included in the request is expired"
        )
    )
    # THE FIX: a bare AccessDenied is now auth here too (was False → refresh
    # never fired), matching the pool that always benched it as auth.
    assert _is_auth_error(Exception("AccessDeniedException"))
    # Non-auth stays not-auth (don't mask real bugs).
    assert not _is_auth_error(ValueError("some non-auth failure"))


# ── THE agreement invariant — the three classifiers never contradict ─────────

# A shared corpus spanning every reason + the historically-divergent strings.
_SHARED_CORPUS = [
    "AccessDeniedException",                 # the bug that motivated P18
    "AccessDenied: not authorized to call",
    "PermissionDenied: 403",
    "401 Unauthorized",
    "403 Forbidden",
    "The security token included in the request is expired",
    "invalid credential",
    "HTTP 429 Too Many Requests",
    "ThrottlingException: rate exceeded",
    "HTTP 402 quota exhausted",
    "insufficient_quota",
    "response failed schema validation",
    "response is not valid JSON",
    "truncated at max_tokens",
    "missing required consumed input: upstream.plan_doc",
    "stalled after 120s",
    "RuntimeError: connection reset by peer",
    "",
]


@pytest.mark.parametrize("msg", _SHARED_CORPUS)
def test_three_classifiers_agree_on_shared_corpus(msg) -> None:
    """Over the shared corpus the three consumers project the SAME canonical
    reason, so they can never disagree the way they did pre-P18."""
    reason = classify_reason(msg)
    exc = Exception(msg)
    rendered = f"{type(exc).__name__}: {exc}"

    # Each consumer == the table/predicate for that reason (no independent logic).
    assert classify_error(msg) == REASON_TO_ERROR_CLASS[reason]
    assert classify_rotation_cause(msg) == REASON_TO_ROTATION_CAUSE[reason]
    # is_auth over the exception-rendered form agrees with the auth reason of the
    # rendered string (what the executor/pool would also see for a raised exc).
    assert _is_auth_error(exc) == (classify_reason(rendered) == "auth")


@pytest.mark.parametrize("msg", _SHARED_CORPUS)
def test_auth_strings_trigger_refresh_and_auth_bench_together(msg) -> None:
    """The core P18 guarantee: a string is auth for the credential-refresh IFF
    it is auth for the pool cooldown IFF it is the executor's auth class — the
    three auth verdicts move as one."""
    is_auth_class = classify_error(msg) == "auth"
    is_auth_rotation = classify_rotation_cause(msg) == "auth"
    is_auth_refresh = _is_auth_error(Exception(msg))
    assert is_auth_class == is_auth_rotation == is_auth_refresh
