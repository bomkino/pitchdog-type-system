# App developers and design tools

Use the seven variable TTF files in this folder first.

- Head and Head Alt: one variable TTF each.
- Body and Body Alt: separate authentic Roman and Italic variable TTFs.
- Eyebrow: the fuller 477-codepoint native master.

Keep production settings on the approved anchors. Some native frameworks expose axes by tag; others expose named instances. Where custom variation values are supported, use the tags and values in `../05-DOCUMENTATION/AXES-AND-ANCHORS.md`.

If a framework or design application mishandles variable instances, remove the variable family and install the matching files in `../03-STATIC-ANCHORS-NATIVE/` instead.

Do not install variable and static duplicates simultaneously.

Note: PD Eyebrow currently installs under the internal family name `Untitled`.

PD Body Italic has correct italic behaviour but exposes `Regular` in two native style-name records. Some native menus may pair it inconsistently; web CSS is unaffected.
