#!/usr/bin/env python3
"""Render validated industry-chain JSON into a standalone interactive HTML map."""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
VALIDATOR = HERE / "validate_industry_data.py"
TEMPLATE = SKILL_ROOT / "assets" / "map-template.html"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    result = subprocess.run([sys.executable, str(VALIDATOR), str(args.input)])
    if result.returncode:
        return result.returncode
    data = json.loads(args.input.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    rendered = template.replace("__MAP_TITLE__", html.escape(str(data["title"]))).replace("__MAP_DATA__", payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
