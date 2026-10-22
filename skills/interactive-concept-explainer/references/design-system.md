# Concept Lab — Design System Reference

Read this before writing any HTML. Every lab in the series shares this shell. Copy the snippets below and adapt the *content*, not the *system*.

## Fonts and base tokens

Always load these two Google Fonts in `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

Base CSS variables — these four never change between labs:

```css
:root{
  --ink:#0d1017; --panel:#151a26; --panel-2:#1b2130; --line:#283043;
  --text:#e7eaf3; --muted:#8b93ab;
  --mono:'IBM Plex Mono', ui-monospace, monospace;
  --disp:'Space Grotesk', system-ui, sans-serif;
}
```

Then add 2–5 **semantic accent colors** specific to this concept's channels/categories/facets, e.g.:

```css
/* example: sparse vs dense vs hybrid vs rerank vs good/warn */
--sparse:#f0a03c; --dense:#3fd6ce; --hybrid:#a487f5; --rerank:#ef5b93;
--good:#3fd67a; --warn:#ef5b93; --tp:#3fd67a; --fp:#e8615a; --fn:#3a4258;
```

If a concept reappears across labs in the same series (e.g. "sparse" and "dense" show up again in a later lab), reuse its established color for continuity. New, unrelated concepts get fresh hues — don't force a palette from an unrelated earlier lab onto something it doesn't conceptually match.

## Page shell

```css
body{
  margin:0;
  background:radial-gradient(900px 500px at 10% -10%, #1a2440 0%, transparent 60%), var(--ink);
  color:var(--text); font-family:var(--disp); line-height:1.5;
}
.wrap{max-width:960px;margin:0 auto;padding:28px 18px 60px}
```

`max-width` ranges 900–1020px depending on how wide the visualization needs to be.

## Header block

```html
<div class="eyebrow">RAG retrieval lab · 06</div>
<h1>Short punchy headline with <span style="color:var(--accent)">one colored span</span>.</h1>
<p class="sub">One sentence: what the user is looking at and what to do with it.</p>
```

```css
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);display:flex;gap:10px;align-items:center;margin-bottom:12px}
.eyebrow::after{content:"";flex:1;height:1px;background:var(--line)}
h1{font-size:clamp(22px,4.5vw,32px);margin:0 0 8px;font-weight:700;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:14px;max-width:64ch;margin:0 0 22px}
```

The eyebrow labels a numbered position in the series (`"<series name> lab · NN"`) — increment it per lab.

## Panels / cards

```css
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:18px}
.card.accentname{border-top:2px solid var(--accentname)}
```

Grids of cards collapse responsively:

```css
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media (max-width:760px){ .grid2,.grid3{grid-template-columns:1fr} }
```

## Chips / tabs (pill toggle buttons)

Used for query presets, category filters, or mode switches.

```css
.chip{font-family:var(--mono);font-size:11.5px;padding:6px 10px;border-radius:99px;cursor:pointer;background:var(--panel-2);border:1px solid var(--line);color:var(--muted)}
.chip:hover{color:var(--text);border-color:#3c4762}
.chip[aria-pressed="true"]{background:#2a2140;border-color:var(--hybrid,--accent);color:#d9caff}
.chip:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
```

Always toggle `aria-pressed` in JS, never just a CSS class — screen readers and the `[aria-pressed="true"]` selector both depend on it.

## Sliders

```css
input[type=range]{accent-color:var(--accent);flex:1;min-width:140px}
```

```html
<div class="row">
  <label for="lambda">λ (relevance ⟷ diversity)</label>
  <input type="range" id="lambda" min="0" max="1" step="0.05" value="0.5" />
  <span class="valpill" id="lambdaVal">0.50</span>
</div>
```

Pair every slider with a row of 3–5 preset buttons that jump to instructive values — presets are how users discover the payoff without hunting for it.

## Stat cards with live bars

```css
.stat{background:var(--panel-2);border:1px solid var(--line);border-radius:10px;padding:12px}
.stat .kicker{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.stat b{display:block;font-size:24px;margin:4px 0 8px;letter-spacing:-.02em}
.bar{height:6px;border-radius:99px;background:#1d2434;overflow:hidden}
.bar i{display:block;height:100%;border-radius:99px;transition:width .4s cubic-bezier(.22,.7,.3,1)}
```

Every stat card: a mono uppercase kicker label, a big number, a thin animated fill bar underneath. Update `textContent` and `style.width` together in `render()`.

## Legend

```css
.legend{display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-top:12px}
.swatch{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
```

## Callout — the payoff line

This is the single most important element. Every lab ends its interactive section with one dynamic paragraph that names, in prose, exactly what the current control state demonstrates.

```css
.callout{margin-top:16px;background:linear-gradient(90deg,#1c1730,#151a26 70%);border:1px solid #3a3060;border-left:3px solid var(--accent);border-radius:8px;padding:13px 15px;font-size:13.5px;color:#cfd4e6}
.callout b{color:#fff}
.callout.warn{border-left-color:var(--warn)}
```

Write the callout text as `if/else` branches keyed to the live computed values (not the raw slider position) — e.g. branch on "recall < 0.5" rather than "k < 5" — so the prose stays correct even if you tune the underlying data later.

## Animated reordering list (for ranking/reranking/MMR-style demos)

Absolute-position rows inside a relative container; only change `top` to animate reordering:

```css
.clist{position:relative}
.crow{position:absolute;left:0;right:0;height:46px;transition:top .55s cubic-bezier(.22,.8,.28,1), border-color .3s, opacity .3s}
```

```js
function render(order){
  order.forEach((item,i)=>{
    rowEls[item.id].row.style.top = (i*ROWH)+'px';
  });
}
```

A dashed `.cutoff` line, absolutely positioned at `top5Count * ROWH`, marks "sent to LLM / dropped" boundaries where relevant.

## SVG scatter plot (for 2D semantic-space demos)

```js
const NS="http://www.w3.org/2000/svg";
function svgEl(tag,attrs){ const e=document.createElementNS(NS,tag); for(const k in attrs) e.setAttribute(k,attrs[k]); return e; }
```

Build circles for points, a diamond `<path>` for the query marker, thin `<line>` elements from query to selected points with fading opacity by pick order.

## Tables

```css
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
thead th{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}
tbody td{padding:10px 12px;font-size:13px;border-bottom:1px solid #1e2434}
```

## JS conventions

```js
const $=id=>document.getElementById(id);
const el=(t,c,x)=>{const e=document.createElement(t); if(c)e.className=c; if(x!=null)e.innerHTML=x; return e;};
```

- One `render()` function that reads all current control state, recomputes every derived value, and rewrites the DOM. Never hand-patch individual elements outside of `render()` — it's the only source of truth and it's what makes "presets" and sliders behave identically.
- Preset buttons just set a control's value and call `render()`.
- Any real algorithm (BM25, greedy MMR, cosine similarity) lives in small pure functions above `render()` so it can be sanity-checked standalone with Node before shipping.

## Responsiveness and accessibility

```css
@media (max-width:700px){ /* collapse grids to 1 column, shrink cell sizes */ }
@media (prefers-reduced-motion:reduce){ *{transition:none !important;animation:none !important} }
```

- `aria-pressed` on every toggle/tab button.
- `:focus-visible{outline:2px solid var(--accent);outline-offset:2px}` on all interactive controls.
- Every `<input type=range>` has a visible `<label for=...>`.

## Non-negotiables

- Single self-contained HTML file — inline `<style>` and `<script>`, only external resources are the two Google Fonts links.
- No `localStorage`/`sessionStorage` — use JS variables/state only.
- No placeholder Lorem Ipsum data — every dataset is hand-designed to teach the specific point.
