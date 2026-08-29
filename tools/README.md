# Tools

- `prepare_fonts.py` — verifies and extracts the seven v13 webfont files locally.
- `validate_release.py` — validates anchors, role contracts, arrows, demo markup and governed font-directory boundaries.
- `typography_guard.py` — flags raw component-level typography declarations unless marked with `pd-type-exception:`.

Run:

```bash
python tools/validate_release.py
```
