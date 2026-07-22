"""Composer v4, Phase 6 — context assembler + sign-off approver.

Covers:
  - ContextAssembler contract test (both concrete assemblers obey the
    same assemble/bounds contract — the swap guard); fail-soft on
    oversize / non-string / strategy crash; windowed head+tail; preflight
    estimate; get_assembler registry.
  - read-path hardening: sensitive denylist, workspace confinement,
    binary sniff.
  - run_sign_off ladder: program reject; agent-disabled approve; confident
    agent approve/reject; escalate on low confidence / high blast; human
    approve/reject; needs_human when human rung unavailable.

All pure/local-I-O; no network, no LLM.
"""

from __future__ import annotations

import pytest

from pathlib import Path

from tessellum.composer import (
    AgentVerdict,
    AssembledContext,
    ContextAssembler,
    FullSourceAssembler,
    SignOffPolicy,
    WindowedAssembler,
    get_assembler,
    is_safe_read_path,
    run_sign_off,
)
from tessellum.composer.context_assembler import (
    DEFAULT_MAX_CONTEXT_CHARS,
    SOFT_WARN_FRACTION,
)


# ── ContextAssembler contract test (the swap guard) ─────────────────────────


ALL_ASSEMBLERS = [FullSourceAssembler, WindowedAssembler]


@pytest.mark.parametrize("cls", ALL_ASSEMBLERS)
def test_assembler_contract_small_source_untouched(cls) -> None:
    a = cls(max_chars=1000)
    out = a.assemble("a small source")
    assert isinstance(out, AssembledContext)
    assert out.text == "a small source"
    assert not out.truncated
    assert out.warnings == ()


@pytest.mark.parametrize("cls", ALL_ASSEMBLERS)
def test_assembler_contract_bounds_oversize(cls) -> None:
    # The universal contract every assembler obeys: an oversized source
    # yields output within the cap AND a fail-soft warning. Whether the
    # base bounder *truncates* (FullSource) or the strategy *shapes it to
    # fit* (Windowed → near-cap warning, no hard truncation) is
    # strategy-specific — the swap guard only pins the shared invariant.
    a = cls(max_chars=50)
    out = a.assemble("x" * 500)
    assert len(out.text) <= 50
    assert out.warnings  # some fail-soft signal was recorded


@pytest.mark.parametrize("cls", ALL_ASSEMBLERS)
def test_assembler_contract_non_string_degrades(cls) -> None:
    a = cls(max_chars=50)
    out = a.assemble(None)  # type: ignore[arg-type]
    assert out.text == ""
    assert out.warnings
    # Never raises — fail-soft.


@pytest.mark.parametrize("cls", ALL_ASSEMBLERS)
def test_assembler_contract_has_strategy_id(cls) -> None:
    a = cls(max_chars=50)
    assert isinstance(a.strategy, str) and a.strategy


def test_assembler_rejects_nonpositive_cap() -> None:
    with pytest.raises(ValueError):
        FullSourceAssembler(max_chars=0)


def test_assembler_soft_warn_near_cap() -> None:
    cap = 100
    a = FullSourceAssembler(max_chars=cap)
    out = a.assemble("x" * int(cap * SOFT_WARN_FRACTION + 1))
    assert not out.truncated
    assert out.warnings  # near-cap soft warning
    assert "near" in out.warnings[0]


def test_assembler_strategy_crash_degrades() -> None:
    class Boom(ContextAssembler):
        @property
        def strategy(self) -> str:
            return "boom"

        def _assemble_raw(self, source: str) -> str:
            raise RuntimeError("kaboom")

    out = Boom(max_chars=100).assemble("anything")
    assert out.text == ""
    assert out.warnings and "failed" in out.warnings[0]


def test_full_source_passes_through() -> None:
    a = FullSourceAssembler(max_chars=1000)
    assert a.assemble("hello world").text == "hello world"


def test_full_source_truncates_oversize() -> None:
    a = FullSourceAssembler(max_chars=50)
    out = a.assemble("x" * 500)
    assert out.truncated
    assert len(out.text) == 50
    assert out.original_chars == 500


def test_windowed_keeps_head_and_tail() -> None:
    w = WindowedAssembler(max_chars=40, head_fraction=0.5)
    out = w.assemble("H" * 100 + "T" * 100)
    assert "[... middle elided ...]" in out.text
    assert out.text.startswith("H")
    assert out.text.endswith("T")
    assert len(out.text) <= 40 + len("\n\n[... middle elided ...]\n\n")


def test_windowed_small_source_no_marker() -> None:
    w = WindowedAssembler(max_chars=1000)
    out = w.assemble("small")
    assert "elided" not in out.text


def test_windowed_rejects_bad_head_fraction() -> None:
    with pytest.raises(ValueError):
        WindowedAssembler(head_fraction=1.5)


def test_estimate_chars_default_is_length() -> None:
    a = FullSourceAssembler()
    assert a.estimate_chars("abcde") == 5


