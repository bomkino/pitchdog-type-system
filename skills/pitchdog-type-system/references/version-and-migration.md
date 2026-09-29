# Version and migration

## Select an immutable version

1. Start from the consumer's pin (SKILL.md step 1). When a tag has no recorded commit, or its recorded lock or receipt commit differs from the commit the tag now resolves to, recover the original commit from installed or lock evidence. Fail closed if that evidence is absent or still disagrees, and ask the user which named commit is the pin.
   A lock that records a full commit for a version with no published tag still has a pin: that commit. Read from it and report the missing tag; do not treat the consumer as unpinned. Fail closed only when the repository has no such commit.
2. Inspect stable GitHub Release records and Git tags independently. Peel annotated tags to commits and record the full SHA.
3. At that commit, compare the package version, canonical token metadata, generated version markers, changelog, and release receipt.
4. Choose the version:
   - **Requested version**: accept its tag when every surface in step 3 names that version and both canonical metadata and the receipt say production. Report a missing GitHub Release without treating it as a blocker.
   - **Default** (no version requested): the newest stable GitHub Release. Accept it only when its tag is also the newest version tag, every surface in step 3 names that version, and both canonical metadata and the receipt say production.

   Use the tag in integration syntax when required and keep the full commit in the lock evidence.

Fail closed when the tag and Release disagree, the default's tag is older than the newest version tag, the chosen version is not explicitly production, canonical tokens disagree with a derived or documented surface, or the retrieved tree differs from the pinned commit. State the conflicting values and the repair the maintainers need. Canonical tokens remain the semantic authority; repair a conflicting derived surface only with authorization. When naming a specific commit or version would resolve the conflict, ask the user to choose between the named candidates.

## Migrate only with authority

When the user authorizes a pin change:

1. Read every changelog and applicable migration note between the current and target versions.
2. Identify changed contracts that can alter line count, component geometry, animation timing, exports, or native registration.
3. Update the smallest dependency or vendor boundary that owns the pin; keep a recovery path to the previous commit.
4. Run the source/package checks and the consumer's relevant runtime checks.
5. Report the old and new tags, commits, changed contracts, and remaining launch gates.

The migration is complete only when the lock resolves to the intended commit and the consumer's real output has been inspected. A dependency-file edit or successful install is not migration proof.
