#!/usr/bin/env python3
"""
export_project_pdfs.py: for each project, render every page in that
project's subtree to its own PDF via headless Chrome, then merge just that
project's pages into one combined PDF (e.g. docs/pdf_exports/gold/gold_complete.pdf).

Each project gets its own combined PDF. This does not merge across projects.

Reads the project list from frontend/site-index.json (the same source of
truth used by the live homepage), so it always tracks whatever projects are
currently registered. Pages are discovered by walking each project's folder
under frontend/project/<slug>/, skipping anything under a data/ directory
(schema/CSV table viewers, not real site pages).

Pages under a prefix listed in deploy/protected-paths.json (currently AUBEB
and Senegal Agroforestry, which require HTTP Basic Auth) are skipped by
default rather than rendered, since headless Chrome can hang indefinitely
on some authenticated pages. Each page render is also subject to a hard
timeout so a single hung/slow page can never freeze the whole run; it is
skipped with a warning instead.

Usage:
    python3 scripts/export_project_pdfs.py --projects gold
    python3 scripts/export_project_pdfs.py --projects gold,west_african_shea
    python3 scripts/export_project_pdfs.py                      # every project in site-index.json
    python3 scripts/export_project_pdfs.py --base-url http://127.0.0.1:8000
    python3 scripts/export_project_pdfs.py --out docs/pdf_exports
    python3 scripts/export_project_pdfs.py --projects gold --long-page

If no server is reachable at --base-url, a temporary server is started via
scripts/serve.py on an unused port and shut down afterward.

--long-page mode:
    By default each HTML page is printed at standard Letter size, so a tall
    page (a dashboard, a long project_context page) spans many 8.5x11 PDF
    pages. Passing --long-page instead renders each HTML page as a single
    continuous PDF page sized exactly to that page's full content height (a
    "long scroll" page), so the combined PDF has one page per HTML page
    instead of many. This uses the Chrome DevTools Protocol directly (via
    the websocket-client package) to measure real rendered content height
    and print with a matching custom paper height; it does not use the
    plain --print-to-pdf CLI flag, which always paginates at Letter size.
"""

import argparse
import base64
import json
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_INDEX = REPO_ROOT / "frontend" / "site-index.json"
PROJECT_ROOT = REPO_ROOT / "frontend" / "project"
PROTECTED_PATHS_FILE = REPO_ROOT / "deploy" / "protected-paths.json"
AUTH_ENV_FILE = REPO_ROOT / "deploy" / "auth.env"
DEFAULT_OUT = REPO_ROOT / "docs" / "pdf_exports"

