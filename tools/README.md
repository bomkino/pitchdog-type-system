# Tools

- `normalize_font_names.py` — applies the 2.0.0 font naming scheme; `--check` verifies every font follows it.
- `compare_font_payloads.py` — proves two font files differ only in naming metadata.
- `requirements.txt` — pinned font tooling for the two scripts above.
- `font-handoff-builder-v13/` — rebuilds the raw v13 handoff from the FontBlind source. Its fonts are then renamed by `normalize_font_names.py`; `scripts/populate_fonts.py` runs both.
- `validate_release.py` — validates anchors, role contracts, arrows, demo markup and governed font-directory boundaries.
- `typography_guard.py` — flags raw component-level typography declarations unless marked with `pd-type-exception:`.

Run:

```bash
python tools/validate_release.py
```
