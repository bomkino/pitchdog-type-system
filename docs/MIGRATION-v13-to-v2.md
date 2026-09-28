# Migration from 13.x to 2.x

2.0.0 is the major release after 13.1.1. Numbering restarted at 2; tools that sort versions will still list 13.x higher, so move pins by tag rather than by "latest".

## What changed

- **Font names.** Every font file now carries the family names the CSS already used: PD Head, PD Head Alt, PD Body, PD Body Alt and PD Eyebrow. PD Eyebrow no longer installs as `Untitled`, its 350 and 400 static anchors no longer collide, and PD Body Italic is labelled Italic. See `FONT-NAMING.md` for the full scheme.
- **Style linking.** Roman and Italic files of PD Body and PD Body Alt now belong to one family each. Static fallbacks follow the standard Regular/Italic/Bold/Bold Italic model; other weights are separate legacy families grouped under one typographic family.
- **Font hashes.** Because the name tables changed, every font file has a new SHA-256 and byte size. Glyphs, metrics, axes, anchors, kerning and every semantic role are unchanged.
- **Paths.** `pitchdog-font-handoff-v13/` is now `pitchdog-font-handoff/`, and the specimen is `pitchdog-typography-system.html`. `MAKE-STANDALONE-v13.html` was an identical copy of the specimen and is gone; the specimen still builds the standalone file.
- **Release assets.** Each GitHub Release now attaches the runtime fonts, the full handoff and the agent skill as ZIPs with SHA-256 sidecars.

## Web projects

1. Change the pin to `#v2.0.0` and reinstall so the lockfile records the new commit.
2. Nothing in CSS, tokens or roles changed. `@font-face` rules still register the same family names, so layouts do not reflow.
3. If your build or CSP pins font hashes or byte sizes, take the new values from `dist/pitchdog-font-runtime.json`.
4. Rebuild and inspect a page that uses every family, including Body Italic and Eyebrow.

## Desktop, Figma and native apps

1. Uninstall every v13 PD font first, including any family that appears as `Untitled`, `pd-head`, `pd-body-roman` or `pd-body-italic`. Leaving the old files installed can make apps pick the wrong face.
2. Install the variable fonts from `pitchdog-font-handoff/02-NATIVE-VARIABLE/` (or from the Release handoff ZIP).
3. In Figma, re-point text styles that referenced the old names to PD Head, PD Head Alt, PD Body, PD Body Alt and PD Eyebrow. The style map in `figma-style-map.csv` already uses these names.
4. Native code that loads fonts by PostScript name must use the new names, for example `PDEyebrow-Regular` instead of `Untitled-Regular`, and `PDBody-Italic` for the Body Italic variable file.

## Rollback

Pin `#v13.1.1` (commit `318e6ff4d4bf76be76f7ed5225aacf7517d2ee82`) and reinstall the v13 fonts.

## From 2.0.0 to 2.1.0

2.1.0 adds deck mode and changes no font file, size, weight or limit.

1. Change the pin to `#v2.1.0` and reinstall.
2. Expect slightly different line breaks in social display, headline, subhead, body and quote roles and in YouTube support copy, which now balance or use pretty wrapping. Check fixed-canvas exports that depend on exact breaks.
3. If you import `docs/figma-style-map.csv`, rename UI and YouTube styles to the new casing (for example `UI / Page Title`).
4. Nothing else is required. Deck roles are new attributes (`data-pd-deck`, `data-pd-deck-canvas`) and do not affect existing markup.
