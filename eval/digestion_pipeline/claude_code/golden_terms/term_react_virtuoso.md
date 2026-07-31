---
tags:
  - resource
  - terminology
  - frontend
  - ui_rendering
keywords:
  - React Virtuoso
  - Virtuoso
  - react-virtuoso
  - list virtualization
  - windowed rendering
  - firstItemIndex
  - virtualized list
  - windowing
  - GroupedVirtuoso
  - TableVirtuoso
  - VirtuosoGrid
topics:
  - frontend
  - list virtualization
language: markdown
date of note: 2026-06-24
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# React Virtuoso — React Virtualization Library for Lists, Grids, Tables, and Chat

## Definition

**React Virtuoso** (npm package `react-virtuoso`, docs at virtuoso.dev) is an open-source, MIT-licensed React component library for **list, grid, and table virtualization** — the technique of rendering only the items currently visible in the viewport (plus a small overscan buffer) instead of mounting the entire dataset into the DOM. This **windowed rendering** keeps the DOM node count bounded regardless of collection size, so a feed of thousands of rows scrolls smoothly without the layout, paint, and memory cost of materializing every row. Its distinguishing capability versus older virtualization libraries is that **variable-sized items work automatically**: Virtuoso measures rendered items at runtime via `ResizeObserver` and reconciles scroll geometry on its own, so callers do not pre-measure rows or hard-code heights. Authored by Petyo Ivanov (`@petyosi`) and written almost entirely in TypeScript, it ships a family of components — `Virtuoso` (flat list), `GroupedVirtuoso` (sticky group headers driven by a `groupCounts` array), `TableVirtuoso` (virtualized HTML `<table>`), `VirtuosoGrid` (uniform grid cells), plus Masonry and a commercially-licensed `VirtuosoMessageList` for chat UIs.

## Context

Virtuoso's client-side loading can follow a progressive *window-then-backfill* model: render the newest slice immediately, then background-fetch the remainder. The pivotal Virtuoso feature for that pattern is the **`firstItemIndex`** prop — a logical index assigned to the first rendered item. To prepend older history (earlier messages or older items) to the top of a list, the caller *decreases* `firstItemIndex` by the number of items being prepended; Virtuoso then inserts the new items above the current ones while holding the viewport on the same item, so backfilling history never causes a visible scroll jump.

Virtuoso's virtualization also imposes a documented **CSS caveat** for anyone authoring custom item styling: because only visible items exist in the DOM at any moment and items are recycled as the user scrolls, CSS that targets specific item indices (`:nth-child`) is unreliable, `display: none` on item containers can corrupt Virtuoso's height measurements and cause scroll jumps (prefer `visibility: hidden` or `opacity: 0` with `pointer-events: none`), and scroll-related CSS (`overflow`, `max-height`) on the list containers can conflict with Virtuoso's own scroll management.

In the broader frontend ecosystem, React Virtuoso competes with `react-window` and `react-virtualized` (Brian Vaughn) and `@tanstack/react-virtual`. Its differentiator is the zero-configuration handling of dynamic, unknown-height content, which makes it a common choice for chat transcripts, comment threads, infinite feeds, and large data tables.

## Key Characteristics

- **Windowed rendering** — only viewport-visible items (plus overscan) are mounted to the DOM; node count stays bounded as the dataset grows. The number of DOM rows is approximately $\lceil h_{viewport} / h_{item} \rceil + k_{overscan}$ rather than $N$.
- **Automatic variable-height measurement** — items are measured at runtime with `ResizeObserver`; no manual measurement, no hard-coded row heights, no `itemSize` callback required.
- **`firstItemIndex` for stable prepend** — assign a logical index to the first item and decrease it by the prepend count to add older items at the top without shifting the visible scroll position (the core mechanic for chat history and infinite-scroll-up).
- **Bi-directional / endless scrolling** — `startReached` and `endReached` callbacks plus initial-scroll-location support enable load-on-demand in both directions.
- **Component family** — `Virtuoso` (flat list via `totalCount` + `itemContent`), `GroupedVirtuoso` (sticky headers via `groupCounts`), `TableVirtuoso` (HTML tables), `VirtuosoGrid` (uniform grid), Masonry, and the commercial `VirtuosoMessageList`.
- **Imperative scroll control** — `scrollToIndex`, sticky/pinned top items, and custom header/footer/empty-list slots.
- **MIT licensed, TypeScript-first** — core package is open source; only `VirtuosoMessageList` carries a commercial license.

## Related Terms


## References

- React Virtuoso official documentation: https://virtuoso.dev/
- React Virtuoso GitHub repository (petyosi/react-virtuoso, MIT): https://github.com/petyosi/react-virtuoso
- React Virtuoso — prepending items with `firstItemIndex`: https://virtuoso.dev/prepend-items/
- `react-virtuoso` on npm: https://www.npmjs.com/package/react-virtuoso
