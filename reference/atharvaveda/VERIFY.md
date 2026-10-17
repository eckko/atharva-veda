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

### Step 3 word check and proofreading (2026-10-17)
- `word_check.py`: stray characters, suspected typos and the metre list are in `checks/`. The metre output (3,922 lines) is not used: the tool's metre model does not fit Vedic metres, so it was set aside (`checks/metre-not-used.tsv`).
- AI proofreading: 4 packs, `checks/PROOFREAD.md`, `checks/proposals.tsv` (18 proposals). Sample error rate 1.4% of 70 sampled lines (one error, 020.071.10). Proposals only; `text/` was not edited. A printed edition is needed to settle them.
- Proposals include 5 stray private-use characters in 004.001 (U+E003).

### Step 5 layers pilot: parts 017, 014, 001 (owner's choice)
- 40 chunks, 322 units, 647 Sanskrit lines (p001: 35 sūktas, 291 lines; p014: 2 sūktas, 280 lines; p017: 1 sūkta, 76 lines). All other parts (17 of 20 kāṇḍas; 710 of the 750 planned chunks in `layers-work/PLAN.json`) are not started.
- Pipeline per chunk: AI draft (Sonnet 5.5) -> `check_chunk.py` (0 errors on all 40) -> independent AI review (another agent that had not seen the draft's reasoning) -> `apply_review.py` -> `merge_chunks.py` -> `write_layers.py`. `text/pNNN-sandhi.md`, `-hindi.md`, `-english.md` have exactly the IDs and line counts of `pNNN.md`; `check_extraction.py`: 0 errors.
- The reviewers found real errors in the drafts (for example reversed senses, Hindi words that differ from the English, grammar labels): 61 errors and 380 minor issues (reviewers' counts) across the 40 chunks. Most were patched; a few points per chunk are left as doubts in each `chunk*_review.json` and in the chunk's `notes` fields. These layers are therefore **reviewed drafts only, not checked by a person**.
- Known open points (no `text/` change made): a probable unflagged typo `avasṛṣṭāḥ vadhāya` (017.001.28); `indrāṇye'tu` (001.027, unit 4) read as `indrāṇy etu`; silent corrections `panthano`, `jatavedāḥ`, `imaṃ` (014.001); `vacaspate` for `vācaspate` (001.002); `vīryāvān` as one word or two (014.001.37). In 001.001.1 the Hindi still renders "thrice-seven" as "इक्कीस" (contested count; fixed only in 001.027).
- Feed: `feed/atharvaveda-p001.epub`, `-p014.epub`, `-p017.epub` (+ `.map.json`, `.txt` parts) built with `build_feed.py` and checked with the template's `extract_book.py` (291, 280, 76 line numbers read back, 0 missing).
