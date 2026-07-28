"""P21-full (FZ 20k9c1a1a1b7c2j) — {{artifact.X}} by-reference channel +
compiler re-emission lint.

Large durable artifacts (plan_text, source_excerpt, planned_notes) travel
between digestion phases BY REFERENCE — the driver injects them into a
consumer's prompt via the {{artifact.X}} namespace — instead of a step
re-emitting them through the LLM (lossy, the E12/E16/E18 chain). The compiler
LINTS a no_op step that consumes AND re-declares an artifact (author-may-emit,
pass-through-must-reference), warn-default with a strict opt-in.

Covers:
  - HALF A (channel): {{artifact.X}} resolves from the store; missing key →
    sentinel; artifacts=None is byte-identical for a prompt with no
    {{artifact.X}}; execute_step_with_retry forwards artifacts into each retry.
  - HALF B (lint): a no_op re-emitter is flagged (warn); a materializing author
    is NOT flagged; strict mode raises ContractViolation(KIND_RE_EMISSION); a
    pure DESCRIBE consumer that does not re-declare is NOT flagged.

Pure/in-memory — no network. Safe alongside a live run.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tessellum.composer import (
    MockBackend,
    compile_skill,
    execute_step,
    execute_step_with_retry,
)
from tessellum.composer.contracts import ContractViolation
from tessellum.composer.executor import _resolve_placeholders
from tessellum.composer.llm import LLMRequest, LLMResponse


# ── HALF A: the {{artifact.X}} channel (pure resolver) ───────────────────────


def test_artifact_placeholder_resolves_from_store():
    out = _resolve_placeholders(
        "read {{artifact.plan_text}} and {{leaf.x}}",
        leaf={"x": "L"}, upstream={}, artifacts={"plan_text": "THE PLAN"},
    )
    assert out == "read THE PLAN and L"


def test_artifact_missing_key_yields_sentinel():
    out = _resolve_placeholders(
        "{{artifact.source_excerpt}}", leaf={}, upstream={}, artifacts={},
    )
    assert out == "<missing artifact.source_excerpt>"


def test_no_second_order_substitution_in_leaf_values():
    """A leaf/upstream VALUE that literally contains {{artifact.X}} must NOT be
    expanded — the single-pass resolver sees only the ORIGINAL template's
    placeholders and never re-scans injected content. Prevents silent content
    corruption when digesting source material that references the artifact
    namespace (e.g. Tessellum's own CHANGELOG/skills/tests)."""
    out = _resolve_placeholders(
        "BODY: {{leaf.note}}",
        leaf={"note": "see {{artifact.plan_text}} in the design"},
        upstream={},
        artifacts={"plan_text": "THE ENTIRE PLAN BODY"},
    )
    assert "THE ENTIRE PLAN BODY" not in out  # NOT expanded
    assert "{{artifact.plan_text}}" in out  # verbatim in output


def test_no_second_order_substitution_in_upstream_values():
    """Same guard for upstream: a value with an embedded {{leaf.X}} or
    {{artifact.X}} token must NOT be expanded when injected by {{upstream.Y}}."""
    out = _resolve_placeholders(
        "REF: {{upstream.plan}}",
        leaf={"x": "LEAF_VALUE"},
        upstream={"plan": "see {{leaf.x}} here"},
        artifacts={},
    )
    assert "LEAF_VALUE" not in out  # NOT expanded
    assert "{{leaf.x}}" in out  # verbatim


def test_artifact_none_store_is_byte_identical_without_artifact_ref():
    """A prompt with NO {{artifact.X}} renders identically whether artifacts is
    None or a store — the IDENT guard for every pre-P21 caller."""
    prompt = "plain {{leaf.x}} and {{upstream.y}}"
    a = _resolve_placeholders(prompt, leaf={"x": "L"}, upstream={"y": "U"})
    b = _resolve_placeholders(prompt, leaf={"x": "L"}, upstream={"y": "U"}, artifacts={})
    c = _resolve_placeholders(prompt, leaf={"x": "L"}, upstream={"y": "U"},
                              artifacts={"plan_text": "unused"})
    assert a == b == c == "plain L and U"


# ── HALF A: execute_step + retry forward the artifacts store ─────────────────

_CANON = textwrap.dedent(
    """\
    ---
    tags:
      - resource
      - skill
    keywords:
      - alpha
      - beta
      - gamma
    topics:
      - X
      - Y
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # Demo

    ## Step 1: read <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: loaded
    ```

    Judge the plan {{artifact.plan_text}} for leaf {{leaf.id}}.
    """
)


def _compile(tmp_path: Path):
    sk = tmp_path / "skill_demo.md"
    sk.write_text(_CANON, encoding="utf-8")
    return compile_skill(sk)


def test_execute_step_injects_artifact_by_reference(tmp_path: Path):
    compiled = _compile(tmp_path)
    backend = MockBackend(default="{}")
    execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "n1"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
        artifacts={"plan_text": "THE FULL PLAN OF RECORD"},
    )
    prompt = backend.calls[0].user_prompt
    assert "THE FULL PLAN OF RECORD" in prompt
    assert "n1" in prompt


