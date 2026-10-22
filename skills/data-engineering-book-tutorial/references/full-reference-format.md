# Full Reference Format

The deep-dive deliverable: every pattern's complete Problem → Solution → Consequences →
Examples, reproduced faithfully, plus diagrams, comparison tables, and a cheat sheet.
This is the "read once, understand deeply" version — contrast with the Cram Sheet, which
is the "scan in 5 minutes" version (see `cram-sheet-format.md`).

## Required content inventory (per chapter)

1. **Chapter framing** — a few sentences: why this pipeline stage matters, how it
   connects to the previous/next chapter. Pulled from the book's own chapter opening.
2. **Pattern-by-pattern breakdown** — one `##` section per pattern, each with the book's
   own four-part anatomy as `###` subsections:
   - **Problem** — the concrete scenario, numbers and situations preserved verbatim in
     spirit (never generalized away).
   - **Solution** — high-level idea first, then implementation model.
   - **Consequences** — every trade-off/gotcha the book lists, with its mitigation where given.
   - **Examples** — every code snippet belonging to that pattern, correct language tag,
     book's own comments preserved.
3. **At least one Mermaid diagram per chapter** reproducing a key relationship —
   architecture (`flowchart`), timing/sequence (`sequenceDiagram`), or a comparison. Where
   patterns are naturally sequential or comparable (Full vs. Incremental Load, Static vs.
   Dynamic Joiner), diagram the *relationship*, not just one isolated pattern.
4. **Trade-off/comparison tables** wherever patterns are natural alternatives — even if
   the book presents them as separate prose, synthesize the comparison, but every claim
   must trace back to something the book actually says about each pattern individually.
5. **Gotchas roundup** — a dedicated chapter-level section pulling every Consequence
   across all patterns into one scannable list, organized by pattern.
6. **Case-study callouts** — reproduced wherever the book grounds a pattern in its
   running blog-analytics case study (visits/users, the 50%-drop anecdote, etc.). Don't
   flatten these into generic prose.
7. **Note / Warning callouts** — the book's own admonition convention, reproduced as
   distinct callouts, not blended into body text.
8. **"Say this out loud" lines** — where the book's Solution/Consequences effectively
   hands you a scripted trade-off explanation, collect the sharpest 1-2 sentences per
   pattern, phrased as something you'd say to a senior interviewer — only from what the
   book actually supports.
9. **Cheat sheet** — chapter-end table, one row per pattern: Problem (one line),
   Solution (one line), single biggest gotcha. Highest information density, no prose.
10. **Further reading** — tool-specific quirks, footnoted references the book gives
    (e.g. *Fundamentals of Data Engineering*), kept as a short list.
11. **Code examples** — every `Example` snippet in fenced blocks with correct language tag.

If a chapter names patterns not yet covered, cross-check the book's appendix
pattern-summary table so nothing is silently skipped.

## Markdown structure

- Filename: `chXX_kebab_case_title.md`
- Real Markdown headers (`#`, `##`, `###`) — never fake headers with bold text. One `##`
  per pattern, `###` per Problem/Solution/Consequences/Examples subsection.
- Genuine Markdown tables for every comparison table and the cheat sheet.
- Blockquotes for Note/Warning/Case-Study/Say-this-out-loud, each with a bolded label:
  `> **📌 Note**` / `> **⚠️ Warning**` / `> **🧩 Case Study**` / `> **✅ Say this out loud**`
- Every diagram as a ` ```mermaid ` code block — `flowchart` for pipeline/data-flow,
  `sequenceDiagram` for replication/CDC-style timing, `erDiagram` or a table for
  history/SCD models. Never a static image or ASCII art substitute.
- Code in fenced blocks with correct language tag (`python`, `sql`, `scala`, `java`).
- End with "Cheat Sheet" (tight table) then "Further Reading."

## HTML structure and design system

Filename: same stem, `.html`. Self-contained (inline `<style>`, Mermaid.js from
`https://cdnjs.cloudflare.com` only external dependency). Structure mirrors the Markdown
section order exactly:

