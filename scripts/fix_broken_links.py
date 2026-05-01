#!/usr/bin/env python3
"""Remove broken same-origin links across the static site.

Scans all HTML under the repo root index and frontend/ (excluding .git and viewable/).
Prunes broken URLs from frontend/site-index.json.

Run with --check-only to audit without writing files (exit 1 if anything is broken).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

SERVER_ROOT = Path(__file__).resolve().parents[1]

# Generated mirror; rebuild with scripts/rebuild-site.sh instead of editing here.
SKIP_DIR_NAMES = frozenset({".git", "viewable", "__pycache__", ".venv", "venv", "node_modules"})


def is_external(url: str) -> bool:
    if not url or url.startswith("#"):
        return True
    if url.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return True
    p = urlparse(url.strip())
    if p.scheme in ("http", "https"):
        return True
    return False


def strip_qf(url: str) -> str:
    return url.split("#")[0].split("?")[0] if url else url


def resolve_local(base_file: Path, url: str) -> Path | None:
    url = strip_qf(url.strip())
    if not url or is_external(url):
        return None
    if url.startswith("/"):
        return (SERVER_ROOT / url.lstrip("/")).resolve()
    return (base_file.parent / url).resolve()


def under_root(path: Path) -> bool:
    try:
        path.resolve().relative_to(SERVER_ROOT)
        return True
    except ValueError:
        return False


def target_ok(path: Path) -> bool:
    if not under_root(path):
        return False
    if path.is_file():
        return True
    if path.is_dir():
        return (path / "index.html").exists() or (path / "index.htm").exists()
    return False


def local_ref_ok(base_file: Path, url: str) -> bool:
    if is_external(url):
        return True
    p = resolve_local(base_file, url)
    if p is None:
        return True
    return target_ok(p)


def site_url_ok(url: str) -> bool:
    if not url or url.startswith(("http://", "https://")):
        return True
    rel = url.lstrip("/")
    p = (SERVER_ROOT / rel).resolve()
    return target_ok(p)


def clean_site_index() -> None:
    path = SERVER_ROOT / "frontend/site-index.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    data["projects"] = [
        p for p in data.get("projects", []) if site_url_ok(p.get("hub", ""))
    ]

    for key in ("research", "reports", "tvpci"):
        block = data.get(key)
        if not isinstance(block, dict):
            continue
        hub = block.get("hub")
        if hub and not site_url_ok(hub):
            block.pop("hub", None)
        new_sections: list = []
        for sec in block.get("sections", []):
            new_items: list = []
            for item in sec.get("items", []):
                links = item.get("links") or []
                if links:
                    kept = [L for L in links if site_url_ok(L.get("url", ""))]
                    if not kept:
                        continue
                    item = dict(item)
                    seen_u = set()
                    deduped = []
                    for L in kept:
                        u = L.get("url", "")
                        if u in seen_u:
                            continue
                        seen_u.add(u)
                        deduped.append(L)
                    item["links"] = deduped
                new_items.append(dict(item))
            if new_items:
                ns = dict(sec)
                ns["items"] = new_items
                new_sections.append(ns)
        block["sections"] = new_sections

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _path_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def list_all_site_html_files() -> list[Path]:
    """Every servable HTML file under SERVER_ROOT (root index + frontend/)."""
    out: list[Path] = []
    ix = SERVER_ROOT / "index.html"
    if ix.is_file():
        out.append(ix.resolve())
    front = SERVER_ROOT / "frontend"
    if front.is_dir():
        for p in front.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in (".html", ".htm"):
                continue
            if _path_skipped(p):
                continue
            out.append(p.resolve())
    return sorted(set(out))


def collect_broken_attrs(path: Path) -> list[tuple[str, str]]:
    """Return [(url, tag_hint), ...] for broken same-origin references in HTML attrs."""
    bad: list[tuple[str, str]] = []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return bad
    soup = BeautifulSoup(raw, "html.parser")

    def chk(url: str, hint: str) -> None:
        if not url or is_external(url):
            return
        if not local_ref_ok(path, url):
            bad.append((strip_qf(url), hint))

    for tag in soup.find_all("a", href=True):
        chk(tag["href"], "a.href")
    for tag in soup.find_all("link", href=True):
        chk(tag["href"], "link.href")
    for tag in soup.find_all("script", src=True):
        chk(tag["src"], "script.src")
    for tag in soup.find_all("iframe", src=True):
        chk(tag["src"], "iframe.src")
    for tag in soup.find_all("embed", src=True):
        chk(tag["src"], "embed.src")
    for tag in soup.find_all("img"):
        if tag.has_attr("src"):
            chk(tag["src"], "img.src")
        if tag.has_attr("srcset"):
            for chunk in tag["srcset"].split(","):
                bits = chunk.strip().split()
                if bits:
                    chk(bits[0], "img.srcset")
    for tag in soup.find_all("form", action=True):
        act = tag["action"]
        if act and not act.strip().startswith("#"):
            chk(act, "form.action")
    for tag in soup.find_all("video", poster=True):
        chk(tag["poster"], "video.poster")
    for tag in soup.find_all(["source", "audio"], src=True):
        chk(tag["src"], tag.name + ".src")
    for tag in soup.find_all("object", data=True):
        chk(tag["data"], "object.data")
    for tag in soup.find_all("meta", attrs={"http-equiv": re.compile("^refresh$", re.I)}):
        content = tag.get("content") or ""
        m = re.search(r"url\s*=\s*([^;]+)", content, re.I)
        if m:
            chk(m.group(1).strip().strip("'\""), "meta.refresh")

    return bad


# Quoted absolute paths inside HTML (inline scripts, JSON blobs)
_INLINE_ABS_URL = re.compile(r"""['\"](/(?:frontend|data|site|schema)/[^'\"#?]*)""")


