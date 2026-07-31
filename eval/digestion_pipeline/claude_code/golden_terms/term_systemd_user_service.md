---
tags:
  - resource
  - terminology
  - infrastructure
  - devops
keywords:
  - systemd user services
  - systemd --user
  - systemctl --user
  - user@.service
  - user unit
  - XDG_RUNTIME_DIR
  - loginctl enable-linger
  - per-user systemd instance
topics:
  - infrastructure
  - Linux
  - DevOps
language: markdown
date of note: 2026-06-24
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# systemd user services — Per-User systemd Service Manager Instance (freedesktop.org)

## Definition

**systemd user services** are units (services, timers, sockets, and other unit types) managed by a per-user instance of the systemd manager — `systemd --user`, started by PID 1 as `user@UID.service` — rather than by the system manager. The per-user instance is the same `systemd` executable as the system manager but operates over a separate, user-owned unit set, letting an unprivileged user start, stop, enable, and disable their own daemons and scheduled tasks with the full feature set of systemd: dependency ordering, socket activation, timers, and cgroup-based process control. This solves the problem of running long-lived, restart-on-failure, boot-persistent background processes **without root, sudo, or any system-level unit file** — the privilege escalation that system units would otherwise require. Developers managing personal daemons on shared multi-user Linux hosts are the primary users.

The per-user instance is normally spawned by `pam_systemd` when the user logs in and is torn down when the user's last session ends, so it depends on two pieces of supporting state. First, it needs `XDG_RUNTIME_DIR` (conventionally `/run/user/UID`, created and removed by the companion `user-runtime-dir@UID.service`) to host its private D-Bus socket; without it, `systemctl --user` fails with `Failed to get D-Bus connection: Connection refused`. Second, because the instance dies with the last session, `loginctl enable-linger <user>` is required to start it at boot and keep it (and its services) running across SSH disconnects and logouts.

## Context

User-level systemd is commonly favored over system-level units on modern multi-user Linux hosts: on distributions shipping systemd 252+ (e.g. Amazon Linux 2023, RHEL 9), `systemctl --user` plus `loginctl enable-linger` gives functional equivalence to system units — boot persistence and SSH-disconnect survival — with no sudo or root needed. On the deeper mechanics: a `--user` instance is triggered by one of three paths (a PAM login via `pam_systemd`, lingering, or a GUI display manager), per-distro `pam_systemd` defaults differ, and `systemctl --user` fails when run as root because there is no `/run/user/0` user bus. By contrast, system-scoped units are owned by PID 1's system manager, not the per-user manager described here.

## Key Characteristics

- Managed by a per-user `systemd --user` instance launched by PID 1 as `user@UID.service`; same executable as the system manager but a disjoint unit set.
- Controlled with `systemctl --user <verb>` (start/stop/enable/disable/status); enabling persists the unit's wanted-by link in the user's config.
- User unit files live under `~/.config/systemd/user/` (plus other XDG/system user-unit search paths).
- Requires `XDG_RUNTIME_DIR` (= `/run/user/UID`, created by `user-runtime-dir@UID.service`) for the per-user D-Bus socket; missing it yields `Failed to get D-Bus connection: Connection refused`.
- The instance is started by `pam_systemd` on first login and dies with the user's last session **unless lingering is enabled** via `loginctl enable-linger <user>`, which also makes it start at boot.
- Processes are collected under `user-UID.slice` within `user.slice`, giving cgroup-based resource accounting and control.
- User units **cannot depend on system units** and **do not inherit shell environment variables** — environment must be set explicitly in the unit or via `systemctl --user import-environment`.
- Cannot be managed as `root` (UID 0 has no `/run/user/0` bus by default); the user instance is per real-UID.

## Related Terms


## References

- [freedesktop.org systemd man: user@.service](https://www.freedesktop.org/software/systemd/man/latest/user@.service.html)
- [Arch Wiki: systemd/User](https://wiki.archlinux.org/title/Systemd/User)

---

**Last Updated**: June 24, 2026
**Status**: Active
