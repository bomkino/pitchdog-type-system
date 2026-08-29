# Optional native static anchors

These are exact source-master anchors for tools that do not handle the variable fonts reliably.

- `pd-head/`: 14 TTF files, Primary and Alt, seven upright weight anchors each. Head italics still require the variable font because the source italic is an axis rather than a separate static family in this release.
- `pd-body/`: 28 OTF files, Primary and Alt, seven authentic Roman and seven authentic Italic anchors per family.
- `pd-eyebrow/`: 20 TTF files, ten Normal-width anchors in Upright and Italic.

Install these only after removing the matching variable family.

**Eyebrow warning:** the 350 and 400 upright files share `Untitled Regular` / `Untitled-Regular`; the 350 and 400 italic files share `Untitled Italic` / `Untitled-Italic`. Native installers can overwrite or hide one face. Prefer the variable Eyebrow. If a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time.
