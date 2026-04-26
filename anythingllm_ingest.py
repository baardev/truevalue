#!/usr/bin/env python3
"""Manifest-driven ingestion for AnythingLLM workspaces.

This script discovers repository documents from a YAML manifest, filters out
generated or duplicate files, uploads the selected files to AnythingLLM, and
then adds the uploaded document locations to a workspace embedding index.

Default manifest:
    frontend/docs/anythingllm_manifest.yaml

Required environment variables for real uploads:
    ANYTHINGLLM_BASE_URL
        Use http://localhost:3001 if you are running AnythingLLM locally.
    ANYTHINGLLM_API_KEY
        Required. The script reads the API key only from this environment
        variable. Do not put API keys in the manifest or commit them to the repo.
    ANYTHINGLLM_WORKSPACE
        Use truevalue-analytics-documents for the starter manifest in this repo.

Recommended values for this project:
    export ANYTHINGLLM_BASE_URL="http://localhost:3001"
    export ANYTHINGLLM_API_KEY="paste-your-anythingllm-api-key-here"
    export ANYTHINGLLM_WORKSPACE="truevalue-analytics-documents"

How to get the workspace slug:
    Create or open the AnythingLLM workspace named "TrueValue Analytics
    Documents". The slug is usually the lower-case URL-safe workspace name.
    For this project, the starter manifest expects truevalue-analytics-documents.

How to get the API key:
    In AnythingLLM, open the API or developer settings, create an API key, and
    export that value as ANYTHINGLLM_API_KEY for the shell session where you run
    this script.

Arguments:
    -m, -manifest frontend/docs/anythingllm_manifest.yaml
    -n, -dry-run
        Print the selected files without uploading anything.
    -l, -limit N
        Process only the first N selected files. Useful for testing.
    -v, -verbose
        Print skipped files and API response details.
    -list-workspaces
        Print available workspace names and slugs, then exit.
    -list-documents
        Print uploaded document locations already known to AnythingLLM, then
        exit.
    -locations-file PATH
        Save uploaded document locations to this JSON file.
    -update-from-locations PATH
        Update the workspace using locations from a previous run.
    -update-from-documents
        Read uploaded document locations from AnythingLLM and update the
        workspace without uploading files again.

Typical workflow:
    python scripts/anythingllm_ingest.py -n
    python scripts/anythingllm_ingest.py -n -l 10
    python scripts/anythingllm_ingest.py

The manifest controls include patterns, exclude patterns, maximum file size,
HTML duplicate handling, and AnythingLLM API endpoint paths. Keep generated
folders such as site/ and viewable/ excluded unless you intentionally want
duplicate generated content in the chat corpus.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import mimetypes
import os
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "PyYAML is required. Install it with: pip install pyyaml"
    ) from exc


@dataclass(frozen=True)
class IngestFile:
    path: Path
    rel_path: str
    size_bytes: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload selected repository documents to an AnythingLLM workspace."
    )
    parser.add_argument(
        "-m",
        "-manifest",
        dest="manifest",
        default="frontend/docs/anythingllm_manifest.yaml",
        help="Path to the ingestion manifest.",
    )
    parser.add_argument(
        "-n",
        "-dry-run",
        dest="dry_run",
        action="store_true",
        help="List files without uploading them.",
    )
    parser.add_argument(
        "-l",
        "-limit",
        dest="limit",
        type=int,
        default=0,
        help="Limit number of files processed. Zero means no limit.",
    )
    parser.add_argument(
        "-v",
        "-verbose",
        dest="verbose",
        action="store_true",
        help="Print skipped files and API responses.",
    )
    parser.add_argument(
        "-list-workspaces",
        dest="list_workspaces",
        action="store_true",
        help="Print available AnythingLLM workspace slugs and exit.",
    )
    parser.add_argument(
        "-list-documents",
        dest="list_documents",
        action="store_true",
        help="Print uploaded AnythingLLM document locations and exit.",
    )
    parser.add_argument(
        "-locations-file",
        dest="locations_file",
        default="anythingllm_uploaded_locations.json",
        help="Path to save uploaded document locations.",
    )
    parser.add_argument(
        "-update-from-locations",
        dest="update_from_locations",
        default="",
        help="Update workspace from a saved locations JSON file.",
    )
    parser.add_argument(
        "-update-from-documents",
        dest="update_from_documents",
        action="store_true",
        help="Update workspace from existing uploaded documents in AnythingLLM.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Manifest not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise SystemExit("Manifest must be a YAML mapping.")
    return data


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    raise SystemExit(f"Expected a string or list, got {type(value).__name__}")


def is_match(rel_path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, pattern) for pattern in patterns)


def has_markdown_sibling(path: Path) -> bool:
    return path.with_suffix(".md").exists() or path.with_suffix(".markdown").exists()


def discover_files(repo_root: Path, manifest: dict[str, Any], verbose: bool) -> list[IngestFile]:
    include_patterns = as_list(manifest.get("include"))
    exclude_patterns = as_list(manifest.get("exclude"))
    allow_html_patterns = as_list(manifest.get("allow_html"))
    max_size_mb = float(manifest.get("max_size_mb", 10))
    max_size_bytes = int(max_size_mb * 1024 * 1024)
    skip_html_with_markdown = bool(manifest.get("skip_html_when_markdown_exists", True))

    if not include_patterns:
        raise SystemExit("Manifest must include at least one include pattern.")

    seen: set[Path] = set()
    selected: list[IngestFile] = []

    for pattern in include_patterns:
        for path in repo_root.glob(pattern):
            if not path.is_file():
                continue

            path = path.resolve()
            if path in seen:
                continue
            seen.add(path)

            rel_path = path.relative_to(repo_root).as_posix()

            if is_match(rel_path, exclude_patterns):
                if verbose:
                    print(f"skip excluded: {rel_path}")
                continue

            if path.suffix.lower() in {".html", ".htm"}:
                html_allowed = is_match(rel_path, allow_html_patterns)
                if skip_html_with_markdown and has_markdown_sibling(path) and not html_allowed:
                    if verbose:
                        print(f"skip duplicate html: {rel_path}")
                    continue

            size_bytes = path.stat().st_size
            if size_bytes > max_size_bytes:
                if verbose:
                    print(f"skip too large: {rel_path} ({size_bytes} bytes)")
                continue

            selected.append(IngestFile(path=path, rel_path=rel_path, size_bytes=size_bytes))

    selected.sort(key=lambda item: item.rel_path)
    return selected


def require_api_config(manifest: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    api = manifest.get("api") or {}
    if not isinstance(api, dict):
        raise SystemExit("Manifest api section must be a mapping.")

    base_url = os.environ.get("ANYTHINGLLM_BASE_URL") or api.get("base_url")
    api_key = os.environ.get("ANYTHINGLLM_API_KEY")
    workspace_slug = os.environ.get("ANYTHINGLLM_WORKSPACE") or manifest.get("workspace_slug")

    if not base_url:
        raise SystemExit("Set ANYTHINGLLM_BASE_URL or api.base_url in the manifest.")
    if not api_key:
        raise SystemExit("Set ANYTHINGLLM_API_KEY in your shell. Do not store API keys in the repo.")
    if not workspace_slug:
        raise SystemExit("Set ANYTHINGLLM_WORKSPACE or workspace_slug in the manifest.")

    upload_path = str(api.get("upload_path", "/api/v1/document/upload"))
    workspaces_path = str(api.get("workspaces_path", "/api/v1/workspaces"))
    documents_path = str(api.get("documents_path", "/api/v1/documents"))
    update_template = str(
        api.get("workspace_update_path_template", "/api/v1/workspace/{workspace_slug}/update-embeddings")
    )
    update_path = update_template.format(workspace_slug=workspace_slug)
    return str(base_url), str(api_key), upload_path, update_path, workspaces_path, documents_path


def request_get_json(url: str, api_key: str) -> dict[str, Any] | list[Any]:
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=120) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach {url}: {exc}") from exc

    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Non-JSON response from {url}: {raw[:500]}") from exc


def request_json(url: str, api_key: str, body: bytes, content_type: str) -> dict[str, Any]:
    request = Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=120) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach {url}: {exc}") from exc

    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Non-JSON response from {url}: {raw[:500]}") from exc


def build_multipart_file(field_name: str, path: Path) -> tuple[bytes, str]:
    boundary = "anythingllm" + uuid.uuid4().hex
    dash2 = "-" * 2
    crlf = "\r\n"
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    header = (
        f"{dash2}{boundary}{crlf}"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{path.name}"{crlf}'
        f"Content-Type: {mime_type}{crlf}{crlf}"
    ).encode("utf-8")
    footer = f"{crlf}{dash2}{boundary}{dash2}{crlf}".encode("utf-8")
    return header + path.read_bytes() + footer, f"multipart/form-data; boundary={boundary}"


def upload_file(base_url: str, api_key: str, upload_path: str, item: IngestFile) -> list[str]:
    body, content_type = build_multipart_file("file", item.path)
    response = request_json(urljoin(base_url, upload_path), api_key, body, content_type)
    documents = response.get("documents") or []
    locations: list[str] = []
    for document in documents:
        if isinstance(document, dict) and document.get("location"):
            locations.append(str(document["location"]))
    if not locations:
        raise RuntimeError(f"Upload succeeded but returned no document location for {item.rel_path}")
    return locations


def update_workspace(base_url: str, api_key: str, update_path: str, locations: list[str]) -> dict[str, Any]:
    payload = json.dumps({"adds": locations, "deletes": []}).encode("utf-8")
    try:
        return request_json(urljoin(base_url, update_path), api_key, payload, "application/json")
    except RuntimeError as exc:
        if "HTTP 400" not in str(exc):
            raise
        fallback = json.dumps({"adds": locations}).encode("utf-8")
        return request_json(urljoin(base_url, update_path), api_key, fallback, "application/json")


def list_workspaces(base_url: str, api_key: str, workspaces_path: str) -> None:
    response = request_get_json(urljoin(base_url, workspaces_path), api_key)
    if isinstance(response, dict):
        workspaces = response.get("workspaces") or []
    else:
        workspaces = response

    if not workspaces:
        print("No workspaces returned.")
        return

    print("Available AnythingLLM workspaces:")
    for workspace in workspaces:
        if not isinstance(workspace, dict):
            continue
        name = workspace.get("name", "")
        slug = workspace.get("slug", "")
        print(f"name={name} slug={slug}")


def collect_document_locations(value: Any) -> list[str]:
    locations: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {"location", "docpath"} and isinstance(nested, str):
                locations.append(nested)
            elif key == "name" and isinstance(nested, str) and nested.endswith(".json"):
                if "/" in nested:
                    locations.append(nested)
                else:
                    locations.append(f"custom-documents/{nested}")
            else:
                locations.extend(collect_document_locations(nested))
    elif isinstance(value, list):
        for item in value:
            locations.extend(collect_document_locations(item))
    return locations


def get_uploaded_document_locations(base_url: str, api_key: str, documents_path: str) -> list[str]:
    response = request_get_json(urljoin(base_url, documents_path), api_key)
    locations = collect_document_locations(response)
    unique_locations = sorted(set(locations))
    return [location for location in unique_locations if location.endswith(".json")]


def list_uploaded_documents(base_url: str, api_key: str, documents_path: str) -> None:
    locations = get_uploaded_document_locations(base_url, api_key, documents_path)
    if not locations:
        print("No uploaded document locations found.")
        return
    print(f"Uploaded AnythingLLM documents: {len(locations)}")
    for location in locations:
        print(location)


def save_locations(path: Path, locations: list[str]) -> None:
    data = {"locations": locations}
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def load_locations(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"Locations file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        locations = data.get("locations") or []
    elif isinstance(data, list):
        locations = data
    else:
        raise SystemExit("Locations file must contain a list or a mapping with locations.")
    return [str(location) for location in locations]


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    manifest_path = (repo_root / args.manifest).resolve()
    manifest = load_manifest(manifest_path)

    if args.list_workspaces:
        base_url, api_key, _upload_path, _update_path, workspaces_path, _documents_path = require_api_config(manifest)
        list_workspaces(base_url, api_key, workspaces_path)
        return 0

    if args.list_documents:
        base_url, api_key, _upload_path, _update_path, _workspaces_path, documents_path = require_api_config(manifest)
        list_uploaded_documents(base_url, api_key, documents_path)
        return 0

    if args.update_from_locations:
        base_url, api_key, _upload_path, update_path, _workspaces_path, _documents_path = require_api_config(manifest)
        locations_path = (repo_root / args.update_from_locations).resolve()
        locations = load_locations(locations_path)
        print(f"Updating workspace with {len(locations)} saved document locations.")
        response = update_workspace(base_url, api_key, update_path, locations)
        if args.verbose:
            print(json.dumps(response, indent=2))
        print("AnythingLLM workspace update complete.")
        return 0

    if args.update_from_documents:
        base_url, api_key, _upload_path, update_path, _workspaces_path, documents_path = require_api_config(manifest)
        locations = get_uploaded_document_locations(base_url, api_key, documents_path)
        if not locations:
            raise SystemExit("No uploaded document locations found in AnythingLLM.")
        print(f"Updating workspace with {len(locations)} existing uploaded document locations.")
        response = update_workspace(base_url, api_key, update_path, locations)
        if args.verbose:
            print(json.dumps(response, indent=2))
        print("AnythingLLM workspace update complete.")
        return 0

    files = discover_files(repo_root, manifest, args.verbose)
    if args.limit > 0:
        files = files[: args.limit]

    print(f"Manifest: {manifest_path.relative_to(repo_root)}")
    print(f"Selected files: {len(files)}")
    for item in files:
        print(f"{item.rel_path}\t{item.size_bytes} bytes")

    if args.dry_run:
        print("Dry run complete. No files uploaded.")
        return 0

    base_url, api_key, upload_path, update_path, _workspaces_path, _documents_path = require_api_config(manifest)
    all_locations: list[str] = []

    for index, item in enumerate(files, start=1):
        print(f"[{index}/{len(files)}] upload {item.rel_path}")
        locations = upload_file(base_url, api_key, upload_path, item)
        all_locations.extend(locations)
        if args.verbose:
            print(json.dumps({"locations": locations}, indent=2))

    if not all_locations:
        print("No document locations returned. Workspace not updated.")
        return 0

    locations_path = (repo_root / args.locations_file).resolve()
    save_locations(locations_path, all_locations)
    print(f"Saved uploaded document locations to {locations_path.relative_to(repo_root)}")

    print(f"Updating workspace with {len(all_locations)} document locations.")
    try:
        response = update_workspace(base_url, api_key, update_path, all_locations)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        print("Workspace update failed. The uploads succeeded and locations were saved.", file=sys.stderr)
        print("Run with -list-workspaces to confirm the correct workspace slug.", file=sys.stderr)
        print(
            f"Then retry with -update-from-locations {locations_path.relative_to(repo_root)}",
            file=sys.stderr,
        )
        return 1
    if args.verbose:
        print(json.dumps(response, indent=2))
    print("AnythingLLM ingestion complete.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)
