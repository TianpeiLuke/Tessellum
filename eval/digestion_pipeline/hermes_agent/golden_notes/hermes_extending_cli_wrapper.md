---
tags:
  - resource
  - documentation
  - hermes_agent
  - developer_guide
  - cli_extension
keywords:
  - extending the cli
  - wrapper cli
  - hermescli extension hooks
  - extra tui widgets
  - tui keybindings
  - process_command
topics:
  - Hermes Agent
  - Developer Guide
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli
access_control_group: ["general"]
---

# Extending the CLI: Wrapper CLIs

## Overview

This is the procedure for building a **wrapper CLI** on top of Hermes' `HermesCLI` class — a subclass that adds custom TUI widgets, keybindings, and layout customizations **without overriding the 1000+ line `run()` method**. Hermes exposes a small set of *protected extension hooks* on `HermesCLI` precisely so that an extension stays decoupled from internal changes to the run loop: you subclass `HermesCLI`, override one or more hooks, and the existing `run()` calls your overrides at the right points. The extension model is classic OOP inheritance plus template-method extension — `run()` is the invariant template, the protected hooks are the overridable seams. There are **five extension seams**: three new protected hooks (`_get_extra_tui_widgets`, `_register_extra_tui_keybindings`, `_build_tui_layout_children`) and two that already existed (`process_command`, `_build_tui_style_dict`). State the wrapper reads — `self.agent`, `self.model`, `self.conversation_history` — is available on the instance, and `self._invalidate()` triggers a prompt_toolkit redraw after a state change.

## Extension points

There are five extension seams available on `HermesCLI`:

| Hook | Purpose | Override when... |
|------|---------|------------------|
| `_get_extra_tui_widgets()` | Inject widgets into the layout | You need a persistent UI element (panel, status line, mini-player) |
| `_register_extra_tui_keybindings(kb, *, input_area)` | Add keyboard shortcuts | You need hotkeys (toggle panels, transport controls, modal shortcuts) |
| `_build_tui_layout_children(**widgets)` | Full control over widget ordering | You need to reorder or wrap existing widgets (rare) |
| `process_command()` | Add custom slash commands | You need `/mycommand` handling (pre-existing hook) |
| `_build_tui_style_dict()` | Custom prompt_toolkit styles | You need custom colors or styling (pre-existing hook) |

The first three are new protected hooks; the last two already existed.

## Quick start: a wrapper CLI

A minimal `MyCLI` subclasses `HermesCLI`, overrides three hooks (extra widget, F2 keybinding, `/panel` slash command), and calls the inherited `run()` unchanged:

```python
#!/usr/bin/env python3
"""my_cli.py — Example wrapper CLI that extends Hermes."""

from cli import HermesCLI
from prompt_toolkit.layout import FormattedTextControl, Window
from prompt_toolkit.filters import Condition


class MyCLI(HermesCLI):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._panel_visible = False

    def _get_extra_tui_widgets(self):
        """Add a toggleable info panel above the status bar."""
        cli_ref = self
        return [
            Window(
                FormattedTextControl(lambda: "📊 My custom panel content"),
                height=1,
                filter=Condition(lambda: cli_ref._panel_visible),
            ),
        ]

    def _register_extra_tui_keybindings(self, kb, *, input_area):
        """F2 toggles the custom panel."""
        cli_ref = self

        @kb.add("f2")
        def _toggle_panel(event):
            cli_ref._panel_visible = not cli_ref._panel_visible

    def process_command(self, cmd: str) -> bool:
        """Add a /panel slash command."""
        if cmd.strip().lower() == "/panel":
            self._panel_visible = not self._panel_visible
            state = "visible" if self._panel_visible else "hidden"
            print(f"Panel is now {state}")
            return True
        return super().process_command(cmd)


if __name__ == "__main__":
    cli = MyCLI()
    cli.run()
```

Run it from the installed Hermes venv:

```bash
cd ~/.hermes/hermes-agent
source .venv/bin/activate
python my_cli.py
```

