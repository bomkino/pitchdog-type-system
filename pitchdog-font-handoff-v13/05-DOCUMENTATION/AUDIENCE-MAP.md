# Audience map

| Audience | Primary files | Optional fallback | Notes |
|---|---|---|---|
| Website developer | `01-WEB-VARIABLE/*.woff2` | `04-OPTIONAL-STATIC-WEB/` | Import the included CSS; keep Head ital explicit. |
| iOS / Android / desktop app developer | `02-NATIVE-VARIABLE/*.ttf` | `03-STATIC-ANCHORS-NATIVE/` | Use exact axes; test platform font registration. |
| Figma / Adobe / Canva / social designer | `02-NATIVE-VARIABLE/*.ttf` | `03-STATIC-ANCHORS-NATIVE/` | Install variable first; do not install duplicates. |
| Video / YouTube designer | `02-NATIVE-VARIABLE/*.ttf` | static native anchors | Head 700 is the approved high-pressure display anchor. |

The full pitch.dog typography, UI, social and YouTube behaviour lives in the separate Type System v13 package. This handoff contains the font assets and the minimum integration contract only.
