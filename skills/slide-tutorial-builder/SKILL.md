---
name: slide-tutorial-builder
description: "Turn a numbered set of slide-deck URLs (e.g. a Slidev deck at https://example.vercel.app/1 through /N) into a written tutorial with Mermaid diagrams. Trigger this skill whenever the user gives a base URL plus a slide-number range (e.g. 'slides 1 to 45', '/1 through /47'), asks to read/summarize/extract content from an online slide deck by number, or asks to build a tutorial/study-guide/markdown-file/notes from a presentation site. Also trigger if the user references a previously-fetched slide deck and asks for a tutorial, write-up, or diagrams based on it. Use this skill even if the user does not say the word 'skill' or 'slides' explicitly — phrases like 'go through these links and summarize them', 'make notes from this deck', or a bare list of sequential numbered URLs are enough to trigger it."
---

# Slide Tutorial Builder

Converts a sequential set of slide-deck URLs into a structured Markdown tutorial with Mermaid diagrams. Built from a real session where a 47-slide Slidev deck ("Voice AI Agent" bootcamp) was fetched via Claude in Chrome and converted into a tutorial doc.

## When this applies

- The person gives a base URL and a numeric slide range, e.g. `https://foo.vercel.app/1` through `/45`.
- Common with **Slidev** decks (`meta-slidev:version` in page source) and similar single-page-app presentation tools, but the workflow generalizes to any site with sequential numbered pages.
- The person wants the *content* turned into a tutorial, notes, or study guide — not just a raw dump of each slide.

## Step 1 — Try the fast path first: `web_fetch`

Attempt `web_fetch` on one slide URL before reaching for a browser. Some slide sites render server-side and this alone works.

**Diagnostic**: fetch two different slide numbers (e.g. `/1` and `/5`). If both return **identical generic content** (just a page `<title>` / `<meta>` block, no slide-specific text), the site is a client-side-rendered SPA (this is common for Slidev, reveal.js, and similar frameworks) — move to Step 2. Do not conclude this from a single fetch; identical output across two different slide numbers is the actual signal.

## Step 2 — Fall back to Claude in Chrome

This is the reliable path for JS-rendered decks.

1. `tool_search` for `"navigate browser chrome"` to load the claude-in-chrome tools if not already loaded.
2. `list_connected_browsers`. If empty, tell the person no Chrome extension is connected and stop — do not proceed without one.
3. If exactly one browser is connected, confirm with the person before selecting it (don't assume). If multiple, ask them to choose.
4. `select_browser` with the chosen `deviceId`.
5. For each slide, batch **navigate → wait → screenshot** in a single `browser_batch` call. Do 2–3 slides per batch call — more than that risks losing track of which screenshot maps to which slide number.
6. Also try `get_page_text` once early on — some decks expose real text this way even when raw `web_fetch` didn't (rare, but cheap to check on slide 1).
7. **Wait duration**: start with 1 second between navigate and screenshot. If a slide renders **blank** (just background, no content), it needs more render time — re-visit that specific slide alone with a 2–3 second wait rather than assuming the slide is genuinely empty. Track any slides that came back blank on the first pass and revisit them at the end.
8. Confirm the actual last slide number from the on-screen page counter (e.g. "1 / 47") — it may not match the number the person originally gave you. Tell them if it differs.

## Step 3 — Read and organize content

While going through screenshots, capture for each slide:
- The literal text (titles, bullets, labels, code blocks, quiz questions)
- Any diagram/flow shown — note its structure (boxes, arrows, stages) well enough to redraw it as Mermaid later
- Which broad section it belongs to (intro / core concept / hands-on / recap — decks are usually chunked this way, often with visible section-divider slides)

Do **not** paste raw screenshots-as-text into the final tutorial. Synthesize into your own words, per copyright practice — summarize and restructure, don't reproduce slide text verbatim at length.

## Step 4 — Draft in-chat first, get approval

Before creating any file:
1. Propose a section structure based on the deck's natural chunking (the deck's own section-divider slides are usually the best outline).
2. Write the full draft as a chat message (headers, bullet points, tables — matching the person's stated formatting preferences if any are known).
3. Ask what to add/remove/reorder. Do not create a file until the person confirms the content is right — drafting first avoids costly rewrites of a formatted deliverable.

## Step 5 — Build the deliverable

Once approved, and only once a concrete file format is requested (Markdown, docx, etc.):

- **Check `/mnt/skills/public/` for a matching skill first** (e.g. `docx` for Word output) and follow it if the person wants a non-Markdown format.
- For **Markdown output**: write directly with `create_file` to `/mnt/user-data/outputs/`. No dedicated skill is needed for plain `.md`.
- **Adding Mermaid diagrams**: for each major architectural or process concept from the slides, add one small, focused Mermaid diagram near the relevant section rather than a single giant diagram. Match diagram type to content:
  - `flowchart` — pipelines, stage-by-stage processes, before/after comparisons
  - `sequenceDiagram` — timing/interaction between components over time (e.g. a threshold-based decision process)
  - `mindmap` — a single concept with several parallel sub-points
  - `gantt` — relative timing/duration comparisons (use relative units like `dateFormat X` with small integers, not real calendar dates, when illustrating latency/duration rather than a schedule)
  - Use consistent, muted color pairs (`fill`/`stroke`) across diagrams in the same doc for visual coherence.
- After writing, `present_files` so the person can access it — a written-but-unpresented file is not visible to them.

## Step 6 — Offer to make this repeatable

After delivering the tutorial, it's reasonable to ask if the person wants this workflow saved as a skill for future decks (this file is the result of that ask). Don't push it — just offer once.

## Known gotchas

- `web_fetch` can only retrieve URLs that already appeared in the conversation (typed by the person, or returned by a prior search/fetch). It cannot be used to guess-and-check a numeric URL pattern on its own — the person (or a search result) must supply each URL, OR you must switch to Claude in Chrome, which navigates directly and isn't subject to this restriction.
- A blank Chrome screenshot is a render-timing issue, not a missing-slide issue, unless it persists after a longer wait.
- Always confirm the true final slide count from the deck's own page indicator — decks often have more or fewer slides than the range the person initially mentions.