## Hook reference

**`_get_extra_tui_widgets()`** returns a list of prompt_toolkit widgets to insert into the TUI layout. Widgets appear **between the spacer and the status bar** — above the input area but below the main output. The default returns `[]`. Each widget should be a prompt_toolkit container (e.g. `Window`, `ConditionalContainer`, `HSplit`); wrap it in `ConditionalContainer` or pass `filter=Condition(...)` to make it toggleable.

**`_register_extra_tui_keybindings(kb, *, input_area)`** is called after Hermes registers its own keybindings and before the layout is built — add your bindings to `kb`. Parameters: `kb` is the `KeyBindings` instance for the prompt_toolkit application; `input_area` is the main `TextArea` widget, available if you need to read or manipulate user input.

```python
def _register_extra_tui_keybindings(self, kb, *, input_area):
    cli_ref = self

    @kb.add("f3")
    def _clear_input(event):
        input_area.text = ""

    @kb.add("f4")
    def _insert_template(event):
        input_area.text = "/search "
```

**Avoid conflicts** with built-in keybindings: `Enter` (submit), `Escape Enter` (newline), `Ctrl-C` (interrupt), `Ctrl-D` (exit), `Tab` (auto-suggest accept). Function keys F2+ and Ctrl-combinations are generally safe.

**`_build_tui_layout_children(**widgets)`** should be overridden **only** when you need full control over widget ordering — most extensions should use `_get_extra_tui_widgets()` instead. It receives all the layout widgets (`sudo_widget`, `secret_widget`, `approval_widget`, `clarify_widget`, `model_picker_widget`, `spinner_widget`, `spacer`, `status_bar`, `input_rule_top`, `image_bar`, `input_area`, `input_rule_bot`, `voice_status_bar`, `completions_menu`) and returns an ordered list (any `None` widgets are filtered out). The default implementation places `*self._get_extra_tui_widgets()` between the `spacer` and the `status_bar`:

```python
[
    Window(height=0),       # anchor
    sudo_widget,            # sudo password prompt (conditional)
    secret_widget,          # secret input prompt (conditional)
    approval_widget,        # dangerous command approval (conditional)
    clarify_widget,         # clarify question UI (conditional)
    model_picker_widget,    # model picker overlay (conditional)
    spinner_widget,         # thinking spinner (conditional)
    spacer,                 # fills remaining vertical space
    *self._get_extra_tui_widgets(),  # YOUR WIDGETS GO HERE
    status_bar,             # model/token/context status line
    input_rule_top,         # ─── border above input
    image_bar,              # attached images indicator
    input_area,             # user text input
    input_rule_bot,         # ─── border below input
    voice_status_bar,       # voice mode status (conditional)
    completions_menu,       # autocomplete dropdown
]
```

## Layout diagram

The default layout from top to bottom: (1) **Output area** — scrolling conversation history; (2) **Spacer**; (3) **Extra widgets** — from `_get_extra_tui_widgets()`; (4) **Status bar** — model, context %, elapsed time; (5) **Image bar** — attached image count; (6) **Input area** — user prompt; (7) **Voice status** — recording indicator; (8) **Completions menu** — autocomplete suggestions. Your extra widgets land at slot 3, between the spacer and the status bar.

## Tips

- **Invalidate the display** after state changes: call `self._invalidate()` to trigger a prompt_toolkit redraw.
- **Access agent state**: `self.agent`, `self.model`, and `self.conversation_history` are all available on the instance.
- **Custom styles**: override `_build_tui_style_dict()` and add entries for your custom style classes.
- **Slash commands**: override `process_command()`, handle your commands, and call `super().process_command(cmd)` for everything else.
- **Don't override `run()`** unless absolutely necessary — the extension hooks exist specifically to avoid that coupling.

**Source**: `inbox/hermes_agent_docs/developer-guide/extending-the-cli.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli
**Last Updated**: 2026-06-19
**Status**: Active
