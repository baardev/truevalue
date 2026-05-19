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

\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

"""

# Defaults kept for paper 6 backward compatibility.
_DEFAULT_TITLE = (
    r"The Qualitative Nature of One, Two, and Three:\\"
    "\n"
    r"\large Structural Role Assignment in Minimal Recursive Systems"
)
_DEFAULT_AUTHOR = r"Jeffrey W. Milton\\[4pt]{\small Independent Researcher}"
_DEFAULT_DATE = "2026"
_DEFAULT_ARXIV = r"math.HO; math.LO (secondary: cs.LO; q-bio.NC)"


def build_preamble(title: str, author: str, date: str, arxiv: str) -> str:
    return (
        PACKAGES
        + f"\\title{{{title}}}\n"
        + f"\\author{{{author}}}\n"
        + f"\\date{{{date}}}\n\n"
        + "\\begin{document}\n"
        + "\\maketitle\n\n"
        + f"\\noindent\\textbf{{Provisional arXiv subjects:}} {arxiv}\n\n"
        + "\\begin{abstract}\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, help="Pandoc standalone .tex")
    ap.add_argument("output", type=Path, help="Output .tex")
    ap.add_argument("--title", default=_DEFAULT_TITLE,
                    help="LaTeX title string (use \\\\ for line break)")
    ap.add_argument("--author", default=_DEFAULT_AUTHOR,
                    help="LaTeX author string")
    ap.add_argument("--date", default=_DEFAULT_DATE)
    ap.add_argument("--arxiv", default=_DEFAULT_ARXIV,
                    help="Provisional arXiv subject string")
    args = ap.parse_args()
    tex = args.input.read_text(encoding="utf-8")

    abstract, body = extract_abstract_and_body(tex)
    body = promote_subsection_headings(body)

    preamble = build_preamble(args.title, args.author, args.date, args.arxiv)
    out = preamble + abstract + "\n\\end{abstract}\n\n" + body
    if "\\end{document}" not in out:
        out += "\n\\end{document}\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(out, encoding="utf-8")
    print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
