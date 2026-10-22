# Tutorial prose style

Builds learner-facing pages for a tutorial, course, or documentation site in one consistent
house format, and converts existing material into it.

The format exists to prevent one specific failure: technical teaching material collapsing into
bullet inventories. An inventory is easy to write and impossible to learn from, because a list
never tells the reader which item matters, why it is true, or what to do when two of them
conflict. Everything below is a way of forcing a page to carry an argument instead.

It is reverse-engineered from the FDE Handbook's GenAI Architecture chapters
(`fdehandbook.com/learn/genai-architecture`), which explain genuinely technical material
without jargon-dumping. Quoted examples come from there.

---

## Two ways in

**From scratch** — a topic, a pile of notes, a notebook, a research pass, or nothing but a
title. Start at **How to build one**.

**From an existing page** — it exists and reads wrong. Start at **Restyling an existing page:
the order of passes**.

Both produce the same page shape and get verified the same way. The only difference is where you
start and whether there is a source to preserve.

## The page you are producing

```markdown
# <Topic as a noun phrase>

*<Tagline: ONE sentence naming the trade-off or tension, not the topic.>*

◷ <N> min

<Lede: TWO sentences. The first kills a wrong prior and is short.
The second prescribes, and cross-references an earlier page rather than re-explaining it.>

---

## 1. <Imperative verb phrase>

<claim → the reason it is true → what to do about it>

## 2. <Imperative verb phrase>
...

---

## Key Takeaways

- <one sentence per section above, compressions, nothing new>

## Check Yourself

<one question per takeaway, answers collapsed or inline>

## References
```

Number the sections only when later ones genuinely depend on earlier ones — numbers promise a
sequence. Many sites also key their in-page navigation off numbered headings, so check the
site's build before dropping numbers from an existing page.

---

## How to build one

**1. Scope the page to one idea, and write down what it will not cover.** A page covering two
ideas cannot have one tagline, and the tagline is the test. Where the material is genuinely two
ideas, that is two pages — say so rather than writing one page that hedges. Decide the reader
too: what they already know, and what they should be able to do afterwards. Those two decisions
settle most of the arguments that come later.

**2. Gather the material before drafting, and reuse what already exists.** Read whatever sources
there are in full — notes, notebooks, transcripts, existing docs, research — and pull out the
concrete numbers, worked examples and failure cases. A page built from real material teaches; a
page built from what sounds right about the topic does not, and the tell is whether the numbers
are specific. Reuse the running example the surrounding material already uses rather than
inventing a second one. Where sources conflict or a fact cannot be verified, say so on the page
instead of smoothing it over, and never invent a figure or a citation to fill a gap.

**3. Find the tension before writing anything.** The tagline is the hardest sentence on the
page and writing it first shapes everything after it. It names two goods pulling against each
other:

> "Capture enough context to explain behavior without leaking sensitive data."

A reader understands the shape of that problem before knowing a single term in it — which is
exactly what licenses the page to use technical terms freely later. If you cannot name a
tension, the page is a reference entry, not a lesson, and should be written as one.

**4. Draft the headings as a standalone outline, and read only them.** Does the reader come away
with instructions? If the outline teaches nothing, the headings are labels.

| Label (weak) | Instruction (strong) |
|---|---|
| `Retrieval vs. Generation` | `Separate Retrieval From Generation` |
| `Caching Strategies` | `Cache What Is Expensive and Stable` |
| `Error Handling` | `Fail Loudly at the Boundary, Quietly Inside` |
| `Multi-Agent Considerations` | `Measure Coordination Cost` |

This matters more than it looks, because on most doc sites the headings become the sidebar, and
the sidebar is what most readers actually consume. `Topic: claim` also works when the colon
carries a real claim.

**5. Write each section in three moves** — claim, the reason it is true, what to do. The middle
move is where the teaching happens, and it compresses into **one short sentence with no jargon
that the reader cannot argue with**, usually an argument from impossibility:

> "A generator cannot faithfully use evidence it never received."

Nine words; it settles the section. Others in the same shape: *"A function cannot defend
against a value it has already accepted."* · *"A cache cannot be correct about data it was never
told changed."* · *"Happy-path success is only half the architecture."*

**If you cannot write this sentence for a section, the section does not yet have a point.**
Merge it into its neighbour or work out what it is actually claiming. This is the highest-
leverage habit in the format, because it turns "explain it plainly" from an aspiration into a
concrete thing to go find.

**6. Spend bullets carefully.** Bullets are right for what a reader will scan, check off, or
look up — checklists, prerequisites, option references, takeaways. They are wrong for anything
forming an argument: if the items only make sense in order, or each needs a clause of
justification, it is prose. A run of three to six short parallel items belongs in a sentence:

