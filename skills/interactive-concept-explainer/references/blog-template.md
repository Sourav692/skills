# Concept Lab — Blog Template Reference

Read this before writing the companion Markdown post. The goal is a post that reads as the written twin of the HTML lab — same numbers, same narrative, different medium.

## Skeleton

```markdown
# {Concept Title}: {short evocative subtitle}

*{Series Name} — Part {N} of {M}*

{One or two sentence hook — connect to the previous part if there is one, or frame the problem this concept solves.}

## TL;DR

- {The whole point, in one bullet}
- {A second key fact}
- {A third, often the trade-off or gotcha}

## {Problem / Motivation}

- Bullets explaining what breaks, or what's inefficient, without this concept.

## {Core Mechanism}

Explain how it actually works. If there's a formula, put it in a fenced code block (not LaTeX — plain text renders everywhere):

    Recall@k = (relevant docs retrieved in top-k) / (total relevant docs)

Follow with bullets unpacking each term.

## Visualizing {X}

```mermaid
{one diagram — see selection guide below}
```

Add 1–2 sentences underneath interpreting the diagram, not just displaying it.

## {Comparison / Trade-off}

A markdown table is almost always the right format here — shape vs shape, method vs method, metric definitions, etc.

## When to Use It — and When Not To

- Bullets: the concrete situations where this shines.
- Bullets: the concrete situations where it backfires or is unnecessary.

## Interview Spotlight: 5 Questions You Might Get Asked

*The kind of production/real-time-use-case questions this concept shows up in at OpenAI-, Anthropic-, and Google-caliber interviews.*

### 1. {Scenario-framed question}

**What a strong answer covers:**
- {point}
- {point}
- {point}

### 2. {Debugging / production-incident question}

**What a strong answer covers:**
- {point}
- {point}
- {point}

### 3. {Design trade-off question}

**What a strong answer covers:**
- {point}
- {point}
- {point}

### 4. {Measurement / monitoring question}

**What a strong answer covers:**
- {point}
- {point}
- {point}

### 5. {Edge case / failure mode question}

**What a strong answer covers:**
- {point}
- {point}
- {point}

## Key Takeaways

- 3–4 bullets, the "if you remember nothing else" summary.

---
*Previous: Part {N-1} — {title}. Next: Part {N+1} — {title}.*
```

Drop the prev/next footer if this is a standalone post rather than part of a series.

## Choosing the right Mermaid diagram

Match the diagram type to the *shape* of the concept, not habit:

| Concept shape | Diagram type | Example |
|---|---|---|
| A pipeline / sequence of stages | `flowchart LR` or `flowchart TD` | Query → Retrieve → Fuse → Rerank → LLM |
| Two parallel mechanisms compared | `flowchart` with two labeled `subgraph`s side by side | Bi-encoder vs cross-encoder |
| An iterative/greedy algorithm | `flowchart TD` with a decision diamond looping back | MMR's greedy selection loop |
| A two-axis trade-off | `quadrantChart` | Precision vs recall as k increases |
| A conversation/interaction sequence | `sequenceDiagram` | Client-server auth handshake |

Use more than one diagram only if the concept genuinely has more than one distinct shape to show (e.g. an architecture diagram *and* a formula-explanation diagram).

## Mermaid syntax gotchas (avoid render failures)

- **Subgraph titles with spaces, parentheses, or punctuation must use the bracket-label form.** Never write `subgraph Bi-Encoder (Retrieval)` — write:

  ```mermaid
  flowchart LR
      subgraph bi["Bi-Encoder (Retrieval)"]
          A --> B
      end
  ```

- **Node labels with line breaks** use `<br/>` inside a quoted label: `A["Sparse Vector<br/>(mostly zero)"]`.

- **`quadrantChart` point names must not contain a colon** — the colon separates the name from its `[x, y]` coordinates. `k=5` is safe; `k: 5` is not.

- **`quadrantChart` quadrant numbering**: `quadrant-1` = top-right, `quadrant-2` = top-left, `quadrant-3` = bottom-left, `quadrant-4` = bottom-right. Set axis labels and quadrant names so they actually match this layout — e.g. if the x-axis is "Low Recall → High Recall" and y-axis is "Low Precision → High Precision," then quadrant-1 (top-right) is the *high/high* "ideal" zone.

- Keep each diagram focused on one idea — resist cramming the entire pipeline plus the algorithm plus the trade-off into a single Mermaid block. Split into two small diagrams instead.

## Writing the Interview Spotlight section

These are not textbook definitional questions — "what is BM25" tests recall, and that's not what a production ML/AI-engineering interview at a frontier lab is actually probing. Every question should force the same kind of judgment call a real on-call engineer or system designer would face.

**Question types to rotate across the 5** (use this as a checklist, not a rigid template):

- **Scenario framing** — open with a concrete product situation ("Your support bot handles 50k tickets/day across 12 languages...") before asking the actual question.
- **Debugging / production incident** — something is visibly broken in front of a customer right now; what do you check first, and why?
- **Design trade-off** — two valid architectures exist; justify a choice under stated constraints (latency budget, cost ceiling, data freshness requirement).
- **Measurement / monitoring** — how would you know this is working (or silently degrading) in production, without waiting for user complaints?
- **Edge case / failure mode** — push on the specific way this concept breaks at scale or under adversarial/unusual input.

**Weak question (avoid):** "What is the difference between sparse and dense retrieval?"
**Strong question (use):** "A customer reports that searching their support KB for an exact order ID like `ORD-88213` returns unrelated articles about 'order tracking' instead of the ticket they meant. Your retriever is dense-only. Walk through how you'd diagnose this and what you'd change — and what you'd tell the customer-facing team in the meantime."

The strong version is answerable only by someone who understands *why* the failure happens (embeddings blur rare tokens) and can reason about a fix under real constraints (can't retrain overnight, customer is waiting) — that's the bar for these five questions.

**Worked example** (topic: Hybrid Search, for calibration — don't reuse verbatim, generate fresh questions tied to the actual concept and dataset in the current lab):

> ### 1. Your RAG-powered support assistant is going live for a fintech client tomorrow. Their KB mixes exact transaction codes with conversational FAQ articles. How do you decide whether to ship dense-only, sparse-only, or hybrid retrieval for launch, given you have one day left to test?
>
> **What a strong answer covers:**
> - Recognizes the mixed query distribution (codes + paraphrase) as the deciding signal, not a preference
> - Proposes a fast smoke test: sample real or synthetic queries of both types, check recall@k per channel
> - Defaults to hybrid as the safe choice under time pressure, with RRF (no tuning needed) over alpha-weighted fusion
> - Flags what they'd still want to validate post-launch (real query logs, not just the pre-launch sample)
>
> ### 2. Three days after launching hybrid search, someone notices the assistant is citing a completely unrelated policy document at position 1 for a common query. How do you find out whether sparse, dense, or the fusion step is at fault?
>
> **What a strong answer covers:**
> - Isolates each channel's raw top-k for that query before blaming fusion
> - Checks whether the offending doc is winning on keyword overlap (sparse false positive) or embedding proximity (dense false positive)
> - Considers whether RRF's k parameter or an alpha weight is over-crediting one channel
> - Proposes a regression query set so this specific failure doesn't silently return

## Tone

- Headers and bullets over dense paragraphs — this is a blog post meant to be scanned, not a textbook chapter.
- Every section should be answerable from the HTML lab's dataset — don't introduce new numbers in the Markdown that don't match what the interactive lab shows.
- End on the "Key Takeaways" list — never end on a diagram or a table with no closing prose.
