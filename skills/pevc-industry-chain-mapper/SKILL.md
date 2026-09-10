---
name: pevc-industry-chain-mapper
description: Research an industry's real upstream-to-downstream structure and generate a source-backed interactive value-chain map with company roles, node explainers, investment views, metrics, and diligence questions. Use for PE/VC industry-chain mapping, value-chain research, industry learning maps, or updates to an existing industry map; do not use for a company-only memo unless an industry map is also requested.
---

# PE/VC Industry Chain Mapper

Create a decision-useful industry map, not a decorative mind map and not an IC memo disguised as a value chain. The map must let a newcomer understand what physically or economically moves from upstream to downstream, then open any node to see how that node works, who participates, how value is captured, and what an investor still needs to verify.

## Modes

- **Build:** research a new industry and create structured data plus an interactive map.
- **Revise:** improve an existing map while preserving correct content and user-approved visual choices.
- **Refresh:** update companies, facts, dates, sources, and investment views without silently changing scope.
- **Audit:** identify missing nodes, unsupported claims, role confusion, stale sources, and broken interactions.

## Research gates

1. **Frame the research.** Define the decision purpose, product, geography, time horizon, public/private company universe, and adjacent-market exclusions. Diagnose the industry's lifecycle and demand state before deciding research depth. Put this compact orientation in map metadata, never in the chain itself.
2. **Build the skeleton from transactions.** Start with the end customer and work backward to the enabling inputs. For every proposed stage, identify the transformation, output, immediate paying customer, and edge to the next stage. Stage titles must be genuine chain stages. Never use “investment judgment,” “valuation,” “risk,” “business model,” or “exit path” as a stage.
3. **Route by industry economics.** Do not reuse generic SaaS, manufacturing, semiconductor, biotech, consumer, or infrastructure metrics across sectors. Select the bottlenecks, maturity tests, and operating metrics that determine commercialization in this industry. Read [references/research-methodology.md](references/research-methodology.md) for routing guidance.
4. **Map support layers honestly.** Represent software, standards, certification, distribution, or infrastructure as `support` layers when they span several chain stages. Do not force a horizontal capability into one linear column.
5. **Research current evidence.** Prefer standards, regulators, government sources, filings, audited reports, technical documentation, and official product material. Triangulate consequential market-size, customer, capacity, pricing, and share claims rather than repeating one source.
6. **Attach companies to roles.** Put companies inside node details, not node titles. Distinguish verified suppliers, customers, participants, reported PoCs, representative targets, and analyst inference. A company name without a role and node-level evidence is not useful.
7. **Explain value and transmission.** For every node, show monetization, major cost drivers, bargaining power, profit-pool logic, technology routes, and the mechanism by which price, capacity, demand, or technical constraints pass to adjacent nodes. Every edge needs a concise transmission explanation.
8. **Write and verify structured data.** Follow [references/schema.md](references/schema.md). Separate fact, inference, and opinion; never convert partnerships or ecosystem membership into production deployment. Run `scripts/validate_industry_data.py`, fix errors, and review warnings rather than suppressing them.
9. **Render and visually inspect.** Run `scripts/render_map.py <data.json> <output.html>`. Open the result and verify initial fit, no overlap, directional arrows, node-to-node highlighting, click-to-open details, search, mouse/trackpad navigation, links, and narrow-screen behavior.

## Node writing standard

Write for an intelligent newcomer. Be concise but not simplistic.

- **Definition and chain position:** use 2–4 plain-language sentences, then state inputs, transformation, outputs, immediate customers, and payer. Across the drawer, aim for roughly 7–12 concise sentences rather than one dense paragraph.
- **Companies:** normally 3–8 relevant names, grouped by role or geography when useful. Cite every company-role assertion.
- **Technology routes:** name the competing routes, maturity, trade-off, and observable adoption signal. Do not list technologies without explaining why the choice matters.
- **Economics:** state how the node earns revenue, the main cost drivers, who has bargaining power, where profit can pool, and how shocks transmit upstream or downstream.
- **Competition:** identify the few variables that actually determine differentiation; add concentration only when the market definition and denominator are defensible.
- **Metrics:** provide 3–5 industry-specific indicators. For each, explain why it matters and what movement would strengthen or weaken the node thesis.
- **Investment view:** explain profit capture, moat, catalyst, risk, and the next observable fact that would change the view. Keep fact and opinion visibly distinct.
- **Diligence:** ask 3–5 questions that distinguish samples, PoCs, design wins, production deployments, repeat purchases, and durable economics.
- **Sources:** attach directly relevant sources at claim-bearing levels; do not rely only on a generic industry homepage.

## Output rules

- Produce both `<industry>-industry-data.json` and `<industry>-industry-map.html`.
- Preserve the structured JSON as the source of truth. Do not hand-edit generated node content inside the HTML.
- Use an `as_of_date` and display it in the map.
- Keep lifecycle, demand state, market definition, key debates, valuation, and recommendations in compact orientation or node details. They are analytical lenses, not chain stages.
- Keep company names out of map-node titles unless the node is explicitly a company-comparison node requested by the user.
- Directional edges must represent a product, service, supply, support, or demand flow and must disclose the transmission mechanism in the connected node drawer.
- Default navigation: trackpad two-finger pan and pinch zoom; mouse mode wheel zoom and drag pan. Clicking without dragging opens that node's detail.
- Keep the map readable at first view; allow focus/zoom for detail rather than shrinking all text to fit.

## References

- Read [references/research-methodology.md](references/research-methodology.md) when defining stages, company roles, evidence status, or adjacent-market boundaries.
- Read [references/schema.md](references/schema.md) before creating or repairing the data file.
- Read [references/quality-checklist.md](references/quality-checklist.md) before final delivery or when auditing an existing map.
