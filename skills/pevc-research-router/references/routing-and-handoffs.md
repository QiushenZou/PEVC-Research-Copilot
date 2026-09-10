# Routing and handoffs

## Gate matrix

| Gate | Decision | Minimum evidence | Output | Stop or reroute when |
|---|---|---|---|---|
| Material intake | What do the materials actually establish? | Readable source set and coverage register | BP fact card | Coverage is too incomplete to identify the business |
| Initial screen | Is more work justified for this fund? | Fact card plus explicit mandate and constraints | Screening decision and test plan | A hard mandate gate fails or return path is implausible |
| Industry understanding | How does the market actually work? | Defined product, geography, customer, and market boundary | Structured map and node evidence | The requested “chain” is actually a company or theme report |
| Diligence | Are decisive company claims supported? | Claim ledger and access to appropriate evidence | Diligence conclusions, tracker, and red flags | Evidence cannot be obtained before the decision or a fatal claim fails |
| IC | What authority should the committee grant? | Stage-appropriate evidence, terms, and model | Decision memo or update | Terms/returns are fabricated, material conflicts remain hidden, or authority requested is unclear |

## Minimum handoff fields

Every handoff preserves:

- project identifier, scope, cutoff date, and decision stage;
- source register with versions and coverage;
- normalized metric definitions and formulas;
- facts, claims, evidence status, counterevidence, and conflicts;
- P0/P1/P2 open items and what each could change;
- current view and its confidence, if a view has been formed;
- next skill, expected output, and stop condition.

## Quality gates

### Fact card → screening

- The product, customer, payer, revenue mechanism, stage, financing ask, and material gaps are visible.
- Material claims have source locators.
- Forecasts, orders, revenue, and cash are not conflated.

### Screening → research/diligence

- Fund gates are explicit rather than invented.
- `Fail`, `Unclear`, and `Not applicable` are distinguished.
- The next work tests claims capable of reversing the decision.

### Industry map → diligence

- Company roles are attached to evidenced nodes.
- Industry facts are not treated as company proof.
- Profit-pool, bargaining-power, technology-route, and transmission hypotheses are expressed as tests for the target.

### Diligence → IC

- Decision-driving claims have support and counterevidence.
- Material financial and operating definitions reconcile or conflicts remain visible.
- Terms and capitalization are executable enough for the requested stage.
- Risks have loss mechanisms, not just labels.

## Reuse before rework

Do not repeat completed work merely because a new deliverable starts. Reuse facts and sources after checking their cutoff, scope, definition, and current validity. When a conclusion changes, add a dated change record rather than overwriting the earlier view silently.
