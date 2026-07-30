"""P8/F6 (FZ 20k9c1a1a1b7c2e) — the runtime grounding gate is re-enablable.

The runtime sliced the per-session close gate to format-only
(``_format_only_gate`` → ``gates[0]``), so the note-level GROUNDING check — the
semantic-fidelity predicate that catches a note unfaithful to its source — was
structurally discarded (the F6 gap: a fabricated note passed the shipped close
gate). P8 wires a policy-gated close-gate selector so a deployment can turn the
grounding check back on; it defaults OFF because the shipped grounding
certificate is fail-closed until calibrated (an uncalibrated certificate
abstains on every note), and ON it correctly fails closed rather than admitting.

Pure — no LLM, no backend. Safe alongside a live run.
"""

from __future__ import annotations

from tessellum.composer.gates import grounding_predicate
from tessellum.runtime.executor import _close_gate_for
from tessellum.runtime.policy import RuntimePolicy


def test_default_policy_is_format_only():
    """W2 (FZ 20k9c1a1a1b7c2k2a4) CHANGED the default: identifier_grounding
    defaults ON, so the grounding rung runs with the free deterministic
    verifier. Format-only remains reachable by turning it off."""
    gate = _close_gate_for(RuntimePolicy())
    assert gate is not None
    assert [g.gate_id for g in gate.gates] == ["format", "grounding", "code_density"]
    off = _close_gate_for(RuntimePolicy(identifier_grounding=False))
    assert [g.gate_id for g in off.gates] == ["format"]


def test_grounding_gate_on_adds_grounding_predicate():
    """grounding_gate=True → the FULL close gate (format + grounding) — the F6
    fix: the grounding check is no longer structurally sliced away."""
    gate = _close_gate_for(RuntimePolicy(grounding_gate=True))
    assert gate is not None
    ids = [g.gate_id for g in gate.gates]
    assert "format" in ids and "grounding" in ids


def test_close_gate_disabled_returns_none():
    assert _close_gate_for(RuntimePolicy(close_gate=False)) is None


def test_grounding_predicate_fails_closed_without_verdict(tmp_path):
    """The safety invariant: with the grounding gate ON but no grounding verdict
    (no verifier injected / no calibrated certificate), the predicate FAILS
    CLOSED — a note is blocked, never silently admitted. This is why the flag
    defaults off until a calibrated certificate exists."""
    note = tmp_path / "n.md"
    note.write_text("body", encoding="utf-8")
    issues = grounding_predicate(note, verdict=None)
    assert issues, "grounding must fail closed when no verdict is available"
