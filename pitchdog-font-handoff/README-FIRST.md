# pitch.dog Font Handoff

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

## Installed names

Every file installs under the family name the CSS uses: **PD Head**, **PD Head Alt**, **PD Body**, **PD Body Alt** and **PD Eyebrow**. Every face has a unique PostScript name, so static anchors can be installed together. If you installed fonts from the v13 handoff, uninstall them first; they used `Untitled` and lowercase `pd-…` names. See `05-DOCUMENTATION/KNOWN-SOURCE-DETAILS.md`.

## Licence

The font binaries are dedicated under CC0 1.0 Universal. See `LICENSE-CC0-NOTE.md`. Keeping that notice with redistributed copies is a provenance best practice, not a licence condition.
