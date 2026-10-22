---
name: study-content-style
description: "Write or rework learner-facing markdown in three modes. Prose mode: create new tutorial pages or restyle existing ones for a tutorial, course, handbook, or docs website so they read as clear plain-English teaching prose in a house format (trade-off tagline, reading time, imperative section headings, three-move sections, worked example, key takeaways, self-check questions). Notebook-cell mode: rewrite an existing notebook's dense Concepts/theory cell as plain bullet points without losing any Big-O, definition or example. Compress mode: trim study, interview, and tutorial markdown so it stays complete but becomes scannable, keeping every fact, number, diagram, and spoken script and turning restated prose into tables. Use for 'write a page explaining X', 'turn these notes into a tutorial', 'restyle this page', 'make this less jargony', content that feels dry or listy (prose mode), and for 'trim', 'compress', 'shorten', 'too verbose', 'reduce reading time' on a .md page (compress mode)."
---

> **Paths:** `<skills-root>` means the folder that holds this skill — the parent of its base directory (e.g. `~/.claude/skills`, or a repo's `.claude/skills`). Sibling skills referenced below live there too.

# Study content style

Three modes. Prose and Compress pull in opposite directions; Notebook-cell applies plain bullets to one notebook cell. Pick one per request.

| The user wants... | Mode | Read |
|---|---|---|
| A new teaching page, or an existing page that reads as a dry bullet inventory turned into plain-English prose | Prose | `references/prose.md` |
| A page that is too long or verbose made scannable without losing facts | Compress | `references/compress.md` |
| An existing notebook's dense Concepts/theory cell rewritten as plain bullet points (one notebook or a folder) | Notebook-cell | `references/notebook-concepts.md` |

Routing rules:
- "Write", "draft", "restyle", "less jargony", or "too listy": use Prose.
- "Trim", "compress", "shorten", "too verbose", or "cut reading time": use Compress.
- "Concepts cell", "theory section", "simpler language" or "proper bullet points" for a `.ipynb`: use Notebook-cell. Writing a brand-new notebook is `leetcode-notebook`'s job.
- Never run Prose and Compress on one page in one pass. Each mode undoes the other. If the user asks for both, ask which sections get which.
- For the `Agent_Evaluation_Demystified` repo, prose mode also reads `references/agent-eval-demystified.md`.

Prose mode bundles two checkers, run from this skill's directory:
- `scripts/check_prose.py`
- `scripts/page_stats.py`

Both modes keep the `◷ N min` reading-time line accurate.
