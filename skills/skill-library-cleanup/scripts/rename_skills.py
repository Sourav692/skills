#!/usr/bin/env python3
"""Rename skills inside a skill library (a git repo of skill folders).

For each OLD=NEW pair: `git mv OLD NEW`, then replace OLD with NEW as a whole
name (not inside longer names) in every tracked text file. SOURCES.md keeps its
source-path column, because those paths record where a copy came from.

  python3 rename_skills.py LIBRARY old-name=new-name other-old=other-new
  python3 rename_skills.py LIBRARY ... --dry-run
"""
import argparse
import re
import subprocess
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library")
    ap.add_argument("pairs", nargs="+", metavar="OLD=NEW")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    lib = Path(a.library).expanduser().resolve()
    ren = dict(p.split("=", 1) for p in a.pairs)
    root = lib / "skills" if (lib / "skills").is_dir() else lib  # publishable layout keeps skills in skills/
    for old, new in ren.items():
        if not (root / old).is_dir():
            raise SystemExit(f"no skill folder: {old}")
        if (root / new).exists():
            raise SystemExit(f"target exists: {new}")
    pat = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, ren)) + r")(?![\w-])")
    sub = lambda s: pat.sub(lambda m: ren[m.group(1)], s)

    git = lambda *args: subprocess.run(["git", "-C", str(lib), *args], check=True,
                                       capture_output=True, text=True).stdout
    if not a.dry_run:
        for old, new in ren.items():
            git("mv", str(root / old), str(root / new))

    for f in filter(None, git("ls-files").split("\n")):
        p = lib / f
        try:
            text = p.read_text()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        if p.name == "SOURCES.md":
            # Only the first cell (the skill name) of each table row.
            new = "\n".join(
                "|".join([c[0], sub(c[1]), *c[2:]]) if (c := line.split("|"))[0] == "" and len(c) > 2 else line
                for line in text.split("\n"))
        else:
            new = sub(text)
        if new != text:
            print(("would edit " if a.dry_run else "edited ") + f)
            if not a.dry_run:
                p.write_text(new)


if __name__ == "__main__":
    main()
