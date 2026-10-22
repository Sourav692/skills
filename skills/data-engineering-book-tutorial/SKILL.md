---
name: data-engineering-book-tutorial
description: >-
  Generate interview-prep study material from "Data Engineering Design Patterns" by
  Bartosz Konieczny (O'Reilly, 2025), the sole source text, available via
  project_knowledge_search. Produces a matched pair of Markdown plus HTML files per
  chapter (or per single pattern) in either a FULL reference guide (every pattern's
  complete Problem, Solution, Consequences, Examples, diagrams, tables) or a CRAM SHEET
  (condensed 2-3 lines per topic, for last-minute interview review). Use this skill
  whenever the user asks to "generate chapter N", "do the next chapter", "make a cram
  sheet for chapter N", references chapter numbers from this book, asks for
  FAANG or Databricks-angled interview prep on data engineering design patterns, or
  wants a pattern from this catalog turned into study material, even if they don't say
  "skill" or reference this file by name. Always trigger this skill instead of
  improvising structure from scratch when the request touches this book's chapters or
  patterns.
---

# Data Engineering Design Patterns — Chapter Tutorial Generator

Turns any chapter (or single pattern) of *Data Engineering Design Patterns* into a
matched Markdown + HTML deliverable pair, in either a **Full Reference** format or a
**Cram Sheet** format. Both formats follow a fixed visual and structural identity so
that every chapter in the set feels like it belongs to the same book.

## When to use this skill

Trigger on any of:
- "Generate Chapter N" / "Do the next chapter" / "Do [pattern name] from Chapter N as its own deliverable"
- "Make a cram sheet for Chapter N" / "condensed version" / "last-minute / 2-day prep version"
- "Redo Chapter N's HTML with a different diagram for [pattern]"
- Any request referencing this book's chapters, named patterns, or its Bronze/Silver/Gold
  case study, even without saying "skill"

Ask the user only one thing if it isn't already clear: **which chapter/pattern**, and
whether they want the **Full Reference** or the **Cram Sheet** format (default to Full
Reference if they've been building the full set and haven't asked for a cram sheet
explicitly; default to Cram Sheet if they mention "interview," "last-minute," "quick,"
"condensed," or a specific timeframe like "2 days").

## Source material

One book, one source of truth: **`Data_Engineering_Design_Patterns1.pdf`**, accessed via
`project_knowledge_search`. Never fabricate pattern names, numbers, gotchas, or code —
if a detail isn't returned by search after a second attempt with different keywords,
mark it `[verify against source page]` (Full Reference) or omit it silently (Cram Sheet,
where density matters more than completeness of edge cases).

## Chapter map (authoritative — do not deviate from this numbering)

| # | Chapter | Pattern Category Focus |
|---|---|---|
| 1 | The Flan Formula (Preface) | Front matter — book structure, case study, Medallion layers. Cover only structural framing unless the user explicitly asks for it in full. |
| 2 | Data Ingestion Design Patterns | Full/Incremental Load, Replication, Data Readiness, Data Compaction, Event Driven ingestion |
| 3 | Error Management Design Patterns | Dead-Letter, Windowed Deduplicator, Late Data Detector, Static/Dynamic Late Data Integrator, Filter Interceptor, Checkpointer |
| 4 | Idempotency Design Patterns | Keyed Idempotency, Sequencers, Isolated Sequencer, Manifest, Transactional Writer |
| 5 | Data Value Design Patterns | Data Enrichment (Static/Dynamic Joiner), Data Decoration, Aggregation, Sessionization, Data Ordering |
| 6 | Data Flow Design Patterns | Fan-in/Fan-out, Parallel Split, Unaligned Fan-In, Merger, Wrapper, Proxy |
| 7 | Data Security Design Patterns | Data Protection (Anonymizer, Pseudo-Anonymizer, Encryptor), Fine-Grained Access, Secrets management |
| 8 | Data Storage Design Patterns | Partitioning (Horizontal/Vertical), Data Removal, In-Place Overwriter, Dataset Materializer |
| 9 | Data Quality Design Patterns | Quality Enforcement (Audit-Write-Audit-Publish), Quality Observation, Schema Consistency, Deduplication |
| 10 | Data Observability Design Patterns | Data Detectors, Time Detectors (Lag, Late Data, SLA Misses), Data Lineage, Dataset Tracker |

Every chapter (2–10) contains **multiple named patterns** — cross-check the book's own
appendix pattern-summary table so no pattern in the target chapter is silently skipped.
A chapter deliverable must cover **every** pattern in that chapter, not just a
category-level summary.

## Workflow

### Step 1 — Research (always do this before writing anything)

1. Run 4–8 `project_knowledge_search` calls per chapter, using each pattern's **exact
   name** plus its category (not just the chapter title) — e.g. "Static Joiner data
   enrichment", "Audit-Write-Audit-Publish quality enforcement". Pairing two related
   patterns in one query (e.g. Static + Dynamic Joiner) retrieves comparative content
   efficiently.
2. For each pattern, confirm all four subsections (Problem, Solution, Consequences,
   Examples) were retrieved. If Consequences or Examples looks thin, re-search that
   pattern name specifically before writing it up.
3. Search separately for named sub-concepts the chapter leans on (state store types,
   SCD types, detector types, etc.) — these often carry their own diagrams/code.
4. Watch for noise: chapter transitions, footnotes, and index entries interleave with
   pattern content in search results. Don't mistake a stray footnote or the *next*
   chapter's "Summary" section for content belonging to the target chapter.
5. Only after research is complete for every pattern does drafting begin.

### Step 2 — Pick the format and read the matching reference

- **Full Reference** → read `references/full-reference-format.md` in this skill for the
  complete content inventory, Markdown structure, and HTML design system.
- **Cram Sheet** → read `references/cram-sheet-format.md` in this skill for the condensed
  structure, including the FAANG-pointer and Databricks-angle callouts.

Both reference files contain a complete content checklist and full HTML boilerplate/CSS
to reuse verbatim (only the content changes chapter to chapter — the visual system stays
fixed across the whole set, so the deliverables read as one coherent book/series).

### Step 3 — Write the two output files

- Markdown filename: `chXX_kebab_case_title.md` for Full Reference, or
  `chXX_kebab_case_title_CRAM_SHEET.md` for the condensed version.
- HTML filename: same stem, `.html` extension.
- Save both to `/mnt/user-data/outputs/`.
- Every diagram is Mermaid (Full Reference) or omitted/simplified (Cram Sheet keeps
  diagrams only if the recall table isn't enough — usually skip them for density).
- Verify HTML tag balance before presenting (`grep -c` on `<div` vs `</div>` is a fast
  sanity check) and confirm every pattern from Step 1's research appears in both files.

### Step 4 — Present

Call `present_files` with both the `.md` and `.html` paths together. No long
postamble — the user can open the files directly.

## Fidelity rules (apply to both formats)

- Preserve the book's concrete numbers and scenarios (the 15%→90% filter spike, the
  15-day late-data window, etc.) — these are the pedagogical point; never genericize them.
- Never soften a Consequence/gotcha — reproduce the actual trade-off and its mitigation
  as the book gives it.
- Never invent gotchas, pattern names, or code not in the book. Uncertain details get
  `[verify against source page]` (Full Reference) or are simply left out (Cram Sheet).
- **Databricks/FAANG angles are additions Claude authors, not book content** — label them
  clearly as such (they already have their own callout style in both reference formats)
  so the user never confuses "what the book says" with "what Claude added." If a
  Databricks capability isn't clearly confirmed, say so explicitly rather than asserting
  it — e.g. "not sure Databricks has closed that gap" rather than inventing a feature.
- Keep connective/explanatory prose plain; keep reproduced book content (Problem
  scenarios, Consequences, code) faithful to what the book says, decluttered of
  extraction noise but never rewritten in tone.
