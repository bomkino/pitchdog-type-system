# pitch.dog Font Handoff Builder — v13

This package creates one clean, shareable font ZIP from:

`FontBlind-Final-2026-08-28-v13.zip`

The builder itself contains **no font binaries**.

## Easiest method

1. Extract this builder ZIP.
2. Open `MAKE-PITCHDOG-FONT-HANDOFF-v13.html` in Chrome.
3. Select `FontBlind-Final-2026-08-28-v13.zip`.
4. Wait for the source checks to complete.
5. Click **Build pitch.dog font handoff ZIP**.

The browser downloads:

`pitchdog-font-handoff-v13.zip`

That generated ZIP contains:

- 7 canonical variable WOFF2 files for web
- 7 canonical variable TTF files for apps and design tools
- 62 native static anchor files
- 62 optional static WOFF2 anchor files
- CSS, audience instructions, axis anchors, licence note, manifest and checksums

Total: **138 font files**, with no QA screenshots, recovery files or private receipts.

## Command-line alternative

```bash
python make_font_handoff.py "/path/to/FontBlind-Final-2026-08-28-v13.zip"
```

No third-party Python packages are required.

## Known source detail

PD Eyebrow's internal installed family name is currently `Untitled`. The generated handoff documents this clearly rather than silently modifying the accepted source binaries.

The 350/400 static Eyebrow anchors collide by internal name. Prefer the variable font; if a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time. PD Body Italic also exposes `Regular` in two native style-name records despite carrying correct italic behaviour.
