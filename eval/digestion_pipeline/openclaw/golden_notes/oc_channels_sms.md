---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - sms
keywords:
  - openclaw sms channel
  - twilio sms setup
  - twilio webhook signature
  - x-twilio-signature validation
  - sms dmpolicy pairing allowlist
  - messaging service sid
  - secretref auth token
  - sms multi-account webhookpath
topics:
  - OpenClaw
  - SMS Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/sms
access_control_group: ["general"]
---

# OpenClaw — Twilio SMS Channel Setup

## Overview

This note is the setup-and-configuration procedure for the OpenClaw **SMS channel**, which receives and sends SMS through a Twilio phone number or Messaging Service. OpenClaw registers an inbound webhook route, validates Twilio request signatures by default, and sends replies back through Twilio's Messages API. It mirrors the `channels/sms` source page end-to-end: prerequisites, the quick-setup flow, config-file / env-var / SecretRef / allowlist / Messaging-Service / default-outbound configuration examples, the `dmPolicy` access-control model, sending SMS, end-to-end verification, `X-Twilio-Signature` webhook security, multi-account config, and troubleshooting. Pairing semantics, gateway security, and cross-channel diagnostics are linked, not redefined.

## Before you begin

You need a Twilio account with an SMS-capable phone number (or a Twilio Messaging Service), the Twilio **Account SID** and **Auth Token**, a public HTTPS URL that reaches your OpenClaw Gateway, and a sender-policy choice: `pairing` for private use, `allowlist` for preapproved phone numbers, or `open` only for intentionally public SMS access. You can use one Twilio number for both SMS and Voice Call if the number has both capabilities, but the SMS webhook and Voice webhook are configured separately in Twilio; this procedure covers only the SMS webhook.

## Quick Setup

The quick-setup flow has five steps:

1. **Create or choose a Twilio sender.** In Twilio open **Phone Numbers > Manage > Active numbers** and choose an SMS-capable number. Save the Account SID (for example `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`), the Auth Token, and the sender phone number (for example `+15551234567`). If you use a Messaging Service instead of a fixed sender number, save the Messaging Service SID (for example `MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`).
2. **Configure the SMS channel.** Save the patch below as `sms.patch.json5`, change the placeholders, then apply it (dry-run first):

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: "twilio-auth-token",
      fromNumber: "+15551234567",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
      dmPolicy: "pairing",
    },
  },
}
```

```bash
openclaw config patch --file ./sms.patch.json5 --dry-run
openclaw config patch --file ./sms.patch.json5
# Step 4 — expose the exact SMS webhook path (Tailscale Funnel example for local testing)
tailscale funnel --bg --set-path /webhooks/sms http://127.0.0.1:<gateway-port>/webhooks/sms
tailscale funnel status
# Step 5 — start the Gateway, then list + approve the first sender
openclaw gateway
openclaw pairing list sms
openclaw pairing approve sms <CODE>
```

3. **Point Twilio at the Gateway webhook.** In the Twilio phone-number settings open **Messaging** and set **A message comes in** to `https://gateway.example.com/webhooks/sms` using HTTP `POST`. The default local path is `/webhooks/sms`; change `channels.sms.webhookPath` if you need a different route.
4. **Expose the exact SMS webhook path** (see the Step-4 commands above). Your public URL must route the SMS path to the Gateway process; if you use Tailscale Funnel for local testing, expose `/webhooks/sms` explicitly. Voice Call and SMS use separate webhook paths, so if one Twilio number handles both, keep both routes configured in Twilio and in your tunnel.
5. **Start the Gateway and approve the first sender** (see the Step-5 commands above). Run `openclaw gateway`, send a text to the Twilio number (the first message creates a pairing request), then list and approve it. Pairing codes expire after 1 hour.

## Configuration Examples

**Config file** — use config-file setup when the channel definition should travel with the Gateway config (the `accountSid` / `authToken` / `fromNumber` / `publicWebhookUrl` / `dmPolicy` block is identical to the quick-setup patch above). **Environment variables** — use env setup for single-account deployments where secrets come from the host environment, then enable the channel in config with just `enabled: true` and `dmPolicy`:

```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="<twilio-auth-token>"
export TWILIO_PHONE_NUMBER="+15551234567"
export SMS_PUBLIC_WEBHOOK_URL="https://gateway.example.com/webhooks/sms"
```

`TWILIO_SMS_FROM` is accepted as an alias for `TWILIO_PHONE_NUMBER`. Use `TWILIO_MESSAGING_SERVICE_SID` instead of a phone-number sender when Twilio should choose the sender from a Messaging Service.

**SecretRef auth token** — `authToken` can be a SecretRef. Use this when the Gateway should resolve the Twilio Auth Token from the OpenClaw secrets runtime instead of storing plaintext config. The referenced environment variable or secret provider must be visible to the Gateway runtime, and you must restart managed Gateway processes after changing host environment variables:

```json5
{
  channels: {
    sms: {
      enabled: true,
      accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      authToken: { source: "env", provider: "default", id: "TWILIO_AUTH_TOKEN" },
      fromNumber: "+15551234567",
      publicWebhookUrl: "https://gateway.example.com/webhooks/sms",
      dmPolicy: "pairing",
    },
  },
}
```

