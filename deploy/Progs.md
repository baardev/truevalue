# Programming manual (`deploy/`)

Executable scripts in this folder. Invocation details live in script headers; this file describes what each program is for.

## `install-service.sh`

Installs the **`tv-web`** systemd unit: copies `tv-web.service` into `/etc/systemd/system/`, reloads systemd, then enables and starts the service. Intended to be run as root (for example with `sudo`).

**Depends on:** `bash`, `systemctl`, `cp`.

## `protected-paths.json`

Lists URL path prefixes that require HTTP Basic Auth when served by `scripts/serve.py`. Currently includes AUBEB and Senegal Agroforestry.

## `auth.env.example`

Template for credentials. Copy to `auth.env` (gitignored) and set `TV_AUTH_USER` and `TV_AUTH_PASSWORD`. Loaded by `serve.py` and optionally by the `tv-web` systemd unit via `EnvironmentFile`.
