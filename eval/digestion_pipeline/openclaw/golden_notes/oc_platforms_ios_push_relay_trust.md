---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - ios
keywords:
  - openclaw ios push relay
  - relay-backed push official builds
  - apns credential isolation
  - app attest storekit jws
  - gateway identity delegation
  - registration-scoped send grant
  - push.apns.register push.test
  - direct apns local builds
  - openclaw_apns env vars
topics:
  - OpenClaw
  - iOS Push Relay Trust Model
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/platforms/ios
access_control_group: ["general"]
---

# OpenClaw — The iOS Relay-Backed Push Trust Model

## Overview

This note argues the design rationale for OpenClaw's **relay-backed push** on official iOS builds: why distributed iPhone builds route Apple Push Notification service (APNs) delivery through the hosted push relay at `https://ios-push-relay.openclaw.ai` instead of publishing the raw APNs token to the user's gateway. It mirrors the `platforms/ios` source page's *Relay-backed push for official builds*, *Authentication and trust flow*, the *Compatibility note*, and the *Local/manual builds direct APNs* sections. The claim is that the relay enforces two security constraints a direct-APNs-on-gateway design cannot — build authenticity and per-gateway send scoping — by inserting an App Attest + StoreKit + gateway-identity delegation hop-by-hop chain, while keeping production APNs credentials off user gateways. The connect/pair/discover runbook itself lives in the sibling **[oc_platforms_ios_connection](oc_platforms_ios_connection.md)**; this note is the "why this design" argument, not the connect procedure.

## The Claim: Relay-Backed Push for Official Builds

Official distributed iOS builds use the **external push relay** instead of publishing the raw APNs token to the gateway. By default, official/TestFlight builds and gateways use the hosted relay at `https://ios-push-relay.openclaw.ai`. Custom relay deployments can override the gateway relay URL:

```json5
{
  gateway: {
    push: {
      apns: {
        relay: {
          baseUrl: "https://relay.example.com",
        },
      },
    },
  },
}
```

The mechanism the argument rests on, as stated by the source: the iOS app registers with the relay using **App Attest** and a **StoreKit app transaction JWS**; the relay returns an **opaque relay handle plus a registration-scoped send grant**; the app fetches the paired gateway identity and includes it in relay registration, so the relay-backed registration is *delegated to that specific gateway*; the app forwards that relay-backed registration to the paired gateway with `push.apns.register`; and the gateway then uses that stored relay handle for `push.test`, background wakes, and wake nudges. Custom gateway relay URLs must match the relay URL baked into the official/TestFlight iOS build, and if the app later connects to a different gateway or a build with a different relay base URL, it refreshes the relay registration instead of reusing the old binding.

The load-bearing consequence — what the gateway does **not** need on this path — is the crux of the argument: **no deployment-wide relay token** and **no direct APNs key** for official/TestFlight relay-backed sends. The expected operator flow is: (1) install the official/TestFlight build; (2) optionally set `gateway.push.apns.relay.baseUrl` only when using a custom relay deployment; (3) pair the app to the gateway and let it finish connecting; (4) the app publishes `push.apns.register` automatically after it has an APNs token, the operator session is connected, and relay registration succeeds; (5) thereafter `push.test`, reconnect wakes, and wake nudges can use the stored relay-backed registration.

## The Two Constraints Direct-APNs Cannot Enforce

The source states the relay exists to enforce **two constraints that direct APNs-on-gateway cannot provide** for official iOS builds. These are the premises the rest of the design defends:

- **Build authenticity** — only genuine OpenClaw iOS builds distributed through Apple can use the hosted relay.
- **Per-gateway send scoping** — a gateway can send relay-backed pushes only for iOS devices that paired with *that specific* gateway.

A naive "put the APNs `.p8` key on every user gateway" design satisfies neither: any holder of the key could send to any token, and a signed-but-unofficial local build could obtain a token. The relay is the trust anchor that makes both constraints checkable, because it (and only it) validates the Apple distribution proof and binds each send grant to a delegated gateway identity.

## The Hop-by-Hop Trust Chain (the supporting argument)

The argument is carried by a five-hop chain where each hop adds a verification the previous hop could not:

