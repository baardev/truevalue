# Canonical vault + TMSU tags + alternate symlink hierarchies

This document describes an end‑to‑end pattern we set up locally: **one canonical directory of real files**, **tags in TMSU**, and **one or more “view” directories** built from symlinks into the canonical vault. Copy or adapt these steps for another application where the same assets must appear under different filesystem trees (e.g. by kind, then by tag such as color).

**Portability:** Example paths use **`/home/jw`**; substitute your repo root or **`$VAULT_ROOT`**. TMSU metadata lives under **`vault/.tmsu/`**—copy it with the vault if you want to preserve tags unchanged; otherwise **`tmsu init .`** plus re‑tagging rebuilds metadata.

---

## 1. Design goals

| Concern | Approach |
|---------|----------|
| Single source of truth for file bytes | Regular files live only under **`vault/`** (canonical). |
| Rich metadata without duplicating data | **[TMSU](https://tmsu.org/)** attaches tags (and optional `tag=value`) to paths. |
| Alternate navigation (Explorer / shell / scripts) | A **peer directory** (`vault-x/`, etc.) exposes **directories + symlinks** whose targets are canonical paths. |
| Idempotent regeneration | Scripts can **`rm -rf`** a view root and recreate symlinks from metadata when needed. |

**Important behaviours**

- Editing a file reached through **`vault-x/…`** modifies the single file under **`vault/…`** (same inode target).
- Removing a **symlink** in `vault-x` does **not** delete the canonical file; removing the **canonical file** removes the data (broken symlinks remain until cleaned up).

---

## 2. Canonical vault layout (`~/vault`)

On this machine:

- Root: **`/home/jw/vault`**
- Immediate subdirectories (taxonomy used for testing):
  - **`plants/`** — `tree.md`, `rose.md`, `fern.md`
  - **`animals/`** — `dog.md`, `cat.md`, `hawk.md`
  - **`insects/`** — `bee.md`, `ant.md`, `beetle.md`, `butterfly.md`

Each `.md` file is trivial placeholder content (title + line of text).

**Application analogue:** Replace `plants/animals/insects` with your domain namespaces (projects, tenants, ingest batches, etc.); TMSU holds cross‑cutting facts (priority, phase, ownership, palette, …).

---

## 3. TMSU database location and tagging

### 3.1 Initialize TMSU in the canonical vault

```bash
cd /path/to/vault
tmsu init .
```

This creates **`.tmsu/`** under the vault directory. Subsequent `tmsu` commands **from any path under `vault/`** use that DB automatically unless you override **`TMSU_DB`** / **`--database`**.

### 3.2 Tag schema used in the demo

- **Kingdom / category:** free tags **`plants`**, **`animals`**, **`insects`** (aligned with subdirectory names).
- **Color:** tag **`color`** with **values**, e.g. `color=green`, `color=red`.

Applied assignments (canonical path → TMSU associations):

| Canonical path | Tags |
|----------------|------|
| `plants/tree.md` | `plants` `color=green` |
| `plants/rose.md` | `plants` `color=red` |
| `plants/fern.md` | `plants` `color=green` |
| `animals/dog.md` | `animals` `color=brown` |
| `animals/cat.md` | `animals` `color=orange` |
| `animals/hawk.md` | `animals` `color=brown` |
| `insects/bee.md` | `insects` `color=yellow` |
| `insects/ant.md` | `insects` `color=black` |
| `insects/beetle.md` | `insects` `color=green` |
| `insects/butterfly.md` | `insects` `color=blue` |

### 3.3 Example `tmsu tag` commands (pattern)

```bash
cd /path/to/vault

tmsu tag plants/tree.md plants color=green
tmsu tag animals/dog.md animals color=brown
# … repeat per file …
```

### 3.4 Inspecting tags: one file, a whole subtree, or the whole database

Run these from anywhere under **`vault/`** (so the correct **`.tmsu`** DB is used), or pass **`-D /path/to/vault/.tmsu`** (or set **`TMSU_DB`**) when your shell’s cwd is elsewhere.

#### Tags on specific path(s)

```bash
cd /path/to/vault

tmsu tags plants/tree.md
tmsu tags a.md b.md    # multiple paths; prints one line per file
```

Common options (see **`tmsu help tags`**):

- **`tmsu tags -e PATH`** (`--explicit`) — hide tags that appear only via **implications** (`tmsu imply`).
- **`tmsu tags -u`** (`--value`) — emphasize **`tag=value`** style associations.
- **`tmsu tags -P PATH`** (`--no-dereference`) — for a **symlink**, show tags on the symlink path itself instead of following it to the target. Useful when browsing **`vault-x/`** symlinks vs canonical **`vault/`** paths.

#### All tag *names* in the database (global vocabulary)

With **no path** argument, **`tmsu tags`** lists every **tag name** known in that database — names only, not values. This is the global vocabulary of all tags ever applied to any file in the DB. To also see the **values** used with a valued tag:

```bash
tmsu values color
tmsu values            # all values (can be noisy)
```

#### Which files under a directory (“branch”) are tagged, and their tags

TMSU stores tags on **individual paths**. A directory like **`plants/`** may show as **untagged** even when every file inside is tagged (tag the directory too if you want it in the DB).

List every **tagged file** whose path is under a prefix:

```bash
tmsu files --path="./plants"
```

Then show tags for each (under large trees, **`xargs`** avoids one process per file):

```bash
tmsu files --path="./plants" -0 | xargs -0 tmsu tags
```

Alternative: walk the tree on disk:

```bash
find ./plants -type f -exec tmsu tags {} +
```

To **union** distinct tag names used under a branch, post-process the output of **`tmsu tags`** (e.g. `awk`, `sort -u`), or query from TMSU’s SQLite if you need SQL.

#### Quick health / coverage for a subtree (not full tag dump)

Shows whether paths are tagged (**`T`**), modified vs DB (**`M`**), missing (**`!`**), or never tagged (**`U`**):

```bash
tmsu status ./plants
```

Add **`-d`** (`--directory`) to stop TMSU from recursing into subdirectories. Run **`tmsu help status`** for the full option list.

#### Queries by tag (anywhere in the DB)

**`tmsu files`** accepts boolean queries. Operators: `and`, `or`, `not`, `==`, `!=`, `<`, `>` (and SQL-style aliases `eq`, `ne`, `lt`, `gt`).

```bash
tmsu files plants
tmsu files color=green
tmsu files "plants and color=green"
tmsu files "plants or animals"
tmsu files "not insects"
tmsu files "color == green"          # same as color=green for equality
```

### 3.5 TMSU installation note (Linux / Arch family)

`tmsu` was not initially on `$PATH`; it was installed from the **AUR** package **`tmsu-bin`** (binary release). Install method on your target environment may differ (distro package, upstream tarball, etc.).

---

## 4. View hierarchy: peer folder `~/vault-x` (color‑based)

### 4.1 Purpose

Expose the **same 10 files** sorted by **`color`** instead of **`plants | animals | insects`**, **without copying** binary content.

### 4.2 Location

- **`/home/jw/vault-x`** — **sibling** of **`/home/jw/vault`** (same parent prefix `~/`).
- Logical root inside: **`vault-x/by-color/<color>/<basename>.md`**

### 4.3 Symlink map (targets are absolute paths)

Symlinks must point at **`/home/jw/vault/...`** so they survive `cd` and relative confusion.

```
/home/jw/vault-x/by-color/black/ant.md
  → /home/jw/vault/insects/ant.md

/home/jw/vault-x/by-color/blue/butterfly.md
  → /home/jw/vault/insects/butterfly.md

/home/jw/vault-x/by-color/brown/dog.md
  → /home/jw/vault/animals/dog.md

/home/jw/vault-x/by-color/brown/hawk.md
  → /home/jw/vault/animals/hawk.md

/home/jw/vault-x/by-color/green/tree.md
  → /home/jw/vault/plants/tree.md

/home/jw/vault-x/by-color/green/fern.md
  → /home/jw/vault/plants/fern.md

/home/jw/vault-x/by-color/green/beetle.md
  → /home/jw/vault/insects/beetle.md

/home/jw/vault-x/by-color/orange/cat.md
  → /home/jw/vault/animals/cat.md

/home/jw/vault-x/by-color/red/rose.md
  → /home/jw/vault/plants/rose.md

/home/jw/vault-x/by-color/yellow/bee.md
  → /home/jw/vault/insects/bee.md
```

### 4.4 How it was built (conceptual commands)

Pattern: create color directories once, then **`ln -sfn TARGET LINK_PATH`** (`-f` overwrites stale links).

```bash
VX=/home/jw/vault-x
BASE="$VX/by-color"
V=/home/jw/vault

mkdir -p "$BASE/black" "$BASE/blue" "$BASE/brown" "$BASE/green" \
         "$BASE/orange" "$BASE/red" "$BASE/yellow"

ln -sfn "$V/insects/ant.md"         "$BASE/black/ant.md"
# … repeat for each row …
```

In a real automation (a shell script, Python, Make, etc.), iterate over tagged files, read the **`color=…`** (or other dimension) value for each, derive the correct `LINK_PATH`, and create the symlink — either with `ln -sfn` in shell or the equivalent in your chosen language.

---

## 5. Recreating elsewhere (checklist)

1. **Canonical tree** — Create your **`vault`** root and subdirectory policy; drop real payloads there only.
2. **TMSU database** — **`tmsu init .`** inside **`vault`** (or copy the existing **`vault/.tmsu/`** directory with the vault). TMSU stores **absolute paths** in a SQLite file; after moving the vault to a new location run **`tmsu repair`** to update stale paths in the DB.
3. **Tagging policy** — Document tag names (`color`, domain tags, statuses). Prefer predictable naming for scripted views.
4. **View roots** — For each hierarchy (by color, by status, …), pick a **`vault-<viewname>/`** sibling (or `./views/by-color/` under repo). Symlink views duplicate **paths**, not TMSU rows: tags normally attach to canonical files under **`vault/`** (`tmsu tags -P` inspects symlink entries when needed).
5. **Symlinks**
   - Use **absolute** targets pointing into **`vault`** unless you deliberately want portability caveats with relative targets.
   - Handle **basename collisions** in one bucket (`green/a.md`, `green/b/a.md`), or prefixed names (`green/plants-tree.md`).
6. **Regeneration script** — Version control the **YAML/JSON/TOML schema** describing each projection; CI or pre-commit regenerates symlink trees idempotently.
7. **Backups / moves** — If `vault-x` crosses filesystems relative to `vault`, **`ln`** cannot produce hard links across devices; symlinks remain the right abstraction.

---

## 6. Out of scope here (possible next steps)

- **TMSU FUSE mounts** (`tmsu … mount`) — another way to browse by tag without maintaining explicit symlink dirs.
- **Tag implications** (`tmsu imply`) — automatic inheritance rules between tags.
- **Watch mode** — inotify/regenerate views when TMSU tags or filenames change.

---

## 7. Path summary (this machine)

| Path | Role |
|------|------|
| **`/home/jw/vault`** | Canonical payload + `.tmsu` DB |
| **`/home/jw/vault/plants`** … **`insects`** | Organizational subfolders |
| **`/home/jw/vault-x/by-color`** | Color‑sorted symlink projection |

Rename **`vault-x`** to match your naming (`staging-views`, `projections`, etc.). The pattern stays the same: **canonical + tags + deterministic symlink synthesis**.
