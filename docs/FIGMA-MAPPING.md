# Figma mapping

Figma mirrors the semantic role names. It is not the source of truth.

- Install the fonts from `pitchdog-font-handoff/02-NATIVE-VARIABLE/`. From 2.0.0 they appear in Figma as PD Head, PD Head Alt, PD Body, PD Body Alt and PD Eyebrow (`FONT-NAMING.md`).
- Import or recreate styles from `figma-style-map.csv`.
- Keep website, UI, Social, YouTube, Deck and Subtitle style groups separate. Deck read density has its own `Deck / Read / …` styles.
- Record Head italic as a variable-axis value, not a synthetic slant.
- Use only the anchor weights.
- Do not create canvas-specific one-off styles outside the approved social, YouTube, deck and subtitle roles.
- Deck sizes are container units; use the px values in `DECKS.md` on 1920 × 1080 frames. Subtitle sizes are container units too; use the px values in `SUBTITLES.md` for each frame.
- `figma-style-map.csv` is generated from the tokens by `scripts/build_dist.py`. Edit the tokens, not the CSV.
- Reconcile Figma against browser specimens after font or copy changes.
