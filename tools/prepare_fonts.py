#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys, zipfile
from pathlib import Path

EXPECTED = [
  {
    "key": "head",
    "family": "PD Head",
    "style": "normal",
    "file": "assets/fonts/pd-head.woff2",
    "sourcePath": "FontBlind-Final-2026-08-28-v13/01-PUBLIC-FONTS/LAB/pd-head/web/pd-head.woff2",
    "bytes": 270176,
    "sha256": "528dd6d9d5d79265f4e3589523a250cd652110d1380e87a0252bca9489da50e9",
    "axes": [
      {
        "tag": "wght",
        "min": 265.0,
        "default": 400.0,
        "max": 900.0
      },
      {
        "tag": "ital",
        "min": 0.0,
        "default": 0.0,
        "max": 1.0
      }
    ],
    "codepointCount": 378,
    "hasRupee": True,
    "arrows": True
  },
  {
    "key": "headAlt",
    "family": "PD Head Alt",
    "style": "normal",
    "file": "assets/fonts/pd-head-alt.woff2",
    "sourcePath": "FontBlind-Final-2026-08-28-v13/01-PUBLIC-FONTS/LAB/pd-head/web/pd-head-alt.woff2",
    "bytes": 276308,
    "sha256": "bf4db03493580a52e3e01cb6aec2fe791da8e7293d6083e2c567c3bb3f0b927a",
    "axes": [
      {
        "tag": "wght",
        "min": 265.0,
        "default": 400.0,
        "max": 900.0
      },
      {
        "tag": "ital",
        "min": 0.0,
        "default": 0.0,
        "max": 1.0
      }
    ],
    "codepointCount": 378,
    "hasRupee": True,
    "arrows": True
  },
  {
    "key": "body",
    "family": "PD Body",
    "style": "normal",
    "file": "assets/fonts/pd-body-roman.woff2",
    "sourcePath": "FontBlind-Final-2026-08-28-v13/01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-roman.woff2",
    "bytes": 171820,
    "sha256": "433a1b69a8e8a903478b978c198b879824541dc9eb62db959058ae37a250819f",
    "axes": [
      {
        "tag": "wght",
        "min": 100.0,
        "default": 400.0,
        "max": 900.0
      }
    ],
    "codepointCount": 395,
    "hasRupee": True,
    "arrows": True
  },
  {
    "key": "bodyItalic",
    "family": "PD Body",
    "style": "italic",
    "file": "assets/fonts/pd-body-italic.woff2",
    "sourcePath": "FontBlind-Final-2026-08-28-v13/01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-italic.woff2",
    "bytes": 218976,
    "sha256": "6bd35c9ad364e585ca5667c1df74f892eebbe32237005ba926b54ffa61df8a78",
    "axes": [
      {
        "tag": "wght",
        "min": 100.0,
        "default": 400.0,
        "max": 900.0
      }
    ],
    "codepointCount": 395,
    "hasRupee": True,
    "arrows": True
  },
  {
    "key": "bodyAlt",
    "family": "PD Body Alt",
    "style": "normal",
    "file": "assets/fonts/pd-body-alt-roman.woff2",
    "sourcePath": "FontBlind-Final-2026-08-28-v13/01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-alt-roman.woff2",
    "bytes": 169540,
    "sha256": "4ae6044273de9010d1a9660001319c34a4a8ece764279bb7f1e0f81f01dca85b",
    "axes": [
      {
        "tag": "wght",
        "min": 100.0,
        "default": 400.0,
        "max": 900.0
      }
    ],
    "codepointCount": 395,
    "hasRupee": True,
    "arrows": True
  },
  {
    "key": "bodyAltItalic",
    "family": "PD Body Alt",
    "style": "italic",
    "file": "assets/fonts/pd-body-alt-italic.woff2",
    "sourcePath": "FontBlind-Final-2026-08-28-v13/01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-alt-italic.woff2",
    "bytes": 179020,
    "sha256": "9f59a7f058ba824e0b3e2760204c0c70b7cfb2f61956a460b730e486b1209285",
    "axes": [
      {
        "tag": "wght",
        "min": 100.0,
        "default": 400.0,
        "max": 900.0
      }
    ],
    "codepointCount": 395,
    "hasRupee": True,
    "arrows": True
  },
  {
    "key": "eyebrow",
    "family": "PD Eyebrow",
    "style": "normal",
    "file": "assets/fonts/pd-eyebrow-site.woff2",
    "sourcePath": "FontBlind-Final-2026-08-28-v13/01-PUBLIC-FONTS/LAB/pd-eyebrow/site/pd-eyebrow-site.woff2",
    "bytes": 916908,
    "sha256": "24aeaf1bfb45a874fe807c8138fc0d815b499b1834e8291c2dc46bb5fc32b7a3",
    "axes": [
      {
        "tag": "wght",
        "min": 100.0,
        "default": 400.0,
        "max": 900.0
      },
      {
        "tag": "wdth",
        "min": 87.5,
        "default": 100.0,
        "max": 100.0
      },
      {
        "tag": "ital",
        "min": 0.0,
        "default": 0.0,
        "max": 1.0
      }
    ],
    "codepointCount": 404,
    "hasRupee": True,
    "arrows": True
  }
]

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()

def main() -> int:
    if len(sys.argv) != 2:
        print('usage: prepare_fonts.py /path/to/FontBlind-Final-2026-08-28-v13.zip', file=sys.stderr); return 2
    source=Path(sys.argv[1]); out=Path(__file__).resolve().parents[1]/'assets'/'fonts'; out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(source) as z:
        names={n.lower():n for n in z.namelist()}
        for rec in EXPECTED:
            suffix=rec['sourcePath'].lower(); matches=[original for lower,original in names.items() if lower.endswith(suffix)]
            if len(matches)!=1: raise SystemExit(f'Expected one match for {suffix}, found {len(matches)}')
            data=z.read(matches[0])
            if len(data)!=rec['bytes'] or sha(data)!=rec['sha256']: raise SystemExit(f'Verification failed: {matches[0]}')
            target=out/Path(rec['file']).name; target.write_bytes(data); print(target)
    return 0
if __name__=='__main__': raise SystemExit(main())
