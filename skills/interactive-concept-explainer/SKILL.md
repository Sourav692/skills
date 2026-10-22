---
name: interactive-concept-explainer
description: Creates a matched pair of teaching artifacts for any topic in one step - (1) an interactive dark-themed HTML "lab" with a live slider, toggle, or tab-driven visualization the user can manipulate, and (2) a companion blog-style Markdown post with headers, bullets, a TL;DR, Mermaid diagrams, and a 5-question "interview spotlight" section framed around real-time production/customer use cases of the kind asked at OpenAI, Anthropic, Google, and similar AI-lab interviews. Use whenever the user asks to explain, teach, or create a diagram, lab, blog post, or interview-prep questions for a concept - technical, scientific, business, or otherwise - especially if they reference "the same format/style as before", ask for "an interactive diagram", or are building a numbered series of concept explainers. Trigger even when only the HTML, only the markdown, or only interview questions are requested by name, or for several topics at once. Skip it for simple one-line factual questions with nothing worth visualizing.
---

# Concept Lab

Turns any concept into a two-file teaching package:

1. **An interactive HTML "lab"** — a single self-contained dark-themed page with one real, working interactive mechanic (a slider, toggle, or tab set) that recomputes honest numbers live and explains what's on screen through a dynamic callout.
2. **A companion Markdown blog post** — headers, a TL;DR, bullet points, comparison tables, one or more Mermaid diagrams that mirror the same mechanism shown in the HTML, and a closing **"Interview Spotlight"** section of 5 practice questions in the style of real-time, production/customer-use-case interviews at companies like OpenAI, Anthropic, and Google.

Both files are numbered and slugged together (`NN-topic-slug.html` / `NN-topic-slug.md`) so they read as one entry in an ongoing series.

## Before you build anything

Read both reference files now — they contain the exact CSS tokens, component snippets, and JS conventions this skill depends on for visual and behavioral consistency across every lab it produces:

- `references/design-system.md` — fonts, colors, layout, and every reusable HTML/CSS/JS component pattern (cards, sliders, tabs, stat bars, callouts, animated reordering lists, SVG scatter plots).
- `references/blog-template.md` — the Markdown skeleton, section conventions, and a guide to picking the right Mermaid diagram type with syntax gotchas to avoid.

Do not improvise new color palettes, fonts, or layout systems — the entire point of this skill is that every lab it produces looks and behaves like it belongs to the same series.

## Workflow

### Step 1 — Establish the topic and series context

- If the user gives one topic, that's a single lab. If they list several, or say "do this for the rest of X," treat each as one part of the same numbered series.
- Check `/mnt/user-data/outputs` for existing `NN-*.html` / `NN-*.md` pairs before naming files — continue the existing numbering and series name rather than restarting at 01, unless the user is clearly starting a new, unrelated series.
- Don't ask the user to specify chart types, colors, or layout — that's this skill's job. Only ask a clarifying question if the topic itself is ambiguous (e.g., "explain trees" — data structure or biology?).

### Step 2 — Design the interactive mechanic first, before writing any code

This is the step that most determines quality. For each concept, decide:

- **The one control** the user will manipulate: a slider (a continuous parameter like λ, k, or alpha), a toggle (two competing methods), or tabs (categories/filters). Resist the urge to add multiple controls — every lab in this series isolates exactly one variable.
- **A small, hand-designed dataset** — 8–20 items — where the relationships are deliberately engineered so the mechanic's payoff is obvious and honest. Never use random or generic placeholder data; pick concrete examples (specific queries, documents, numbers) whose designed answer teaches the concept. If a running example theme already exists in this series (e.g. a customer-support KB), reuse it for continuity instead of inventing a new one.
- **What the numbers actually mean** — decide whether to compute the underlying math for real in JS (e.g. actual BM25, actual greedy selection, actual cosine similarity on real coordinates) or to hand-place illustrative scores designed to tell a clean story. Prefer real computation whenever the algorithm is simple enough to implement in vanilla JS in a few dozen lines (ranking formulas, greedy loops, distance metrics) — it makes the interactivity trustworthy rather than scripted. Hand-placed scores are fine for anything that would require an actual trained model (e.g. a real cross-encoder or embedding model) — just design them so the narrative is internally consistent.
- **The payoff moment** — know in advance what the user should notice as they move the control (a number flips, items reorder, a category disappears). The dynamic callout text (see design-system.md) exists specifically to name that moment in prose as it happens.

