---
tags:
  - resource
  - documentation
  - hermes_agent
  - plugin_system
  - cli
keywords:
  - hermes plugins management
  - plugins enabled disabled allow-list
  - hermes plugins install update remove
  - interactive plugin toggle UI
  - provider plugin radio picker
  - nixos extraPlugins declarative
topics:
  - Hermes Agent
  - Plugin System
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
access_control_group: ["general"]
---

# Hermes Agent — Managing Plugins

## Overview

This note is the **operational procedure for turning Hermes plugins on and off** — the management half of the [plugin system](hermes_plugins_system.md). Where the system note explains what a plugin *is* (a `register(ctx)` Python extension discovered under `~/.hermes/plugins/`), this note covers the verbs and state model you use day-to-day: the `hermes plugins` interactive UI, the `install`/`update`/`remove`/`enable`/`disable` subcommands, the three plugin states (`enabled` / `disabled` / `not enabled`), the radio pickers that select single-active provider plugins (memory, context engine), and the NixOS declarative path that installs plugins without ever running `hermes plugins install`.

General plugins are **opt-in**: discovery finds them so they appear in the UI, but nothing with hooks or tools loads until the plugin's name is added to `plugins.enabled` in `~/.hermes/config.yaml`. This is the consent gate for arbitrary code dropped into `~/.hermes/plugins/`. Managing a plugin therefore means editing that allow-list — directly, through the CLI, through the interactive screen, or declaratively via Nix.

## The opt-in allow-list and the three toggle commands

General plugins and user-installed backends are disabled by default. Discovery still surfaces them (they show up in `hermes plugins` and `/plugins`), but they only load once their name is added to `plugins.enabled`:

```yaml
plugins:
  enabled:
    - my-tool-plugin
    - disk-cleanup
  disabled:       # optional deny-list — always wins if a name appears in both
    - noisy-plugin
```

There are three ways to flip a plugin's state:

```bash
hermes plugins                    # interactive toggle (space to check/uncheck)
hermes plugins enable <name>      # add to allow-list
hermes plugins disable <name>     # remove from allow-list + add to disabled
```

After `hermes plugins install owner/repo`, you're asked `Enable 'name' now? [y/N]` — defaulting to no. For scripted, non-interactive installs, skip the prompt with `--enable` or `--no-enable`.

## The `hermes plugins` command set

The full CLI verb set for installing and lifecycle-managing plugins:

```bash
hermes plugins                               # unified interactive UI
hermes plugins list                          # table: enabled / disabled / not enabled
hermes plugins install user/repo             # install from Git, then prompt Enable? [y/N]
hermes plugins install user/repo --enable    # install AND enable (no prompt)
hermes plugins install user/repo --no-enable # install but leave disabled (no prompt)
hermes plugins update my-plugin              # pull latest
hermes plugins remove my-plugin              # uninstall
hermes plugins enable my-plugin              # add to allow-list
hermes plugins disable my-plugin             # remove from allow-list + add to disabled
```

`install` clones the plugin from a Git source into the user plugins directory; `update` pulls the latest from that source; `remove` uninstalls it. `enable`/`disable` only edit the allow-list and deny-list and do not touch the on-disk plugin files.

## Interactive UI

Running `hermes plugins` with no arguments opens a composite interactive screen:

```
Plugins
  ↑↓ navigate  SPACE toggle  ENTER configure/confirm  ESC done

  General Plugins
 → [✓] my-tool-plugin — Custom search tool
   [ ] webhook-notifier — Event hooks
   [ ] disk-cleanup — Auto-cleanup of ephemeral files [bundled]

  Provider Plugins
     Memory Provider          ▸ honcho
     Context Engine           ▸ compressor
```

The screen has two sections with distinct interaction models:

- **General Plugins section** — checkboxes toggled with SPACE. Checked = in `plugins.enabled`; unchecked = in `plugins.disabled` (explicit off). Bundled plugins appear in the same list with a `[bundled]` tag.
- **Provider Plugins section** — shows the current selection. Press ENTER to drill into a radio picker where you choose the single active provider. These are the single-select [provider plugins](hermes_plugins_system.md) (memory, context engine) — only one of each can be active.

Provider-plugin selections are written to `config.yaml` as scalar keys, not allow-list entries:

```yaml
memory:
  provider: "honcho"      # empty string = built-in only

context:
  engine: "compressor"    # default built-in compressor
```

## Enabled vs. disabled vs. neither

Every plugin occupies exactly one of three states:

| State | Meaning | In `plugins.enabled`? | In `plugins.disabled`? |
|---|---|---|---|
| `enabled` | Loaded on next session | Yes | No |
| `disabled` | Explicitly off — won't load even if also in `enabled` | (irrelevant) | Yes |
| `not enabled` | Discovered but never opted in | No | No |

The deny-list always wins: a name appearing in both `enabled` and `disabled` stays off. The default for a newly-installed or bundled plugin is `not enabled`. `hermes plugins list` distinguishes all three states so you can tell what was explicitly turned off versus what is merely waiting to be enabled. In a running session, `/plugins` shows which plugins are currently loaded.

## NixOS declarative plugins

On NixOS, plugins can be installed declaratively through the module options — no `hermes plugins install` step is needed. (See the Nix Setup guide for the full module reference.)

```nix
services.hermes-agent = {
  # Directory plugin (source tree with plugin.yaml)
  extraPlugins = [ (pkgs.fetchFromGitHub { ... }) ];
  # Entry-point plugin (pip package)
  extraPythonPackages = [ (pkgs.python312Packages.buildPythonPackage { ... }) ];
  # Enable in config
  settings.plugins.enabled = [ "my-plugin" ];
};
```

`extraPlugins` takes directory-style plugins (a source tree carrying a `plugin.yaml`); `extraPythonPackages` takes entry-point (pip-distributed) plugins; `settings.plugins.enabled` opts them into the same allow-list. Declarative plugins are symlinked with a `nix-managed-` prefix so they coexist with manually installed plugins and are cleaned up automatically when removed from the Nix config.

**Source**: `inbox/hermes_agent_docs/user-guide/features/plugins.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
**Last Updated**: 2026-06-19
**Status**: Active
