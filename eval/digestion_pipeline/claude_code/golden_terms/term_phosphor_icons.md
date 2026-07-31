---
tags: [resource, terminology, developer_tools, frontend]
keywords: ["Phosphor Icons", "Phosphor", "phosphor-icons", "@phosphor-icons/react", "phosphoricons.com", "Phosphor icon family", "Phosphor icon name"]
topics: [icon library, UI components, workspacetool plugins, frontend tooling, open source]
language: markdown
date of note: 2026-06-24
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Phosphor Icons — Open-Source Flexible Icon Family for Interfaces

## Definition

**Phosphor Icons** is an open-source, MIT-licensed icon family for interfaces, diagrams, and presentations, published at [phosphoricons.com](https://phosphoricons.com) and maintained by the Phosphor Icons project. It solves the recurring frontend problem of needing a single, visually consistent set of glyphs that scales across an entire application: every icon is drawn on a 16×16px grid (so it reads well small and scales up cleanly) and is offered in six coordinated **weights** — Thin, Light, Regular, Bold, Fill, and Duotone — so a product can switch emphasis without changing icon families. The catalog is large (over 1,200 named icons and growing) and ships as framework-native packages rather than a single SVG dump, which is why it is a common default for design systems and developer tools.

The family is delivered through an ecosystem of official packages so consumers pick icons the idiomatic way for their stack: `@phosphor-icons/react` (tree-shakeable React components), `@phosphor-icons/web` (a webfont mapping characters to icons via `<i>` tags), plus Vue, Flutter, SwiftUI, Web Components, and a framework-agnostic `@phosphor-icons/core` catalog. Each icon has a stable **PascalCase name** (e.g. `Plug`, `Shield`, `GitPullRequest`) that is consistent across all packages. **workspacetool uses Phosphor as its icon vocabulary: a plugin does not ship icon assets — it names a Phosphor icon by string (e.g. `icon: 'Plug'`) in its panel descriptor, and the workspacetool client resolves that name to the rendered Phosphor glyph throughout the UI.**

## Context

Within the workspacetool (OpenClaw) plugin model, Phosphor is the contract for all plugin-supplied iconography. When a plugin declares a panel from inside `initialize()` as a field on its returned `PluginCapabilities`, the panel descriptor carries a `title`, a Phosphor `icon` name string, and a `contentEndpoint`; the top-bar indicator likewise specifies a default Phosphor `icon` (e.g. `'Shield'`). Because the icon is passed as a plain string name rather than an asset, plugins stay lightweight and the client owns rendering — guaranteeing visual consistency across first-party and third-party plugins. workspacetool plugin code that needs an icon component directly (e.g. a custom mention-provider React surface) imports straight from the React package, as in `import { GitPullRequest } from '@phosphor-icons/react'`.

In the broader ecosystem, Phosphor competes with families like Lucide, Heroicons, and Feather, distinguishing itself by the six-weight design and the breadth of official framework bindings. Its MIT license and component-per-icon tree-shaking make it well suited to TypeScript/React applications like the workspacetool client, where bundle size and a single coherent visual language both matter.

## Key Characteristics

- **Open source, MIT-licensed** — free for commercial and personal use, attributed to Phosphor Icons.
- **Six weights** — Thin, Light, Regular, Bold, Fill, and Duotone, all drawn from the same geometry so weight is an interchangeable axis.
- **16×16px design grid** — icons read well at small sizes and scale up without distortion; raw stroke information is retained for fine-tuning.
- **Large, growing catalog** — over 1,200 named icons; each has a stable PascalCase name consistent across every package.
- **Framework-native packages** — official `@phosphor-icons/react`, `/web` (webfont), `/vue`, `/flutter`, `/swift`, `/webcomponents`, and `/core`, plus Figma/Sketch/Penpot plugins and many community ports (Svelte, SolidJS, etc.).
- **Tree-shakeable React components** — only the imported icons land in the bundle, which matters for client apps like workspacetool.
- **Name-by-string consumption in workspacetool** — plugin panel descriptors and top-bar indicators reference an icon by its Phosphor name; the client resolves and renders it, so plugins ship no icon assets.

## Related Terms


## References

- [Phosphor Icons — Official Site](https://phosphoricons.com) — interactive catalog, weights, and usage.
- [phosphor-icons on GitHub](https://github.com/phosphor-icons/homepage) — project overview, package ecosystem (`@phosphor-icons/react`, `/web`, `/vue`, etc.), and MIT license.
