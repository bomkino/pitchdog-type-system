# Font naming

From v2.0.0 every font file in `assets/fonts/` and `pitchdog-font-handoff/` carries the same family names the CSS uses, so desktop apps, Figma and native platforms show the fonts the way the web does. Glyphs, metrics, axes and kerning are byte-for-byte the FontBlind v13 originals; only naming and style-linking metadata changed.

## Families

| Family | PostScript prefix | Files |
| --- | --- | --- |
| PD Head | `PDHead` | `pd-head*` (not `pd-head-alt*`) |
| PD Head Alt | `PDHeadAlt` | `pd-head-alt*` |
| PD Body | `PDBody` | `pd-body*` (not `pd-body-alt*`) |
| PD Body Alt | `PDBodyAlt` | `pd-body-alt*` |
| PD Eyebrow | `PDEyebrow` | `pd-eyebrow*` |

## Variable fonts

| File | Family | Style | PostScript name | Instance prefix |
| --- | --- | --- | --- | --- |
| `pd-head` | PD Head | Regular | `PDHead-Regular` | `PDHead` |
| `pd-head-alt` | PD Head Alt | Regular | `PDHeadAlt-Regular` | `PDHeadAlt` |
| `pd-body-roman` | PD Body | Regular | `PDBody-Regular` | `PDBody` |
| `pd-body-italic` | PD Body | Italic | `PDBody-Italic` | `PDBodyItalic` |
| `pd-body-alt-roman` | PD Body Alt | Regular | `PDBodyAlt-Regular` | `PDBodyAlt` |
| `pd-body-alt-italic` | PD Body Alt | Italic | `PDBodyAlt-Italic` | `PDBodyAltItalic` |
| `pd-eyebrow`, `pd-eyebrow-site`, `pd-eyebrow-full` | PD Eyebrow | Regular | `PDEyebrow-Regular` | `PDEyebrow` |

PD Body and PD Body Alt Roman and Italic now share one family, so native font menus pair them as Regular and Italic of the same typeface. Named instances read `Bold`, `Bold Italic`, and so on, with PostScript names such as `PDBody-BoldItalic`. Head's instances cover both postures of its `ital` axis (`PDHead-Black`, `PDHead-BlackItalic`).

## Static fallbacks

Static files follow the standard four-style linking model:

- Regular (400) and Bold (700) sit in the base family, e.g. `PD Eyebrow` Regular, Italic, Bold, Bold Italic.
- Every other weight gets its own legacy family, e.g. `PD Eyebrow Book` Regular and Italic for 350.
- The typographic family (`name` ID 16) is always the base family and the typographic style (ID 17) is the full weight and posture, e.g. `Book Italic`, so modern apps group all weights under one family.
- Only 700 sets the Bold style bit; only italic files set the Italic bit.

Weight names: 100 Thin, 200 ExtraLight, 250 ExtraLight (PD Body's lightest-but-one master), 265 Thin (PD Head's lightest master), 300 Light, 350 Book, 400 Regular, 500 Medium, 600 SemiBold, 700 Bold, 800 ExtraBold, 900 Black.

Every face now has a unique PostScript and full name. The v13 collision between Eyebrow 350 and 400 is gone: they are `PDEyebrow-Book` and `PDEyebrow-Regular`.

## Keeping it true

`tools/normalize_font_names.py` applies this scheme and, with `--check`, fails on any file that drifts from it or any two faces that share a PostScript name. CI runs the check on every push. `tools/compare_font_payloads.py` proves a before/after pair differs only in naming metadata; `evidence/font-name-normalization-v2.0.0.json` records that proof for every file in this release.
