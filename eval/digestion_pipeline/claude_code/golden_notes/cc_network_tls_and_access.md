---
tags:
  - resource
  - documentation
  - claude_code
  - network_config
  - tls
keywords:
  - ca certificate store
  - custom ca certificates
  - mtls authentication
  - claude_code_cert_store
  - node_extra_ca_certs
  - tls inspection proxy
  - network access requirements
  - egress allowlist
topics:
  - Claude Code
  - Network Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/network-config
access_control_group: ["general"]
---

# Claude Code — Network TLS Trust & Access Requirements

## Overview

For enterprise environments, Claude Code exposes environment variables that control **TLS trust** (which Certificate Authorities it accepts), **mutual TLS (mTLS)** client-certificate authentication, and a documented **network-access allowlist** of URLs the proxy/firewall must permit. This note is the procedure for those three concerns: configuring the CA certificate store so TLS-inspection proxies are trusted, adding a custom CA, presenting a client certificate for mTLS, and allowlisting the destinations Claude Code reaches. The corporate-proxy and LLM-gateway configuration that fronts this traffic is the sibling procedure [cc_proxy_and_gateway_config](cc_proxy_and_gateway_config.md). All environment variables on this page can also be configured in `settings.json` (the settings-files reference is documented on the [settings page](https://code.claude.com/docs/en/settings)).

## CA certificate store

By default, Claude Code trusts **both** its bundled Mozilla CA certificates **and** your operating system's certificate store. Enterprise TLS-inspection proxies such as **CrowdStrike Falcon** and **Zscaler** work without additional configuration when their root certificate is installed in the OS trust store.

`CLAUDE_CODE_CERT_STORE` accepts a comma-separated list of sources. The recognized values are `bundled` (the Mozilla CA set shipped with Claude Code) and `system` (the operating-system trust store). The default is `bundled,system`. To narrow trust to just one source:

```bash
# Trust only the bundled Mozilla CA set
export CLAUDE_CODE_CERT_STORE=bundled

# Trust only the OS certificate store
export CLAUDE_CODE_CERT_STORE=system
```

`CLAUDE_CODE_CERT_STORE` has **no dedicated `settings.json` schema key**. Set it via the `env` block in `~/.claude/settings.json` or directly in the process environment.

## Custom CA certificates

If your enterprise environment uses a custom CA, configure Claude Code to trust it directly by pointing `NODE_EXTRA_CA_CERTS` at the certificate file:

```bash
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS authentication

For enterprise environments that require **client certificate authentication**, Claude Code presents a client cert/key pair (with an optional passphrase for an encrypted key):

```bash
# Client certificate for authentication
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Client private key
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Optional: Passphrase for encrypted private key
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Network access requirements

Claude Code requires access to the following URLs. Allowlist these in your proxy configuration and firewall rules, especially in containerized or restricted network environments:

| URL | Required for |
| --- | --- |
| `api.anthropic.com` | Claude API requests |
| `claude.ai` | claude.ai account authentication |
| `platform.claude.com` | Anthropic Console account authentication |
| `downloads.claude.ai` | Plugin executable downloads; native installer and native auto-updater |
| `storage.googleapis.com` | Native installer and native auto-updater on versions prior to 2.1.116 |
| `bridge.claudeusercontent.com` | Claude in Chrome extension WebSocket bridge |
| `raw.githubusercontent.com` | Changelog feed for `/release-notes` and the post-update release notes; plugin marketplace install counts |

If you install Claude Code through npm or manage your own binary distribution, end users may not need access to `downloads.claude.ai` or `storage.googleapis.com`.

Claude Code also sends optional operational telemetry by default, which you can disable with environment variables — see [Telemetry services](https://code.claude.com/docs/en/data-usage#telemetry-services) for how to disable it before finalizing your allowlist.

### Cloud-provider and GitHub-IP caveats

When using Amazon Bedrock, Google Vertex AI, or Microsoft Foundry, model traffic and authentication go to **your provider** instead of `api.anthropic.com`, `claude.ai`, or `platform.claude.com`. The WebFetch tool still calls `api.anthropic.com` for its domain safety check unless you set `skipWebFetchPreflight: true` in settings.

Claude Code on the web and Code Review connect to your repositories from **Anthropic-managed infrastructure**. If your GitHub Enterprise Cloud organization restricts access by IP address, enable IP allow-list inheritance for installed GitHub Apps — the Claude GitHub App registers its IP ranges, so enabling this allows access without manual configuration. Alternatively, add the Anthropic API IP ranges to your allow list manually or to other firewalls. For self-hosted GitHub Enterprise Server instances behind a firewall, allowlist the same Anthropic API IP addresses so Anthropic infrastructure can reach your GHES host to clone repositories and post review comments.

## Additional resources

- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Environment variables reference](https://code.claude.com/docs/en/env-vars)
- [Troubleshooting guide](https://code.claude.com/docs/en/troubleshooting)

**Source**: https://code.claude.com/docs/en/network-config
**Last Updated**: 2026-06-13
**Status**: Active
