"""Smoke tests for tessellum.composer.contracts."""

from __future__ import annotations

import pytest

from tessellum.composer.contracts import (
    BACKEND_CONTRACTS,
    BodyMarkdownFrontmatterToFileContract,
    BodyMarkdownToFileContract,
    ContractViolation,
    EditsApplyToFilesContract,
    EditsApplyXmlTagsContract,
    LLMBackendContract,
    MATERIALIZER_CONTRACTS,
    MCP_CONTRACTS,
    MCPContract,
    MaterializerContract,
    NoOpContract,
    PlanDoc,
)


def test_materializer_registry_has_five_entries():
    assert set(MATERIALIZER_CONTRACTS.keys()) == {
        "body_markdown_to_file",
        "body_markdown_frontmatter_to_file",
        "edits_apply_to_files",
        "edits_apply_xml_tags",
        "no_op",
    }


def test_materializer_keys_match_contract_keys():
    """Each entry's key must equal its contract's materializer_key field."""
    for key, contract in MATERIALIZER_CONTRACTS.items():
        assert contract.materializer_key == key


def test_body_markdown_frontmatter_contract_shape():
    c = MATERIALIZER_CONTRACTS["body_markdown_frontmatter_to_file"]
    assert isinstance(c, BodyMarkdownFrontmatterToFileContract)
    assert c.wire_format == "markdown_with_frontmatter"
    assert c.operation_verb == "PRODUCE"
    assert c.requires_tool_free_backend is True
    assert c.requires_existing_files is False
    assert c.required_output_fields == ("output_path",)


def test_edits_apply_xml_tags_requires_apply_directive():
    c = MATERIALIZER_CONTRACTS["edits_apply_xml_tags"]
    assert isinstance(c, EditsApplyXmlTagsContract)
    assert c.wire_format == "xml_tag_list"
    assert c.operation_verb == "APPLY"
    assert c.requires_existing_files is True
    assert c.apply_mode_directive_required is True


def test_no_op_contract_no_side_effect():
    c = MATERIALIZER_CONTRACTS["no_op"]
    assert isinstance(c, NoOpContract)
    assert c.operation_verb == "DESCRIBE"
    assert c.required_output_fields == ()


def test_materializer_contract_is_frozen():
    c = MATERIALIZER_CONTRACTS["no_op"]
    with pytest.raises((TypeError, ValueError, AttributeError)):
        c.materializer_key = "tampered"  # type: ignore[misc]


def test_materializer_contract_extra_fields_forbidden():
    with pytest.raises(Exception):  # Pydantic ValidationError
        MaterializerContract(
            materializer_key="x",
            wire_format="json",
            operation_verb="PRODUCE",
            unknown_field="should-fail",  # type: ignore[call-arg]
        )


def test_backend_registry_has_mock_only_in_v009():
    assert set(BACKEND_CONTRACTS.keys()) == {"mock"}


def test_mock_backend_is_tool_free():
    mock = BACKEND_CONTRACTS["mock"]
    assert isinstance(mock, LLMBackendContract)
    assert mock.allowed_tools == ()
    assert mock.supports_batched_dispatch is True


def test_mcp_registry_ships_session_mcp():
    """Tessellum ships the session-mcp contract (read-only access to the
    active Claude Code transcript); library users add their own MCPs by
    mutating ``MCP_CONTRACTS`` before invoking the compiler."""
    assert "session-mcp" in MCP_CONTRACTS
    contract = MCP_CONTRACTS["session-mcp"]
    assert set(contract.available_tools) == {
        "get_session_metadata",
        "get_tool_uses",
        "read_recent_messages",
        "search_transcript",
    }
    assert contract.auth_required is False  # local-only transcript read
    assert contract.fallback_strategy == "degrade"  # missing transcript → degraded result


def test_mcp_contract_construction():
    contract = MCPContract(
        name="my-test-mcp",
        available_tools=("Search", "Read"),
        auth_required=False,
    )
    assert contract.name == "my-test-mcp"
    assert contract.available_tools == ("Search", "Read")
    assert contract.fallback_strategy == "fail_fast"  # default


