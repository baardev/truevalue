#!/usr/bin/env python3

import os
import time
import base64
import mimetypes
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from bs4 import BeautifulSoup

COGNEE_URL = "https://tenant-1f6e75c1-89fc-4caa-bf2a-b5a4e596ac92.aws.cognee.ai"
ENDPOINT = f"{COGNEE_URL}/api/v1/remember"

SOURCE_DIR = Path("/home/jw/src/tv")
DATASET = "tv-local-data"
CHECKPOINT_FILE = Path("/home/jw/src/tv/.cognee_checkpoint.json")

SLEEP_SECONDS = 0.1
MAX_WORKERS = 4
MAX_RETRIES = 3
MAX_FILE_BYTES = 5 * 1024 * 1024  # skip files larger than 5 MB

_checkpoint_lock = threading.Lock()

TEXT_EXTENSIONS = {
    ".txt", ".md", ".csv", ".json", ".yaml", ".yml",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".htm",
    ".css", ".sql", ".xml",
}

IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg",
}

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".cache", "dist", "build", ".next",
}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def load_checkpoint() -> set:
    if CHECKPOINT_FILE.exists():
        try:
            return set(json.loads(CHECKPOINT_FILE.read_text()))
        except Exception:
            return set()
    return set()


def save_checkpoint(done: set) -> None:
    with _checkpoint_lock:
        CHECKPOINT_FILE.write_text(json.dumps(sorted(done), indent=2))


def clean_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")

    for tag in soup(["style", "script", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else path.name
    body = soup.get_text(separator="\n")

    lines = [line.strip() for line in body.splitlines()]
    lines = [line for line in lines if line]

    return f"# {title}\n\nSource file: {path}\n\n" + "\n".join(lines)


def read_text_file(path: Path) -> str:
    if path.suffix.lower() in {".html", ".htm"}:
        return clean_html(path)

    text = path.read_text(encoding="utf-8", errors="ignore")
    return f"# {path.name}\n\nSource file: {path}\n\n{text}"


def image_to_base64_document(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "application/octet-stream"

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")

    return f"""# Image file: {path.name}

Source file: {path}
MIME type: {mime_type}
Encoding: base64

data:{mime_type};base64,{encoded}
"""


def iter_uploadable_files():
    for path in SOURCE_DIR.rglob("*"):
        if not path.is_file():
            continue

        if should_skip(path):
            continue

        suffix = path.suffix.lower()

        if suffix in TEXT_EXTENSIONS or suffix in IMAGE_EXTENSIONS:
            yield path


def make_upload_document(path: Path) -> tuple[str, bytes]:
    suffix = path.suffix.lower()
    relative = path.relative_to(SOURCE_DIR)

    if suffix in IMAGE_EXTENSIONS:
        content = image_to_base64_document(path)
        upload_name = str(relative) + ".base64.txt"
    else:
        content = read_text_file(path)
        upload_name = str(relative)

        if suffix in {".html", ".htm"}:
            upload_name = str(relative) + ".clean.txt"

    return upload_name, content.encode("utf-8")


def upload_document(path: Path, api_key: str) -> bool:
    if path.stat().st_size > MAX_FILE_BYTES:
        print(f"SKIP {path}  (>{MAX_FILE_BYTES // (1024*1024)} MB)")
        return False

    upload_name, content = make_upload_document(path)

    headers = {"X-Api-Key": api_key}
    data = {"datasetName": DATASET}
    files = {"data": (upload_name, content, "text/plain")}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                ENDPOINT,
                headers=headers,
                data=data,
                files=files,
                timeout=180,
            )
        except requests.exceptions.Timeout:
            wait = 2 ** attempt
            print(f"TIMEOUT {path}  (attempt {attempt}/{MAX_RETRIES}, retry in {wait}s)")
            if attempt < MAX_RETRIES:
                time.sleep(wait)
            continue
        except Exception as e:
            print(f"FAIL {path}: {e}")
            return False

        if response.ok:
            print(f"OK   {path}")
            return True

        print(f"ERR  {path}")
        print(f"     HTTP {response.status_code}: {response.text[:500]}")
        return False

    print(f"FAIL {path}  (all {MAX_RETRIES} attempts timed out)")
    return False


def main():
    api_key = os.environ.get("COGNEE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Missing COGNEE_API_KEY. Run:\n"
            "export COGNEE_API_KEY='your-api-key-here'"
        )

    all_files = list(iter_uploadable_files())
    done = load_checkpoint()

    pending = [p for p in all_files if str(p) not in done]

    print(f"Source:  {SOURCE_DIR}")
    print(f"Dataset: {DATASET}")
    print(f"Files:   {len(all_files)} total, {len(done)} already uploaded, {len(pending)} pending")
    print()

    ok = 0
    fail = 0

    def process(path: Path) -> tuple[Path, bool]:
        result = upload_document(path, api_key)
        time.sleep(SLEEP_SECONDS)
        return path, result

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(process, p): p for p in pending}
        for future in as_completed(futures):
            path, success = future.result()
            if success:
                ok += 1
                with _checkpoint_lock:
                    done.add(str(path))
                save_checkpoint(done)
            else:
                fail += 1

    print()
    print(f"Done. Successful: {ok}, Failed: {fail}")
    if fail:
        print(f"Re-run to retry failed files. Checkpoint saved to {CHECKPOINT_FILE}")


if __name__ == "__main__":
    main()