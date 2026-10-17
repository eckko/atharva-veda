#!/usr/bin/env python3
"""Parse DharmicData AtharvaVeda JSON (source S1) into the FORMAT.md layout.

Input : a directory holding atharvaveda_kaanda_1.json ... _20.json
        (fetch them with fetch_s1.sh).
Output (in OUT_DIR):
  text/*.md          Sanskrit, one "ID | text" line per source line
  sukta_meta.json    per sukta: title and header lines, interior header lines
  issues.json        doubts: [line ID, kind, what]
  manifest.json      file layout per kanda

Nothing is corrected. Text is copied from the source; a trailing verse
number (॥१॥) becomes the closing ॥; text is NFC-normalised. Lines that are
not mantra text (titles, rishi/devata/chandas lines, paryaya markers, a
colophon, a footer in Latin letters) are kept in sukta_meta.json or
issues.json, not in the text files.

Run:  python3 -I parse_dharmicdata.py RAW_DIR OUT_DIR
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
# a verse-end marker at the end of a line: danda(s), number, danda(s)
END_NUM = re.compile(r"\s*[॥।]{1,2}\s*([०-९]+)\s*[॥।]{0,2}([0-9]?)\s*$")
STD_END = re.compile(r"॥\s*[०-९]+\s*॥\s*$")
END_PLAIN = re.compile(r"॥\s*$")       # closing ॥ without a number
ACCENTS = "॒॑॓॔"  # udatta, anudatta, and the two others
LATIN = re.compile(r"[A-Za-z]")
LINE_LIMIT = 1000
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def is_verse_line(line):
    return bool(END_NUM.search(line)) or any(c in line for c in ACCENTS)


def split_sukta(text):
    """Return (header, body, interior, latin).

    header   leading lines without accents or marker (title, rishi line ...)
    body     mantra lines
    interior non-mantra lines found between mantra lines: [(index in body
             where it occurred, text)]
    latin    mantra lines containing Latin letters (none expected)
    """
    lines = [unicodedata.normalize("NFC", x).strip() for x in text.split("\n")]
    lines = [x for x in lines if x]
    latin = []
    start = 0
    while start < len(lines) and not is_verse_line(lines[start]):
        start += 1
    header, rest = lines[:start], lines[start:]
    body, interior = [], []
    for line in rest:
        if is_verse_line(line):
            body.append(line)
            if LATIN.search(line):
                latin.append(line)
        else:
            interior.append((len(body), line))
    return header, body, interior, latin


def group_verses(body):
    """Group body lines into verses. Returns [(label or None, lines)]."""
    out, cur = [], []
    for line in body:
        cur.append(line)
        found = END_NUM.search(line)
        if found:
            out.append((found.group(1).translate(DIGITS), cur))
            cur = []
        elif END_PLAIN.search(line):
            out.append((None, cur))
            cur = []
    if cur:
        out.append((None, cur))
    return out


def clean(line):
    """Replace a trailing verse number by the closing ॥ (text unchanged
    otherwise)."""
    if END_NUM.search(line):
        return END_NUM.sub(" ॥", line)
    return line


def main(raw_dir, out_dir):
    raw_dir, out_dir = Path(raw_dir), Path(out_dir)
    (out_dir / "text").mkdir(parents=True, exist_ok=True)
    meta, issues, manifest, parts = {}, [], {}, {}
    latin_seen = {}
    for kanda in range(1, 21):
        data = json.load(open(raw_dir / f"atharvaveda_kaanda_{kanda}.json",
                              encoding="utf8"))
        data.sort(key=lambda x: x["sukta"])
        rows_by_sukta = {}
        for item in data:
            s = item["sukta"]
            pid = f"{kanda:03d}.{s:03d}"
            header, body, interior, latin = split_sukta(item["text"])
            for text in latin:
                latin_seen.setdefault(text, []).append(pid)
            groups = group_verses(body)
            labels = [g[0] for g in groups]
            numeric = [int(x) for x in labels if x]
            good = (None not in labels and numeric == sorted(set(numeric)))
            rows, nonstd = [], []
            if not good and groups:
                shown = " ".join(x or "-" for x in labels[:40])
                issues.append((pid, "numbering",
                               "source verse numbers are repeated, reordered "
                               "or missing, so position 1..n is used as the "
                               "verse number; source numbers in order: "
                               f"{shown}{' ...' if len(labels) > 40 else ''}"))
            for index, (label, vlines) in enumerate(groups, start=1):
                v = label if good else str(index)
                if len(vlines) > len(LETTERS):
                    issues.append((f"{pid}.{v}", "other",
                                   f"{len(vlines)} lines under one verse "
                                   "number; check marker"))
                for j, line in enumerate(vlines):
                    suffix = "" if len(vlines) == 1 else LETTERS[j % 26]
                    rows.append((f"{pid}.{v}{suffix}", clean(line)))
                if STD_END.search(vlines[-1]) is None and label is not None:
                    nonstd.append(f"{v}")
                found = END_NUM.search(vlines[-1])
                if found and found.group(2):
                    issues.append((f"{pid}.{v}", "possible-typo",
                                   f"stray character '{found.group(2)}' after "
                                   "the verse-end marker in source; removed "
                                   "from the text along with the marker"))
            if nonstd:
                issues.append((pid, "possible-typo",
                               f"{len(nonstd)} verse-end marker(s) not in the "
                               "standard ॥N॥ form in source (e.g. missing or "
                               "doubled danda); verses: "
                               f"{' '.join(nonstd[:12])}"
                               f"{' ...' if len(nonstd) > 12 else ''}"))
            if good and numeric:
                gaps = [n for n in range(numeric[0], numeric[-1] + 1)
                        if n not in numeric]
                if gaps:
                    issues.append((pid, "numbering",
                                   f"source skips verse number(s) {gaps}"))
                if numeric[0] != 1:
                    issues.append((pid, "numbering",
                                   f"first verse number in source is "
                                   f"{numeric[0]} (numbering continues from "
                                   "an earlier sukta or section)"))
            if not groups:
                issues.append((pid, "missing",
                               "source has the header line(s) but no mantra "
                               "text for this sukta"))
            if not header:
                issues.append((pid, "other",
                               "no title or header line in source"))
            for pos, text in interior:
                issues.append((pid, "other",
                               f"non-mantra line left out of text (before "
                               f"mantra line {pos + 1}): {text}"))
            meta[pid] = {"kanda": kanda, "sukta": s, "header": header,
                         "interior": [[p, t] for p, t in interior],
                         "verses": len(groups), "lines": len(rows)}
            rows_by_sukta[s] = rows
        parts[kanda] = rows_by_sukta
    for text, where in latin_seen.items():
        issues.append((where[0] if len(where) == 1 else f"{where[0]}..",
                       "other",
                       f"Latin-letter line in source left out (in "
                       f"{len(where)} sukta(s): {', '.join(where[:6])}"
                       f"{' ...' if len(where) > 6 else ''}): {text}"))

    for kanda, rows_by_sukta in parts.items():
        total = sum(len(r) for r in rows_by_sukta.values())
        if total < LINE_LIMIT:
            name = f"p{kanda:03d}.md"
            lines = [f"{i} | {t}" for r in rows_by_sukta.values()
                     for i, t in r]
            (out_dir / "text" / name).write_text("\n".join(lines) + "\n",
                                                 encoding="utf8")
            manifest[kanda] = {"layout": "part", "file": f"text/{name}",
                               "lines": total}
        else:
            files = {}
            for s, r in rows_by_sukta.items():
                if not r:
                    continue
                name = f"ch{kanda:03d}.{s:03d}.md"
                lines = [f"{i} | {t}" for i, t in r]
                (out_dir / "text" / name).write_text("\n".join(lines) + "\n",
                                                     encoding="utf8")
                files[s] = name
            manifest[kanda] = {"layout": "chapter", "lines": total,
                               "files": files}
    for name, obj in (("sukta_meta.json", meta), ("issues.json", issues),
                      ("manifest.json", manifest)):
        json.dump(obj, open(out_dir / name, "w", encoding="utf8"),
                  ensure_ascii=False, indent=1)
    print(len(meta), "suktas", sum(m["verses"] for m in meta.values()),
          "verses", len(issues), "issues")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
