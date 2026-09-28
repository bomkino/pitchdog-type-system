# pitch.dog Type System

The canonical typography system for pitch.dog across website, dense editorial content, interfaces, social media and YouTube.

## Start here

1. Open `pitchdog-typography-system.html` from a full checkout. It loads the repository fonts through `dist/pitchdog-fonts.template.css`.
2. Inspect the real fonts and every system layer.
3. To make a one-file review artifact, choose the `assets/fonts/` folder (or a release's `pitchdog-fonts-<tag>.zip`) in the local loader and click **Build embedded standalone HTML**. The loader verifies all seven SHA-256 hashes first.

## Governing decisions

- Variable fonts are mandatory.
- Production values snap to authentic source anchors.
- Head italics use the font's real `ital` axis directly.
- Body Roman and Italic remain separate authentic variable files, installed as one family.
- Eyebrow uses only `87.5` or `100` width and binary posture.
- Website, UI, social and YouTube share one family architecture but keep separate semantic role APIs.
- All twelve native arrows are supported and governed.

## Main files

- `tokens/pitchdog.system.tokens.json` — canonical source
- `dist/pitchdog-system.css` — complete generated CSS
- `dist/pitchdog-system.ts` — typed anchors and role names
- `docs/SPECIFICATION.md` — full system
- `docs/FONT-NAMING.md` — installed font names
- `docs/VALIDATION-REPORT.md` and `RELEASE-RECEIPT.md` — evidence and remaining launch checks
