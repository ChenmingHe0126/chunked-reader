# chunked-reader

A Claude skill that turns a book, a paper, or a reading list into a small web app of 3–5 minute lesson cards.

Each card keeps only what you would write on an index card: the algorithm, the rule, the number, the definition. It adds a redrawn diagram, two quiz questions, and a box that says what the idea means for *your* project. The home screen tracks what you have read.

把一本书、一篇论文或一份阅读清单拆成 3–5 分钟一张的精读卡片，只留算法、概念和硬信息，配重画的示意图、小测和「和你的项目」，做成一个能在手机上读的单页应用。

## What it does

1. Pins down who is reading and what to keep.
2. Reads the sources for real, one reader per part (in parallel when subagents are available).
3. Handles figures honestly: redraws mechanisms as SVG, embeds original figures only when an open licence is confirmed, links out to everything else.
4. Validates and assembles one self-contained page.

## Install

Copy `skills/chunked-reader` into `~/.claude/skills/` (or your project's `.claude/skills/`).

```
git clone https://github.com/ChenmingHe0126/chunked-reader
cp -r chunked-reader/skills/chunked-reader ~/.claude/skills/
```

Then ask Claude: "把这几篇论文做成分块阅读器" or "make a chunked reader from this PDF".

## Build by hand

```
python skills/chunked-reader/scripts/build.py <data_dir> <figs_dir> <out_dir>
```

`data_dir` holds `book.json` and `part_*.json` (see `skills/chunked-reader/references/schema.md`). Needs Python 3.9+ and Pillow.

## Notes on copyright

Cards are study notes written in the reader's own words. The skill never translates or copies a source at length. Original figures are embedded only with a recorded licence; `build.py` refuses a figure that has no credit and licence evidence.

## Licence

MIT
