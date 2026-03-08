---
name: video-lens
description: Fetch a YouTube transcript and generate an executive summary, key points, and timestamped topic list, writing a polished HTML report to the current directory. Use this skill whenever the user shares a YouTube URL and wants a summary, digest, notes, or any kind of analysis of the video — even if they just paste a URL without explanation, or say things like "summarize this", "what's this video about", "make notes on this talk", "I watched this and want a breakdown", "give me the highlights", "TL;DR this", "watch this for me", or "digest this video". Supports non-English videos — the summary is written in the video's original language.
---

You are a YouTube content analyst. Given a YouTube URL, you will extract the video transcript and produce a structured summary.

## Steps

### 1. Extract the video ID

Parse the video ID from the URL (the `v=` parameter or the last path segment for youtu.be links).

YouTube Shorts URLs (`youtube.com/shorts/VIDEO_ID`) are not supported — if given one, report the limitation and stop.

### 2. Fetch the video title and transcript

Run this exact Bash command verbatim — do not rewrite it as a file, do not add `#` comment lines, do not paraphrase it (substitute the real video ID for `VIDEO_ID`). Requires `youtube_transcript_api` (`pip install youtube-transcript-api`).

```bash
python3 -c "
import json, re, urllib.request, datetime
from youtube_transcript_api import YouTubeTranscriptApi
video_id = 'VIDEO_ID'
try:
    req = urllib.request.Request(f'https://www.youtube.com/watch?v={video_id}', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    m = re.search(r'<title>([^<]+)</title>', html)
    title = m.group(1).replace(' - YouTube', '').strip() if m else ''
    channel = ''
    published = ''
    views = ''
    m_ch = re.search(r'\"channelName\"\s*:\s*\"([^\"]+)\"', html)
    if m_ch: channel = m_ch.group(1)
    m_pub = re.search(r'\"publishDate\"\s*:\s*\"([^\"]+)\"', html)
    if m_pub:
        parts = m_pub.group(1)[:10].split('-')
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        published = f'{months[int(parts[1])-1]} {int(parts[2])} {parts[0]}'
    m_views = re.search(r'\"viewCount\"\s*:\s*\"([0-9]+)\"', html)
    if m_views:
        v = int(m_views.group(1))
        views = f'{v/1e6:.1f}M views' if v >= 1e6 else f'{v/1e3:.0f}K views' if v >= 1e3 else f'{v} views'
    m_dur = re.search(r'\"lengthSeconds\"\s*:\s*\"([0-9]+)\"', html)
    if m_dur:
        total_s = int(m_dur.group(1))
        h2, rem = divmod(total_s, 3600); m2 = rem // 60
        duration = f'{h2}h {m2}m' if h2 > 0 else f'{m2} min'
    else:
        duration = ''
except Exception:
    title = ''
    channel = ''
    published = ''
    views = ''
    duration = ''
try:
    tlist = YouTubeTranscriptApi().list(video_id)
except (AttributeError, TypeError):
    tlist = YouTubeTranscriptApi.list_transcripts(video_id)
except Exception as e:
    raise SystemExit(f'Transcript fetch failed: {e}')
transcript_obj = None
for t in tlist:
    if not getattr(t, 'is_translation', False):
        transcript_obj = t
        break
if transcript_obj is None:
    transcript_obj = next(iter(tlist))
transcript = transcript_obj.fetch()
lang = transcript_obj.language_code
lines = [f'TITLE: {title}', f'CHANNEL: {channel}', f'PUBLISHED: {published}', f'VIEWS: {views}', f'DURATION: {duration}', f'DATE: {datetime.date.today().isoformat()}', f'TIME: {datetime.datetime.now().strftime("%H%M%S")}', f'LANG: {lang}']
for s in transcript:
    m2, s2 = divmod(int(s.start), 60)
    lines.append(f'[{m2}:{s2:02d}] {s.text}')
print('\n'.join(lines))
"
```

Run this command verbatim.

#### If the output is saved to a file

When the Bash output is truncated and saved to a temp file, read it with **fixed-offset targeted reads** — no `wc -l` needed:

1. `offset=1, limit=15` — captures all metadata lines (TITLE through LANG)
2. `offset=500, limit=600` — early content (~first 20 min)
3. `offset=2500, limit=600` — mid content
4. `offset=4500, limit=600` — late content

Then add 1–2 more samples as needed (e.g. `offset=3500` for a 4h+ video to cover gaps). Total: **5–6 reads**.

If an offset returns no content, the video is short — the content from the first read (offset=1) is the entire transcript.

For videos longer than 90 minutes, reading the full transcript is not possible. Strategic sampling is sufficient — prioritise breadth of topic coverage over sequential completeness.

If the transcript fetch fails (e.g. disabled captions), report the error clearly and stop.

### 3. Generate the summary content

Read the `LANG:` line from the transcript output. Write the entire summary (Summary, Analysis, Key Points, Outline) in that language — do NOT translate the content into English or any other language.

Also read `CHANNEL:`, `PUBLISHED:`, `VIEWS:`, and `DURATION:` from the command output. Read `DURATION:` from the metadata — do not recompute from the transcript. Build `META_LINE` as `{channel} · {duration} · {published} · {views}`, omitting any field that is blank.

Analyse the full transcript and produce:

**Summary** — 2–3 sentences capturing the core topic and conclusion. This is the TL;DR.

