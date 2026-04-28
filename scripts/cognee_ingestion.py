#!/usr/bin/env python3

import os
import time
import requests
from pathlib import Path

# CONFIG
COGNEE_URL = "https://tenant-1f6e75c1-89fc-4caa-bf2a-b5a4e596ac92.aws.cognee.ai"
API_KEY = os.environ.get("COGNEE_API_KEY")
DATASET = "tv-local-data"
SOURCE_DIR = Path.home() / "src" / "tv"

ENDPOINT = f"{COGNEE_URL}/api/v1/remember"

# FILE TYPES THAT ACTUALLY WORK WELL
ALLOWED = {".txt", ".md", ".csv", ".json", ".html"}

def iter_files():
    for path in SOURCE_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() in ALLOWED:
            yield path

def upload_file(path):
    try:
        with open(path, "rb") as f:
            files = {
                "data": (path.name, f, "application/octet-stream")
            }

            data = {
                "datasetName": DATASET
            }

            headers = {
                "X-Api-Key": API_KEY
            }

            r = requests.post(
                ENDPOINT,
                headers=headers,
                files=files,
                data=data,
                timeout=120
            )

        if r.status_code == 200:
            print(f"OK  {path}")
            return True
        else:
            print(f"ERR {path} -> {r.status_code} {r.text}")
            return False

    except Exception as e:
        print(f"FAIL {path} -> {e}")
        return False


def main():
    if not API_KEY:
        print("❌ Set API key first:")
        print("export COGNEE_API_KEY=your_key")
        return

    files = list(iter_files())
    print(f"Found {len(files)} files")

    ok = 0
    fail = 0

    for file in files:
        if upload_file(file):
            ok += 1
        else:
            fail += 1

        time.sleep(0.3)  # avoid rate limiting

    print(f"\nDONE → OK: {ok}, FAIL: {fail}")


if __name__ == "__main__":
    main()
    