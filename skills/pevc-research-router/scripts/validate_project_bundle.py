#!/usr/bin/env python3
"""Validate a PE/VC project manifest, evidence bundle, and decision record.

Uses only the Python standard library so it can run in a clean Codex workspace.
The JSON Schema files document the contract; this script enforces the material
cross-file and investment-arithmetic invariants that generic schema validation
does not cover.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any


FACT_STATUSES = {
    "verified_fact",
    "management_claim",
    "third_party_estimate",
    "calculation",
    "inference",
    "investment_view",
    "open_question",
    "conflict",
}
CONFIDENCE = {"high", "medium", "low", "unknown"}
WORKFLOW_STAGES = {
    "intake",
    "screening",
    "industry-research",
    "diligence",
    "preliminary-ic",
    "final-ic",
    "update",
}
DECISION_STAGES = {"screening", "preliminary-ic", "final-ic", "update"}
RECOMMENDATIONS = {
    "decline",
    "hold",
    "continue-diligence",
    "approve-preliminary-work",
    "approve",
    "approve-with-conditions",
    "reconfirm",
    "reprice",
    "restructure",
    "reduce-size",
}
OPEN_PRIORITIES = {"P0", "P1", "P2"}
OPEN_STATUSES = {"not-started", "requested", "received", "in-review", "complete", "blocked", "red-flag"}


def read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"missing file: {path}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read JSON {path}: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"top level must be an object: {path}")
        return None
    return data


def require(obj: dict[str, Any], keys: tuple[str, ...], label: str, errors: list[str]) -> None:
    for key in keys:
        if key not in obj or obj[key] in (None, ""):
            errors.append(f"{label}: missing or empty {key}")


def check_date(value: Any, label: str, errors: list[str], *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str):
        errors.append(f"{label}: expected ISO date")
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: expected YYYY-MM-DD, got {value!r}")


def duplicate_ids(items: Any, key: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{label}: must be a list")
        return set()
    values: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}]: must be an object")
            continue
        value = item.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"{label}[{index}]: missing {key}")
            continue
        values.append(value)
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    for value in sorted(duplicates):
        errors.append(f"{label}: duplicate {key} {value}")
    return set(values)


def close(a: float, b: float, tolerance: float = 0.01) -> bool:
    scale = max(abs(a), abs(b), 1.0)
    return abs(a - b) / scale <= tolerance


def validate_manifest(data: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    require(data, ("schema_version", "project_id", "as_of_date", "workflow_stage", "investment_type", "scope", "decision"), "manifest", errors)
    if data.get("schema_version") != "1.0":
        errors.append("manifest.schema_version must be '1.0'")
    check_date(data.get("as_of_date"), "manifest.as_of_date", errors)
    if data.get("workflow_stage") not in WORKFLOW_STAGES:
        errors.append(f"manifest.workflow_stage invalid: {data.get('workflow_stage')}")
    if data.get("investment_type") not in {"pe-control", "growth-minority", "vc", "undetermined"}:
        errors.append(f"manifest.investment_type invalid: {data.get('investment_type')}")
    scope = data.get("scope")
    if isinstance(scope, dict):
        require(scope, ("geography", "time_horizon", "included", "excluded"), "manifest.scope", errors)
        if not scope.get("company") and not scope.get("industry") and not scope.get("product"):
            errors.append("manifest.scope: at least one of company, industry, or product is required")
    else:
        errors.append("manifest.scope must be an object")
    decision = data.get("decision")
    if isinstance(decision, dict):
        require(decision, ("current_gate", "requested_authority"), "manifest.decision", errors)
        check_date(decision.get("deadline"), "manifest.decision.deadline", errors, nullable=True)
    else:
        errors.append("manifest.decision must be an object")
    confidentiality = data.get("confidentiality", {})
    if confidentiality.get("classification") in {"confidential", "highly-confidential"} and confidentiality.get("external_sharing_allowed") is True:
        warnings.append("manifest: confidential project allows external sharing; verify authorization")


def validate_evidence(data: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    require(data, ("schema_version", "project_id", "as_of_date", "sources", "facts", "claims", "open_items", "change_log"), "evidence", errors)
    if data.get("schema_version") != "1.0":
        errors.append("evidence.schema_version must be '1.0'")
    check_date(data.get("as_of_date"), "evidence.as_of_date", errors)

    source_ids = duplicate_ids(data.get("sources"), "source_id", "evidence.sources", errors)
    fact_ids = duplicate_ids(data.get("facts"), "fact_id", "evidence.facts", errors)
    duplicate_ids(data.get("claims"), "claim_id", "evidence.claims", errors)
    duplicate_ids(data.get("open_items"), "item_id", "evidence.open_items", errors)

    for index, source in enumerate(data.get("sources", [])):
        if not isinstance(source, dict):
            continue
        label = f"source[{index}] {source.get('source_id', '?')}"
        require(source, ("title", "source_type", "accessed_date", "confidential"), label, errors)
        check_date(source.get("source_date"), f"{label}.source_date", errors, nullable=True)
        check_date(source.get("accessed_date"), f"{label}.accessed_date", errors)
        if source.get("confidential") and source.get("url"):
            warnings.append(f"{label}: confidential source contains a URL; verify it is not a private access link")

    for index, fact in enumerate(data.get("facts", [])):
        if not isinstance(fact, dict):
            continue
        label = f"fact[{index}] {fact.get('fact_id', '?')}"
        require(fact, ("subject", "statement", "status", "source_ids", "confidence", "decision_impact"), label, errors)
        status = fact.get("status")
        if status not in FACT_STATUSES:
            errors.append(f"{label}: invalid status {status}")
        if fact.get("confidence") not in CONFIDENCE:
            errors.append(f"{label}: invalid confidence {fact.get('confidence')}")
        refs = fact.get("source_ids")
        if not isinstance(refs, list):
            errors.append(f"{label}: source_ids must be a list")
            refs = []
        for ref in refs:
            if ref not in source_ids:
                errors.append(f"{label}: unknown source_id {ref}")
        if status in {"verified_fact", "management_claim", "third_party_estimate", "calculation", "conflict"} and not refs:
            errors.append(f"{label}: status {status} requires at least one source")
        if status == "calculation" and not fact.get("formula"):
            errors.append(f"{label}: calculation requires formula")
        if fact.get("value") is not None:
            if not fact.get("period"):
                warnings.append(f"{label}: quantified fact has no period")
            if not fact.get("actual_or_forecast"):
                warnings.append(f"{label}: quantified fact has no actual_or_forecast label")

    for index, claim in enumerate(data.get("claims", [])):
        if not isinstance(claim, dict):
            continue
        label = f"claim[{index}] {claim.get('claim_id', '?')}"
        require(claim, ("claim", "supporting_fact_ids", "counterevidence_fact_ids", "confidence", "decision_implication", "next_test"), label, errors)
        if claim.get("confidence") not in CONFIDENCE:
            errors.append(f"{label}: invalid confidence {claim.get('confidence')}")
        for field in ("supporting_fact_ids", "counterevidence_fact_ids"):
            refs = claim.get(field)
            if not isinstance(refs, list):
                errors.append(f"{label}.{field}: must be a list")
                continue
            for ref in refs:
                if ref not in fact_ids:
                    errors.append(f"{label}.{field}: unknown fact_id {ref}")
        if not claim.get("supporting_fact_ids"):
            warnings.append(f"{label}: no supporting facts; keep conclusion provisional")
        if not claim.get("counterevidence_fact_ids"):
            warnings.append(f"{label}: no recorded counterevidence; confirm a disconfirming search was attempted")
        check_date(claim.get("due_date"), f"{label}.due_date", errors, nullable=True)

    for index, item in enumerate(data.get("open_items", [])):
        if not isinstance(item, dict):
            continue
        label = f"open_item[{index}] {item.get('item_id', '?')}"
        require(item, ("priority", "question", "rationale", "evidence_requested", "status", "consequence_if_unresolved"), label, errors)
        if item.get("priority") not in OPEN_PRIORITIES:
            errors.append(f"{label}: invalid priority {item.get('priority')}")
        if item.get("status") not in OPEN_STATUSES:
            errors.append(f"{label}: invalid status {item.get('status')}")
        check_date(item.get("due_date"), f"{label}.due_date", errors, nullable=True)
        if item.get("status") == "complete" and not item.get("resolution"):
            warnings.append(f"{label}: marked complete without a resolution note")

    for index, entry in enumerate(data.get("change_log", [])):
        if not isinstance(entry, dict):
            errors.append(f"change_log[{index}]: must be an object")
            continue
        require(entry, ("date", "change", "reason"), f"change_log[{index}]", errors)
        check_date(entry.get("date"), f"change_log[{index}].date", errors)
        for ref in entry.get("source_ids", []):
            if ref not in source_ids:
                errors.append(f"change_log[{index}]: unknown source_id {ref}")


def validate_decision(data: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    require(data, ("schema_version", "project_id", "as_of_date", "decision_stage", "requested_authority", "recommendation", "thesis", "risks", "conditions", "human_review_items"), "decision", errors)
    if data.get("schema_version") != "1.0":
        errors.append("decision.schema_version must be '1.0'")
    check_date(data.get("as_of_date"), "decision.as_of_date", errors)
    if data.get("decision_stage") not in DECISION_STAGES:
        errors.append(f"decision.decision_stage invalid: {data.get('decision_stage')}")
    if data.get("recommendation") not in RECOMMENDATIONS:
        errors.append(f"decision.recommendation invalid: {data.get('recommendation')}")
    for field in ("thesis", "risks", "conditions", "human_review_items"):
        if not isinstance(data.get(field), list):
            errors.append(f"decision.{field} must be a list")

    terms = data.get("terms", {})
    if isinstance(terms, dict):
        pre = terms.get("pre_money")
        primary = terms.get("primary_proceeds")
        post = terms.get("post_money")
        ownership = terms.get("new_money_ownership_pct")
        if all(isinstance(v, (int, float)) for v in (pre, primary, post)) and not close(float(post), float(pre) + float(primary)):
            errors.append("decision.terms: post_money does not equal pre_money + primary_proceeds")
        if all(isinstance(v, (int, float)) for v in (primary, post, ownership)) and post:
            expected = float(primary) / float(post) * 100
            if not close(float(ownership), expected, tolerance=0.02):
                errors.append(f"decision.terms: new_money_ownership_pct {ownership} does not match primary/post-money {expected:.2f}%")
        ev = terms.get("enterprise_value")
        equity = terms.get("equity_value")
        debt = terms.get("debt")
        cash = terms.get("cash")
        if all(isinstance(v, (int, float)) for v in (ev, equity, debt, cash)) and not close(float(ev), float(equity) + float(debt) - float(cash)):
            errors.append("decision.terms: enterprise_value does not equal equity_value + debt - cash")
    elif terms is not None:
        errors.append("decision.terms must be an object")

    scenarios = data.get("return_scenarios", [])
    if not isinstance(scenarios, list):
        errors.append("decision.return_scenarios must be a list")
        scenarios = []
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            errors.append(f"return_scenarios[{index}] must be an object")
            continue
        label = f"return_scenarios[{index}] {scenario.get('name', '?')}"
        require(scenario, ("name", "provisional", "narrative"), label, errors)
        moic = scenario.get("moic")
        irr = scenario.get("irr_pct")
        years = scenario.get("holding_years")
        if all(isinstance(v, (int, float)) for v in (moic, irr, years)):
            if moic <= 0 or years <= 0:
                errors.append(f"{label}: moic and holding_years must be positive")
            else:
                expected = (math.pow(float(moic), 1.0 / float(years)) - 1.0) * 100.0
                if abs(float(irr) - expected) > 0.75:
                    errors.append(f"{label}: irr_pct {irr} is inconsistent with MOIC/holding years ({expected:.2f}%)")
        elif not scenario.get("provisional"):
            errors.append(f"{label}: missing return inputs must be marked provisional")

    if data.get("decision_stage") == "final-ic":
        if not scenarios:
            warnings.append("decision: final IC has no return scenarios")
        if not data.get("model_version"):
            warnings.append("decision: final IC has no model_version")
    if data.get("recommendation") == "approve-with-conditions" and not data.get("conditions"):
        errors.append("decision: approve-with-conditions requires at least one explicit condition")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="Directory containing project-manifest.json and evidence-bundle.json")
    parser.add_argument("--require-decision", action="store_true", help="Require decision-record.json even before an IC stage")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    root = args.project_dir
    manifest = read_json(root / "project-manifest.json", errors)
    evidence = read_json(root / "evidence-bundle.json", errors)
    decision_path = root / "decision-record.json"
    decision = read_json(decision_path, errors) if decision_path.exists() or args.require_decision else None

    if manifest:
        validate_manifest(manifest, errors, warnings)
    if evidence:
        validate_evidence(evidence, errors, warnings)
    if decision:
        validate_decision(decision, errors, warnings)

    project_ids = [x.get("project_id") for x in (manifest, evidence, decision) if x]
    if project_ids and len(set(project_ids)) != 1:
        errors.append(f"cross-file project_id mismatch: {project_ids}")
    as_of_dates = [x.get("as_of_date") for x in (manifest, evidence, decision) if x]
    if as_of_dates and len(set(as_of_dates)) != 1:
        warnings.append(f"cross-file as_of_date differs: {as_of_dates}; confirm intentional update timing")
    if manifest and manifest.get("workflow_stage") in {"preliminary-ic", "final-ic", "update"} and not decision:
        errors.append("manifest workflow_stage requires decision-record.json")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: project bundle valid with {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
