# Known source-font details

## PD Eyebrow internal family name

The Eyebrow binaries currently identify internally as `Untitled` / `Untitled Regular`, even though their filenames and design-system alias are `pd-eyebrow` / `PD Eyebrow`.

Consequences:

- Web: no practical issue. `@font-face` aliases the file as `PD Eyebrow`.
- Desktop design tools: the font may appear as `Untitled`.
- Native apps: some APIs may require the internal PostScript or family name rather than the filename.
- Collision risk: another installed font using the family name `Untitled` may conflict.

The static source also contains two internal collisions:

- 350 and 400 upright both expose `Untitled Regular` / `Untitled-Regular` and the same unique-name record.
- 350 and 400 italic both expose `Untitled Italic` / `Untitled-Italic` and the same unique-name record.

Native installers can overwrite, hide or substitute these distinct files. Prefer the variable Eyebrow. If a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time.

## PD Body Italic style name

`pd-body-italic` has correct italic flags and italic angle, but its subfamily and typographic-subfamily records say `Regular`. Web CSS works correctly; some native menus or pairing APIs may display it inconsistently.

The handoff deliberately preserves the accepted v13 source binaries. A future font-source release should rename the internal records rather than patching them ad hoc in downstream products.
