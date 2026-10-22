#!/usr/bin/env python3
"""Check a skill library after any merge, removal or rename. Exit 1 on failure.

- every SKILL.md `name:` matches its folder
- every `<skills-root>/<skill>` reference points at a skill that exists
- every .py file compiles
- (--gone NAME...) no removed or renamed name is still referenced,
  except in README.md and SOURCES.md, which keep history

  python3 validate_library.py LIBRARY [--gone old-name other-old-name]
"""
import argparse
import py_compile
import re
import sys
from pathlib import Path

TEXT = {".md", ".py", ".json", ".txt", ".yaml", ".yml", ".sh"}
HISTORY = {"README.md", "SOURCES.md"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library")
    ap.add_argument("--gone", nargs="*", default=[])
    a = ap.parse_args()
    lib = Path(a.library).expanduser()
    root = lib / "skills" if (lib / "skills").is_dir() else lib  # publishable layout keeps skills in skills/
    files = [f for f in lib.rglob("*") if f.is_file() and ".git" not in f.parts
             and "__pycache__" not in f.parts]
    errors = []

    skills = sorted(p.parent for p in root.glob("*/SKILL.md"))
    for s in skills:
        m = re.search(r"^name:\s*(\S+)", (s / "SKILL.md").read_text(), re.M)
        if not m or m.group(1) != s.name:
            errors.append(f"name mismatch: {s.name}/SKILL.md says {m and m.group(1)}")
        # Strict YAML (the `npx skills` CLI) drops a skill whose plain description contains ": ".
        d = re.search(r"^description:\s*([^\"'>|\s].*)$", (s / "SKILL.md").read_text(), re.M)
        if d and ": " in d.group(1):
            errors.append(f"unquoted ': ' in description (invalid YAML): {s.name}/SKILL.md")

    gone = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, a.gone)) + r")(?![\w-])") if a.gone else None
    for f in files:
        if f.suffix == ".py":
            try:
                py_compile.compile(str(f), doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(f"does not compile: {f.relative_to(lib)}: {e.msg.strip()}")
        if f.suffix not in TEXT:
            continue
        text = f.read_text(errors="replace")
        for ref in set(re.findall(r"<skills-root>/([\w-]+)", text)):
            if not (root / ref).is_dir():
                errors.append(f"missing sibling: {f.relative_to(lib)} -> {ref}")
        if gone and f.name not in HISTORY:
            for m in set(gone.findall(text)):
                errors.append(f"old name still used: {f.relative_to(lib)}: {m}")

    print(f"{len(skills)} skills checked")
    for e in errors:
        print("FAIL", e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
