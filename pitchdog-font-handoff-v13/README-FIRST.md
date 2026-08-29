# pitch.dog Font Handoff — v13

Send this entire folder to web developers, app developers and social/content designers.

## Which folder each person uses

- **Web developers:** `01-WEB-VARIABLE/`
- **App developers:** `02-NATIVE-VARIABLE/`
- **Social, video and graphic designers:** install `02-NATIVE-VARIABLE/`
- **Fallback when a tool mishandles variable fonts:** uninstall the matching variable family, then use `03-STATIC-ANCHORS-NATIVE/`
- **Legacy or non-variable web target only:** `04-OPTIONAL-STATIC-WEB/`

## Canonical rule

The variable fonts are authoritative. Production values should land on the approved source anchors rather than arbitrary in-between values. Continuous interpolation is reserved for intentional animation or controlled experiments.

## Do not install duplicates

Do **not** install the variable and static versions of the same family at the same time. Font menus can merge or hide duplicate family records unpredictably. Use variable first. Use static anchors only as a fallback.

## Eyebrow naming caveat

The files are named `pd-eyebrow`, but the current internal installed family name is **Untitled**. Web CSS aliases it to `PD Eyebrow`, so web work is unaffected. Desktop and native tools may display `Untitled` in font menus. This is source-font metadata, not a packaging error. Rename it in a future source build if a clean installed name is required.

The 350 and 400 static Eyebrow anchors also share the same full and PostScript names. Do not install all Eyebrow static anchors together. Prefer the variable font; when a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time.

## Licence

The font binaries are dedicated under CC0 1.0 Universal. See `LICENSE-CC0-NOTE.md`. Keeping that notice with redistributed copies is a provenance best practice, not a licence condition.