CHROME_CANDIDATES = [
    "google-chrome-stable",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

# Hard ceiling on a single Chrome render; a hung page is skipped, not fatal.
RENDER_TIMEOUT_SECONDS = 45

# Pages sort earlier within their directory when their filename appears here.
FILE_PRIORITY = [
    "index.html",
    "dashboard.html",
    "project_context.html",
    "system_lifecycle.html",
    "recycling_analysis.html",
    "what_if_simulator.html",
]


def find_chrome() -> str:
    for name in CHROME_CANDIDATES:
        if shutil.which(name):
            return name
    sys.exit("No Chrome/Chromium binary found (tried: %s)" % ", ".join(CHROME_CANDIDATES))


def load_projects(filter_ids):
    data = json.loads(SITE_INDEX.read_text())
    projects = data["projects"]
    if filter_ids:
        wanted = set(filter_ids)
        projects = [p for p in projects if p["id"] in wanted]
        missing = wanted - {p["id"] for p in projects}
        if missing:
            sys.exit(f"Unknown project id(s): {', '.join(sorted(missing))}")
    return projects


def discover_pages(project_dir: Path):
    """All HTML pages in a project's subtree, in a sensible reading order.

    Skips anything under a data/ directory (schema/CSV table viewers, not
    real navigable site pages).
    """
    def dir_key(rel_dir_parts):
        if not rel_dir_parts:
            return (0, ())
        if rel_dir_parts[0] == "supply_chain":
            return (1, rel_dir_parts)
        if rel_dir_parts[0] == "value_chain":
            return (2, rel_dir_parts)
        return (3, rel_dir_parts)

    def file_key(name):
        try:
            return FILE_PRIORITY.index(name)
        except ValueError:
            return len(FILE_PRIORITY)

    pages = []
    for html_path in project_dir.rglob("*.html"):
        rel = html_path.relative_to(project_dir)
        if "data" in rel.parts[:-1]:
            continue
        pages.append(rel)

    pages.sort(key=lambda rel: (dir_key(rel.parts[:-1]), file_key(rel.name), rel.name))
    return pages


def label_for(rel_path: Path) -> str:
    parts = list(rel_path.with_suffix("").parts)
    if parts == ["index"]:
        return "hub"
    if parts[-1] == "index":
        parts = parts[:-1]
    return "_".join(parts)


def load_protected_prefixes():
    if not PROTECTED_PATHS_FILE.exists():
        return []
    return json.loads(PROTECTED_PATHS_FILE.read_text()).get("paths", [])


def load_basic_auth_credentials():
    if not AUTH_ENV_FILE.exists():
        return None
    values = {}
    for line in AUTH_ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        values[key.strip()] = val.strip()
    user, password = values.get("TV_AUTH_USER"), values.get("TV_AUTH_PASSWORD")
    return (user, password) if user and password else None


def is_protected(url_path: str, prefixes) -> bool:
    return any(url_path.startswith(prefix) for prefix in prefixes)


def with_credentials(url: str, user: str, password: str) -> str:
    scheme, rest = url.split("://", 1)
    return f"{scheme}://{user}:{password}@{rest}"


def redact_credentials(url: str) -> str:
    scheme, sep, rest = url.partition("://")
    if "@" in rest:
        rest = rest.split("@", 1)[1]
    return f"{scheme}{sep}{rest}"


def server_is_up(base_url: str) -> bool:
    try:
        urllib.request.urlopen(base_url, timeout=2)
        return True
    except Exception:
        return False


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_temp_server():
    port = free_port()
    proc = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "scripts" / "serve.py"),
         "--http-only", "--bind", "127.0.0.1", "--http", str(port)],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"
    for _ in range(30):
        if server_is_up(base_url):
            return proc, base_url
        time.sleep(0.5)
    proc.terminate()
    sys.exit("Temporary dev server did not come up in time")


