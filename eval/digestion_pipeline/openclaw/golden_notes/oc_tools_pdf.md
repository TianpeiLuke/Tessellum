---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - pdf
keywords:
  - openclaw pdf tool
  - pdf native provider mode
  - pdf extraction fallback
  - pdfModel resolution chain
  - clawpdf pdfium webassembly
  - document-extract plugin
  - pdfMaxPages pdfMaxBytesMb
  - unsupported_pdf_reference too_many_pdfs
topics:
  - OpenClaw
  - PDF Tool
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/pdf
access_control_group: ["general"]
---

# OpenClaw — The `pdf` Document-Analysis Tool

## Overview

This note documents the OpenClaw `pdf` agent tool, which analyzes one or more PDF documents and returns text. It mirrors the `tools/pdf` source page end to end: the auth-aware model-availability resolution chain that decides whether the tool is even exposed, the input parameters (`pdf` / `pdfs` / `prompt` / `pages` / `password` / `model` / `maxBytesMb`), the supported PDF reference schemes and their rejections, the two execution modes (native provider vs extraction fallback), the `agents.defaults` config keys, the structured `details` output, the error behavior, and the worked examples. The tool supports single (`pdf`) or multi (`pdfs`) input, with a maximum of 10 PDFs per call.

## Availability

The tool is only registered when OpenClaw can resolve a PDF-capable model config for the agent. The resolution chain is:

1. `agents.defaults.pdfModel`
2. fallback to `agents.defaults.imageModel`
3. fallback to the agent's resolved session/default model
4. if native-PDF providers are auth-backed, prefer them ahead of generic image fallback candidates

If no usable model can be resolved, the `pdf` tool is not exposed. The fallback chain is **auth-aware**: a configured `provider/model` only counts if OpenClaw can actually authenticate that provider for the agent. The native PDF providers are currently **Anthropic** and **Google**. If the resolved session/default provider already has a configured vision/PDF model, the PDF tool reuses that before falling back to other auth-backed providers.

## Input reference

The tool accepts the following parameters (verbatim from source):

- `pdf` (`string`) — One PDF path or URL.
- `pdfs` (`string[]`) — Multiple PDF paths or URLs, up to 10 total.
- `prompt` (`string`, default `"Analyze this PDF document."`) — Analysis prompt.
- `pages` (`string`) — Page filter like `1-5` or `1,3,7-9`.
- `password` (`string`) — Password for encrypted PDFs in extraction fallback mode.
- `model` (`string`) — Optional model override in `provider/model` form.
- `maxBytesMb` (`number`) — Per-PDF size cap in MB. Defaults to `agents.defaults.pdfMaxBytesMb` or `10`.

Input notes from the source: `pdf` and `pdfs` are merged and deduplicated before loading; if no PDF input is provided, the tool errors; `pages` is parsed as 1-based page numbers, deduped, sorted, and clamped to the configured max pages; `password` applies to every PDF in the request and is only used by extraction fallback mode; `maxBytesMb` defaults to `agents.defaults.pdfMaxBytesMb` or `10`.

## Supported PDF references

The tool accepts these reference forms:

- local file path (including `~` expansion)
- `file://` URL
- `http://` and `https://` URL
- OpenClaw-managed inbound refs such as `media://inbound/<id>`

Reference rules: other URI schemes (for example `ftp://`) are rejected with `unsupported_pdf_reference`. In sandbox mode, remote `http(s)` URLs are rejected. With workspace-only file policy enabled, local file paths outside allowed roots are rejected, but managed inbound refs and replayed paths under OpenClaw's inbound media store are allowed with workspace-only file policy.

## Execution modes

### Native provider mode

Native mode is used for provider `anthropic` and `google`. The tool sends raw PDF bytes directly to provider APIs. Native mode limits: `pages` is not supported (if set, the tool returns an error); `password` is not supported (use a non-native model to analyze encrypted PDFs); multi-PDF input is supported, with each PDF sent as a native document block / inline PDF part before the prompt.

### Extraction fallback mode

Fallback mode is used for non-native providers. The flow is:

1. Extract text from selected pages (up to `agents.defaults.pdfMaxPages`, default `20`).
2. If extracted text length is below `200` chars, render selected pages to PNG images and include them.
3. Send extracted content plus prompt to the selected model.

Fallback details: page image extraction uses a pixel budget of `4,000,000`; encrypted PDFs can be opened with the top-level `password` parameter; if the target model does not support image input and there is no extractable text, the tool errors; if text extraction succeeds but image extraction would require vision on a text-only model, OpenClaw drops the rendered images and continues with the extracted text. Extraction fallback uses the bundled `document-extract` plugin, which owns `clawpdf` — the component that provides text extraction and image rendering through PDFium WebAssembly.

## Config

PDF defaults are set under `agents.defaults` (json5):

```json5
{
  agents: {
    defaults: {
      pdfModel: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["openai/gpt-5.4-mini"],
      },
      pdfMaxBytesMb: 10,
      pdfMaxPages: 20,
    },
  },
}
```

See the Configuration Reference (linked under References) for full field details.

## Output details

The tool returns text in `content[0].text` and structured metadata in `details`. Common `details` fields:

- `model` — resolved model ref (`provider/model`)
- `native` — `true` for native provider mode, `false` for fallback
- `attempts` — fallback attempts that failed before success

Path fields: single PDF input populates `details.pdf`; multiple PDF inputs populate `details.pdfs[]` with `pdf` entries; sandbox path rewrite metadata (when applicable) is recorded under `rewrittenFrom`.

## Error behavior

- **Missing PDF input** — throws `pdf required: provide a path or URL to a PDF document`.
- **Too many PDFs** — returns a structured error in `details.error = "too_many_pdfs"`.
- **Unsupported reference scheme** — returns `details.error = "unsupported_pdf_reference"`.
- **Native mode with `pages`** — throws a clear `pages is not supported with native PDF providers` error.

## Examples

Single PDF:

```json
{
  "pdf": "/tmp/report.pdf",
  "prompt": "Summarize this report in 5 bullets"
}
```

Multiple PDFs:

```json
{
  "pdfs": ["/tmp/q1.pdf", "/tmp/q2.pdf"],
  "prompt": "Compare risks and timeline changes across both documents"
}
```

Page-filtered fallback model (the `pages` filter and `model` override route to extraction fallback):

```json
{
  "pdf": "https://example.com/report.pdf",
  "pages": "1-3,7",
  "model": "openai/gpt-5.4-mini",
  "prompt": "Extract only customer-impacting incidents"
}
```

An encrypted-PDF example uses the top-level `password` plus a non-native `model` so extraction fallback mode handles decryption (native providers do not support `password`).

**Source**: OpenClaw documentation — `tools/pdf` (mirror `inbox/openclaw_docs/tools/pdf.md`)
**Last Updated**: 2026-06-22
**Status**: Active