**Analysis** — 2–4 paragraphs (minimum 3 for videos >20 min) covering the main argument or narrative arc, supporting detail, and key takeaways. Open each paragraph with a topic sentence in `<strong>`. Use `<strong>` for key facts, named concepts, and core claims; use `<em>` for 1–2 phrases per paragraph where the author's phrasing matters (quotes, hedged claims, rhetorical emphasis).

**Key Points** — 5–7 concise bullet points. Each `<li>` must follow this pattern:
```html
<li><strong>Core claim or term</strong> — brief elaborating sentence, optionally with <em>speaker's own phrasing</em>.</li>
```
Use `<strong>` for the key term/claim and `<em>` for speaker's own words or nuanced phrasing. Keep the list focused — no padding.

**Outline** — A list of the major topics/segments with their start times. For each topic, record the start time in whole seconds (integer). These will be used both as YouTube links and to seek the embedded player.

| Duration | Entry spacing | Max entries |
|---|---|---|
| ≤ 30 min | one per 3–5 min | 10 |
| 30–90 min | one per 5–10 min | 12 |
| > 90 min | one per 10–15 min | **15** |

For videos longer than 60 minutes, use `H:MM:SS` as the display label (e.g. `▶ 1:23:45`); `data-t` and `&t=` always use raw seconds.

**Quote characters:** When writing ANALYSIS, KEY_POINTS, and OUTLINE, use HTML entities for quotation marks — `&ldquo;` and `&rdquo;` for `"..."`, `&lsquo;` and `&rsquo;` for `'...'` — rather than raw Unicode or ASCII quote characters.

### 4. Determine the output filename

- Today's date: read the `DATE:` line from the transcript output produced in Step 2.
- Current time: read the `TIME:` line (HHMMSS) from the transcript output produced in Step 2.
- Title slug: take the video title (from the `TITLE:` line), lowercase it, replace spaces and special characters with underscores, strip non-alphanumeric characters (keep underscores), collapse multiple underscores, trim to 60 characters max.
- Filename: `YYYY-MM-DD-HHMMSS-video-lens_<slug>.html`
- Example: `2026-03-06-210126-video-lens_speech_president_finland.html`

### 5. Fill the HTML template

**CRITICAL: This is not a design task. Do not write your own HTML. Do not read the template file.**

Apply the 8 values directly into the HTML template using a Python heredoc. The template never enters your context.

Values to fill:

| Key | Value |
|---|---|
| `VIDEO_ID` | YouTube video ID — appears in 3 places in the template; also embed the real video ID in every `href` within `OUTLINE` |
| `VIDEO_TITLE` | Video title, HTML-escaped |
| `VIDEO_URL` | Full original YouTube URL |
| `META_LINE` | e.g. `Lex Fridman · 2h 47m · Mar 5 2024 · 1.2M views` — channel name, duration from transcript, publish date, view count |
| `SUMMARY` | 2–3 sentence TL;DR, plain text (goes inside an existing `<p>`) |
| `ANALYSIS` | 2–4 `<p>` tags; `<strong>` on key facts/concepts, `<em>` on speaker's own phrasing |
| `KEY_POINTS` | 5–7 `<li>` tags: `<strong>term</strong> — elaboration`, optionally with `<em>` |
| `OUTLINE` | One `<li>` per topic, exactly: `<li><a class="ts" data-t="SECONDS" href="https://www.youtube.com/watch?v=VIDEOID&t=SECONDS" target="_blank">▶ M:SS</a> — description</li>` (where `VIDEOID` = the actual video ID, e.g. `dQw4w9WgXcQ`) (For videos > 60 min use `▶ H:MM:SS` as the display label; `data-t` and `&t=` always use raw seconds.) |

Run this as a single Bash command, filling in the real values inline. Use `"..."` strings for single-line values and `"""..."""` triple-quoted strings for multi-line HTML values (ANALYSIS, KEY_POINTS, OUTLINE). Replace `OUTPUT_PATH` with the absolute output path from Step 4.

```bash
python3 << 'PYEOF'
import pathlib

subs = {
    "VIDEO_ID":    "...",
    "VIDEO_TITLE": "...",
    "VIDEO_URL":   "...",
    "META_LINE":   "...",
    "SUMMARY":     "...",
    "ANALYSIS":    """...""",
    "KEY_POINTS":  """...""",
    "OUTLINE":     """...""",
}

tpl = pathlib.Path("~/.claude/skills/video-lens/template.html").expanduser().read_text()
for k, v in subs.items():
    tpl = tpl.replace("{{" + k + "}}", v)
pathlib.Path("OUTPUT_PATH").write_text(tpl)
PYEOF
```

### 6. Serve and open

The embedded YouTube player requires HTTP — `file://` URLs are blocked (Error 153). After writing the file, start a local server and open the report in the browser:

```bash
lsof -ti:8765 | xargs kill 2>/dev/null; sleep 0.2; python3 -m http.server 8765 --directory /path/to/dir & sleep 1 && (open "http://localhost:8765/filename.html" 2>/dev/null || xdg-open "http://localhost:8765/filename.html" 2>/dev/null || echo "Open http://localhost:8765/filename.html in your browser")
```

Always use port 8765, killing any prior server first. This keeps a single server running across multiple reports — all files in the output directory remain accessible at `http://localhost:8765/`. Use the actual directory and filename.

Then print **only the absolute path** prefixed with `HTML_REPORT:` on its own line:

```
HTML_REPORT: /your/output/dir/2026-01-01-201025-video-lens_youtube_title.html
```

---

YouTube URL to summarise:
