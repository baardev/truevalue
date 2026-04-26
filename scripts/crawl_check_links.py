#!/usr/bin/env python3
"""BFS a static site, extract href/src from HTML, check same-origin targets (GET)."""
from __future__ import annotations

import argparse
import sys
from collections import deque
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

DEFAULT_UA = "tv-crawl/1.0 (link audit)"


class Ex(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = {k: v for k, v in attrs if v is not None}
        if tag == "a" and "href" in d:
            self.urls.append(d["href"])
        if tag in ("img", "script", "iframe", "source", "use") and "src" in d:
            self.urls.append(d["src"])
        if tag == "link" and d.get("href"):
            self.urls.append(d["href"])


def same_origin(a: str, u: str) -> bool:
    return urlparse(a).netloc == urlparse(u).netloc


def absolutize(base: str, rel: str) -> str | None:
    u = urljoin(base, rel)
    p = urlparse(u)
    if p.scheme not in ("http", "https"):
        return None
    return urlunparse((p.scheme, p.netloc, p.path or "/", p.params, p.query, ""))


def is_skipped_fragment(rel: str) -> bool:
    if not rel or rel.startswith(
        ("#", "javascript:", "mailto:", "tel:", "data:", "about:")
    ):
        return True
    return False


def check(url: str, timeout: int) -> tuple[int | None, str | None, str | None]:
    for method in ("HEAD", "GET"):
        try:
            r = Request(url, method=method, headers={"User-Agent": DEFAULT_UA})
            with urlopen(r, timeout=timeout) as resp:  # noqa: S310
                c = int(resp.getcode() or 200)
                if c < 400:
                    return c, method, None
        except HTTPError as e:
            if e.code == 405 and method == "HEAD":
                continue
            if method == "HEAD" and e.code in (400, 404, 500):
                continue
            last = f"HTTP {e.code}"
        except URLError as e:
            last = str(e.reason) if e.reason else str(e)
        except OSError as e:
            last = str(e)
    # final GET
    try:
        r = Request(url, method="GET", headers={"User-Agent": DEFAULT_UA})
        with urlopen(r, timeout=timeout) as resp:  # noqa: S310
            c = int(resp.getcode() or 200)
            if c < 400:
                return c, "GET", None
    except HTTPError as e:
        return None, None, f"HTTP {e.code} {e.reason}"
    except (URLError, OSError) as e:
        return None, None, str(e)
    return None, None, "unknown error"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("start", help="Start URL, e.g. http://dev.tholonia.com:8000/index.html")
    ap.add_argument("--max-pages", type=int, default=400)
    ap.add_argument("--timeout", type=int, default=25)
    a = ap.parse_args()

    start = a.start
    base_host = urlparse(start).netloc
    if not base_host:
        print("Invalid start URL", file=sys.stderr)
        return 2

    q: deque[tuple[str, str | None]] = deque([(start, None)])
    seen_key: set[str] = set()
    pages_ok: list[str] = []
    broken_hrefs: list[tuple[str, str, str, str]] = []  # from_page, raw, abs, err
    checked: set[str] = set()  # absolute URL, query included

    def page_key(p: str) -> str:
        u = urlparse(p)
        return f"{u.path}?{u.query}" if u.query else (u.path or "/")

    while q and len(pages_ok) < a.max_pages:
        u, ref = q.popleft()
        if page_key(u) in seen_key:
            continue
        c, m, err = check(u, a.timeout)
        if c is None or c >= 400:
            # e.g. /data/index.html 404s while /data/ returns 200 (no index file)
            parent_ok = False
            if (u.rstrip("/") or "/").endswith("index.html"):
                parent = u.rsplit("/", 1)[0] + "/"
                c3, _, _ = check(parent, a.timeout)
                if c3 is not None and c3 < 400:
                    parent_ok = True
            if not parent_ok:
                rfs = ref or "?"
                err_s = str(err) if err else f"status {c}"
                broken_hrefs.append((rfs, f"(crawl) -> {u}", u, err_s))
                print(
                    f"PAGE 404/ERR: {u} (linked from {rfs}) -> {err}",
                    file=sys.stderr,
                )
            else:
                print(
                    f"INFO skip (parent OK): {u} 404 but {parent!r} returns 200",
                    file=sys.stderr,
                )
            seen_key.add(page_key(u))
            continue
        seen_key.add(page_key(u))
        pages_ok.append(u)
        try:
            r = Request(u, headers={"User-Agent": DEFAULT_UA})
            with urlopen(r, timeout=a.timeout) as resp:  # noqa: S310
                text = resp.read().decode("utf-8", "replace")
        except (HTTPError, URLError, OSError) as e:
            print(f"READ FAIL {u}: {e}", file=sys.stderr)
            continue
        ex = Ex()
        try:
            ex.feed(text)
        except Exception as e:  # noqa: BLE001
            print(f"PARSE {u}: {e}", file=sys.stderr)

        for rel in ex.urls:
            if is_skipped_fragment(rel):
                continue
            absu = absolutize(u, rel)
            if not absu:
                continue
            p = urlparse(absu)
            if p.netloc != base_host:
                continue
            if absu not in checked:
                checked.add(absu)
                c2, _, err2 = check(absu, a.timeout)
                if c2 is None or c2 >= 400:
                    broken_hrefs.append(
                        (u, rel, absu, err2 or f"status {c2}")
                    )
            pl = p.path.lower()
            if pl.endswith((".html", ".htm")):
                nxt = absu
            elif p.path.endswith("/") or p.path == "" or p.path == "/":
                nxt = urljoin(absu.rstrip("/") + "/", "index.html")
            else:
                continue
            if page_key(nxt) not in seen_key:
                q.append((nxt, u))

    print(f"Crawled {len(pages_ok)} HTML pages (max {a.max_pages}).")
    print(f"Checked {len(checked)} unique same-origin href/src targets.")
    print(f"Broken: {len(broken_hrefs)}")
    for fp, raw, ab, er in broken_hrefs:
        print("---")
        print("from:", fp)
        print(" raw:", raw)
        print(" abs:", ab)
        print(" err:", er)
    return 0 if not broken_hrefs else 1


if __name__ == "__main__":
    raise SystemExit(main())
