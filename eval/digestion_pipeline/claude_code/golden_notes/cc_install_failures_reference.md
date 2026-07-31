---
tags:
  - resource
  - documentation
  - claude_code
  - installation
  - troubleshooting
keywords:
  - install failures reference
  - command not found claude
  - install script returns html
  - tls ssl connection errors
  - musl glibc binary mismatch
  - illegal instruction avx
  - install hangs in docker
  - native binary not found
  - symptom to fix lookup
topics:
  - Claude Code
  - Installation Troubleshooting
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/troubleshoot-install
access_control_group: ["general"]
---

# Claude Code — Install Failures Reference

## Overview

This is the symptom-to-fix lookup table for Claude Code **installation** failures. When the install command errors out, the docs page opens with a **"Find your error"** router table that maps each error string (e.g. `command not found: claude`, `syntax error near unexpected token '<'`, `curl: (56)`, `TLS connect error`, `Illegal instruction`) to its fix. This note captures that router plus the page's **19 "Common installation issues"** — each a symptom, its root cause, and the recovery steps.

The fixes fall into recurring root-cause families: PATH not configured, the install URL returning HTML or a 403, corporate proxies breaking TLS, low memory or a filesystem scan exhausting the install process, the wrong shell command for the platform, and native-binary incompatibilities (musl vs glibc, missing AVX, old macOS, WSL1). For the ordered diagnostic checks that narrow down an unlisted error, see [Install Diagnostics](cc_install_diagnostics.md); for login/auth failures see [Login and Authentication Troubleshooting](cc_login_authentication_troubleshooting.md); for the base install procedure see [Install](cc_install.md).

## Find your error (router table)

Match the error message or symptom to a fix. The most common mappings from the page's router table:

