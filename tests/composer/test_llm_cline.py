"""ClineBackend — one-shot completions through the ``cline`` CLI (no network).

Every test drives the backend against a FAKE ``cline`` executable written into
``tmp_path``: a shell shim that execs a Python script which records its argv
and stdin to files, then plays a canned scenario chosen by the
``FAKE_CLINE_MODE`` environment variable. Nothing here touches the real
``cline`` binary, ``~/.cline``, or the network.

The scenarios pin the rules the reference ``ask_cline`` learned the hard way:
the argv shape (NO ``--data-dir``; ``--cwd`` at an empty sandbox;
``--auto-approve false``; ``-s`` replacing the coding system prompt), the
answer being the ``text`` of the final ``run_result`` line with streamed
reasoning ignored, and every failure — ``Unauthorized``, ``rate limit``, an
empty non-zero exit, a missing ``run_result``, a hang — RAISING so the retry
ladder sees a real exception instead of error text as content.
"""

from __future__ import annotations

import json
import os
import stat
import sys
import textwrap
import time
from pathlib import Path

import pytest

from tessellum.composer import ClineBackend, LLMRequest
from tessellum.composer.error_taxonomy import classify_reason
from tessellum.composer.llm import (
    _CLINE_ARGV_PROMPT_MAX_BYTES,
    ClineBackendError,
    _split_prompt_for_argv,
)
from tessellum.runtime.executor import BackendConfig, build_backend

# ── the fake cline ─────────────────────────────────────────────────────────

_FAKE_CLINE_PY = textwrap.dedent(
    '''\
    """Fake `cline`: record argv + stdin, then play the FAKE_CLINE_MODE scenario."""
    import json
    import os
    import sys
    import time

    log_dir = os.environ["FAKE_CLINE_LOG_DIR"]
    with open(os.path.join(log_dir, "argv.json"), "w", encoding="utf-8") as fh:
        json.dump(sys.argv[1:], fh)
    stdin_text = "" if sys.stdin.isatty() else sys.stdin.read()
    with open(os.path.join(log_dir, "stdin.txt"), "w", encoding="utf-8") as fh:
        fh.write(stdin_text)

    mode = os.environ.get("FAKE_CLINE_MODE", "ok")
    answer = os.environ.get("FAKE_CLINE_ANSWER", '{"ok": true}')

    def emit(obj):
        sys.stdout.write(json.dumps(obj) + "\\n")

    if mode == "ok":
        # Streamed scratchpad first -- must never be returned as the answer.
        emit({"type": "reasoning", "text": "Let me think about Unauthorized access..."})
        emit({"type": "chunk", "value": "partial "})
        sys.stdout.write("cline: plain-text status line\\n")
        emit({"type": "run_result", "finishReason": "stop", "iterations": 1,
              "usage": {"totalCost": 0.0}, "aggregateUsage": {"totalCost": 0.0025},
              "durationMs": 1234, "text": answer, "model": "deepseek/deepseek-v4-flash"})
        sys.exit(0)
    if mode == "unauthorized_text":
        emit({"type": "run_result", "finishReason": "error", "text": "Unauthorized",
              "model": "deepseek/deepseek-v4-flash"})
        sys.exit(0)
    if mode == "finish_error":
        # Verified LIVE against cline 3.0.61 + DeepSeek's daily cap: a clean
        # exit, a run_result, finishReason "error", the gateway's JSON envelope
        # as the text, and total_cost 0. Nothing in it says "unauthorized" or
        # "rate limit".
        emit({"type": "run_result", "finishReason": "error", "iterations": 1,
              "usage": {"totalCost": 0}, "text": answer,
              "model": "deepseek/deepseek-v4-flash"})
        sys.exit(0)
    if mode == "unauthorized_stderr":
        sys.stderr.write(json.dumps({"type": "error", "message": "Unauthorized"}) + "\\n")
        sys.exit(1)
    if mode == "rate_limit":
        sys.stderr.write(json.dumps({"type": "error",
                                     "message": "Provider rate limit exceeded"}) + "\\n")
        sys.exit(1)
    if mode == "empty_rc1":
        sys.stderr.write("boom\\n")
        sys.exit(1)
    if mode == "no_run_result":
        emit({"type": "chunk", "value": "partial"})
        sys.exit(0)
    if mode == "empty_text":
        emit({"type": "run_result", "finishReason": "length", "text": "",
              "model": "deepseek/deepseek-v4-flash"})
        sys.exit(0)
    if mode == "hang":
        time.sleep(30)
        sys.exit(0)
    sys.stderr.write("unknown FAKE_CLINE_MODE\\n")
    sys.exit(3)
    '''
)


