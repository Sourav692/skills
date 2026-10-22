---
name: dsa-snippet-explainer
description: "Explain DSA notebook code step by step with a full execution-trace markdown table (Step | Action | state columns) that matches the notebook's asserts — the format used for the Combination Sum / Combination Sum II trace. Two output modes — (a) CELL, the default: insert one markdown cell right after the target code cell; (b) FILE: write a `<notebook>_explained.md` reference doc next to the notebook, one section per function, with ASCII diagrams, line-by-line tables and full iteration traces. Either mode can be written in English (default) or Bengali (বাংলা). Works for any DSA (trees, heaps, hashing, sorting, graphs, two pointers, tries, backtracking). Use when the user asks to explain a notebook cell/snippet/algorithm step by step, \"in the same format\" as a prior walkthrough, to add a markdown cell after code, to \"explain the notebook\" / \"create reference notes\" / write an `_explained.md`, or to explain or translate a trace \"in Bengali\" / \"বাংলায়\"."
---

# DSA Snippet Explainer

Turn notebook code into a trace the reader can follow without running it. Canonical example: the
Combination Sum / Combination Sum II trace cell in `deep_dive/21_Backtracking/21_backtracking.ipynb`
(after `combine` / `combination_sum` / `combination_sum2`), plus its Bengali twin right below it.

Never rewrite the code cell. Never overwrite a non-empty explanation (cell or file) without asking.

## Pick the mode

