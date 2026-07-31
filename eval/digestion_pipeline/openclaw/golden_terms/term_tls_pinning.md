---
tags:
  - resource
  - terminology
  - tls-pinning
  - certificate-pinning
  - mobile-security
  - openclaw
keywords:
  - TLS pinning
  - certificate pinning
  - public key pinning
  - HPKP
  - take-once latch
  - URLSessionDelegate
  - CertificatePinner
  - Keychain pin store
topics:
  - Transport security
  - Mobile app security
  - OpenClaw security architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning
access_control_group: ["general"]
---

# TLS Pinning

## Definition

**TLS pinning** (also known as **certificate pinning** or **SSL pinning**) is a transport-security control in which a client refuses to trust any server identity except a small, pre-declared set of cryptographic credentials — typically the SHA-256 fingerprint of an X.509 leaf certificate (**certificate pin**) or the hash of the `subjectPublicKeyInfo` field (**SPKI pin** / public-key pin). Pinning runs in addition to the platform's normal CA-chain validation: even if the system trust store accepts a certificate, the connection is still rejected when its fingerprint is absent from the pinset. This narrows the attack surface from "any of the ~150 trusted root CAs could mis-issue" down to "only the specific keypair I baked in is accepted," defeating both mis-issuance and on-path TLS interception by enterprise / consumer MITM proxies.

The browser-facing form of pinning, **HTTP Public Key Pinning (HPKP)** (RFC 7469), was deprecated in 2017 and removed from Chrome by version 72 (2020) in favor of **Certificate Transparency** logs, because misconfigured pinsets repeatedly soft-bricked production sites for the duration of the pin's `max-age`. The picture is different in mobile apps: pinning is alive and recommended *only* when the client and server are controlled by the same party and the pinset can be rotated via forced app upgrade — exactly the regime where there's no "lockout for everyone forever" tail risk. SPKI pinning is preferred over leaf-certificate pinning because the public key survives certificate reissuance, so routine renewal does not silently break trust.

## Context

TLS pinning is canonically implemented at the networking-stack hook that fires during the TLS handshake. On iOS, that's `URLSessionDelegate.urlSession(_:didReceive:completionHandler:)` filtered to `NSURLAuthenticationMethodServerTrust`, where the delegate extracts the leaf via `SecTrustCopyCertificateChain`, computes SHA-256, and either calls `.useCredential` or `.cancelAuthenticationChallenge`. On Android, the canonical surfaces are **OkHttp's `CertificatePinner`** (SPKI hash pins, attached to the `OkHttpClient` builder) and the **Network Security Configuration** XML (declarative `<pin-set>` per `<domain>`). Pinning is standard in Signal, WhatsApp, and most banking / brokerage apps; it is what stops a corporate MITM box (or a compromised public-Wi-Fi root) from silently decrypting in-flight traffic that the app is willing to send.

OpenClaw's `OpenClawKit` Swift library pins the gateway WebSocket connection because the gateway is a **local-first daemon** with a self-signed development certificate — the system trust store has no opinion about it, and the user is connecting on `localhost` / LAN where on-path attackers are realistic. `GatewayTLSPinningSession` follows the Apple `URLSessionDelegate` pattern with a three-step chain: **explicit pin** (compare leaf SHA-256 to `expectedFingerprint`) → **trust-on-first-use** (save the leaf to a Keychain-backed `GatewayTLSStore` keyed by gateway `stableID` when `allowTOFU` is set) → **system-trust fallback** gated by a `required` flag. The pin store migrates one-shot on first read from a legacy `UserDefaults(suiteName:)` location, and validation failures are funneled into a single-slot **take-once latch** (`consumeLastTLSFailure()`) that the channel reads to surface a structured `GatewayTLSValidationError` (`pinMismatch` / `certificateUnavailable` / `untrustedCertificate`) — never the same error twice.

## Key Characteristics

- **Certificate pin vs SPKI pin**: a cert pin matches the full leaf X.509 (brittle — every renewal changes the fingerprint); an SPKI pin matches `Hash(subjectPublicKeyInfo)` and survives renewal as long as the keypair is reused. OWASP and OkHttp recommend SPKI for mobile.
- **Pinset, not single pin**: production deployments carry at least two pins (active + backup) so a key rotation can be staged ahead of the cutover without bricking installed clients.
- **System-trust-fallback chain**: an explicit pin is checked first; if no pin exists for the host, the implementation may fall through to trust-on-first-use, then to platform CA validation gated by a `required` flag.
- **Trust on First Use (TOFU) bootstrap**: when no pin is configured, the first observed leaf is saved and treated as the pin for all subsequent connections — analogous to SSH's `known_hosts` model, used when the server identity isn't known at app-build time (OpenClaw's gateway-pairing flow).
- **Keychain-backed pin store with UserDefaults migration**: pins live in `kSecClassGenericPassword` under a per-service identifier (`ai.openclaw.tls-pinning`), with idempotent read-path migration from a legacy `UserDefaults(suiteName:)` location to fix a historical storage choice without losing pins.
- **Single-slot take-once failure latch**: instead of streaming every TLS error, the delegate holds the most recent `GatewayTLSValidationFailure` under an `NSLock` and a reader call (`consumeLastTLSFailure()`) atomically locks-reads-nils — so the reconnect loop never reports the same pin mismatch twice.
- **Closed-set failure taxonomy**: failures are a three-case enum (`pinMismatch` / `certificateUnavailable` / `untrustedCertificate`), making the `errorDescription` switch exhaustive at compile time and keeping the user-facing copy consistent.
- **Explicit pin overrides system trust**: a pin mismatch with `SecTrustEvaluateWithError == true` still cancels the handshake — the whole point of pinning is to refuse system-CA-blessed impostor certs.
- **Pin-rotation strategies**: pre-publish the next pin in a release that's already deployed, flip the key, then drop the old pin in the release after — never ship a single-pin app that the server can't roll back to.

## Related Terms


## Related Code Snippets

- [OpenClawKit — Gateway TLS Pinning](../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — 286-LOC Swift module with `GatewayTLSParams`, `GatewayTLSStore` (Keychain + UserDefaults migration), `GatewayTLSPinningSession` (`URLSessionDelegate` with single-slot take-once latch), and the pin / TOFU / system-trust decision chain.

## References

- [Certificate and Public Key Pinning — OWASP Foundation](https://owasp.org/www-community/controls/Certificate_and_Public_Key_Pinning) — primary external reference; defines cert pin vs SPKI pin and current mobile-app guidance.
- [HTTP Public Key Pinning — Wikipedia](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning) — HPKP deprecation history (Chrome 67 deprecation 2018, Chrome 72 removal 2020) and successor Certificate Transparency.
- [HTTPS — OkHttp documentation](https://square.github.io/okhttp/features/https/) — canonical Android `CertificatePinner` reference with SPKI-hash pin builder syntax.
- [Pinning Cheat Sheet — OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html) — when-to-pin guidance and rotation best practices for mobile clients.
