# video-lens

**Turn any YouTube video into a polished research report.**

video-lens is a [Claude Code](https://claude.ai/code) skill that fetches a YouTube transcript and generates a structured HTML report — executive summary, key points, timestamped topic outline, and an embedded in-page player. No API keys, no external services beyond Claude itself.

<img src="docs/video-lens-example.png" alt="video-lens example report" width="700">

---

## What you get

- **Executive summary** — the 3-5 sentence version of the whole video
- **Key takeaways** — bulleted, scannable insights
- **Timestamped outline** — click any topic to jump straight to that moment in the player
- **In-page YouTube player** — watch while reading, keyboard shortcuts included
- **Markdown export** — copy the full report as Markdown in one click
- **Dark mode** — auto-detects system preference

---

## Requirements

| Tool | Purpose |
|------|---------|
| [Claude Code](https://claude.ai/code) | Runs the skill |
| Python 3 | Fetches the transcript |
| [Task](https://taskfile.dev) | Install / dev commands (`brew install go-task` or [download](https://taskfile.dev/installation/)) |
| **Optional:** [Raycast](https://www.raycast.com) | Trigger from anywhere via hotkey |
| **Optional:** [iTerm2](https://iterm2.com) or Terminal.app | Used by the Raycast script |

> **Note:** video-lens only works for videos that have captions/subtitles available. Videos with captions disabled will produce an error.

---

## Install

### 1. Clone and install Python dependency

```bash
git clone https://github.com/kar2phi/video-lens.git
cd video-lens
pip install -r requirements.txt
```

### 2. Install the Claude Code skill

```bash
task install-skill
```

This copies `skill/SKILL.md` and `skill/template.html` into `~/.claude/skills/video-lens/`.

### 3. (Optional) Install the Raycast script

> **macOS only.** The Raycast script uses AppleScript, `pbpaste`, and iTerm2/Terminal.app — none of which are available on Windows or Linux.

```bash
task install-raycast
```

Requires Raycast. The script opens a new iTerm2 tab (or Terminal.app if iTerm2 isn't installed), launches Claude with the required permissions, and runs the skill.

---

## Usage

### In Claude Code

```
/video-lens https://www.youtube.com/watch?v=...
```

Claude fetches the transcript, generates the report, and opens it in your browser at `http://localhost:8765/`.

### Via Raycast

Invoke the **video-lens** command, paste a YouTube URL (or leave blank to use the clipboard), and choose a model (default: Sonnet). The report opens automatically in your browser.

Reports are saved to `~/Downloads/`.

---

## Dev server

To iterate on `skill/template.html` without running a real video:

```bash
task dev
```

Opens a rendered sample report at `http://localhost:8765/sample_output.html`.

---

## Repo layout

```
video-lens/
  skill/
    SKILL.md          ← Claude skill prompt (source of truth)
    template.html     ← HTML report template (source of truth)
  scripts/
    raycast-video-lens.sh ← Raycast script (source of truth)
    yt_template_dev.py← Dev server helper
  Taskfile.yml
  requirements.txt
```

**Always edit files in this repo, then deploy with `task install-skill` or `task install-raycast`.** Never edit directly in `~/.claude/skills/` or `~/.raycast/scripts/`.

---

## Contributing

PRs welcome. Keep the skill prompt in `skill/SKILL.md` and the HTML template in `skill/template.html` — those are the sources of truth.

## License

MIT
