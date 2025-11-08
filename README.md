# PyO3Lab Docs

Static site powered by MkDocs + Material theming.

## Getting started

```powershell
# Install/refresh dependencies in .venv (required if pyproject changed)
uv sync

# Run the live-reload dev server
uv run mkdocs serve

# Build the production site
uv run mkdocs build
```

> If `mkdocs serve` complains that a plugin such as `macros` is missing, it means
> your local `.venv` is out of date. Re-run `uv sync` after pulling new changes.

## Managing the project list

Active/Planned/Completed tables on `Projects` are generated from `projects.json`.

1. Edit `projects.json` and add/update entries. Valid `status` values:
   - `on_plan`
   - `on_developing`
   - `done`
2. Each entry supports localized descriptions under `desc.en` and `desc.zh`.
3. Run `uv run mkdocs serve` or `uv run mkdocs build` to see the updated tables in both languages automatically.

The Markdown files (`docs/projects*.md`) render using Jinja templates at build time—no manual edits required once the JSON is updated.
