# Contributing

This repository is maintained by pitch.dog. Bug reports and focused pull requests are welcome; typography decisions stay with the maintainers.

Everything outside the font binaries is all rights reserved (`LICENSE.md`). Opening an issue or pull request does not change that.

## Before you open a pull request

1. Start from an issue for anything larger than a typo, so the change can be agreed first.
2. Change the canonical source, not a derived copy. Semantic values live in `tokens/pitchdog.system.tokens.json`; `dist/` and the split token files must agree with it.
3. Keep production values on the governed anchors (`docs/ANCHOR-POLICY.md`) and follow `docs/GOVERNANCE.md` for exceptions.
4. Never commit font source archives, `.npmrc`, `.env` files or credentials.

## Checks

Run these from a full checkout. CI runs the same commands and must be green before merge.

```bash
python3 scripts/verify_repository.py
python3 -m pip install -r tools/requirements.txt
python3 tools/normalize_font_names.py --check assets/fonts pitchdog-font-handoff
```

If you change any tracked file, refresh the repository manifest and commit it:

```bash
python3 scripts/checksums.py --write
```

## Font binaries

Font files are replaced only through `scripts/populate_fonts.py`, which rebuilds them from the accepted source, applies the name normalization and checks every hash. Hand-edited or re-exported fonts will fail verification.

## Versioning

Follow the rules in the README. Any change to a font binary, metric, axis, family name or existing role is a major version. Bump `package.json`, the token metadata and the other version markers the verifier lists, add a `CHANGELOG.md` section, and merging to `main` publishes the Release.
