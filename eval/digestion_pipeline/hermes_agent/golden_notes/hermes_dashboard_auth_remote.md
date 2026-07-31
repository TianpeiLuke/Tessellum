---
tags:
  - resource
  - documentation
  - hermes_agent
  - authentication
  - web_dashboard
keywords:
  - dashboard auth gate
  - gated mode
  - DashboardAuthProvider
  - username password provider
  - self-hosted OIDC
  - remote backend Hermes Desktop
  - public_url override
  - fail-closed bind
topics:
  - Hermes Agent
  - Web Dashboard
  - Authentication
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
access_control_group: ["general"]
---

# Hermes Dashboard — Authentication & Remote Backend

## Overview

This is the procedure for **securing a non-loopback `hermes dashboard`** and **wiring Hermes Desktop to a remote backend**. A loopback dashboard (the default `127.0.0.1` bind) ships with no login; bind it to a reachable address and it engages an **auth gate** that bounces every unauthenticated request to `/login`. Three `DashboardAuthProvider`s ship in the box — **Nous Portal OAuth**, a bundled **username/password** provider, and a **self-hosted OIDC** provider — and the gate **fails closed**: if it would engage but no provider is registered, `hermes dashboard` refuses to bind. Once a user signs in, Hermes Desktop reuses that session for the live chat WebSocket automatically (no token to copy), which is why "remote backend ready but chat never works" is almost always an auth-gate or bind-host problem, not a Desktop bug. Everything here applies to the same FastAPI server fronted by [hermes_dashboard_rest_api](hermes_dashboard_rest_api.md) and toured by [hermes_web_dashboard_overview](hermes_web_dashboard_overview.md); OAuth/PKCE internals and Nous Portal billing are linked, not duplicated.

## When the Gate Engages

The dashboard engages its auth gate when bound to a non-loopback address — anything other than `127.0.0.1` / `localhost`. Loopback dashboards are unaffected (no auth, no login page).

| Flags | Auth gate | Use case |
|-------|-----------|----------|
| `hermes dashboard` (default — binds to `127.0.0.1`) | OFF | Local development |
| `hermes dashboard --host 0.0.0.0` | **ON** | Remote / production — protect with username/password or OAuth |

The gate is on iff (1) the bind host is not `127.0.0.1`, `::1`, `localhost`, or `0.0.0.0`, **and** (2) `--insecure` is **not** set. `--insecure` skips the gate and serves an unauthenticated dashboard that reads/writes your `.env` and can run agent commands — a last-resort escape hatch for a trusted, firewalled single-host network, never for a remote connection.

## Fail-Closed Semantics

If the gate would engage but **no** `DashboardAuthProvider` is registered, `hermes dashboard` refuses to bind with an explicit error. There is no "default-deny but accept everything" fallback — a misconfigured gated dashboard never starts:

```
Refusing to bind dashboard to 0.0.0.0 — the OAuth auth gate engages on
non-loopback binds, but no auth providers are registered.

Bundled providers reported these issues:
  • nous: HERMES_DASHBOARD_OAUTH_CLIENT_ID is not set (and
    dashboard.oauth.client_id in config.yaml is empty). …set it…
    or pass --insecure to skip the OAuth gate entirely.

Or pass --insecure to skip the auth gate (NOT recommended on untrusted
networks).
```

## The Three Bundled Providers

