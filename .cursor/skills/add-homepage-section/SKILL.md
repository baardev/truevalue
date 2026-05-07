---
name: add-homepage-section
description: Add a new section or content entry to the TrueValue Analytics homepage (index.html). Use when the user asks to add a hub section, a project card, a papers entry, or any new navigable block to the homepage. Handles both project cards (site-index.json projects array + homepage-layout.json categories) and hub sections (new key in site-index.json + HTML + JS in index.html). Prompts for category name if needed.
---

# Add a Section to the TrueValue Analytics Homepage

There are two distinct addition types. Determine which applies before acting.

## Type A: New project card

A project card appears in the top grid, grouped by category.

**Files:**
- `frontend/site-index.json` — `projects` array (card data)
- `frontend/homepage-layout.json` — `categories` array (which grid section it goes in)

**Steps:**

1. Read `frontend/site-index.json` and `frontend/homepage-layout.json`.
2. Add the project object to `site-index.json > projects`:
   ```json
   {
     "id": "<slug>",
     "title": "...",
     "icon": "...",
     "accent": "#rrggbb",
     "hub": "/frontend/project/<slug>/index.html",
     "desc": "...",
     "tag": "..."
   }
   ```
3. Assign the `id` to a category in `homepage-layout.json > categories[].project_ids`.
   - If no suitable category exists, ask the user what the category should be called, then add it:
     ```json
     {
       "id": "<cat-slug>",
       "label": "Category Name",
       "icon": "...",
       "desc": "...",
       "project_ids": ["<slug>"]
     }
     ```
4. Validate both JSON files: `python3 -m json.tool frontend/site-index.json > /dev/null && python3 -m json.tool frontend/homepage-layout.json > /dev/null`.
5. No HTML changes needed for Type A. The homepage JS renders from the JSON files at runtime.

---

## Type B: New hub section (PDI, Papers, PCI, Twistors, etc.)

A hub section appears below the project grid as a labeled row of rich cards.

**Files:**
- `frontend/site-index.json` — new top-level key with `sections > items`
- `index.html` — CSS, HTML placeholder, JS render block, JS error handler

**Steps:**

### 1. Add items to `site-index.json`

Append a new top-level key (e.g. `"papers"`) **before the closing `}`**:

```json
"<key>": {
  "sections": [
    {
      "title": "Section display title",
      "items": [
        {
          "id": "<unique-id>",
          "icon": "...",
          "title": "Card title",
          "desc": "Short description.",
          "tags": [
            { "label": "Tag", "cls": "paper" }
          ],
          "links": [
            { "label": "Read", "url": "/docnav/view.html?file=<relative-path>.md" }
          ]
        }
      ]
    }
  ]
}
```

Tag `cls` values available: `theory`, `paper`, `data`, `finance`, `ndc`, `investor`, `analysis`, `strategy`, `brief`, `tvpci`, `math`, `core`, `explainer`, `example`.

For DocNav Markdown links use: `/docnav/view.html?file=<path-relative-to-docnav-root>.md`

### 2. Add `#hub-<key>` to the CSS in `index.html`

Find the CSS block listing hub IDs and add `#hub-<key>` to both rules:

```css
/* width rule */
#hub-pdi,
...
#hub-<key>,
#hub-additional { width: 100%; max-width: none; }

/* margin rule */
#hub-pdi,
...
#hub-<key>,
#hub-additional { margin-bottom: 8px; }
```

### 3. Add the HTML placeholder in `index.html`

Insert before the `<!-- ── Phase Mapping -->` comment (or at a logical position in the section order):

```html
<!-- ── <Label> ───────────────────────────────────────────────── -->
<div class="row-label" style="margin-top:48px;"><Label></div>
<div id="hub-<key>">
<p style="color:#6b7280;padding:8px 0;">Loading…</p>
</div>
```

### 4. Add the JS render block in `index.html`

Inside the `.then(function(results){...})` callback, after the game theory block and before the "additional" block:

```js
/* Render <Label> */
var hub<Camel> = document.getElementById('hub-<key>');
if (hub<Camel>) {
  var <key>Items = collectAdditionalItems(siteData, ['<key>']);
  if (!<key>Items.length) {
    hub<Camel>.innerHTML = '<p style="color:#6b7280;padding:8px 0;">No <label> entries. Edit frontend/site-index.json (<key>).</p>';
  } else {
    hub<Camel>.innerHTML = '<div class="grid">' + <key>Items.map(renderHubItem).join('') + '</div>';
  }
}
```

### 5. Add the JS error handler entry

Inside the `.catch(function(err){...})` block, after the game theory error line and before the hub-additional line:

```js
var hub<Camel> = document.getElementById('hub-<key>');
if (hub<Camel>) hub<Camel>.innerHTML = '<p style="color:#f87171;padding:8px 0;">Could not load site index: ' + msg + '</p>';
```

### 6. Validate and finish

```bash
python3 -m json.tool frontend/site-index.json > /dev/null && echo OK
```

Update the `?v=` cache-bust timestamp on the `SITE_INDEX` variable in `index.html` to today's date (format: `YYYYMMDD`).

Also note the addition in `tree.md` root line if it is a new permanent section.

---

## Key file locations

| File | Purpose |
|------|---------|
| `index.html` | Homepage HTML, CSS, and JS renderer |
| `frontend/site-index.json` | All card/section data (single source of truth) |
| `frontend/homepage-layout.json` | Project card category grouping |
| `docnav/view.html` | Markdown viewer; links use `?file=<path>` relative to docnav root |

## When to ask the user

- If the target category for a project card does not exist in `homepage-layout.json`, ask what the category should be called and what icon/description it should have.
- If the new hub section key might clash with an existing key in `site-index.json`, confirm the key name before writing.
- If the content to link is not under `docnav/`, ask for the correct URL.
