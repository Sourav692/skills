# Audit rubrics

This file holds the criteria for each audit phase in `SKILL.md`. Every audit is read-only and ends in a table for the user to approve.

## Where skills load from (Claude Code)

| Location | Loaded? |
|---|---|
| `~/.claude/skills/<name>/` (often symlinks to `~/.agents/skills/`) | Every session |
| Plugins (`~/.claude/plugins/installed_plugins.json`) | Every session |
| claude.ai skills (`~/.claude/skills/synced/<uuid>/`, read-only cache) | Every session, as `anthropic-skills:*` |
| `<repo>/.claude/skills/<name>/` | Only in that repo |
| `~/.cursor`, `~/Downloads`, `.agents/skills`, nested `skills/` folders | Never |

A skill library outside these locations is a source of truth, not a load path. Install from it by symlinking a folder into `~/.claude/skills`, by copying it into a repo's `.claude/skills`, or by uploading a zip to claude.ai.

## Ownership

| Evidence | Means |
|---|---|
| Git author of the commit that added `SKILL.md` = the user's email | Theirs |
| claude.ai manifest `creatorType: user` (`source: custom`) | Theirs |
| `creatorType: anthropic`, `source: anthropic-example` | Built-in |
| `~/.agents/.skill-lock.json` source repo, plugin caches, vendored sets | Third-party |
| A teammate's repo, even if cloned locally | Not theirs |

Only skills the user owns are in scope. Never rename, merge or delete built-in, plugin or third-party skills.

## Variants (same name, different content)

Put each copy in `_variants/<name>__<tag>/`. Diff them, then pick:
1. The superset: the copy that contains everything the others do.
2. If no copy is a superset, the newest one (by git date, not mtime), plus the unique parts of the others merged in. List each merged part.
3. A copy built for another runtime (for example, one that uses claude.ai-only tools) stays as its own skill, or becomes a mode of the chosen skill. It is not a variant.

## Overlap audit

For every pair of skills that share inputs or outputs, ask:

| Finding | Action |
|---|---|
| Identical files | Keep one. Remove the other |
| One is a subset of the other (a "bundle" already contains it) | Remove the subset |
| Same job, different input (for example, a page vs a notebook cell) | Merge as a mode of one skill |
| Two copies of a shared contract (a format, a rubric) | One owner holds it. The others point there with `<skills-root>/<owner>/...` |
| Pipeline neighbours (A's output is B's input) | Keep both. Each one names the other at its boundary |

A skill does one job. "One owner per job" also covers snippets: if a check exists in one skill, other skills call that skill instead of copying the code.

## Necessity audit (run before renaming)

Collect usage evidence first:
- **Claude Code transcripts:** `~/.claude/projects/*/*.jsonl`. Count `Base directory for this skill: .../<name>`, `<command-name>/<name>` and Skill tool calls with `"skill": "<name>"`.
- **Cursor transcripts,** if Cursor is used.
- **claude.ai usage isn't visible.** Say so, and don't count it as zero.
- **Target check:** do the repos, folders or files that the skill works on still exist? Check git history for retirements and splits.

| Class | When |
|---|---|
| KEEP | Recurring job, target exists, no overlap left |
| MERGE | Overlaps another skill (see the overlap table) |
| CONVERT | A repo convention or a standing preference, not a workflow. Move it to that repo's `CLAUDE.md`/`AGENTS.md`, or to the claude.ai personal preferences |
| REMOVE | A one-time job that is finished, or its target was retired |
| REVIEW | The evidence conflicts. Give your lean and the one fact that would decide it |

Split the result into a high-confidence group and the subjective items. List the subjective items one by one, so the user can approve the high-confidence group in one go.

## Rename audit

Rename only when a name is vague, misleading, uses an unexplained abbreviation, carries a version number, or breaks its family's pattern. Rules:
- Lowercase kebab-case. Names must not contain version numbers or private abbreviations.
- Say what the skill acts on and what it produces: `course-repo-cleanup`, `dsa-index-updater`.
- Families share a prefix or a suffix: `site-*`, `dsa-*`, `*-mock-interview`, `*-book-tutorial`.
- Pairs read together: `site-plan`, then `site-plan-to-tasks`.
- Do not rename runtime skills that an app loads by name.

The table columns are: Current, Proposed, Purpose, Reason. Also list what stays as is, and why.

## Done means

- The validator passes: `validate_library.py LIBRARY --gone <removed and old names>`.
- Every bundled script you touched has run once on a real input.
- One commit per phase, each with a tag that you can roll back to.
- The report lists everything the user must do by hand: claude.ai uploads, deletes and preferences, uncommitted repo edits, and old repo copies to delete.