def test_execute_step_no_artifacts_leaves_sentinel(tmp_path: Path):
    compiled = _compile(tmp_path)
    backend = MockBackend(default="{}")
    execute_step(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "n1"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
    )
    assert "<missing artifact.plan_text>" in backend.calls[0].user_prompt


def test_execute_step_with_retry_forwards_artifacts_each_attempt(tmp_path: Path):
    """A crash-then-success backend retries; the artifact must be present in the
    retry's prompt too (forwarded through the retry wrapper)."""
    class _CrashThenSuccess:
        backend_id = "cts"

        def __init__(self) -> None:
            self.calls = 0
            self.prompts: list[str] = []

        def call(self, request: LLMRequest) -> LLMResponse:
            self.calls += 1
            self.prompts.append(request.user_prompt)
            if self.calls == 1:
                raise RuntimeError("transient blip")
            return LLMResponse(content="{}", elapsed_ms=1.0, backend_id=self.backend_id)

    compiled = _compile(tmp_path)
    backend = _CrashThenSuccess()
    execute_step_with_retry(
        compiled.steps[0],
        leaf={"_id": "leaf_0", "id": "n1"},
        upstream={},
        backend=backend,
        vault_root=tmp_path,
        artifacts={"plan_text": "PLAN-OF-RECORD"},
    )
    assert backend.calls == 2
    # BOTH the first attempt and the retry saw the artifact by reference.
    assert all("PLAN-OF-RECORD" in p for p in backend.prompts), backend.prompts


# ── HALF B: the compiler re-emission lint ────────────────────────────────────

# A no_op step that CONSUMES {{...plan_text}} AND re-declares plan_text as its
# output — the pass-through re-emission smell.
_RE_EMITTER = textwrap.dedent(
    """\
    ---
    tags: [resource, skill]
    keywords: [a, b, c]
    topics: [X, Y]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # Demo

    ## Step 1: read <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: plan_doc
    expected_output_schema:
      type: object
      required: [plan_text]
      properties:
        plan_text:
          type: string
    ```

    Read the plan {{artifact.plan_text}} and echo it.
    """
)

# A no_op consumer that reads the artifact but does NOT re-declare it (a pure
# DESCRIBE that emits only a verdict) — legitimate, must NOT be flagged.
_PURE_CONSUMER = textwrap.dedent(
    """\
    ---
    tags: [resource, skill]
    keywords: [a, b, c]
    topics: [X, Y]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # Demo

    ## Step 1: judge <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: corpus_wide
    batchable: false
    depends_on: []
    materializer: no_op
    output_key: verdict
    expected_output_schema:
      type: object
      required: [ready]
      properties:
        ready:
          type: boolean
    ```

    Judge the plan {{artifact.plan_text}} and return ready.
    """
)

