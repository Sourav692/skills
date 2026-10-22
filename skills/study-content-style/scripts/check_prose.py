#!/usr/bin/env python3
"""Check a Markdown tutorial page against the study-content-style prose-mode targets.

    python3 check_prose.py PAGE.md [PAGE.md ...]      summary, exit 1 on any fail
    python3 check_prose.py --verbose PAGE.md          also list offending sentences
    python3 check_prose.py --tool-free PAGE.md        also fail on API names in prose
    python3 check_prose.py --tool-free --allow=expected_output,GEval PAGE.md

Why this exists: structural rules ("every heading starts with a verb") verify
themselves -- you can see at a glance whether they hold. Rhythm rules do not, so
they get skipped silently and the page ships reading exactly like the draft it
replaced. These thresholds come from measuring a reference page in the target
style; they are a floor to clear, not a style in themselves.

Stdlib only. Measures body prose: fenced blocks, indented blocks, tables,
blockquotes, headings and list items are all excluded, so code and reference
material do not distort the sentence statistics.
"""
import re
import statistics
import sys

# Targets, measured off a reference page in this style (mean 13.4 words,
# median 13, 46% under 12 words, 4% over 30, zero second person). They are set
# looser than the reference: a deep consolidation page carries more qualifying
# clauses than a six-minute chapter and should not be flattened to match.
TARGETS = {
    "median_sentence_words": (16, "at most"),
    "pct_over_30_words": (10, "at most"),
    "pct_under_12_words": (35, "at least"),
    "you_per_1000": (2.0, "at most"),
}

# A heading is checked for what makes it a LABEL, not for membership of a verb
# list. Listing verbs never converges -- every new page invents a fresh one, and
# the check then fails on good headings. The closed set is the other side: the
# handful of openers that mean a heading is naming a topic rather than giving an
# instruction. Gerunds ("Building the Harness") are labels too, which is why a
# leading -ing word counts.
LABEL_OPENER = re.compile(
    r"""^(?:\d+[\.\)]\s+)?             # optional section number
        (?:The|A|An|Why|What|How|When|Where|Which|Who|Whose|Our|Your|Its|This|
           That|These|Those|Some|More|Introduction|Overview|Summary|Background|
           Basics|Fundamentals|Notes|Appendix|Glossary|Conclusion)\b
        |^(?:\d+[\.\)]\s+)?\w+ing\b  # gerund: "Building ...", "Writing ..."
    """, re.X | re.I)

YOU = re.compile(r"\b[Yy]ou(?:r|rs|'re|'ve|'ll)?\b")
QUOTED = re.compile(r'"[^"]{0,200}"')


def unquoted(text):
    """Text with double-quoted spans removed.

    Second person inside a quotation is the example speaking, not the author
    addressing the reader: *"Your flight is booked!"* is the product's voice.
    Counting it pushes a page toward rewriting its own worked examples, which
    is the opposite of what the voice rule is for.
    """
    return QUOTED.sub(" ", text)
CLOSERS = ("Key Takeaways", "Check Yourself", "References", "Summary")


API_IDENT = re.compile(r"`([A-Za-z_][A-Za-z0-9_.]*)`")
CAMEL = re.compile(r"^[a-z]+(?:[A-Z][a-z0-9]*)+$|^[A-Z][a-z0-9]*(?:[A-Z][a-z0-9]*)+$")
SNAKE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")
DATA_LABEL = re.compile(r"^[a-z]+_\d+$")


def api_identifiers(blocks, allow=()):
    """Backticked CamelCase / snake_case names in prose -- i.e. API surface.

    Not every such name is noise. Some are the shared vocabulary of a field and
    genuinely help a reader (`expected_output` says what the field holds better
    than "the reference answer" does on the fifth mention). What does not belong
    is a tour of one framework's API: class inventories, constructor arguments,
    sync-vs-async mechanics, library-versus-library comparisons.

    No regex can tell those apart, so this does not try. It lists every
    code-shaped name in prose and expects the author to declare the intended
    vocabulary via --allow. Declaring it IS the editorial decision, made once
    and visible in the command rather than left implicit in the draft.
    """
    found = []
    for b in blocks:
        for ident in API_IDENT.findall(b):
            if ident in allow:
                continue                      # declared page vocabulary
            if DATA_LABEL.match(ident):
                continue                      # chunk_1, doc_3: example data, not API
            if CAMEL.match(ident) or SNAKE.match(ident) or "." in ident:
                found.append(ident)
    return sorted(set(found))


def has_tagline(md):
    """A one-sentence italic paragraph directly under the H1 title.

    Checked as a paragraph rather than a line: the tagline wraps, and matching a
    single line silently passes on any stray italic elsewhere in the page (a
    source pointer, a caption) while the real tagline is missing.
    """
    m = re.search(r"^#\s+.*$", md, re.M)
    if not m:
        return False
    after = md[m.end():].lstrip("\n")
    para = after.split("\n\n", 1)[0].strip()
    return para.startswith("*") and para.endswith("*") and not para.startswith("**")


def split_page(text):
    """Return (body_markdown, full_markdown) with fenced blocks removed."""
    stripped = re.sub(r"```.*?```", "", text, flags=re.S)
    body = re.split(r"^##\s+(?:%s)" % "|".join(CLOSERS), stripped, flags=re.M)[0]
    return body, stripped


