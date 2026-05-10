"""Single source of version + status. Imported by ``tessellum.__init__`` and
``tessellum.cli`` so neither holds its own copy."""

__version__ = "0.0.36"

__status__ = (
    "alpha — session-mcp ported as Tessellum's first built-in MCP. Pure "
    "Python handlers (tessellum.composer.session_mcp: get_session_metadata, "
    "read_recent_messages, search_transcript, get_tool_uses) + a stdio "
    "MCP server (scripts/tessellum_session_mcp_server.py) that registers "
    "into ~/.claude/settings.json. MCP_CONTRACTS now ships the "
    "'session-mcp' entry so skills can declare mcp_dependencies: "
    "session-mcp and the compiler validates the tool list against the "
    "contract. skill_tessellum_write_coe sidecar restores its step_1 "
    "MCP dependency."
)
