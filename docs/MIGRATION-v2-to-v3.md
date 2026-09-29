# Migration from 2.x to 3.0.0

3.0.0 changes two sets of existing roles, so it is a major release. Fonts, anchors, families, weights, line heights and tracking are unchanged. This is not the older pre-13 v3 line; see `MIGRATION-v3-to-v13.md` for that.

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

## Steps

1. Change the pin to `#v3.0.0` and reinstall.
2. Web: paragraphs in lead and body roles get narrower. Check layouts that relied on a paragraph filling its column; if one genuinely needs a wider line, set `data-pd-measure` rather than overriding `max-inline-size`.
3. Social: re-export fixed-canvas posts and check them at phone width. Posts that were close to their line limits may now need shorter copy; cut words rather than shrinking the role.
4. Figma: update the five `Social / …` styles from `docs/figma-style-map.csv`.
5. Replace any installed copy of the `pitchdog-type-system` skill with the one in the v3.0.0 Release. It now checks characters per line, size at delivery and colliding display lines.
