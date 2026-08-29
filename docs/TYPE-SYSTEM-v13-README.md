# pitch.dog Type System v13

Version 13 is the canonical typography system for pitch.dog across website, dense editorial content, interfaces, social media and YouTube.

## Start here

1. Open `pitchdog-typography-system-v13.html`.
2. Select `FontBlind-Final-2026-08-28-v13.zip` in the local loader.
3. Inspect the real fonts and every system layer.
4. Click **Build embedded standalone HTML** when you need a one-file review artifact.

The original standalone-review distributable contained no font binaries. This private source repository deliberately adds the seven hash-verified runtime WOFF2 files in `assets/fonts/` and the complete handoff in `pitchdog-font-handoff-v13/`.

## Governing decisions

- Variable fonts are mandatory.
- Production values snap to authentic source anchors.
- Head italics use the font's real `ital` axis directly.
- Body Roman and Italic remain separate authentic variable files.
- Eyebrow uses only `87.5` or `100` width and binary posture.
- Website, UI, social and YouTube share one family architecture but keep separate semantic role APIs.
- All twelve native arrows are supported and governed.

## Main files

- `tokens/pitchdog.system.tokens.json` — canonical source
- `dist/pitchdog-system.css` — complete generated CSS
- `dist/pitchdog-system.ts` — typed anchors and role names
- `docs/SPECIFICATION.md` — full system
- `docs/VALIDATION-REPORT.md` — completed evidence and remaining launch checks
