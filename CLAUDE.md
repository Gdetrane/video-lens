# video-lens

## Workflow

> **Source of truth is always this repo.** Edit files here first — never in `~/.claude/skills/`. That is a deploy target, not a source.

After editing, sync to deployed location:
- `skills/video-lens/` or `template.html` → `task install-skill-local`
- `skills/video-lens-gallery/index.html` → `task build-index` (regenerates `~/Downloads/video-lens/index.html`)

## Install commands

```bash
task install-libraries          # installs Python dependencies (pip install -r requirements.txt)
task install-skill-local        # copies skills/ → ~/.claude/skills/
task build-index                # rebuilds gallery manifest
```

## Repo layout

```
video-lens/
  CLAUDE.md
  Taskfile.yml
  requirements.txt
  scripts/
    yt_template_dev.py     ← dev server helper
  skills/
    video-lens/
      SKILL.md             ← skill prompt (source of truth)
      template.html        ← HTML report template (source of truth)
      scripts/
        fetch_transcript.py
        fetch_metadata.py
        render_report.py
        serve_report.sh
    video-lens-gallery/
      SKILL.md             ← gallery skill prompt (source of truth)
      index.html           ← gallery viewer (source of truth)
      scripts/
        backfill_meta.py   ← backfills meta blocks into old reports
        build_index.py     ← builds manifest.json and copies index.html
```

## Dev

```bash
task dev   # renders template → ~/Downloads/sample_output.html, serves at http://localhost:8765/sample_output.html
```