| What you see | Solution |
| :--- | :--- |
| `command not found: claude` / `'claude' is not recognized` | Fix your PATH (see [Install Diagnostics](cc_install_diagnostics.md)) |
| `syntax error near unexpected token '<'`, `<!DOCTYPE html>`, or `Invoke-Expression: Missing argument in parameter list` | Install script returns HTML |
| `curl: (22) ... error: 403` | Install script returned 403 |
| `curl: (23)` or `curl: (56) Failure writing output to destination` | Check connectivity or use an alternative installer |
| `Killed` during install on Linux | Add swap space for low-memory servers |
| `TLS connect error`, `SSL/TLS secure channel`, or `unable to get local issuer certificate` | Update / configure CA certificates |
| `Failed to fetch version` or can't reach download server | Check network and proxy settings |
| `irm is not recognized`, `&& is not valid`, or `'bash' is not recognized as the name of a cmdlet` | Use the right command for your shell |
| `Claude Code on Windows requires either Git for Windows ... or PowerShell` | Install a shell |
| `Claude Code does not support 32-bit Windows` | Open `Windows PowerShell`, not the x86 entry |
| `The process cannot access the file ... because it is being used by another process` | Clear the downloads folder and retry |
| `Error loading shared library` | Wrong binary variant (musl/glibc) |
| `Illegal instruction` | Architecture or CPU instruction-set mismatch |
| `cannot execute binary file: Exec format error` in WSL | WSL1 native-binary regression |
| `dyld: cannot load`, `dyld: Symbol not found`, or `Abort trap` on macOS | Binary incompatibility |
| `App unavailable in region` | Claude Code is not available in your country |
| `OAuth error` or `403 Forbidden` | Fix authentication ([Login Troubleshooting](cc_login_authentication_troubleshooting.md)) |
| `Could not load ... credentials`, `ChainedTokenCredential authentication failed`, `CredentialUnavailableError` | Bedrock/Vertex/Foundry credentials ([Login Troubleshooting](cc_login_authentication_troubleshooting.md)) |
| `API Error: 500`, `529 Overloaded`, `429`, or other 4xx/5xx | See the error reference (https://code.claude.com/docs/en/errors) |

If the issue isn't listed, work through the diagnostic checks in [Install Diagnostics](cc_install_diagnostics.md).

## Network and download failures

**Install script returns HTML instead of a shell script.** Errors like `bash: line 1: syntax error near unexpected token '<'` / `'<!DOCTYPE html>'`, PowerShell's `Invoke-Expression: Missing argument in parameter list.`, or a bare `curl: (22) The requested URL returned error: 403` all mean the install URL returned an HTML page or an error status instead of the script. If the HTML says "App unavailable in region," Claude Code is not available in your country. A bare 403 can also come from a corporate proxy/firewall — work through network connectivity first, since the alternative installers reach the same hosts. Otherwise use an alternative install method (`brew install --cask claude-code` on macOS, `winget install Anthropic.ClaudeCode` on Windows) or retry after a few minutes.

**`command not found: claude` after installation.** The install finished but the install directory isn't on your shell's search path. The error varies by platform (`zsh: command not found: claude`, `bash: claude: command not found`, `'claude' is not recognized as an internal or external command`, or PowerShell's `claude : The term 'claude' is not recognized as the name of a cmdlet`). The fix is the PATH check in [Install Diagnostics](cc_install_diagnostics.md).

**`curl: (56) Failure writing output to destination`.** The `curl ... | bash` pipe did not receive the complete script. Exit code 56 means the download itself was interrupted; the related exit code 23 means curl couldn't write to the pipe, usually because Bash exited early. Test connectivity to `downloads.claude.ai`; an `HTTP/2 200` means the failure was intermittent (retry), while `Could not resolve host` means the network is blocking the download. Or use an alternative installer (Homebrew/WinGet).

**TLS or SSL connection errors.** Errors like `curl: (35) TLS connect error`, `schannel: next InitializeSecurityContext failed`, or PowerShell's `Could not establish trust relationship for the SSL/TLS secure channel` are TLS handshake failures. Fixes: update system CA certificates (`sudo apt-get update && sudo apt-get install ca-certificates` on Ubuntu/Debian; updating macOS updates its root certs); on Windows enable TLS 1.2 before installing; and if a corporate proxy performs TLS inspection (`unable to get local issuer certificate`, `SELF_SIGNED_CERT_IN_CHAIN`), point curl at your corporate CA bundle for the install step, then set `NODE_EXTRA_CA_CERTS` so the installed Claude Code trusts the same bundle:

```bash theme={null}
curl --cacert /path/to/corporate-ca.pem -fsSL https://claude.ai/install.sh | bash
```

On Windows, if you see `CRYPT_E_NO_REVOCATION_CHECK (0x80092012)` or `CRYPT_E_REVOCATION_OFFLINE (0x80092013)`, your network blocks the certificate revocation lookup — add `--ssl-revoke-best-effort` to the install command or install with WinGet, which avoids curl. (Env vars like `NODE_EXTRA_CA_CERTS` are owned by https://code.claude.com/docs/en/settings.)

**`Failed to fetch version from downloads.claude.ai`.** The installer couldn't reach the download server, typically because `downloads.claude.ai` is blocked. Test connectivity directly; if behind a proxy set `HTTPS_PROXY` so the installer routes through it; on a restricted network try a different network/VPN or an alternative install method.

## Wrong command, locked file, or low memory

**Wrong install command on Windows.** `'irm' is not recognized`, `The token '&&' is not valid`, or `'bash' is not recognized as the name of a cmdlet` mean you copied the command for a different shell/OS. `irm` not recognized → you're in CMD, not PowerShell (open PowerShell and run the original command, or use the CMD installer). `&&` not valid → you're in PowerShell but ran the CMD command. `bash` not recognized → you ran the macOS/Linux installer on Windows. In the PowerShell cases, use the PowerShell installer:

```powershell theme={null}
irm https://claude.ai/install.ps1 | iex
```

**`The process cannot access the file` during Windows install.** `Failed to download binary: The process cannot access the file ... because it is being used by another process` means the installer couldn't write to `%USERPROFILE%\.claude\downloads`, usually because a previous install is still running or antivirus is scanning a partial binary. Close other installer windows, wait for the scan to release the file, then delete the downloads folder and re-run the installer.

**Install killed on low-memory Linux servers.** A `Killed` line during install (e.g. `bash: line 142: 34803 Killed "$binary_path" install`) means the Linux OOM killer terminated the process — Claude Code requires at least 4 GB of available RAM. Add swap space, close other processes, or use a larger instance. The swap-file fix:

```bash theme={null}
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Install hangs in Docker.** Installing as root into `/` causes hangs because the installer scans the entire filesystem, exhausting memory. Set a `WORKDIR` before running the installer to limit the scan, and increase Docker memory limits (`docker build --memory=4g .`) if using Docker Desktop:

```dockerfile theme={null}
WORKDIR /tmp
RUN curl -fsSL https://claude.ai/install.sh | bash
```

**Claude Desktop overrides the `claude` command on Windows.** An older Claude Desktop may register a `Claude.exe` in the `WindowsApps` directory that takes PATH priority over the Claude Code CLI, so running `claude` opens the Desktop app instead. Update Claude Desktop to the latest version to fix this.

## Windows shell and 32-bit issues

**Claude Code on Windows requires Git for Windows (for bash) or PowerShell.** This error means neither shell was found (Git for Windows is optional — Claude Code uses the PowerShell tool when Git Bash is absent). If PowerShell is missing from PATH, add `C:\Windows\System32\WindowsPowerShell\v1.0\` or install PowerShell 7 (`pwsh`). To install Git for Windows, download it and select "Add to PATH." If Git is installed but not found, set its path in `settings.json`:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

If the path is correct but Claude Code still reports Git as not found, endpoint security software (AppLocker, Group Policy software restriction policies, EDR agents) may be interfering: on versions before v2.1.116, Claude Code spawned `cmd.exe` to verify the path, which these policies can block. v2.1.116 and later check the filesystem directly, so update first; if it persists, have IT allowlist `claude.exe` and the processes it spawns (`cmd.exe`, `bash.exe`).

**Claude Code does not support 32-bit Windows.** Windows lists two PowerShell entries — `Windows PowerShell` and `Windows PowerShell (x86)`. The x86 entry runs as a 32-bit process and triggers this error even on a 64-bit machine. Run `[Environment]::Is64BitOperatingSystem` in the same window: `True` means your OS is fine (close the window, open `Windows PowerShell` without the x86 suffix, and reinstall); `False` means you're on a 32-bit edition and Claude Code requires a 64-bit OS.

## Native-binary incompatibilities

These are failures where the binary itself can't run on the system.

**Linux musl or glibc binary mismatch.** Errors about missing shared libraries (e.g. `Error loading shared library libstdc++.so.6: No such file or directory`, `libgcc_s.so.1`) mean the installer downloaded the wrong variant — common on glibc systems that have musl cross-compilation packages installed, causing musl misdetection. Check which libc you use with `ldd --version 2>&1 | head -1` (`GNU libc`/`GLIBC` = glibc; `musl` = musl). If you're on glibc but got the musl binary, remove and reinstall (you can manually download the correct binary from the per-version `manifest.json`) and file a GitHub issue. If you're actually on musl (e.g. Alpine), install the required packages with `apk add libgcc libstdc++ ripgrep`.

**`Illegal instruction`.** The native binary uses CPU instructions your processor doesn't support — two distinct causes. (1) *Architecture mismatch* — the installer downloaded the wrong binary (e.g. x86 on an ARM server); check with `uname -m` (or `$env:PROCESSOR_ARCHITECTURE`) and file a GitHub issue if it doesn't match. (2) *Missing AVX instruction set* — the CPU lacks AVX (roughly pre-2013 Intel/AMD, or a VM whose hypervisor doesn't pass AVX through); run `grep -m1 -ow avx /proc/cpuinfo` (empty result = no AVX). There is no native-binary workaround; track the tracking issue and report your CPU model. Alternative install methods download the same binary and won't resolve either cause.

**`dyld: cannot load` on macOS.** `dyld: cannot load`, `dyld: Symbol not found` (e.g. referencing `libicucore`), or `Abort trap: 6` during install means the binary is incompatible with your macOS version or hardware. Claude Code requires macOS 13.0 or later — check via Apple menu → About This Mac, and update macOS if older. Alternative install methods download the same binary and won't resolve this.

**`Exec format error` on WSL1.** `cannot execute binary file: Exec format error` means you're on WSL1 hitting a known native-binary regression (the binary's program headers changed in a way WSL1's loader can't handle). The cleanest fix is to convert the distribution to WSL2 from PowerShell (`wsl --set-version <DistroName> 2`). To stay on WSL1, invoke the binary through the dynamic linker by adding a wrapper function to `~/.bashrc`:

```bash theme={null}
claude() {
  /lib64/ld-linux-x86-64.so.2 "$(readlink -f "$HOME/.local/bin/claude")" "$@"
}
```

## npm-path and permission failures

**npm install errors in WSL.** These apply only if you installed with `npm install -g` inside WSL (skip if you used the native installer). *OS/platform detection* — if npm reports a platform mismatch, WSL is picking up the Windows `npm`; run `npm config set os linux` first, then `npm install -g @anthropic-ai/claude-code --force` (do not use `sudo`). *`exec: node: not found`* — WSL is using the Windows Node.js (`/mnt/c/...` paths are Windows binaries); install Node via your Linux package manager or `nvm`. *nvm version conflicts* — if nvm is in both WSL and Windows, the Windows nvm can take PATH priority; the most common cause is nvm not being loaded in your shell, so add the nvm loader to `~/.bashrc`/`~/.zshrc` or `source` it. Avoid `appendWindowsPath = false` (breaks calling Windows executables from WSL).

**Permission errors during installation.** If the native installer fails with permission errors, the target directory may not be writable — see the directory-permission check in [Install Diagnostics](cc_install_diagnostics.md). If you previously installed with npm and hit npm-specific permission errors, switch to the native installer (`curl -fsSL https://claude.ai/install.sh | bash`).

**Native binary not found after npm install.** The `@anthropic-ai/claude-code` npm package pulls in the native binary through a per-platform optional dependency (e.g. `@anthropic-ai/claude-code-darwin-arm64`). If `claude` prints `Could not find native binary package "@anthropic-ai/claude-code-<platform>"`, check three causes: (1) *Optional dependencies disabled* — remove `--omit=optional` (npm), `--no-optional` (pnpm), or `--ignore-optional` (yarn), and check `.npmrc` doesn't set `optional=false`, then reinstall (there is no JavaScript fallback). (2) *Unsupported platform* — prebuilt binaries exist for `darwin-arm64`, `darwin-x64`, `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`, `win32-x64`, and `win32-arm64` only. (3) *Corporate npm mirror missing the platform packages* — ensure the registry mirrors all eight `@anthropic-ai/claude-code-*` platform packages plus the meta package. Note: `--ignore-scripts` does not trigger this error but skips the postinstall link step, so launches are slower; reinstall with scripts enabled for direct execution.

**Source**: https://code.claude.com/docs/en/troubleshoot-install
**Last Updated**: 2026-06-13
**Status**: Active
