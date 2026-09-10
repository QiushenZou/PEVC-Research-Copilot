from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "scripts" / "validate_project_bundle.py"
EXAMPLE = REPO / "examples" / "synthetic-project"


class ProjectBundleValidationTests(unittest.TestCase):
    def run_validator(self, project: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(project), "--require-decision"],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_synthetic_example_passes(self) -> None:
        result = self.run_validator(EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_id_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            shutil.copytree(EXAMPLE, project)
            evidence_path = project / "evidence-bundle.json"
            data = json.loads(evidence_path.read_text(encoding="utf-8"))
            data["project_id"] = "wrong-project"
            evidence_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            result = self.run_validator(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("project_id mismatch", result.stdout)

    def test_inconsistent_valuation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            shutil.copytree(EXAMPLE, project)
            decision_path = project / "decision-record.json"
            data = json.loads(decision_path.read_text(encoding="utf-8"))
            data["terms"]["post_money"] = 120.0
            decision_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            result = self.run_validator(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("post_money", result.stdout)

    def test_inconsistent_return_math_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            shutil.copytree(EXAMPLE, project)
            decision_path = project / "decision-record.json"
            data = json.loads(decision_path.read_text(encoding="utf-8"))
            data["return_scenarios"][1]["irr_pct"] = 40.0
            decision_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            result = self.run_validator(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("inconsistent with MOIC", result.stdout)


if __name__ == "__main__":
    unittest.main()
