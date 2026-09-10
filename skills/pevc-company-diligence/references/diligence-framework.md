# Company diligence framework

Use only the modules relevant to the decision, but do not omit a module that could plausibly reverse the recommendation.

## 0. Decision frame and gates

Record the decision being made, deadline, deal stage, security, control rights, check size, proposed valuation, and known fund constraints. Distinguish:

- **Eligibility gates:** sector, geography, stage, ownership, check size, concentration, regulatory or mandate restrictions.
- **Underwriting questions:** claims that determine growth, margin, cash need, downside, and return.
- **Execution gates:** information, approvals, customer references, legal/tax work, or milestones required before signing or closing.

The initial fund gate belongs in `pevc-deal-screening`. Company diligence should inherit that gate and test the claims capable of changing it. If no screening decision exists, record the intended decision and explicit diligence questions rather than inventing fund criteria.

## 1. Business model and value proposition

- Customer problem, urgency, and cost of doing nothing
- Economic buyer, user, influencer, and procurement owner
- Product or service delivered and required complements
- Pricing unit, contract structure, revenue recognition, and collection terms
- Gross-profit formation and the resources required to deliver each unit
- Scalability constraints and incremental capital requirements

## 2. Market position

- Addressed segment rather than generic industry size
- Demand drivers, adoption barriers, and replacement cycle
- Direct competitors, substitutes, internal build, and “do nothing”
- Win/loss reasons and the conditions under which each competitor wins
- Route to market, partner dependence, and sales-cycle economics

## 3. Product and technology

- Plain-language architecture and workflow position
- Product maturity: prototype, sample, pilot, design win, production, scaled deployment
- Performance dimensions that customers actually purchase
- Roadmap dependencies, technical debt, security, reliability, and certification
- IP ownership, third-party components, open-source exposure, and key-person dependence
- Switching costs, integration depth, data advantage, and interoperability

## 4. Customers and revenue quality

- Customer count and definitions of active, paying, repeat, and churned
- Concentration, cohort behavior, retention, expansion, and contraction
- Contract duration, termination rights, acceptance clauses, rebates, and warranties
- Pipeline stages, historical conversion, sales cycle, backlog quality, and cancellations
- Related-party, channel stuffing, pass-through, reseller, or non-recurring revenue
- Referenceability and evidence of actual use in production
- Customer evidence sample spanning top revenue accounts, recent wins, churn/losses, and strategically important deployments rather than only management-selected advocates
- Separate user, technical evaluator, economic buyer, procurement owner, and payer; their views answer different questions

## 5. Financial quality

- Three-year or longest available income statement, balance sheet, and cash flow trend
- Revenue bridge by product, customer, geography, and recurring/non-recurring type
- Gross-margin bridge: price, mix, utilization, yield, input cost, service burden
- Operating expense by function and distinction between growth investment and maintenance spend
- Working capital, capital expenditure, capitalization, taxes, and cash conversion
- Debt, guarantees, off-balance-sheet obligations, contingent liabilities, and funding runway

Build the smallest set of bridges that can falsify the underwriting case:

- **Revenue-to-cash:** opening receivables + revenue ± tax/other items − closing receivables − write-offs = implied collections; reconcile to cash records where available.
- **EBITDA-to-free-cash-flow:** reported EBITDA − cash taxes − cash interest − working-capital investment − maintenance capex − recurring capitalized costs ± other recurring cash items.
- **Gross margin:** price, mix, volume/utilization, yield, input cost, channel, cloud/hosting, implementation, support, warranty, freight, and pass-through effects.
- **Forecast credibility:** compare prior budgets with actuals before relying on the current plan; separate signed backlog, probability-weighted pipeline, management target, and analyst case.

## 6. Organization and governance

- Founder and management fit for the next stage
- Sales, product, engineering, operations, finance, and compliance depth
- Incentives, related-party transactions, board oversight, and reporting quality
- Hiring bottlenecks, key-person risk, turnover, and succession

## 7. PE and VC branching

### PE/control or growth buyout emphasis

- Normalized EBITDA and quality of add-backs
- Maintenance versus growth capex
- Cash conversion and debt-service capacity
- Operational improvement levers and execution ownership
- Downside covenant headroom and refinancing risk
- Working-capital peg, debt-like items, leakage, and closing-account exposure
- Management rollover, succession, carve-out or separation dependencies, and the owner's ability to execute operational levers
- Entry-to-exit value bridge separating organic growth, margin improvement, deleveraging, add-ons, and multiple change

### VC/minority growth emphasis

- Product-market fit and repeatability of go-to-market
- ARR quality, retention, burn multiple, runway, and milestone financing
- Ownership, dilution, liquidation preference, pro rata, and follow-on reserves
- Technology and market timing risk
- Exit outcomes required to return the fund
- Stage-appropriate proof: repeat demand and velocity matter more than mature margins at early stage; efficient scaling and governance matter more at growth stage
- Milestone-to-cash plan: next technical/commercial milestone, time and cash required, evidence of achievement, and financing contingency
- Cap-table and preference-stack outcomes across down, flat, and up exits; do not use headline ownership alone

## 8. Business-model branches

Apply only the relevant branch:

- **Software/SaaS:** ARR definition, cohort retention, expansion/contraction, implementation burden, hosting/support cost, CAC payback, sales capacity, and usage-to-renewal linkage.
- **Manufacturing/hard tech:** prototype-to-sample-to-certification-to-design-win-to-serial-production status, yield, utilization, qualification time, bill of materials, supply bottlenecks, warranties, and capex-to-capacity conversion.
- **Consumer/brand:** sell-in versus sell-through, channel inventory, returns, discounting, repeat purchase, contribution after traffic acquisition and fulfillment, and distributor dependence.
- **Marketplace/transaction:** GMV-to-net-revenue bridge, take rate, subsidies, leakage/disintermediation, liquidity by local market, and cohort contribution.
- **Healthcare/life sciences:** clinical or validation evidence, regulatory path, reimbursement and payer mix, CMC/manufacturing, adoption workflow, cash to next value-inflection milestone.
- **Project/ToB/ToG:** order-to-acceptance-to-revenue-to-collection timeline, tender coverage, project gross margin, performance obligations, receivables aging, guarantees, and repeatability outside relationship-led wins.
