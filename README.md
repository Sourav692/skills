# Skills

Agent skills I wrote for study notes and tutorials, DSA practice, notebook and course-repo cleanup, site planning and audits, Python environments, and keeping a skill library tidy. They work in Claude Code and in any agent that the [`skills` CLI](https://skills.sh) supports.

## Install

**Into one repo (or globally) with npx.** Run this inside the repo:

```bash
npx skills@latest add Sourav692/skills                         # choose from a list
npx skills@latest add Sourav692/skills --skill format-notebook  # one skill
npx skills@latest add Sourav692/skills --skill format-notebook --skill course-repo-cleanup
npx skills@latest add Sourav692/skills --skill '*'              # every skill
npx skills@latest add Sourav692/skills --list                   # list without installing
```

Add `-g` to install for every project instead of the current one. Add `-a claude-code` to skip the agent prompt. Update later with `npx skills@latest update`.

**As a Claude Code plugin (all skills, updates itself):**

```bash
/plugin install sourav-skills --marketplace Sourav692/skills
```

On older Claude Code versions, run `claude plugin marketplace add Sourav692/skills` first, then `claude plugin install sourav-skills@sourav692`. Plugin skills are namespaced, e.g. `sourav-skills:format-notebook`.

Pick one method per agent. Installing both gives you every skill twice.

### Install these together

Some skills call a sibling skill's file through `<skills-root>/<skill>/...`, where `<skills-root>` is the folder that holds the installed skills. Install the sibling too:

| If you install | Also install | Why |
|---|---|---|
| course-repo-cleanup | format-notebook | Uses its notebook format rules |
| dsa-index-updater | link-check | Runs its link checker |
| site-plan-to-tasks | site-plan | Reads the plan that site-plan writes |

**Scope** in the tables below says whether a skill works in any repo or is written for one repo's layout.

## 1. Career (1)

| Skill | What it does | Scope |
|---|---|---|
| career-docs | Resumes, ATS checks, bullets, layout, sections, executive resumes, academic CVs, cover letters and application answers — one mode per job, each in `references/` | Any |

## 2. Study, tutorial and explainer content (8)

| Skill | What it does | Scope |
|---|---|---|
| fde-study-notes | FDE study notes in 3 modes: chapter → full tutorial, tutorial → interview-cram `_v2`, fdehandbook.com page → bullets | Any |
| data-engineering-book-tutorial | Writes interview study notes from *Data Engineering Design Patterns* (claude.ai Project only) | Any |
| agentic-ai-book-tutorial | Writes short tutorials with many diagrams from *Cracking Agentic AI* (claude.ai Project only) | Any |
| slide-tutorial-builder | Turns a numbered set of slide-deck URLs into a tutorial | Any |
| interactive-concept-explainer | Builds an interactive explainer plus study notes for any topic, in one step | Any |
| notebook-interview-tutorial | Turns a notebook folder into an interview study guide plus an interactive HTML quiz in `Study_Guides/` | Any |
| eval-concept-explainer | Explains an eval metric, failure mode or confusing sentence in plain English | Agent_Evaluation_Demystified |
| study-content-style | Learner content in 3 modes: write/restyle as plain teaching prose, compress to scannable bullets, or rewrite a notebook's Concepts cell as plain bullets | Any |

## 3. DSA and interview practice (8)

| Skill | What it does | Scope |
|---|---|---|
| coding-mock-interview | Runs a mock coding interview as a senior interviewer | Any |
| system-design-mock-interview | Runs a voice-friendly mock FDE system-design interview | Any |
| dsa-interactive-lesson | Builds a single-file interactive HTML lesson for one DSA concept | Any (best in dsa_demystified) |
| dsa-snippet-explainer | Step-by-step trace of notebook code: a cell after the code, or a `_explained.md` file; English or Bengali | Any |
| leetcode-notebook | Generates a structured study notebook for any coding problem | Any (best in dsa_demystified) |
| leetcode-visualizer | Turns problem notebooks into interactive HTML pages plus a patterns page | Any (best in dsa_demystified) |
| neetcode-pattern | Builds one pattern of the NeetCode 150 track | dsa_demystified |
| dsa-index-updater | Updates every index after adding or renaming a problem or topic | dsa_demystified |

## 4. Notebooks and course repos (2)

| Skill | What it does | Scope |
|---|---|---|
| format-notebook | **The** educational notebook format (rules 1–9); every other notebook skill points here | Any |
| course-repo-cleanup | A course repo, or one module or folder: audit, branch, consolidate, migrate LangChain 0.x (bundled scanner) and other libraries, run every notebook, PR | Course repos |

## 5. Websites (6)

| Skill | What it does | Scope |
|---|---|---|
| site-plan | Writes a buildable site plan from a senior UI/UX designer's point of view | Any |
| site-plan-to-tasks | Reviews that plan, then turns it into phased task cards (`check_plan.py`) | Any |
| verify-site | Runs sync, content check, lint, typecheck and build, then reports failures | Sites with `site/` |
| link-check | Finds broken relative links, case-exactly against git (`--html` adds hrefs and .html files) | Any |
| fde-html-explorer | Builds a standalone HTML explorer for one FDE system-design case | Any |
| site-audit | Audits a site's structure, UX and quality on a 10-dimension rubric against competitors and tracks scores over time; one profile per site (FDE, eval) | FDE and eval sites |

## 6. Dev environment and skill tooling (3)

| Skill | What it does | Scope |
|---|---|---|
| python-repo-env | One root uv environment: quick commands, full setup or repair, kernels, notebook-output hygiene | Any |
| ml-repo-commit | Makes clean commits in Python AI/ML repos | Any |
| skill-library-cleanup | Inventories, consolidates, prunes and renames your own skills into one library, with an approval gate per audit (`inventory.py`, `rename_skills.py`, `validate_library.py`) | Any |

## Consolidation log

How the library got to its current shape (2026-10-22): 62 skills cut to 41 by an overlap audit, then to 27 by a necessity audit; then 10 renames and one new skill.

| Removed | Now covered by | Why |
|---|---|---|
| interview-book-tutorial-builder | agentic-ai-book-tutorial | Identical file |
| agentic-ai-interview-tutorial | notebook-interview-tutorial | Older copy of the same skill |
| resume-tailor, resume-ats-optimizer, resume-bullet-writer, resume-formatter, resume-section-builder, executive-resume-writer, academic-cv-builder, cover-letter-generator, application-form-filler | career-docs | The bundle already contained each one in full |
| tutorial-prose-style, compress-study-markdown | study-content-style | The bundle already contained both |
| fde-chapter-tutorial, fde-tutorial-interview-format, fdebook-summarizer | fde-study-notes | Bundle; its interview-format mode was refreshed to the newest version first |
| dsa-snippet-explainer-bn | dsa-snippet-explainer | Has a built-in Bengali mode |
| tree-notebook-explainer | dsa-snippet-explainer | FILE mode is the newer version of the same output |
| virtual-env-setup | python-repo-env | Superset; gained a quick-commands table |
| notebook-folder-cleanup-planner | notebook-folder-cleanup | Folded in as its planning stage (`references/planning.md`) |
| fde-site-audit, eval-site-audit | site-audit | Same engine; one profile per site |
| course-repo-cleanup's own `notebook-format.md` | format-notebook | Two format definitions contradicted each other (install cells, outputs, LLM setup); merged into one |
| The "reformat Concepts cell" section of leetcode-notebook | plain-theory-formatter | One owner per job |
| explainer | — (retired) | Its target folder was archived on 2026-10-15 |
| ai-roadmap-organizer | — (retired) | Its repo (AI-ENGINEERING-DEMYSTIFIED) was split into 14 repos on 2026-09-29 |
| learning-tracker | — (retired) | Tracked phases of the retired monorepo |
| langchain-v1-pipeline, plan-to-tasks (migration), plan-to-teaching-notebook, notebook-review | — (retired) | Task-board machinery for the finished monorepo migration |
| langchain-v1-migration-audit | course-repo-cleanup (`scripts/scan_langchain_v1.py`, `references/langchain-v1-*.md`) | Scanner and rewrite map kept; plan-file workflow dropped |
| notebook-folder-cleanup (2nd round) | course-repo-cleanup (`references/library-migration-map.md`, archive option) | Its target repo was retired; aied already covers one module or folder |
| plain-theory-formatter | study-content-style (Notebook-cell mode, `references/notebook-concepts.md`) | Same job as compress mode, applied to a notebook cell |
| fde-case-study-worksheet-v3 | — (retired) | One-time batch, finished (32 answer keys) |
| add-module | Forward-Deployed-Engineer-Interview-Prep `CLAUDE.md` § "Adding a module, track or scenario" | Repo convention, not a workflow |
| agentic-eval-notebooks | Agent_Evaluation_Demystified `courses/03-agentic-eval-harness/AGENTS.md` (+ `CLAUDE.md` importing it) | Series is complete; only maintenance rules remain |
| dual-format-deliverables | claude.ai Settings → Profile → personal preferences | A standing preference, not a workflow |
| dsa-index-updater's link snippet | link-check (`--html`, case-exact) | One owner for link checking |

## Rename log (2026-10-22)

Renamed for clarity after the necessity audit. Repo copies and SOURCES.md source paths keep the old names.

| Old name | New name |
|---|---|
| dsa-mock | coding-mock-interview |
| fde-system-design-mock | system-design-mock-interview |
| aied-course-cleanup | course-repo-cleanup |
| register-content | dsa-index-updater |
| concept-lab | interactive-concept-explainer |
| dedp-chapter-tutorial | data-engineering-book-tutorial |
| agentic-ai-tutorial-builder | agentic-ai-book-tutorial |
| plain-english-explainer | eval-concept-explainer |
| git-smart-commit | ml-repo-commit |
| website-implementation-plan | site-plan |
