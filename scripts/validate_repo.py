#!/usr/bin/env python3
"""Run repository-level structural and example validation."""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for skill in sorted((repo / "skills").iterdir()):
        if not skill.is_dir():
            continue
        entry = skill / "SKILL.md"
        metadata = skill / "agents" / "openai.yaml"
        if not entry.exists():
            errors.append(f"{skill.name}: missing SKILL.md")
            continue
        text = entry.read_text(encoding="utf-8")
        if not text.startswith("---\n") or f"name: {skill.name}\n" not in text:
            errors.append(f"{skill.name}: invalid or mismatched frontmatter name")
        if "description:" not in text.split("---", 2)[1]:
            errors.append(f"{skill.name}: missing description")
        if not metadata.exists():
            errors.append(f"{skill.name}: missing agents/openai.yaml")
        elif f"${skill.name}" not in metadata.read_text(encoding="utf-8"):
            errors.append(f"{skill.name}: default prompt does not mention ${skill.name}")

    for path in sorted((repo / "skills" / "pevc-research-router" / "references" / "schemas").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(repo)}: invalid JSON: {exc}")

    eval_path = repo / "evals" / "cases.json"
    try:
        eval_cases = json.loads(eval_path.read_text(encoding="utf-8"))
        skill_names = {path.name for path in (repo / "skills").iterdir() if path.is_dir()}
        if not isinstance(eval_cases, list) or not eval_cases:
            errors.append("evals/cases.json must contain a non-empty list")
        else:
            case_ids: set[str] = set()
            for case in eval_cases:
                if case.get("id") in case_ids:
                    errors.append(f"evals/cases.json duplicate id: {case.get('id')}")
                case_ids.add(case.get("id"))
                if case.get("skill") not in skill_names:
                    errors.append(f"eval {case.get('id')}: unknown skill {case.get('skill')}")
                for field in ("request", "must_do", "must_not_do"):
                    if not case.get(field):
                        errors.append(f"eval {case.get('id')}: missing {field}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"evals/cases.json invalid: {exc}")

    for path in sorted(repo.rglob("*.py")):
        if ".git" in path.parts:
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{path.relative_to(repo)}: {exc}")

    bundle = subprocess.run(
        [sys.executable, str(repo / "scripts" / "validate_project_bundle.py"), str(repo / "examples" / "synthetic-project"), "--require-decision"],
        text=True,
        capture_output=True,
        check=False,
    )
    if bundle.returncode:
        errors.append("synthetic project bundle failed:\n" + bundle.stdout + bundle.stderr)

    map_data = repo / "examples" / "synthetic-industry-map" / "industry-data.json"
    map_validator = repo / "skills" / "pevc-industry-chain-mapper" / "scripts" / "validate_industry_data.py"
    map_renderer = repo / "skills" / "pevc-industry-chain-mapper" / "scripts" / "render_map.py"
    map_check = subprocess.run(
        [sys.executable, str(map_validator), str(map_data)],
        text=True,
        capture_output=True,
        check=False,
    )
    if map_check.returncode:
        errors.append("synthetic industry map failed validation:\n" + map_check.stdout + map_check.stderr)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "synthetic-industry-map.html"
            render = subprocess.run(
                [sys.executable, str(map_renderer), str(map_data), str(output)],
                text=True,
                capture_output=True,
                check=False,
            )
            if render.returncode or not output.exists() or output.stat().st_size < 10000:
                errors.append("synthetic industry map failed rendering:\n" + render.stdout + render.stderr)

    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(repo / "tests"), "-p", "test_*.py"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if tests.returncode:
        errors.append("unit tests failed:\n" + tests.stdout + tests.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} repository issue(s)")
        return 1
    print("OK: repository structure, schemas, scripts, example bundle, and tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
