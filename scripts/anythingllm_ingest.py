#!/usr/bin/env python3
"""Compatibility wrapper for the root AnythingLLM ingestion script.

The canonical implementation lives at:

    anythingllm_ingest.py

This wrapper exists so commands that use the historical scripts path still
work. It changes the working directory to the repository root before running
the canonical script, so relative manifest paths such as
`frontend/docs/anythingllm_manifest.yaml` resolve correctly no matter where
the wrapper is invoked from.
"""

from __future__ import annotations

import os
import runpy
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    os.chdir(repo_root)
    runpy.run_path(str(repo_root / "anythingllm_ingest.py"), run_name="__main__")


if __name__ == "__main__":
    main()
