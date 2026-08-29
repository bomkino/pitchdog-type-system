# Web developers

Use the seven WOFF2 variable files in this folder and import `pitchdog-fonts.css`.

## Runtime faces

1. `pd-head.woff2`
2. `pd-head-alt.woff2`
3. `pd-body-roman.woff2`
4. `pd-body-italic.woff2`
5. `pd-body-alt-roman.woff2`
6. `pd-body-alt-italic.woff2`
7. `pd-eyebrow.woff2`

The Eyebrow file is the smaller 404-codepoint website runtime. It retains all 34 supported currencies, ₹, fraction slash, required shaping closure and the complete arrow set.

## Important implementation details

- Head and Head Alt carry `wght` and `ital` in one file. For critical italic display work, explicitly set `"ital" 1` rather than relying only on synthetic or inferred italics.
- Body and Body Alt use separate authentic Roman and Italic variable files.
- Eyebrow carries `wght`, `wdth` and binary `ital` axes.
- Use exact anchors from `../05-DOCUMENTATION/AXES-AND-ANCHORS.md`.
- Do not preload all seven files. Preload only fonts required by the likely first viewport.
- The static WOFF2 folder is optional and should not ship beside the variable files unless a specific target cannot use variable fonts.
