---
tags:
  - resource
  - terminology
  - javascript
  - frontend
keywords:
  - React.js
  - React
  - ReactJS
  - React library
  - component-based UI
  - JSX
  - React hooks
  - useState
  - useEffect
  - useRef
  - virtual DOM
  - single-page app
topics:
  - frontend development
  - user interface
  - JavaScript library
language: markdown
date of note: 2026-06-24
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# React.js — JavaScript Library for Building User Interfaces

## Definition

**React.js** (commonly just **React**, also **ReactJS**) is a free, open-source front-end **JavaScript library** for building user interfaces out of reusable **components**. It is **declarative** — a developer describes what the UI should look like for a given application state, and React handles efficiently updating and rendering the right pieces when the underlying data changes. React solves the problem of keeping a complex, stateful UI in sync with changing data: rather than manually mutating the DOM, the developer composes components (JavaScript functions that return markup) and lets React reconcile changes against an in-memory **virtual DOM**, updating only the parts that actually changed. It was created by Jordan Walke at Facebook and open-sourced in 2013; it is maintained today by **Meta** together with a large community of developers and companies, and is one of the most widely used UI libraries on the web. A key clarification: React is a *library* focused on the UI/rendering layer, **not** a full framework — routing, data fetching, and build tooling are typically supplied by adjacent tools (e.g., Next.js, bundlers, REST/WebSocket clients).

Here, React.js is most relevant as the technology behind the **workspacetool client** — workspacetool's browser-facing single-page app is a React 18 SPA (a Slack-like rooms/threads/messages chat surface). The client composes roughly 200 components and 57 hooks around a large `App.tsx` orchestrator, using built-in hooks such as `useState`, `useEffect`, and `useRef` to manage WebSocket connection state, panel layout, and streaming agent output, and talking to the Express/ACP server over a REST `api.ts` client plus a WebSocket connection. **React.js (the UI library) is entirely distinct from `ReAct` (Reasoning + Acting), the agentic-reasoning prompting paradigm** captured separately in this documentation set — they share an acronym/spelling but are unrelated.

## Context

workspacetool's `src/client` module is the canonical internal consumer of React.js documented here. It is built with **React 18** and **TypeScript** (`.tsx`), structured as a single-page application: an `index.tsx` React root bootstraps from URL-hash/localStorage init params, mounts `App.tsx` (the orchestrator that owns rooms/threads state and WebSocket lifecycle), and renders a tree of `components/` (compose box, command palette, sidebar, thread/message panels, tool-call cards, a Monaco/xterm code editor, and an `@xyflow/react` workflow-graph editor) driven by `hooks/` such as `useWebSocket`, `useRooms`, and `useThreads`. This maps directly onto React's core model — components for structure/appearance, hooks for state and side effects, props for parent-to-child data flow, and JSX for markup.

More broadly, React.js sits in the JavaScript front-end ecosystem alongside the [Node.js](term_node_js.md) runtime (used for tooling and server-side rendering), [TypeScript](term_typescript.md) (the typed superset most large React codebases including workspacetool adopt), and [npm](term_npm.md) (the package manager that distributes React and its ecosystem libraries). Client-side React apps consume backend data over [REST](term_rest.md)-style APIs and real-time channels such as [WebSocket](term_websocket.md), and are typically served as static assets behind a CDN such as [CloudFront](term_cloudfront.md).

## Key Characteristics

- **Component-based**: UIs are built by creating and nesting reusable components — JavaScript/TypeScript functions that return JSX markup. A component can be as small as a button or as large as a whole page.
- **Declarative**: The developer describes the UI for each state; React computes and applies the minimal set of changes ("properties flow down, actions flow up").
- **JSX**: An optional but near-universal syntax extension that embeds HTML-like markup in JavaScript; curly braces `{ }` escape back into JavaScript expressions. Compiles to plain JavaScript.
- **Virtual DOM + reconciliation**: React diffs an in-memory representation against the real DOM and updates only changed nodes, avoiding expensive full re-renders.
- **State and props**: `useState` lets a component "remember" data and re-render on change; `props` pass data from parent to child, enabling "lifting state up" to a common ancestor.
- **Hooks**: Functions prefixed with `use` (e.g., `useState`, `useEffect`, `useRef`, `useContext`) let function components hook into state and lifecycle. Introduced in React 16.8 (2019). They must be called at the top level of a component, not inside conditionals or loops.
- **Unidirectional data flow**: One-way binding makes state changes predictable and easier to debug than two-way binding.
- **Library, not framework**: Focused on the view layer; routing, data fetching, and bundling come from companion tools (Next.js, bundlers, API clients).
- **Beyond the web**: The same component model powers native mobile apps via React Native and server-rendered apps via frameworks like Next.js.

## Related Terms


## References

- [React – The library for web and native user interfaces (react.dev)](https://react.dev/)
- [Quick Start (react.dev/learn)](https://react.dev/learn)
- [React (software) — Wikipedia](https://en.wikipedia.org/wiki/React_(software))
- [React on GitHub (facebook/react)](https://github.com/facebook/react)
