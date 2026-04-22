#!/usr/bin/env python3
"""
Render JSON or YAML as a standalone HTML page (table when data is a list of
objects; otherwise pretty-printed, escaped text).  Matches csv2html.py styling.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

# Skip embedding extremely large files (browser-friendly cap)
MAX_EMBED_BYTES = 5 * 1024 * 1024

BASE_CSS = """
    :root {
      --bg: #0f172a;
      --panel: #111827;
      --text: #e5e7eb;
      --muted: #94a3b8;
      --accent: #38bdf8;
      --border: #334155;
      --row-alt: #0b1220;
      --hover: #1e293b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
      color: var(--text);
    }
    .container { max-width: 1400px; margin: 0 auto; padding: 32px 20px 40px; }
    .card {
      background: rgba(17, 24, 39, 0.92);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }
    .header {
      padding: 24px 24px 16px;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, rgba(30,41,59,.9), rgba(17,24,39,.95));
    }
    h1 { margin: 0 0 10px; font-size: 28px; color: #fff; font-family: ui-sans-serif, system-ui, sans-serif; }
    .subtitle { margin: 0; color: var(--muted); font-size: 14px; font-family: ui-sans-serif, system-ui, sans-serif; }
    .warn {
      margin: 16px 24px;
      padding: 12px 14px;
      background: rgba(180, 83, 9, 0.2);
      border: 1px solid rgba(245, 158, 11, 0.4);
      color: #fcd34d;
      border-radius: 10px;
      font-size: 14px;
      font-family: ui-sans-serif, system-ui, sans-serif;
    }
    .pre-wrap {
      margin: 0;
      padding: 20px 24px 24px;
      overflow: auto;
      max-height: 80vh;
      font-size: 13px;
      line-height: 1.5;
      white-space: pre;
      color: #dbe4ee;
    }
    .table-wrap { overflow: auto; max-height: 75vh; }
    table { width: 100%; border-collapse: collapse; min-width: 500px; font-family: ui-sans-serif, system-ui, sans-serif; }
    thead th {
      position: sticky; top: 0; z-index: 2;
      background: #172033; color: #f8fafc; text-align: left; font-size: 13px;
      border-bottom: 1px solid var(--border); padding: 12px 10px;
    }
    tbody td {
      padding: 10px; border-bottom: 1px solid rgba(51, 65, 85, 0.5);
      vertical-align: top; color: #dbe4ee; font-size: 13px; line-height: 1.4;
      word-break: break-word; font-family: ui-monospace, monospace; font-size: 12px;
    }
    tbody tr:nth-child(even) { background: var(--row-alt); }
    tbody tr:hover { background: var(--hover); }
    .footer {
      padding: 14px 24px 20px; color: var(--muted); font-size: 12px;
      font-family: ui-sans-serif, system-ui, sans-serif; border-top: 1px solid var(--border);
    }
"""

def render_page(
    title: str,
    source_name: str,
    source_kind: str,
    body_html: str,
    footer_note: str,
) -> str:
    """Build full document (CSS must not pass through str.format — braces)."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
{BASE_CSS}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <div class="header">
        <h1>{esc(title)}</h1>
        <p class="subtitle">Generated from <strong>{esc(source_name)}</strong> ({esc(source_kind)})</p>
      </div>
{body_html}
      <div class="footer">
        {esc(footer_note)}
      </div>
    </div>
  </div>
</body>
</html>
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def cell_value(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (str, int, float, bool)):
        return esc(str(v))
    return esc(json.dumps(v, ensure_ascii=False))


def is_tabular_list(data: Any) -> bool:
    if not isinstance(data, list) or len(data) < 1:
        return False
    if not all(isinstance(x, dict) for x in data):
        return False
    return True


def build_table(keys: list[str], rows: list[dict[str, Any]]) -> str:
    th = "".join(f"<th>{esc(k)}</th>" for k in keys)
    trs: list[str] = []
    for row in rows:
        tds = "".join(
            f"<td>{cell_value(row.get(k))}</td>" for k in keys
        )
        trs.append(f"<tr>{tds}</tr>")
    return f"""
      <div class="table-wrap">
        <table>
          <thead><tr>{th}</tr></thead>
          <tbody>
            {"".join(trs)}
          </tbody>
        </table>
      </div>"""


def pretty_text(data: Any, source_path: Path) -> str:
    if source_path.suffix.lower() in (".yml", ".yaml") and yaml is not None:
        try:
            return yaml.dump(
                data, default_flow_style=False, allow_unicode=True, sort_keys=False
            )
        except Exception:
            pass
    return json.dumps(data, indent=2, ensure_ascii=False)


def main() -> None:
    if len(sys.argv) != 3:
        print(
            "Usage: python3 jsonyaml2html.py input.json|yaml output.html",
            file=sys.stderr,
        )
        print(
            "  (output may be under viewable/<path>/… to mirror the source tree)",
            file=sys.stderr,
        )
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    if not input_file.is_file():
        print(f"Error: input not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    ext = input_file.suffix.lower()
    if ext == ".json":
        kind = "JSON"
    elif ext in (".yml", ".yaml"):
        kind = "YAML"
        if yaml is None:
            print("Error: PyYAML is required for YAML. Install with: pip install pyyaml", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: expected .json, .yml, or .yaml, got {ext}", file=sys.stderr)
        sys.exit(1)

    size = input_file.stat().st_size
    title = input_file.stem.replace("_", " ").replace("-", " ").title()
    name = input_file.name

    if size > MAX_EMBED_BYTES:
        body = f"""
      <p class="warn">File is {size / (1024*1024):.1f} MB (limit {MAX_EMBED_BYTES // (1024*1024)} MB for this viewer).
      Open the raw {esc(kind)} file in your editor or inspect it with tooling.</p>"""
        footer = f"Source: {name} — not embedded (too large)."
        out = render_page(title, name, kind, body, footer)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(out, encoding="utf-8")
        print(f"Created (oversize stub): {output_file}")
        return

    raw = input_file.read_text(encoding="utf-8-sig")
    if ext == ".json":
        try:
            data: Any = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        data = yaml.safe_load(raw)
        if data is None:
            data = {}

    if is_tabular_list(data):
        keys = sorted({k for row in data for k in row.keys()})
        body = build_table(keys, data)  # type: ignore[arg-type]
        footer = f"Table: {len(data)} row(s), {len(keys)} column(s). Nested values are shown as JSON text."
    else:
        text = pretty_text(data, input_file)
        body = f'<pre class="pre-wrap">{esc(text)}</pre>'
        footer = "Pretty-printed view. For list-of-objects with uniform keys, a table is shown instead."

    out = render_page(title, name, kind, body, footer)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(out, encoding="utf-8")
    print(f"Created: {output_file}")


if __name__ == "__main__":
    main()
