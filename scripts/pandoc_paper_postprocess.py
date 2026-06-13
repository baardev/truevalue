#!/usr/bin/env python3
"""
Post-process Pandoc standalone LaTeX: fix section hierarchy (subtitle + abstract + numbered sections).
Used for research papers under docnav/Research/papers/.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Markdown header parser
# ---------------------------------------------------------------------------

def _parse_md_header(md_path: Path) -> dict:
    """
    Parse the canonical paper header fields from a Markdown source file.

    Expected header format (fields may appear in any order after the title):
        # Full Title: Optional Subtitle

        **Author:** J. W. Milton, Affiliation Name
        **Version:** 1.0
        **Date:** D Month YYYY
        **Proposed arXiv subjects:** math.CA; math.NT (secondary: ...)
        **Keywords:** ...   (optional)
    """
    text = md_path.read_text(encoding="utf-8")
    result: dict = {}

    # Title: first non-empty line starting with "# "
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            result["title_raw"] = line[2:].strip()
            break

    # Bold-field lines: **Label:** value  (colon is inside the bold markers)
    for m in re.finditer(r"^\*\*([^*]+):\*\*\s*(.+)$", text, re.MULTILINE):
        label = m.group(1).strip().rstrip(":")
        value = m.group(2).strip()
        key = label.lower()
        if "author" in key:
            result["author_raw"] = value
        elif "version" in key:
            result["version"] = value
        elif "date" in key:
            result["date"] = value
        elif "arxiv" in key or "arXiv" in key:
            result["arxiv_label"] = label
            result["arxiv_subjects"] = value
        elif "keyword" in key:
            result["keywords"] = value

    return result


def _md_title_to_latex(title_raw: str) -> str:
    """
    Convert a plain-text paper title to a LaTeX \\title{} argument.
    If the title contains ': ', the first part becomes the main title
    and the rest becomes a \\large subtitle on the next line.
    """
    if ": " in title_raw:
        main, sub = title_raw.split(": ", 1)
        return main + ":\\\\\n\\large " + sub
    return title_raw


def _md_author_to_latex(author_raw: str) -> str:
    """
    Convert "Name, Affiliation" to "Name\\[4pt]{\\small Affiliation}".
    If there is no comma, use the full string as-is.
    """
    if ", " in author_raw:
        name, affil = author_raw.split(", ", 1)
        return name + "\\\\[4pt]{\\small " + affil + "}"
    return author_raw


# ---------------------------------------------------------------------------
# LaTeX extraction helpers
# ---------------------------------------------------------------------------

def extract_abstract_and_body(tex: str) -> tuple[str, str]:
    """Return (abstract text, body from first numbered \\subsection{1. ...} onward)."""
    m_intro = re.search(
        r"\\subsection\{1\.\s+[^}]+\}(?:\\label\{[^}]+\})?",
        tex,
        re.DOTALL,
    )
    if not m_intro:
        raise ValueError("Could not find first numbered \\\\subsection{1. ...}")
    intro_start = m_intro.start()

    m_abs = re.search(r"\\subsection\{Abstract\}\s*(?:\\label\{[^}]+\})?\s*", tex)
    if not m_abs:
        raise ValueError("Could not find \\\\subsection{Abstract}")
    abs_start = m_abs.end()

    abstract_raw = tex[abs_start:intro_start].strip()
    abstract_raw = re.sub(
        r"\\begin\{center\}\\rule\{[^}]+\}\{[^}]+\}\\end\{center\}\s*$",
        "",
        abstract_raw,
    ).strip()

    rest = tex[intro_start:]
    return abstract_raw, rest


def promote_subsection_headings(body: str) -> str:
    r"""\subsection{N. Title...} -> \section{Title...}; \subsubsection{N.M ...} -> \subsection{...}."""
    body = re.sub(
        r"\\subsection\{(\d+)\.\s+((?:[^}]|\n)+?)\}(\s*\\label\{[^}]+\})?",
        lambda m: "\\section{%s}%s"
        % (re.sub(r"\s+", " ", m.group(2).strip()), m.group(3) or ""),
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"\\subsubsection\{(\d+\.\d+)\s+((?:[^}]|\n)+?)\}(\s*\\label\{[^}]+\})?",
        lambda m: "\\subsection{%s}%s"
        % (re.sub(r"\s+", " ", m.group(2).strip()), m.group(3) or ""),
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"\\subsection\{References[^}]*\}",
        r"\\section{References}",
        body,
        count=1,
    )
    body = re.sub(
        r"\\subsection\{Appendix:",
        r"\\section{Appendix:",
        body,
        count=1,
    )
    return body


# ---------------------------------------------------------------------------
# Preamble builder
# ---------------------------------------------------------------------------

PACKAGES = r"""\pdfoutput=1
\documentclass[12pt]{article}