def prose_blocks(md):
    """Body prose, as a list of paragraphs.

    Paragraphs are kept apart rather than joined into one string: a label line
    that ends without a full stop ("**The four metrics:**") would otherwise be
    glued to the paragraph after it and counted as one enormous sentence.
    Tables, quotes, headings, lists and indented code are dropped, so code and
    reference material cannot distort the sentence statistics.
    """
    blocks, cur = [], []
    for line in md.splitlines():
        if not line.strip():
            if cur:
                blocks.append(" ".join(cur))
                cur = []
            continue
        if line.startswith("    ") or line.startswith("\t") \
           or line.lstrip().startswith(("|", ">", "#")) \
           or re.match(r"^\s*(?:[-*+]\s|\d+[\.\)]\s)", line):
            if cur:
                blocks.append(" ".join(cur))
                cur = []
            continue
        cur.append(line.strip())
    if cur:
        blocks.append(" ".join(cur))
    return blocks


def sentences(blocks):
    """Sentences within each paragraph; a paragraph end is a sentence end."""
    out = []
    for b in blocks:
        for part in re.split(r"(?<=[.?!])\s+", b):
            if len(part.split()) > 2:
                out.append(part.strip())
    return out


def measure(path, allow=()):
    text = open(path, encoding="utf-8").read()
    body, full = split_page(text)
    blocks = prose_blocks(body)
    prose = " ".join(blocks)
    sents = sentences(blocks)
    if not sents:
        return None
    lens = [len(s.split()) for s in sents]
    words = len(prose.split())

    heads = [h.strip() for h in re.findall(r"^##\s+(.*)$", full, re.M)]
    core = [h for h in heads if h.strip() not in CLOSERS]
    non_imp = [h for h in core if LABEL_OPENER.match(re.sub(r"[*`]", "", h).strip())]

    bullets = len(re.findall(r"^\s*[-*+]\s", body, re.M))
    paras = len(blocks)

    return {
        "path": path,
        "words": words,
        "sentences": len(sents),
        "mean_sentence_words": statistics.mean(lens),
        "median_sentence_words": statistics.median(lens),
        "pct_over_30_words": 100 * sum(1 for n in lens if n > 30) / len(lens),
        "pct_under_12_words": 100 * sum(1 for n in lens if n < 12) / len(lens),
        "you_per_1000": 1000 * len(YOU.findall(unquoted(prose))) / max(words, 1),
        "sections": len(core),
        "non_imperative_headings": non_imp,
        "bullets": bullets,
        "paragraphs": paras,
        "has_tagline": has_tagline(full),
        "has_reading_time": bool(re.search(r"\b\d+\s*min\b", full)),
        "has_takeaways": "## Key Takeaways" in full,
        "long_sentences": sorted(
            [s for s in sents if len(s.split()) > 30], key=lambda s: -len(s.split())
        ),
        "you_sentences": [s for s in sents if YOU.search(unquoted(s))],
        "api_identifiers": api_identifiers(blocks, allow),
    }


def report(m, verbose=False, tool_free=False):
    print("\n%s" % m["path"])
    print("  %d words of body prose, %d sentences, %d sections"
          % (m["words"], m["sentences"], m["sections"]))
    ok = True
    for key, (limit, direction) in TARGETS.items():
        val = m[key]
        good = val <= limit if direction == "at most" else val >= limit
        ok &= good
        print("  %-24s %6.1f  (%s %s)  %s"
              % (key, val, direction, limit, "PASS" if good else "FAIL"))

    if m["non_imperative_headings"]:
        ok = False
        print("  headings not led by a verb   FAIL")
        for h in m["non_imperative_headings"]:
            print("      - %s" % h)
    else:
        print("  %-24s %6d  (all verb-led)      PASS"
              % ("imperative headings", m["sections"]))

    if tool_free:
        if m["api_identifiers"]:
            ok = False
            print("  undeclared API names        FAIL -- %d found (allow them or cut them)"
                  % len(m["api_identifiers"]))
            print("      %s" % ", ".join(m["api_identifiers"][:14]))
        else:
            print("  %-24s %6d  (all declared)      PASS" % ("undeclared API names", 0))

    if m["bullets"] > m["paragraphs"]:
        ok = False
        print("  bullets(%d) > paragraphs(%d)   FAIL -- this is a deck, not a lesson"
              % (m["bullets"], m["paragraphs"]))

    for label, key in (("tagline", "has_tagline"),
                       ("reading time", "has_reading_time"),
                       ("Key Takeaways", "has_takeaways")):
        if not m[key]:
            ok = False
            print("  missing %s   FAIL" % label)

    if verbose:
        if m["long_sentences"]:
            print("\n  -- sentences over 30 words (split these) --")
            for s in m["long_sentences"][:12]:
                print("   %3d  %s" % (len(s.split()), s[:150]))
        if m["you_sentences"]:
            print("\n  -- second person (convert to imperative) --")
            for s in m["you_sentences"][:12]:
                print("        %s" % s[:150])
    return ok


def main(argv):
    verbose = "--verbose" in argv or "-v" in argv
    tool_free = "--tool-free" in argv
    allow = set()
    for a in argv:
        if a.startswith("--allow="):
            allow = {x.strip() for x in a.split("=", 1)[1].split(",") if x.strip()}
    paths = [a for a in argv[1:] if not a.startswith("-")]
    if not paths:
        sys.exit(__doc__)
    allok = True
    for p in paths:
        m = measure(p, allow)
        if m is None:
            print("%s: no body prose found" % p)
            allok = False
            continue
        allok &= report(m, verbose, tool_free)
    print("\n%s" % ("All pages meet the prose targets."
                    if allok else "Some targets not met -- see FAIL lines above."))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
