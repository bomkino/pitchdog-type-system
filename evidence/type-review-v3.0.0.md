# Type review — v3.0.0

Date: 29 September 2026

A review of sizes, leading, tracking, measure and spacing in 2.2.0, done by rendering the specimen, the starter deck and test pages in Chromium (Playwright 1.56) and reading font metrics with fontTools. It led to the two role changes in 3.0.0.

## Findings that changed roles

**Line length.** `ch` is the width of the zero, and in PD Body one `ch` holds about 1.36 average characters of English. The 2.2.0 role widths therefore set far more text per line than their numbers suggest. Median characters per rendered line at a 1440 px viewport, same English paragraph:

| Role | 2.2.0 | 3.0.0 |
| --- | --- | --- |
| `lead.hero` | 66 (44ch) | 57 (38ch) |
| `lead.section` | 73 (56ch) | 65 (48ch) |
| `body.reading` | 92 (64ch) | 65 (45ch) |
| `body.default` | 102 (68ch) | 74 (48ch) |
| `body.compact` | 99 (72ch) | 70 (52ch) |
| `body.small` | 102 (74ch) | 72 (52ch) |

At 390 px nothing changes, because the column is narrower than every measure.

**Social small text.** Computed size on the canvas, and in brackets the size at a 390 px phone-feed width:

| Role | 2.2.0 square | 2.2.0 portrait | 3.0.0 square | 3.0.0 portrait |
| --- | --- | --- | --- | --- |
| `social.subhead` | 31 (11.3) | 37 (13.3) | 42.1 (15.2) | 47.5 (17.2) |
| `social.body` | 21 (7.6) | 25 (9.0) | 32.4 (11.7) | 36.7 (13.3) |
| `social.label` | 16 (5.7) | 19 (6.8) | 27.0 (9.8) | 30.2 (10.9) |
| `social.metadata` | 12 (4.4) | 15 (5.4) | 25.9 (9.4) | 28.1 (10.1) |
| `social.credit` | 15 (5.5) | 19 (6.7) | 23.8 (8.6) | 25.9 (9.4) |

Story matches portrait. Landscape (1200 × 630) is limited by its height and is meant for display and headline only.

## Findings left unchanged

- **Display leading.** PD Head's ascender (0.75 em) plus descender (0.23 em) is 0.98 em, so at `display.hero`'s 0.88 a descender directly above an ascender will touch. The specimen hero does this: the p of "pitch’s" meets the f of "friend". At 0.94 it still touches. The tight leading is part of the voice, so 3.0.0 keeps it and the skill now checks display lines for collisions.
- **Deck present density.** `deck.body` is 30 px on a 1080 slide, 15 pt in PowerPoint and 11 pt in Google Slides, which is small for a room. A size change is a taste decision for the maintainers.
- **Spacing.** Apart from `p + p { margin-block-start: 1em }`, the system has no spacing scale for the space between a heading and its text or between blocks. Pages make their own.
- **Scale, tracking and body leading.** Display sizes step by about 1.15–1.3 on phones and 1.3–1.45 on desktop, tracking tightens with size and relaxes below 40rem, uppercase Eyebrow gets positive tracking, and body leading of 1.45–1.58 suits the fonts' 0.47 em x-height. No change.

No browser console or page errors in any specimen view.
