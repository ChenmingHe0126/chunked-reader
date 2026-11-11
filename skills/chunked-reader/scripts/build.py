#!/usr/bin/env python3
"""Assemble a chunked reader from book.json + part_*.json + figs/.

    python build.py <data_dir> <figs_dir> <out_dir>

data_dir/book.json   title, brand, sub, thesis, thesisNote, howto, colophon, storageKey, labels, theme
data_dir/part_*.json one part each: key, title, chapters, lessons[], glossary[], figures[], figure_links[]
figs_dir             original figures named in part "figures" (only openly licensed ones)
out_dir              gets index.html and figs/*.webp

Exits non-zero on validation errors. Prints a JSON file map for publishing.
"""
import json, re, sys, pathlib

REQUIRED = ["id", "title", "gist", "gistShort", "body"]
SVG_CLASSES = {"ink", "mut", "c1", "c2", "wr", "inkf", "mutf", "c1f", "c2f", "wrf", "soft", "bgf", "m", "k1", "k2", "w"}


def fail(msgs):
    for m in msgs:
        print("ERROR", m, file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    data, figs, out = (pathlib.Path(a) for a in sys.argv[1:])
    shell = (pathlib.Path(__file__).resolve().parent.parent / "assets" / "shell.html").read_text(encoding="utf-8")
    book = json.loads((data / "book.json").read_text(encoding="utf-8"))
    errors, warns, seen = [], [], set()
    parts, glossary, filemap = [], [], {}
    (out / "figs").mkdir(parents=True, exist_ok=True)

    for pf in sorted(data.glob("part_*.json")):
        p = json.loads(pf.read_text(encoding="utf-8"))
        lessons = {}
        for l in p.get("lessons", []):
            lid = l.get("id", "?")
            for k in REQUIRED:
                if not l.get(k):
                    errors.append(f"{pf.name} {lid}: missing {k}")
            if lid in seen:
                errors.append(f"{pf.name} {lid}: duplicate id")
            seen.add(lid)
            if len(l.get("gistShort", "")) > 40:
                warns.append(f"{lid}: gistShort is long ({len(l['gistShort'])} chars)")
            if len(l.get("quiz", [])) not in (0, 2, 3):
                warns.append(f"{lid}: {len(l.get('quiz', []))} quiz questions")
            for f in l.get("figs", []):
                svg = f.get("svg", "")
                if "viewBox" not in svg:
                    errors.append(f"{lid}: svg without viewBox")
                for hexc in set(re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]{3,8})"', svg)):
                    warns.append(f"{lid}: svg hard-codes colour {hexc}")
                for cls in re.findall(r'class="([^"]+)"', svg):
                    for c in cls.split():
                        if c not in SVG_CLASSES:
                            warns.append(f"{lid}: svg class '{c}' is not in the palette")
            l.setdefault("orig", [])
            l.setdefault("links", [])
            lessons[lid] = l
        for f in p.get("figures", []):
            l = lessons.get(f.get("lesson"))
            src = figs / f.get("file", "")
            if not l:
                warns.append(f"{pf.name}: figure {f.get('file')} points at unknown lesson {f.get('lesson')}")
                continue
            if not src.is_file():
                warns.append(f"{pf.name}: figure file missing: {f.get('file')}")
                continue
            if not f.get("credit") or not f.get("license_evidence"):
                errors.append(f"{pf.name}: figure {f['file']} has no credit or licence evidence; do not publish it")
                continue
            from PIL import Image
            im = Image.open(src)
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if "A" in im.getbands() or im.mode == "P" else "RGB")
            if im.width > 1500:
                im = im.resize((1500, round(im.height * 1500 / im.width)))
            name = src.stem + ".webp"
            im.save(out / "figs" / name, "WEBP", quality=82)
            filemap["figs/" + name] = str((out / "figs" / name).resolve())
            l["orig"].append({"src": "figs/" + name, "n": f.get("n", ""), "w": im.width, "h": im.height,
                              "caption": f.get("caption", ""), "credit": f["credit"], "page": f.get("page", "")})
        for k in p.get("figure_links", []):
            l = lessons.get(k.get("lesson"))
            if l and k.get("url", "").startswith("http"):
                l["links"].append({"label": k.get("label", k["url"]), "url": k["url"]})
        glossary += p.get("glossary", [])
        parts.append({"key": p["key"], "title": p["title"], "chapters": p.get("chapters", ""),
                      "lessons": list(lessons.values())})

    for g in glossary:
        if g.get("ref") and g["ref"] not in seen:
            warns.append(f"glossary '{g.get('term')}': ref {g['ref']} is not a lesson")
    if errors:
        fail(errors)
    order = book.get("partOrder")
    if order:
        parts.sort(key=lambda p: order.index(p["key"]) if p["key"] in order else 99)
    dedup = {}
    for g in glossary:
        dedup.setdefault(g["term"], g)
    book["parts"] = parts
    book["glossary"] = sorted(dedup.values(), key=lambda g: g["term"])
    theme = book.pop("theme", "")
    blob = json.dumps(book, ensure_ascii=False).replace("</", "<\\/")
    html = shell.replace("__TITLE__", book["title"]).replace("/*__THEME__*/", theme).replace("/*__BOOK__*/null", blob)
    (out / "index.html").write_text(html, encoding="utf-8")
    for w in warns:
        print("WARN", w, file=sys.stderr)
    n = sum(len(p["lessons"]) for p in parts)
    print(json.dumps({"lessons": n, "parts": len(parts), "figures": len(filemap),
                      "minutes": sum(l.get("minutes", 4) for p in parts for l in p["lessons"]),
                      "bytes": len(html.encode("utf-8")), "files": filemap}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
