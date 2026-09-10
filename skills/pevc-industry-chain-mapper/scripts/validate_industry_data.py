#!/usr/bin/env python3
"""Validate PE/VC industry-chain research data before rendering."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


COMPANY_STATUSES = {
    "verified_supplier",
    "verified_customer",
    "verified_participant",
    "reported_poc",
    "representative_target",
    "inference",
}
EDGE_TYPES = {"supply", "product", "service", "demand", "support"}
FORBIDDEN_STAGE_TERMS = {
    "投资判断",
    "投资建议",
    "估值",
    "退出路径",
    "风险判断",
    "商业模式",
    "市场规模",
    "竞争格局",
    "政策环境",
    "business model",
    "valuation",
    "exit path",
    "market size",
}
ORIENTATION_FIELDS = {
    "purpose",
    "lifecycle_stage",
    "lifecycle_basis",
    "demand_state",
    "market_definition",
    "key_debates",
    "source_ids",
}
CHAIN_ROLE_FIELDS = {"inputs", "transformation", "outputs", "customers", "payer"}
ECONOMICS_FIELDS = {
    "revenue_model",
    "cost_drivers",
    "bargaining_power",
    "profit_pool_logic",
    "price_or_capacity_transmission",
}
TECHNOLOGY_FIELDS = {"name", "maturity", "trade_off", "adoption_signal", "source_ids"}
METRIC_FIELDS = {"name", "why_it_matters", "signal", "source_ids"}
INVESTMENT_FIELDS = {"thesis", "moat", "catalyst", "risk", "watch"}


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def nonempty(value: object) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def check_fields(obj: dict, fields: set[str], label: str, errors: list[str]) -> None:
    for key in sorted(fields):
        if not nonempty(obj.get(key)):
            errors.append(f"{label}: missing or empty {key}")


def check_source_ids(
    ids: object,
    source_set: set[str],
    label: str,
    errors: list[str],
    *,
    required: bool = True,
) -> set[str]:
    if not isinstance(ids, list):
        errors.append(f"{label}: source_ids must be a list")
        return set()
    if required and not ids:
        errors.append(f"{label}: at least one source_id is required")
    result = set(ids)
    for source_id in ids:
        if source_id not in source_set:
            errors.append(f"{label}: references unknown source {source_id}")
    return result


def valid_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in ("title", "as_of_date", "scope", "orientation", "stages", "nodes", "edges", "sources"):
        if key not in data:
            errors.append(f"missing top-level field: {key}")
    if errors:
        return errors, warnings

    if not valid_iso_date(data["as_of_date"]):
        errors.append("as_of_date must use YYYY-MM-DD")

    scope = data["scope"]
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
    else:
        check_fields(
            scope,
            {"product", "geography", "time_horizon", "company_universe", "included", "excluded"},
            "scope",
            errors,
        )
        for key in ("included", "excluded"):
            if key in scope and not isinstance(scope[key], list):
                errors.append(f"scope.{key} must be a list")

    stages = data["stages"]
    nodes = data["nodes"]
    edges = data["edges"]
    sources = data["sources"]
    if not all(isinstance(x, list) for x in (stages, nodes, edges, sources)):
        errors.append("stages, nodes, edges, and sources must be lists")
        return errors, warnings

    stage_ids = [x.get("id") for x in stages]
    node_ids = [x.get("id") for x in nodes]
    source_ids = [x.get("id") for x in sources]

    for label, values in (("stage", stage_ids), ("node", node_ids), ("source", source_ids)):
        if None in values or "" in values:
            errors.append(f"{label} ids must be non-empty")
        if len(values) != len(set(values)):
            errors.append(f"duplicate {label} ids")

    stage_set, node_set, source_set = set(stage_ids), set(node_ids), set(source_ids)

    orientation = data["orientation"]
    if not isinstance(orientation, dict):
        errors.append("orientation must be an object")
    else:
        check_fields(orientation, ORIENTATION_FIELDS, "orientation", errors)
        check_source_ids(orientation.get("source_ids"), source_set, "orientation", errors)
        if not isinstance(orientation.get("key_debates"), list):
            errors.append("orientation.key_debates must be a list")

    chain_stages = [x for x in stages if x.get("kind", "chain") == "chain"]
    if len(chain_stages) < 2:
        errors.append("at least two chain stages are required")
    orders = [x.get("order") for x in chain_stages]
    if any(not isinstance(x, (int, float)) for x in orders):
        errors.append("chain stages require numeric order")
    elif len(orders) != len(set(orders)):
        errors.append("chain stage order values must be unique")

    for stage in stages:
        sid = stage.get("id", "<unknown>")
        kind = stage.get("kind", "chain")
        if kind not in {"chain", "support"}:
            errors.append(f"stage {sid}: kind must be chain or support")
        title = str(stage.get("title", ""))
        if kind == "chain" and any(term.lower() in title.lower() for term in FORBIDDEN_STAGE_TERMS):
            errors.append(f"stage {sid}: '{title}' is an analytical lens, not a chain stage")
        if not stage.get("description"):
            warnings.append(f"stage {sid}: missing description")
        if not any(node.get("stage_id") == sid for node in nodes):
            errors.append(f"stage {sid}: contains no nodes")

    nested_source_refs: set[str] = set()
    node_source_map: dict[str, set[str]] = {}
    for node in nodes:
        nid = node.get("id", "<unknown>")
        sid = node.get("stage_id")
        if sid not in stage_set:
            errors.append(f"node {nid}: unknown stage_id {sid}")
        required = {
            "title",
            "summary",
            "chain_role",
            "companies",
            "technology_routes",
            "economics",
            "competition",
            "metrics",
            "investment_view",
            "diligence_questions",
            "source_ids",
        }
        check_fields(node, required, f"node {nid}", errors)
        node_sources = check_source_ids(node.get("source_ids"), source_set, f"node {nid}", errors)
        node_source_map[nid] = node_sources

        role = node.get("chain_role", {})
        if not isinstance(role, dict):
            errors.append(f"node {nid}: chain_role must be an object")
        else:
            check_fields(role, CHAIN_ROLE_FIELDS, f"node {nid}: chain_role", errors)
            for key in ("inputs", "outputs", "customers"):
                if key in role and not isinstance(role[key], list):
                    errors.append(f"node {nid}: chain_role.{key} must be a list")

        companies = node.get("companies", [])
        if not isinstance(companies, list):
            errors.append(f"node {nid}: companies must be a list")
            companies = []
        if len(companies) < 1:
            errors.append(f"node {nid}: at least one company is required")
        if len(companies) < 3:
            warnings.append(f"node {nid}: fewer than three companies; confirm this reflects market reality")
        for index, company in enumerate(companies, 1):
            label = f"node {nid}: company {index}"
            check_fields(company, {"name", "role", "evidence_status", "source_ids"}, label, errors)
            status = company.get("evidence_status")
            if status not in COMPANY_STATUSES:
                errors.append(f"{label}: invalid evidence_status {status}")
            refs = check_source_ids(company.get("source_ids"), source_set, label, errors)
            nested_source_refs.update(refs)
            if not refs.issubset(node_sources):
                errors.append(f"{label}: nested source_ids must also appear in node source_ids")

        routes = node.get("technology_routes", [])
        if not isinstance(routes, list) or not routes:
            errors.append(f"node {nid}: technology_routes must be a non-empty list")
            routes = []
        for index, route in enumerate(routes, 1):
            label = f"node {nid}: technology route {index}"
            check_fields(route, TECHNOLOGY_FIELDS, label, errors)
            refs = check_source_ids(route.get("source_ids"), source_set, label, errors)
            nested_source_refs.update(refs)
            if not refs.issubset(node_sources):
                errors.append(f"{label}: nested source_ids must also appear in node source_ids")

        economics = node.get("economics", {})
        if not isinstance(economics, dict):
            errors.append(f"node {nid}: economics must be an object")
        else:
            check_fields(economics, ECONOMICS_FIELDS, f"node {nid}: economics", errors)
            if "cost_drivers" in economics and not isinstance(economics["cost_drivers"], list):
                errors.append(f"node {nid}: economics.cost_drivers must be a list")

        if "competition" in node and not isinstance(node["competition"], list):
            errors.append(f"node {nid}: competition must be a list")

        metrics = node.get("metrics", [])
        if not isinstance(metrics, list) or len(metrics) < 3:
            errors.append(f"node {nid}: at least three structured metrics are required")
            metrics = []
        if len(metrics) > 5:
            warnings.append(f"node {nid}: more than five metrics may reduce decision focus")
        for index, metric in enumerate(metrics, 1):
            label = f"node {nid}: metric {index}"
            if not isinstance(metric, dict):
                errors.append(f"{label}: metric must be an object with why_it_matters and signal")
                continue
            check_fields(metric, METRIC_FIELDS, label, errors)
            refs = check_source_ids(metric.get("source_ids"), source_set, label, errors)
            nested_source_refs.update(refs)
            if not refs.issubset(node_sources):
                errors.append(f"{label}: nested source_ids must also appear in node source_ids")

        questions = node.get("diligence_questions", [])
        if not isinstance(questions, list) or len(questions) < 3:
            errors.append(f"node {nid}: at least three diligence questions are required")
        if isinstance(questions, list) and len(questions) > 5:
            warnings.append(f"node {nid}: more than five diligence questions may reduce focus")

        view = node.get("investment_view", {})
        if not isinstance(view, dict):
            errors.append(f"node {nid}: investment_view must be an object")
        else:
            check_fields(view, INVESTMENT_FIELDS, f"node {nid}: investment_view", errors)

    for edge in edges:
        start, end = edge.get("from"), edge.get("to")
        label = f"edge {start}->{end}"
        if start not in node_set or end not in node_set:
            errors.append(f"{label}: unknown node")
        if start == end:
            errors.append(f"{label}: self-loop is not allowed")
        if edge.get("type") not in EDGE_TYPES:
            errors.append(f"{label}: invalid type {edge.get('type')}")
        check_fields(edge, {"label", "mechanism", "source_ids"}, label, errors)
        refs = check_source_ids(edge.get("source_ids"), source_set, label, errors)
        nested_source_refs.update(refs)
        for endpoint in (start, end):
            if endpoint in node_source_map and not refs.issubset(node_source_map[endpoint]):
                errors.append(f"{label}: edge source_ids must also appear in endpoint node {endpoint} source_ids")

    if len({(e.get("from"), e.get("to"), e.get("type")) for e in edges}) != len(edges):
        warnings.append("duplicate directed edge/type combinations detected")

    chain_sorted = sorted(chain_stages, key=lambda x: x.get("order", 0))
    for left, right in zip(chain_sorted, chain_sorted[1:]):
        left_nodes = {n.get("id") for n in nodes if n.get("stage_id") == left.get("id")}
        right_nodes = {n.get("id") for n in nodes if n.get("stage_id") == right.get("id")}
        crosses = any(
            edge.get("from") in left_nodes
            and edge.get("to") in right_nodes
            and edge.get("type") != "support"
            for edge in edges
        )
        if not crosses:
            warnings.append(f"no forward edge connects adjacent chain stages {left.get('id')} -> {right.get('id')}")

    connected_nodes = {e.get("from") for e in edges} | {e.get("to") for e in edges}
    for node in nodes:
        if node.get("id") not in connected_nodes:
            warnings.append(f"node {node.get('id')}: orphan node has no incoming or outgoing edge")

    for source in sources:
        sid = source.get("id", "<unknown>")
        check_fields(source, {"title", "publisher", "url", "accessed_date", "source_type", "supports"}, f"source {sid}", errors)
        parsed = urlparse(str(source.get("url", "")))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"source {sid}: invalid URL")
        if not valid_iso_date(source.get("accessed_date")):
            errors.append(f"source {sid}: accessed_date must use YYYY-MM-DD")
        elif valid_iso_date(data["as_of_date"]) and source["accessed_date"] > data["as_of_date"]:
            warnings.append(f"source {sid}: accessed_date is later than as_of_date")
        published = source.get("published_date")
        if published is not None and not valid_iso_date(published):
            errors.append(f"source {sid}: published_date must be null or YYYY-MM-DD")
        if "supports" in source and not isinstance(source["supports"], list):
            errors.append(f"source {sid}: supports must be a list")

    top_refs = set(orientation.get("source_ids", [])) if isinstance(orientation, dict) else set()
    top_refs.update(source_id for node in nodes for source_id in node.get("source_ids", []))
    top_refs.update(nested_source_refs)
    unused = source_set - top_refs
    if unused:
        warnings.append("unreferenced sources: " + ", ".join(sorted(unused)))
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        data = load(args.input)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors, warnings = validate(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(
        f"OK: {len(data['stages'])} stages, {len(data['nodes'])} nodes, "
        f"{len(data['edges'])} edges, {len(data['sources'])} sources; {len(warnings)} warning(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
