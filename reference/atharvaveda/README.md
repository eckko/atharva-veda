# Atharvaveda Saṃhitā (Śaunaka): raw extracted source bank

Stage 1 (extraction) is done and stage 2 (verification) has started: see `VERIFY.md`. Sandhi/Hindi/English AI draft layers exist for parts 001, 014 and 017 only (`text/p001-*.md` etc., feed in `feed/`); they are reviewed drafts, not human-checked. This folder holds the raw text, not a finished edition. Nothing here has been proofread, and it comes from a single source (S1) that has not been compared with a printed edition.

Read, in order: FORMAT.md (file and line format), toc.md (structure), STATUS.md (what is done), sources.md (where text came from), ISSUES.md (known doubts), sukta-headers.md (title and ṛṣi/devatā/chandas lines of each sūkta).

Layout: kāṇḍa = part, sūkta = chapter, mantra = verse; IDs are `PPP.CCC.V` (3 digits because kāṇḍas 6, 7 and 20 have more than 99 sūktas). Kāṇḍas 1 to 19 are `text/pNNN.md`; kāṇḍa 20 is one file per sūkta `text/ch020.CCC.md`. The text keeps the Vedic accent marks of the source.

Rebuild from source: `sh tools/fetch_s1.sh RAW_DIR`, then `python3 -I tools/parse_dharmicdata.py RAW_DIR OUT_DIR`, then `python3 -I tools/build_toc.py OUT_DIR .` (the parser writes `text/`, `sukta_meta.json`, `issues.json` into OUT_DIR). ISSUES.md and STATUS.md were generated from `issues.json` and `sukta_meta.json`.

Rules for anyone editing here:
- Text lines come only from sources listed in sources.md; never from memory.
- Do not rename files or change line IDs of finished chapters.
- Record every doubt in ISSUES.md; fix text only in a later, explicit proofreading stage.
- Run `python3 reference/tools/check_extraction.py reference/atharvaveda` before every commit.
- Branch pattern: `docs/YYYY-MM-DD/version-N`; push new branches only; the owner merges.

How to continue: open STATUS.md, take the first chapter not marked extracted (all are, except 020.003 and 020.013, whose mantra text is missing in S1), or add a second source, then follow the skill `/extract-vedic-book-web` (or the steps in FORMAT.md and sources.md if the skill is not available).
