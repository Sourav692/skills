# Runbook: the Agent_Evaluation_Demystified repo

Repo-specific procedure for `~/Github_Repos/Agent_Evaluation_Demystified`. Read this when
restyling anything under `docs/` there. The reasoning behind the passes is in `SKILL.md`; this
file is only what is specific to that repo.

## Scope

Governs prose under `docs/` — the roadmap explainers, the concept companions, the question bank,
the study guide. Notebooks have their own separate contract in
`<skills-root>/format-notebook/SKILL.md`; do not apply prose rules to notebook code cells.

Third-party material under `labs/agent-evaluation/arize-phoenix-labs/` is kept unmodified. Never
restyle it.

## One standing conflict, already resolved

The repo's own `explainer` skill records a preference for "tables/bullets over dense prose".
That sits against the bullet budget, and both are right about different things. The resolution
that applies here: **bullets for what a reader scans, checks off, or looks up** — checklists,
prerequisites, "you are done when you can" lists, reference enumerations, takeaways — and
**prose for anything that forms an argument**. Do not read the bullet rule as deleting the
checklists.

## Restyling an explainer

**Set up.** Copy the source to `<same-name>-v2.md` in `docs/roadmap-explainers/`, so the two can
be compared live before one replaces the other.

**Register it**, or the build's completeness check fails:

- a `RENDER` entry in `site/build.py`, under `Roadmap explainers`, directly after the original;
- a `### ` section of its own in `INDEX.md`, listing its headings.

**Restyle** by whole-paragraph replacement rather than sentence edits — tables, diagrams and
code blocks are then structurally untouchable, which is what makes the preservation check come
back clean.

**Check.** All five are free and run offline:

```bash
S=<skills-root>/study-content-style/scripts
python3 $S/check_prose.py --tool-free \
  --allow=expected_output,actual_output,retrieval_context,GEval,criteria,evaluation_steps \
  docs/roadmap-explainers/<page>-v2.md
python3 $S/page_stats.py reading-time docs/roadmap-explainers/<page>-v2.md
python3 $S/page_stats.py preserved docs/roadmap-explainers/<page>.md \
                                   docs/roadmap-explainers/<page>-v2.md

uv run --no-project --with markdown python3 site/build.py
python3 .github/scripts/check_index_coverage.py
python3 <skills-root>/link-check/scripts/check_links.py docs
```

Each level's `--allow` list is its own: level 2 wants tool-call and trajectory field names, level
4 judge and rubric ones. Declare them per page rather than maintaining a global list.

**Preview** with `python3 -m http.server -d site/dist 8000`, then read the restyled page beside
the original.

**Promote**, once accepted: move the content into the canonical filename, delete the `-v2` file,
and drop the extra `RENDER` and `INDEX.md` entries, so the URL and navigation stay put.

**Expect sections to die.** The section-necessity test removed Level 1's framework-comparison
section outright, and its one functional idea folded into a neighbour that was already
half-stating it. Rebalance takeaways and self-check questions to stay one-per-section afterwards.

## Publishing

`docs/` is published at https://eval-demystified.vercel.app and **a push to `main` is the
deploy**. Pushing is outward-facing; ask before pushing unless the user asked for the site to be
updated.

## Level 1 as the worked example

`docs/roadmap-explainers/01-rag-retrieval-and-generation-v2.md` is the reference restyle.
Measured before and after:

| Target | Threshold | Reference style | Level 1 before → after |
|---|---|---|---|
| Median sentence words | ≤ 16 | 13 | 19 → 14 |
| Sentences over 30 words | ≤ 10% | 4% | 22.1% → 3.8% |
| Sentences under 12 words | ≥ 35% | 46% | 29.7% → 37.3% |
| "you"/"your" per 1,000 words | ≤ 2.0 | 0 | 9.9 → 1.8 |
| Headings led by a verb | all | 6 of 7 | 0 of 12 → 10 of 10 |

## Worklist for the remaining explainers

Measured with `check_prose.py --tool-free`. Targets: median ≤16, >30w ≤10%, <12w ≥35%,
you ≤2.0, label headings 0.

| Explainer | median | >30w | <12w | you/1k | label headings | API names |
|---|---|---|---|---|---|---|
| 00-orientation | 19 | 16.5% | 23.1% | 20.1 | 10 | 1 |
| 02-agents-tools-trajectories | 19 | 23.4% | 18.0% | 8.0 | 6 | 20 |
| 03-ground-truth | 22 | 35.6% | 13.8% | 8.9 | 9 | 12 |
| 04-judges | 19 | 17.1% | 22.1% | 5.1 | 10 | 5 |
| 05-statistics | 21 | 34.0% | 19.6% | 20.5 | 9 | 2 |
| 06-release-gate | 19 | 17.3% | 18.1% | 3.0 | 11 | 3 |
| 07-online-evaluation | 25.5 | 38.7% | 14.5% | 12.1 | 10 | 3 |
| 08-safety-adversarial | 18 | 15.5% | 22.3% | 4.9 | 8 | 11 |
| 09-harness-as-product | 24 | 34.1% | 20.0% | 6.5 | 6 | 12 |
| 10-enterprise-harness | 18.5 | 23.7% | 24.6% | 7.7 | 11 | 7 |

07 is the hardest on rhythm, 02 has the worst framework leakage, and 00 and 05 are where second
person is heaviest. Re-measure rather than trusting this table if the files have changed.
