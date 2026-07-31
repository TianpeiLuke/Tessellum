---
tags:
  - resource
  - documentation
  - hermes_agent
  - dashboard
  - theming
keywords:
  - hermes dashboard theme
  - dashboard-themes YAML
  - 3-layer palette color-mix
  - layoutVariant cockpit
  - componentStyles color overrides
  - customCSS built-in themes
topics:
  - Hermes Agent
  - Web Dashboard
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
access_control_group: ["general"]
---

# Hermes Dashboard Themes

## Overview

A Hermes **dashboard theme** is a drop-in YAML file that repaints the `hermes dashboard` web UI without forking the codebase. Drop a file in `~/.hermes/dashboard-themes/`, refresh, and it appears in the header's theme switcher. Every field is optional — missing keys fall back to the built-in `default` theme, so a theme can be as small as a single color. The theme is the first of the three extension layers the dashboard exposes (themes, UI plugins, backend plugins); this note covers themes only — plugin authoring lives in the [plugins](hermes_dashboard_plugins.md) note and the stable contract in the [extension API](hermes_dashboard_extension_api.md) note.

The heart of a theme is a **3-layer palette** from which the dashboard's design-system cascade derives every shadcn-compatible token (card, popover, muted, border, primary, destructive, ring, …) via CSS `color-mix()`. Overriding three colors cascades into the whole UI. On top of the palette a theme can set typography, layout/density, a `layoutVariant` shell, image `assets` (exposed as CSS vars), per-component chrome via `componentStyles`, explicit `colorOverrides`, and a raw `customCSS` block (capped at 32 KiB). The active selection persists to `config.yaml` under `dashboard.theme` and is restored on reload. Note that the dashboard theme system is **unrelated to the CLI [skin system](hermes_skins_themes.md)** (the page says so explicitly).

## Quick start — your first theme

Create the directory and a minimal two-color theme:

```yaml
# ~/.hermes/dashboard-themes/neon.yaml
name: neon
label: Neon
description: Pure magenta on black

palette:
  background: "#000000"
  midground: "#ff00ff"
```

