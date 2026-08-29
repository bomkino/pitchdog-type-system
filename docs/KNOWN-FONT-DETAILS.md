# Known font details

## PD Eyebrow internal name

The accepted v13 PD Eyebrow binaries identify internally as `Untitled` / `Untitled Regular`.

- Web: `@font-face` aliases the file to `PD Eyebrow`; no practical issue.
- Desktop tools: the family may appear as `Untitled`.
- Native APIs: some environments may require the internal family or PostScript name.
- Collision risk: another installed family named `Untitled` can conflict.

The static fallback collides with itself too:

- Upright 350 and 400 both expose `Untitled Regular` / `Untitled-Regular` and the same unique-name record.
- Italic 350 and 400 both expose `Untitled Italic` / `Untitled-Italic` and the same unique-name record.
- The variable Eyebrow also exposes `Untitled-Regular` at its default instance.

Native installers can overwrite, hide or substitute these distinct faces. Do not install all Eyebrow static anchors. Prefer the variable font; if a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time.

Do not patch individual downstream copies. Rename the internal records only in a future canonical font-source release, then issue a major type-system version because the binary hashes and native registration contract will change.

## PD Body Italic style name

The v13 `pd-body-italic` variable file carries correct italic behaviour (`fsSelection`, `macStyle` and italic angle), but its subfamily and typographic-subfamily name records say `Regular`. Web CSS declares it as italic and works correctly. Some native font menus or pairing APIs may display it inconsistently. `pd-body-alt-italic` has the expected `Italic` name.
