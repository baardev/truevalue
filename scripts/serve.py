#!/usr/bin/env python3
"""
serve.py: dual HTTP + HTTPS static file server for the TrueValue Analytics repo.

HTTP  -> port 8000 (redirects to HTTPS)
HTTPS -> port 8443 (serves files from WEBROOT)

A self-signed certificate is generated automatically in CERT_DIR if absent.
For production, replace the generated cert/key with a real certificate.

Usage:
    python3 scripts/serve.py [--http PORT] [--https PORT] [--bind HOST]
    python3 scripts/serve.py --http-only      # plain HTTP only, no redirect
    python3 scripts/serve.py --https-only     # HTTPS only
"""

import argparse
import http.server
import ipaddress
import os
import socket
import ssl
import subprocess
import sys
import threading
from pathlib import Path

WEBROOT   = Path(__file__).resolve().parent.parent   # repo root
CERT_DIR  = WEBROOT / ".certs"
CERT_FILE = CERT_DIR / "server.crt"
KEY_FILE  = CERT_DIR / "server.key"

DEFAULT_HTTP_PORT  = 8000
DEFAULT_HTTPS_PORT = 8443
DEFAULT_BIND       = "127.0.0.1"


# ---------------------------------------------------------------------------
# Certificate generation
# ---------------------------------------------------------------------------

def generate_self_signed_cert(bind_host: str) -> None:
    """Generate a self-signed cert/key pair via openssl if not already present."""
    CERT_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    if CERT_FILE.exists() and KEY_FILE.exists():
        return

    # Decide the Subject Alt Name based on the bind address.
    try:
        addr = ipaddress.ip_address(bind_host)
        san = f"IP:{addr}"
    except ValueError:
        san = f"DNS:{bind_host}"

    san_cfg = CERT_DIR / "san.cnf"
    san_cfg.write_text(
        "[req]\n"
        "distinguished_name = req_distinguished_name\n"
        "x509_extensions    = v3_req\n"
        "prompt             = no\n"
        "[req_distinguished_name]\n"
        "CN = TrueValue Analytics Dev\n"
        "[v3_req]\n"
        "subjectAltName = " + san + "\n"
        "keyUsage = digitalSignature, keyEncipherment\n"
        "extendedKeyUsage = serverAuth\n"
    )

    cmd = [
        "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
        "-keyout", str(KEY_FILE),
        "-out",    str(CERT_FILE),
        "-days",   "3650",
        "-config", str(san_cfg),
    ]
    print(f"[cert] Generating self-signed certificate in {CERT_DIR} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[cert] openssl error:\n" + result.stderr, file=sys.stderr)
        sys.exit(1)
    os.chmod(KEY_FILE, 0o600)
    san_cfg.unlink(missing_ok=True)
    print(f"[cert] Certificate written to {CERT_FILE}")


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------

class RepoHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files from WEBROOT; suppress most access log noise."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEBROOT), **kwargs)

    def log_message(self, fmt, *args):
        # Keep the output readable: skip 304 and asset noise if desired.
        sys.stdout.write(f"[http ] {self.address_string()} {fmt % args}\n")
        sys.stdout.flush()


class RedirectHandler(http.server.BaseHTTPRequestHandler):
    """Redirect every HTTP request to the HTTPS counterpart."""

    https_port: int = DEFAULT_HTTPS_PORT

    def do_GET(self):
        self._redirect()

    def do_HEAD(self):
        self._redirect()

    def do_POST(self):
        self._redirect()

    def _redirect(self):
        host = self.headers.get("Host", self.server.server_address[0])
        # Strip any port already in Host.
        host = host.split(":")[0]
        target = f"https://{host}:{self.https_port}{self.path}"
        self.send_response(301)
        self.send_header("Location", target)
        self.end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[redir] {self.address_string()} {fmt % args}\n")
        sys.stdout.flush()


# ---------------------------------------------------------------------------
# Server builders
# ---------------------------------------------------------------------------

def make_https_server(bind: str, port: int) -> http.server.HTTPServer:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=str(CERT_FILE), keyfile=str(KEY_FILE))
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    srv = http.server.HTTPServer((bind, port), RepoHandler)
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    return srv


def make_http_server(bind: str, port: int, https_port: int) -> http.server.HTTPServer:
    RedirectHandler.https_port = https_port
    return http.server.HTTPServer((bind, port), RedirectHandler)


def make_plain_http_server(bind: str, port: int) -> http.server.HTTPServer:
    return http.server.HTTPServer((bind, port), RepoHandler)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bind",        default=DEFAULT_BIND,
                   help=f"Bind address (default: {DEFAULT_BIND})")
    p.add_argument("--http",        type=int, default=DEFAULT_HTTP_PORT, metavar="PORT",
                   help=f"HTTP port (default: {DEFAULT_HTTP_PORT})")
    p.add_argument("--https",       type=int, default=DEFAULT_HTTPS_PORT, metavar="PORT",
                   help=f"HTTPS port (default: {DEFAULT_HTTPS_PORT})")
    p.add_argument("--http-only",   action="store_true",
                   help="Plain HTTP only (no redirect, no HTTPS)")
    p.add_argument("--https-only",  action="store_true",
                   help="HTTPS only (no HTTP redirect listener)")
    return p.parse_args()


def serve_in_thread(server: http.server.HTTPServer, label: str) -> threading.Thread:
    t = threading.Thread(target=server.serve_forever, name=label, daemon=True)
    t.start()
    return t


def main() -> None:
    args = parse_args()

    bind       = args.bind
    http_port  = args.http
    https_port = args.https

    servers = []

    if args.http_only:
        srv = make_plain_http_server(bind, http_port)
        print(f"[serve] HTTP  http://{bind}:{http_port}/  (root: {WEBROOT})")
        servers.append((srv, "http-plain"))
    else:
        generate_self_signed_cert(bind)

        if not args.https_only:
            http_srv = make_http_server(bind, http_port, https_port)
            print(f"[serve] HTTP  http://{bind}:{http_port}/  -> redirects to HTTPS")
            servers.append((http_srv, "http-redirect"))

        https_srv = make_https_server(bind, https_port)
        print(f"[serve] HTTPS https://{bind}:{https_port}/  (root: {WEBROOT})")
        servers.append((https_srv, "https"))

    if not servers:
        print("Nothing to serve. Check your flags.", file=sys.stderr)
        sys.exit(1)

    print("[serve] Press Ctrl-C to stop.\n")

    threads = [serve_in_thread(srv, lbl) for srv, lbl in servers]

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n[serve] Shutting down ...")
        for srv, _ in servers:
            srv.shutdown()


if __name__ == "__main__":
    main()
