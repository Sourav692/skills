---
name: dsa-interactive-lesson
description: Build a beginner-friendly, single-file interactive HTML lesson for a Data Structures and Algorithms concept — the `deep_dive/NN_Title_Case/NN_snake_lesson.html` format. Use when the user asks to "explain this DSA concept as an interactive HTML", "make an interactive lesson for X", "create an HTML tutorial for Y data structure", "step-by-step interactive visualization for X", or "teach me BFS/DFS/Dijkstra/Union-Find/Backtracking with an interactive HTML", or wants a new/refreshed Deep Dive lesson page. Produces ONE self-contained offline HTML file in the instructor-grade format of the "Number of Connected Components" reference template — fixed 13-section structure, synced code highlighting, interactive step-by-step traces (Previous / Resume / Next / Reset), edge-case tabs, interview reasoning, practice questions — verified with `scripts/check_lesson.py`. For Blind 75 per-problem pages and topic `patterns.html`, use `leetcode-visualizer` instead. Not for non-DSA content, essays, or slide decks.
---

> **Paths:** `<skills-root>` means the folder that holds this skill — the parent of its base directory (e.g. `~/.claude/skills`, or a repo's `.claude/skills`). Sibling skills referenced below live there too.

# DSA Interactive Lesson (HTML)

You are acting as an **expert DSA instructor**. Your job with this skill is to convert any DSA concept, algorithm, or LeetCode-style problem into a **single self-contained interactive HTML lesson** that a beginner can learn from without help.

## When to use

Load this skill when the user asks for a **DSA teaching artifact** as HTML. Some examples:

- "Explain Kadane's algorithm as an interactive HTML"
- "Make a beginner HTML tutorial for BFS"
- "Turn this LeetCode problem into an interactive lesson"
- "Explain Union-Find step by step in a page"
- "Create a step-by-step HTML for Dijkstra"

Do NOT use this skill for:

- General articles unrelated to DSA
- Slide decks or multi-page docs
- Blind 75 per-problem pages and topic `patterns.html` (use `leetcode-visualizer`)

## Non-negotiable output contract

- Produce **ONE** self-contained HTML file named `<slug>_lesson.html` (`<slug>` = snake_case concept name). Pick the folder in this order and state the path before writing: (1) the folder/path the user names; (2) the folder of an existing notebook for this concept or problem, anywhere in the repo — for a Deep Dive topic that's `deep_dive/NN_Title_Case/NN_snake_lesson.html`, matching the notebook's `NN_snake` name; (3) otherwise `outputs/<slug>/<slug>_lesson.html` at the repo root. Do not overwrite an existing lesson without asking.
- Inline all CSS in `<style>` and all JS in `<script>`
- ALWAYS run `python3 <skills-root>/dsa-interactive-lesson/scripts/check_lesson.py <file.html>` and fix every FAIL before delivering, then do the visual pass in Step 6
- Wrap the trace script inside `window.addEventListener('DOMContentLoaded', () => { ... })`
- Every button MUST use `type="button"`
- Never use external CSS files, external JS files, or CDN dependencies

## Required page structure (in this order)

The finished HTML MUST have these sections, in this order, using the same visual language as the reference template in `references/lesson-template.html`:

1. **Hero**
   - Concept title
   - One-line plain description
   - Chips: core idea, methods covered, interactive tag
   - Canonical example on the right with a small SVG diagram
   - Green result badge showing the expected answer for the canonical example

2. **Why this problem matters**
   - 3 real-world use cases in a 3-column grid
   - Callout with an instructor note

3. **What is <concept>?**
   - Simple definition
   - What you are actually counting / computing / building
   - Beginner shortcut callout

4. **Step-by-step thinking process**
   - 4 numbered cards summarizing the problem-solving flow

5. **How the input becomes X** (adjacency list, DP table, heap, etc.)
   - Left card: input, right card: transformed structure, arrow between them
   - Timeline of how each input piece is added

6. **Method 1: <primary approach>**
   - Intuition sentence
   - Full Python code block with `.stepped` class and per-line `<span class="code-line" data-line="N">`
   - Interactive trace with graph SVG on the left, controls + state grid on the right
   - Full step-by-step trace table below
   - Three insight cards: key mental model, common mistake, why the data structure matters

7. **Method 2: <alternative approach>** (only if there is a genuinely different second method)
   - Same shape as Method 1

8. **Edge cases you should test**
   - Tabs UI (3 examples minimum: minimal, chain / full, mixed)

9. **Method comparison table**
   - Time and space complexity for every method

10. **How to derive this in an interview**
    - Reasoning timeline
    - "What to say out loud" bullets

11. **Common beginner coding mistakes**
    - Two-column list per method

12. **Practice questions**
    - 3 `<details>` blocks with progressive difficulty and reveal answers

13. **Final takeaway**
    - Single closing card + footer note

## Interactive trace rules

Every interactive trace MUST include:

- **Controls**: Previous, Resume (toggles to Pause), Next, Reset
- **Progress bar** + step counter pill
- **State grid** with 4-6 boxes showing the runtime state of the algorithm (stack, queue, set, parent list, DP table, count, current node, etc.)
- **Live SVG graph / structure** with color states
- **Synced code highlighting**: each step lists the code lines it maps to via `lines: [N, N, N]`
- **Active row highlight** on the trace table

Legend colors (reuse consistently):

- Blue `#315efb` = first side / visited / stable state
- Green `#13a46b` = second side / frontier / in queue-stack
- Orange `#ff9f1c` = currently active / current pop
- Gray `#c8d2e7` = untouched / not yet reached

## Code block rules

- Wrap stepped Python code in `<div class="code-block stepped"><code id="...-code">...</code></div>`
- Every line, including blank ones, is wrapped in `<span class="code-line" data-line="N"></span>`
- The `stepped` class collapses blank-line height so the code stays compact
- Non-stepped code cards (input examples, adjacency list output) use plain `<div class="code-block"><code>...</code></div>` — do NOT add the `stepped` class or their text will disappear

## Design rules

- Minimal, clean, instructor-tone layout — never marketing / decorative
- Card + panel layout with soft shadow, 18px radius
- Inter font, 1.6 line-height
- Palette: use the CSS variables in the template exactly — do NOT hard-code hex colors elsewhere
- Real diagrams (inline SVG), not emoji

## Content rules (this is the instructor part)

- Write like an instructor, not a reference. Every explanation must answer "why".
- Explain the **transformation of the input** to the working structure (adjacency list, table, heap) explicitly. This is where beginners lose the thread.
- Every method must include: intuition, code, trace, mistakes.
- Interview section must show the derivation, not just the answer.
- Practice questions must have hidden reveal-answers.
- No fabricated tricks or shortcuts. Only teach what the code actually does.
- Do NOT include emojis anywhere.

## Workflow to follow

Use this exact order. Do not skip steps.

### Step 1 — Gather the concept context

Confirm you have:
- Concept name (e.g. "BFS", "Kadane", "Trie", "Union-Find")
- Canonical example (input + expected output). If missing, invent a small illustrative one and clearly say so
- At least one working Python solution
- 1-2 edge cases

If a notebook for this concept or problem exists anywhere in the repo (`git ls-files '*.ipynb' | grep -i '<slug>'`, or the topic notebook in `deep_dive/NN_Title_Case/`), take the code and example from it so the lesson and notebook agree; trace the notebook's own asserts.

If any is unclear, ask ONCE (a single AskUserQuestion call) before generating. Otherwise proceed with sensible defaults.

### Step 2 — Plan the trace

For each method:
- Write out the state per step in a Python dict list. This is the ground truth for the JS trace.
- Confirm each step has: title, text, per-state values (stack / queue / parent / dp / etc), what changed, and the mapped code lines.
- If the state cannot be represented visually, add a smaller diagram (bars, tree, table) as SVG.

### Step 3 — Copy the reference template

Start from `references/lesson-template.html`. It contains:
- All CSS
- Placeholder structure for every required section
- Working DFS + Union-Find style scripts for the trace player

Replace the concept-specific parts. Do NOT rewrite CSS from scratch.

### Step 4 — Build the interactive traces

- Fill `steps = [ {...}, {...}, ... ]` for each method
- Wire renderers (`renderMethodA`, `renderMethodB`) to update state + graph + highlighted code
- Test that the buttons work (`type="button"` and DOMContentLoaded wrapper — see script skeleton in the template)

### Step 5 — Fill the teaching sections

- Hero, use cases, definition, thinking process, input-to-structure explainer
- Every method's insight cards
- Edge case tabs
- Comparison table
- Interview reasoning
- Common mistakes
- Practice questions with reveal answers

### Step 6 — Verify

1. **Structure (always):** `python3 <skills-root>/dsa-interactive-lesson/scripts/check_lesson.py <file.html>`. It fails on external resources, `<button>` without `type="button"`, missing `DOMContentLoaded`, a trace missing any of `<prefix>-prev/-next/-play/-reset`, no `data-line` code sync, fewer than 3 practice `<details>`, unbalanced tags, or a missing required section. Fix and re-run until PASS.
2. **Visual (when a browser tool is available):** open `file://<absolute path>` and take a full-page screenshot — e.g. Playwright MCP (`browser_navigate` + `browser_take_screenshot` with `fullPage: true`) or Chrome DevTools MCP (`new_page` + `take_screenshot`). Read the image and fix clipping, blank code cards (a `.stepped` class on a non-stepped block hides its text), overlapping SVG labels, or spacing issues. Click each trace's Next button a few times and re-screenshot to confirm the state grid, SVG, code highlight, and table row all move together. Check the browser console for errors.
3. If no browser tool is available, say the visual pass was skipped and ask the user to open the file.

### Step 7 — Deliver

- If the lesson landed inside a track (`deep_dive/`, `blind_75/`, `neetcode_150/`), run the `dsa-index-updater` skill so its indexes (e.g. the `deep_dive/README.md` "Interactive HTML" column and `deep_dive/index.html`) link the new lesson. Skip that for `outputs/`.
- Reply with the file path, the check result, whether the visual pass ran, and what sections and interactive features were included.

## Reference material

- `references/lesson-template.html` — full working template. START HERE. Contains complete CSS, JS trace player, and all section placeholders.
- `scripts/check_lesson.py` — structural checker (Step 6). Stdlib only; exit 0 = pass.
- `scripts/build_lesson.py` — optional: copies the template and swaps only the title, hero description, and canonical example from a JSON spec (`python3 build_lesson.py spec.json out.html`). Everything else is still adapted by hand.
- Finished examples in this repo: `deep_dive/*/*_lesson.html` (e.g. `deep_dive/21_Backtracking/21_backtracking_lesson.html`, 3 traces).

## Anti-patterns to avoid

- Rewriting the CSS from scratch instead of reusing the template
- Skipping the interactive trace (this is the single most important feature)
- Skipping the input-to-structure explainer (this is where beginners fail)
- Skipping edge cases or practice questions
- Delivering without a passing `check_lesson.py` run (and the screenshot pass when a browser tool exists)
- Adding CDN links or external stylesheets
- Marketing tone, emojis, decorative flourishes

## Reminder

Your job is not to describe an algorithm. Your job is to **teach it** so a beginner can walk away and code it themselves. Every design choice above serves that goal.
