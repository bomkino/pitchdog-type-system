# Release receipt

## Identity

- Product: **pitch.dog Type System**
- Canonical display version: **13**
- Package version: **13.1.0**
- Font authority: `FontBlind-Final-2026-08-28-v13.zip`
- Release date: **31 August 2026**
- State: **production release**

## Scope

Version 13 governs typography across:

- website and long-form editorial pages
- dense operational content
- product and internal-tool interfaces
- social media
- YouTube thumbnails, Shorts, podcast covers, channel banners, and end screens
- web reading measures and content-role wrapping contracts
- the complete native arrow set

## Canonical decisions

- Variable fonts remain mandatory.
- Static production typography snaps to authentic source anchors.
- Head and Head Alt use the real continuous `ital` axis, with `0` and `1` as static semantic states.
- Body and Body Alt use separate authentic Roman and Italic variable files.
- Eyebrow uses only the approved weight anchors, width endpoints `87.5` and `100`, and binary posture.
- Components consume semantic roles rather than raw typographic values.
- Short display copy balances; selected editorial prose uses pretty wrapping; controls, navigation, data and dense UI retain normal wrapping.
- Calibrated opt-in measures target about 56–80 characters in PD Body. They are font-specific approximations, not generic `ch` folklore.
- The progressive `avoid-orphans` contract falls back to normal wrapping where it is not supported.
- The default HTML contains no embedded font payload. The private repository includes seven governed runtime WOFF2 files plus the complete 138-file handoff.
- `MAKE-STANDALONE-v13.html` embeds the accepted CC0-1.0 font binaries locally when a one-file review artifact is needed.

## Validation receipt

- Static contract checks: **250 / 250 passed**
- Repository checks: **493 / 493 passed**
- Version 13 font/browser gauntlet retained: **100 / 100 passed**
- Browser console errors: **0**
- Browser page errors: **0**
- Runtime variable fonts verified: **7 / 7**
- Runtime font binaries: **7 / 7 hash-verified**
- Handoff font binaries: **138 / 138 hash-verified**
- Parsed font binaries: **145 / 145**

## Primary artifacts

- `pitchdog-typography-system-v13.html`
- `MAKE-STANDALONE-v13.html`
- `tokens/pitchdog.system.tokens.json`
- `tokens/pitchdog.system.dtcg.json`
- `dist/pitchdog-system.css`
- `dist/pitchdog-wrap-contracts.json`
- `dist/pitchdog-system.ts`
- `docs/SPECIFICATION.md`
- `docs/WEB-TEXT-WRAPPING.md`
- `docs/VALIDATION-REPORT.md`
- `evidence/pitchdog-typography-preview-v13.png`
- `SHA256SUMS.txt`

## Launch boundary

Version 13.1 is an additive web-typography release; the governed font binaries are unchanged from version 13. The pitch.dog website received focused Chromium checks at 320, 390, 1200 and 3840 CSS px. Cross-browser, hardware and assistive-technology checks remain explicit consumer launch gates rather than claims made by this package.