def test_contract_violation_has_actionable_message():
    err = ContractViolation(
        step_id="step_1_foo",
        kind=ContractViolation.KIND_UNKNOWN_MATERIALIZER,
        message="materializer 'unknown_thing' is not in MATERIALIZER_CONTRACTS",
        suggested_fix="use one of: body_markdown_to_file, no_op, ...",
    )
    msg = str(err)
    assert "step_1_foo" in msg
    assert "UNKNOWN_MATERIALIZER" in msg
    assert "unknown_thing" in msg
    assert "fix" in msg


def test_contract_violation_kinds_are_strings():
    """Violation kind enum values must be strings (used in error messages)."""
    assert ContractViolation.KIND_UNKNOWN_MATERIALIZER == "UNKNOWN_MATERIALIZER"
    assert ContractViolation.KIND_WIRE_FORMAT_MISMATCH == "WIRE_FORMAT_MISMATCH"
    assert ContractViolation.KIND_UNKNOWN_MCP == "UNKNOWN_MCP"


@pytest.mark.parametrize(
    "klass",
    [
        BodyMarkdownToFileContract,
        BodyMarkdownFrontmatterToFileContract,
        EditsApplyToFilesContract,
        EditsApplyXmlTagsContract,
        NoOpContract,
    ],
)
def test_concrete_contracts_round_trip_through_dict(klass):
    """Contracts must be Pydantic-serializable for JSON output / debugging."""
    contract = klass()
    data = contract.model_dump()
    assert data["materializer_key"] == contract.materializer_key
    assert data["version"] == contract.version
    # Reconstruct
    rebuilt = klass(**data)
    assert rebuilt == contract


# ── PlanDoc — the thin typed dataflow envelope (P22; FZ 20k9c1a1a1b7c2f) ─────


def test_plan_doc_alias_fold_fills_canonical_from_aliases():
    """The E6 bridge: write-plan materializer aliases fill the canonical keys
    the gate + downstream read."""
    pd = PlanDoc.from_dict(
        {"output_path": "/p", "body_markdown": "# Body", "planned_note_count": 5}
    )
    assert pd.plan_path == "/p"
    assert pd.plan_text == "# Body"
    assert pd.total_notes == 5


def test_plan_doc_alias_fold_does_not_clobber_canonical():
    """A value already set under the canonical key is NOT overwritten by an alias."""
    pd = PlanDoc.from_dict(
        {"plan_path": "/canonical", "output_path": "/alias"}
    )
    assert pd.plan_path == "/canonical"


def test_plan_doc_estimated_note_count_alias():
    pd = PlanDoc.from_dict({"estimated_note_count": 7})
    assert pd.total_notes == 7


def test_plan_doc_longest_of_plan_text_restores_body():
    """A lossy re-emission (short plan_text) is overridden by the longer
    authoritative body_markdown."""
    pd = PlanDoc.from_dict(
        {"plan_text": "short", "body_markdown": "a much longer authoritative body"}
    )
    assert pd.plan_text == "a much longer authoritative body"


def test_plan_doc_longest_of_keeps_longer_plan_text():
    """A plan_text already longer than body_markdown is not shrunk."""
    pd = PlanDoc.from_dict(
        {"plan_text": "the full and complete plan text", "body_markdown": "tiny"}
    )
    assert pd.plan_text == "the full and complete plan text"


def test_plan_doc_total_notes_floor_restores_shrunk_count():
    """P21 core: total_notes below the enumerated planned_notes count is
    restored to the enumerated floor — you can't declare fewer than enumerated."""
    pd = PlanDoc.from_dict(
        {"planned_notes": [{"f": i} for i in range(5)], "total_notes": 2}
    )
    assert pd.total_notes == 5


def test_plan_doc_total_notes_keeps_larger_declared():
    """A legitimately-larger declared total (a master plan enumerating a
    subset) is preserved, not shrunk to the enumerated count."""
    pd = PlanDoc.from_dict(
        {"planned_notes": [{"f": "a"}, {"f": "b"}], "total_notes": 29}
    )
    assert pd.total_notes == 29


def test_plan_doc_total_notes_set_from_planned_when_missing():
    pd = PlanDoc.from_dict(
        {"planned_notes": [{"f": "a"}, {"f": "b"}, {"f": "c"}]}
    )
    assert pd.total_notes == 3


