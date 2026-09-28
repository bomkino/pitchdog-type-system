# Known source-font details

The FontBlind v13 source binaries shipped with inconsistent internal names. pitch.dog Type System 2.0.0 corrected them in every file of this handoff. Glyphs, metrics, axes and kerning are unchanged from the source; only naming and style-linking metadata was rewritten.

## Fixed in 2.0.0

- **PD Eyebrow called itself `Untitled`.** It now installs as `PD Eyebrow` (`PDEyebrow-Regular` and so on).
- **Eyebrow 350 and 400 static anchors collided.** Both exposed `Untitled Regular` / `Untitled-Regular` (and `Untitled Italic` for the italics). 350 is now `PD Eyebrow Book` / `PDEyebrow-Book`; 400 is `PD Eyebrow` Regular / `PDEyebrow-Regular`.
- **PD Body Italic said `Regular`.** Its style records now say `Italic`, and it shares the `PD Body` family with the Roman file so menus pair them. PD Body Alt follows the same pattern.
- **Head and Body used lowercase file-style names** (`pd-head`, `pd-body-roman`). They now use `PD Head`, `PD Head Alt`, `PD Body` and `PD Body Alt`.
- **Static Bold flags were inconsistent.** Only 700 is Bold; only italic files are Italic.

The full scheme is in the type-system repository at `docs/FONT-NAMING.md`.

## Still true

- Head italics exist only on the variable font's `ital` axis. There are no static Head italic files.
- The native `pd-eyebrow-full.ttf` master covers 477 codepoints; the web Eyebrow covers 404.
