# Tessellum MCP Server

## Mental model

An MCP host — Claude Desktop, an MCP-aware IDE, any agent that speaks the Model Context Protocol — needs a way to reach into a Tessellum vault. It wants to search the vault, validate a note, audit the graph, walk a Folgezettel trail, or write a new note. The MCP server is that front door. It wraps Tessellum's deterministic runtime as a small set of callable tools and serves them over stdio, so the connected agent can operate on the vault without knowing anything about Tessellum's internals.

The core idea is a clean division of labor: the server does the deterministic work, the agent does the thinking. Every runtime tool is a thin wrapper over a pure Python API, so the server never calls an LLM. On top of that, the server acts as a skills-as-tools front door. Two of its tools hand back the raw text of a shipped skill so that the *calling* agent runs the procedure in its own model context. The canonical is the prompt; the agent supplies the LLM.

This is a shipped component, not a stub. The server advertises seven working tools and serves them over a real transport. The only thing gating it is the optional `[mcp]` install extra.

## Model

```
MCP host (Claude Desktop / IDE)
        │  JSON-RPC over stdio
        ▼
run_stdio()  ──►  build the "tessellum" MCP Server
        │                       │
        │       list-tools handler   │  advertises 7 tool descriptors
        │       call-tool handler     │  receives (name, arguments)
        ▼                            ▼
   stdio transport              dispatch by tool name
                                     │
              ┌──────────────────────┼────────────────────────┐
              ▼                       ▼                         ▼
     Runtime tools (no LLM)    Capture (write side)     Skill tools (prompt fetch)
     search    ─► retrieval      capture ─► new note      list-skills ─► canonicals
     format    ─► validator                              get-skill   ─► one canonical
     bb-audit  ─► graph telemetry
     fz-walk   ─► Folgezettel walk
```

Three layers sit between the host and the vault. At the edge, `run_stdio()` opens the stdio transport and hands the read/write streams to a freshly built server instance. That server owns two handlers. One advertises the tool descriptors — each tool's name, description, and input schema — when the host asks what is available. The other receives every call as a name plus an argument object. The second handler routes the call to the matching implementation and serializes whatever comes back.

The tools fall into three families. The runtime tools — search, format-check, BB-audit, and Folgezettel traversal — are read-only wrappers over Tessellum's retrieval and graph APIs. Capture is the one write-side tool: it creates a new typed note from a template. The skill tools — list-skills and get-skill — read skill canonicals off disk and return their text. The runtime and capture families touch the index database and the vault; the skill family reads the shipped skills directory.

## Procedure

When a host connects, it first asks for the tool list. The server returns the seven descriptors verbatim from a static specification. From then on every interaction is a tool call. The host sends a name and an argument object, the call handler dispatches to the implementation, and the implementation runs a deterministic Python API and returns a plain dictionary.

Each family follows its own short flow. Search resolves the index database path, runs hybrid BM25-plus-dense-plus-graph retrieval, and returns the ranked hits with their scores and per-signal ranks. Format-check takes a file or a directory — a directory expands to every Markdown note beneath it — validates each note against the format rules, and returns only the notes that have issues. BB-audit loads the Building-Block graph from the database and reports node and edge counts, how many edges are untyped, and which schema edges the corpus has not yet realized. Folgezettel traversal loads the same graph, finds the starting note by its Folgezettel ID, and walks to its ancestors, descendants, or siblings. Capture resolves the vault root and writes a new note from the requested template flavor, returning the created path.

The two skill tools are the front door for procedural knowledge. List-skills enumerates the shipped skill canonicals, returning each one's name, title, and whether it carries a pipeline sidecar. Get-skill returns the full canonical body of one skill, plus its sidecar body when present. The server does not run the skill. It hands the text back, and the connected agent applies the procedure in its own LLM context.

Whatever an implementation returns, the call handler serializes it to a single JSON text block and sends it back as the tool result. Errors take the same path as success. The handler wraps every dispatch in a try/except, and on failure it returns a small error payload as the content rather than letting the exception escape across the wire.

## Design decisions and why

The server side is deterministic — no LLM runs in-process. Runtime tools wrap pure Python, and skill tools return text. This keeps the server a trustworthy, reproducible substrate. The host agent owns model choice, cost, and every source of non-determinism. It is the same read/write split Tessellum draws everywhere — descriptive retrieval plus prescriptive capture on the server, agent cognition on the far side of the wire — extended out to the tool boundary.

The skill canonical is the prompt. Rather than embedding an LLM to run a procedure, get-skill returns the procedure's text and lets the calling agent execute it. This is what makes the front door composable. Any agent, on any model, can pull a Tessellum skill and run it in its own context, and the server stays LLM-free.

The MCP SDK is imported lazily. Nothing at package-import time depends on the `mcp` library; the SDK is only pulled in when the server is actually built or run. A user who has not installed the `[mcp]` extra must still be able to load the CLI and use every other subcommand, so the optional dependency only materializes when someone runs `serve`.

A missing extra or a bad invocation exits with code 2, never a traceback. If the `[mcp]` extra is absent, both the runner and the CLI catch the import failure, print an actionable `pip install tessellum[mcp]` hint, and return 2. Running the `mcp` group with no sub-subcommand does the same. A missing optional dependency or a misused subcommand is a user-configuration problem, and the interface treats it as one rather than crashing.

Errors are content, not protocol faults. A bad argument or a missing index database degrades to a readable JSON error payload instead of a broken JSON-RPC frame. An agent can read a JSON error and recover or retry; it cannot reason about a corrupted wire frame.

Folgezettel traversal is deliberately naive. It loads the whole graph and scans it linearly per call, matching ancestors and descendants by Folgezettel string prefix and siblings by shared parent. The choice is correctness-first over a graph that is already in memory: no separate Folgezettel index is needed on the MCP path. Sibling matching depends on the parent field being populated on the nodes.

Capture destinations are overridable, not fixed. The capture tool forwards optional destination and filename-prefix overrides to the underlying API, which treats each flavor's registered location as a default rather than a constraint. The calling agent often knows a note's true sub-category better than a static registry can — a model-flavored repository note belongs with code repos, an algorithm note with tools — so it can steer the write.

Only stdio is wired. The stdio transport is the one path implemented today. The `[mcp]` extra also pulls in web-server libraries, but no HTTP or SSE transport exists yet. That is unwired headroom, not a shipped feature.

**Reference:** [reference/mcp.md](reference/mcp.md) — API, symbols, and signatures.