# A materializing AUTHOR (body_markdown_to_file / PRODUCE) that emits
# body_markdown — the legitimate writer, must NOT be flagged even though it
# consumes an artifact.
_AUTHOR = textwrap.dedent(
    """\
    ---
    tags: [resource, skill]
    keywords: [a, b, c]
    topics: [X, Y]
    language: markdown
    date of note: 2026-05-10
    status: active
    building_block: procedure
    ---

    # Demo

    ## Step 1: write <!-- :: section_id = step_1 :: -->

    ```yaml
    role: CORE
    aggregation: per_leaf
    batchable: false
    depends_on: []
    materializer: body_markdown_to_file
    output_key: written
    expected_output_schema:
      type: object
      required: [output_path, body_markdown]
      properties:
        output_path:
          type: string
        body_markdown:
          type: string
    ```

    Author the note, referencing the plan {{artifact.plan_text}}.
    """
)


def _write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_lint_flags_no_op_re_emitter(tmp_path: Path):
    compiled = compile_skill(_write(tmp_path, "skill_reemit.md", _RE_EMITTER))
    assert len(compiled.re_emission_warnings) == 1
    assert "plan_text" in compiled.re_emission_warnings[0]
    assert "step_1" in compiled.re_emission_warnings[0]


def test_lint_does_not_flag_pure_consumer(tmp_path: Path):
    compiled = compile_skill(_write(tmp_path, "skill_pure.md", _PURE_CONSUMER))
    assert compiled.re_emission_warnings == ()


def test_lint_does_not_flag_materializing_author(tmp_path: Path):
    compiled = compile_skill(_write(tmp_path, "skill_author.md", _AUTHOR))
    assert compiled.re_emission_warnings == ()


def test_lint_warn_default_does_not_raise(tmp_path: Path):
    # Default: the re-emitter compiles (warns), does not raise.
    compiled = compile_skill(_write(tmp_path, "skill_reemit2.md", _RE_EMITTER))
    assert compiled.re_emission_warnings  # warned, but compiled


def test_lint_strict_mode_raises(tmp_path: Path):
    with pytest.raises(ContractViolation) as exc:
        compile_skill(
            _write(tmp_path, "skill_reemit3.md", _RE_EMITTER),
            strict_re_emission=True,
        )
    assert exc.value.kind == ContractViolation.KIND_RE_EMISSION


def test_lint_strict_mode_passes_clean_skill(tmp_path: Path):
    # A clean skill compiles under strict mode without raising.
    compile_skill(
        _write(tmp_path, "skill_pure2.md", _PURE_CONSUMER),
        strict_re_emission=True,
    )


def test_lint_catches_required_only_artifact_declaration(tmp_path: Path):
    """A no_op step declaring plan_text ONLY under 'required' (not 'properties')
    still re-emits it — the lint must catch it (the required sub-key forces the
    LLM to emit the field via schema-injection + jsonschema validation)."""
    skill = textwrap.dedent(
        """\
        ---
        tags: [resource, skill]
        keywords: [a, b, c]
        topics: [X, Y]
        language: markdown
        date of note: 2026-05-10
        status: active
        building_block: procedure
        ---

        # Demo

        ## Step 1: read <!-- :: section_id = step_1 :: -->

        ```yaml
        role: CORE
        aggregation: corpus_wide
        batchable: false
        depends_on: []
        materializer: no_op
        output_key: plan_doc
        expected_output_schema:
          type: object
          required: [plan_path, status, plan_text]
          properties:
            plan_path:
              type: string
            status:
              type: string
        ```

        Read {{artifact.plan_text}} and output the plan identity.
        """
    )
    compiled = compile_skill(_write(tmp_path, "skill_required_only.md", skill))
    assert len(compiled.re_emission_warnings) == 1, (
        "a required-only plan_text re-declaration must be caught by the lint"
    )
    assert "plan_text" in compiled.re_emission_warnings[0]
