---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - fly
keywords:
  - openclaw fly.io deploy
  - fly.toml gateway config
  - fly volumes secrets
  - openclaw_gateway_token bind lan
  - openclaw_state_dir persistent volume
  - fly private deployment hardened
  - fly machine update troubleshooting
  - fly proxy wireguard ssh access
topics:
  - OpenClaw
  - Install
  - Fly.io
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/fly
access_control_group: ["general"]
---

# OpenClaw — Deploy on Fly.io

## Overview

This note is the step-by-step **procedure** for running the OpenClaw Gateway on a [Fly.io](https://fly.io) machine with persistent storage, automatic HTTPS, and Discord/channel access, mirroring the `install/fly` source page. It covers what you need (flyctl, Fly account, model + channel credentials), the beginner quick path (clone → `fly.toml` → app + volume → secrets → `fly deploy` → first-run config), Troubleshooting (listen address, health checks, OOM, gateway lock, config-read, SSH config writes, state persistence), Updates (`fly deploy` and `fly machine update`), the hardened **private deployment** (no public IP, accessed via proxy/WireGuard/SSH, webhooks via tunnels), and Notes / Cost. The full 27 source fences are reproduced selectively here (≤6) with link-out to the source page for the complete sequence.

## What you need

- [flyctl CLI](https://fly.io/docs/hands-on/install-flyctl/) installed.
- Fly.io account (free tier works).
- Model auth: API key for your chosen model provider.
- Channel credentials: Discord bot token, Telegram token, etc.

## Beginner quick path

The high-level path is: (1) clone repo → customize `fly.toml`; (2) create app + volume → set secrets; (3) deploy with `fly deploy`; (4) SSH in to create config or use Control UI. The source documents this as six nested `<Steps>`.

**Step 1 — Create the Fly app.** Clone the repo, create a Fly app (pick your own name), and create a persistent 1GB volume. Choose a region close to you — common options: `lhr` (London), `iad` (Virginia), `sjc` (San Jose).

```bash
# Clone the repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Create a new Fly app (pick your own name)
fly apps create my-openclaw

# Create a persistent volume (1GB is usually enough)
fly volumes create openclaw_data --size 1 --region iad
```

**Step 2 — Configure `fly.toml`.** Edit `fly.toml` to match your app name and requirements. **Security note:** the default config exposes a public URL; for a hardened deployment with no public IP, see [Private deployment (hardened)](#private-deployment-hardened) below or use `deploy/fly.private.toml`.

```toml
app = "my-openclaw"  # Your app name
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  OPENCLAW_PREFER_PNPM = "1"
  OPENCLAW_STATE_DIR = "/data"
  NODE_OPTIONS = "--max-old-space-size=1536"

[processes]
  app = "node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[vm]]
  size = "shared-cpu-2x"
  memory = "2048mb"

[mounts]
  source = "openclaw_data"
  destination = "/data"
```

The OpenClaw Docker image uses `tini` as its entrypoint; Fly process commands replace Docker `CMD` without replacing `ENTRYPOINT`, so the process still runs under `tini`. Key settings: `--bind lan` binds to `0.0.0.0` so Fly's proxy can reach the gateway; `--allow-unconfigured` starts without a config file (you create one after); `internal_port = 3000` must match `--port 3000` (or `OPENCLAW_GATEWAY_PORT`) for Fly health checks; `memory = "2048mb"` because 512MB is too small (2GB recommended); `OPENCLAW_STATE_DIR = "/data"` persists state on the volume.

**Step 3 — Set secrets.** Set the gateway token (required for non-loopback binding), model provider API keys, and channel tokens as Fly secrets. The source uses example-only placeholder values for keys.

```bash
# Required: Gateway token (for non-loopback binding)
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)

# Model provider API keys
fly secrets set ANTHROPIC_API_KEY=example-anthropic-key-not-real

# Optional: Other providers
fly secrets set OPENAI_API_KEY=example-openai-key-not-real
fly secrets set GOOGLE_API_KEY=...

# Channel tokens
fly secrets set DISCORD_BOT_TOKEN=example-discord-bot-token
```

Notes on secrets: non-loopback binds (`--bind lan`) require a valid gateway auth path — this Fly.io example uses `OPENCLAW_GATEWAY_TOKEN`, but `gateway.auth.password` or a correctly configured non-loopback `trusted-proxy` deployment also satisfy the requirement. Treat these tokens like passwords. **Prefer env vars over config file** for all API keys and tokens, to keep secrets out of `openclaw.json` where they could be accidentally exposed or logged.

**Step 4 — Deploy.** Run `fly deploy`. The first deploy builds the Docker image (~2-3 minutes); subsequent deploys are faster. After deployment verify with `fly status` and `fly logs`. You should see lines like `[gateway] listening on ws://0.0.0.0:3000 (PID xxx)` and `[discord] logged in to discord as xxx`.

**Step 5 — Create config file.** SSH into the machine (`fly ssh console`), create `/data`, and write `/data/openclaw.json`. With `OPENCLAW_STATE_DIR=/data` the config path is `/data/openclaw.json`. Replace `https://my-openclaw.fly.dev` with your real Fly app origin — gateway startup seeds local Control UI origins from the runtime `--bind`/`--port` values so first boot can proceed before config exists, but browser access through Fly still needs the exact HTTPS origin listed in `gateway.controlUi.allowedOrigins`. The Discord token can come from the `DISCORD_BOT_TOKEN` env var (recommended) or the config file `channels.discord.token`; with the env var the gateway reads it automatically. After writing, `exit` and `fly machine restart <machine-id>` to apply.

```bash
fly ssh console
mkdir -p /data
cat > /data/openclaw.json << 'EOF'
{
  "agents": { "defaults": { "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["anthropic/claude-sonnet-4-6", "openai/gpt-5.4"] },
      "maxConcurrent": 4 },
    "list": [ { "id": "main", "default": true } ] },
  "auth": { "profiles": {
      "anthropic:default": { "mode": "token", "provider": "anthropic" },
      "openai:default": { "mode": "token", "provider": "openai" } } },
  "bindings": [ { "agentId": "main", "match": { "channel": "discord" } } ],
  "channels": { "discord": {
      "enabled": true, "groupPolicy": "allowlist",
      "guilds": { "YOUR_GUILD_ID": {
          "channels": { "general": { "allow": true } },
          "requireMention": false } } } },
  "gateway": { "mode": "local", "bind": "auto",
    "controlUi": { "allowedOrigins": [
        "https://my-openclaw.fly.dev",
        "http://localhost:3000", "http://127.0.0.1:3000" ] } },
  "meta": {}
}
EOF
```

**Step 6 — Access the Gateway.** Open the Control UI with `fly open` (or visit `https://my-openclaw.fly.dev/`) and authenticate with the configured shared secret — this guide uses the gateway token from `OPENCLAW_GATEWAY_TOKEN`; if you switched to password auth, use that password. View logs with `fly logs` (live) or `fly logs --no-tail` (recent). Open an SSH console with `fly ssh console`.

## Troubleshooting

- **"App is not listening on expected address"** — the gateway is binding to `127.0.0.1` instead of `0.0.0.0`. Fix: add `--bind lan` to your process command in `fly.toml`.
- **Health checks failing / connection refused** — Fly can't reach the gateway on the configured port. Fix: ensure `internal_port` matches the gateway port (set `--port 3000` or `OPENCLAW_GATEWAY_PORT=3000`).
- **OOM / Memory Issues** — container keeps restarting or getting killed; signs are `SIGABRT`, `v8::internal::Runtime_AllocateInYoungGeneration`, or silent restarts. Fix: increase memory in `fly.toml` (`[[vm]] memory = "2048mb"`), or update an existing machine with `fly machine update <machine-id> --vm-memory 2048 -y`. 512MB is too small; 1GB may work but can OOM under load or with verbose logging; **2GB is recommended.**
- **Gateway lock issues** — gateway refuses to start with "already running" errors, which happens when the container restarts but the PID lock file persists on the volume. Fix: delete the lock file (`fly ssh console --command "rm -f /data/gateway.*.lock"`) then `fly machine restart <machine-id>`. The lock file is at `/data/gateway.*.lock` (not in a subdirectory).
- **Config not being read** — `--allow-unconfigured` only bypasses the startup guard; it does not create or repair `/data/openclaw.json`, so make sure your real config exists and includes `gateway.mode="local"` for a normal local gateway start. Verify with `fly ssh console --command "cat /data/openclaw.json"`.
- **Writing config via SSH** — `fly ssh console -C` doesn't support shell redirection. To write a config file, pipe from local to remote with `echo '{"your":"config"}' | fly ssh console -C "tee /data/openclaw.json"`, or use `fly sftp shell` then `put /local/path/config.json /data/openclaw.json`. `fly sftp` may fail if the file already exists — delete it first with `fly ssh console --command "rm /data/openclaw.json"`.
- **State not persisting** — if you lose auth profiles, channel/provider state, or sessions after a restart, the state dir is writing to the container filesystem. Fix: ensure `OPENCLAW_STATE_DIR=/data` is set in `fly.toml` and redeploy.

## Updates

Routine update flow: `git pull` for the latest changes, `fly deploy` to redeploy, then check health with `fly status` and `fly logs`.

### Updating machine command

To change the startup command without a full redeploy, get the machine ID with `fly machines list`, then update the command:

```bash
# Update command
fly machine update <machine-id> --command "node dist/index.js gateway --port 3000 --bind lan" -y

# Or with memory increase
fly machine update <machine-id> --vm-memory 2048 --command "node dist/index.js gateway --port 3000 --bind lan" -y
```

After `fly deploy`, the machine command may reset to what's in `fly.toml`; if you made manual changes, re-apply them after deploy.

## Private deployment (hardened)

By default Fly allocates public IPs, making the gateway accessible at `https://your-app.fly.dev` — convenient but discoverable by internet scanners (Shodan, Censys, etc.). For a hardened deployment with **no public exposure**, use the private template.

**When to use private deployment** — you only make **outbound** calls/messages (no inbound webhooks); you use **ngrok or Tailscale** tunnels for any webhook callbacks; you access the gateway via **SSH, proxy, or WireGuard** instead of a browser; or you want the deployment **hidden from internet scanners**.

**Setup** — use `deploy/fly.private.toml` instead of the standard config (`fly deploy -c deploy/fly.private.toml`). To convert an existing deployment, list current IPs (`fly ips list -a my-openclaw`), release the public IPs (`fly ips release <public-ipv4> -a my-openclaw` and the `<public-ipv6>`), switch to the private config so future deploys don't re-allocate public IPs (remove `[http_service]` or deploy with the private template), then allocate a private-only IPv6 (`fly ips allocate-v6 --private -a my-openclaw`). Afterward `fly ips list` should show only a `private` type IP (e.g. `v6  fdaa:x:x:x:x::x  private  global`).

**Accessing a private deployment** — since there is no public URL, use one of: **Option 1 (simplest)** local proxy `fly proxy 3000:3000 -a my-openclaw` then open `http://localhost:3000`; **Option 2** WireGuard VPN — `fly wireguard create` (one-time), import to a WireGuard client, then access via internal IPv6 (e.g. `http://[fdaa:x:x:x:x::x]:3000`); **Option 3** SSH only — `fly ssh console -a my-openclaw`.

**Webhooks with private deployment** — if you need webhook callbacks (Twilio, Telnyx, etc.) without public exposure: (1) **ngrok tunnel** run inside the container or as a sidecar; (2) **Tailscale Funnel** to expose specific paths; or (3) **outbound-only** (some providers like Twilio work fine for outbound calls without webhooks). Example voice-call config with ngrok — the tunnel runs inside the container and provides a public webhook URL without exposing the Fly app itself; set `webhookSecurity.allowedHosts` to the public tunnel hostname so forwarded host headers are accepted:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio",
          tunnel: { provider: "ngrok" },
          webhookSecurity: {
            allowedHosts: ["example.ngrok.app"],
          },
        },
      },
    },
  },
}
```

**Security benefits** — a public deployment is discoverable by internet scanners, open to direct attacks, accesses the Control UI via the browser, and delivers webhooks directly; a private deployment is hidden from scanners, blocks direct attacks, accesses the Control UI via proxy/VPN, and delivers webhooks via tunnel.

## Notes, Cost, and Next steps

**Notes:** Fly.io uses **x86 architecture** (not ARM); the Dockerfile is compatible with both architectures. For WhatsApp/Telegram onboarding, use `fly ssh console`. Persistent data lives on the volume at `/data`. Signal requires Java + signal-cli — use a custom image and keep memory at 2GB+.

**Cost:** with the recommended config (`shared-cpu-2x`, 2GB RAM), roughly **$10-15/month** depending on usage; the free tier includes some allowance. See [Fly.io pricing](https://fly.io/docs/about/pricing/) for details.

**Next steps:** set up messaging channels ([Channels](https://docs.openclaw.ai/channels)), configure the Gateway ([Gateway configuration](https://docs.openclaw.ai/gateway/configuration)), and keep OpenClaw up to date ([Updating](https://docs.openclaw.ai/install/updating)).

**Source**: OpenClaw documentation — `install/fly` (mirror `inbox/openclaw_docs/install/fly.md`)
**Last Updated**: 2026-06-22
**Status**: Active
