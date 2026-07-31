---
tags:
  - resource
  - terminology
  - developer_tools
  - frontend
keywords:
  - Lexical
  - lexical.dev
  - Lexical framework
  - Lexical editor
  - LexicalComposer
  - LexicalTypeaheadMenuPlugin
  - MentionNode
  - rich text editor framework
  - contentEditable
topics:
  - Text Editing Frameworks
  - Frontend Development
  - Rich Text Editing
language: markdown
date of note: 2026-06-24
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Lexical — Extensible Text Editor Framework (Meta)

## Definition

**Lexical** is an extensible, open-source JavaScript framework, created by Meta (lexical.dev), for building rich-text editing experiences in web applications. It exists to remove the well-known difficulty of working directly against the browser's `contentEditable` element and the raw DOM — a notoriously inconsistent, edge-case-laden surface — by interposing a declarative, reliable, and accessible programming model. Rather than mutating the DOM imperatively, developers describe the document as a tree of **nodes** held in an immutable **EditorState**; Lexical's reconciler then diffs the pending state against the current one and applies only the minimal DOM changes (analogous to a virtual DOM, but able to skip much of the diffing because it already knows what mutated). The core is small (roughly 22 kB min+gzip) and dependency-free, with extensibility delivered through lazy-loadable plugins so applications "pay only for what they use." Lexical powers editing surfaces across Meta's products (Facebook, Workplace, Messenger, WhatsApp, Instagram), and is widely adopted outside Meta for chat composers, comment boxes, and document editors.

## Context

Lexical sits in the **frontend / developer-tooling** layer of any product that needs structured text input. A typical integration wraps the editor in a `LexicalComposer`, and an @mention picker is a thin contract layered over Lexical's `LexicalTypeaheadMenuPlugin` — plugins register a custom `MentionNode` in the composer's `nodes` array, supply a trigger matcher (e.g. `useBasicTypeaheadTriggerMatch('@')`), and provide `onQueryChange` / `onSelectOption` callbacks to populate and resolve the menu.

In the broader ecosystem, Lexical is the successor to Meta's earlier **Draft.js** editor and competes with frameworks such as ProseMirror, Slate, and TipTap. It is framework-agnostic at its core, with official React bindings shipped as `@lexical/react` (the package that provides `LexicalComposer`, plugin components, and node helpers), and is distributed via npm.

## Key Characteristics

- **Extensible and modular** — a small dependency-free core (~22 kB min+gzip) plus lazy-loadable plugins; applications include only the features they use.
- **Immutable EditorState** — the document is an immutable tree of nodes plus a selection object, fully serializable to and from JSON, enabling reliable undo/redo, collaboration, and persistence.
- **DOM reconciler** — diffs pending vs. current state and applies minimal DOM mutations (virtual-DOM-like), and handles LTR/RTL text direction automatically.
- **`$`-prefixed read/update API** — state is read or mutated only inside `editor.read()` / `editor.update()` closures using `$`-prefixed helper functions (e.g. `$getRoot()`, `$createTextNode()`), conceptually similar to React Hooks requiring an active context.
- **Listeners, node transforms, and commands** — registered via `register`-prefixed methods that return unsubscribe functions; commands form a priority-ordered messaging system created with `createCommand()`.
- **Custom nodes** — applications define bespoke node classes (e.g. an inline `MentionNode`, decorator nodes that render React components) and register them in `initialConfig.nodes`.
- **`LexicalTypeaheadMenuPlugin`** — a React plugin that powers autocomplete menus triggered by a sentinel character (`@` for mentions, `:` for emoji), positioning the menu at the trigger location and inserting a node on selection.
- **Reliable, accessible, performant** — the three stated design priorities; web-only today, with native ports under exploration.
- **Framework-agnostic core** — usable standalone, with official React bindings (`@lexical/react`); distributed via npm.

## References

- [Lexical — Overview (lexical.dev)](https://lexical.dev/docs/intro)
- [Lexical React Plugins (lexical.dev)](https://lexical.dev/docs/react/plugins)
- [Lexical GitHub repository (facebook/lexical)](https://github.com/facebook/lexical)
- [Lexical (text editor) — Wikipedia](https://en.wikipedia.org/wiki/Lexical_(text_editor))
