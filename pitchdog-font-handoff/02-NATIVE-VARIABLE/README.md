# App developers and design tools

Use the seven variable TTF files in this folder first.

- Head and Head Alt: one variable TTF each.
- Body and Body Alt: separate authentic Roman and Italic variable TTFs.
- Eyebrow: the fuller 477-codepoint native master.

Keep production settings on the approved anchors. Some native frameworks expose axes by tag; others expose named instances. Where custom variation values are supported, use the tags and values in `../05-DOCUMENTATION/AXES-AND-ANCHORS.md`.

If a framework or design application mishandles variable instances, remove the variable family and install the matching files in `../03-STATIC-ANCHORS-NATIVE/` instead.

Do not install variable and static duplicates simultaneously.

Installed names: PD Head, PD Head Alt, PD Body (Regular and Italic), PD Body Alt (Regular and Italic) and PD Eyebrow. Code that loads by PostScript name uses `PDHead-Regular`, `PDBody-Italic`, `PDEyebrow-Regular` and so on.