def collect_broken_inline_urls(path: Path) -> list[tuple[str, str]]:
    """Heuristic: quoted /frontend, /data, /site, /schema paths in raw HTML."""
    bad: list[tuple[str, str]] = []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return bad
    seen: set[str] = set()
    for m in _INLINE_ABS_URL.finditer(raw):
        url = m.group(1)
        if url in seen:
            continue
        seen.add(url)
        if is_external(url):
            continue
        if not local_ref_ok(path, url):
            bad.append((url, "quoted path in file"))
    return bad


def audit_site_index_json() -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    p = SERVER_ROOT / "frontend/site-index.json"
    if not p.exists():
        return [("<missing>", "frontend/site-index.json")]

    def walk(o: object, prefix: str) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "url" and isinstance(v, str) and v.startswith("/"):
                    if not site_url_ok(v):
                        issues.append((v, prefix))
                elif k == "hub" and isinstance(v, str) and v.startswith("/"):
                    if not site_url_ok(v):
                        issues.append((v, prefix + ".hub"))
                walk(v, prefix + "/" + str(k))
        elif isinstance(o, list):
            for i, item in enumerate(o):
                walk(item, f"{prefix}[{i}]")

    walk(json.loads(p.read_text(encoding="utf-8")), "$")
    return issues


def audit_frontend_js() -> list[tuple[str, str, str]]:
    """Report broken quoted root-relative URLs in frontend/**/*.js."""
    bad: list[tuple[str, str, str]] = []
    js_dir = SERVER_ROOT / "frontend"
    if not js_dir.is_dir():
        return bad
    for js_path in js_dir.rglob("*.js"):
        if _path_skipped(js_path):
            continue
        try:
            text = js_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(js_path.relative_to(SERVER_ROOT))
        for m in _INLINE_ABS_URL.finditer(text):
            url = m.group(1)
            if not site_url_ok(url):
                bad.append((rel, url, "js quoted path"))
    return bad


def run_full_audit() -> list[tuple[str, str, str]]:
    """Return list of (location, url, reason)."""
    rows: list[tuple[str, str, str]] = []
    for hf in list_all_site_html_files():
        rel = str(hf.relative_to(SERVER_ROOT))
        for url, hint in collect_broken_attrs(hf):
            rows.append((rel, url, hint))
        for url, hint in collect_broken_inline_urls(hf):
            rows.append((rel, url, hint))
    for url, ctx in audit_site_index_json():
        rows.append(("frontend/site-index.json", url, ctx))
    rows.extend(audit_frontend_js())
    return rows


