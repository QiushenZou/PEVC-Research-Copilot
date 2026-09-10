---
name: pevc-deal-screening
description: Screen an inbound PE/VC opportunity against explicit fund criteria and decide whether additional work is justified. Use after a project fact base exists to produce an advance, hold, or decline decision with fatal questions and low-cost verification tests; do not invent a fund mandate, treat unknowns as failures, or replace full diligence or final IC approval.
---

# PE/VC Deal Screening

Make the next resource-allocation decision, not a premature final investment decision.

## Required inputs

- A fact card or equivalent source-traceable project summary.
- The fund's actual mandate, constraints, and stage-appropriate return requirements.
- Known transaction stage, check size, security, valuation or ownership information, and timing where available.

If fund criteria are unavailable, produce a neutral `screening readiness note` listing the criteria needed. Do not invent weights, cutoffs, or a universal scoring model.

## Workflow

1. **Confirm the gate.** State whether the decision is to take a meeting, request data, begin research, allocate diligence budget, submit a preliminary indication, hold, or decline.
2. **Check hard eligibility.** Compare sector, geography, stage, check size, ownership, control/minority fit, concentration limits, regulatory restrictions, timing, and other supplied constraints.
3. **Test the business mechanism.** Explain what is sold, who pays, why demand may exist, how gross profit and cash form, and what must scale.
4. **Identify the strongest signal and counter-signal.** Use evidence status and source locators. Early evidence is acceptable; disguised certainty is not.
5. **Assess the plausible fund-return path.** For PE, consider earnings, cash conversion, leverage and exit plausibility. For VC, consider ownership, future dilution, capital needs, and the exit value required to matter to the fund. Use ranges and feasibility tests when terms are incomplete.
6. **Define fatal questions.** Select only uncertainties that can reverse the gate decision. For each, specify the cheapest credible test, evidence required, cost/time, and stop condition.
7. **Decide.** Use `Advance`, `Advance with conditions`, `Hold`, or `Decline`, followed by the exact next authority or resource being requested.

Read [references/screening-framework.md](references/screening-framework.md) for the output and PE/VC branches.

## Evidence rules

- Use `Pass`, `Fail`, `Unclear`, or `Not applicable` for supplied criteria. An unknown is never automatically a failure.
- A large TAM does not establish accessible demand. A strong company does not establish an acceptable price.
- Present management claims, external facts, calculations, and investment views separately.
- Do not create a polished return model from missing ownership, entry price, dilution, leverage, or exit assumptions.
- State what new evidence would reverse the recommendation.

## Handoff

- Route unresolved industry structure or market-boundary questions to `pevc-industry-chain-mapper`.
- Route customer, order, technology, financial-quality, and red-flag tests to `pevc-company-diligence`.
- Route a formal resource or investment approval request to `pevc-ic-memo` at screening or preliminary stage.

End with the recommended next work, owner, expected evidence, budget/time if known, and an explicit stop condition.

In a structured suite workflow, append the screening view and fatal questions to `evidence-bundle.json`. Create or update `decision-record.json` only when the screen is being used as a formal committee gate; otherwise keep the result as a screening note.
