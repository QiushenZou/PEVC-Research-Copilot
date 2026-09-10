# PE/VC Research Skills

A modular, evidence-first Codex skill set for moving from industry understanding to company diligence and investment-committee decisions.

## Included skills

| Skill | Purpose |
|---|---|
| `pevc-industry-chain-mapper` | Research a real upstream-to-downstream value chain and generate a source-backed interactive HTML map with node explainers and company roles. |
| `pevc-company-diligence` | Analyze a target company's business model, customers, product and technology, competition, financial quality, risks, and open diligence questions. |
| `pevc-ic-memo` | Convert research and diligence into a decision-ready screening, preliminary, final, or update IC memo. |

The skills are intentionally separate. The value-chain map should not become a company report, and a company report should not silently become an investment recommendation.

## Install

### Requirements

- Codex with local skill discovery
- Python 3.9+ only for the industry-map validator and renderer; the other two skills have no runtime dependencies

After cloning or downloading this repository, copy the desired folders into your Codex skills directory:

```bash
SKILLS_HOME="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$SKILLS_HOME"
cp -R skills/pevc-industry-chain-mapper "$SKILLS_HOME/"
cp -R skills/pevc-company-diligence "$SKILLS_HOME/"
cp -R skills/pevc-ic-memo "$SKILLS_HOME/"
```

Restart Codex or refresh skill discovery after installation. To update an installed skill, replace that skill's directory rather than mixing files from different releases.

```text
skills/
├── pevc-industry-chain-mapper/
├── pevc-company-diligence/
└── pevc-ic-memo/
```

Each skill can be invoked explicitly:

```text
$pevc-industry-chain-mapper
$pevc-company-diligence
$pevc-ic-memo
```

Automatic invocation is also enabled when a request clearly matches the skill.

Example requests:

```text
Use $pevc-industry-chain-mapper to map the DPU value chain in China and globally.
Use $pevc-company-diligence to review this target using the attached materials and public evidence.
Use $pevc-ic-memo to draft a preliminary IC memo and clearly label unresolved assumptions.
```

## Research workflow

1. Use the industry-chain skill to understand structure, participants, profit pools, bargaining power, and technology routes.
2. Use the company-diligence skill to test how the target company makes money, whether demand and differentiation are real, and what remains unverified.
3. Use the IC-memo skill to make the decision, valuation, return path, downside, approval conditions, and monitoring plan explicit.

See [docs/workflow.md](docs/workflow.md) for handoffs and quality gates.

## Repository layout

```text
skills/   Installable Codex skills
docs/     Shared workflow, provenance, and release guidance
```

Each installable directory is self-contained and includes its own `SKILL.md`. The industry-chain mapper additionally contains a standalone HTML template and standard-library Python helpers.

## Methodology, provenance, and confidentiality

These skills are an independent implementation of common PE/VC research practices: evidence labeling, claim reconciliation, disconfirming review, scenario analysis, and explicit decision gates. During design, public ecosystem references—including the [N.E.I. PEVC Skill Library](https://nei-pevc.com/) and its public task taxonomy—were surveyed for coverage and workflow comparison. No N.E.I. Skill or Workflow text, private library content, credentials, or MCP tokens are bundled in this repository, and this project is not affiliated with or endorsed by N.E.I.

Do not commit confidential data-room files, internal investment materials, customer information, interview transcripts, access tokens, or generated work products containing such information. See [docs/methodology-and-provenance.md](docs/methodology-and-provenance.md) and [docs/release-checklist.md](docs/release-checklist.md).

Third-party names and trademarks belong to their respective owners. Example company and source names in schemas are illustrative and do not imply endorsement.

## Status

This repository starts at `v0.1.0`. It is suitable for internal testing and iterative use. Outputs remain dependent on the quality, completeness, authorization, and date of the underlying evidence and are not legal, tax, audit, or regulated investment advice.
