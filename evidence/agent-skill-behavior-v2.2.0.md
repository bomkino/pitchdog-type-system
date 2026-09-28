# Agent Skill behaviour evidence — v2.2.0

Date: 28 September 2026

Three independent Claude agents received the candidate skill, one realistic request, and a fixture for that branch. They made no edits. These are decision-level runs, not user acceptance or a substitute for testing a real consumer. They repeat the three branches of the v13.1.1 evidence after the v2.2 writing pass.

## Candidate binding

The agents read this skill payload:

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
7f9f47626fbd013177bb25981df1e5931e12dcbd75b906a73251b76474819015  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
0aa658a06804aeb7f49d89a5df2d6fcd8849f1fbab2ebfc3a30355e312b6392e  references/runtime-verification.md
5302abc4298aea74c6bc5ee2881beb6509f8acf00d6427a007d0ed87b66f1ec8  references/task-routing.md
a7b682e74d9af3971dcd38ac93babd25c243de523d39b3d7d8e6c15bb74fc5b2  references/version-and-migration.md
```

The shipped skill differs from this payload only by the wording repairs listed under "Changes after the runs".

## Existing pinned consumer

The consumer asked for UI role changes and ruled out an upgrade. Its manifest named tag v13.1.1, while its lock recorded an older commit whose metadata said production candidate. The agent peeled the tag, found that the tag and the lock named different commits, failed closed, changed nothing, and asked which commit was the pin. It still listed the shared, web and interface documents it would route to once the pin was settled.

Observed invariant: a tag and a lock that disagree did not become a silent upgrade or downgrade.

## Contradictory “latest”

A new consumer asked for the latest production system. The stable Release pointed at a commit whose tokens and receipt said candidate, and a newer tag that said production had no Release. The agent selected neither, changed nothing, and named the repair: publish a Release for the newer tag, and mark the older Release as a prerelease or correct its metadata.

Observed invariant: a tidy endpoint did not overrule contradictory source evidence.

## Runtime font diagnosis

The fixture reported a successful build, a 404 for one face, `document.fonts.status` of "loaded", synthesis enabled, and an unlayered app rule declaring the family at an ungoverned weight. The agent kept build, asset request, font loading, computed style, rendered face and role fit as separate states. It identified the missing asset, the cascade override, synthesis and an unexplained fallback stack as separate causes. It also noted that an aggregate `document.fonts` status does not show that each face loaded, and it named hash, network, per-face, cascade and rendered-font checks.

Observed invariant: build success did not become runtime proof, and a missing font did not explain away a separate cascade mismatch.

The run also found stale install references to v13.1.1 in `docs/USING-IN-PROJECTS.md` at v2.0.0.

## Changes after the runs

The agents quoted every sentence they found ambiguous. Those sentences were repaired:

- Version selection now defines the requested and default cases, replaces “stale” and “required Release object” with testable conditions, covers a tag whose recorded commit disagrees, and drops a visibility sentence the rights section already carries.
- Fail closed now applies to the type system's own identities and sources. A consumer that deviates from the system is a finding to diagnose.
- The report surfaces now come from runtime verification, and a diagnosis has its own completion criterion.
