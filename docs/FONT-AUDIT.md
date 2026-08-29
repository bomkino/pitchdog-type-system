# Font audit

Source: `FontBlind-Final-2026-08-28-v13.zip`

| Runtime face | Bytes | Codepoints | Axes | ₹ | 12 arrows |
|---|---:|---:|---|---|---|
| head | 270,176 | 378 | wght, ital | yes | yes |
| headAlt | 276,308 | 378 | wght, ital | yes | yes |
| body | 171,820 | 395 | wght | yes | yes |
| bodyItalic | 218,976 | 395 | wght | yes | yes |
| bodyAlt | 169,540 | 395 | wght | yes | yes |
| bodyAltItalic | 179,020 | 395 | wght | yes | yes |
| eyebrow | 916,908 | 404 | wght, wdth, ital | yes | yes |

## Findings

- Body ₹ is present in Roman, Italic, Alt Roman and Alt Italic variable files.
- The selected Eyebrow website runtime contains 404 codepoints and all required axes.
- All seven runtime files contain the twelve arrow glyphs.
- Head and Head Alt contain genuine `wght` and `ital` axes.
- Body and Body Alt use separate authentic Roman and Italic variable files.
- Eyebrow website runtime is preferred over the larger full master for site delivery.

In a complete Git checkout, machine-readable audit evidence lives in `evidence/font-audit.json`. The lean installed package ships the seven-face runtime manifest at `dist/pitchdog-font-runtime.json` instead.
