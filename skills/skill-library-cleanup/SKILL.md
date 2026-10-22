---
name: skill-library-cleanup
description: Use when the user wants to find, list, organize, deduplicate, consolidate, prune or rename their own Claude/agent skills (SKILL.md files) across ~/.claude, repos, Downloads or claude.ai; when they ask "which skills do I have", "are any of my skills overlapping", "which skills can I delete", or "rename my skills"; or when the same skill exists in several places with different content.
---

# Skill Library Cleanup

Turn skills scattered across folders into one canonical library: every skill the user owns appears once, does one job, has a clear name, and has a recorded source. The user must approve every change. All work happens inside the library, which is a git repo, so every phase can be undone.

## Ground rules

- **Audits are read-only.** Each audit ends with a table and stops until the user approves. Apply only what they approved, nothing more.
- **Only the user's own skills are in scope.** Never rename, merge or delete built-in, plugin, vendored or teammate skills. See "Ownership" in `references/audit-rubrics.md`.
- **Instructions stay unchanged.** Renames and moves touch only names, paths and cross-references.
- **Leave user repos alone.** Edit only the library. If a repo needs an edit (a convention moved into its `CLAUDE.md`), leave the change uncommitted for the user to review. Never delete repo copies of skills; tell the user which ones they can delete.
- **Order:** consolidate, then prune, then rename. Never rename a skill the next audit might remove.

## Phases

1. **Inventory (read-only).** Run `python3 <skills-root>/skill-library-cleanup/scripts/inventory.py ROOT... --author EMAIL`. Group the results by function, give a one-line description for each skill, and mark which ones the user owns. Say which locations actually load (see "Where skills load from" in the rubrics).
2. **Collect.** Copy the skills the user owns into the library, one folder per skill under `skills/` (`skills/<name>/SKILL.md`), so the library can be published as is.
   - Run `git init` in the library and commit a snapshot.
   - Write `SOURCES.md` with the columns skill, chosen copy, source path and date.
   - When a skill has several variants, put the copies in `_variants/` and compare them (see the rubrics). Recommend one copy, apply the user's pick, then delete `_variants/`.
3. **Make paths portable.** Replace repo paths (`.claude/skills/x/...`, `plugins/...`) with `<skills-root>/<skill>/...`. In Python, find sibling skills with `Path(__file__).resolve().parents[2]`.
4. **Catalog.** Write `README.md`: one table per function group, with the columns Skill, What it does, Global?, Scope. Add a "Consolidation log" table (Removed, Now covered by, Why) and a "Rename log" table.
5. **Overlap audit.** Fill in the overlap table from the rubrics. Wait for approval. Merge the approved skills, then validate and commit.
6. **Coverage check.** Confirm that every owned skill under each repo's `.claude/skills` is either in the library or listed as intentionally excluded.
7. **Necessity audit.** Gather usage evidence, then classify each skill as KEEP, MERGE, CONVERT, REMOVE or REVIEW. Present a high-confidence group plus the subjective items. Before applying, run `git tag pre-necessity-audit`, then apply, validate and commit.
8. **Rename audit.** Fill in the rename table from the rubrics. Wait for approval. Before applying, run `git tag pre-rename`, then run `python3 <skills-root>/skill-library-cleanup/scripts/rename_skills.py LIBRARY OLD=NEW ...` (try `--dry-run` first). Add the renames to the README's "Rename log", then validate and commit.
9. **claude.ai.** Skills can't be uploaded from the CLI, and `~/.claude/skills/synced/` is a read-only cache, so never edit it. For each changed or renamed skill that lives on claude.ai, build `<name>.zip` with `name/SKILL.md` at the root of the zip. Put the zips in `~/Downloads/claude-ai-skill-updates/`, with a `README.txt` listing what to upload, what to delete (renames: upload the new zip first, then delete the old name) and any preference text to paste.

10. **Publish (optional).** Make the library installable with `npx skills add OWNER/REPO` and as a Claude Code plugin:
    - Keep `skills/` flat; the installer flattens skills anyway, and `<skills-root>` siblings must sit side by side. Put categories in the README.
    - Add `.claude-plugin/plugin.json` (plugin name, version, author, repository, license) and `.claude-plugin/marketplace.json` (one plugin with `"source": "./"`). Run `claude plugin validate .`.
    - In the README, show install commands for one skill (`--skill NAME`), for all of them (`--skill '*'`), for listing (`--list`) and for the plugin. Add an "Install these together" table for every `<skills-root>` dependency.
    - Before the first push, scan for secrets, real emails, absolute home paths and personal data, and show the user what you find. Keep anything not meant to be public out of the history: publish an orphan `main` and keep the old history on a local branch.
    - Creating the repo and pushing are outward-facing. Confirm with the user first.
    - Test from a scratch folder: `--list`, install one skill, install all of them, and run one sibling-script reference.

After every phase that changes files, run:

```bash
python3 <skills-root>/skill-library-cleanup/scripts/validate_library.py LIBRARY --gone OLD_OR_REMOVED_NAMES...
```

It checks that each `name:` matches its folder, that every `<skills-root>` reference resolves, that all scripts compile, and that no old name is left. Also run each script you touched on a real input once.

## Quick reference

| Need | Use |
|---|---|
| Who owns a skill | Git author of the commit that added it, or `creatorType` in the claude.ai manifest |
| Is it used | Search the transcripts in `~/.claude/projects/*/*.jsonl` for `Base directory for this skill` |
| Two skills share one contract | One owner keeps it; the others point to `<skills-root>/<owner>/...` |
| A skill that is a convention, not a workflow | CONVERT it into the repo's `CLAUDE.md`/`AGENTS.md` |
| A standing preference on claude.ai | CONVERT it into a personal-preference text the user pastes |
| Undo a phase | `git reset --hard <tag>` in the library, after confirming with the user |

## Common mistakes

- **Counting copies as skills.** Skip `.venv/`, `site-packages/`, `.claude/worktrees/` and `tests/fixtures/`, and dedupe by `name:`. The inventory script does both.
- **Blind find-and-replace when renaming.** A short name can also be an ordinary word or a field value, for example a task type called `explainer`. Match whole names only, and read the dry-run list.
- **Rewriting the source column in SOURCES.md.** Its paths record where each copy came from, so they keep the old names.
- **Moving a claude.ai-only skill into `CLAUDE.md`.** If the skill uses claude.ai tools, it belongs in the claude.ai preferences instead.
- **Merging two skills that both have gates,** such that one calls the other and the user is asked to approve the same thing twice. Draw the boundary first, or fold one skill into the other.
- **zsh:** `for x in $LIST` loops only once, and `$n__x` is read as one variable name. Use arrays or Python, and write `${n}__${tag}`.