def test_get_assembler_registry() -> None:
    assert isinstance(get_assembler("full_source"), FullSourceAssembler)
    assert isinstance(get_assembler("windowed"), WindowedAssembler)
    assert get_assembler().max_chars == DEFAULT_MAX_CONTEXT_CHARS


def test_get_assembler_unknown_raises() -> None:
    with pytest.raises(KeyError):
        get_assembler("nonexistent_strategy")


# ── read-path hardening ─────────────────────────────────────────────────────


def test_read_path_allows_safe_text(tmp_path: Path) -> None:
    p = tmp_path / "note.md"
    p.write_text("body")
    assert is_safe_read_path(p, workspace_root=tmp_path)


def test_read_path_denies_sensitive_name(tmp_path: Path) -> None:
    p = tmp_path / ".env"
    p.write_text("SECRET=1")
    assert not is_safe_read_path(p, workspace_root=tmp_path)


def test_read_path_denies_sensitive_dir(tmp_path: Path) -> None:
    assert not is_safe_read_path(
        tmp_path / ".aws" / "credentials", workspace_root=tmp_path
    )


def test_read_path_denies_workspace_escape(tmp_path: Path) -> None:
    assert not is_safe_read_path(Path("/etc/hosts"), workspace_root=tmp_path)


def test_read_path_denies_binary(tmp_path: Path) -> None:
    p = tmp_path / "blob.dat"
    p.write_bytes(b"\x00\x01\x02\x03")
    assert not is_safe_read_path(p, workspace_root=tmp_path)


def test_read_path_absent_but_confined_is_ok(tmp_path: Path) -> None:
    # A not-yet-created target under the workspace is fine (a write target).
    assert is_safe_read_path(tmp_path / "future.md", workspace_root=tmp_path)


# ── sign-off ladder ─────────────────────────────────────────────────────────


def _pass_gate():
    return (True, None)


def _fail_gate():
    return (False, "structural defect")


def test_signoff_program_reject_short_circuits() -> None:
    calls = []
    res = run_sign_off(
        program_gate=_fail_gate,
        policy=SignOffPolicy(),
        agent_judge=lambda: (calls.append("a"), AgentVerdict(True, 1.0))[1],
    )
    assert res.decision == "rejected"
    assert res.deciding_rung == "program"
    assert calls == []  # agent never consulted


def test_signoff_agent_disabled_program_pass_approves() -> None:
    res = run_sign_off(program_gate=_pass_gate, policy=SignOffPolicy(use_agent=False))
    assert res.decision == "approved"
    assert res.deciding_rung == "program"


def test_signoff_confident_agent_approve() -> None:
    res = run_sign_off(
        program_gate=_pass_gate,
        policy=SignOffPolicy(min_agent_confidence=0.7, blast_radius_threshold=50),
        agent_judge=lambda: AgentVerdict(True, 0.9, "looks sound"),
        blast_radius=5,
    )
    assert res.decision == "approved"
    assert res.deciding_rung == "agent"
    assert res.escalated == ("agent",)


def test_signoff_confident_agent_reject() -> None:
    res = run_sign_off(
        program_gate=_pass_gate,
        policy=SignOffPolicy(),
        agent_judge=lambda: AgentVerdict(False, 0.9, "coverage gap"),
    )
    assert res.decision == "rejected"
    assert res.deciding_rung == "agent"


def test_signoff_low_confidence_escalates_to_human_approve() -> None:
    res = run_sign_off(
        program_gate=_pass_gate,
        policy=SignOffPolicy(use_human=True, min_agent_confidence=0.7),
        agent_judge=lambda: AgentVerdict(True, 0.3),
        human_prompt=lambda: True,
    )
    assert res.decision == "approved"
    assert res.deciding_rung == "human"
    assert res.escalated == ("agent", "human")


def test_signoff_low_confidence_human_rejects() -> None:
    res = run_sign_off(
        program_gate=_pass_gate,
        policy=SignOffPolicy(use_human=True),
        agent_judge=lambda: AgentVerdict(True, 0.2),
        human_prompt=lambda: False,
    )
    assert res.decision == "rejected"
    assert res.deciding_rung == "human"


def test_signoff_high_blast_escalates() -> None:
    res = run_sign_off(
        program_gate=_pass_gate,
        policy=SignOffPolicy(use_human=True, blast_radius_threshold=10),
        agent_judge=lambda: AgentVerdict(True, 0.99),  # confident, but big change
        human_prompt=lambda: True,
        blast_radius=100,
    )
    assert res.decision == "approved"
    assert res.deciding_rung == "human"


def test_signoff_needs_human_when_human_rung_unavailable() -> None:
    res = run_sign_off(
        program_gate=_pass_gate,
        policy=SignOffPolicy(use_human=False, min_agent_confidence=0.7),
        agent_judge=lambda: AgentVerdict(True, 0.3),  # low confidence, no human
    )
    assert res.decision == "needs_human"
    assert res.deciding_rung == "agent"