\usepackage{amsmath, amssymb, amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{longtable}
\usepackage{calc}
\usepackage{etoolbox}
\makeatletter
\patchcmd\longtable{\par}{\if@noskipsec\mbox{}\fi\par}{}{}
\makeatother
\IfFileExists{footnotehyper.sty}{\usepackage{footnotehyper}}{\usepackage{footnote}}
\makesavenoteenv{longtable}
\usepackage[colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue]{hyperref}
\usepackage{geometry}
\geometry{margin=1in}

\makeatletter
\newsavebox\pandoc@box
\newcommand*\pandocbounded[1]{%
  \sbox\pandoc@box{#1}%
  \Gscale@div\@tempa{\textheight}{\dimexpr\ht\pandoc@box+\dp\pandoc@box\relax}%
  \Gscale@div\@tempb{\linewidth}{\wd\pandoc@box}%
  \ifdim\@tempb\p@<\@tempa\p@\let\@tempa\@tempb\fi
  \ifdim\@tempa\p@<\p@\scalebox{\@tempa}{\usebox\pandoc@box}%
  \else\usebox{\pandoc@box}%
  \fi
}
\makeatother
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

"""


def build_preamble(title: str, author: str, date: str,
                   arxiv_subjects: str, arxiv_label: str = "Provisional arXiv subjects",
                   version: str = "") -> str:
    date_version = f"\\small {date}" + (f" \\\\ v{version}" if version else "")
    return (
        PACKAGES
        + f"\\title{{{title}}}\n"
        + f"\\author{{{author}}}\n"
        + f"\\date{{{date_version}}}\n\n"
        + "\\begin{document}\n"
        + "\\maketitle\n\n"
        + f"\\noindent\\textbf{{{arxiv_label}:}} {arxiv_subjects}\n\n"
        + "\\begin{abstract}\n"
    )


# ---------------------------------------------------------------------------
# Defaults (paper-6 backward compatibility)
# ---------------------------------------------------------------------------

_DEFAULT_TITLE = (
    r"The Qualitative Nature of One, Two, and Three:\\"
    "\n"
    r"\large Structural Role Assignment in Minimal Recursive Systems"
)
_DEFAULT_AUTHOR = r"Jeffrey W. Milton\\[4pt]{\small Independent Researcher}"
_DEFAULT_DATE = "2026"
_DEFAULT_ARXIV_LABEL = "Provisional arXiv subjects"
_DEFAULT_ARXIV = r"math.HO; math.LO (secondary: cs.LO; q-bio.NC)"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, help="Pandoc standalone .tex")
    ap.add_argument("output", type=Path, help="Output .tex")
    ap.add_argument("--md", type=Path, default=None,
                    help="Source Markdown file; header fields are read from it automatically")
    ap.add_argument("--title", default=None,
                    help="LaTeX title string (overrides --md)")
    ap.add_argument("--author", default=None,
                    help="LaTeX author string (overrides --md)")
    ap.add_argument("--date", default=None,
                    help="Date string (overrides --md)")
    ap.add_argument("--arxiv-label", default=None,
                    help="arXiv label prefix, e.g. 'Proposed arXiv subjects' (overrides --md)")
    ap.add_argument("--arxiv", default=None,
                    help="arXiv subject string (overrides --md)")
    args = ap.parse_args()

    # Read Markdown header if provided
    md_fields: dict = {}
    if args.md:
        md_fields = _parse_md_header(args.md)

    # Resolve each field: explicit arg > markdown > default
    def resolve(arg_val, md_key, default):
        if arg_val is not None:
            return arg_val
        if md_key in md_fields:
            return md_fields[md_key]
        return default

    title_raw = resolve(args.title, "title_raw", None)
    title = _md_title_to_latex(title_raw) if title_raw else _DEFAULT_TITLE

    author_raw = resolve(args.author, "author_raw", None)
    author = _md_author_to_latex(author_raw) if author_raw else _DEFAULT_AUTHOR

    date = resolve(args.date, "date", _DEFAULT_DATE)
    version = resolve(None, "version", "")
    arxiv_label = resolve(args.arxiv_label, "arxiv_label", _DEFAULT_ARXIV_LABEL)
    arxiv_subjects = resolve(args.arxiv, "arxiv_subjects", _DEFAULT_ARXIV)

    tex = args.input.read_text(encoding="utf-8")
    abstract, body = extract_abstract_and_body(tex)
    body = promote_subsection_headings(body)
    body = re.sub(
        r"\\includegraphics\[keepaspectratio\]",
        r"\\includegraphics[width=\\linewidth,keepaspectratio]",
        body,
    )

    preamble = build_preamble(title, author, date, arxiv_subjects, arxiv_label, version)
    out = preamble + abstract + "\n\\end{abstract}\n\n" + body
    if "\\end{document}" not in out:
        out += "\n\\end{document}\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(out, encoding="utf-8")
    print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
