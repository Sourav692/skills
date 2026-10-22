#!/usr/bin/env python3
"""Planner for the neetcode-pattern skill. Run from the repo root. Stdlib only.

  pattern_plan.py list              every DSA type / pattern with build status
  pattern_plan.py plan <query>      one pattern: target folder, problems, blind_75 copy sources
  pattern_plan.py copy <query>      copy that pattern's blind_75 notebooks + HTML in, re-pointing links
  pattern_plan.py index             rewrite neetcode_150/README.md from the CSV + files on disk
  pattern_plan.py docs <outdir>     dump the two NeetCode .docx references to plain text for grepping

<query> is a problem name ("Two Sum"), or type/pattern words ("Trees/BFS", "dynamic knapsack").
"""
import csv
import html
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from itertools import groupby
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "references" / "neetcode150_patterns.csv"
ROWS = list(csv.DictReader(open(CSV, encoding="utf-8")))
TRACK = "neetcode_150"
DOCS = {"archetypes": "NeetCode 150 — Python Pattern Archetypes & Memorizable Templates.docx",
        "red_herrings": "NeetCode 150 — Red Herring Traps & Pattern Disambiguation.docx"}


def files_on_disk():
    out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                         capture_output=True, text=True, check=True).stdout
    return set(filter(None, out.split("\0")))


def blind75_by_stem(files):
    # blind_75 names carry optional "N. " / "N, " prefixes: "5. binary_tree_level_order_traversal.ipynb"
    return {re.sub(r"^\d+[.,]\s*", "", os.path.basename(f))[:-6]: f
            for f in files if f.startswith("blind_75/") and f.endswith(".ipynb")}


def patterns():
    return [(key, list(g)) for key, g in groupby(ROWS, key=lambda r: (r["type"], r["pattern"]))]


def folder(t, p):
    return f"{TRACK}/{t}/{p}"


def lesson_name(p):
    return f"{p.lower()}_lesson.html"


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def resolve(q):
    nq = norm(q)
    hits = {(r["type"], r["pattern"]) for r in ROWS if norm(r["problem"]) == nq}
    if not hits:
        words = nq.split()
        hits = {(r["type"], r["pattern"]) for r in ROWS if all(w in norm(f'{r["type"]} {r["pattern"]}') for w in words)}
    if not hits:
        hits = {(r["type"], r["pattern"]) for r in ROWS if nq in norm(r["problem"])}
    return sorted(hits)


def status(t, p, probs, files):
    d = folder(t, p)
    built = sum(f"{d}/{r['file']}.ipynb" in files and f"{d}/{r['file']}.html" in files for r in probs)
    pages = (f"{d}/README.md" in files) + (f"{d}/{lesson_name(p)}" in files)
    return built, pages


def cmd_list(files):
    for (t, p), probs in patterns():
        built, pages = status(t, p, probs, files)
        mark = "done" if built == len(probs) and pages == 2 else f"{built}/{len(probs)} problems, {pages}/2 pattern pages"
        print(f"{t + '/' + p:<46} {mark}")


def one_pattern(q):
    hits = resolve(q)
    if len(hits) != 1:
        print(f"'{q}' matches {len(hits)} patterns:" if hits else f"'{q}' matches nothing. Run `list`.")
        for t, p in hits:
            print(f"  {t}/{p}")
        sys.exit(2)
    (t, p), = hits
    return t, p, [r for r in ROWS if (r["type"], r["pattern"]) == (t, p)]


def copy_source(r, ext, files, b75):
    src = b75.get(r["file"])
    if not src:
        return None
    copy = src if ext == ".ipynb" else f"{os.path.dirname(src)}/{r['file']}{ext}"  # html never has the "N. " prefix
    return copy if copy in files else None


def cmd_plan(q, files):
    t, p, probs = one_pattern(q)
    d, b75 = folder(t, p), blind75_by_stem(files)
    have = lambda f: "exists" if f in files else "missing"
    print(f"Pattern {t}/{p}  ->  {d}/")
    print(f"  README.md{'':<24}{have(d + '/README.md')}")
    print(f"  {lesson_name(p):<33}{have(d + '/' + lesson_name(p))}")
    for r in probs:
        print(f"\n  {r['order']}. {r['problem']} ({r['difficulty']}, NeetCode #{r['neetcode_no']}) {r['leetcode']}")
        print(f"     signal: {r['signal']}")
        for ext, tool in ((".ipynb", "leetcode-notebook"), (".html", "leetcode-visualizer")):
            dst, src = f"{d}/{r['file']}{ext}", copy_source(r, ext, files, b75)
            how = "exists" if dst in files else f"COPY from {src}" if src else f"NEW via {tool}"
            print(f"     {r['file'] + ext:<52} {how}")


def relabel(h, p):
    """Re-word links to the pattern lesson; the blind_75 text ("All Tree problems") no longer fits."""
    name = p[3:].replace("_", " ")
    def sub(m):
        back = 'class="back"' in m.group(1)
        return m.group(1) + (f"← {name} lesson" if back else f"→ {name}: the pattern lesson and its other problems")
    return re.sub(rf'(<a [^>]*href="{re.escape(lesson_name(p))}"[^>]*>)([^<]*)', sub, h)


