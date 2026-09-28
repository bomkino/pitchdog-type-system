# Known font details

## Resolved in 2.0.0

The FontBlind v13 source fonts had naming defects that showed up in desktop apps, Figma and native platforms. Version 2.0.0 fixed all of them in every shipped file, without touching glyphs, metrics or axes:

- PD Eyebrow installed as `Untitled`. It now installs as `PD Eyebrow`.
- Eyebrow's 350 and 400 static anchors shared one name and could overwrite each other. They are now `PD Eyebrow Book` and `PD Eyebrow` Regular.
- PD Body Italic's style name said `Regular`. It now says `Italic` and pairs with PD Body Regular.
- Head and Body files used lowercase names such as `pd-head` and `pd-body-roman`. They now use the canonical family names.

`docs/FONT-NAMING.md` has the full scheme; `docs/MIGRATION-v13-to-v2.md` covers reinstalling.

## Still worth knowing

- Head italics exist only on the variable font's `ital` axis. There are no static Head italic files; tools that cannot drive the axis cannot show Head italics.
- The native `pd-eyebrow-full.ttf` master covers 477 codepoints; the web Eyebrow (`pd-eyebrow-site.woff2`) covers 404.
- Installing the variable and static versions of one family together can make menus merge or hide faces. Install one or the other.