> "Record tool calls, policy decisions, retries, state changes, and stop reasons."

Anything two-dimensional is a table, not nested bullets. **If a finished page has more bullets
than paragraphs, it is a deck — go back to step 4.**

**7. Build tables as question → instrument.** Natural-language worry on the left, technical name
on the right:

| FAILURE QUESTION | BEST FIRST EVALUATOR |
|---|---|
| Was the correct source in the top five? | Retrieval relevance label |
| Were tool arguments valid and authorized? | Schema and policy check |

Write the left column the way a worried person speaks — "Was the correct source in the top
five?", never "precision@5". The reader arrives holding a worry and leaves holding a metric
name. Column headers carry meaning too: `BEST FIRST EVALUATOR` encodes a triage philosophy in
one word.

**8. Close by compressing.** Key Takeaways introduce nothing new — one sentence per section,
one section per takeaway. Then end with one portable line that also names the failure it
prevents:

> "connect every major architectural component to one failure mode and one measurable signal.
> That makes evaluation part of the design rather than a final 'we will monitor it' box."

**9. Measure the result.** Run `scripts/check_prose.py` and set the header's reading time from
`scripts/page_stats.py reading-time` (see **Verify before shipping**), then fix what they flag.
Do not skip this because the page looks right — the parts that look right are the structural
ones, and they are not the parts that fail. `page_stats.py preserved` does not apply to a page
written from scratch; there is no source to preserve.

---

## Voice

**Never introduce a term unpaired with its function.** The goal is not fewer technical words —
good prose uses *deterministic*, *idempotent*, *probabilistic* freely. It never leaves a term
standing as a name the reader is expected to already respect.

> Before: "Use idempotency keys for all mutating endpoints."
>
> After: "A client that times out cannot tell a failed write from a slow one, so it retries. An
> idempotency key — an id the caller supplies and the server remembers — lets the second request
> return the first one's result instead of writing twice."

Jargon is the **output** of an explanation, never the price of entry. Prefer a two-noun coinage
that carries the argument by itself: "mixing data with authority" explains prompt injection
completely without using the phrase.

**Use the imperative, not the second person.** *Record… Inject… Compare… Verify…*, not "you
should record". Instruction without a lecturer is most of why good technical prose never reads
as preachy.

**Hedge recommendations; never hedge mechanisms.** "Useful metrics *include*" and "*may* improve
specialization" are right; "a generator *cannot*" is also right. Prose that hedges uniformly
reads as spineless; prose that hedges nothing reads as marketing.

**Keep the rhythm short, and prefer more sentences over longer ones.** The reference style runs
a median of 13 words a sentence, with 46% of sentences under 12 words and only 4% over 30. That
rhythm is not decoration: a short declarative is what makes a claim land, and a page of 30-word
sentences reads as qualified even when every clause is correct.

This collides with the inlining rule above, and the collision is real rather than apparent.
Turning a six-item bullet list into one sentence *manufactures* a long sentence. The reference
style gets away with it because a six-minute chapter has only ~28 sentences, so one long series
is rare by construction. On a longer page, inline the series **and** cut the sentences around it,
or the page ends up with a worse rhythm than the bullet list it replaced. When the two rules
cannot both be satisfied, the rhythm wins: split the series across two sentences rather than
letting one run past 30 words.

**Open without runway.** Delete anything resembling "In today's rapidly evolving…", "As systems
become increasingly complex…", or "Before we dive in". Where the topic departs from something
familiar, open on the contrast and name the single axis of difference.

**Use the economic register where the subject is a trade-off** — *cost per success*,
*coordination overhead*, *bounded budget*. It frames engineering choices as spend rather than
virtue, which is how practitioners decide.

**Use one worked example, in domain language.** One per page, expressed in the reader's domain
rather than a framework's API, and always followed by the sentence that cashes it out against
the abstraction. An uncashed example is decoration. Reuse whatever running example the
surrounding material already has — a second example system costs more than it teaches.

**Preserve exact figures verbatim** — `0.94`, `2,500+ calls`, `~606 traces`. They are
load-bearing, not filler.

---

## Restyling an existing page: the order of passes

Most runs are conversions, and the order below is not arbitrary — each pass creates the problem
the next one solves. Doing them out of order produces a page that looks restyled and reads
exactly like the draft it replaced.

**Read the source in full first.** These pages usually consolidate several sources, so dropping
content is the main risk. The conversion is a restyle, not a rewrite: every number, table,
diagram, worked example and caveat survives unless it is cut on purpose.

