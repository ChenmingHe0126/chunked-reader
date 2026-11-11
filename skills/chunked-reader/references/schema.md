# Data files

## data/book.json

```json
{
  "title": "Page title, 2–4 words",
  "brand": "Short name in the top bar (defaults to title)",
  "sub": "One or two sentences under the title: what was read, how many cards, how long. HTML allowed.",
  "thesis": "The single claim the whole reading supports. HTML allowed.",
  "thesisNote": "Small print under the thesis (optional)",
  "howto": "How to use the page (optional)",
  "colophon": "Sources, licence notes, what could not be read. HTML allowed.",
  "storageKey": "unique-key-for-progress",
  "partOrder": ["A", "B", "C"],
  "labels": {"apply": "和你的项目"},
  "theme": ""
}
```

## data/part_<key>.json

```json
{
  "key": "A",
  "title": "Part title",
  "chapters": "One line: which sources this part covers",
  "lessons": [],
  "glossary": [{"term": "痕迹协作", "en": "stigmergy", "def": "One sentence.", "ref": "a03"}],
  "figures": [{"lesson": "a02", "file": "a_src_fig03.png", "n": "3", "caption": "One sentence, in the reading language",
               "credit": "Author Year, CC BY 4.0", "page": "https://…", "license_evidence": "where the licence is stated"}],
  "figure_links": [{"lesson": "a02", "label": "Fig. 2: what it shows", "url": "https://…"}],
  "notes": "For the editor: what was not read, what is uncertain"
}
```

## A lesson

| field | required | notes |
|---|---|---|
| `id` | yes | part key in lower case + two digits: `a01` |
| `title` | yes | says what the card teaches |
| `source` | | short source name + section |
| `where` | | pages / section / figure numbers |
| `minutes` | | 3–5 |
| `gist` | yes | the conclusion, one or two sentences |
| `gistShort` | yes | ≤ 24 characters, shown in the index |
| `body` | yes | HTML: `p ul ol li strong code pre table h3` |
| `figs` | | `[{"svg": "<svg viewBox=…>", "cap": "…"}]`, 0 or 1 |
| `facts` | | `<ul>` of hard information, each with a location |
| `quiz` | | exactly two `{"q","a"}` |
| `ext` | | what happened after the source (optional) |
| `apply` | | `<ul>` of concrete actions for the reader's project |

`orig` and `links` are filled by `build.py` from the part's `figures` and `figure_links`.

## SVG palette

`viewBox` width 600. No literal colours. Strokes: `ink mut c1 c2 wr`. Fills: `inkf mutf c1f c2f wrf soft bgf`. Text is body colour by default; `m` muted, `k1`, `k2`, `w` for the accents. Prefix marker ids with the lesson id.
