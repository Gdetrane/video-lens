# video-lens Linux Adaptation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Adapt video-lens for Linux/Claude-Code-only use with security and code quality improvements.

**Architecture:** Targeted in-place edits to strip macOS specifics, simplify agent discovery to Claude-only, harden security (noreferrer, PID-file server), and make yt-dlp a hard requirement.

**Tech Stack:** Python 3, Bash, HTML/CSS/JS (vanilla)

---

### Task 1: Security — Add noreferrer to all external links

**Files:**
- Modify: `skills/video-lens/scripts/fetch_metadata.py:15` (_linkify function)
- Modify: `skills/video-lens/template.html:986` (meta-line YouTube link)
- Modify: `skills/video-lens-gallery/index.html:555,926,1017` (help link, list title, card title)

**Step 1:** In `fetch_metadata.py`, change `rel="noopener"` to `rel="noopener noreferrer"` in the `_linkify()` function.

**Step 2:** In `template.html`, add `rel="noopener noreferrer"` to the "Open on YouTube" link in the meta-line.

**Step 3:** In `index.html`, add `noreferrer` to all link `rel` attributes (help modal link, list-title links, card-title links).

**Step 4:** Run: `pytest tests/test_e2e.py -v -m "not slow"` — verify template tests still pass.

**Step 5:** Commit: `git commit -am "security: add noreferrer to all external links"`

---

### Task 2: Security — PID-file server management

**Files:**
- Modify: `skills/video-lens/scripts/serve_report.sh`

**Step 1:** Replace `lsof -ti:PORT | xargs kill` with PID-file approach using `~/.cache/video-lens/server.pid`. Prioritize `xdg-open` over `open`.

**Step 2:** Run: `pytest tests/test_e2e.py::test_render_and_serve -v` — verify serve still works.

**Step 3:** Commit: `git commit -am "security: use PID-file instead of lsof port scan"`

---

### Task 3: Platform — Delete Raycast, simplify Taskfile

**Files:**
- Delete: `scripts/raycast-video-lens.sh`
- Modify: `Taskfile.yml` (remove install-raycast task)

**Step 1:** Delete `scripts/raycast-video-lens.sh`.

**Step 2:** Remove the `install-raycast` task from `Taskfile.yml`.

**Step 3:** Commit: `git commit -am "platform: remove macOS-only Raycast script and task"`

---

### Task 4: Platform — Simplify agent discovery to Claude-only

**Files:**
- Modify: `skills/video-lens/SKILL.md` (5 bash command blocks)
- Modify: `skills/video-lens-gallery/SKILL.md` (discovery block)

**Step 1:** Replace all `_sd=$(for d in ~/.agents ~/.claude ...` patterns in SKILL.md with direct `$HOME/.claude/skills/video-lens/scripts` lookup.

**Step 2:** Same for gallery SKILL.md — both `_sd` and `_gd` patterns.

**Step 3:** Remove `brew install yt-dlp` reference in SKILL.md error handling table; use `pip install yt-dlp`.

**Step 4:** Commit: `git commit -am "platform: simplify agent discovery to Claude-only"`

---

### Task 5: Code quality — Make yt-dlp required, fix version pin

**Files:**
- Modify: `skills/video-lens/scripts/fetch_metadata.py` (exit code on missing yt-dlp)
- Modify: `skills/video-lens/SKILL.md` (Step 2b framing, error table)
- Modify: `requirements.txt`

**Step 1:** In `fetch_metadata.py`, change `sys.exit(0)` to `sys.exit(1)` for FileNotFoundError (yt-dlp missing).

**Step 2:** In SKILL.md, update Step 2b intro and error table to reflect yt-dlp as required.

**Step 3:** Fix `requirements.txt`: pin `yt-dlp>=2026.3.17`.

**Step 4:** Commit: `git commit -am "quality: make yt-dlp a hard requirement"`

---

### Task 6: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1:** Simplify for single-agent (Claude) workflow. Remove multi-agent install references.

**Step 2:** Commit: `git commit -am "docs: simplify CLAUDE.md for Claude-only workflow"`

---

### Task 7: Verify all tests pass

**Step 1:** `pip install 'youtube-transcript-api>=0.6.3'` if not already installed.

**Step 2:** Run: `pytest tests/test_e2e.py -v -m "not slow"`

**Step 3:** Verify all pass.
