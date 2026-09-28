# Working in this repository

`CONTRIBUTING.md` is the source of truth for checks, versioning and font binaries. What it leaves unwritten:

- `LICENSE.md`, `FONT-LICENSE.md` and `skills/pitchdog-type-system/NOTICE.md` are the maintainers' legal wording. Change them only when a maintainer asks for that change.
- A full `tools/normalize_font_names.py` rename pass takes minutes. Run it per file in parallel (`xargs -P4`); the `--check` pass is fast.
- `skills/pitchdog-type-system/` is written for agents. After editing it, keep the verifier's skill checks green and record a behaviour run under `evidence/`, following `evidence/agent-skill-behavior-v13.1.1.md`.