Each provider plugs into the same gate. All read two surfaces — `config.yaml` (canonical) and environment variables — with the **env var winning when set non-empty** (an empty env value is unset, so a provisioned-but-empty platform secret can't shadow a valid `config.yaml` entry). The login page lists every registered provider; multiple can be stacked.

- **Nous Research (OAuth)** — `plugins/dashboard_auth/nous`, **always installed and auto-loaded**, registers a provider `nous` once an OAuth client ID (shape `agent:{id}`) is configured. Verified against your Nous account, so it is **suitable for public-internet exposure** and the recommended remote-Desktop path. Get a client ID with `hermes dashboard register` (writes `HERMES_DASHBOARD_OAUTH_CLIENT_ID` into `~/.hermes/.env`; optional `--name`/`--redirect-uri`) or the Portal's [`/local-dashboards`](https://portal.nousresearch.com/local-dashboards) GUI.
- **Username/password** — `plugins/dashboard_auth/basic`, a provider `basic` using a username + password instead of an OAuth redirect. Sessions are stateless HMAC-signed tokens it mints itself (**no database, no external IDP**); hashing uses stdlib `scrypt`. Activates only when `username` plus `password_hash` (preferred) or `password` are set. **Trusted network / VPN only — not for public exposure** (single shared credential, no MFA). `/auth/password-login` is rate-limited per IP (default 10/min → 429) and returns one generic `401 Invalid credentials` for unknown users and wrong passwords alike, so it isn't an enumeration oracle.
- **Self-hosted OIDC** — `plugins/dashboard_auth/self_hosted`, authenticates against any conformant OpenID Connect server (Authentik, Keycloak, Zitadel, Authelia, Auth0, Okta, Google, …) using a **public PKCE client (no client secret)**. You configure only `issuer` and `client_id`; the plugin fetches `authorization_endpoint`/`token_endpoint`/`jwks_uri` from `{issuer}/.well-known/openid-configuration`, then verifies the OIDC **ID token** (RS256/ES256) against the `jwks_uri` with `iss`/`aud` pinned. Confidential clients (with a `client_secret`) are **not supported yet**.

## Provider Configuration

The Nous provider needs only `dashboard.oauth.client_id` in `config.yaml` (`agent:01HXYZ…`), env override `HERMES_DASHBOARD_OAUTH_CLIENT_ID` winning — that single value engages the gate and activates `nous`.

The username/password provider reads `config.yaml` (env overrides `HERMES_DASHBOARD_BASIC_AUTH_{USERNAME,PASSWORD_HASH,PASSWORD,SECRET,TTL_SECONDS}` win):

```yaml
dashboard:
  basic_auth:
    username: admin
    # Preferred — no plaintext at rest:
    #   python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('PW'))"
    password_hash: "scrypt$16384$8$1$…$…"
    # password: "s3cret"                 # ...or plaintext (hashed in-memory at load; less safe at rest)
    secret: "<32+ random bytes, base64 or hex>"  # token-signing key
    session_ttl_seconds: 43200                    # optional; access-token lifetime (default 12h)
```

An empty `secret` generates a random per-process signing key, so **sessions are invalidated on restart** and don't span workers — set an explicit `secret` for restart-surviving / multi-worker deployments. The plaintext `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` **wins over a config `password_hash`** so you can rotate via env.

The self-hosted OIDC provider needs only an issuer + public client (register `<public URL>/auth/callback` as a redirect URI in your IDP, code + PKCE/S256 grant):

```yaml
dashboard:
  oauth:
    provider: self-hosted
    self_hosted:
      issuer: https://auth.example.com/application/o/hermes/   # required
      client_id: hermes-dashboard                              # required
      scopes: "openid profile email"                           # optional (this is the default)
```

Env overrides: `HERMES_DASHBOARD_OIDC_{ISSUER,CLIENT_ID,SCOPES}`. OIDC claims map onto the session (`sub`→`user_id`, `email`, `name`/`preferred_username`/`nickname`→`display_name`, `org_id`/`groups`→`org_id`). Endpoints must be HTTPS (loopback `http://` allowed for local-dev IDPs), the discovery `issuer` must match the configured one, and refresh tokens (when issued) drive silent re-auth.

## Writing Your Own Provider

`basic` is one implementation of an extension point. Any plugin can register a **password** provider: set `supports_password = True` on a `DashboardAuthProvider` subclass and implement `complete_password_login(*, username, password) -> Session` (OAuth methods can stay `NotImplementedError` stubs). For a non-Nous **OAuth** provider, register a full `DashboardAuthProvider`:

```python
# ~/.hermes/plugins/dashboard-auth-myidp/__init__.py
from hermes_cli.dashboard_auth import DashboardAuthProvider, Session, LoginStart

class MyIdPProvider(DashboardAuthProvider):
    name = "myidp"
    display_name = "My Identity Provider"

    def start_login(self, *, redirect_uri): ...
    def complete_login(self, *, code, state, code_verifier, redirect_uri): ...
    def verify_session(self, *, access_token): ...
    def refresh_session(self, *, refresh_token): ...
    def revoke_session(self, *, refresh_token): ...

def register(ctx):
    ctx.register_dashboard_auth_provider(MyIdPProvider())
```

The framework handles the form, route, cookies, and refresh — the path for LDAP-bind, a credentials database, or any non-redirect scheme.

## OAuth Flow, Cookies, Logout & Audit Log

The Nous provider implements the Nous Portal OAuth contract v1 — authorization-code grant with PKCE (S256): unauthenticated `/` → `/login`; "Continue with Nous Research" → `/auth/login?provider=nous`; the server stashes PKCE state in a short-lived cookie and redirects to the Portal `/oauth/authorize`; the callback exchanges the code at `POST /api/oauth/token`, verifies the JWT against the Portal's JWKS, and sets `hermes_session_at`. **Access tokens have a 15-min TTL and there is no refresh token in contract v1** — on expiry the SPA detects the `401` and navigates back to `/login`.

| Cookie | Lifetime | Notes |
|------|----------|-------|
| `hermes_session_at` | Token TTL (15 min) | HttpOnly, SameSite=Lax, Secure-when-HTTPS |
| `hermes_session_pkce` | 10 min | HttpOnly; holds the PKCE verifier + provider hint during the round trip |
| `hermes_session_rt` | unused in v1 | reserved for forward-compat; not written when `refresh_token` is empty |

All three are `Path=/`, `SameSite=Lax`; `Secure` is set over HTTPS (from the request URL scheme, honouring `X-Forwarded-Proto`). **Logout**: the sidebar widget POSTs `/auth/logout`, clearing all dashboard-auth cookies and redirecting to `/login`. **Audit log**: every login start/success/failure and session-verify failure is a JSON line in `$HERMES_HOME/logs/dashboard-auth.log`, with `access_token`/`refresh_token`/`code`/`code_verifier`/`state`/`Authorization` redacted.

## Public URL Override (Behind a Reverse Proxy)

By default the dashboard reconstructs the OAuth callback URL from `X-Forwarded-Host`/`-Proto`/`-Prefix` (uvicorn `proxy_headers=True`, enabled under the gate). For proxies that don't reliably forward those headers, set the complete public URL — `dashboard.public_url: "https://dashboard.example.com/hermes"` (env override `HERMES_DASHBOARD_PUBLIC_URL` wins). The callback then becomes `<public_url>/auth/callback` verbatim and `X-Forwarded-Prefix` is **ignored** (to avoid double-prefixing). Validation rejects values without a scheme/host or with quote/angle/whitespace/control characters — a malformed value silently falls through to header reconstruction rather than dispatching to a hostile URL. `public_url` overrides the **callback only**; the `Secure` cookie flag still follows `request.url.scheme`, so an `http://` `public_url` on a TLS-terminated deploy produces non-Secure cookies — pair it with upstream TLS.

## Verifying the Gate

From any machine, confirm the gate state and advertised provider:

```bash
curl -s http://<host>:9119/api/status | jq '.auth_required, .auth_providers'
# true
# ["nous"]   # or ["basic"], ["self-hosted"], …
```

`auth_required: true` plus the expected provider → sign-in works. `auth_required: false` → loopback bind or the gate didn't engage. `auth_required: true` but the provider missing → its env/config aren't loaded. `GET /api/auth/me` returns the verified session once signed in.

## Connecting Hermes Desktop to a Remote Backend

Hermes Desktop can drive a backend on another machine via **Settings → Gateway → Remote gateway** (a **Remote URL** + a way to **Sign in**). The "remote backend" Desktop attaches to **is** a `hermes dashboard` process on the remote host — the same server this page documents; it must be up and reachable first (keep it under `systemd`/`tmux`), and Desktop does not start it. The messaging **gateway** is a separate process, not what Desktop connects to.

The "Desktop says ready but chat never works" report happens because Desktop's readiness probe only hits the public `GET /api/status` (answers as soon as *any* dashboard is up), while live chat is a **separate** WebSocket to `/api/ws` (and `/api/pty`) gated by two checks the probe never touches: (1) **you must be authenticated** — a non-loopback bind engages the gate (without a provider it fails closed at startup); Desktop reuses its session for the WS via a single-use ticket; (2) **the bind host must allow the client and match the Host header** — a loopback bind rejects remote clients at the socket layer regardless of credentials, so bind non-loopback (`--host 0.0.0.0`) and use a Remote URL reaching the dashboard by the same host it bound to (the DNS-rebinding guard requires a matching Host header).

### On the Backend (Remote Machine)

The username/password path is quickest on a trusted network (for OAuth, register with `hermes dashboard register`):

```bash
# 1. Set login credentials in ~/.hermes/.env (secrets file, 0600).
cat >> ~/.hermes/.env <<'EOF'
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=admin
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=choose-a-strong-password
HERMES_DASHBOARD_BASIC_AUTH_SECRET=$(openssl rand -base64 32)   # stable → sessions survive restarts
EOF
chmod 600 ~/.hermes/.env

# 2. Run the dashboard on a reachable address: the non-loopback bind engages
#    the auth gate; the username/password provider handles login.
hermes dashboard --no-open --host 0.0.0.0 --port 9119
```

Prefer no plaintext at rest? Use `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH` with a scrypt hash. A systemd unit with `EnvironmentFile=%h/.hermes/.env` picks up the credentials at boot. **Never expose a password-protected dashboard to the open internet** — put it behind a VPN ([Tailscale](https://tailscale.com/): bind to the tailscale IP); for public reach use the OAuth (Nous Portal) provider.

### In Hermes Desktop

Under **Settings → Gateway → Remote gateway**: set **Remote URL** to `http://<backend-host>:9119` (reverse-proxy path prefixes like `/hermes` are supported), click **Sign in** (enter the step-1 credentials), then **Save and reconnect**. The session refreshes automatically and survives restarts when `HERMES_DASHBOARD_BASIC_AUTH_SECRET` is set. Alternatively set `HERMES_DESKTOP_REMOTE_URL` before launching Desktop — it overrides the saved in-app URL (the panel shows an "env override" badge); you still **Sign in** from the panel.

### Troubleshooting

- **"Remote gateway incomplete"** — no Remote URL.
- **Sign-in fails with 401 / "Invalid credentials"** — username or password doesn't match the backend's `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` / `..._PASSWORD` (same generic error for both cases; check both). Confirm with `/api/status` → expect `true` and `"basic"`.
- **No "Sign in" button — asks for a session token** — the `basic` provider isn't active (`/api/status` won't list `"basic"`); set username + password (or hash) and confirm the process loaded them.
- **Signed out on every restart** — set a stable `HERMES_DASHBOARD_BASIC_AUTH_SECRET`.
- **Connection refused / times out** — the backend bound to `127.0.0.1`, or a firewall/VPN blocks the port; bind to `0.0.0.0` and open the port.
- **`/api/ws` close codes** (in `desktop.log` + dashboard logs from the same retry): **4403** = WS rejected by the request guard (Host/peer mismatch); **4401** = the WS ticket didn't authenticate.

**Source**: `inbox/hermes_agent_docs/user-guide/features/web-dashboard.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
**Last Updated**: 2026-06-19
**Status**: Active
