"""``tessellum composer digest`` — the context CHARACTER budget is a sweepable knob.

Why this file exists: on a benchmark vault built by this digestion pipeline the
context budget moved chain completeness by more than an order of magnitude
beyond what any retrieval strategy moved it. A lever that large must be a
named, documented parameter reachable from where a run is configured. These
tests pin two things about the ``digest`` CLI surface:

1. **The default is unchanged.** With neither ``--context-strategy`` nor
   ``--context-max-chars`` the CLI passes NO assembler, and the driver's own
   fallback is the named ``DEFAULT_DIGESTION_CONTEXT_MAX_CHARS`` (still
   ``HARD_PROMPT_CAP_CHARS - 4096`` — a byte-identical replacement for the
   arithmetic expression that used to be inlined at each fallback site).
2. **The parameter takes effect.** ``--context-max-chars N`` alone yields a
   ``windowed`` assembler at ``N``; adding ``--context-strategy full_source``
   selects the other strategy at the same budget.

The driver is spied, not run: the budget's only observable at this seam is the
assembler object handed to ``run_digestion_pipeline``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import tessellum.cli.composer as cli_composer
from tessellum.cli.main import main
from tessellum.composer.compiler import HARD_PROMPT_CAP_CHARS
from tessellum.composer.context_assembler import (
    FullSourceAssembler,
    WindowedAssembler,
)
from tessellum.composer.digestion import (
    DEFAULT_DIGESTION_CONTEXT_MAX_CHARS,
    DigestionResult,
)
from tessellum.composer.loader import PipelineValidationError


@pytest.fixture
def digest_args(tmp_path: Path) -> list[str]:
    """The minimum argv prefix ``composer digest`` accepts (a real skills dir
    + a JSON-object source); the driver itself is spied by ``spy_driver``."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    source = tmp_path / "source.json"
    source.write_text(json.dumps({"id": "demo"}), encoding="utf-8")
    return [
        "composer", "digest",
        "--skills-dir", str(skills_dir),
        "--source", str(source),
        "--vault", str(tmp_path / "vault"),
        "--format", "json",
    ]


@pytest.fixture
def spy_driver(monkeypatch: pytest.MonkeyPatch) -> dict:
    """Replace the CLI's bound ``run_digestion_pipeline`` with a recorder
    that returns a minimal completed result (the CLI prints a few fields)."""
    seen: dict = {}

    def _fake(**kwargs):
        seen.update(kwargs)
        return DigestionResult(
            completed=True, stopped_at=None, sign_off=None, phases=(),
            run_id=kwargs.get("run_id"),
        )

    monkeypatch.setattr(cli_composer, "run_digestion_pipeline", _fake)
    return seen


def test_default_budget_constant_is_unchanged() -> None:
    """The named default is exactly the value the two inlined fallback sites
    used to compute — no behaviour change by naming it."""
    assert DEFAULT_DIGESTION_CONTEXT_MAX_CHARS == HARD_PROMPT_CAP_CHARS - 4_096
    assert DEFAULT_DIGESTION_CONTEXT_MAX_CHARS == 145_904


def test_digest_without_flags_passes_no_assembler(digest_args, spy_driver, capsys) -> None:
    """No flags → the CLI does not construct an assembler; the driver's own
    fallback (a windowed assembler at the named default) applies."""
    assert main(digest_args) == 0
    assert "context_assembler" not in spy_driver
    json.loads(capsys.readouterr().out)  # still a well-formed JSON report


def test_driver_fallback_uses_named_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """``run_digestion_pipeline`` with ``context_assembler=None`` builds its
    fallback from the named constant (spied at the constructor seam)."""
    from tessellum.composer import digestion

    built: list[int] = []

    class _Spy(WindowedAssembler):
        def __init__(self, *, max_chars: int, **kw) -> None:
            built.append(max_chars)
            super().__init__(max_chars=max_chars, **kw)

    monkeypatch.setattr(digestion, "WindowedAssembler", _Spy)
    # Halt right after the fallback is chosen: the first thing the driver does
    # next is compile the plan skill from skills_dir, which does not exist.
    with pytest.raises(PipelineValidationError):
        digestion.run_digestion_pipeline(
            skills_dir=Path("/nonexistent/skills"), source_leaf={"id": "x"},
            backend=None, vault_root=Path("/nonexistent/vault"), dry_run=True,
        )
    assert built == [DEFAULT_DIGESTION_CONTEXT_MAX_CHARS]


def test_context_max_chars_alone_keeps_windowed_strategy(digest_args, spy_driver) -> None:
    """The sweep case: a budget with no strategy keeps ``windowed`` (the
    driver's default strategy) at the requested size."""
    assert main([*digest_args, "--context-max-chars", "300"]) == 0
    assembler = spy_driver["context_assembler"]
    assert isinstance(assembler, WindowedAssembler)
    assert assembler.max_chars == 300


def test_context_strategy_alone_keeps_default_budget(digest_args, spy_driver) -> None:
    """A strategy with no budget keeps the driver's default SIZE — it does not
    silently widen to the assembler module's own 200K default."""
    assert main([*digest_args, "--context-strategy", "full_source"]) == 0
    assembler = spy_driver["context_assembler"]
    assert isinstance(assembler, FullSourceAssembler)
    assert assembler.max_chars == DEFAULT_DIGESTION_CONTEXT_MAX_CHARS


def test_both_flags_take_effect(digest_args, spy_driver) -> None:
    assert main([
        *digest_args, "--context-strategy", "full_source", "--context-max-chars", "4096",
    ]) == 0
    assembler = spy_driver["context_assembler"]
    assert isinstance(assembler, FullSourceAssembler)
    assert assembler.max_chars == 4096