@pytest.fixture
def fake_cline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Write the fake ``cline`` into ``tmp_path`` and return its path.

    A ``/bin/sh`` shim execs the current interpreter on the Python body, so
    the shebang never depends on a ``python3`` on PATH (or on its length).
    """
    script = tmp_path / "fake_cline.py"
    script.write_text(_FAKE_CLINE_PY, encoding="utf-8")
    shim = tmp_path / "cline"
    shim.write_text(
        f'#!/bin/sh\nexec "{sys.executable}" "{script}" "$@"\n', encoding="utf-8"
    )
    shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    log_dir = tmp_path / "log"
    log_dir.mkdir()
    monkeypatch.setenv("FAKE_CLINE_LOG_DIR", str(log_dir))
    monkeypatch.setenv("FAKE_CLINE_MODE", "ok")
    monkeypatch.delenv("FAKE_CLINE_ANSWER", raising=False)
    return shim


def _recorded_argv(tmp_path: Path) -> list[str]:
    return json.loads((tmp_path / "log" / "argv.json").read_text(encoding="utf-8"))


def _recorded_stdin(tmp_path: Path) -> str:
    return (tmp_path / "log" / "stdin.txt").read_text(encoding="utf-8")


def _req(user: str = "What is 2+2?", system: str = "You are terse.") -> LLMRequest:
    return LLMRequest(system_prompt=system, user_prompt=user, max_tokens=256)


# ── argv shape ─────────────────────────────────────────────────────────────


def test_argv_shape_matches_reference(fake_cline: Path, tmp_path: Path) -> None:
    sandbox = tmp_path / "sandbox"
    backend = ClineBackend(
        model="deepseek/deepseek-v4-flash", provider="cline",
        sandbox=sandbox, timeout_s=90.0, cline_bin=str(fake_cline),
    )
    backend.call(_req())
    argv = _recorded_argv(tmp_path)

    assert "--data-dir" not in argv, "NEVER --data-dir: it yields Unauthorized on every call"
    assert argv[argv.index("--cwd") + 1] == str(sandbox)
    assert argv[argv.index("--auto-approve") + 1] == "false"
    assert argv[argv.index("-s") + 1] == "You are terse."
    assert argv[argv.index("-P") + 1] == "cline"
    assert argv[argv.index("-m") + 1] == "deepseek/deepseek-v4-flash"
    assert argv[argv.index("-t") + 1] == "90"
    assert "--json" in argv
    assert argv[-1] == "What is 2+2?", "the user prompt is the trailing positional"
    # Ordering as the reference builds it: flags first, prompt last.
    assert argv.index("-P") < argv.index("--cwd") < argv.index("--auto-approve")
    assert argv.index("-s") < argv.index("-m") < len(argv) - 1


def test_sandbox_is_created_and_stdin_is_devnull(fake_cline: Path, tmp_path: Path) -> None:
    sandbox = tmp_path / "deep" / "sandbox"
    assert not sandbox.exists()
    backend = ClineBackend(sandbox=sandbox, cline_bin=str(fake_cline))
    backend.call(_req())
    assert sandbox.is_dir()
    # stdin must be closed (/dev/null), never an inherited pipe cline would
    # read to EOF -- an orchestrator's open stdin would stall every call.
    assert _recorded_stdin(tmp_path) == ""


def test_default_sandbox_lives_under_tmp_and_timeout_rounds_up(fake_cline: Path) -> None:
    backend = ClineBackend(cline_bin=str(fake_cline), timeout_s=0.5)
    assert backend.sandbox.name == "tessellum-cline-sandbox"
    argv, stdin_tail = backend.build_command(_req())
    assert argv[argv.index("-t") + 1] == "1", "cline wants an integer >= 1"
    assert stdin_tail is None
    assert backend.backend_id == "cline"
    assert backend.cline_bin == str(fake_cline)


def test_missing_binary_fails_at_construction(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        ClineBackend(cline_bin=str(tmp_path / "definitely-not-cline"))


# ── the happy path ─────────────────────────────────────────────────────────


def test_run_result_text_is_returned_and_reasoning_ignored(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FAKE_CLINE_ANSWER", '{"answer": "4"}')
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    resp = backend.call(_req())
    assert resp.content == '{"answer": "4"}'
    assert "partial" not in resp.content and "Let me think" not in resp.content
    assert resp.backend_id == "cline"
    assert resp.elapsed_ms >= 0
    assert resp.metadata["model"] == "deepseek/deepseek-v4-flash"
    assert resp.metadata["provider"] == "cline"
    assert isinstance(resp.metadata["elapsed"], float)
    assert resp.metadata["stop_reason"] == "stop"
    assert resp.metadata["total_cost"] == pytest.approx(0.0025)
    # cline exposes no max-tokens flag; the request's cap is echoed for the trace.
    assert resp.metadata["max_tokens_requested"] == 256


def test_long_answer_mentioning_unauthorized_is_content(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A real note body ABOUT 401s must not be raised as a refusal: the
    # reasoning stream in the "ok" scenario already says "Unauthorized", and
    # here the answer itself does too -- at note length it is content.
    body = ("The API returns 401 Unauthorized when the token is missing. " * 20).strip()
    assert len(body) > 600
    monkeypatch.setenv("FAKE_CLINE_ANSWER", body)
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    assert backend.call(_req()).content == body


# ── failures RAISE (never returned as content) ─────────────────────────────


def test_unauthorized_run_result_text_raises_auth(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FAKE_CLINE_MODE", "unauthorized_text")
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    with pytest.raises(ClineBackendError) as ei:
        backend.call(_req())
    assert "Unauthorized" in str(ei.value)
    assert classify_reason(str(ei.value)) == "auth"


def test_unauthorized_stderr_error_line_raises_auth(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # In --json mode cline writes {"type":"error"} lines to STDERR.
    monkeypatch.setenv("FAKE_CLINE_MODE", "unauthorized_stderr")
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    with pytest.raises(ClineBackendError) as ei:
        backend.call(_req())
    assert classify_reason(str(ei.value)) == "auth"


def test_rate_limit_raises_rate_limit(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FAKE_CLINE_MODE", "rate_limit")
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    with pytest.raises(ClineBackendError) as ei:
        backend.call(_req())
    assert classify_reason(str(ei.value)) == "rate_limit"


def test_empty_stdout_with_nonzero_exit_raises(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FAKE_CLINE_MODE", "empty_rc1")
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    with pytest.raises(ClineBackendError) as ei:
        backend.call(_req())
    msg = str(ei.value)
    assert "rc=1" in msg and "empty stdout" in msg and "boom" in msg


def test_missing_run_result_raises(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FAKE_CLINE_MODE", "no_run_result")
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    with pytest.raises(ClineBackendError, match="no run_result"):
        backend.call(_req())


def test_empty_run_result_text_raises(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FAKE_CLINE_MODE", "empty_text")
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    with pytest.raises(ClineBackendError, match="empty run_result"):
        backend.call(_req())


def test_timeout_raises_instead_of_hanging(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FAKE_CLINE_MODE", "hang")
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline), timeout_s=0.5)
    started = time.monotonic()
    with pytest.raises(ClineBackendError) as ei:
        backend.call(_req())
    assert time.monotonic() - started < 10.0, "a wedged cline must fail, not hang"
    assert "timed out" in str(ei.value)
    assert classify_reason(str(ei.value)) == "stall", "transient rung, not crash"


# ── long prompts spill to stdin (Linux caps one argv string at 128KB) ──────


def test_split_prompt_keeps_small_prompts_whole() -> None:
    assert _split_prompt_for_argv("short prompt") == ("short prompt", None)


def _long_paragraph_prompt(extra_paragraphs: int) -> str:
    para = "some words in a paragraph, then more words. " * 25
    n = _CLINE_ARGV_PROMPT_MAX_BYTES // len(para) + extra_paragraphs
    return "\n\n".join([para.strip()] * n)


def test_split_prompt_cuts_on_a_paragraph_so_cline_rejoin_is_lossless(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The installed cline (3.0.61, read from the binary) joins the argv prompt
    and a piped stdin tail as f"{prompt}\\n\\n{stdin.strip()}" -- a DOUBLE
    NEWLINE, not a space. The first version of this test pinned a space join,
    which would have put a spurious paragraph break ~100KB into every long
    digestion prompt, mid-table or mid-fence."""
    monkeypatch.setattr(sys, "platform", "linux")
    prompt = _long_paragraph_prompt(20)
    head, tail = _split_prompt_for_argv(prompt)
    assert tail is not None
    assert len(head.encode("utf-8")) <= _CLINE_ARGV_PROMPT_MAX_BYTES
    assert f"{head}\n\n{tail}" == prompt


