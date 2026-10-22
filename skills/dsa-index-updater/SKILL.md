---
name: dsa-index-updater
description: After adding or renaming a Blind 75 problem or a deep_dive topic, update every index that should link to it (topic README/index.html, track README tables and counts, deep_dive/index.html, root README). Use when new notebooks/HTML lessons were created, files were renamed/moved, or the user says "register", "link it up", "update the indexes".
---

> **Paths:** `<skills-root>` means the folder that holds this skill — the parent of its base directory (e.g. `~/.claude/skills`, or a repo's `.claude/skills`). Sibling skills referenced below live there too.

Make new or moved content reachable from every index. Target: $ARGUMENTS (a path, or empty = everything changed per `git status`).

1. **Find what changed.** `git status --porcelain` plus the target path. List new/renamed `.ipynb`, `.html`, `_explained.md`, and folders. Quote paths — they contain spaces.

2. **Blind 75 problem** (`blind_75/<Topic>/[Group N_<pattern>/]<problem>.*`):
   - `<Topic>/README.md`: add the problem under its group/pattern section, matching neighbouring entries.
   - `<Topic>/index.html`: add a card/link for `<problem>.html`, copying an existing card's markup exactly.
   - `<Topic>/patterns.html`: add the problem to its pattern's list if the page lists problems per pattern.
   - `blind_75/README.md`: bump the `N problems` count in the Topics table; add a pattern to "Core patterns" only if genuinely new.
   - `blind_75/index.html`: update counts/links if it lists them.

3. **Deep Dive topic** (`deep_dive/NN_Title_Case/`):
   - `deep_dive/README.md`: add a row to the right track table: `| NN | [Title](NN_X/README.md) | what you'll learn | [open](NN_X/NN_x_lesson.html) |`.
   - `deep_dive/index.html`: add the topic card, copying an existing card's markup.
   - Root `README.md`: update the "NN numbered topics" count in the Tracks table if it changed.

4. **Verify links — case-sensitively.** Run the `link-check` skill's script on every index you edited:
   ```bash
   python3 <skills-root>/link-check/scripts/check_links.py --html "blind_75/README.md" OTHER_EDITED_FILES
   ```
   It checks markdown links and `href`s case-exactly against the paths git knows (macOS ignores case;
   GitHub does not). Fix every broken link you introduced; report pre-existing ones. A folder whose case
   differs only on disk (git has `Docs/`, disk shows `docs/`) needs a two-step rename:
   `git mv Docs tmp && git mv tmp docs`.

4b. **NeetCode 150** (`neetcode_150/<Type>/<NN_Pattern>/`): run `python3 <skills-root>/neetcode-pattern/scripts/pattern_plan.py index` — it regenerates `neetcode_150/README.md` from the CSV and the files on disk. Never hand-edit that README.

4c. **Anything else** (a new folder): update the nearest `README.md` / `index.html` above the new file that lists its siblings, copying the existing entry format. If none exists, don't invent one — report it.
   - `outputs/` is a staging area and is not indexed. When the user moves `outputs/<slug>/` into a track, run this skill on the new location.

5. Report: one line per index edited, plus any index you deliberately skipped and why. Do not commit.
