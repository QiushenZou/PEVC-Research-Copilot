#!/usr/bin/env python3
"""Repository entry point for the router's project-bundle validator."""

from pathlib import Path
import runpy

runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "skills" / "pevc-research-router" / "scripts" / "validate_project_bundle.py"),
    run_name="__main__",
)
