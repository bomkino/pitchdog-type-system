# Agent Skill behaviour evidence — v2.2.0

Date: 28 September 2026

Four independent Claude agents received a candidate skill, one realistic request, and a fixture for that branch. They made no edits. These are decision-level runs, not user acceptance or a substitute for testing a real consumer. Runs 1 to 3 repeat the three branches of the v13.1.1 evidence after the v2.2 writing pass. Run 4 covers the deck branch added in 2.1.0.

## Candidate binding

Runs 1 to 3 read this skill payload:

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
7f9f47626fbd013177bb25981df1e5931e12dcbd75b906a73251b76474819015  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
0aa658a06804aeb7f49d89a5df2d6fcd8849f1fbab2ebfc3a30355e312b6392e  references/runtime-verification.md
5302abc4298aea74c6bc5ee2881beb6509f8acf00d6427a007d0ed87b66f1ec8  references/task-routing.md
a7b682e74d9af3971dcd38ac93babd25c243de523d39b3d7d8e6c15bb74fc5b2  references/version-and-migration.md
```

Run 4 read this payload, after the first repairs and the merge of 2.1.0's deck routing:

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
c7737a4301413bcc6d04e760f084707bb9e56238c7af278409c02e0986284ab8  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
0aa658a06804aeb7f49d89a5df2d6fcd8849f1fbab2ebfc3a30355e312b6392e  references/runtime-verification.md
c3ef02cc7483b837dc459a05d4c772825bc6abd98a3cbd09fd3f2e1d03f16dfa  references/task-routing.md
13cdc981412da6323a263651eb9150b15212ef308694d7f257135406d1b27a81  references/version-and-migration.md
```

The shipped skill differs from these payloads only by the wording repairs listed under "Changes after the runs".

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

## Deck task

A consumer pinned to v2.1.0 asked for a six-slide 16:9 investor deck to be emailed as a PDF, plus Keynote sizes for the title and body slides. The agent kept the pin, read the files at the tag rather than the newer working tree, and routed to the deck documents, tokens, CSS and contracts. It chose read density because the deck travels as a PDF, the widescreen canvas, and governed roles for each slide. It quoted the pinned Keynote sizes (title 102 pt; body 30 pt at present density, 25 pt at read density) and ruled out Google Slides because it cannot use the PD families. Every rendered surface stayed `blocked` or `unverified` because the fixture had no browser.

Observed invariant: a new surface came through the same pin, route and verify process, with no raw sizes invented.

## Changes after the runs

The agents quoted every sentence they found ambiguous. Those sentences were repaired:

- Version selection now defines the requested and default cases, replaces “stale” and “required Release object” with testable conditions, covers a tag whose recorded commit disagrees, and drops a visibility sentence the rights section already carries.
- Fail closed now applies to the type system's own identities and sources. A consumer that deviates from the system is a finding to diagnose.
- The report surfaces now come from runtime verification, and a diagnosis has its own completion criterion.
- Deck routing gives read-density point sizes from the read column and says slides do not take the web wrapping branch. Step 2 no longer asks a contract to agree with `package.json`, which holds no values, and the repository verifier applies only to a full checkout.