def cmd_copy(q, files):
    t, p, probs = one_pattern(q)
    d, b75 = folder(t, p), blind75_by_stem(files)
    os.makedirs(d, exist_ok=True)
    pattern_md = f"**Pattern:** [{p[3:].replace('_', ' ')}](README.md)"
    for r in probs:
        for ext in (".ipynb", ".html"):
            dst, src = f"{d}/{r['file']}{ext}", copy_source(r, ext, files, b75)
            if dst in files or not src:
                continue
            shutil.copyfile(src, dst)
            if ext == ".html":
                # blind_75 pages link their topic hub; the pattern lesson is the hub here
                h = Path(dst).read_text(encoding="utf-8")
                h = re.sub(r'href="(?:\.\./)?(?:index|patterns)\.html"', f'href="{lesson_name(p)}"', h)
                h = relabel(h, p)
                Path(dst).write_text(h, encoding="utf-8")
            else:
                nb = json.load(open(dst, encoding="utf-8"))
                head = "".join(nb["cells"][0]["source"])
                new = re.sub(r"\*\*Topic:\*\* [^·\n]*", f"**Topic:** {t.replace('_', ' ')} · {pattern_md} ", head, count=1)
                if new == head:
                    print(f"  ! no **Topic:** in {dst} header; add `{pattern_md}` by hand")
                nb["cells"][0]["source"] = new.splitlines(keepends=True)
                Path(dst).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"copied {src} -> {dst}")


def link(text, path, files, base):
    return f"[{text}]({path})" if f"{base}/{path}" in files else "—"


def cmd_index(files):
    pats = patterns()
    done = sum(status(t, p, probs, files)[0] for (t, p), probs in pats)
    full = sum(status(t, p, probs, files) == (len(probs), 2) for (t, p), probs in pats)
    out = ["# NeetCode 150 — pattern-wise", "",
           "<!-- Generated by <skills-root>/neetcode-pattern/scripts/pattern_plan.py index. Do not edit by hand. -->", "",
           "The 150 problems grouped by DSA type, then by pattern. Each pattern folder has a `README.md` that explains "
           "the pattern, an interactive `NN_pattern_lesson.html`, and for each problem a notebook (brute force → optimal, "
           "asserts, benchmark) plus an interactive step-through HTML. Build one pattern at a time with `/neetcode-pattern <pattern>`.",
           "", f"Built: **{done} / {len(ROWS)}** problems, **{full} / {len(pats)}** patterns complete. "
           "Also here: the [question tracker](index.html) and [reference docs](docs/).", ""]
    for t, group in groupby(pats, key=lambda x: x[0][0]):
        out += [f"## {t.replace('_', ' ')}", "", "| Pattern | # | Problem | Difficulty | Notebook | Interactive |",
                "|---|---|---|---|---|---|"]
        for (_, p), probs in group:
            for i, r in enumerate(probs):
                cell = ""
                if i == 0:
                    name = p.replace("_", " ")
                    cell = link(name, f"{t}/{p}/README.md", files, TRACK)
                    cell = name if cell == "—" else cell
                    lesson = link("lesson", f"{t}/{p}/{lesson_name(p)}", files, TRACK)
                    cell += "" if lesson == "—" else f" · {lesson}"
                nb = link("ipynb", f"{t}/{p}/{r['file']}.ipynb", files, TRACK)
                ht = link("html", f"{t}/{p}/{r['file']}.html", files, TRACK)
                out.append(f"| {cell} | {r['neetcode_no']} | [{r['problem']}]({r['leetcode']}) | {r['difficulty']} | {nb} | {ht} |")
        out.append("")
    Path(TRACK, "README.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {TRACK}/README.md: {done}/{len(ROWS)} problems, {full}/{len(pats)} patterns complete")


def cmd_docs(outdir):
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DOCS.items():
        xml = zipfile.ZipFile(Path(TRACK, "docs", fn)).read("word/document.xml").decode()
        lines, prev = [], None
        for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
            t = html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))).strip()
            if t and t != prev:  # the docx repeats many paragraphs back to back
                lines.append(t)
            prev = t or prev
        Path(outdir, f"{name}.txt").write_text("\n".join(lines), encoding="utf-8")
        print(f"{outdir}/{name}.txt  ({len(lines)} lines)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("list", "plan", "copy", "index", "docs") or (a[0] in ("plan", "copy", "docs") and len(a) < 2):
        sys.exit(__doc__.strip())
    if a[0] == "docs":
        cmd_docs(a[1])
    elif a[0] in ("plan", "copy"):
        {"plan": cmd_plan, "copy": cmd_copy}[a[0]](" ".join(a[1:]), files_on_disk())
    else:
        {"list": cmd_list, "index": cmd_index}[a[0]](files_on_disk())