**Allowlist-only private number** — use `dmPolicy: "allowlist"` with an explicit `allowFrom` array of E.164 numbers (e.g. `allowFrom: ["+15557654321"]`) when only known phone numbers should be able to talk to the agent. **Messaging Service sender** — set `messagingServiceSid: "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"` instead of `fromNumber` when Twilio should choose the sender through a Messaging Service; if both `fromNumber` and `messagingServiceSid` are present after config and env resolution, `fromNumber` is used. **Default outbound target** — set `defaultTo` (e.g. `defaultTo: "+15557654321"`) so automation or agent-initiated delivery has a default destination when a send flow omits an explicit target.

## Access control

`channels.sms.dmPolicy` controls direct SMS access with four values: `pairing` (default), `allowlist` (requires at least one sender in `allowFrom`), `open` (requires `allowFrom` to include `"*"`), and `disabled`. `allowFrom` entries should be E.164 phone numbers such as `+15551234567`; `sms:` prefixes are accepted and normalized. For a private assistant, prefer `dmPolicy: "allowlist"` with explicit phone numbers.

## Sending SMS

Outbound SMS targets use the `sms:` service prefix with the SMS channel selected (`openclaw message send --channel sms --target sms:+15551234567 --message "hello"`). When channel selection is implicit, `twilio-sms:+15551234567` selects this channel without taking over the existing channel-owned `sms:` service prefix used by iMessage:

```bash
openclaw message send --channel sms --target sms:+15551234567 --message "hello"
openclaw message send --target twilio-sms:+15551234567 --message "hello"
```

The CLI requires an explicit `--target`; `defaultTo` is for automation and agent-initiated delivery paths where the target can be resolved from channel config. Agent replies from inbound SMS conversations automatically go back to the sender through the configured Twilio sender. SMS output is plain text: OpenClaw strips markdown, flattens fenced code blocks, preserves readable links, and chunks long replies before sending them through Twilio.

## Verify Setup

After the Gateway starts: (1) confirm the Gateway log shows the SMS webhook route; (2) run a Twilio-side probe with `openclaw channels capabilities --channel sms` and `openclaw channels status --channel sms --probe --json`; (3) send an SMS to the Twilio number from your phone; (4) run `openclaw pairing list sms`; (5) approve the pairing code with `openclaw pairing approve sms <CODE>`; (6) send another SMS and confirm the agent replies. For outbound-only testing, use `openclaw message send --channel sms --target sms:+15557654321 --message "OpenClaw SMS test"`.

### End-to-end test from macOS iMessage/SMS

On a Mac that can send carrier SMS through Messages, you can use `imsg` to drive the sender side without touching your phone: run `imsg send --to "+15551234567" --service sms --text "OpenClaw SMS E2E $(date -u +%Y%m%dT%H%M%SZ)" --json`, then `openclaw pairing list sms` and `openclaw pairing approve sms <CODE>`, then `imsg send --to "+15551234567" --service sms --text "reply exactly SMS pong" --json`. The first message creates a pairing request; the second message should receive the agent reply through Twilio.

## Webhook security

By default, OpenClaw validates `X-Twilio-Signature` using `publicWebhookUrl` and `authToken`. Keep `publicWebhookUrl` byte-for-byte aligned with the URL configured in Twilio — including scheme, host, path, and query string — because Twilio signs the public URL string and any mismatch breaks validation. For local tunnel testing only, you can set `dangerouslyDisableSignatureValidation: true` under `channels.sms` in config; do not use disabled signature validation on a public Gateway.

## Multi-account config

Use `accounts` when you operate more than one Twilio number. Each account should use a distinct `webhookPath`:

```json5
{
  channels: {
    sms: {
      accounts: {
        support: {
          enabled: true,
          accountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          authToken: "twilio-auth-token",
          fromNumber: "+15551234567",
          publicWebhookUrl: "https://gateway.example.com/webhooks/sms/support",
          webhookPath: "/webhooks/sms/support",
          dmPolicy: "allowlist",
          allowFrom: ["+15557654321"],
        },
      },
    },
  },
}
```

## Troubleshooting

- **Twilio returns 403 or OpenClaw rejects the webhook** — check that `publicWebhookUrl` exactly matches the URL configured in Twilio (scheme, host, path, query string). Twilio signs the public URL string, so proxy rewrites and alternate hostnames break signature validation.
- **No pairing request appears** — check the Twilio number's **Messaging** webhook URL and method (it must point to the SMS webhook URL and use `POST`), and confirm the Gateway is reachable from the public internet or through your tunnel. If the Twilio message log shows error `11200`, Twilio accepted the inbound SMS but could not reach your webhook; verify **Messaging > A message comes in** points at `publicWebhookUrl`, the method is `POST`, the tunnel/reverse proxy exposes the exact `webhookPath` (for Tailscale Funnel, run `tailscale funnel status` and confirm `/webhooks/sms` is listed), and `publicWebhookUrl` uses the same scheme, host, path, and query string Twilio sends so signature validation can reproduce the signed URL.
- **Outbound sends fail** — confirm `accountSid`, `authToken`, and either `fromNumber` or `messagingServiceSid` are resolved. On a trial Twilio account the destination number may need to be verified in Twilio before outbound SMS will send.
- **Messages arrive but the agent does not answer** — check `dmPolicy` and `allowFrom`. With the default `pairing` policy the sender must be approved before normal agent turns are processed.

**Source**: OpenClaw documentation — `channels/sms` (mirror `inbox/openclaw_docs/channels/sms.md`)
**Last Updated**: 2026-06-22
**Status**: Active
