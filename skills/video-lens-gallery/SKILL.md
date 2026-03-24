---
name: video-lens-gallery
description: Open or rebuild the video-lens gallery index. Triggers on "show my gallery", "open video library", "rebuild the index", "browse saved videos", "build gallery", "show video-lens index", "backfill metadata", "update index".
license: MIT
allowed-tools: Bash
---

# video-lens-gallery

Manage and browse your saved video-lens reports.

## Step 1 — Locate skill scripts

```bash
_sd="$HOME/.claude/skills/video-lens/scripts"
_gd="$HOME/.claude/skills/video-lens-gallery/scripts"
```

If `$_sd` does not exist, exit with:

> `video-lens skill not found — copy video-lens to ~/.claude/skills/video-lens/`

## Step 2 — Backfill metadata (only if requested)

If the user's request mentions "backfill" or "update metadata", run:

```bash
python3 "$_gd/backfill_meta.py" --dir ~/Downloads/video-lens
```

## Step 3 — Rebuild index

```bash
python3 "$_gd/build_index.py" --dir ~/Downloads/video-lens
```

## Step 4 — Serve gallery

```bash
bash "$_sd/serve_report.sh" ~/Downloads/video-lens/index.html
```
