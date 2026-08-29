# Anchor policy

## Rule

Use variable font files. Land static production typography on authentic source masters.

## Allowed anchors

```json
{
  "head": {
    "wght": [
      265,
      300,
      400,
      500,
      600,
      700,
      900
    ],
    "ital": [
      0,
      1
    ],
    "continuous": [
      "ital"
    ]
  },
  "headAlt": {
    "wght": [
      265,
      300,
      400,
      500,
      600,
      700,
      900
    ],
    "ital": [
      0,
      1
    ],
    "continuous": [
      "ital"
    ]
  },
  "body": {
    "wght": [
      100,
      250,
      300,
      400,
      600,
      700,
      900
    ],
    "posture": [
      "roman",
      "italic"
    ],
    "continuous": []
  },
  "bodyAlt": {
    "wght": [
      100,
      250,
      300,
      400,
      600,
      700,
      900
    ],
    "posture": [
      "roman",
      "italic"
    ],
    "continuous": []
  },
  "eyebrow": {
    "wght": [
      100,
      200,
      300,
      350,
      400,
      500,
      600,
      700,
      800,
      900
    ],
    "wdth": [
      87.5,
      100
    ],
    "ital": [
      0,
      1
    ],
    "continuous": []
  }
}
```

## Why

The fonts interpolate, but not every interpolated coordinate has the same drawing quality as the true source masters. Anchor-locking keeps the delivery benefits of variable fonts while preventing casual use of visually weaker middle values.

## Allowed interpolation

- Head `ital`: deliberate 0 → 1 transition, tested with the actual text
- Laboratory controls and font QA
- No production weight animation
- No Body posture interpolation
- No Eyebrow width or italic interpolation

## Enforcement

Installed packages expose `dist/pitchdog-system.ts` for typed code. Repository maintainers can additionally run `tools/typography_guard.py` from a complete Git checkout; `tools/` is deliberately excluded from the lean installed package. The full-checkout browser specimen also records every approved anchor.
