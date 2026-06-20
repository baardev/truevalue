---
name: faq-md-to-html
description: Convert docnav/FAQ/tholonic-faq.md into docnav/FAQ/tholonic-faq.html. Produces a self-contained HTML page with a sticky two-column TOC, N-D-C role colours, MathJax rendering, IntersectionObserver active highlighting, and callout boxes. Use when the user asks to rebuild, regenerate, or sync the FAQ HTML from the markdown source, or says "convert the FAQ", "rebuild the HTML FAQ", or "update tholonic-faq.html".
disable-model-invocation: true
---

# FAQ Markdown to HTML Converter

Converts `docnav/FAQ/tholonic-faq.md` into `docnav/FAQ/tholonic-faq.html`.

## Source and target

| File | Path |
|---|---|
| Source | `docnav/FAQ/tholonic-faq.md` |
| Output | `docnav/FAQ/tholonic-faq.html` |

**Always read the full source markdown first before writing the HTML.** The markdown is the source of truth. Do not use stale content from memory.

---

## Required HTML structure

### Page layout

Two-column flex layout:

- Left: `#toc-sidebar` — 280px, sticky, `height: 100vh`, scrollable, lists all questions grouped by section
- Right: `<main>` — `flex: 1`, `max-width: 860px`, `padding: 48px 52px 80px`

Mobile breakpoint at 900px: stack columns vertically, TOC becomes static full-width strip.

### TOC sidebar

- One `.toc-section` block per markdown `##` section heading
- Inside each block: a `.toc-section-label` span and a `.toc-questions` `<ul>`
- One `<li><a href="#slug">Question text (shortened)</a></li>` per `###` question
- ID slugs: lowercase, hyphens, no punctuation (e.g. `"What is a tholon?"` → `what-is-tholon`)

### Q&A items

Each `###` question becomes a `<div class="qa" id="slug">` containing:

```html
<div class="qa-question">Question text</div>
<div class="qa-answer"> ... </div>
```

The `.qa-question` gets a blue "Q" badge via `::before` pseudo-element.

---

## N-D-C role colours (canonical — non-negotiable)

| Role | CSS class | Text colour hex |
|---|---|---|
| N (Negotiation) | `.role-n` | `#1d4ed8` (dark blue) |
| D (Definition) | `.role-d` | `#15803d` (dark green) |
| C (Contribution) | `.role-c` | `#b91c1c` (dark red) |

Apply `.role-n`, `.role-d`, `.role-c` to every inline mention of N, D, and C in answer text. Use matching light fills (`#dbeafe`, `#dcfce7`, `#fee2e2`) for callout box backgrounds.

---

## Callout boxes

Use `.callout` with a modifier class for visually distinct inline blocks:

- `.callout-n` — blue left border + blue light fill — use for N-state explanations
- `.callout-d` — green left border + green light fill — use for D definitions
- `.callout-c` — red left border + red light fill — use for C definitions
- `.callout-neutral` — grey left border + grey fill — use for examples and notes

---

## Math rendering

Load MathJax 3 from CDN (async, no defer):

```html
<script>MathJax = { tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] } };</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
```

Wrap display equations in `<div class="math-block">$$...$$</div>` (styled as a bordered, centred panel).

---

## N-D-C context table (special rendering)

The six-row domain table (Plant, Society, Astronomy, History, Science, Mechanics) must have:

- Column headers for N, D, C using `.th-n`, `.th-d`, `.th-c` classes (colour-coded)
- Body cells for N, D, C using `.td-n`, `.td-d`, `.td-c` classes
- First column (context name) using `.td-context` (bold)

---

## IntersectionObserver active TOC highlighting

Add this script before `</body>`:

```javascript
const qaItems = document.querySelectorAll('.qa[id]');
const tocLinks = document.querySelectorAll('#toc-sidebar a');
const tocMap = {};
tocLinks.forEach(a => { tocMap[a.getAttribute('href').slice(1)] = a; });
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const link = tocMap[entry.target.id];
    if (!link) return;
    if (entry.isIntersecting) {
      tocLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      link.scrollIntoView({ block: 'nearest' });
    }
  });
}, { rootMargin: '-10% 0px -80% 0px', threshold: 0 });
qaItems.forEach(el => observer.observe(el));
```

Active TOC links get: `color: #1d4ed8; font-weight: 600; border-left: 2px solid #1d4ed8; background: #dbeafe`.

---

## Conversion rules for markdown elements

| Markdown | HTML |
|---|---|
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `**N**`, `**D**`, `**C**` standalone | wrap in `.role-n`, `.role-d`, `.role-c` |
| Pipe tables | `<table>` with styled `<th>` and `<td>` |
| `- item` lists | `<ul><li>` |
| `$$...$$` | `<div class="math-block">$$...$$</div>` |
| `$...$` inline | keep as-is (MathJax renders) |
| `---` section separator | not rendered (answered items are naturally separated by `.qa` card borders) |
| `## Section` | `.section-heading` div above the section's `.qa` cards |
| `[text](file.md)` | `<a href="/docnav/view.html?file=docnav/FAQ/file.md">text</a>` (resolve to repo-relative path first) |

### Markdown link rewriting rule

Any hyperlink whose `href` ends in `.md` must be rewritten to route through the markdown viewer using the full repo-relative path (from the repo root, no leading slash):

```
/docnav/view.html?file=<repo-relative-path-to-file.md>
```

The original markdown href may be a bare filename or a relative path. Resolve it against the location of the source `.md` file to produce the repo-relative path before inserting it into the `file=` parameter.

Examples (source file is `docnav/FAQ/tholonic-faq.md`):

| Original markdown link | Resolved repo-relative path | Rendered HTML href |
|---|---|---|
| `[Five Dimensions](five-dimensions-plain-labels.md)` | `docnav/FAQ/five-dimensions-plain-labels.md` | `/docnav/view.html?file=docnav/FAQ/five-dimensions-plain-labels.md` |
| `[Paper](../Research/papers/1_recursive-tholonic-five-constants.md)` | `docnav/Research/papers/1_recursive-tholonic-five-constants.md` | `/docnav/view.html?file=docnav/Research/papers/1_recursive-tholonic-five-constants.md` |

This rule applies to every `<a>` element produced during conversion, whether it comes from inline links `[text](href)`, reference-style links, or any other markdown link syntax. Do not apply this rule to anchors that start with `#` (same-page fragment links) or to links that already contain `view.html`.

---

## Checklist before writing the output file

- [ ] All `###` questions present as `.qa` cards with correct `id` slugs
- [ ] All `##` sections present in TOC sidebar
- [ ] N, D, C role colours applied inline throughout
- [ ] N-D-C context table has coloured column headers
- [ ] MathJax script tags present in `<head>`
- [ ] All `$$` formulas wrapped in `.math-block`
- [ ] IntersectionObserver script present before `</body>`
- [ ] Mobile breakpoint present at 900px
- [ ] No em-dashes anywhere in the output (project-wide rule)
- [ ] Footer references `docnav/FAQ/tholonic-faq.md` as source of truth
- [ ] All links to `.md` files rewritten to `/docnav/view.html?<original-href>`
- [ ] Fragment-only links (`#anchor`) and links already containing `view.html` are NOT rewritten
