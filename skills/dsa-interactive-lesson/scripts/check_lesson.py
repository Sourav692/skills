#!/usr/bin/env python3
"""Structural check for a dsa-interactive-lesson HTML page.

Usage: python3 check_lesson.py lesson.html [more.html ...]
Exit 0 = every check passed; 1 = at least one FAIL (printed).
Stdlib only. Visual layout still needs a screenshot pass (see SKILL.md step 6).
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr", "path", "circle", "rect", "line", "polygon",
        "polyline", "ellipse", "stop", "use"}
# Required sections, matched case-insensitively against <h2> text.
# Each entry: any one alternative must appear ("What is X?" or "What are X and Y?").
REQUIRED_H2 = [("why",), ("what is", "what are"), ("thinking",), ("method 1",), ("edge case",),
               ("interview",), ("mistake",), ("practice",), ("takeaway",)]


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.h2, self._in_h2 = [], [], [], False

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self._in_h2, self._buf = True, ""
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag == "h2" and self._in_h2:
            self.h2.append(self._buf.strip())
            self._in_h2 = False
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif any(t == tag for t, _ in self.stack):
            while self.stack and self.stack[-1][0] != tag:
                t, line = self.stack.pop()
                self.errors.append(f"<{t}> opened on line {line} never closed")
            self.stack.pop()
        else:
            self.errors.append(f"stray </{tag}> on line {self.getpos()[0]}")

    def handle_data(self, data):
        if self._in_h2:
            self._buf += data


def check(path):
    html = Path(path).read_text(encoding="utf-8")
    fails = []

    ext = re.findall(r'(?:src|href)\s*=\s*"(https?:[^"]+)"|@import\s+url\(|url\((https?:[^)]+)\)', html)
    if ext:
        fails.append(f"external resources (must be fully offline): {ext[:3]}")

    buttons = re.findall(r"<button\b[^>]*>", html)
    untyped = [b for b in buttons if 'type="button"' not in b]
    if untyped:
        fails.append(f'{len(untyped)} <button> without type="button", e.g. {untyped[0]}')

    if "DOMContentLoaded" not in html:
        fails.append("trace script not wrapped in DOMContentLoaded")

    prefixes = set(re.findall(r'id="([\w-]+)-prev"', html))
    if not prefixes:
        fails.append("no interactive trace controls (<prefix>-prev/-next/-play/-reset ids)")
    for p in sorted(prefixes):
        missing = [s for s in ("next", "play", "reset") if f'id="{p}-{s}"' not in html]
        if missing:
            fails.append(f"trace '{p}' is missing controls: {missing}")

    if "data-line=" not in html:
        fails.append('no synced code lines (<span class="code-line" data-line="N">)')

    if len(re.findall(r"<details\b", html)) < 3:
        fails.append("fewer than 3 practice questions (<details> blocks)")

    parser = Balance()
    parser.feed(html)
    parser.close()
    fails += parser.errors[:5]
    fails += [f"<{t}> opened on line {line} never closed" for t, line in parser.stack[:5]]

    h2 = " | ".join(parser.h2).lower()
    missing_h2 = [alts[0] for alts in REQUIRED_H2 if not any(a in h2 for a in alts)]
    if missing_h2:
        fails.append(f"missing required sections (h2 containing): {missing_h2}")

    print(f"{'PASS' if not fails else 'FAIL'}  {path}  ({len(parser.h2)} sections, "
          f"{len(prefixes)} traces: {', '.join(sorted(prefixes)) or '-'})")
    for f in fails:
        print(f"  - {f}")
    return not fails


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    sys.exit(0 if all([check(p) for p in sys.argv[1:]]) else 1)
