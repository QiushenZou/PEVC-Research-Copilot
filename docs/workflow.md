# PE/VC research workflow

## Architecture

```text
pevc-research-router
  ├─ pevc-bp-fact-card
  ├─ pevc-deal-screening
  ├─ pevc-industry-chain-mapper
  ├─ pevc-company-diligence
  └─ pevc-ic-memo
```

The router coordinates; it does not replace the specialist skills. Each specialist can also be invoked directly.

## Stage 0: Project registration

**Input:** scope, materials, current decision gate, investment type, cutoff date, and confidentiality constraints.

**Skill:** `pevc-research-router`

**Output:** routing note and `project-manifest.json` for multi-stage work.

**Quality gate:** the decision requested, evidence available, critical unknowns, selected sequence, and stop conditions are explicit.

## Stage 1: Neutral fact base

**Input:** BP, CIM, teaser, project summary, or management materials.

**Skill:** `pevc-bp-fact-card`

**Output:** project fact card plus initialized `evidence-bundle.json` when structured handoff is useful.

**Quality gate:** reading coverage is explicit; product, customer, payer, business model, operating data, financing, conflicts, and missing information are separated; no investment recommendation is made.

## Stage 2: Initial fund gate

**Input:** fact card and the fund's actual criteria.

**Skill:** `pevc-deal-screening`

**Output:** advance, conditional advance, hold, or decline; fatal questions and minimum-cost tests.

**Quality gate:** fund criteria were not invented; `Fail` and `Unclear` are separated; next work can plausibly reverse or confirm the decision.

## Stage 3: Industry understanding

**Input:** defined product, geography, time horizon, market boundary, and questions raised by screening.

**Skill:** `pevc-industry-chain-mapper`

**Output:** structured industry JSON and interactive value-chain HTML.

**Quality gate:** the map reflects real product, service, supply, support, and demand flows. Each node has relevant companies, evidence, metrics, technology routes, economics, transmission, investment observations, and diligence questions.

## Stage 4: Company verification

**Input:** decisive claims, project fact base, industry hypotheses, data-room materials, public evidence, interviews, and financial data.

**Skill:** `pevc-company-diligence`

**Output:** verification or full-diligence report, updated evidence bundle, request tracker, red flags, and decision consequences.

**Quality gate:** important commercial and financial claims have evidence labels and counterevidence; customer status and metric definitions reconcile; conclusions explain what could change the view.

## Stage 5: Investment decision

**Input:** evidence bundle, transaction terms, capitalization, valuation or return model, residual risks, and prior decisions where relevant.

**Skill:** `pevc-ic-memo`

**Output:** screening, preliminary, final, or update IC memo plus `decision-record.json` when using the structured workflow.

**Quality gate:** decision, recommendation, terms, scenarios, risks, unresolved items, approval conditions, and model version are visible and internally consistent.

## Cross-stage rules

- Industry facts do not prove company access, share, or execution.
- Company quality does not justify the proposed price or structure by itself.
- Management targets remain claims until supported.
- Handoffs preserve source locators, dates, definitions, formulas, evidence status, counterevidence, and open items.
- Conclusions change through dated change records rather than silent overwrites.
- Completed work is reused only after checking scope, cutoff, and metric compatibility.
- Every unresolved material issue ends as a test, price/structure response, condition, monitoring trigger, hold, or decline.

## Optional external routing

N.E.I. MCP may be used as an optional, de-identified method-discovery layer. Public-source connectors may support specific verification. Neither is a destination for confidential project context, and neither converts retrieved text into verified deal evidence without source-level review.
