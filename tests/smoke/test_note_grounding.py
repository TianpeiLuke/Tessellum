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
