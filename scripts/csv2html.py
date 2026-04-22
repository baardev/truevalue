#!/usr/bin/env python3

import csv
import html
import sys
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #0f172a;
      --panel: #111827;
      --panel-2: #1f2937;
      --text: #e5e7eb;
      --muted: #94a3b8;
      --accent: #38bdf8;
      --accent-2: #0ea5e9;
      --border: #334155;
      --row-alt: #0b1220;
      --hover: #1e293b;
      --shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
      color: var(--text);
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 32px 20px 40px;
    }}

    .card {{
      background: rgba(17, 24, 39, 0.92);
      border: 1px solid var(--border);
      border-radius: 16px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }}

    .header {{
      padding: 24px 24px 16px;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, rgba(30,41,59,.9), rgba(17,24,39,.95));
    }}

    h1 {{
      margin: 0 0 10px;
      font-size: 28px;
      line-height: 1.2;
      color: white;
    }}

    .subtitle {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
    }}

    .controls {{
      padding: 16px 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      border-bottom: 1px solid var(--border);
      background: rgba(15, 23, 42, 0.65);
    }}

    .search-box {{
      flex: 1 1 320px;
      min-width: 240px;
    }}

    input[type="text"] {{
      width: 100%;
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #0b1220;
      color: var(--text);
      outline: none;
      font-size: 14px;
    }}

    input[type="text"]:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }}

    .meta {{
      color: var(--muted);
      font-size: 14px;
      white-space: nowrap;
    }}

    .table-wrap {{
      overflow: auto;
      max-height: 75vh;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 700px;
    }}

    thead th {{
      position: sticky;
      top: 0;
      z-index: 2;
      background: #172033;
      color: #f8fafc;
      text-align: left;
      font-size: 14px;
      letter-spacing: 0.02em;
      border-bottom: 1px solid var(--border);
      padding: 14px 12px;
      cursor: pointer;
      user-select: none;
    }}

    thead th:hover {{
      background: #1d2940;
    }}

    tbody td {{
      padding: 12px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.5);
      vertical-align: top;
      color: #dbe4ee;
      font-size: 14px;
      line-height: 1.4;
      word-break: break-word;
    }}

    tbody tr:nth-child(even) {{
      background: var(--row-alt);
    }}

    tbody tr:hover {{
      background: var(--hover);
    }}

    .sort-indicator {{
      color: var(--accent);
      margin-left: 6px;
      font-size: 12px;
    }}

    .footer {{
      padding: 14px 24px 20px;
      color: var(--muted);
      font-size: 12px;
    }}

    .hidden {{
      display: none;
    }}

    @media (max-width: 720px) {{
      h1 {{
        font-size: 22px;
      }}

      .container {{
        padding: 16px 10px 24px;
      }}

      .header, .controls, .footer {{
        padding-left: 14px;
        padding-right: 14px;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <div class="header">
        <h1>{title}</h1>
        <p class="subtitle">CSV viewer generated from <strong>{source_name}</strong></p>
      </div>

      <div class="controls">
        <div class="search-box">
          <input type="text" id="searchInput" placeholder="Search all rows...">
        </div>
        <div class="meta">
          Rows shown: <span id="rowCount">{row_count}</span> / {row_count}
        </div>
      </div>

      <div class="table-wrap">
        <table id="csvTable">
          <thead>
            <tr>
              {headers_html}
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>

      <div class="footer">
        Click a column header to sort. Use the search box to filter rows.
      </div>
    </div>
  </div>

  <script>
    const searchInput = document.getElementById("searchInput");
    const table = document.getElementById("csvTable");
    const tbody = table.querySelector("tbody");
    const rowCount = document.getElementById("rowCount");
    const headers = table.querySelectorAll("thead th");

    searchInput.addEventListener("input", function () {{
      const query = this.value.toLowerCase();
      let visible = 0;

      for (const row of tbody.rows) {{
        const text = row.innerText.toLowerCase();
        const match = text.includes(query);
        row.classList.toggle("hidden", !match);
        if (match) visible++;
      }}

      rowCount.textContent = visible;
    }});

    headers.forEach((header, index) => {{
      header.dataset.direction = "asc";

      header.addEventListener("click", () => {{
        const rows = Array.from(tbody.rows);
        const currentDirection = header.dataset.direction;
        const newDirection = currentDirection === "asc" ? "desc" : "asc";

        headers.forEach(h => {{
          h.dataset.direction = "";
          const indicator = h.querySelector(".sort-indicator");
          if (indicator) indicator.textContent = "";
        }});

        rows.sort((a, b) => {{
          const aText = a.cells[index]?.innerText.trim() ?? "";
          const bText = b.cells[index]?.innerText.trim() ?? "";

          const aNum = parseFloat(aText.replace(/,/g, ""));
          const bNum = parseFloat(bText.replace(/,/g, ""));

          let comparison = 0;

          if (!isNaN(aNum) && !isNaN(bNum)) {{
            comparison = aNum - bNum;
          }} else {{
            comparison = aText.localeCompare(bText, undefined, {{
              numeric: true,
              sensitivity: "base"
            }});
          }}

          return newDirection === "asc" ? comparison : -comparison;
        }});

        for (const row of rows) {{
          tbody.appendChild(row);
        }}

        header.dataset.direction = newDirection;
        const indicator = header.querySelector(".sort-indicator");
        if (indicator) {{
          indicator.textContent = newDirection === "asc" ? "▲" : "▼";
        }}
      }});
    }});
  </script>
</body>
</html>
"""


def escape(value):
    return html.escape("" if value is None else str(value))


def build_headers(headers):
    parts = []
    for h in headers:
        parts.append(
            f'<th>{escape(h)}<span class="sort-indicator"></span></th>'
        )
    return "\n".join(parts)


def build_rows(rows):
    body = []
    for row in rows:
        tds = "".join(f"<td>{escape(cell)}</td>" for cell in row)
        body.append(f"<tr>{tds}</tr>")
    return "\n".join(body)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 csv2html.py input.csv output.html")
        print("  (output may be under viewable/<path>/… to mirror the source tree)")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: input file not found: {input_file}")
        sys.exit(1)

    with input_file.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        all_rows = list(reader)

    if not all_rows:
        print("Error: CSV file is empty.")
        sys.exit(1)

    headers = all_rows[0]
    rows = all_rows[1:]

    title = input_file.stem.replace("_", " ").replace("-", " ").title()

    html_output = HTML_TEMPLATE.format(
        title=escape(title),
        source_name=escape(input_file.name),
        headers_html=build_headers(headers),
        rows_html=build_rows(rows),
        row_count=len(rows),
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_output, encoding="utf-8")
    print(f"Created: {output_file}")


if __name__ == "__main__":
    main()