### Step 3 — Build the HTML lab

- Follow `references/design-system.md` exactly for the `<head>` font imports, CSS root variables, and component classes.
- Single self-contained file: inline `<style>` and `<script>`, no external JS/CSS dependencies besides the two Google Fonts. No `localStorage`/`sessionStorage`.
- Include: a short header (eyebrow label + H1 + one-sentence subtitle), the interactive control(s), a live-updating visualization (scatter plot, ranked list, matrix grid, or bar/stat cards — whichever fits the concept), stat cards with live numbers, and a dynamic callout paragraph that changes with the control state.
- Make it mobile-responsive (stack grids to one column under ~700px) and accessible (`aria-pressed` on toggles, `:focus-visible` outlines, a `prefers-reduced-motion` rule).
- If you implemented any real algorithm (BM25, greedy MMR, cosine similarity, etc.), sanity-check it before finalizing: extract the core scoring logic and run it standalone with `bash_tool`/Node to confirm it produces the ordering the lesson depends on. Fix the dataset or logic if it doesn't — never leave a callout claiming a result the code doesn't actually produce.

### Step 4 — Build the companion Markdown post

- Follow `references/blog-template.md` for section structure and Mermaid diagram choice.
- Reuse the *same* numbers, dataset, and narrative beats from the HTML lab — the two files should feel like two views of one lesson, not two different explanations.
- Pick the Mermaid diagram type that matches the concept's shape (pipeline → flowchart, two-axis trade-off → quadrantChart, algorithm loop → flowchart with a decision diamond, two mechanisms compared → flowchart with labeled subgraphs). Multiple small diagrams are fine if the concept has multiple distinct parts (e.g. an architecture diagram plus a formula-explanation diagram).
- Include: title + italicized series tag line, TL;DR bullets, the problem/motivation, the core mechanism (formula in a code block if there is one), the Mermaid diagram(s), a comparison/trade-off table, a "when to use / when to avoid" section, an **Interview Spotlight** section (see below), and a closing "Key Takeaways" bullet list.
- End with a one-line prev/next series footer if this is part of a numbered series.

**Interview Spotlight section — always include this.** Write 5 interview questions on the concept, in the style asked at OpenAI, Anthropic, Google, and similar AI-lab interviews for real-time, production, customer-facing use cases. Follow `references/blog-template.md` for the exact format and the good-vs-weak question guidance — in short:

- Frame every question around a live production scenario (scale, latency, freshness, cost, monitoring, failure handling, ambiguous trade-offs), never a bare definitional "what is X" — that tests recall, not engineering judgment, and isn't what these interviews actually probe.
- Ground each question in the same concept and, where natural, the same running example/dataset used in this lab, so it reads as an extension of the lesson rather than a generic quiz.
- Pair every question with a short "what a strong answer covers" bullet list (3–4 points) — this is interview prep, not a trivia list, so the reader needs to know what a good answer actually contains, not just the prompt.
- Vary the 5 across question types: at least one debugging/production-incident question, one design-trade-off question, one "how would you measure/monitor this" question, and one question that pushes on a genuine edge case or failure mode of the concept.

### Step 5 — Save and present

- Save as `/mnt/user-data/outputs/NN-topic-slug.html` and `/mnt/user-data/outputs/NN-topic-slug.md` with matching numbers and slugs.
- Call `present_files` with both paths together.
- In your reply, keep the surrounding prose in the same register as the lab itself: headers/bullets for the written explanation, then a one-line pointer at the end telling the user what to click or drag first to see the payoff moment.

## Multi-topic / full-series requests

If asked to generate a whole series at once, repeat Steps 2–4 once per topic, incrementing the series number each time, and cross-link each post's prev/next footer to the actual neighboring titles. Keep the accent-color choices per lab distinct enough to tell labs apart, but keep the base tokens (ink/panel/text/muted, fonts, component shapes) identical across all of them — that shared shell is what makes the whole thing read as one series.
