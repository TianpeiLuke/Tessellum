---
tags:
  - resource
  - documentation
  - claude_code
  - setup
  - installation
keywords:
  - advanced installation
  - install specific version
  - linux package managers
  - signed apt dnf apk repository
  - npm global install
  - optional dependency
  - binary integrity
  - gpg manifest signature
  - code signing
topics:
  - Claude Code
  - Setup
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/setup
access_control_group: ["general"]
---

# Claude Code — Advanced Installation Options and Binary Verification

## Overview

The advanced installation options cover four needs beyond the recommended native install: pinning a **specific version** (or channel) at install time, installing through signed **Linux package managers** (apt, dnf, apk), installing as a **global npm package**, and verifying **binary integrity and code signing** before trusting the binary. These are procedures for version-pinned, reproducible, and supply-chain-verified installs of Claude Code. Version pinning, channel selection, and managed enforcement of update floors are documented separately in [Update and Release Channels](cc_update_and_release_channels.md); first-time install and platform requirements are in [Install Claude Code](cc_install.md).

This note inlines one representative command per method to stay within the code-block cap; the full per-platform variant set (Windows PowerShell/CMD forms, latest-channel repository URLs, per-OS checksum commands) lives on the source page.

## Install a Specific Version

The native installer accepts either a specific version number or a release channel (`latest` or `stable`). The channel you choose at install time becomes your default for auto-updates. To install the latest version (the default), run the standard install one-liner. To install the stable version on macOS, Linux, or WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash -s stable
```

To install a specific version number, pass it the same way:

```bash
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
```

Windows PowerShell uses a script-block form (`& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable`) and Windows CMD passes the argument to the downloaded `install.cmd` — see the source page for those variants. Release-channel selection and how the install-time choice interacts with auto-updates are covered in [Update and Release Channels](cc_update_and_release_channels.md).

## Install with Linux Package Managers

Claude Code publishes **signed** apt, dnf, and apk repositories. Each repository offers two channels: `stable` serves a version that is typically about one week old, skipping releases with major regressions, and `latest` serves every release as soon as it ships. Package manager installations do **not** auto-update through Claude Code; updates arrive through your normal system upgrade workflow. All repositories are signed with the Claude Code release signing key, and you must verify that key before trusting it.

The apt example (Debian and Ubuntu) configures the `stable` channel:

```bash
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
  -o /etc/apt/keyrings/claude-code.asc
echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
  | sudo tee /etc/apt/sources.list.d/claude-code.list
sudo apt update
sudo apt install claude-code
```

Verify the GPG key fingerprint before trusting it: `gpg --show-keys /etc/apt/keyrings/claude-code.asc` should report `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`. Upgrade later with `sudo apt update && sudo apt upgrade claude-code`.

The **dnf** path (Fedora and RHEL) writes a `/etc/yum.repos.d/claude-code.repo` file with `gpgcheck=1` and `gpgkey=https://downloads.claude.ai/keys/claude-code.asc`; dnf downloads the key on first install and prompts you to confirm the same fingerprint. The **apk** path (Alpine) fetches `claude-code.rsa.pub` into `/etc/apk/keys/`, adds the repository line, and is verified with `sha256sum` reporting `395759c1f7449ef4cdef305a42e820f3c766d6090d142634ebdb049f113168b6`. Switching to the `latest` channel changes both the URL path and the suite name; the full apt/dnf/apk commands and latest-channel URLs are on the source page.

## Install with npm

You can also install Claude Code as a global npm package. The package requires Node.js 18 or later:

```bash
npm install -g @anthropic-ai/claude-code
```

The npm package installs the **same native binary** as the standalone installer. npm pulls the binary in through a per-platform **optional dependency** such as `@anthropic-ai/claude-code-darwin-arm64`, and a postinstall step links it into place. The installed `claude` binary does not itself invoke Node. Supported npm install platforms are `darwin-arm64`, `darwin-x64`, `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`, `win32-x64`, and `win32-arm64`. Your package manager must allow optional dependencies; if the binary is missing after install, see the native-binary-not-found fix in [Install Failures Reference](cc_install_failures_reference.md).

To upgrade an npm installation, run `npm install -g @anthropic-ai/claude-code@latest`. Avoid `npm update -g`, which respects the semver range from the original install and may not move you to the newest release. Do **NOT** use `sudo npm install -g`, as this can lead to permission issues and security risks.

## Binary Integrity and Code Signing

Each release publishes a `manifest.json` containing SHA256 checksums for every platform binary. The manifest is signed with an Anthropic GPG key, so verifying the signature on the manifest **transitively verifies** every binary it lists.

### Verify the Manifest Signature

Steps 1-3 require a POSIX shell with `gpg` and `curl`; on Windows, run them in Git Bash or WSL (Step 4 includes a PowerShell option). First download and import the public key, then display its fingerprint:

```bash
curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
gpg --fingerprint security@anthropic.com
```

Confirm the output includes the fingerprint `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`. Next, set `VERSION` to the release you want and download the manifest and its detached signature, then verify:

```bash
gpg --verify manifest.json.sig manifest.json
```

A valid result reports `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`. `gpg` also prints `WARNING: This key is not certified with a trusted signature!` for any freshly imported key — this is expected; the `Good signature` line confirms the cryptographic check passed, and the Step 1 fingerprint comparison confirms the key itself is authentic. Finally, compare the SHA256 checksum of your downloaded binary (`sha256sum claude` on Linux, `shasum -a 256 claude` on macOS, `(Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()` on Windows) against the value under `platforms.<platform>.checksum` in `manifest.json`. Manifest signatures are available for releases from `2.1.89` onward; earlier releases publish checksums in `manifest.json` without a detached signature.

### Platform Code Signatures

In addition to the signed manifest, individual binaries carry platform-native code signatures where supported:

- **macOS**: signed by "Anthropic PBC" and notarized by Apple. Verify with `codesign --verify --verbose ./claude`.
- **Windows**: signed by "Anthropic, PBC". Verify with `Get-AuthenticodeSignature .\claude.exe`.
- **Linux**: binaries are not individually code-signed. If you download directly from the `claude-code-releases` bucket or use the native installer, verify integrity with the manifest signature above. If you install with apt, dnf, or apk, your package manager verifies signatures automatically using the repository signing key.

**Source**: https://code.claude.com/docs/en/setup
**Last Updated**: 2026-06-13
**Status**: Active
