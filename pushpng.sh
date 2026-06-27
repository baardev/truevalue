#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 <<'PY' | git lfs push --object-id origin --stdin
import os
import re
import subprocess

paths = subprocess.check_output(
    ["git", "ls-tree", "-r", "HEAD", "--name-only", "docnav/Research/papers/"],
    text=True,
).splitlines()

oids = []
for path in paths:
    if not (path.endswith(".pdf") or path.endswith(".png")):
        continue

    content = subprocess.check_output(["git", "show", f"HEAD:{path}"], text=True)
    if not content.startswith("version https://git-lfs.github.com"):
        continue

    match = re.search(r"oid sha256:([a-f0-9]+)", content)
    if not match:
        continue

    oid = match.group(1)
    obj = f".git/lfs/objects/{oid[:2]}/{oid[2:4]}/{oid}"
    if os.path.isfile(obj):
        oids.append(oid)

print("\n".join(oids))
PY
