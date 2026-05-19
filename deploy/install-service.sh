#!/usr/bin/env bash
# install-service.sh: install (or reinstall) the tv-web systemd service.
# Run as root or via sudo.
set -euo pipefail

UNIT_SRC="$(cd "$(dirname "$0")" && pwd)/tv-web.service"
UNIT_DST="/etc/systemd/system/tv-web.service"

echo "[install] Copying ${UNIT_SRC} -> ${UNIT_DST}"
cp "$UNIT_SRC" "$UNIT_DST"

echo "[install] Reloading systemd daemon ..."
systemctl daemon-reload

echo "[install] Enabling and starting tv-web ..."
systemctl enable --now tv-web.service

echo ""
echo "[install] Done. Useful commands:"
echo "  systemctl status  tv-web"
echo "  journalctl -u tv-web -f"
echo "  systemctl restart tv-web"
echo "  systemctl stop    tv-web"
echo "  systemctl disable tv-web"
