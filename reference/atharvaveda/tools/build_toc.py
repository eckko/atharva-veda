#!/usr/bin/env python3
"""Write toc.md and sukta-headers.md from the parser output.

Usage: python3 -I build_toc.py PARSE_OUT_DIR BOOK_DIR
(PARSE_OUT_DIR holds sukta_meta.json and manifest.json from
parse_dharmicdata.py; BOOK_DIR is reference/atharvaveda.)
"""
import json
import re
import sys
from pathlib import Path

DEVA_NUM = re.compile(r"[०-९0-9]")


def title_of(header):
    """Sukta title = first header line, if it looks like a title."""
    if not header:
        return None
    first = header[0]
    if first.startswith("(") or DEVA_NUM.search(first):
        return None
    return first.rstrip("।| ").strip()


def short(text, limit=110):
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def main(parse_dir, book_dir):
    parse_dir, book_dir = Path(parse_dir), Path(book_dir)
    meta = json.load(open(parse_dir / "sukta_meta.json", encoding="utf8"))
    manifest = json.load(open(parse_dir / "manifest.json"))
    total_suktas = len(meta)
    total_verses = sum(m["verses"] for m in meta.values())
    out = [
        "# Atharvaveda Saṃhitā, Śaunaka recension (अथर्ववेदसंहिता, शौनकीया)",
        "",
        "- Author / compiler: traditionally attributed to the sages Atharvan "
        "and Aṅgiras; Śaunaka śākhā (vulgate recension)",
        "- Subject and purpose of the book: a collection of Vedic hymns and "
        "prose passages (mantras) for healing, protection, kingship, "
        "domestic rites, cosmology and speculation (inferred from the sukta "
        "titles and header lines of source S1; the text itself does not "
        "state a purpose)",
        "- Base edition: Vedic Heritage Portal (vedicheritage.gov.in) Śaunaka "
        "Saṃhitā text with Vedic accents, as published in the DharmicData "
        "JSON dataset (source S1 in sources.md). The printed edition behind "
        "the portal is not named in S1.",
        "- Mapping: part = kāṇḍa, chapter = sūkta, verse = mantra "
        "(IDs are `PPP.CCC.V`, 3-digit part and chapter because kāṇḍas 6, 7 "
        "and 20 have more than 99 sūktas)",
        f"- Totals: 20 parts, {total_suktas} chapters, {total_verses} verses "
        "extracted (traditional: unknown; Atharvaveda is usually described as "
        "about 730 hymns and about 6,000 mantras, not checked against a "
        "printed edition)",
        "",
        "Sūkta titles in the `Sanskrit name` column are the first line of each "
        "sūkta in S1 (`--` where S1 has none). The `Purpose` column is the "
        "start of S1's ṛṣi / devatā / chandas line (full lines in "
        "`sukta-headers.md`); S1 header text is the portal's, not ours. "
        "English names are not given (they would be our own translation). "
        "`Verses (traditional)` is `unknown` throughout because no edition "
        "with verse counts has been checked yet.",
        "",
        "Layout: kāṇḍas 1 to 19 each in one part file (`pNNN.md`, under "
        "1000 lines); kāṇḍa 20 has one file per sūkta (`chNNN.CCC.md`) "
        "because it has 1,536 lines.",
        "",
    ]
    heads = ["# Sūkta headers as in source S1",
             "",
             "One block per sūkta: ID, title line, then the ṛṣi / devatā / "
             "chandas lines exactly as S1 has them (NFC-normalised). "
             "Interior header lines (paryāya marks and "
             "metre notes inside a sūkta) are listed in `ISSUES.md`.",
             ""]
    by_kanda = {}
    for pid, m in meta.items():
        by_kanda.setdefault(m["kanda"], []).append((pid, m))
    for kanda in range(1, 21):
        items = by_kanda[kanda]
        n_s = len(items)
        n_v = sum(m["verses"] for _, m in items)
        info = manifest[str(kanda)]
        out += [f"## Part {kanda:03d}: काण्ड {kanda} (Kāṇḍa {kanda})", "",
                f"Purpose: sūktas {items[0][1]['sukta']} to "
                f"{items[-1][1]['sukta']} ({n_s} sūktas, {n_v} mantras "
                "extracted); no kāṇḍa-level purpose is stated in S1 "
                "(inferred: see sūkta titles)", "",
                "| Part | Chapter | Sanskrit name | English name | Purpose | "
                "Verses (extracted) | Verses (traditional) | File | Status |",
                "|---|---|---|---|---|---|---|---|---|"]
        for pid, m in items:
            title = title_of(m["header"])
            rest = m["header"][1:] if title is not None else m["header"]
            purpose = short(" ".join(rest)) if rest else "--"
            purpose = purpose.replace("|", "/")
            if info["layout"] == "part":
                file = info["file"]
            else:
                name = info["files"].get(str(m["sukta"]))
                file = f"text/{name}" if name else "--"
            status = "extracted" if m["verses"] else "blocked"
            out.append(f"| {kanda:03d} | {m['sukta']:03d} | "
                       f"{(title or '--').replace('|', '/')} | -- | "
                       f"{purpose} | {m['verses']} | unknown | {file} | "
                       f"{status} |")
            heads.append(f"## {pid}")
            heads.append("")
            heads.append(f"- title: {title or '--'}")
            for line in rest:
                heads.append(f"- header: {line}")
            heads.append("")
        out.append("")
    (book_dir / "toc.md").write_text("\n".join(out) + "\n", encoding="utf8")
    (book_dir / "sukta-headers.md").write_text("\n".join(heads) + "\n",
                                               encoding="utf8")
    print("toc.md and sukta-headers.md written")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
