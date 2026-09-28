# Optional native static anchors

These are exact source-master anchors for tools that do not handle the variable fonts reliably.

- `pd-head/`: 14 TTF files, Primary and Alt, seven upright weight anchors each. Head italics still require the variable font because the source italic is an axis rather than a separate static family in this release.
- `pd-body/`: 28 OTF files, Primary and Alt, seven authentic Roman and seven authentic Italic anchors per family.
- `pd-eyebrow/`: 20 TTF files, ten Normal-width anchors in Upright and Italic.

Install these only after removing the matching variable family.

Every static face has a unique name. Regular and Bold sit in the base family (for example `PD Eyebrow` Regular, Italic, Bold, Bold Italic); other weights appear as their own family in older apps (`PD Eyebrow Book`, `PD Body Light`) and are grouped under the base family in apps that read typographic names.