def fix_broken_inline_lines(path: Path) -> bool:
    """Remove single-line JS snippets that reference missing root-relative paths."""
    orig = path.read_text(encoding="utf-8", errors="replace")
    raw = orig
    while True:
        bad_urls = {
            m.group(1)
            for m in _INLINE_ABS_URL.finditer(raw)
            if not is_external(m.group(1)) and not local_ref_ok(path, m.group(1))
        }
        if not bad_urls:
            break
        new_raw = raw
        for url in bad_urls:
            esc = re.escape(url)
            new_raw = re.sub(
                rf"^[ \t]*\{{[^\n]*href:\s*['\"]{esc}['\"][^\n]*\}},?\s*\n?",
                "",
                new_raw,
                flags=re.MULTILINE,
            )
            new_raw = re.sub(
                rf"^[ \t]*[^\n]*fetch\s*\(\s*['\"]{esc}['\"]\s*\)[^\n]*\n?",
                "",
                new_raw,
                flags=re.MULTILINE,
            )
            new_raw = re.sub(
                rf"^[ \t]*var\s+\w+\s*=\s*['\"]{esc}['\"]\s*;?\s*\n?",
                "",
                new_raw,
                flags=re.MULTILINE,
            )
            new_raw = re.sub(
                rf"^[ \t]*const\s+\w+\s*=\s*['\"]{esc}['\"]\s*;?\s*\n?",
                "",
                new_raw,
                flags=re.MULTILINE,
            )
        if new_raw == raw:
            break
        raw = new_raw
    if raw != orig:
        path.write_text(raw, encoding="utf-8")
        return True
    return False


def parse_srcset(srcset: str, base_file: Path) -> tuple[str | None, bool]:
    parts_out: list[str] = []
    changed = False
    for chunk in srcset.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        bits = chunk.split()
        url = bits[0]
        rest = bits[1:]
        if local_ref_ok(base_file, url):
            parts_out.append(" ".join([url] + rest))
        else:
            changed = True
    if not parts_out:
        return None, True
    return ", ".join(parts_out), changed


def fix_html_file(path: Path) -> int:
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    n = 0

    for tag in soup.find_all("a", href=True):
        if not local_ref_ok(path, tag["href"]):
            tag.unwrap()
            n += 1

    for tag in soup.find_all("link", href=True):
        if not local_ref_ok(path, tag["href"]):
            tag.decompose()
            n += 1

    for tag in soup.find_all("script", src=True):
        if not local_ref_ok(path, tag["src"]):
            tag.decompose()
            n += 1

    for tag in soup.find_all("iframe", src=True):
        if not local_ref_ok(path, tag["src"]):
            tag.decompose()
            n += 1

    for tag in soup.find_all("embed", src=True):
        if not local_ref_ok(path, tag["src"]):
            tag.decompose()
            n += 1

    for tag in soup.find_all("img"):
        if tag.has_attr("src") and not local_ref_ok(path, tag["src"]):
            tag.decompose()
            n += 1
            continue
        if tag.has_attr("srcset"):
            new_ss, _ = parse_srcset(tag["srcset"], path)
            if new_ss is None:
                tag.decompose()
                n += 1
            elif new_ss != tag["srcset"]:
                tag["srcset"] = new_ss
                n += 1

    for tag in soup.find_all("form", action=True):
        act = tag["action"]
        if act and not act.strip().startswith("#") and not local_ref_ok(path, act):
            del tag["action"]
            n += 1

    for tag in soup.find_all("video", poster=True):
        if not local_ref_ok(path, tag["poster"]):
            del tag["poster"]
            n += 1

    for tag in soup.find_all(["source", "audio"], src=True):
        if not local_ref_ok(path, tag["src"]):
            tag.decompose()
            n += 1

    for tag in soup.find_all("object", data=True):
        if not local_ref_ok(path, tag["data"]):
            tag.decompose()
            n += 1

    for tag in soup.find_all("meta", attrs={"http-equiv": re.compile("^refresh$", re.I)}):
        content = tag.get("content") or ""
        m = re.search(r"url\s*=\s*([^;]+)", content, re.I)
        if m:
            url = m.group(1).strip().strip("'\"")
            if not local_ref_ok(path, url):
                tag.decompose()
                n += 1

    out = str(soup)
    if out != raw:
        path.write_text(out, encoding="utf-8")
    return n