def render_pdf(chrome: str, url: str, out_path: Path):
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={out_path}",
        "--print-to-pdf-no-header",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=15000",
        url,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=RENDER_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"Chrome timed out after {RENDER_TIMEOUT_SECONDS}s rendering "
            f"{redact_credentials(url)}")
    if result.returncode != 0 or not out_path.exists():
        raise RuntimeError(
            f"Chrome failed to render {redact_credentials(url)}\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )


def _cdp_wait_for_debug_port(port: int, timeout: float = 10.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError("Chrome remote debugging port did not come up in time")


def _cdp_get_page_ws_url(port: int) -> str:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=5) as resp:
        targets = json.loads(resp.read())
    for target in targets:
        if target.get("type") == "page" and "webSocketDebuggerUrl" in target:
            return target["webSocketDebuggerUrl"]
    raise RuntimeError("No page target found on Chrome remote debugging port")


class _CDPSession:
    """Minimal Chrome DevTools Protocol client over a single websocket.

    Only supports the request/response and event-waiting patterns needed by
    render_pdf_long_page: enable a domain, navigate, wait for the load event,
    evaluate JS, and print to PDF.
    """

    def __init__(self, ws_url: str):
        import websocket  # local import: only required for --long-page
        self._ws = websocket.create_connection(ws_url, timeout=30)
        self._next_id = 1
        self._responses = {}
        self._events = []

    def _pump(self, timeout: float):
        self._ws.settimeout(max(timeout, 0.1))
        raw = self._ws.recv()
        msg = json.loads(raw)
        if "id" in msg:
            self._responses[msg["id"]] = msg
        else:
            self._events.append(msg)

    def call(self, method: str, params=None, timeout: float = 30.0):
        msg_id = self._next_id
        self._next_id += 1
        self._ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while msg_id not in self._responses:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise RuntimeError(f"Timed out waiting for CDP response to {method}")
            self._pump(remaining)
        msg = self._responses.pop(msg_id)
        if "error" in msg:
            raise RuntimeError(f"CDP error for {method}: {msg['error']}")
        return msg.get("result", {})

    def wait_for_event(self, method: str, timeout: float = 30.0):
        deadline = time.time() + timeout
        while True:
            for i, ev in enumerate(self._events):
                if ev.get("method") == method:
                    return self._events.pop(i).get("params", {})
            remaining = deadline - time.time()
            if remaining <= 0:
                raise RuntimeError(f"Timed out waiting for CDP event {method}")
            self._pump(remaining)

    def close(self):
        try:
            self._ws.close()
        except Exception:
            pass


def render_pdf_long_page(chrome: str, url: str, out_path: Path,
                          viewport_width_px: int = 816, dpi: int = 96,
                          margin_in: float = 0.25, timeout: float = RENDER_TIMEOUT_SECONDS):
    """Render one HTML page as a single PDF page sized to its full content height.

    Launches its own headless Chrome instance with a remote debugging port
    (separate from any --print-to-pdf invocation), measures
    document.documentElement.scrollHeight at a fixed viewport width via CDP,
    then calls Page.printToPDF with a custom paperHeight matching that
    content, so the page never breaks across multiple Letter-size sheets.
    """
    try:
        import websocket  # noqa: F401  (import check; real use is inside _CDPSession)
    except ImportError as exc:
        raise RuntimeError(
            "--long-page requires the 'websocket-client' package: "
            "pip install websocket-client"
        ) from exc

    port = free_port()
    proc = subprocess.Popen(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         f"--remote-debugging-port={port}", "--remote-allow-origins=*", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    session = None
    try:
        _cdp_wait_for_debug_port(port, timeout=10)
        ws_url = _cdp_get_page_ws_url(port)
        session = _CDPSession(ws_url)
        session.call("Page.enable", timeout=timeout)
        session.call("Emulation.setDeviceMetricsOverride", {
            "width": viewport_width_px, "height": 1024,
            "deviceScaleFactor": 1, "mobile": False,
        }, timeout=timeout)
        session.call("Page.navigate", {"url": url}, timeout=timeout)
        session.wait_for_event("Page.loadEventFired", timeout=timeout)
        time.sleep(1.0)  # let inline scripts (SVG pentagons, DOM injection) settle
        eval_result = session.call("Runtime.evaluate", {
            "expression": "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)",
            "returnByValue": True,
        }, timeout=timeout)
        scroll_height_px = eval_result.get("result", {}).get("value")
        if not scroll_height_px:
            raise RuntimeError("Could not measure page content height via CDP")
        width_in = viewport_width_px / dpi + margin_in * 2
        height_in = scroll_height_px / dpi + margin_in * 2 + 0.1
        pdf_result = session.call("Page.printToPDF", {
            "landscape": False,
            "printBackground": True,
            "paperWidth": width_in,
            "paperHeight": max(height_in, 1.0),
            "marginTop": margin_in,
            "marginBottom": margin_in,
            "marginLeft": margin_in,
            "marginRight": margin_in,
            "preferCSSPageSize": False,
            "scale": 1,
        }, timeout=timeout)
        data = base64.b64decode(pdf_result["data"])
        out_path.write_bytes(data)
    except Exception as exc:
        raise RuntimeError(f"Long-page render failed for {redact_credentials(url)}: {exc}") from exc
    finally:
        if session is not None:
            session.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"Long-page render produced no output for {redact_credentials(url)}")


def merge_pdfs(pdf_paths, combined_path: Path):
    from pypdf import PdfWriter

    writer = PdfWriter()
    for p in pdf_paths:
        writer.append(str(p))
    combined_path.parent.mkdir(parents=True, exist_ok=True)
    with open(combined_path, "wb") as f:
        writer.write(f)


def export_project(chrome, base_url, out_root, proj, protected_prefixes, credentials,
                    include_protected, long_page=False):
    project_dir = PROJECT_ROOT / proj["id"]
    if not project_dir.is_dir():
        print(f"  WARNING: {proj['id']}: no folder at {project_dir}, skipping")
        return None

    pages = discover_pages(project_dir)
    if not pages:
        print(f"  WARNING: {proj['id']}: no HTML pages found, skipping")
        return None

    out_dir = out_root / proj["id"]
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_paths = []
    for i, rel in enumerate(pages, start=1):
        url_path = f"/frontend/project/{proj['id']}/{rel.as_posix()}"

        if is_protected(url_path, protected_prefixes):
            if not include_protected:
                print(f"  [{i}/{len(pages)}] {rel.as_posix()} -> SKIPPED "
                      f"(behind HTTP Basic Auth; pass --include-protected to render it)")
                continue
            if not credentials:
                print(f"  [{i}/{len(pages)}] {rel.as_posix()} -> SKIPPED "
                      f"(behind HTTP Basic Auth; deploy/auth.env has no credentials)")
                continue
            page_url = with_credentials(base_url + url_path, *credentials)
        else:
            page_url = base_url + url_path

        out_path = out_dir / f"{i:02d}_{label_for(rel)}.pdf"
        print(f"  [{i}/{len(pages)}] {rel.as_posix()} -> {out_path.name}")
        try:
            if long_page:
                render_pdf_long_page(chrome, page_url, out_path)
            else:
                render_pdf(chrome, page_url, out_path)
        except RuntimeError as exc:
            print(f"    WARNING: skipping this page: {exc}")
            continue
        pdf_paths.append(out_path)

    if not pdf_paths:
        print(f"  WARNING: {proj['id']}: no pages rendered, no combined PDF produced")
        return None

    combined_path = out_dir / f"{proj['id']}_complete.pdf"
    merge_pdfs(pdf_paths, combined_path)
    return combined_path


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000",
                         help="Base URL of a running site server (default: %(default)s)")
    parser.add_argument("--out", default=str(DEFAULT_OUT),
                         help="Output root directory; each project gets its own subfolder")
    parser.add_argument("--projects", default="",
                         help="Comma-separated project ids to export (default: all in site-index.json)")
    parser.add_argument("--include-protected", action="store_true",
                         help="Attempt to render pages behind HTTP Basic Auth (AUBEB, Senegal "
                              "Agroforestry) using deploy/auth.env credentials. Off by default: "
                              "some authenticated pages are known to hang headless Chrome.")
    parser.add_argument("--long-page", action="store_true",
                         help="Render each HTML page as a single continuous PDF page sized to "
                              "its full content height, instead of many Letter-size pages. "
                              "Requires the websocket-client package.")
    args = parser.parse_args()

    chrome = find_chrome()
    out_root = Path(args.out)

    filter_ids = [p.strip() for p in args.projects.split(",") if p.strip()]
    projects = load_projects(filter_ids)
    if not projects:
        sys.exit("No projects to export")

    temp_proc = None
    base_url = args.base_url.rstrip("/")
    if not server_is_up(base_url + "/frontend/site-index.json"):
        print(f"No server reachable at {base_url}, starting a temporary one...")
        temp_proc, base_url = start_temp_server()
        print(f"Temporary server up at {base_url}")

    protected_prefixes = load_protected_prefixes()
    credentials = load_basic_auth_credentials() if args.include_protected else None

    try:
        results = []
        for proj in projects:
            print(f"=== {proj['id']} ===")
            combined_path = export_project(
                chrome, base_url, out_root, proj, protected_prefixes, credentials,
                args.include_protected, long_page=args.long_page)
            if combined_path:
                results.append((proj["id"], combined_path))

        print("\nDone. Combined PDFs:")
        for project_id, combined_path in results:
            print(f"  {project_id}: {combined_path}")
    finally:
        if temp_proc is not None:
            temp_proc.terminate()
            temp_proc.wait(timeout=5)


if __name__ == "__main__":
    main()
