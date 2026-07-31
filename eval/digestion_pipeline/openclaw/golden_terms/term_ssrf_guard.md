---
tags:
  - resource
  - terminology
  - ssrf
  - ssrf-guard
  - web-security
  - openclaw
keywords:
  - SSRF
  - Server-Side Request Forgery
  - SSRF protection
  - URL allowlist
  - cloud metadata
  - IMDSv2
  - DNS rebinding
topics:
  - Web vulnerabilities
  - Outbound-request hardening
  - OpenClaw security architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Server-side_request_forgery
access_control_group: ["general"]
---

# SSRF Guard

## Definition

**Server-Side Request Forgery (SSRF)** is a web vulnerability — listed as **OWASP Top 10 2021 A10** and tracked as **CWE-918** — in which an attacker abuses a server-side feature that fetches a user-supplied URL to make that server issue requests to unintended destinations. The canonical attack target is the **cloud metadata endpoint** (AWS / Azure / GCP all expose `http://169.254.169.254/`), which silently returns IAM-role credentials to any process that can reach it from inside the VPC. Other SSRF surfaces include `file://`, `gopher://`, and `dict://` schemes (local file read, byte-level protocol smuggling), private RFC1918 ranges, and chained redirects that flip from a public host to an internal one after the allowlist check has already passed.

An **SSRF guard** is the wrapper that sits in front of every outbound HTTP call whose URL is influenced by user input or by a configured plugin. Rather than trusting the URL string, it parses the URL, asserts the scheme is in a short allowlist (typically `https` only, sometimes `http`), resolves the hostname to an IP, checks that IP against a deny list (no link-local `169.254.0.0/16`, no `127.0.0.0/8`, no RFC1918 private ranges, no AWS metadata host), re-resolves on connect to defeat DNS rebinding, and revalidates every hop in any redirect chain. Credentials are injected as request headers (e.g. `xi-api-key`, `Authorization`) rather than URL query parameters so they cannot leak through redirects or referrer logs.

## Context

SSRF earned its own OWASP Top 10 slot in 2021 largely because of the **Capital One breach (July 2019)**. A misconfigured ModSecurity WAF on an EC2 instance was tricked via SSRF into relaying a request to **IMDSv1** at `169.254.169.254`, which handed back the WAF's IAM-role credentials; the attacker then enumerated 700+ S3 buckets and exfiltrated ~106 million credit-card applications. AWS's response was **IMDSv2**, a session-based protocol that requires a `PUT` request with a custom `X-aws-ec2-metadata-token-ttl-seconds` header to obtain a token before any metadata `GET` will succeed — most SSRF primitives can only trigger `GET` requests with no custom headers, so IMDSv2 hard-blocks the Capital-One attack class. IMDSv2 also enforces a hop-limit of 1, preventing token theft through container or proxy networks.

Inside [OpenClaw](term_openclaw.md), every adapter that issues an outbound HTTP request on behalf of a user-configured plugin wraps the call in an SSRF guard — referenced in the codebase as `fetchWithSsrFGuard`. The pattern appears across all speech providers: the [ElevenLabs](../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) TTS adapter calls `fetchWithSsrFGuard` with the `xi-api-key` header rather than passing the API key in the URL, and the Deepgram STT adapter does the analogous wrap for its streaming WebSocket open. The same wrapper protects external-content fetchers, webhook callbacks, OAuth-redirect handlers, and any tool that follows a user-supplied URL — a single uncovered call inside an LLM-agent runtime is enough to give a prompt-injection attacker reachability to cloud credentials, internal services, or the local filesystem.

## Key Characteristics

- **URL scheme allowlist** — only `https` (sometimes `http`) accepted; reject `file://`, `gopher://`, `dict://`, `ftp://`, `data:`, `blob:`, custom schemes
- **Host deny list** — reject `169.254.0.0/16` (cloud metadata, link-local), `127.0.0.0/8` (loopback), RFC1918 private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), `::1`, `fc00::/7`, and the metadata DNS aliases (`metadata.google.internal`, etc.)
- **DNS-rebinding mitigation** — re-resolve the hostname at connect time and recheck against the deny list; do not trust the resolution that passed pre-flight validation
- **Redirect-chain validation** — disable automatic redirect following, or revalidate every `3xx` `Location` header against the same allowlist before opening the next hop; cap the chain length (typically 5)
- **Header-based auth, never URL-param auth** — inject API keys and OAuth tokens as request headers (`Authorization`, `xi-api-key`) so they don't leak through redirects, proxies, or browser referrer logs
- **Content-type and size validation** — assert the response `Content-Type` matches what the calling tool expects and impose a hard byte-cap on the response body to defeat zip-bombs and memory-exhaustion variants
- **Hostname allowlist over IP allowlist** — for plugin-configured endpoints, allowlist hostnames at config time and re-resolve on every request; never bake in an IP that might later belong to a different tenant
- **Defense in depth** — pair the application-layer guard with egress firewall rules (default-deny to RFC1918, metadata IPs blackholed) and least-privilege IAM roles so a single guard bypass cannot extract usable credentials

## Related Terms


## Related Code Snippets

- [snippet_openclaw_speech_elevenlabs_tts.md](../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS adapter wraps `fetchWithSsrFGuard` around every `/v1/text-to-speech` POST and injects credentials via the `xi-api-key` header

## References

- [Server Side Request Forgery — OWASP Foundation](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
- [A10 Server-Side Request Forgery (SSRF) — OWASP Top 10:2021](https://owasp.org/Top10/2021/A10_2021-Server-Side_Request_Forgery_(SSRF)/)
- [Server Side Request Forgery Prevention Cheat Sheet — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [CWE-918: Server-Side Request Forgery (SSRF) — MITRE](https://cwe.mitre.org/data/definitions/918.html)
- [Server-side request forgery — Wikipedia](https://en.wikipedia.org/wiki/Server-side_request_forgery)
- [What We Can Learn from the Capital One Hack — Krebs on Security](https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/)
- [Instance Metadata Service Version 2 (IMDSv2) — AWS Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
