# Compress study markdown

Rewrite the page so a reader can scan it the night before. Same facts, fewer sentences. Do not summarize away a requirement, a number, a failure mode, or a line the reader is supposed to say out loud.

## What to cut

Cut a paragraph when a table, diagram, or the next sentence already says it.

- Lectures that define a format ("a requirement that cannot fail a test…") — one line, then the table.
- A walkthrough that repeats the rows of the table under it.
- A second telling of the same architecture (prose after the diagram).
- "Because" clauses that restate the row. Put the test in an **Accepted when** column instead.

## What to keep

- Every must / should / could / won't, every threshold, every owner.
- ASCII and Mermaid when both are present. They are two views, not duplicates to delete. If you add or restore one, keep the other.
- Spoken scripts, closing lines, and story beats the reader will say.
- SQL, filter encodings, and "what actually ran / what was not verified."
- Section cross-references. If you insert or remove a section, renumber headings and fix every "section N" pointer, including the intro map, takeaways, and references.

## Rewrite patterns

**Requirements.** One sentence on the split, then:

| Priority | Requirement | Accepted when |
| -------- | ----------- | ------------- |
| Must | … | the test that fails it |

Label the non-functional table **Non-functional**. Columns: Constraint | Testable form. Latency stays a percentile with a number, never "fast enough."

**Comparisons** (weak / average / strong, before / after, option A / B) become a table. One row per option. No paragraph that narrates the rows.

**Assumptions** become one block or a short bullet list, then the schema line unchanged.

**Follow-ups** stay as a table. Answer cells are one or two sentences. Keep the decision, drop the warmup.

**Failure stories** become a labeled path: what passes, why that is the bug, the fix. Not a scene.

**Scale.** A table of Quantity | Figure | What it forces. End with the lines to say, not an essay.

## Diagrams

ASCII must be readable in a narrow code block. Stack it. One step per line. Do not draw one box so wide the query path wraps.

```
QUERY  (sync)
  user
   --> gateway     authN
   --> ENFORCE     trust boundary
   --> answer
```

Mermaid stays. Prefer `flowchart TB` when the ASCII is top to bottom, so the rendered graph matches the reading order.

## Reading time

If the page has a `◷ N min` line, lower N after a real cut. Do not lower it for a diagram restore. Spoken scripts and deep-dive sections still count.

## Done when

- A section that was prose is a table or a short labeled block.
- No sentence only repeats the diagram above it.
- No fact from the original Must list, NFR list, or spoken close is missing.
- Cross-references still point at the right heading.
---