1. **Decide what the page is for**, then apply the section-necessity test to every section: what
   does a reader lose if this is gone? Cut what only exists because a tool exists, and fold any
   functional idea it carried into a neighbour. Do this before writing prose — rewriting a
   section you are about to delete is the most common waste in this work.
2. **Add what the format needs and the source lacks** — tagline, reading time, key takeaways,
   self-check. Usually missing entirely.
3. **Rewrite every heading into an imperative.** Do it before touching prose: a heading that
   states a claim tells you what its section has to prove.
4. **Promote each section's unanswerable sentence.** It is often already in the source as a
   callout or a parenthetical; move it to the section's second sentence.
5. **Convert argument-carrying bullet runs to prose.** Leave scannable lists, tables and
   diagrams alone. Inlining forces an argument, which is why it improves a draft rather than
   merely compressing it:

   > Before:
   > ```
   > The retry policy should consider:
   > - network timeouts
   > - rate limits
   > - malformed responses
   > - partial writes
   > ```
   > After: "A retry policy has to distinguish network timeouts, rate limits, malformed
   > responses, and partial writes — only the first two are safe to retry blindly."

   The list asserted four things exist. The sentence says which ones to act on. While here, cut
   *restated* content rather than content: long consolidated pages repeat themselves across
   sections, and the fix is to delegate to the earlier section by name.
6. **Run the rhythm pass.** Not optional after step 5 — inlining a series *lengthens* sentences,
   so this is what pays for it. `check_prose.py --verbose` gives the worklist: split anything
   over 30 words at its natural hinge, and turn second-person constructions into imperatives.
7. **Strip the framework tour** (see the section above), declaring intended vocabulary with
   `--allow`.
8. **Make questions stand alone** — full question and answer on the page, no pointers into a
   bank, no index bookkeeping.
9. **Recompute the reading time**, which has changed: `page_stats.py reading-time PAGE.md`.
10. **Verify nothing was lost**: `page_stats.py preserved SOURCE.md RESTYLED.md`. Every line of
    its output should be an absence you can explain. This is the step that catches a paragraph
    rewrite that quietly took a figure or a table row with it.
11. **Re-run `check_prose.py` and the site's own build and link checks**, then give the user the
    URL rather than only the file path.

Two mechanical notes that matter more than they look. Edit by **replacing whole paragraphs**
rather than editing sentences in place — tables, diagrams and code blocks are then structurally
untouchable, which is most of why step 10 comes back clean. And when restyling a page that
already exists, write **alongside** the original at a second URL unless asked otherwise, so the
two can be read side by side before one replaces the other.

## Keep the page free of framework tours

The line is not "no names." It is **no deep dive into any framework's functionality.** A reader
learning a concept, a decomposition, or how to reason about a problem should leave able to apply
it with any toolkit — including one that does not exist yet.

**Keep a name when it is the shared vocabulary of the work and carries meaning.** Field names
often are: `expected_output` says what the field holds more precisely than "the reference
answer" does on its fifth mention, and it is the term that will come up in a design review.
Metric names — precision@K, recall@K, nDCG, faithfulness, groundedness — are the discipline's,
not one vendor's. Gloss each in plain words the first time it appears, then use it freely.

**Cut the API tour.** These are the shapes that signal a framework tour rather than an
explanation:

- A class inventory or a mapping table between two libraries' class names.
- Constructor arguments, import paths, decorators, method signatures.
- Mechanics that change nothing conceptual — synchronous versus asynchronous scoring, how a
  judge object is constructed, which wrapper buys which providers.
- A whole section comparing library A with library B. If the section survives only as
  "these two exist and differ," it is not a section. Either find the transferable idea
  underneath it, or cut the section — most of the time, cut it.
- Per-section pointers at source files ("*Notebook: `06_Thing_In_Practice.ipynb`*"). They break
  the reading flow and date the page; provenance belongs in the references section.

**A section that only exists because a tool exists is not mandatory.** Ask what a reader would
lose if it were gone. If the answer is "knowing that a second library exists," cut it and fold
any genuinely functional idea it carried into a neighbouring section — usually there is one, and
usually it was already half-stated there.

`scripts/check_prose.py --tool-free` lists code-shaped names in prose; `--allow=a,b,c` declares
the ones that are intended page vocabulary. Declaring them **is** the editorial decision, made
once and visible in the command rather than left implicit in the draft.

**Questions and exercises must stand alone.** When a page carries practice questions drawn from
a larger bank, reproduce the question and its answer in full on the page. A pointer like "see
§10.2 of the question bank" makes the page depend on a document the reader may not have open,
and a reader working through a page should never have to leave it to finish a question. Drop the
bookkeeping ("§10.1 has 5 questions") and credit the bank in the references section instead.

## Verify before shipping

