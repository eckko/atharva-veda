# VERIFY log: atharvaveda

Dated log of the verification stage (skill: verify-vedic-book-reference). Append only.

## 2026-10-17 (branch docs/2026-10-17/version-2)
- Inventory (`inventory.py`): base = `text/` (160 Sanskrit files, `ID | Devanagari`, extraction contract format), `toc.md`, `sources.md`, `ISSUES.md` present. Unknown-looking files were the extraction tooling written by Claude (`tools/parse_dharmicdata.py`, `fetch_s1.sh`, `build_toc.py`, `reference/tools/check_extraction.py`, an untracked `__pycache__`): not book text, ignored.
- Second edition: not available (owner answer). Comparison step skipped.
- Note: branch docs/2026-10-17/version-1 was merged to main (PR 1) before this run; this work is on a new branch from main.

### Step 2 completeness (structure_check.py, check_extraction.py)
- 20 parts, 734 chapters with text, 6,169 verse numbers, 11,121 lines. check_extraction.py: 0 errors, 1 warning (double space in 011.003.129, text as in source).
- FLAG part 020: chapters 3 and 13 missing (source S1 has only the header line). Cannot be repaired from memory or another edition; blocked. Fix needs the mantra text of 020.003 and 020.013 from a second source.
- FLAG part 008: "last chapter 010 ends without a danda" is a symptom of finding F1 below, not a true truncation.
- F1 (extraction defect in 008.010, 67 lines): S1 writes verse-end markers there as `॥N॥(M)` or `।।N।।(M)` with a running number in brackets. The extraction parser did not recognise them, so the markers stay inside the text lines and the verse grouping is wrong (for example 008.010.12 holds 12 lines a to l, verse numbers 12, 13, 1..10 in the source). Only 008.010 is affected (25 lines with `(N)`). Proposed fix, not applied: let the parser accept `(M)` after the marker for this sukta and regenerate 008.010 IDs. This renumbers IDs of a finished sukta, so it needs the owner's approval.
