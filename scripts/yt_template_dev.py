#!/usr/bin/env python3
"""
Template dev server for youtube-summarizer.
Edit template.html, run this script, and see the result instantly.

Usage:
    python scripts/yt_template_dev.py
"""
import os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'skill', 'template.html')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'sample_output.html')

# ── Hardcoded content for https://www.youtube.com/watch?v=3Y1G9najGiI ──────
# AWS re:Invent 2025 — Werner Vogels final keynote

CONTENT = {
    "VIDEO_ID": "3Y1G9najGiI",

    "VIDEO_TITLE": "AWS re:Invent 2025 — Keynote with Dr. Werner Vogels",

    "VIDEO_URL": "https://www.youtube.com/watch?v=3Y1G9najGiI",

    "META_LINE": "AWS Events · 1h 16m · Dec 4 2025 · 13.8M views",

    "SUMMARY": (
        "Dr. Werner Vogels uses his final re:Invent keynote to confront the recurring fear "
        "that each new wave of abstraction will render developers obsolete, arguing that AI — "
        "like COBOL, OOP, and the cloud before it — elevates rather than eliminates. He frames "
        "the response around the <strong>Renaissance Developer</strong>: a builder who combines "
        "curiosity, systems thinking, precise communication, ownership, and polymath breadth to "
        "thrive alongside AI. Clare Liguori reinforces the communication thesis with a live "
        "demo of the <strong>Kiro IDE</strong>, showing how spec-driven development catches "
        "architectural surprises that vibe coding would have buried in generated code."
    ),

    "ANALYSIS": """
<p><strong>Werner opens with a cinematic time-travel sequence</strong> revisiting every era in which
developers were declared obsolete — from the introduction of COBOL in the 1960s through visual
programming, object orientation, and cloud infrastructure. Each prophecy failed for the same reason:
abstraction <em>&ldquo;liberated developers to operate at higher levels,&rdquo;</em> it never
replaced them. The historical survey lands squarely on today&rsquo;s AI-assisted workflows, and
Werner announces — with characteristic bluntness — that this is his last re:Invent keynote after
14 years, not because he is leaving Amazon but because <em>&ldquo;new voices from across AWS&rdquo;</em>
should take the stage. The farewell frames everything that follows as a legacy statement: a distilled
philosophy of what it means to build software when machines can write it for you.</p>

<p><strong>The centrepiece is the Renaissance Developer framework</strong>, named for the Florentine
polymaths who refused to draw lines between art, science, and engineering. Werner identifies five
qualities. <strong>Curiosity</strong> — stay intellectually hungry; failed builds teach more than
documentation, and the <strong>Yerkes-Dodson curve</strong> shows real learning happens on the rising
slope where curiosity meets pressure. He illustrates with extended travel stories: <strong>AJE</strong>
giving Amazon River communities an economic future, <strong>Rwanda&rsquo;s Health Intelligence
Centre</strong> using real-time data to place maternal clinics, and <strong>KOKO Networks</strong> in
Nairobi dispensing five cents of ethanol so families can cook without burning carbon.
<strong>Systems thinking</strong> arrives via Donella Meadows and the <strong>wolves of
Yellowstone</strong> — removing predators didn&rsquo;t create more life, it destabilised the entire
ecosystem, and reintroducing them changed even the course of rivers. The lesson for software:
<em>&ldquo;you can&rsquo;t change one part in isolation&rdquo;</em> because every service, cache, and
ownership boundary creates feedback loops that reshape the whole.</p>

<p><strong>Communication is where Werner hands the stage to Clare Liguori</strong>, who introduces
the <strong>Kiro IDE</strong> and its spec-driven development workflow. Where vibe coding asks a model
to guess intent from a short prompt — producing <em>&ldquo;a million possible outcomes, only one of
which matches what you had in mind&rdquo;</em> — spec-driven development front-loads that intent
into three artefacts: requirements, design, and task list. Clare walks through a production example:
building agent-completion notifications for Kiro itself. The spec process revealed that what appeared
to be a simple hook into agent code actually required a full notification subsystem built on
<strong>Electron&rsquo;s native API</strong> inside a 2-million-line codebase — complexity that vibe
coding would have silently generated and left for code review to discover. The team shipped the
feature in roughly half the time precisely because the spec surfaced architectural decisions before
a single line of code was written.</p>

<p><strong>Werner returns to name two structural risks of the AI era.</strong>
<strong>Verification debt</strong>: code arrives faster than humans can comprehend it, letting
software reach production before anyone truly understands what it does. <strong>Hallucination</strong>:
models invent plausible APIs and propose architecturally incoherent designs with full confidence.
His antidote is <strong>mechanisms, not good intentions</strong> — illustrated by Jeff Bezos
introducing Amazon&rsquo;s version of Toyota&rsquo;s <strong>Andon Cord</strong>. Everyone already
knew a drop-shipper was packaging tables badly; 70 % came back damaged. But nothing changed until
Bezos gave customer-service agents a button that made the product <em>&ldquo;unviable&rdquo;</em>,
forcing immediate resolution. Code reviews, S3&rsquo;s durability modelling (writing down every
imaginable threat before touching guarantees), and spec verification are all mechanisms — and they
become <em>more</em> important as generation accelerates. He closes with a call to become
<strong>T-shaped polymaths</strong>, citing his mentor <strong>Jim Gray</strong>, inventor of database
transactions and Turing Award winner, who once diagnosed a flawed database layout in 30 seconds
by listening to the sound of the disks. <em>&ldquo;Werner out.&rdquo;</em></p>
""",

    "KEY_POINTS": """
<li><strong>Every &ldquo;end of the developer&rdquo; prediction has been wrong.</strong> COBOL,
visual programming, OOP, and the cloud each raised the level of abstraction; none eliminated
builders. AI follows the same pattern — it elevates what developers can do, not who is needed.</li>

<li><strong>The Renaissance Developer framework</strong> distils five qualities for the AI era:
insatiable <strong>curiosity</strong>, learning by doing (not by reading), <strong>systems
thinking</strong> that traces second-order effects, precise <strong>communication</strong> that
reduces ambiguity for both humans and models, and <strong>ownership</strong> that refuses to
outsource accountability to a tool.</li>

<li><strong>Spec-driven development is the antidote to vibe coding&rsquo;s ambiguity.</strong>
The Kiro IDE generates structured requirements, design, and tasks <em>before</em> writing code,
letting developers iterate on intent rather than on misunderstood output — and caught an
architectural scope explosion that vibe coding would have silently shipped.</li>

<li><strong>Verification debt is the hidden cost of AI-generated code.</strong> When you write
code yourself, comprehension comes with the act of creation; when the machine writes it, you must
<em>&ldquo;rebuild that comprehension during review.&rdquo;</em></li>

<li><strong>Mechanisms beat good intentions every time.</strong> The Amazon Andon Cord story shows
that a known defect persisted until a formal mechanism — a button that made the product
unpurchaseable — forced resolution. Code reviews, durability modelling, and spec verification are
all mechanisms that matter more, not less, as AI accelerates output.</li>

<li><strong>Code reviews are the last checkpoint between AI output and production.</strong> In a
world where generation outpaces comprehension, human-to-human review is where judgment,
mentorship, and knowledge transfer converge — <em>&ldquo;the craft is still learned person to
person.&rdquo;</em></li>

<li><strong>&ldquo;The work is yours, not the tools.&rdquo;</strong> Regulatory liability, system
correctness, and architectural ownership remain with the developer regardless of what generated
the code. Werner frames this not as a burden but as the source of professional pride in
<em>&ldquo;the unseen systems that stay up through the night.&rdquo;</em></li>
""",

    "OUTLINE": """
<li data-t="0"><a class="ts" href="#" data-t="0">0:00</a> Opening cinematic &mdash; &ldquo;End of the Developer?&rdquo;</li>
<li data-t="396"><a class="ts" href="#" data-t="396">6:36</a> Werner announces his final re:Invent keynote after 14 years</li>
<li data-t="576"><a class="ts" href="#" data-t="576">9:36</a> History of developer evolution: assembly &rarr; COBOL &rarr; cloud &rarr; AI</li>
<li data-t="1141"><a class="ts" href="#" data-t="1141">19:01</a> The Renaissance Developer framework introduced</li>
<li data-t="1202"><a class="ts" href="#" data-t="1202">20:02</a> Quality 1 &mdash; Be Curious: Yerkes-Dodson, learning by doing, travel stories</li>
<li data-t="1981"><a class="ts" href="#" data-t="1981">33:01</a> Quality 2 &mdash; Think in Systems: Donella Meadows &amp; wolves of Yellowstone</li>
<li data-t="2285"><a class="ts" href="#" data-t="2285">38:05</a> Quality 3 &mdash; Communicate: specs reduce ambiguity, Apollo Guidance System</li>
<li data-t="2580"><a class="ts" href="#" data-t="2580">43:00</a> Clare Liguori: Kiro IDE &amp; spec-driven development</li>
<li data-t="2942"><a class="ts" href="#" data-t="2942">49:02</a> Spec-driven vs. vibe coding &mdash; agent notifications live demo</li>
<li data-t="3301"><a class="ts" href="#" data-t="3301">55:01</a> Quality 4 &mdash; Be an Owner: verification debt &amp; hallucination risks</li>
<li data-t="3601"><a class="ts" href="#" data-t="3601">1:00:01</a> Mechanisms vs. good intentions &mdash; the Andon Cord story</li>
<li data-t="3900"><a class="ts" href="#" data-t="3900">1:05:00</a> Quality 5 &mdash; Become a Polymath: Jim Gray &amp; T-shaped developers</li>
<li data-t="4260"><a class="ts" href="#" data-t="4260">1:11:00</a> Closing: pride in the unseen work &amp; &ldquo;Werner out&rdquo;</li>
""",
}
# ─────────────────────────────────────────────────────────────────────────────


def render():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    for key, value in CONTENT.items():
        html = html.replace("{{" + key + "}}", value)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Rendered → {OUTPUT_PATH}")


if __name__ == "__main__":
    render()
