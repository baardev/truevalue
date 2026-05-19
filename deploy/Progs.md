# Programming manual (`deploy/`)

Executable scripts in this folder. Invocation details live in script headers; this file describes what each program is for.

## `install-service.sh`

Installs the **`tv-web`** systemd unit: copies `tv-web.service` into `/etc/systemd/system/`, reloads systemd, then enables and starts the service. Intended to be run as root (for example with `sudo`).

**Depends on:** `bash`, `systemctl`, `cp`.
