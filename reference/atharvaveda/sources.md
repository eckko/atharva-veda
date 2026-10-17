# Sources: atharvaveda

| ID | Name | URL | Edition / editor / year | Script | Licence | Covers | Fetched how | Quality note | Role |
|---|---|---|---|---|---|---|---|---|---|
| S1 | DharmicData, folder `AtharvaVeda` (Śaunaka Saṃhitā, 20 JSON files, one per kāṇḍa) | https://github.com/bhavykhatri/DharmicData/tree/main/AtharvaVeda (raw files: https://raw.githubusercontent.com/bhavykhatri/DharmicData/main/AtharvaVeda/atharvaveda_kaanda_N.json) | text credited to the Vedic Heritage Portal (vedicheritage.gov.in); printed edition and editor not named in the dataset | Devanāgarī with Vedic accent marks | repo: ODbL v1.0 (per its README); licence of the underlying portal text unknown | all 20 kāṇḍas, 736 sūktas | `curl` from raw.githubusercontent.com (tools/fetch_s1.sh), 2026-10-17 | one JSON record per sūkta (`kaanda`, `sukta`, `text`); text holds title, ṛṣi/devatā/chandas lines and mantras; some marker typos, 2 sūktas without mantra text, see ISSUES.md | primary |

Raw files are not committed (licence of the portal text unknown); fetch them with `tools/fetch_s1.sh DIR`. SHA-256 of the files fetched on 2026-10-17:

```
c91ba777a1a160602b4a3966adeac08e7d64108884531bf59e0f77c2cd5c4e07  atharvaveda_kaanda_1.json
09f055f88175028bae6e496d0f896520e1c3fd5356869623a7e8a0c48b5431b1  atharvaveda_kaanda_2.json
3edc9e271225e1412d5c269a328f3016c3aeb7a996bd88389e4014ab7da6ecca  atharvaveda_kaanda_3.json
1fad564633fdfecfc07cfb810d4e9f4cb8b22bd25985274030b8676261777f7f  atharvaveda_kaanda_4.json
64150bb4886ef8e9867f04f34ebd1dda492d0e9f2071ee387f0d0ec597ac44f3  atharvaveda_kaanda_5.json
c2f93415909c80d12bb74790754298846dfaf150d0e94d962a1c2dee4dbbdd23  atharvaveda_kaanda_6.json
149768ac89f253402f57ed966e55b5abe3194d25f7cab2e7848e78c2a463e3f7  atharvaveda_kaanda_7.json
7551e75ae50d0effa1ffcf0cd8b86b90f0ef70f8abd0bfa7878f21caab9de221  atharvaveda_kaanda_8.json
2950bbf1bc097a2fc752a27e497deedffaa0944cc13823052820e03c5cd8b1ee  atharvaveda_kaanda_9.json
7da3422d6859c6f46961b78a546517dac643a557042418dfea2566c61dc72b42  atharvaveda_kaanda_10.json
f58218eb1a66192f844b0980263995f85dac9a234b1747e7c0731598d819dc1f  atharvaveda_kaanda_11.json
a3c62863895c999552642419894bf730253f494a9c3fe381489b482fb154f2c1  atharvaveda_kaanda_12.json
68df3f2eb9113e83e15df8645514c15249a281cd24f75a7972eb7d9235a4e065  atharvaveda_kaanda_13.json
498444b6085e03fa8264bca026952ddd5e7425d52f3d72d259cab16b30d8a7cb  atharvaveda_kaanda_14.json
e2f07d135c1aa198969b9127645e15620cd2bbc1d5b4835872af449fe0f8ce22  atharvaveda_kaanda_15.json
e6f2c80296b647084659a85fecb48eef106ce1c91a11cbc1b10b9d5a148ff142  atharvaveda_kaanda_16.json
bd44f0ab41a410c30b25b3d6efaeed59fb21c0cad24412b6f9af460282775fb4  atharvaveda_kaanda_17.json
5e41804e28f2f5858c36bb9799a89d93d64e08830f22629f5d6332e2a85dc938  atharvaveda_kaanda_18.json
5c5d0c66e986c378304caf050d93095c1c987ca3d843903524ef0bd37c5ce4bd  atharvaveda_kaanda_19.json
3885cccab8c5c4e5b746a3088761ad09c5e9ac0b184591c71d1c2cb11706f47f  atharvaveda_kaanda_20.json
```

Not reachable from the shell in this session (blocked): GRETIL, Sanskrit Documents, Sanskrit Wikisource, sanskritlibrary.org (TITUS/Sanskrit Library TEI XML edition of the Śaunaka Saṃhitā, CC BY-NC-SA 3.0), archive.org, vedicheritage.gov.in. A second source for cross-checking would come from one of these (download by the owner, then attach or add to the repo).

Notes on conversion: none (text is already Devanāgarī). Text is NFC-normalised; a trailing verse number `॥N॥` is replaced by the closing `॥`; title, ṛṣi/devatā/chandas lines, paryāya marks and a colophon are kept out of the text files (sukta-headers.md and ISSUES.md).
