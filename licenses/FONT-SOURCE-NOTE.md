# Font source note

The release consumes the user-supplied `FontBlind-Final-2026-08-28-v13.zip`. Font binaries were deliberately excluded from the original standalone-review distributable. The canonical repository and web package contain the governed runtime files; use `scripts/populate_fonts.py` with the separate source archive when rebuilding them. Since 2.0.0 the shipped files are the source binaries with corrected naming metadata only (`docs/FONT-NAMING.md`).
