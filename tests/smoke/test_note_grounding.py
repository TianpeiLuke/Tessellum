"""Phase 2 (FZ 20k9c1a1a1b7c2k2a3a) — note-level fabrication defense."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from tessellum.composer import MockBackend
from tessellum.composer.note_grounding import (
    extract_note_identifiers,
    identifier_violations,
    make_grounded_verifier,
)
from tessellum.composer.semantic_certificate import ConformalThresholds

_THRESHOLDS = ConformalThresholds(
    thresholds={"grounding": 0.85}, alpha=0.05,
    n_calibration=40, domains=("documentation",),
)


def test_identifier_extraction_is_code_span_scoped() -> None:
    text = (
        "Run `mcp add --scope project` and set `MAX_MCP_OUTPUT_TOKENS`.\n"
        "Prose mentioning API and configuration.value words is NOT extracted.\n"
        "But `server.transport.stdio` inside backticks is.\n"
    )
    idents = extract_note_identifiers(text)
    assert "--scope" in idents
    assert "MAX_MCP_OUTPUT_TOKENS" in idents
    assert "server.transport.stdio" in idents
    assert "API" not in idents  # prose caps word, outside backticks


def test_identifier_violations_flag_only_absent_tokens() -> None:
    source = "docs: use --scope with MAX_MCP_OUTPUT_TOKENS."
    note = "Set `--scope` and `MAX_MCP_OUTPUT_TOKENS`; also `--made-up-flag`."
    assert identifier_violations(note, source) == ["--made-up-flag"]
    assert identifier_violations(note, "") == []  # no source → not checkable here


def _result_for(note_path: Path) -> SimpleNamespace:
    return SimpleNamespace(
        materialized=SimpleNamespace(
            files_written=(note_path,), files_applied=(), structured={},
        )
    )


def test_verifier_layer1_blocks_without_spending_the_scorer(tmp_path: Path) -> None:
    """An invented identifier returns ungrounded BEFORE any scorer call."""
    note = tmp_path / "n.md"
    note.write_text("Claims `--invented-flag` exists.", encoding="utf-8")
    backend = MockBackend()
    verifier = make_grounded_verifier(
        backend, _THRESHOLDS, "source text without that flag",
    )
    verdict = verifier(None, {"_id": "x", "source_ref": ["src"]}, _result_for(note))
    assert verdict.status == "ungrounded"
    assert "--invented-flag" in (verdict.detail or "")
    assert backend.calls == []  # deterministic layer spent nothing


def test_verifier_layer2_reaches_the_certificate(tmp_path: Path) -> None:
    """A clean note falls through to the calibrated certificate (which, with
    an entailment-affirming mock scorer, ACCEPTS → grounded)."""
    note = tmp_path / "n.md"
    note.write_text(
        "The server supports project scope configuration for tools.",
        encoding="utf-8",
    )
    backend = MockBackend(default='{"entailment": 0.95, "abstain": false}')
    verifier = make_grounded_verifier(
        backend, _THRESHOLDS,
        "The server supports project scope configuration for tools.",
    )
    verdict = verifier(None, {"_id": "x", "source_ref": ["src"]}, _result_for(note))
    assert backend.calls  # the scorer ran
    assert verdict.status == "grounded"


def test_placeholders_and_universal_tokens_are_not_violations() -> None:
    """Precision tuning from the first offline audit: writer-invented
    placeholders and universal tokens are legitimate; invented API surface
    stays flagged."""
    note = (
        "Set `YOUR_ASANA_TOKEN` in `PATH`; run `--help`.\n"
        "Then use `--memory` and `agents.defaults.memory.lancedb`.\n"
    )
    v = identifier_violations(note, "source with no identifiers at all")
    assert v == ["--memory", "agents.defaults.memory.lancedb"]


# ── W2 (FZ 20k9c1a1a1b7c2k2a4): the free two-tier identifier verifier ───────


class _Written:
    def __init__(self, path):
        self.materialized = type("M", (), {"files_written": (path,), "files_applied": ()})()


def _note(tmp_path, text):
    p = tmp_path / "n.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_identifier_verifier_blocks_invented_tokens(tmp_path):
    from tessellum.composer.note_grounding import make_identifier_verifier

    v = make_identifier_verifier("run `tool --real-flag` here")
    note = _note(tmp_path, "use `tool --invented-flag`")
    verdict = v(None, {}, _Written(note))
    assert verdict.status == "ungrounded" and "--invented-flag" in verdict.detail


def test_identifier_verifier_advisory_on_cross_slice(tmp_path):
    from tessellum.composer.note_grounding import make_identifier_verifier

    source = "# A\n\nuse `--alpha-flag`\n\n# B\n\nuse `--beta-flag`\n"
    v = make_identifier_verifier(source)
    note = _note(tmp_path, "use `--beta-flag`")
    leaf = {"owned_source_slice": "# A\n\nuse `--alpha-flag`\n"}
    verdict = v(None, leaf, _Written(note))
    assert verdict.status == "grounded"
    assert "--beta-flag" in (verdict.advisory or "")  # advisory, not a block


def test_identifier_verifier_clean_in_owned_slice(tmp_path):
    from tessellum.composer.note_grounding import make_identifier_verifier

    source = "# A\n\nuse `--alpha-flag`\n"
    v = make_identifier_verifier(source)
    note = _note(tmp_path, "use `--alpha-flag`")
    verdict = v(None, {"owned_source_slice": source}, _Written(note))
    assert verdict.status == "grounded" and not verdict.advisory


def test_grounding_predicate_advisory_is_warning_not_block(tmp_path):
    from tessellum.composer.gates import GroundingVerdict, build_close_gate
    from tessellum.format import Severity

    note = _note(tmp_path, "---\ntags:\n  - x\n---\n\n# N\n\nbody\n")
    suite = build_close_gate()
    composite = suite.evaluate(
        note, verdict=GroundingVerdict("grounded", advisory="cross-contamination: ..."),
        short_circuit=False,
    )
    ground = next(r for r in composite.results if r.gate_id == "grounding")
    assert ground.passed  # WARNING never blocks
    assert any(i.severity is Severity.WARNING and i.rule_id == "GROUND-003"
               for i in ground.issues)


def test_policy_identifier_grounding_default_on_and_gate_selection():
    from tessellum.runtime.executor import _close_gate_for
    from tessellum.runtime.policy import RuntimePolicy

    p = RuntimePolicy()
    assert p.identifier_grounding is True
    gate = _close_gate_for(p)
    assert [g.gate_id for g in gate.gates] == ["format", "grounding"]
    off = RuntimePolicy(identifier_grounding=False)
    assert [g.gate_id for g in _close_gate_for(off).gates] == ["format"]
