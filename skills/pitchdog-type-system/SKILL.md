---
name: pitchdog-type-system
description: Use the canonical pitch.dog type system for every task involving typography, fonts, text roles or hierarchy, wrapping or measure, or rendered text. Always invoke for any type work; resolve an immutable source, preserve existing pins, consume semantic roles and exports, and verify the real output.
---

# pitch.dog Type System

Use the canonical pitch.dog repository as the sole typography authority for every output. This skill defines the process; `tokens/pitchdog.system.tokens.json` at the resolved commit defines the semantic system. The same commit's `dist/` provides generated consumption surfaces and `docs/` explains their use. Reconcile them rather than recreating their values here or in a downstream project.

## 1. Resolve the source

Identify the consumer, read its local instructions, and inspect its dependency files, lockfiles, submodules, vendored receipts, or release records for an existing type-system pin.

- Read [version and migration](references/version-and-migration.md) during this step for an unpinned consumer, an explicit target version, “latest,” a pin change, release work, or any source contradiction.
- Preserve an existing immutable pin and its resolved commit unless the user explicitly authorizes migration.
- For an unpinned consumer, resolve the requested version. If no version was requested, accept a default only when the stable release, tag, and package version agree and the canonical metadata explicitly says production.
- Resolve a tag to its full commit SHA. Treat a branch name, a tag name alone, or `/releases/latest` alone as mutable evidence, not a lock.
- Obtain canonical files from the consumer's exact package or checkout, or from `https://github.com/bomkino/pitchdog-type-system` at the resolved commit. Keep temporary source outside the consumer and remove it after the task.

Resolution is complete when the source location, version or tag, and full commit are recorded and the retrieved tree agrees with them. Stop on conflicting identity, missing provenance, a non-production default, or disagreement between the canonical tokens and a derived or documented surface.

## 2. Route the type work

Read [task routing](references/task-routing.md) after resolution. Load only the canonical documents and generated contracts for the task's branch.

Select semantic roles and supported exports from the resolved source. Trace every semantic decision to the canonical token source, trace every export to `package.json`, and confirm the generated contract agrees with both. Keep raw family names, font values, scales, measures, wrapping rules, CSS, and binaries in their existing authoritative files.

If no governed role fits, surface the gap. Create a governed exception only when the user explicitly authorizes it, then follow the canonical exception process.

## 3. Apply without drifting

Use the resolved package exports, semantic attributes, classes, tokens, or handoff described by the relevant canonical documentation. Keep the target's existing integration shape and pin unless the requested work requires an authorized change.

Limit edits to the requested surface. Preserve an existing recorded exception; do not broaden it or create another without authorization.

Application is complete when every touched type decision points to a governed role or recorded exception, and no pin or unrelated typography changed without authorization.

## 4. Verify reality

For implementation, build, migration, or diagnosis, read [runtime verification](references/runtime-verification.md). Verify the actual target after its build or export; a successful import, build, validator, or screenshot proves only that narrow surface.

Report source resolution, package or handoff, consumer integration, emitted assets, rendered output, and migration state separately. Completion requires direct evidence for every in-scope surface; preserve `unverified`, `mismatch`, or `blocked` where evidence does not hold.

## Rights boundary

Repository visibility is not a licence. Read this skill's `NOTICE.md`, then `LICENSE.md` and `FONT-LICENSE.md` at the resolved commit before redistributing anything. Only the binary files covered by the font licence receive its CC0 dedication; the skill and surrounding type-system material remain all-rights-reserved.
