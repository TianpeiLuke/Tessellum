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


def test_mcp_registry_is_empty_in_v009():
    """Tessellum ships no built-in MCPs — users register their own."""
    assert MCP_CONTRACTS == {}


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
