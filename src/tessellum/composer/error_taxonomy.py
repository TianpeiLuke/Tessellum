"""Canonical error taxonomy — the single source of truth the three composer
error classifiers project from (P18; FZ 20k9c1a1a1b7c2f design review).

Before this module three classifiers hand-mirrored overlapping token lists and
**disagreed**:

- ``executor.classify_error`` — the diagnostic ``error_class`` on every
  ``StepResult`` (drives the P16 retry ladder's truncation branch).
- ``credential_pool.classify_rotation_cause`` — which cooldown a benched key
  gets.
- ``llm._is_auth_error`` — whether the P1 credential-refresh fires.

A bare ``AccessDenied`` was ``crash`` in the executor, ``auth`` in the pool, and
**not-auth** in ``_is_auth_error`` — so the credential-refresh (which fires ONLY
on ``_is_auth_error``) never triggered on the exact failure it targets, while the
pool correctly benched the key. Now every classifier calls
:func:`classify_reason` once and projects the single canonical :data:`Reason`
into its own vocabulary, so the three **agree by construction**.

Pure, deterministic string heuristic — no LLM, no I/O (IDENT-3). Leaf module:
imports only stdlib, so ``executor`` / ``llm`` / ``credential_pool`` can all
depend on it without an import cycle.
"""

from __future__ import annotations

from typing import Literal

Reason = Literal[
    "stall",
    "missing_consumed",
    "truncated",
    "validation",
    "quota",
    "rate_limit",
    "auth",
    "unknown",
]
"""The finest-grained cause. Every consumer projects this into its own class
via the tables below; this is the ONE list of token heuristics they share."""


def classify_reason(error_msg: str | None) -> Reason:
    """Classify a normalized error message into the canonical :data:`Reason`.

    Precedence, checked against the lower-cased message (highest first):

    1. ``stall`` — the watchdog stall marker (``"stalled after"``).
    2. ``missing_consumed`` — a required ``{{upstream.X}}`` was absent (P23):
       the fix is upstream, not a retry here.
    3. ``truncated`` — response cut at the token cap
       (``"truncated at max_tokens"``); ABOVE ``validation`` because a truncated
       payload also fails JSON parse and the size diagnosis is the actionable one.
    4. ``validation`` — schema / materializer / contract / bad-JSON failures.
    5. ``quota`` — a HARD billing/quota exhaustion (``"402"`` / ``"quota"`` /
       ``"insufficient"`` / ``"billing"``); ABOVE ``rate_limit`` because it is the
       harder cause (long cooldown).
    6. ``rate_limit`` — a soft throttle (``"429"`` / ``"rate limit"`` /
       ``"too many requests"`` / ``"throttl"``).
    7. ``auth`` — a bad/expired credential or permission failure (``"401"`` /
       ``"403"`` / ``"authentication"`` / ``"authoriz"`` (authorization/
       authorized/unauthorized) / ``"login"`` / ``"expired"`` / ``"credential"``
       / ``"forbidden"`` / ``"accessdenied"`` / ``"access denied"`` /
       ``"permissiondenied"`` / ``"permission denied"`` / ``"security token"``).
       NB the **bare** token ``"auth"`` is deliberately NOT used — it matches the
       substring in ``"non-auth failure"``, which must stay ``unknown`` so the P1
       credential-refresh does not fire on a non-auth error.
    8. ``unknown`` — anything else (backend raised / unclassified); also the
       fail-closed result for a ``None``/empty message (IDENT-5).

    ``validation`` deliberately outranks ``auth``/``rate_limit``/``quota`` so a
    logic-class message that merely *mentions* a status token is still diagnosed
    as the logic defect it is; backend exceptions (all the pool ever sees) don't
    contain the validation tokens, so their ordering is unaffected.
    """
    if not error_msg:
        return "unknown"
    msg = error_msg.lower()

    if "stalled after" in msg:
        return "stall"
    if "missing required consumed input" in msg:
        return "missing_consumed"
    if "truncated at max_tokens" in msg:
        return "truncated"
    if (
        "schema" in msg
        or "materializer" in msg
        or "contract" in msg
        or "not valid json" in msg
    ):
        return "validation"
    if "402" in msg or "quota" in msg or "insufficient" in msg or "billing" in msg:
        return "quota"
    if (
        "429" in msg
        or "rate limit" in msg
        or "ratelimit" in msg
        or "too many requests" in msg
        or "throttl" in msg
    ):
        return "rate_limit"
    if (
        "401" in msg
        or "403" in msg
        or "authentication" in msg
        or "authoriz" in msg  # authorization / authorized / unauthorized
        or "login" in msg
        or "expired" in msg
        or "credential" in msg
        or "forbidden" in msg
        or "accessdenied" in msg
        or "access denied" in msg
        or "permissiondenied" in msg
        or "permission denied" in msg
        or "security token" in msg
    ):
        return "auth"
    return "unknown"


# ── Projections — each consumer's vocabulary, keyed on the canonical Reason ───

# executor.classify_error → ErrorClass. ``quota`` folds into ``rate_limit`` (the
# executor's diagnostic tag doesn't distinguish billing from throttling); the
# unclassified ``unknown`` is the executor's ``crash``.
REASON_TO_ERROR_CLASS: dict[Reason, str] = {
    "stall": "transient",
    "missing_consumed": "missing_consumed",
    "truncated": "truncated",
    "validation": "validation",
    "quota": "rate_limit",
    "rate_limit": "rate_limit",
    "auth": "auth",
    "unknown": "crash",
}

# credential_pool.classify_rotation_cause → RotationCause. Only the three
# key-affecting causes are distinct; everything else keeps the key (``transient``).
REASON_TO_ROTATION_CAUSE: dict[Reason, str] = {
    "stall": "transient",
    "missing_consumed": "transient",
    "truncated": "transient",
    "validation": "transient",
    "quota": "quota",
    "rate_limit": "rate_limit",
    "auth": "auth",
    "unknown": "transient",
}


def is_auth(error_msg: str | None) -> bool:
    """True iff the message is the ``auth`` reason — the single predicate the P1
    credential-refresh and the pool's auth cooldown both key on."""
    return classify_reason(error_msg) == "auth"
