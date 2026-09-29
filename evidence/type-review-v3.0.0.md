# Type review — v3.0.0

Date: 29 September 2026

A review of sizes, leading, tracking, measure and spacing in 2.2.0, done by rendering the specimen, the starter deck and test pages in Chromium (Playwright 1.56) and reading font metrics with fontTools. It led to the role changes and additions in 3.0.0.

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

**Deck present density.** `deck.body` was 30 px on a 1080 slide, 15 pt in PowerPoint and 11 pt in Google Slides, small for a room. Present sizes step up by about 1.07 to 1.21; read density is unchanged. On a 1080 slide: headline 58.3 → 64.8 px, lead 38.9 → 43.2, body 30.2 → 36.7, bullet 32.4 → 38.9, quote 56.2 → 60.5, kicker 23.8 → 25.9, label and data 24.8 → 28.1, source 21.6 → 23.8, footer 19.4 → 21.6. In the starter deck at both densities and on both canvases, no element leaves a slide's safe area.

**YouTube small text.** A 3840 × 2160 thumbnail is seen about 384 px wide. At that size `youtube.support` was 8.6 px and kicker, badge and credit 4.3 to 5.7 px. They now land at 12.1, 9.1, 9.5 and 8.6 px.

## Additions

**Spacing.** 2.2.0 had no spacing beyond `p + p { margin-block-start: 1em }`. 3.0.0 adds a web scale, a flow contract and a deck scale. Measured gaps in a test article with `data-pd-flow` at 1440 px: kicker → chapter 8 px, chapter → lead 36, text → text 20 (1em), text → subsection 64, subsection → text 20, text → section 112, section → text 36, title card → text 12. At 390 px the fluid steps shrink (text → section 65 px, chapter → lead 24).

**Subtitles.** Candidates from the family were rendered on a mid-grey-to-white gradient frame in the cinema style (yellow on black at 70 %): Body 400 and 600, Body Alt 400 and 600, Body Italic and Eyebrow. Judged by eye, Body 600 kept the clearest counters and the most even colour through the translucent box, and Body 400 looked thin against it. Measured at 64 px on the same sentence, Body Alt sets 2 % wider than Body with no gain in legibility, and Eyebrow is monospaced and sets 27 % wider, which costs about a fifth of the characters per line and reads as a label, not speech. Body 600 Italic carries narration, and Body Alt 700 the short vertical punch captions.

Measured in Chromium: line height is 7.08 % of the frame height on 16:9, 4:3 and 1:1 frames and 4.18 % on 9:16 (BBC ranges 7–8 % and 3.9–4.5 %). With one element per line, line boxes abut exactly (no gap, no overlap) at every tested size; an inline box with `box-decoration-break` left 1–2 px gaps from rounding, so the layer sets each line as its own block. Characters that fit a line of mixed English: 45 on 16:9, 44 on 4:3, 32 on 1:1 and 31 on 9:16, so the frames publish 42, 42, 30 and 28. Contrast of the boxed styles composited over pure white: broadcast 10.4:1, cinema 6.2:1.

## Findings left unchanged

- **Display leading.** PD Head's ascender (0.75 em) plus descender (0.23 em) is 0.98 em, so at `display.hero`'s 0.88 a descender directly above an ascender will touch. The specimen hero does this: the p of "pitch’s" meets the f of "friend". At 0.94 it still touches. The tight leading is part of the voice, so 3.0.0 keeps it and the skill now checks display lines for collisions.
- **Scale, tracking and body leading.** Display sizes step by about 1.15–1.3 on phones and 1.3–1.45 on desktop, tracking tightens with size and relaxes below 40rem, uppercase Eyebrow gets positive tracking, and body leading of 1.45–1.58 suits the fonts' 0.47 em x-height. No change.

No browser console or page errors in any specimen view.