- Each pattern as its own visually bounded card (name → Problem → Solution →
  Consequences → Examples in order) so the catalog nature of the book is scannable
  without reading prose.
- Callout boxes with distinct left-border colors/icons for Note, Warning, Case Study,
  Say-this-out-loud.
- Trade-off tables as real `<table>` elements.
- Key figures as interactive SVG/HTML/JS widgets where interaction adds value (hoverable
  nodes, a slider-driven example like a watermark demo), Mermaid render otherwise.
- Code blocks with monospace styling and a visible language label.
- A visually distinct Cheat Sheet panel near the end — boxed grid/card layout per pattern.
- Responsive to mobile, visible focus states, respects `prefers-reduced-motion`. No
  login, no external API calls, no tracking.

### Design identity — reuse across every Full Reference chapter

Established with Chapter 3 ("Incident Log" system) and meant to carry across the whole
set so all chapters read as one book. Reuse this exact palette/type system; only the
`--rust`/`--blue`/`--green`/`--amber` *usage* (which callout maps to which color) should
stay fixed — do not invent a new palette per chapter.

```css
:root {
  --paper: #F6F1E7;        /* page background */
  --paper-raised: #FFFDF8; /* card background */
  --ink: #211D18;          /* body text / dark surfaces */
  --ink-soft: #55504A;
  --ink-faint: #8A8378;
  --rule: #DCD3C0;
  --rule-strong: #C9BCA0;
  --blue: #2B4C6F;    --blue-bg: #E6EDF3;    --blue-border: #A9C1D6;   /* Solution / Note */
  --rust: #C4622D;    --rust-bg: #F7E9DF;    --rust-border: #E3AE8C;  /* Problem / Warning */
  --green: #3F6B4F;   --green-bg: #E6EEE8;   --green-border: #A9C7B4; /* Examples / Case Study / resolved */
  --amber: #A9772E;   --amber-bg: #F3EAD6;   --amber-border: #DDBE85;/* Consequences / Say-this-out-loud */
  --code-bg: #211D18; --code-fg: #F1EADC;
}
```

- **Display face:** Source Serif 4 (headers, editorial feel).
- **Body/UI face:** Inter.
- **Code face:** JetBrains Mono.
- Load all three from Google Fonts via `@import url(...)`.
- Masthead: dark gradient (`#2A241B` → `#211D18`) with a rust bottom border, kicker label,
  serif `h1`, lede paragraph, source-tag pill, and a `.toc` quick-nav row of pill links to
  each pattern's `id` anchor.
- Pattern cards: dark header bar (`#221E19` → `#2E2820` gradient) with a rust index chip
  (`P·01`, `P·02`, ...) and white serif pattern name; body on `--paper-raised` with
  subsection labels using a colored 20px bar + uppercase JetBrains Mono label
  (`.subsec-label.problem` = rust, `.solution` = blue, `.consequences` = amber,
  `.examples` = green).
- Cheat sheet: same dark gradient as masthead, centered header, `.cheat-grid` of cards
  (`repeat(auto-fit, minmax(260px, 1fr))`), each with label/value rows and a distinct
  gotcha row style.
- Diagrams render inside a `.diagram-wrap` card with a small uppercase title above the
  `.mermaid` div; initialize Mermaid with `theme: 'base'` and `themeVariables` pulling
  from the same palette (`background: '#FFFDF8'`, `primaryColor: '#E6EDF3'`, etc.) so
  diagrams match the page rather than using Mermaid's defaults.
- If a chapter benefits from one interactive widget (a slider, a toggle, a hover state),
  build it as plain HTML/CSS/JS in the same file — no framework — following the pattern
  of the Chapter 3 watermark slider (drag a value, re-render positions/colors on `input`).
  Not required for every chapter; use only where it clarifies a genuinely dynamic concept
  (a moving threshold, a state transition, a before/after).

### Verification before presenting

```bash
grep -c '<div' file.html   # compare against
grep -c '</div>' file.html # — must match
```

Also confirm every pattern name from the chapter's research appears as its own `##`
(Markdown) / `<article class="pattern">` (HTML) section — cross-check against the
appendix pattern list so nothing was silently dropped.
