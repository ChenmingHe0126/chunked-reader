---
name: chunked-reader
description: Turn a book, a paper, or a reading list into a small web app of 3–5 minute lesson cards that keep only the algorithms, concepts and hard facts, with redrawn diagrams, openly licensed original figures, quizzes, a glossary and reading progress. Use when the user asks to "help me read", "精读", "拆成小块读", "做成阅读器", "reading app", or hands over papers/books/links and wants the important parts distilled into something they can read on a phone.
---

# Chunked reader

A reading list becomes one self-contained page: a home screen with progress, and one short card per idea. The reader finishes a card in a few minutes, checks themselves with two questions, and sees how the idea applies to their own project.

The method has four stages. Do them in order; do not start writing cards before the format and the reader are pinned down.

## 1. Pin down the reader and the cut

Write these down before reading anything (ask only if the conversation does not already answer them):

- **Who reads it and why.** Their background, what they can already do, the project this reading serves. Every card's `apply` box is written against that project.
- **What to keep.** Default: algorithms, rules, parameters, data structures, definitions, reproducible procedures, numbers. Default drop: acknowledgements, literature-review padding, repeated rhetoric, credits, long philosophy (keep a philosophical idea only when it changes *how to do* something, in two or three sentences).
- **Parts.** Group sources into 3–6 parts with a letter key (A, B, …). One part per major source or per theme. Put the most important source first.

Create `data/book.json` (see `references/schema.md`) and a project brief by copying `references/brief.md` and filling in the reader paragraph.

## 2. Read for real, one reader per part

The cards must come from the sources, not from memory.

- Give each part to its own subagent when subagents are available (they run in parallel and each keeps a long source out of the main context). Each gets: the brief file path, its part key and title, its output path `data/part_<key>.json`, a temp directory for downloads, the exact URLs, and a short list of *what to dig out* for that source. Otherwise read the parts yourself one at a time.
- PDFs: download and extract text with a script (`pypdf`); do not rely on page rendering being available.
- A reader that cannot reach a source says so in its `notes` and writes fewer cards. It never fills the gap from memory. Anything the reader adds beyond the source is wrapped in `<span class="bc">【补充：</span>…】` (or the equivalent marker in the reading language).

## 3. Figures: redraw, or reuse only what is licensed

Three kinds of picture, kept visibly separate in the page:

1. **Redrawn diagrams** (`figs[].svg`): the reader's own SVG of the mechanism, using the palette classes so both themes work. Always allowed. Caption ends with "示意图，非原文插图".
2. **Original figures** (`figures[]` → shown under "原文配图"): only when an open licence is confirmed on the source page (CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA, CC0, public domain) or the figure comes from a file the user owns and the reader stays private. Record `credit` and `license_evidence`; `build.py` refuses a figure without them.
3. **Links out** (`figure_links[]`): everything else. One line saying what the figure shows and a URL that lands on it.

Text follows the same rule: paraphrase everything; at most one short quoted phrase per card. A card is a study note about the source, never a translation of it.

## 4. Build, look once, publish

```
python scripts/build.py <data_dir> <figs_dir> <out_dir>
```

It validates every card, converts figures to WebP, inlines the data into `assets/shell.html`, and prints a file map. Fix every ERROR; read every WARN (hard-coded SVG colours and unknown classes are the usual ones).

Then read the merged result as an editor before publishing:

- Cut cards that repeat each other across parts; keep the better one and cross-reference.
- Check each `gist` states a conclusion, not a topic.
- Check claims that matter (numbers, who did what, which year) against the reader's `facts` locations.
- Open the page once: home, one card with an SVG, one with an original figure, the glossary.

Publish as an Artifact when the tool is available: `index.html` as the page, the printed file map as `files`. Otherwise hand over the `out_dir` folder. Keep `data/` in the user's project so the next pass edits JSON, not HTML.

Tell the user plainly: how many cards and minutes, which sources could not be read, and which figures are links rather than images and why.

## Card anatomy

`id · source · where · minutes` → title → **gist** (the conclusion in one or two sentences) → body (plain explanation, pseudocode in `<pre><code>`) → redrawn diagram → original figures → links to protected figures → **facts** (hard information with locations) → **quiz** (two questions that test understanding) → ext (optional, what happened since) → **apply** (concrete actions for the reader's project).

Sizing: 3–5 minutes per card, one idea per card, 3–8 cards per source. Fewer, denser cards beat coverage.

## Changing the look

`book.json` → `theme` takes a CSS string that overrides the `:root` tokens (`--bg --surface --sunk --ink --muted --rule --accent --accent-soft --c1 --c1-soft --warn`); supply the light values on `:root` and the dark values in both dark blocks, as in the shell. `labels` renames any UI string (for example `{"apply": "和你的论文"}`).

## Files

- `assets/shell.html` — the reader app (styles, router, progress in localStorage, lightbox, glossary).
- `scripts/build.py` — validate + assemble.
- `references/schema.md` — `book.json` and `part_*.json` fields.
- `references/brief.md` — the writing brief handed to each reader.
