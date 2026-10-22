#!/usr/bin/env python3
"""Reading time, and what a restyle dropped.

    python3 page_stats.py reading-time PAGE.md
    python3 page_stats.py preserved SOURCE.md RESTYLED.md

`reading-time` prints the minutes to put in the page header. Guessing it is
worse than omitting it: the number is a contract with the reader, and a guessed
one is wrong by minutes on a long page.

`preserved` is the safety net for a restyle. Rewriting prose paragraph by
paragraph should leave every figure, table row and diagram untouched, and this
says whether it did. It reports rather than fails, because a restyle also
removes things on purpose -- a cut section, a framework tour -- and only the
author knows which absences were intended. Read the list; every line should be
one you can explain.

Stdlib only.
"""
import re
import sys

WPM = 200.0                 # prose reading speed
VISUAL_SECONDS = 15.0       # per diagram, and per ~6 table rows


def parts(md):
    fenced = re.findall(r"```(\w*)", md)
    body = re.sub(r"```.*?```", "", md, flags=re.S)
    lines = body.splitlines()
    table = [l for l in lines if l.strip().startswith("|")]
    prose = [l for l in lines if not l.strip().startswith("|")]
    return fenced, table, " ".join(prose)


def reading_time(md):
    fenced, table, prose = parts(md)
    visuals = len(fenced) // 2 + len(table) / 6.0
    return max(1, round(len(prose.split()) / WPM + visuals * VISUAL_SECONDS / 60.0))


def facts(md):
    """The load-bearing details a restyle must not silently lose."""
    fenced, table, _ = parts(md)
    return {
        "numbers": set(re.findall(r"\b\d+\.\d{2}\b", md)),
        "percents": set(re.findall(r"\b\d+(?:\.\d+)?%", md)),
        "code_tokens": set(re.findall(r"`([^`\n]{2,40})`", md)),
        "diagrams": len(fenced) // 2,
        "table_rows": len(table),
        "headings": [h.strip() for h in re.findall(r"^#{1,3}\s+(.*)$", md, re.M)],
    }


def preserved(src_path, new_path):
    a, b = facts(open(src_path).read()), facts(open(new_path).read())
    print("%-14s source -> restyled" % "")
    print("  diagrams     %3d -> %3d %s" % (a["diagrams"], b["diagrams"],
          "" if a["diagrams"] == b["diagrams"] else "  <-- CHECK"))
    print("  table rows   %3d -> %3d %s" % (a["table_rows"], b["table_rows"],
          "" if a["table_rows"] <= b["table_rows"] else "  <-- rows dropped, confirm intended"))
    for label in ("numbers", "percents"):
        missing = sorted(a[label] - b[label])
        print("  %-12s %3d -> %3d %s" % (label, len(a[label]), len(b[label]),
              "" if not missing else "  MISSING: " + ", ".join(missing)))
    gone = sorted(a["code_tokens"] - b["code_tokens"])
    if gone:
        print("\n  code tokens no longer present (%d) -- each should be a deliberate cut:" % len(gone))
        for g in gone:
            print("      %s" % g)
    added = sorted(b["code_tokens"] - a["code_tokens"])
    if added:
        print("\n  code tokens newly introduced (%d):" % len(added))
        for g in added[:20]:
            print("      %s" % g)
    print("\n  Nothing above is an error by itself. Every line should be one you can explain.")


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd = argv[1]
    if cmd == "reading-time":
        print("%d min" % reading_time(open(argv[2]).read()))
    elif cmd == "preserved":
        if len(argv) < 4:
            sys.exit("preserved needs SOURCE.md and RESTYLED.md")
        preserved(argv[2], argv[3])
    else:
        sys.exit(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
