---
name: pevc-ic-memo
description: Draft, update, or challenge decision-ready PE/VC investment committee memos from available deal evidence. Use for screening, preliminary IC, final IC, and post-IC updates across control, growth, and venture investments; not for inventing diligence, silently filling deal terms, or substituting for legal, tax, audit, or regulated investment advice.
---

# PE/VC IC Memo

Turn research and diligence into an inspectable decision. The memo is not a company report: it must tell the committee **what decision is requested, why the evidence supports it, what could make it wrong, what the price and structure imply, and what conditions protect the fund**.

## Route the assignment

Select two independent axes before drafting:

1. **Decision stage:** screening, preliminary IC, final IC, or update/addendum.
2. **Investment type:** PE/control, growth/minority, or VC.

Read [references/stage-playbooks.md](references/stage-playbooks.md) for the selected stage. Read the relevant PE/VC section in [references/valuation-and-returns.md](references/valuation-and-returns.md). Do not force final-IC depth onto a screening memo or PE metrics onto an early-stage VC case.

## Establish the decision contract

At the top of the working notes, record:

- exact approval requested and permitted decision vocabulary;
- fund and strategy fit, check size, security, ownership, valuation, reserve or leverage, and timing when known;
- information cutoff date, currency, model version, and source set;
- decision-critical unknowns and any terms that must not be inferred.

Use the recommendation that matches the stage: `decline`, `hold`, `continue diligence`, `approve preliminary work/indication`, `approve`, or `approve with conditions`. If a required term is missing, ask when it blocks the decision; otherwise preserve a visible `TBD` and explain the consequence. Never manufacture returns, terms, customers, diligence results, or certainty.

## Build evidence before prose

Create a compact claim ledger using [references/evidence-standard.md](references/evidence-standard.md). For every decision-driving claim capture:

`claim → status → supporting evidence → counterevidence → source/date → confidence → decision implication → remaining test`

Distinguish `verified fact`, `management claim`, `third-party estimate`, `analyst calculation`, `inference`, `investment view`, and `open question`. Reconcile conflicting figures or display the conflict; never select the convenient number silently. Evidence about a market is not automatically evidence about the company.

## Draft decision-first

1. Write the **decision requested** and a one-paragraph recommendation before the background sections.
2. Express the investment case as three to five independently testable propositions. For each, state proof, contrary evidence, falsifier, and leading indicator.
3. Explain company, market, competition, team, and business model only to the depth needed to evaluate those propositions.
4. Link operating assumptions to the financial case and the financial case to valuation and fund returns. Follow [references/valuation-and-returns.md](references/valuation-and-returns.md).
5. Write risks as causal loss mechanisms: trigger, transmission path, financial or strategic impact, mitigation, residual exposure, monitor, and decision response.
6. Convert unresolved material issues into diligence tests, pricing or structure changes, closing conditions, reserved capital, governance rights, or a stop decision.
7. Draft with [references/memo-structure.md](references/memo-structure.md), omitting sections that add no decision value.
8. Run the challenge review in [references/decision-quality.md](references/decision-quality.md) before delivery.

## PE/control emphasis

Focus on normalized earnings, cash conversion, maintenance versus growth capex, working capital, debt capacity, covenant and liquidity headroom, operational value creation, management depth, downside recovery, and exit multiple sensitivity. Separate entry underwriting from value created by leverage or multiple expansion.

## VC/minority emphasis

Focus on founder and team learning velocity, product-market-fit evidence, market timing, retention or repeat behavior, gross-margin path, distribution efficiency, burn and runway, milestone-linked capital needs, ownership and dilution, preference stack, follow-on strategy, and the exit value required to matter to the fund. Early uncertainty should change test design and position sizing, not be disguised as precision.

## Update/addendum rule

Anchor the update to the prior memo and decision. State what changed, why it changed, whether the original thesis or assumptions drifted, the impact on valuation/returns/risk, and the new action requested. Do not rewrite the entire company history. Preserve unresolved prior conditions and show each as closed, open, waived, or breached.

## Output contract

- Default to concise Markdown or Word-ready prose; use the firm's supplied template when available.
- Put the requested decision, terms snapshot, headline return range, top thesis points, top risks, and decisive unknowns on the first page or equivalent opening section.
- Use tables for terms, scenarios, evidence conflicts, risks, and open items; use prose for causal reasoning.
- Cite source title, date, page or section, and model/file version where available. Keep a source register.
- Keep the main memo sufficient for the decision; use appendices for detailed extracts and calculations, never to hide a critical uncertainty.
- End with an action table showing condition/test, owner, deadline, evidence required, and consequence if failed.
- When evidence is incomplete, deliver a clearly marked partial memo plus a prioritized evidence request rather than a polished fiction.
- In a structured suite workflow, consume the existing `evidence-bundle.json`, write the decision and model references to `decision-record.json`, and run the router's project-bundle validator. A passing validator confirms structural and arithmetic checks only; it does not prove the investment conclusion.

## Writing standard

- Lead each section with the answer, then evidence, counterevidence, and caveat.
- Avoid unsupported adjectives such as “leading,” “sticky,” “large,” or “high margin”; define the metric and comparator.
- Do not use TAM as proof of accessible demand, logo lists as proof of revenue quality, or management forecasts as the underwriting case.
- Prefer ranges and sensitivities to false precision.
- State what would cause the committee to stop, reprice, restructure, reduce size, reserve more capital, or reverse a prior approval.

## Method basis

The workflow adapts useful elements from the Anthropic PE IC memo skill indexed by N.E.I., N.E.I.'s IC workbench, public Bessemer venture memos, and ILPA investment-process materials. Read [references/design-basis.md](references/design-basis.md) when maintaining or materially revising this skill.