def test_plan_doc_empty_total_notes_zero_so_plan003_fires():
    """No count anywhere → total_notes 0 (the silent-reject fix must NOT mask a
    genuinely empty plan; PLAN-003 still sees 0)."""
    assert PlanDoc.from_dict({}).total_notes == 0


def test_plan_doc_non_int_total_notes_preserved_verbatim():
    """A garbage non-int total_notes is left UNTOUCHED (byte-identical to the
    pre-P22 imperative code, which never coerced it) — total_notes is an ``Any``
    field, not a strict int, so validation never raises. Nothing downstream
    reads a non-int total as a count (``_declared_note_count`` treats it as 0)."""
    assert PlanDoc.from_dict({"total_notes": "two"}).total_notes == "two"
    # With planned_notes present, the floor overrides it (a non-int total < the
    # enumerated count, so the floor applies) → the enumerated len.
    pd = PlanDoc.from_dict({"total_notes": "two", "planned_notes": [{"a": 1}]})
    assert pd.total_notes == 1


def test_plan_doc_non_str_plan_text_does_not_raise():
    """Byte-identity: a non-str / None plan_text or plan_path must NOT raise a
    ValidationError (the fields are ``Any``, not strict ``str``) — the pre-P22
    code left such a value untouched and the fail-closed plan gate rejected it
    cleanly. A strict ``str`` field would abort the phase instead."""
    for bad in (
        {"plan_text": None},
        {"plan_path": None},
        {"plan_text": 123},
        {"plan_text": []},
        {"plan_path": 123, "body_markdown": "B"},
    ):
        pd = PlanDoc.from_dict(bad)  # must not raise
        # The value is preserved verbatim (only a str body longer than a str
        # plan_text triggers the longest-of restore; a non-str plan_text is not
        # a str so the guard is skipped — untouched, exactly like the old code).
        if "plan_text" in bad:
            assert pd.plan_text == bad["plan_text"]
        if "plan_path" in bad:
            assert pd.plan_path == bad["plan_path"]


def test_plan_doc_tuple_planned_notes_not_floored():
    """Byte-identity: the floor guards on ``list`` only (like the old code), so
    a tuple planned_notes does NOT trigger the floor (a real plan_doc always
    carries a list; this pins the exact pre-P22 behaviour)."""
    pd = PlanDoc.from_dict({"planned_notes": ({"a": 1}, {"b": 2})})
    assert pd.total_notes == 0  # not floored (tuple, not list)


def test_plan_doc_preserves_extra_keys_losslessly():
    """The ~dozen non-envelope keys a real plan carries round-trip untouched
    (extra='allow')."""
    raw = {
        "body_markdown": "B",
        "members": [1, 2, 3],
        "routing_decision": {"target_directory": "d"},
        "note_intent_graph": {"nodes": []},
        "section_coverage_map": {"h2": "note"},
        "file_prefix": "cc_",
    }
    out = PlanDoc.from_dict(raw).to_normalized_dict()
    assert out["members"] == [1, 2, 3]
    assert out["routing_decision"] == {"target_directory": "d"}
    assert out["note_intent_graph"] == {"nodes": []}
    assert out["section_coverage_map"] == {"h2": "note"}
    assert out["file_prefix"] == "cc_"
    # And the canonical fold still ran.
    assert out["plan_text"] == "B"


def test_plan_doc_is_idempotent():
    """Re-folding an already-normalized envelope is a no-op."""
    raw = {"planned_notes": [{"f": "a"}], "body_markdown": "B", "plan_text": "B"}
    once = PlanDoc.from_dict(raw).to_normalized_dict()
    twice = PlanDoc.from_dict(once).to_normalized_dict()
    assert once == twice


def test_plan_doc_frozen():
    """The envelope is a value, not live state — frozen."""
    pd = PlanDoc.from_dict({"plan_text": "x"})
    with pytest.raises((ValueError, TypeError)):
        pd.plan_text = "mutated"  # type: ignore[misc]


def test_plan_doc_verdict_and_ready_fields():
    pd = PlanDoc.from_dict({"ready": True, "failures": ["a", "b"], "verdict": {"ok": 1}})
    assert pd.ready is True
    assert list(pd.failures) == ["a", "b"]
    assert pd.verdict == {"ok": 1}
