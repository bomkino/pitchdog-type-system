---
name: pitchdog-type-system
description: pitch.dog typography authority for fonts, type roles and hierarchy, wrapping and measure, and any rendered text on web, interface, social, video, native or design-tool surfaces. Always invoke for any type work.
---

# pitch.dog Type System

The canonical pitch.dog repository is the sole typography authority. This skill is the process. At the resolved commit, `tokens/pitchdog.system.tokens.json` is the semantic source of truth, `dist/` holds the generated consumption surfaces, and `docs/` explains them. Point to those files; their values stay there, out of this skill and out of the consumer.

Two words carry the whole process:

- **Pin**: the full commit SHA a consumer's type system resolves to. An existing pin holds until the user authorizes a migration.
- **Fail closed**: when identities or sources disagree, stop, name the conflicting values, and change nothing.

## 1. Resolve the pin

Inspect the consumer's dependency files, lockfiles, submodules, vendored receipts and release records for an existing pin.

- An existing pin stays, and the work reads from that commit even when a newer release exists.
- No pin, an explicit target version, “latest”, a pin change, release work, or a source contradiction: read [version and migration](references/version-and-migration.md) now.
- Resolve a tag to its full commit SHA. A branch, a bare tag name, or `/releases/latest` is mutable evidence, never a pin.
- Read canonical files from the consumer's exact package or checkout, or from `https://github.com/bomkino/pitchdog-type-system` at the pinned commit. Keep temporary source outside the consumer and remove it afterwards.

Resolution is complete when the source location, version or tag, and full commit are recorded and the retrieved tree matches them. Fail closed on conflicting identity, missing provenance, a version not explicitly marked production, or canonical tokens disagreeing with a derived or documented surface.

## 2. Route the type work

Read [task routing](references/task-routing.md), combine every branch the task touches, and read each branch's documents at the pinned commit.

Select semantic roles and supported exports from those documents. Trace each role to the canonical token source and each export to `package.json`, and confirm the generated contract agrees with both. Raw family names, font values, scales, measures, wrapping rules, CSS and binaries stay in their authoritative files; the consumer references them.

When no governed role fits, surface the gap. A governed exception needs the user's explicit authorization, then follows the canonical exception process.

Routing is complete when every touched surface has a branch and every chosen role or export traces to the token source and `package.json`.

## 3. Apply

Use the pinned package exports, semantic attributes, classes, tokens or handoff that the branch documents describe, in the consumer's existing integration shape. Keep an existing recorded exception exactly as recorded.

Application is complete when every touched type decision points to a governed role or recorded exception, and the pin and unrelated typography are unchanged unless the user authorized the change.

## 4. Verify the rendered result

For implementation, build, migration or diagnosis, read [runtime verification](references/runtime-verification.md) and inspect the real target after its build or export. Each check proves only its own surface: an import, build, validator or screenshot is narrow evidence.

Report source resolution, package or handoff, consumer integration, emitted assets, rendered output and migration state as separate claims, each `verified`, `unverified`, `mismatch` or `blocked`. Completion requires direct evidence for every in-scope surface.

## Rights

Repository visibility is not a licence. Before redistributing any file, read this skill's [rights notice](NOTICE.md), then `LICENSE.md` and `FONT-LICENSE.md` at the pinned commit.
