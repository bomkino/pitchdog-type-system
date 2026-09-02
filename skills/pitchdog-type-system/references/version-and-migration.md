# Version and migration

Use this branch for an unpinned consumer, “latest” request, pin change, migration, release, or source contradiction.

## Select an immutable version

1. Inspect the consumer first. An existing full commit, package lock, submodule SHA, or vendored receipt is the pin and wins over a newer upstream version unless migration is authorized. A tag without a recorded commit establishes the intended version, not immutable identity; recover its original commit from installed or lock evidence and stop if that evidence is absent or conflicts with the current remote tag.
2. Inspect stable GitHub Release records and Git tags independently. Peel annotated tags to commits and record the full SHA.
3. At that commit, compare the package version, canonical token metadata, generated version markers, changelog, and release receipt. Read GitHub visibility independently from licensing files.
4. For a new unpinned consumer, accept the newest stable release only when those surfaces identify the same version and both canonical metadata and the receipt explicitly say production. Use the tag in integration syntax when required and retain the full commit in the lock evidence.

Fail closed when the tag and Release disagree, `/releases/latest` is stale, a required Release object is absent, any default candidate is not explicitly production, canonical tokens disagree with a derived or documented surface, or the retrieved tree differs from the resolved commit. State the conflicting values. Canonical tokens remain the semantic authority; repair a conflicting derived surface only with authorization, otherwise keep the task blocked. Ask the user only when a non-semantic release-identity conflict genuinely requires their choice.

## Migrate only with authority

When the user authorizes a pin change:

1. Read every changelog and applicable migration note between the current and target versions.
2. Identify changed contracts that can alter line count, component geometry, animation timing, exports, or native registration.
3. Update the smallest dependency or vendor boundary that owns the pin; keep a recovery path to the previous commit.
4. Run the source/package checks and the consumer's relevant runtime checks.
5. Report the old and new tags, commits, changed contracts, and remaining launch gates.

The migration is complete only when the lock resolves to the intended commit and the consumer's real output has been inspected. A dependency-file edit or successful install is not migration proof.
