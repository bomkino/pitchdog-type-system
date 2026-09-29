# Migration from 2.x to 3.0.0

3.0.0 changes existing web, social, deck and YouTube roles, so it is a major release. It also adds a spacing scale and a subtitle layer, which change nothing until you use them. Fonts, anchors, families, weights, line heights and tracking are unchanged. This is not the older pre-13 v3 line; see `MIGRATION-v3-to-v13.md` for that.

## What changes

**Reading measures.** The lead and body roles now carry the calibrated measures from `WEB-TEXT-WRAPPING.md`. The old role widths set 87 to 102 characters per line in PD Body on a laptop, past the 80-character WCAG ceiling.

| Role | 2.x | 3.0.0 | Measured characters per line |
| --- | --- | --- | --- |
| `lead.hero` | 44ch | 38ch (`narrow`) | about 52 |
| `lead.section` | 56ch | 48ch (`intro`) | about 64 |
| `body.reading` | 64ch | 45ch (`reading`) | about 63 |
| `body.default` | 68ch | 48ch (`default`) | about 72 |
| `body.compact` | 72ch | 52ch (`wide`) | about 70 |
| `body.small` | 74ch | 52ch (`wide`) | about 70 |

`--pd-measure-reading`, `--pd-measure-default` and `--pd-measure-compact` (and so `.pd-prose`) follow the same values, so they no longer disagree with `data-pd-measure="reading"`.

**Social small text.** A 1080-pixel post shows at about a third of its size in a phone feed, where the old small roles landed at 4 to 9 px. They now land at about 9 to 13 px.

| Role | 2.x | 3.0.0 | Portrait 1080 × 1350 |
| --- | --- | --- | --- |
| `social.subhead` | min(3.4cqi, 2.9cqb) | min(4.4cqi, 3.9cqb) | 37 → 48 px |
| `social.body` | min(2.32cqi, 1.95cqb) | min(3.4cqi, 3cqb) | 25 → 37 px |
| `social.label` | min(1.75cqi, 1.45cqb) | min(2.8cqi, 2.5cqb) | 19 → 30 px |
| `social.metadata` | min(1.38cqi, 1.12cqb) | min(2.6cqi, 2.4cqb) | 15 → 28 px |
| `social.credit` | min(1.72cqi, 1.4cqb) | min(2.4cqi, 2.2cqb) | 19 → 26 px |

Copy limits are unchanged.

**Deck present sizes.** Slides are read from across a room, and body text at present density was 15 pt in PowerPoint. Present sizes now step up; read density is unchanged.

| Role | 2.x | 3.0.0 | On a 1080-pixel slide |
| --- | --- | --- | --- |
| `deck.headline` | min(3.24cqi, 5.4cqb) | min(3.6cqi, 6cqb) | 58 → 65 px |
| `deck.lead` | min(2.16cqi, 3.6cqb) | min(2.4cqi, 4cqb) | 39 → 43 px |
| `deck.body` | min(1.68cqi, 2.8cqb) | min(2.04cqi, 3.4cqb) | 30 → 37 px |
| `deck.bullet` | min(1.8cqi, 3cqb) | min(2.16cqi, 3.6cqb) | 32 → 39 px |
| `deck.quote` | min(3.12cqi, 5.2cqb) | min(3.36cqi, 5.6cqb) | 56 → 60 px |
| `deck.kicker` | min(1.32cqi, 2.2cqb) | min(1.44cqi, 2.4cqb) | 24 → 26 px |
| `deck.label` | min(1.38cqi, 2.3cqb) | min(1.56cqi, 2.6cqb) | 25 → 28 px |
| `deck.data` | min(1.38cqi, 2.3cqb) | min(1.56cqi, 2.6cqb) | 25 → 28 px |
| `deck.source` | min(1.2cqi, 2cqb) | min(1.32cqi, 2.2cqb) | 22 → 24 px |
| `deck.footer` | min(1.08cqi, 1.8cqb) | min(1.2cqi, 2cqb) | 19 → 22 px |

The present floor rises from 2 % to 2.2 % of the slide height. Copy limits are unchanged.

**YouTube small text.** A thumbnail is seen at about a tenth of its size.

| Role | 2.x | 3.0.0 | At a 384 px preview |
| --- | --- | --- | --- |
| `youtube.support` | min(2.9cqi, 4cqb) | min(4.06cqi, 5.6cqb) | 8.6 → 12.1 px |
| `youtube.kicker` | min(1.8cqi, 2.5cqb) | min(3.05cqi, 4.2cqb) | 5.4 → 9.1 px |
| `youtube.badge` | min(1.9cqi, 2.65cqb) | min(3.19cqi, 4.4cqb) | 5.7 → 9.5 px |
| `youtube.credit` | min(1.45cqi, 2cqb) | min(2.9cqi, 4cqb) | 4.3 → 8.6 px |

**New, opt-in.** `data-pd-flow` and the `--pd-space-*` and `--pd-deck-space-*` steps (`SPACING.md`), and the subtitle layer (`SUBTITLES.md`). Nothing changes until markup uses them. `pitchdog-system.css` now bundles the subtitle layer.

## Steps

1. Change the pin to `#v3.0.0` and reinstall.
2. Web: paragraphs in lead and body roles get narrower. Check layouts that relied on a paragraph filling its column; if one genuinely needs a wider line, set `data-pd-measure` rather than overriding `max-inline-size`.
3. Social: re-export fixed-canvas posts and check them at phone width. Posts that were close to their line limits may now need shorter copy; cut words rather than shrinking the role.
4. Figma: update the five `Social / …` styles from `docs/figma-style-map.csv`.
5. Decks: re-check slides that were close to their limits at present density; split a slide or cut words rather than switching a live deck to read density. In Keynote, PowerPoint and Google Slides, take the new point sizes from `DECKS.md`.
6. YouTube: re-export thumbnails and check them at preview size; the kicker, badge and credit are much larger, so trim them if they now crowd the title.
7. Figma: update the `Deck / …` and `YouTube / …` styles, and add the `Subtitle / …` styles, from `docs/figma-style-map.csv`.
8. Optional: replace hand-set margins between text blocks with `data-pd-flow`, and gaps inside slides with `--pd-deck-space-*`.
9. Replace any installed copy of the `pitchdog-type-system` skill with the one in the v3.0.0 Release. It now checks characters per line, size at delivery, colliding display lines, flow spacing and subtitles.