def test_split_prompt_does_not_spill_on_macos(monkeypatch: pytest.MonkeyPatch) -> None:
    """macOS has no per-argument cap, so spilling there only risks altering a
    prompt that would have arrived intact. The spill is Linux-only."""
    monkeypatch.setattr(sys, "platform", "darwin")
    prompt = _long_paragraph_prompt(20)
    assert _split_prompt_for_argv(prompt) == (prompt, None)


def test_long_user_prompt_tail_is_piped_on_stdin(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "platform", "linux")
    prompt = _long_paragraph_prompt(30)
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    backend.call(_req(user=prompt))
    argv = _recorded_argv(tmp_path)
    assert len(argv[-1].encode("utf-8")) <= _CLINE_ARGV_PROMPT_MAX_BYTES
    assert f"{argv[-1]}\n\n{_recorded_stdin(tmp_path).strip()}" == prompt


def test_finish_reason_error_raises_even_with_json_text(
    fake_cline: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verified live: a daily-cap 429 arrives as a run_result with finishReason
    "error" and the gateway's JSON envelope as the text. It must raise --
    answer_eval.py calls backend.call() directly, bypassing the executor's
    body guard, and would otherwise score the envelope as an answer."""
    monkeypatch.setenv("FAKE_CLINE_MODE", "finish_error")
    monkeypatch.setenv(
        "FAKE_CLINE_ANSWER",
        '{"error":{"code":"INFERENCE_CAP_ERROR","message":"Error 429: Daily free '
        'limit reached on model deepseek/deepseek-v4-flash-0731. Try again in 17h 20m"}}',
    )
    backend = ClineBackend(sandbox=tmp_path / "sb", cline_bin=str(fake_cline))
    with pytest.raises(ClineBackendError) as ei:
        backend.call(_req())
    assert classify_reason(str(ei.value)) == "rate_limit"


# ── registration ───────────────────────────────────────────────────────────


def test_runtime_build_backend_selects_cline(
    fake_cline: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(fake_cline.parent) + os.pathsep + os.environ.get("PATH", ""))
    backend = build_backend(BackendConfig(kind="cline"))
    assert isinstance(backend, ClineBackend)
    assert backend.model == "deepseek/deepseek-v4-flash"
    assert build_backend(BackendConfig(kind="cline", model="x/y")).model == "x/y"


@pytest.mark.parametrize(
    "argv",
    [
        ["composer", "run", "skill.md", "--backend", "cline"],
        ["composer", "digest", "--source", "leaf.json", "--backend", "cline"],
        ["composer", "batch", "jobs.json", "--backend", "cline"],
        ["composer", "eval", "scenarios", "--backend", "cline", "--judge-backend", "cline"],
        ["runtime", "work", "--backend", "cline"],
        ["dks", "--backend", "cline"],
    ],
)
def test_cli_backend_choices_accept_cline(argv: list[str]) -> None:
    from tessellum.cli.main import _build_parser

    ns = _build_parser().parse_args(argv)
    assert ns.backend == "cline"
