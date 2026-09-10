#!/usr/bin/env python3
"""Install or link every PE/VC skill in this repository into Codex."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills")
    parser.add_argument("--link", action="store_true", help="Create symlinks for development instead of copying")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    source_root = repo / "skills"
    skills = sorted(path for path in source_root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())
    args.target.mkdir(parents=True, exist_ok=True)

    for source in skills:
        destination = args.target / source.name
        action = "link" if args.link else "copy"
        print(f"{action}: {source.name} -> {destination}")
        if args.dry_run:
            continue
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        elif destination.exists():
            shutil.rmtree(destination)
        if args.link:
            destination.symlink_to(source, target_is_directory=True)
        else:
            shutil.copytree(source, destination)
    print(f"Installed {len(skills)} skills. Refresh Codex skill discovery to use them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
