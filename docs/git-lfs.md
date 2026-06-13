# Git LFS

Large project binaries (archives and slide decks under `frontend/project/`) are stored with [Git LFS](https://git-lfs.github.com) so pushes stay within GitHub file size limits.

## Tracked patterns

| Pattern | Typical use |
|---------|-------------|
| `*.zip` | DD2022 document bundles |
| `*.ppsx` | PowerPoint slide shows |
| `*.pptx` | PowerPoint presentations |

See `.gitattributes` for the authoritative list.

## One-time setup (new clone or new machine)

```bash
# Install the client (Manjaro/Arch)
sudo pacman -S git-lfs

# Register hooks for your user account (once per machine)
git lfs install

# Clone, or after clone:
git lfs pull
```

## Adding a new large binary

If the file matches a tracked pattern, add it normally:

```bash
git add path/to/file.zip
git commit -m "add DD2022 archive"
git push
```

Git LFS uploads the blob to LFS storage; the git commit holds only a small pointer file.

## GitHub

LFS bandwidth and storage quotas apply on GitHub free and paid plans. See [GitHub LFS docs](https://docs.github.com/en/repositories/working-with-files/managing-large-files).

## Not in LFS

These stay out of git entirely (see `.gitignore`):

- Hugging Face model caches under `frontend/project/tholonic_ai/phi_ratio_measurement/.cache/`
- Python virtualenvs (`**/.venv/`)
