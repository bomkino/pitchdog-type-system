# pitch.dog Type System v13 — Validation report

**Validation date:** 28 August 2026  
**Validation state at capture:** production candidate
**Font authority:** `FontBlind-Final-2026-08-28-v13.zip`

This report preserves the pre-release browser and font evidence captured on 28 August 2026. The package was later promoted to production; current release identity and repository checks belong to `RELEASE-RECEIPT.md`. The historical candidate label is not the current package state.

## Result

| Gate | Result |
|---|---:|
| Static release-contract checks | **237 / 237 passed** |
| Automated Chromium browser checks | **100 / 100 passed** |
| Browser console errors | **0** |
| Browser page errors | **0** |
| Font binaries in original standalone-review distributable | **0** |
| Embedded font payloads in distributable HTML | **0** |
| Runtime variable faces verified in web package | **7 / 7** |

The release passed every gate available in this environment.

## Font verification

The browser-local loader verified the exact byte size and SHA-256 digest of all seven approved variable WOFF2 files before loading them:

1. PD Head
2. PD Head Alt
3. PD Body Roman
4. PD Body Italic
5. PD Body Alt Roman
6. PD Body Alt Italic
7. PD Eyebrow

The audit also confirmed:

- every runtime face contains `₹`
- every runtime face contains `← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↩ ↪`
- PD Eyebrow contains 404 encoded characters
- PD Eyebrow contains all 34 audited currency symbols
- PD Eyebrow exposes genuine `wght`, `wdth`, and `ital` axes
- Body and Body Alt use separate authentic Roman and Italic variable files

Exact paths, sizes, hashes, axes, instances, metrics, character counts, currencies, and arrow coverage are recorded in `evidence/font-audit.json` in the complete Git checkout. The lean installed package instead ships `dist/pitchdog-font-runtime.json` with the runtime manifest.

## Head italic repair

The previous failure was not treated as a cosmetic issue. Version 13 drives Head posture through the font's actual `ital` axis:

```css
font-family: var(--pd-font-head-active);
font-style: normal;
font-variation-settings: "wght" 600, "ital" 1;
```

Automated validation proved all of the following:

- the upright specimen resolves to `ital: 0`
- the italic specimen resolves to `ital: 1`
- semantic Head emphasis resolves to `ital: 1`
- the feature-quote role resolves to `ital: 1`
- a pixel-difference comparison found a non-empty changed-glyph region between the upright and italic renderings

This is an actual change in the rendered outlines, not merely a CSS declaration that the browser ignored.

## Anchor policy verification

Every production role was checked against the approved source anchors.

### Head and Head Alt

- Weight: `265, 300, 400, 500, 600, 700, 900`
- Italic: static states use `0` or `1`

### Body and Body Alt

- Weight: `100, 250, 300, 400, 600, 700, 900`
- Posture: authentic Roman or authentic Italic file

### Eyebrow

- Weight: `100, 200, 300, 350, 400, 500, 600, 700, 800, 900`
- Width: `87.5` or `100`
- Italic: `0` or `1`

No semantic role uses an unanchored production weight, width, or static posture.

## System-surface verification

The static contract validated:

- **17** website roles
- **14** UI roles
- **9** social roles
- **7** YouTube roles
- **4** social canvases
- **5** YouTube canvases
- **12** governed arrow glyphs

The browser lab activated and rendered every view:

- Overview
- Anchors
- Web roles
- Dense text
- UI / UX
- Social
- YouTube
- Arrows
- Stress

## Dense-text gauntlet

The dense view contains:

- **46 paragraphs**
- **9,202 characters** of sustained body copy
- two-column long-form reading
- an eight-step productive process grid
- aligned USD and INR pricing data
- regular and semibold body texture
- a sticky reading-contract panel

The dense desktop specimen produced no unintended local overflow. It also remained page-overflow-free on the 390 px mobile viewport.

## UI gauntlet

The interface layer was validated with:

- application navigation
- project cards
- a dense data table
- buttons and filters
- form fields
- status badges
- mobile interface composition
- normal, hover, selected, focus, disabled, error, loading, empty, success, and toast states

The specimen contains 16 interactive controls. None of its primary controls fell below the governed target geometry in the tested state.

## Social and YouTube gauntlet

The social layer renders all canonical ratios:

- 1:1
- 4:5
- 9:16
- 1200:630 landscape

The YouTube layer renders:

- three standard 16:9 thumbnail treatments
- a Shorts cover
- a podcast cover
- a channel banner with central cross-device safe region
- an end-screen typography composition

All three standard thumbnail previews measured at 16:9 in the browser.

## Accessibility and responsive gauntlet

The browser pass included:

- 200% root text size
- WCAG-style line, paragraph, letter, and word spacing overrides
- native wrapping with enhanced line-breaking disabled
- 390 px mobile viewport
- mobile checks for Overview, Dense text, UI, and YouTube
- fixed-height clipping checks
- page-level horizontal-overflow checks
- reduced-motion-safe static rendering

No tested state introduced page-level horizontal overflow.

## Local standalone-baker round trip

The automated browser test selected the supplied v13 ZIP, then:

1. unpacked its WOFF2 files locally
2. matched the seven approved source paths
3. verified each file's byte size and SHA-256 digest
4. loaded all seven variable faces
5. generated a one-file embedded review HTML
6. reopened that generated file
7. confirmed authentic Head `ital: 1`
8. confirmed no horizontal overflow
9. confirmed the loader and baker code had been removed
10. confirmed the inline favicon remained

The generated embedded test file was deleted after validation. The HTML review artifact contains no embedded font data by default. The canonical repository distributes the governed fonts separately in `assets/fonts/` and `pitchdog-font-handoff-v13/`.

## Static release integrity

From a complete Git checkout, `tools/validate_release.py` checks:

- every JSON file parses
- version and font authority
- exact axis anchors
- every role's family, weight, posture, and width
- role and canvas counts
- arrow contracts
- font-audit claims
- Head italic proof
- local ZIP and SHA-256 machinery
- favicon assets and manifest target
- browser-validation evidence
- required documentation
- font binaries confined to governed runtime and handoff directories
- absence of embedded font payloads

The repaired release-contract validator completes with **237 passes and zero failures**. From a complete Git checkout, repository packaging, manifests and font hashes are checked separately by `scripts/verify_repository.py`. Neither repository-only script is included in the lean installed package.

## Remaining pre-launch environment gates

These cannot be honestly marked complete from this Linux/Chromium environment:

- Safari desktop rendering
- Firefox desktop rendering
- iOS Safari hardware testing
- Android hardware testing
- Windows ClearType rendering
- forced-colours mode
- VoiceOver, NVDA, or equivalent assistive-technology pass
- deployed LCP and CLS measurement
- deployed cache and font-swap behaviour
- final GSAP/WebGL geometry after production font loading
- compressed social and YouTube artwork on physical phones

These are deployment and environment gates. They do not leave an unresolved typography-system decision.

## Evidence in the complete Git checkout

The following repository evidence is deliberately excluded from the lean installed package:

- `evidence/browser-validation.json`
- `evidence/validation.json`
- `evidence/font-audit.json`
- `evidence/screenshots/`
- `evidence/previews/`
- `evidence/pitchdog-typography-preview-v13.png`
- `SHA256SUMS.txt`
