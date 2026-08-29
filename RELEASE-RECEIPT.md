# Release receipt

## Identity

- Product: **pitch.dog Type System**
- Canonical display version: **13**
- Package version: **13.0.0**
- Font authority: `FontBlind-Final-2026-08-28-v13.zip`
- Release date: **28 August 2026**
- State: **production candidate**

## Scope

Version 13 governs typography across:

- website and long-form editorial pages
- dense operational content
- product and internal-tool interfaces
- social media
- YouTube thumbnails, Shorts, podcast covers, channel banners, and end screens
- the complete native arrow set

## Canonical decisions

- Variable fonts remain mandatory.
- Static production typography snaps to authentic source anchors.
- Head and Head Alt use the real continuous `ital` axis, with `0` and `1` as static semantic states.
- Body and Body Alt use separate authentic Roman and Italic variable files.
- Eyebrow uses only the approved weight anchors, width endpoints `87.5` and `100`, and binary posture.
- Components consume semantic roles rather than raw typographic values.
- The default HTML contains no embedded font payload. The private repository includes seven governed runtime WOFF2 files plus the complete 138-file handoff.
- `MAKE-STANDALONE-v13.html` embeds the accepted CC0-1.0 font binaries locally when a one-file review artifact is needed.

## Validation receipt

- Static contract checks: **237 / 237 passed**
- Repository checks: **488 / 488 passed**
- Automated Chromium checks: **100 / 100 passed**
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
- `dist/pitchdog-system.ts`
- `docs/SPECIFICATION.md`
- `docs/VALIDATION-REPORT.md`
- `evidence/pitchdog-typography-preview-v13.png`
- `SHA256SUMS.txt`

## Launch boundary

The system is complete as a production candidate. Cross-browser, hardware, assistive-technology, deployed performance, and final motion-geometry checks remain explicit launch gates.