FOOTER_JS_LINES = (
    "    { label: 'Documentation Wiki',       href: '/site/index.html',                          icon: '📖' },\n",
    "      { label: cap + ' Scenario Baseline', href: '/frontend/project/' + project + '/data/processed/' + project + '_scenario_baseline.csv', icon: '🎲' },\n",
    "      { label: 'Custody & Flow Schema',   href: '/data/custody_and_flow.html',        icon: '🏷️' },\n",
    "    { label: 'Research & Publications',  href: '/frontend/research/index.html',             icon: '🔬', color: 'red' },\n",
    "    { label: 'Reports & Briefings',      href: '/frontend/report/index.html',               icon: '📄' },\n",
    "    { label: 'TVPCI',                    href: '/frontend/tvpci/index.html',                icon: '🧭' },\n",
)

_HUB_NAV_RE = re.compile(
    r"^\s*\{ label: 'Research & Publications',\s+href: '/frontend/research/index\.html',\s+"
    r"icon: '🔬', color: 'red' \},\s*\n"
    r"\s*\{ label: 'Reports & Briefings',\s+href: '/frontend/report/index\.html',\s+"
    r"icon: '📄' \},\s*\n"
    r"\s*\{ label: 'TVPCI',\s+href: '/frontend/tvpci/index\.html',\s+icon: '🧭' \},\s*\n",
    re.MULTILINE,
)


def strip_embedded_footer_js() -> None:
    """Remove broken wiki / scenario CSV / custody / hub index entries from copied footer scripts."""
    paths: list[Path] = []
    root_ix = SERVER_ROOT / "index.html"
    if root_ix.is_file():
        paths.append(root_ix)
    front = SERVER_ROOT / "frontend"
    if front.is_dir():
        paths.extend(p for p in front.rglob("*.html") if not _path_skipped(p))
    for path in paths:
        try:
            t = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        orig = t
        for chunk in FOOTER_JS_LINES:
            t = t.replace(chunk, "")
        t = _HUB_NAV_RE.sub("", t)
        if t != orig:
            path.write_text(t, encoding="utf-8")


def patch_root_index_inline_js() -> None:
    p = SERVER_ROOT / "index.html"
    t = p.read_text(encoding="utf-8")

    t = re.sub(
        r'\n\s*<a href="/site/index\.html">[^<]*</a>\s*',
        "\n",
        t,
        count=1,
    )

    t = t.replace(
        "      { label: cap + ' Scenario Baseline', href: '/frontend/project/' + project + '/data/processed/' + project + '_scenario_baseline.csv', icon: '🎲' },\n",
        "",
        1,
    )

    t = t.replace(
        "      { label: 'Custody & Flow Schema',   href: '/data/custody_and_flow.html',        icon: '🏷️' },\n",
        "",
        1,
    )

    t = t.replace(
        "    { label: 'Documentation Wiki',       href: '/site/index.html',                          icon: '📖' },\n",
        "",
        1,
    )

    p.write_text(t, encoding="utf-8")


def main() -> int:
    check_only = "--check-only" in sys.argv
    if not check_only:
        clean_site_index()
        patch_root_index_inline_js()
        strip_embedded_footer_js()
        html_files = list_all_site_html_files()
        tag_edits = 0
        inline_files = 0
        for hf in html_files:
            tag_edits += fix_html_file(hf)
            if fix_broken_inline_lines(hf):
                inline_files += 1
        print(
            f"Cleaned site-index.json; scanned {len(html_files)} HTML files "
            f"({tag_edits} HTML tag edits; {inline_files} files with inline JS/path cleanup)."
        )

    bad = run_full_audit()
    if bad:
        print(f"\nBroken links remaining ({len(bad)}):\n")
        for loc, url, hint in bad[:200]:
            print(f"  {loc}\n    {url}\n    ({hint})\n")
        if len(bad) > 200:
            print(f"  ... and {len(bad) - 200} more.")
        return 1
    print("Audit OK: no broken same-origin links found (HTML attrs, quoted paths, site-index.json, frontend JS).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
