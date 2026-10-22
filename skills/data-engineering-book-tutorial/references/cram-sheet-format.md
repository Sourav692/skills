# Cram Sheet Format

The condensed deliverable for last-minute interview review — 2-3 lines per topic, built
for scanning under time pressure, not reading. Contrast with the Full Reference (see
`full-reference-format.md`), which is the deep-dive version.

## Required content per pattern (keep every item to 2-3 lines max)

1. **Problem** — one sentence, the concrete scenario compressed to its essence.
2. **Solution** — one sentence, the core mechanism only (no implementation walkthrough).
3. **Gotcha** — the single biggest trade-off, one sentence. If the book lists several,
   pick the one most likely to come up as a follow-up question, not all of them.
4. **📌 Note** — one short callout with the single most essential piece of book context
   (a definition, a distinction) needed to not misunderstand the pattern. Skip if nothing
   in the book rises to "essential" — don't pad.
5. **✅ Say this out loud** — one ready-to-speak sentence a candidate could say verbatim
   in an interview, grounded in what the book actually supports (same fidelity rule as
   the Full Reference — never invent a scripted line the book doesn't back).
6. **🎯 FAANG pointer** — one sentence naming the kind of follow-up question interviewers
   tend to ask about this pattern, and the shape of the correct answer. This is Claude's
   own interview-coaching addition, not book content — keep it labeled as such via the
   callout style, never blended into the Problem/Solution/Gotcha lines.
7. **🧱 Databricks angle** — one sentence connecting the pattern to a genuine Databricks
   or Delta Lake capability, *only if one is clearly confirmed* (in the book's own
   examples, or well-established product behavior like `checkpointLocation`,
   `dropDuplicates`, `MERGE INTO`, Delta table version history, Unity Catalog, etc.). If
   no clear capability exists, say so plainly — e.g. "No dedicated product feature here;
   it's just a write pattern on Delta" or "not sure Databricks has closed that gap" —
   rather than inventing one. This is also Claude's own addition, not book content.

## What to cut relative to the Full Reference

- No implementation walkthroughs, no multi-step Solution breakdowns — one sentence only.
- Code examples are optional and should be omitted unless a single short snippet is the
  fastest way to jog memory of a specific API call (e.g. `.withWatermark(...)`) — never
  reproduce a full multi-block example.
- Diagrams are optional — most chapters don't need them in Cram Sheet form; the recall
  table usually does the job. Only include a diagram if the chapter's core concept is
  genuinely hard to hold in your head as text (e.g. a watermark timeline, a fan-out
  topology) — one diagram maximum for the whole chapter, not per pattern.
- Skip case-study callouts, warnings, and secondary gotchas — density beats completeness
  here. If forced to choose, keep the Gotcha and Say-this-out-loud lines over anything else.

## Required structural elements (whole-chapter level)

1. **One-page recall table** — every pattern as a single row: `# | Pattern | Problem |
   Fix | #1 Gotcha`. Place this near the top (Markdown) or right under the header
   (HTML) so it works as a standalone crib sheet even without reading further.
2. **The connecting thread** — a short callout (3-4 sentences) tying the chapter
   together conceptually, usually drawn from the book's own chapter summary/closing
   paragraph. Place near the top (Markdown intro) and echo briefly at the end (HTML
   closer) as a "before you close the laptop" reminder.
3. Per-pattern sections in the same order as the book presents them.

## Markdown structure

- Filename: `chXX_kebab_case_title_CRAM_SHEET.md`
- `#` chapter title, then the recall table, then one `##` per pattern (numbered, e.g.
  `## 1. Dead-Letter`).
- Bold inline labels for Problem/Solution/Gotcha (`**Problem:**`, `**Solution:**`,
  `**Gotcha:**`) rather than full `###` subsections — this is a deliberate density choice
  vs. the Full Reference's `###` structure.
- Blockquotes for Note/Say-this-out-loud/FAANG pointer/Databricks angle, same emoji-label
  convention as the Full Reference: `> **📌 Note:**`, `> **✅ Say this in interview:**`,
  `> **🎯 FAANG pointer:**`, `> **Databricks:**` (plain bold, no emoji needed for this one
  since it's answered in prose, not a blockquote-callout, in the Markdown version).
- Close with the one-page recall table repeated (or once, positioned wherever reads
  best) and a short closing section naming the chapter's unifying thread.

## HTML structure and design system

Filename: same stem, `.html`. Reuses the **same palette and type system** as the Full
Reference (see `full-reference-format.md`'s CSS variables) for series consistency, but
flattened into a single-screen-per-pattern "flashcard stack" layout rather than the
long-form card structure:

- Sticky header with chapter title, one-line description, and a pill-style quick-nav
  jumping to each pattern's card anchor.
- A `.thread` callout (purple accent, distinct from the four existing callout colors,
  since it's chapter-level framing rather than a pattern-level callout) stating the
  chapter's unifying idea, right under the header.
- The one-page recall `<table>` immediately after the thread callout.
- One compact `.card` per pattern: dark header bar with index chip + name (same style as
  Full Reference pattern cards), then inside the body:
  - Three `.row` lines (Problem / Solution / Gotcha) with a fixed-width colored tag label
    and flowing text — not full subsection blocks.
  - Up to four small `.callout` boxes (note / say / faang / dbx) using the same
    color-coding as the Full Reference (blue=note, amber=say-this-out-loud) plus two new
    ones for this format: rust-tinted for FAANG pointer, green-tinted for Databricks angle.
- A closing `.closer` panel (same dark gradient as the header) with a short "before you
  close the laptop" reminder line.
- Responsive, focus-visible states, respects `prefers-reduced-motion`, no external calls
  beyond Google Fonts.

### Reusable CSS additions specific to this format (on top of the Full Reference palette)

```css
--purple: #6B4C8A; --purple-bg: #EFE7F5;  /* chapter-level "thread" callout only */
```

```css
.row { display: flex; gap: 10px; margin-bottom: 10px; align-items: baseline; flex-wrap: wrap; }
.row .tag {
  font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; letter-spacing: 0.06em;
  text-transform: uppercase; font-weight: 700; flex-shrink: 0; width: 74px; padding-top: 2px;
}
.row .txt { flex: 1; min-width: 220px; font-size: 0.92rem; }
.row.problem .tag { color: var(--rust); }
.row.solution .tag { color: var(--blue); }
.row.gotcha .tag { color: var(--amber); }
```

Callout variants to add beyond the Full Reference's four (note/warning/case/say):

```css
.callout.faang { background: var(--rust-bg); border-color: var(--rust-border); }
.callout.faang .lbl { color: var(--rust); }
.callout.dbx { background: var(--green-bg); border-color: var(--green-border); }
.callout.dbx .lbl { color: var(--green); }
```

Use `<span class="dbx-unsure">` (italic, `--ink-soft` color) to visually flag the
sentence fragment where a Databricks capability is uncertain, so the honesty signal is
visible at a glance, not just in the wording.

### Verification before presenting

Same `<div>`/`</div>` balance check as the Full Reference. Also confirm the recall table
has exactly one row per pattern researched in Step 1, and that every pattern has all
four callout types (note, say, faang, dbx) — a missing Databricks callout should still
be *present* with an honest "no dedicated feature" line, not silently dropped.
