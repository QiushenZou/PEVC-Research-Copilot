# Changelog

## 1.0.0 - 2026-09-10

- Added `pevc-research-router` as a thin task and handoff coordinator.
- Split neutral BP fact extraction and fund-specific screening into `pevc-bp-fact-card` and `pevc-deal-screening`.
- Narrowed `pevc-company-diligence` to claim verification, full diligence, refresh, and red-flag work.
- Added shared project-manifest, evidence-bundle, and decision-record schemas.
- Added deterministic project-bundle checks for source references, evidence states, valuation bridges, and MOIC/IRR consistency.
- Added a synthetic end-to-end project, negative tests, repository validation, CI, and a complete Chinese usage guide.
- Documented optional, de-identified N.E.I. MCP method discovery while keeping confidential execution local.

## 0.1.0 - 2026-09-10

- Added `pevc-industry-chain-mapper` with structured data validation and interactive HTML rendering.
- Added `pevc-company-diligence` for evidence-backed target-company diligence.
- Added `pevc-ic-memo` for screening, preliminary, final, update, and challenge-review investment memos.
- Added a shared three-stage research workflow and handoff quality gates.
- Documented installation, methodology provenance, confidentiality boundaries, and the pre-publication release checklist.