Refresh the dashboard, click the palette icon in the header, and pick **Neon**. The background goes black, text and accents go magenta, and every derived color (card, border, muted, ring, etc.) is recomputed from that 2-color triplet via `color-mix()` in CSS. That is the whole onboarding: one file, two colors. Everything below is optional refinement. The file name does not matter (the theme's `name:` field is what the system uses), but convention is `<name>.yaml`.

## Palette, typography, layout

These three blocks are the heart of a theme. Each is independent — override one, leave the others.

### Palette (3-layer)

The palette is a triplet of color layers plus a warm-glow vignette color and a noise-grain multiplier. Each layer accepts either `{hex: "#RRGGBB", alpha: 0.0–1.0}` or a bare hex string (alpha defaults to 1.0).

| Key | Description |
|-----|-------------|
| `palette.background` | Deepest canvas color — typically near-black. Drives page background and card fill. |
| `palette.midground` | Primary text and accent. Most UI chrome reads this (foreground text, button outlines, focus rings). |
| `palette.foreground` | Top-layer highlight. The default theme sets this to white at alpha 0 (invisible); themes wanting a bright top accent can raise its alpha. |
| `palette.warmGlow` | `rgba(...)` string used as the vignette color by `<Backdrop />`. |
| `palette.noiseOpacity` | 0–1.2 multiplier on the grain overlay. Lower = softer, higher = grittier. |

### Typography

| Key | Description |
|-----|-------------|
| `fontSans` | CSS font-family stack for body copy (applied to `html`, `body`). |
| `fontMono` | CSS font-family stack for code blocks, `<code>`, `.font-mono` utilities. |
| `fontDisplay` | Optional heading/display stack. Falls back to `fontSans`. |
| `fontUrl` | Optional external stylesheet URL. Injected as `<link rel="stylesheet">` in `<head>` on theme switch; the same URL is never injected twice. Works with Google Fonts, Bunny Fonts, self-hosted `@font-face` sheets. |
| `baseSize` | Root font size — controls the rem scale (e.g. `"14px"`, `"16px"`). |
| `lineHeight` | Default line-height (e.g. `"1.5"`, `"1.65"`). |
| `letterSpacing` | Default letter-spacing (e.g. `"0"`, `"0.01em"`, `"-0.01em"`). |

**Changing the font from the UI (no YAML):** the theme picker has a **Font** section below the theme list. Pick any font there and it overrides the body font of whatever theme is active — the choice is independent of the theme and persists across theme switches (stored in `config.yaml` under `dashboard.font`). Choose **Theme default** to clear the override. The picker offers a curated catalog (system stacks plus Google-Fonts families across sans/serif/mono) and deliberately does **not** accept a free-text font URL, keeping the injected origins fixed. For a fully custom face, set `fontSans` + `fontUrl` in a theme YAML. The theme's `fontMono` (code blocks, terminal) is always left untouched by the UI override.

### Layout

| Key | Values | Description |
|-----|--------|-------------|
| `radius` | any CSS length (`"0"`, `"0.25rem"`, `"0.5rem"`, `"1rem"`, …) | Corner-radius token. Maps to `--radius` and cascades into `--radius-sm/md/lg/xl` — every rounded element shifts together. |
| `density` | `compact` \| `comfortable` \| `spacious` | Spacing multiplier applied as the `--spacing-mul` CSS var. `compact = 0.85×`, `comfortable = 1.0×` (default), `spacious = 1.2×`. Scales Tailwind's base spacing so padding, gap, and space-between utilities all shift proportionally. |

## Layout variants

`layoutVariant` picks the overall shell layout. Defaults to `"standard"` when absent.

| Variant | Behaviour |
|---------|-----------|
| `standard` | Single column, 1600px max-width (default). |
| `cockpit` | Left sidebar rail (260px) + main content. Populated by plugins via the `sidebar` slot. Without a plugin the rail shows a placeholder. |
| `tiled` | Drops the max-width clamp so pages can use the full viewport width. |

The current variant is exposed as `document.documentElement.dataset.layoutVariant`, so raw CSS in `customCSS` can target it via `:root[data-layout-variant="cockpit"] …`.

## Theme assets (images as CSS vars)

Ship artwork URLs with a theme. Each named slot becomes a CSS var (`--theme-asset-<name>`) that the built-in shell and any plugin can read. The `bg` slot is automatically wired into the backdrop; other slots (`hero`, `crest`, `logo`, `sidebar`, `header`, and arbitrary `custom.<name>` keys) are plugin-facing. Values accept bare URLs (wrapped in `url(...)` automatically), pre-wrapped `url(...)` / `linear-gradient(...)` / `radial-gradient(...)` expressions (used as-is), or `"none"` (explicit opt-out). Every asset is also emitted as `--theme-asset-<name>-raw` (the unwrapped URL) in case a plugin needs to pass it to `<img src>` instead of `background-image`. Plugins read these with plain CSS or JS, e.g. `getComputedStyle(document.documentElement).getPropertyValue("--theme-asset-hero").trim()`.

## Component chrome overrides

`componentStyles` restyles individual shell components without writing CSS selectors. Each bucket's entries become CSS vars (`--component-<bucket>-<kebab-property>`) that the shell's shared components read — so `card:` overrides apply to every `<Card>`, `header:` to the app bar, etc. Supported buckets: `card`, `header`, `footer`, `sidebar`, `tab`, `progress`, `badge`, `backdrop`, `page`. Property names use camelCase (`clipPath`) and are emitted as kebab (`clip-path`). Values are plain CSS strings — anything CSS accepts (`clip-path`, `border-image`, `background`, `box-shadow`, `animation`, …).

## Color overrides

Most themes won't need this — the 3-layer palette derives every shadcn token. Use `colorOverrides` when you want a specific accent the derivation won't produce (a softer destructive red for a pastel theme, a specific success green for a brand). Supported keys: `card`, `cardForeground`, `popover`, `popoverForeground`, `primary`, `primaryForeground`, `secondary`, `secondaryForeground`, `muted`, `mutedForeground`, `accent`, `accentForeground`, `destructive`, `destructiveForeground`, `success`, `warning`, `border`, `input`, `ring`. Each key maps 1:1 to the `--color-<kebab>` CSS var (e.g. `primaryForeground` → `--color-primary-foreground`). Any key set here wins over the palette cascade **for the active theme only** — switching to another theme clears the overrides.

## Raw `customCSS`

For selector-level chrome that `componentStyles` can't express — pseudo-elements, animations, media queries, theme-scoped overrides — drop raw CSS into `customCSS`:

```yaml
customCSS: |
  /* Scanline overlay — only visible when cockpit variant is active. */
  :root[data-layout-variant="cockpit"] body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 100;
    background: repeating-linear-gradient(to bottom,
      transparent 0px, transparent 2px,
      rgba(64, 200, 255, 0.035) 3px, rgba(64, 200, 255, 0.035) 4px);
    mix-blend-mode: screen;
  }
```

The CSS is injected as a single scoped `<style data-hermes-theme-css>` tag on theme apply and cleaned up on theme switch. **Capped at 32 KiB per theme.** (If you need more, split across multiple themes or inject a full stylesheet via a plugin's `css` field — no size cap there.)

## Built-in themes

Each built-in ships its own palette, typography, and layout — switching produces visible changes beyond color alone. Themes that reference Google Fonts (all except Hermes Teal) load the stylesheet on demand — the first time you switch to them a `<link>` tag is injected into `<head>`.

| Theme | Palette | Typography | Layout |
|-------|---------|------------|--------|
| **Hermes Teal** (`default`) | Dark teal + cream | System stack, 15px | 0.5rem radius, comfortable |
| **Hermes Teal (Large)** (`default-large`) | Same as default | System stack, 18px, line-height 1.65 | 0.5rem radius, spacious |
| **Midnight** (`midnight`) | Deep blue-violet | Inter + JetBrains Mono, 14px | 0.75rem radius, comfortable |
| **Ember** (`ember`) | Warm crimson + bronze | Spectral (serif) + IBM Plex Mono, 15px | 0.25rem radius, comfortable |
| **Mono** (`mono`) | Grayscale | IBM Plex Sans + IBM Plex Mono, 13px | 0 radius, compact |
| **Cyberpunk** (`cyberpunk`) | Neon green on black | Share Tech Mono everywhere, 14px | 0 radius, compact |
| **Rosé** (`rose`) | Pink + ivory | Fraunces (serif) + DM Mono, 16px | 1rem radius, spacious |

## Full theme YAML reference

Every knob in one file — copy and trim what you don't need. Selection persists to `config.yaml` under `dashboard.theme` and is restored on reload; switch themes live from the header bar by clicking the palette icon.

```yaml
# ~/.hermes/dashboard-themes/ocean.yaml
name: ocean
label: Ocean Deep
description: Deep sea blues with coral accents

# 3-layer palette (accepts {hex, alpha} or bare hex)
palette:
  background:
    hex: "#0a1628"
    alpha: 1.0
  midground:
    hex: "#a8d0ff"
    alpha: 1.0
  foreground:
    hex: "#ffffff"
    alpha: 0.0
  warmGlow: "rgba(255, 107, 107, 0.35)"
  noiseOpacity: 0.7

typography:
  fontSans: "Poppins, system-ui, sans-serif"
  fontMono: "Fira Code, ui-monospace, monospace"
  fontDisplay: "Poppins, system-ui, sans-serif"   # optional
  fontUrl: "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap"
  baseSize: "15px"
  lineHeight: "1.6"
  letterSpacing: "-0.003em"

layout:
  radius: "0.75rem"
  density: comfortable

layoutVariant: standard        # standard | cockpit | tiled

assets:
  bg: "https://example.com/ocean-bg.jpg"
  hero: "/my-images/kraken.png"
  crest: "/my-images/anchor.svg"
  logo: "/my-images/logo.png"
  custom:
    pattern: "/my-images/waves.svg"

componentStyles:
  card:
    boxShadow: "inset 0 0 0 1px rgba(168, 208, 255, 0.18)"
  header:
    background: "linear-gradient(180deg, rgba(10, 22, 40, 0.95), rgba(5, 9, 26, 0.9))"

colorOverrides:
  destructive: "#ff6b6b"
  ring: "#ff6b6b"

customCSS: |
  /* Any additional selector-level tweaks */
```

**Source**: `inbox/hermes_agent_docs/user-guide/features/extending-the-dashboard.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
**Last Updated**: 2026-06-19
**Status**: Active
