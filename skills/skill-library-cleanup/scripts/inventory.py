#!/usr/bin/env python3
"""Find every SKILL.md under the given roots and report who owns each one.

Read-only. Dedupes by `name:`, flags variants (same name, different content),
and marks ownership from git authorship or the claude.ai sync manifest.

  python3 inventory.py ~/.claude ~/Github_Repos ~/Downloads --author you@example.com
  python3 inventory.py ROOT... --json > inventory.json
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
from collections import defaultdict
from pathlib import Path

# Copies that inflate the count without being anyone's real skill.
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "site-packages", "__pycache__"}
SKIP_PARTS = ("/.claude/worktrees/", "/tests/fixtures/")


def frontmatter(text):
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    block = m.group(1) if m else ""
    name = re.search(r"^name:\s*(.+)$", block, re.M)
    desc = re.search(r"^description:\s*(?:>-?\s*\n)?\s*(.+)$", block, re.M)
    return (name.group(1).strip().strip("\"'") if name else None,
            desc.group(1).strip().strip("\"'") if desc else "")


def git_author(path):
    """Email of the commit that added the file, or None outside git."""
    r = subprocess.run(
        ["git", "-C", str(path.parent), "log", "--diff-filter=A", "--format=%ae", "--", path.name],
        capture_output=True, text=True)
    lines = r.stdout.split()
    return lines[-1] if r.returncode == 0 and lines else None


def synced_owners(roots):
    """claude.ai sync manifests: name -> 'user' | 'anthropic' | ..."""
    owners = {}
    for root in roots:
        for mf in Path(root).expanduser().rglob("manifest.json"):
            if mf.parent.parent.name != "synced":
                continue
            for s in json.loads(mf.read_text()).get("skills", []):
                owners[s["name"]] = s.get("creatorType") or s.get("source")
    return owners


def walk(root):
    seen = set()
    for dirpath, dirs, files in os.walk(Path(root).expanduser(), followlinks=True):
        real = os.path.realpath(dirpath)
        if real in seen:
            dirs[:] = []
            continue
        seen.add(real)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if "SKILL.md" in files and not any(p in dirpath + "/" for p in SKIP_PARTS):
            yield Path(dirpath) / "SKILL.md"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--author", help="your git email; marks skills you created")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    synced = synced_owners(a.roots)
    by_name = defaultdict(list)
    for p in (p for r in a.roots for p in walk(r)):
        text = p.read_text(errors="replace")
        name, desc = frontmatter(text)
        name = name or p.parent.name
        author = git_author(p)
        if "/skills/synced/" in str(p):
            owner = "yours" if synced.get(name) == "user" else synced.get(name, "?")
        elif a.author and author == a.author:
            owner = "yours"
        else:
            owner = author or "?"
        by_name[name].append({
            "path": str(p.parent), "owner": owner, "desc": desc[:120],
            "sha": hashlib.sha1(text.encode()).hexdigest()[:8],
            "mtime": int(p.stat().st_mtime),
        })

    if a.json:
        print(json.dumps(by_name, indent=2))
        return
    print("| Skill | Owner | Copies | Variants | Description |\n|---|---|---|---|---|")
    for name in sorted(by_name):
        c = by_name[name]
        owner = "yours" if any(x["owner"] == "yours" for x in c) else c[0]["owner"]
        print(f"| {name} | {owner} | {len(c)} | {len({x['sha'] for x in c})} | {c[0]['desc']} |")


if __name__ == "__main__":
    main()
