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
        **Keywords:** term1; term2; term3
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

def extract_abstract_and_body(tex: str) -> tuple[str, str, str]:
    """Return (pre_abstract block, abstract text, body from first numbered subsection onward).

    pre_abstract captures any content that appears between \\begin{document} and
    \\subsection{Abstract} that is not part of the title/header block — specifically
    CONFIDENTIAL notices and unnumbered summary sections such as 'Results at a Glance'.
    These are injected into the final document after \\maketitle and keywords but before
    \\begin{abstract}.
    """
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

    # ── Extract pre-abstract block ─────────────────────────────────────────
    # Everything between \begin{document} and \subsection{Abstract} is normally
    # the title section header block, which the postprocessor replaces with
    # \maketitle.  But authors may include two extra elements there:
    #   1. A CONFIDENTIAL notice (bold paragraph before the \section{title})
    #   2. An unnumbered summary section (e.g. "Results at a Glance")
    # We extract these and re-inject them after \maketitle.
    pre_abstract = ""
    doc_match = re.search(r"\\begin\{document\}", tex)
    if doc_match:
        pre_block = tex[doc_match.end():m_abs.start()]

        # 1. CONFIDENTIAL notice: bold paragraph before the \section{} title
        conf_match = re.search(r"\\textbf\{(CONFIDENTIAL[^}]*)\}", pre_block)
        if conf_match:
            pre_abstract += (
                "\\begin{center}\n"
                "\\textbf{\\large " + conf_match.group(1) + "}\n"
                "\\end{center}\n\n"
                "\\bigskip\n\n"
            )

        # 2. Unnumbered summary subsections (e.g. "Results at a Glance")
        # Match \subsection{<non-digit-starting title>} ... up to the next \subsection
        for m in re.finditer(
            r"(\\subsection\{(?!\d)(?P<title>[^}]+)\}"
            r"(?:\\label\{[^}]+\})?\s*"
            r"(?P<content>.*?))"
            r"(?=\\subsection\{|\\begin\{center\}\\rule|\Z)",
            pre_block,
            re.DOTALL,
        ):
            title = m.group("title").strip()
            content = m.group("content").strip()
            # Strip trailing \rule dividers from content
            content = re.sub(
                r"\\begin\{center\}\\rule\{[^}]+\}\{[^}]+\}\\end\{center\}\s*$",
                "",
                content,
            ).strip()
            if content:
                pre_abstract += f"\\subsection*{{{title}}}\n\n{content}\n\n\\bigskip\n\n"

    return pre_abstract, abstract_raw, rest


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
# Pandoc code-block preamble (stripped when we replace the document preamble)
# ---------------------------------------------------------------------------

def extract_pandoc_code_preamble(tex: str) -> str:
    """
    Pull Pandoc's fancyvrb + syntax-highlighting definitions from standalone .tex.

    Postprocess replaces Pandoc's preamble; without these lines, \\begin{Shaded} and
    \\begin{Highlighting} blocks render as a single garbled line in the PDF.
    """
    m = re.search(
        r"(\\usepackage\{color\}\s*\n"
        r"\\usepackage\{fancyvrb\}.*?"
        r"\\newcommand\{\\WarningTok\}.*?\n)"
        r"(?=\\usepackage\{longtable)",
        tex,
        re.DOTALL,
    )
    return (m.group(1) + "\n") if m else ""


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
\usepackage{xurl}
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
                   keywords: str = "", version: str = "",
                   packages: str = PACKAGES,
                   pre_abstract: str = "") -> str:
    date_version = f"\\small {date}" + (f" \\\\ v{version}" if version else "")
    keywords_block = ""
    if keywords.strip():
        keywords_block = f"\\noindent\\textbf{{Keywords:}} {keywords}\n\n"
    pre_abstract_block = (pre_abstract + "\n") if pre_abstract.strip() else ""
    return (
        packages
        + f"\\title{{{title}}}\n"
        + f"\\author{{{author}}}\n"
        + f"\\date{{{date_version}}}\n\n"
        + "\\begin{document}\n"
        + "\\maketitle\n\n"
        + keywords_block
        + pre_abstract_block
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
_DEFAULT_KEYWORDS = ""


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
    ap.add_argument("--keywords", default=None,
                    help="Keywords line for title page (overrides --md)")
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
    keywords = resolve(args.keywords, "keywords", _DEFAULT_KEYWORDS)

    tex = args.input.read_text(encoding="utf-8")
    pre_abstract, abstract, body = extract_abstract_and_body(tex)
    body = promote_subsection_headings(body)
    body = re.sub(
        r"\\includegraphics\[keepaspectratio\]",
        r"\\includegraphics[width=\\linewidth,keepaspectratio]",
        body,
    )

    # Rewrite absolute image paths to paths relative to the output .tex directory.
    # Markdown sources use absolute paths (e.g. /home/user/.../figures/foo.png) so
    # the IDE preview works regardless of where the .md file lives.  pdflatex runs
    # from inside the paper directory, so the .tex must use paths relative to that
    # directory (e.g. figures/foo.png).
    out_dir = args.output.parent.resolve()

    def _rewrite_img_path(m: re.Match) -> str:
        path_str = m.group(1)
        if path_str.startswith("/"):
            try:
                rel = str(Path(path_str).resolve().relative_to(out_dir))
                return "{" + rel + "}"
            except ValueError:
                pass
        return m.group(0)

    body = re.sub(
        r"\{(/[^}]+\.(?:png|jpg|jpeg|pdf|eps|svg))\}",
        _rewrite_img_path,
        body,
    )

    packages = PACKAGES
    code_preamble = extract_pandoc_code_preamble(tex)
    if code_preamble:
        packages = PACKAGES + "\n" + code_preamble

    preamble = build_preamble(title, author, date, keywords, version, packages=packages,
                              pre_abstract=pre_abstract)
    out = preamble + abstract + "\n\\end{abstract}\n\n" + body
    if "\\end{document}" not in out:
        out += "\n\\end{document}\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(out, encoding="utf-8")
    print(f"Wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
