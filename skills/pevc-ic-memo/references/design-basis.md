# Design basis and source notes

Use this file when maintaining the skill. It records which external workflows were studied and which design choices were retained. It is not a substitute for citing the deal evidence used in an actual memo.

## 1. Anthropic PE `ic-memo` skill

Sources:

- N.E.I. catalog copy: <https://nei-pevc.com/posts/51>
- Anthropic source path: <https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/private-equity/skills/ic-memo/SKILL.md>
- Accessed 2026-09-10.

The exact source was reviewed. Its useful mechanics are:

- gather company, industry, historical financial, management, deal-term, diligence, value-creation, and returns inputs before drafting;
- use a familiar IC sequence covering executive summary, company, market, financials, thesis, terms, returns, risks, and recommendation;
- default to an editable Word deliverable while allowing Markdown;
- use financial and returns tables, maintain a balanced bull/bear presentation, honor the firm's template, reconcile key calculations, and avoid inventing missing deal terms.

This skill preserves those principles but does not copy the source structure mechanically. It adds stage routing, VC/minority treatment, claim-level evidence, update/addendum controls, decision thresholds, approval-condition logic, and stronger downside and fund-return tests.

N.E.I. identifies the original as Anthropic's PE IC memo skill and records the upstream license as Apache License 2.0. Preserve this attribution if materially redistributing derivative instructions.

## 2. N.E.I. IC workbench and investment-report workflow

Sources:

- IC workbench: <https://nei-pevc.com/tasks/ic-memo>
- “一键生成VCPE投资建议书（Word格式）”: <https://nei-pevc.com/posts/146>
- Accessed 2026-09-10.

Useful workflow lessons:

- separate analytical memo drafting from formal Word production, Office processing, and final format QA;
- maintain a shared structured fact base across chapters rather than allowing each section to invent its own numbers;
- archive public-source workpapers and make the final document reproducible;
- generate a formal deliverable only after the analytical sections are complete.

This skill adopts the single-source-of-truth and traceability logic while remaining tool-agnostic: it must work with local documents, connected data, public research, or user-provided evidence without requiring NotebookLM, iFind, or a particular search vendor.

## 3. Bessemer Venture Partners public investment memos

Sources:

- Memo library: <https://www.bvp.com/memos>
- Twilio seed memo: <https://www.bvp.com/memos/twilio>
- Shopify Series A memo: <https://www.bvp.com/memos/shopify>
- Accessed 2026-09-10.

Useful VC lessons:

- lead with the exact investment ask and recommendation;
- use stage-appropriate proof rather than imposing mature-company evidence on seed investing;
- make uncertainties explicit and use a smaller or staged commitment to buy information when appropriate;
- connect product, customer behavior, distribution, unit economics, team, financing, and outcome analysis directly to the recommendation;
- treat founder/team adaptability and learning velocity as evidence because early products and markets can change materially.

The public memos also show why a VC memo should preserve what was knowable at the decision date rather than rewrite history with hindsight.

## 4. ILPA investment-process materials

Source:

- ILPA Due Diligence 101 process material: <https://ilpa.org/wp-content/uploads/2015/09/ILPA-Workshops-2015_Due-Diligence-101.pdf>
- Accessed 2026-09-10.

Useful process lesson: the decision memorandum should document diligence findings, key issues, financial analysis including scenario sensitivities, and reference work before the investment committee makes the commitment decision. This supports the skill's evidence ledger, scenario discipline, and explicit decision gate.

## Maintenance rule

When incorporating another memo template or workflow, extract only decisions that improve routing, evidence quality, calculation integrity, or committee usability. Do not accumulate headings merely because another institution uses them. Preserve the firm's supplied template and approval vocabulary when the user provides them.