1. **`iOS app -> gateway`** — the app first pairs with the gateway through the normal Gateway auth flow, giving the app an authenticated **node session plus an authenticated operator session**. The operator session is used to call `gateway.identity.get`.
2. **`iOS app -> relay`** — the app calls the relay registration endpoints over HTTPS. Registration includes **App Attest proof plus a StoreKit app transaction JWS**. The relay validates the bundle ID, App Attest proof, and Apple distribution proof, and **requires the official/production distribution path**. This is what blocks local Xcode/dev builds from using the hosted relay: a local build may be signed, but it does not satisfy the official Apple distribution proof the relay expects (constraint 1).
3. **`gateway identity delegation`** — before relay registration, the app fetches the paired gateway identity from `gateway.identity.get`, includes that identity in the relay registration payload, and the relay returns a relay handle and a **registration-scoped send grant delegated to that gateway identity** (this is the binding behind constraint 2).
4. **`gateway -> relay`** — the gateway stores the relay handle and send grant from `push.apns.register`. On `push.test`, reconnect wakes, and wake nudges, the gateway **signs the send request with its own device identity**. The relay verifies **both** the stored send grant **and** the gateway signature against the delegated gateway identity from registration. Therefore another gateway cannot reuse that stored registration *even if it somehow obtains the handle* — the signature would not match the delegated identity.
5. **`relay -> APNs`** — the relay owns the production APNs credentials and the raw APNs token for the official build; the gateway never stores the raw APNs token for relay-backed official builds; and the relay sends the final push to APNs on behalf of the paired gateway.

## Why This Design Was Created

The source explicitly enumerates the design intent, which is the conclusion of the argument:

- To keep **production APNs credentials out of user gateways**.
- To avoid **storing raw official-build APNs tokens on the gateway**.
- To allow hosted relay usage **only for official/TestFlight OpenClaw builds**.
- To **prevent one gateway from sending wake pushes to iOS devices owned by a different gateway**.

Each goal maps back to a hop: credential isolation and raw-token avoidance are satisfied because hop 5 keeps APNs material entirely on the relay; the official-builds-only restriction is enforced at hop 2 (Apple distribution proof); and cross-gateway prevention is enforced at hops 3–4 (delegated identity + gateway-signed send verified against it).

## The Fallback: Local/Manual Builds Use Direct APNs

The argument scopes itself: **local/manual builds remain on direct APNs** because they cannot satisfy the official distribution proof. For testing those builds without the relay, the gateway still needs direct APNs credentials, supplied as **gateway-host runtime env vars** (not Fastlane settings):

```bash
export OPENCLAW_APNS_TEAM_ID="TEAMID"
export OPENCLAW_APNS_KEY_ID="KEYID"
export OPENCLAW_APNS_PRIVATE_KEY_P8="$(cat /path/to/AuthKey_KEYID.p8)"
```

The source clarifies the boundary: `apps/ios/fastlane/.env` only stores App Store Connect / TestFlight auth such as `APP_STORE_CONNECT_KEY_ID` and `APP_STORE_CONNECT_ISSUER_ID`; it does **not** configure direct APNs delivery for local iOS builds. Recommended gateway-host key storage (locked-down directory and `.p8` permissions) is:

```bash
mkdir -p ~/.openclaw/credentials/apns
chmod 700 ~/.openclaw/credentials/apns
mv /path/to/AuthKey_KEYID.p8 ~/.openclaw/credentials/apns/AuthKey_KEYID.p8
chmod 600 ~/.openclaw/credentials/apns/AuthKey_KEYID.p8
export OPENCLAW_APNS_PRIVATE_KEY_PATH="$HOME/.openclaw/credentials/apns/AuthKey_KEYID.p8"
```

The source's standing rule: **do not commit the `.p8` file or place it under the repo checkout**. This fallback is the deliberate exception — direct APNs on the gateway is acceptable precisely where the relay's two constraints are not in scope (a local build the operator already controls and trusts).

## Compatibility Note (env overrides)

Two temporary environment-variable overrides remain valid alongside the relay design: `OPENCLAW_APNS_RELAY_BASE_URL` still works as a temporary env override for the **gateway**, and `OPENCLAW_PUSH_RELAY_BASE_URL` still works as a temporary env override for **official/TestFlight iOS builds**. These let an operator point at a custom relay deployment without rebuilding, but the standing rule from the relay design still binds: a custom gateway relay URL must match the relay URL baked into the official/TestFlight build, or the app refreshes (rather than reuses) its relay registration.

**Source**: OpenClaw documentation — `platforms/ios` (mirror `inbox/openclaw_docs/platforms/ios.md`)
**Last Updated**: 2026-06-22
**Status**: Active