| User says | Mode | Output |
|---|---|---|
| "explain this cell/snippet", "add a markdown cell after this", "same format as the combination-sum trace" | **CELL** (default) | one markdown cell inserted after the code cell |
| "explain the notebook", "reference notes", "write the `_explained.md`", "all tree notebooks" | **FILE** | `<notebook_basename>_explained.md` in the **same folder** as the notebook |
| "in Bengali", "বাংলায়", "translate this trace" | same mode as asked, **language = Bengali** (see [Bengali](#bengali)) | |

Only ask a question if it is genuinely ambiguous *which* function(s) to trace. Never ask about depth or diagram style.

## Shared rules (both modes)

1. **Source of truth = the notebook.** Use the cell's own demo data and its `assert`/`print` output for
   the final state. Neighbouring README only to name invariants — trace the notebook's numbers, not a
   tutorial's example.
2. **Simulate every step.** Every recursive call, choose/include, prune/break, un-choose/exclude, pop/push,
   pointer move, record. One table row per real step. No `...` rows, no invented shortcuts. If the true
   trace has 50 rows, write 50 rows.
3. **Trace table shape:** `Step` + `Action` + one column per piece of mutable state (`path`/`out`/`res`
   after, plus whatever drives the loop/recursion: `remaining`, `i`, `start`, pointers, `stack`, `queue`).

   ```
   | Step | Action | `path` after | `remaining` after | `res` after |
   |---|---|---|---|---|
   | 1 | `backtrack(0, 7)` entered | `[]` | 7 | `[]` |
   | 2 | `i=0`: CHOOSE `2` | `[2]` | 5 | `[]` |
   ```

   - `Action` names the operation in bold/caps (`CHOOSE`, `INCLUDE`, `EXCLUDE`, `BREAK`, `SKIP`, `RECORD`,
     `UN-CHOOSE`, `PUSH`, `POP`, `VISIT`) plus the comparison/index that drove it (`i=2: 6 > 3 → **BREAK**`).
   - Stack written `[bottom ... top]`, queue `[front ... back]` — say which end pops.
4. **Tie-out:** right after each table, one sentence matching the last row to the notebook
   (`Final res = [[2, 2, 3], [7]] — matches assert cs == [[2, 2, 3], [7]]`). Put complexity here too, not in
   its own section.
5. **Mental model** at the end: 3–5 bullets on the *why* (which line/guard changes semantics, what the loop
   variable really represents, what a prune buys) — not a restatement of the loop.
6. **Style:** complete sentences, no filler, gloss any jargon in ≤5 words the first time. Match the
   notebook's names exactly (`path` vs `out` vs `res`, 0-based indices, `//`). Don't import leftovers from
   other chats.

## CELL mode

Insert one markdown cell with the notebook editor (`edit_mode: "insert"`, `cell_id` = target code cell,
`cell_type: "markdown"`). If an empty stub cell sits in that slot, replace or delete it.

If the cell defines several functions, trace **all of them** in one cell, each in its own `####`
subsection, in the order the demo runs (unless the user named a subset). Fill-in template:
[TEMPLATE.md](TEMPLATE.md).

Shape:

- `### Step-by-step: what this cell actually does`
- Opening, 2–4 sentences: the shared shape/invariant, exactly what differs between the functions (one or
  two lines of code), and the demo inputs/expected results.
- Per function, `#### \`fn(...)\` — short tagline`:
  1. Numbered algorithm list, 2–5 steps (fold any "why this invariant" explanation in here).
  2. `Demo: <exact call as the notebook writes it>`.
  3. The full trace table.
  4. The tie-out sentence (+ optionally one line on the row that changed the outcome).
- `#### Mental model`

No ASCII/mermaid per-step diagrams in CELL mode — the table row *is* the picture. A one-line index map
(`index: 0 1 2 3 → value: 1 1 2 5`) is fine in the opening prose when needed.

## FILE mode

Write `<notebook_basename>_explained.md` next to the notebook (e.g.
`deep_dive/04_Tree_Traversal/04_tree_traversal_explained.md`,
`blind_75/Tree/Group 1_Basic Tree DFS/same_tree_explained.md`). Pasted code with no notebook → the folder
the user names, else `outputs/<slug>/<slug>_explained.md` at the repo root. Template:
[FILE_TEMPLATE.md](FILE_TEMPLATE.md). One `##` section per function that implements an algorithm (class
definitions brief; skip pure `assert`/`print` cells unless they teach something). Each section, in order:

1. One-sentence purpose.
2. Input used for the trace — ASCII diagram of the exact tree/array/graph the asserts use (ASCII over
   mermaid; it renders everywhere). Label the root; say BST vs binary vs generic.
3. Code, verbatim from the notebook.
4. Line-by-line table: `| Line / code | What it does |`.
5. Step-by-step trace table (shared rule 3), bold the visited/popped value each row.
6. Final output + tie-out (shared rule 4), then `Time O(...)` / `Space O(...)` with one-line reasons.
7. Mental model.
8. Common confusions, when relevant — e.g. in-order is sorted **only** on a BST; iterative pre-order
   pushes right then left; two-stack post-order reverses Root→Right→Left; `height` base case `-1` vs `0`.

Trace depth in FILE mode:

| Algorithm | Depth |
|---|---|
| Recursive DFS on ≤7 nodes | every visit in order |
| Iterative with stack/queue | every loop iteration until empty |
| BFS level order | queue after each dequeue + enqueue batch |
| Rebuild from traversals | first 2–3 `build()` calls with split indices |
| O(1)-ish helpers (`size`, `find`) | one example call, 2–3 node unwind |

`...` allowed only after ≥3 identical consecutive steps already shown. Batch requests ("all tree
notebooks") → one file per notebook, consistent terminology, no giant merged file. After writing,
report each path and the functions covered.

## Bengali

Same mode, same structure, same table — only the prose changes language.

- If an English trace for this code already exists (cell below the code, or the `_explained.md`), it is
  the source of truth: translate it, don't re-derive. Otherwise simulate first with full rigor, then write
  in Bengali.
- Translate: headings (`### ধাপে ধাপে ব্যাখ্যা (বাংলায়): এই সেলটা আসলে কী করছে`), algorithm-list prose,
  the descriptive words in `Action`, tie-out sentences, mental-model bullets
  (`#### মানসিক মডেল (Mental model)`).
- Never translate: identifiers, code, numbers, Python values in state columns, table pipes/backticks, or
  the caps keywords (`CHOOSE`, `BREAK`, `SKIP`, …) — `i=2: 6 > 3 → **BREAK**` stays byte-identical.
- Same row count, same step numbers, same values as the source trace. Same number of mental-model bullets.
- Add an English gloss in parentheses for any non-obvious Bengali technical term on first use.
- CELL mode placement: if an English trace cell exists, insert the Bengali cell **after it** (English
  first); otherwise directly after the code cell. FILE mode: `<notebook_basename>_explained_bn.md`.

## Quality checklist

- [ ] Every traced function has its own section with demo line and full table; every row is a real step.
- [ ] Final rows match the notebook's `assert`/printed output.
- [ ] Mental model present.
- [ ] CELL: new cell sits right after the code (or after the English trace, for Bengali); no stub left;
      no per-step ASCII blocks.
- [ ] FILE: saved next to the notebook; ASCII input diagram precedes the first trace; line-by-line table
      present; common confusions where relevant.
- [ ] Bengali: values/code/keywords byte-identical to the source; only prose translated.
