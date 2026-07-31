---
tags:
  - resource
  - documentation
  - claude_code
  - cloud
  - network
keywords:
  - network access levels
  - none trusted full custom
  - allowed domains allowlist
  - github proxy
  - security proxy
  - default allowed domains
  - scoped credential
  - wildcard subdomain
topics:
  - Claude Code
  - Cloud Environment
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/claude-code-on-the-web
access_control_group: ["general"]
---

# Claude Code on the Web — Cloud Network Access

## Overview

Network access controls outbound connections from a Claude Code on the web cloud environment. Each environment specifies exactly **one access level** — None, Trusted, Full, or Custom — and you can extend it with custom allowed domains. The default is **Trusted**, which permits package registries, GitHub, cloud SDKs, and the rest of the built-in allowlist. To change an environment's network access, open it for editing and use the **Network access** selector in the dialog; there is no separate Environments page, and the cloud icon appears wherever you start a cloud session or configure a routine.

Two dedicated proxies sit between the sandbox and the internet. The **GitHub proxy** transparently handles all git interactions using a scoped credential so your real GitHub token never enters the container, and it is independent of the access-level setting. The **security proxy** carries all other outbound traffic for abuse prevention, content filtering, and a DNS-level audit trail. One notable exception to the allowlist model: MCP connector traffic is routed through Anthropic's servers, so connectors you enable on a session or routine work without adding their hosts to **Allowed domains** (this relies on the same Anthropic-bound channel described under Security and isolation).

## Access levels

Choose an access level when you create or edit an environment:

| Level       | Outbound connections                                                                         |
| :---------- | :------------------------------------------------------------------------------------------- |
| **None**    | No outbound network access                                                                   |
| **Trusted** | Allowlisted domains only: package registries, GitHub, cloud SDKs                             |
| **Full**    | Any domain                                                                                   |
| **Custom**  | Your own allowlist, optionally including the defaults                                        |

GitHub operations use a separate proxy that is independent of this setting.

## Allow specific domains

To allow domains that aren't in the Trusted list, select **Custom** in the environment's network access settings. An **Allowed domains** field appears. Enter one domain per line:

```text
api.example.com
*.internal.example.com
registry.example.com
```

Use `*.` for wildcard subdomain matching. Check **Also include default list of common package managers** to keep the Trusted domains alongside your custom entries, or leave it unchecked to allow only what you list.

## GitHub proxy

For security, all GitHub operations go through a dedicated proxy service that transparently handles all git interactions. Inside the sandbox, the git client authenticates using a custom-built scoped credential. This proxy:

- Manages GitHub authentication securely: the git client uses a scoped credential inside the sandbox, which the proxy verifies and translates to your actual GitHub authentication token
- Restricts git push operations to the current working branch for safety
- Enables cloning, fetching, and PR operations while maintaining security boundaries

## Security proxy

Environments run behind an HTTP/HTTPS network proxy for security and abuse prevention purposes. All outbound internet traffic passes through this proxy, which provides:

- Protection against malicious requests
- Rate limiting and abuse prevention
- Content filtering for enhanced security
- A DNS-level audit trail of requested hostnames

## Default allowed domains

When using **Trusted** network access, a built-in set of domains is allowed by default. Domains marked with `*` indicate wildcard subdomain matching, so `*.gcr.io` allows any subdomain of `gcr.io`. The source page lists the full allowlist as an accordion grouped by category; the categories are:

- **Anthropic services** — e.g. `api.anthropic.com`, `claude.ai`, `code.claude.com`, `docs.claude.com`, `platform.claude.com`, `statsig.anthropic.com`
- **Version control** — GitHub (`github.com`, `api.github.com`, `*.githubusercontent.com` hosts, `codeload.github.com`, `gist.github.com`), GitLab, and Bitbucket
- **Container registries** — Docker Hub (`registry-1.docker.io`, `auth.docker.io`, `hub.docker.com`), `gcr.io`/`*.gcr.io`, `ghcr.io`, `mcr.microsoft.com`, `public.ecr.aws`
- **Cloud platforms** — Google Cloud (`*.googleapis.com`), Azure/Microsoft, AWS (`*.amazonaws.com`, `*.api.aws`), Oracle/Java
- **Language package managers** — JavaScript/Node (npm, yarn), Python (PyPI, `files.pythonhosted.org`), Ruby (RubyGems), Rust (crates.io, rustup), Go (`proxy.golang.org`), JVM (Maven, Gradle, Spring, Kotlin), and **Other** (Composer/packagist, NuGet, pub.dev, hex.pm, CPAN, CocoaPods, Haskell, Swift)
- **Linux distributions** — Ubuntu (`*.ubuntu.com`, Launchpad PPAs), `*.nixos.org`
- **Development tools and platforms** — Kubernetes, HashiCorp, Anaconda/Conda, Apache, Eclipse, Node.js, Apple/Android developer sites, Prisma
- **Cloud services and monitoring** — Statsig, Sentry (`*.sentry.io`), Datadog (`*.datadoghq.com`/`.eu`), Honeycomb
- **Content delivery and mirrors** — SourceForge, packagecloud, Google Fonts
- **Schema and configuration** — `json-schema.org`, `schemastore.org`
- **Model Context Protocol** — `*.modelcontextprotocol.io`

Setup scripts and SessionStart hooks that install packages need network access to reach these registries; an environment using **None** access will fail to install packages, while the **Trusted** defaults cover npm, PyPI, RubyGems, and crates.io. Docker image pulls also follow the environment's access level, and the Trusted defaults include Docker Hub and other common registries.

**Source**: https://code.claude.com/docs/en/claude-code-on-the-web
**Last Updated**: 2026-06-13
**Status**: Active
