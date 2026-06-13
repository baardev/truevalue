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
import base64
import http.server
import ipaddress
import json
import os
import secrets
import socket
import ssl
import subprocess
import sys
import threading
import urllib.parse
from pathlib import Path

WEBROOT   = Path(__file__).resolve().parent.parent   # repo root
CERT_DIR  = WEBROOT / ".certs"
CERT_FILE = CERT_DIR / "server.crt"
KEY_FILE  = CERT_DIR / "server.key"
PROTECTED_PATHS_FILE = WEBROOT / "deploy" / "protected-paths.json"
AUTH_ENV_FILES = (
    WEBROOT / "deploy" / "auth.env",
    WEBROOT / ".env",
)

DEFAULT_HTTP_PORT  = 8000
DEFAULT_HTTPS_PORT = 8443
DEFAULT_BIND       = "127.0.0.1"
AUTH_REALM         = "TrueValue Protected Projects"


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
# Protected path configuration
# ---------------------------------------------------------------------------

def _load_dotenv_file(path: Path) -> None:
    """Merge KEY=VALUE pairs from a dotenv-style file into os.environ."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def load_auth_credentials() -> tuple[str, str] | None:
    """Return (user, password) when configured, else None."""
    for env_file in AUTH_ENV_FILES:
        _load_dotenv_file(env_file)
    user = os.environ.get("TV_AUTH_USER", "").strip()
    password = os.environ.get("TV_AUTH_PASSWORD", "").strip()
    if user and password:
        return user, password
    return None


def load_protected_prefixes() -> list[str]:
    """Return normalized URL path prefixes that require HTTP Basic Auth."""
    if not PROTECTED_PATHS_FILE.is_file():
        return []
    data = json.loads(PROTECTED_PATHS_FILE.read_text(encoding="utf-8"))
    prefixes: list[str] = []
    for raw in data.get("paths", []):
        prefix = raw if raw.startswith("/") else f"/{raw}"
        prefixes.append(prefix.rstrip("/") or "/")
    return prefixes


PROTECTED_PREFIXES = load_protected_prefixes()
AUTH_CREDENTIALS = load_auth_credentials()


def path_requires_auth(request_path: str) -> bool:
    path = urllib.parse.unquote(request_path.split("?", 1)[0])
    for prefix in PROTECTED_PREFIXES:
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


def credentials_valid(auth_header: str | None, expected: tuple[str, str]) -> bool:
    if not auth_header:
        return False
    try:
        scheme, encoded = auth_header.split(" ", 1)
        if scheme.lower() != "basic":
            return False
        decoded = base64.b64decode(encoded, validate=True).decode("utf-8")
        user, password = decoded.split(":", 1)
    except (ValueError, UnicodeDecodeError):
        return False
    expected_user, expected_password = expected
    user_ok = secrets.compare_digest(user, expected_user)
    password_ok = secrets.compare_digest(password, expected_password)
    return user_ok and password_ok


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------

class RepoHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files from WEBROOT; enforce Basic Auth on protected prefixes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEBROOT), **kwargs)

    def _send_auth_challenge(self) -> None:
        self.send_response(401)
        self.send_header("WWW-Authenticate", f'Basic realm="{AUTH_REALM}"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Authentication required.\n")

    def _send_auth_not_configured(self) -> None:
        self.send_response(503)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        body = (
            "Protected project paths are enabled but TV_AUTH_USER and "
            "TV_AUTH_PASSWORD are not configured. Copy deploy/auth.env.example "
            "to deploy/auth.env and restart the server.\n"
        )
        self.wfile.write(body.encode("utf-8"))

    def _authorize_request(self) -> bool:
        if not path_requires_auth(self.path):
            return True
        if AUTH_CREDENTIALS is None:
            self._send_auth_not_configured()
            return False
        if credentials_valid(self.headers.get("Authorization"), AUTH_CREDENTIALS):
            return True
        self._send_auth_challenge()
        return False

    def do_GET(self):
        if not self._authorize_request():
            return
        super().do_GET()

    def do_HEAD(self):
        if not self._authorize_request():
            return
        super().do_HEAD()

    def log_message(self, fmt, *args):
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


def log_protection_status() -> None:
    if not PROTECTED_PREFIXES:
        return
    print("[auth ] Protected path prefixes:")
    for prefix in PROTECTED_PREFIXES:
        print(f"         {prefix}")
    if AUTH_CREDENTIALS is None:
        print("[auth ] WARNING: credentials not configured; protected paths return 503")
        print("[auth ]          copy deploy/auth.env.example to deploy/auth.env")
    else:
        print("[auth ] Credentials loaded for HTTP Basic Auth")


def main() -> None:
    args = parse_args()

    bind       = args.bind
    http_port  = args.http
    https_port = args.https

    log_protection_status()

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
