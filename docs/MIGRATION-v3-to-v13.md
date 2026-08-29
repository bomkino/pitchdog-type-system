# Migration from v3 to v13

1. Replace the v3 token source with `pitchdog.system.tokens.json`.
2. Remove all intermediate production weights such as 460, 575, 595 and 620.
3. Replace Eyebrow widths such as 92 or 96 with 87.5 or 100.
4. Load Head once and drive the `ital` axis explicitly.
5. Keep Body Roman and Italic as separate files.
6. Update font paths and hashes to FontBlind v13.
7. Add the UI role API where interface components previously borrowed website roles.
8. Add YouTube canvas and role contracts.
9. Replace external arrow icons where the native glyph system is semantically adequate.
10. Run the complete font-loader, responsive, dense-text and accessibility validation matrix.