Structural rules verify themselves — "every heading starts with a verb" either holds or it does
not, and you can see it at a glance. Rhythm and voice rules do not, so they get skipped silently
and the page ships reading exactly like the draft it was meant to replace. That failure is easy
to miss precisely because the visible parts look right.

Two bundled scripts. Run both before calling a page done:

```bash
# rhythm, voice, headings, structure -- exits 1 on failure
python3 <skill-dir>/scripts/check_prose.py PAGE.md
python3 <skill-dir>/scripts/check_prose.py --verbose PAGE.md          # the worklist
python3 <skill-dir>/scripts/check_prose.py --tool-free --allow=a,b PAGE.md

# reading time, and what a restyle dropped
python3 <skill-dir>/scripts/page_stats.py reading-time PAGE.md
python3 <skill-dir>/scripts/page_stats.py preserved SOURCE.md RESTYLED.md
```

`page_stats.py preserved` reports rather than fails, because a restyle removes things on
purpose and only the author knows which absences were intended. Read its list; every line
should be an absence you can explain. It is the step that catches a paragraph rewrite that
quietly took a figure or a table row with it.

| Target | Threshold | Reference style |
|---|---|---|
| Median sentence words | at most 16 | 13 |
| Sentences over 30 words | at most 10% | 4% |
| Sentences under 12 words | at least 35% | 46% |
| "you"/"your" per 1,000 words | at most 2.0 | 0 |
| Headings led by a verb | all of them | 6 of 7 |
| Bullets vs. paragraphs | fewer bullets | bullets only in takeaways |

It also checks that the tagline, reading time and Key Takeaways exist at all. Thresholds are
deliberately looser than the reference: a deep consolidation page carries more qualifying
clauses than a six-minute chapter and should not be flattened to match. Measurement covers body
prose only — tables, code, quotes, headings and list items are excluded, and closing sections
are excluded too, so self-check questions may address the reader as "you".

Three checks stay manual, because no script can make them. Point at the sentence in each
section that makes its argument unanswerable — a section where you cannot is a section without a
point. Find the first technical term and confirm its function is given in the same sentence. And
read the takeaways against the sections, one for one.

`--verbose` prints the over-long sentences and the second-person ones, which is the worklist.
Fixing them is mechanical: split at the natural hinge (a colon, an "and", an em-dash), and turn
"when you have no labelled IDs" into "without labelled IDs". Expect a rhythm pass to *reduce*
word count by 5-10%.

## Project runbooks

A repo usually has its own mechanics around a page — where the file goes, what must be
registered before the build accepts it, which checks run, how a draft gets promoted over the
page it replaces. Those are worth writing down once per project rather than rediscovering, and
they live in this skill's `references/` directory, one file per project.

- `references/agent-eval-demystified.md` — the `Agent_Evaluation_Demystified` repo: the
  roadmap explainers under `docs/`, its registration and gate commands, the per-level `--allow`
  lists, the worked Level 1 restyle with before/after numbers, and the remaining worklist.

Read the matching file before starting work in that repo. When working somewhere with no file
here yet, learn the mechanics from the repo itself and offer to add one.

## Fitting the site

Before writing the file, check how the site registers and renders pages: many static builders
require every new page to be listed somewhere, key in-page navigation off a specific heading
level, or treat one heading level as the document title. Match those constraints — a page that
does not build is not a page. After writing, run the site's own build and link checks, and tell
the user the URL to look at rather than only the file path.

When restyling an existing page, prefer writing alongside the original at a second URL unless
the user asks for an in-place rewrite, so the two can be compared before one replaces the other.

## Adapting to the format

The rules are scale-invariant; section length is not.

- **Short chapter (5–8 min).** Sections of 3–5 sentences, at most one table each. The uniform
  shortness is what makes the reading-time promise credible.
- **Deep explainer or consolidation page.** Sections may run much longer. Hold at *no section
  longer than about 40 lines without a subheading*, and keep every other rule.
- **API or reference documentation.** The bullet budget relaxes — reference material is looked
  up, not read. "Never an unpaired term" and instructing headings still apply, and matter more.
- **Notebooks.** Markdown cells follow these rules; code cells follow the project's own
  formatting contract.

## Do not overcorrect

Say these when handing back a page, so the format is not read as stricter than it is:

- It does not ask for shorter pages. The rules target density, not length.
- It does not ask for fewer tables. Tables are the preferred home for anything two-dimensional.
- It does not ask for the removal of every list — checklists and reference enumerations keep
  their bullets.
- It does not ask for simpler ideas. Nothing here licenses dropping a hard concept, only
  refusing to name one without explaining it.
- It does not apply to third-party or vendored material, which stays as its author wrote it.
