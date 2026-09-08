#!/usr/bin/env python3
"""Install the local package without dependencies or network access."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile

# --check and --dry-run must not create an import cache in the source package.
sys.dont_write_bytecode = True

from validate import ALIAS_NAME, MAIN_NAME, REPO_ROOT, ValidationError, tree_snapshot, validate_package


def real_directory_or_missing(path: Path) -> None:
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise ValidationError(f"Expected a real directory or missing path: {path}")


def install(destination: Path, *, with_alias: bool, dry_run: bool, check: bool, update: bool) -> int:
    validate_package(REPO_ROOT, require_alias=with_alias)
    destination = Path(os.path.abspath(destination.expanduser()))
    real_directory_or_missing(destination)
    sources = [REPO_ROOT / "skills" / MAIN_NAME]
    if with_alias:
        sources.append(REPO_ROOT / "skills" / ALIAS_NAME)

    # Preflight every selected target before writing anything.
    package_root = REPO_ROOT.resolve()
    plans = []
    conflicts = []
    for source in sources:
        target = destination / source.name
        resolved_target = target.resolve()
        if (resolved_target.is_relative_to(package_root / "skills")
                or package_root.is_relative_to(resolved_target)):
            raise ValidationError(f"Installation target overlaps package source: {target}")
        real_directory_or_missing(target)
        expected = tree_snapshot(source)
        current = tree_snapshot(target) if target.exists() else None
        action = "unchanged" if current == expected else "update" if current is not None else "install"
        plans.append((source, target, expected, current, action))
        if action == "update" and not update and not check:
            conflicts.append(target)

    if check:
        for _, target, _, _, action in plans:
            print(f"{'OK' if action == 'unchanged' else 'DIFFERS' if action == 'update' else 'MISSING'}: {target}")
        return int(any(action != "unchanged" for *_, action in plans))
    if conflicts:
        raise ValidationError("Existing skills differ; use --update to back them up and replace: "
                              + ", ".join(str(path) for path in conflicts))

    changed = [plan for plan in plans if plan[-1] != "unchanged"]
    backup_root = destination.parent / f".{destination.name}-backups"
    if any(plan[-1] == "update" for plan in changed):
        real_directory_or_missing(backup_root)
    if dry_run or not changed:
        for _, target, _, _, action in plans:
            print(f"{'Would ' if dry_run and action != 'unchanged' else ''}{action}: {target}")
            if action == "update":
                print(f"  Would preserve exact previous tree under: {backup_root}")
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    backup_run = None
    applied = []
    with tempfile.TemporaryDirectory(prefix=".i2e-install-", dir=destination) as staging_name:
        staging = Path(staging_name)
        for source, _, expected, _, _ in changed:
            staged = staging / source.name
            shutil.copytree(source, staged, symlinks=True)
            if tree_snapshot(staged) != expected:
                raise ValidationError(f"Source changed while staging; retry: {source}")
        try:
            for _, target, _, current, action in changed:
                real_directory_or_missing(target)
                if (tree_snapshot(target) if target.exists() else None) != current:
                    raise ValidationError(f"Target changed during installation; retry: {target}")
                backup = None
                if action == "update":
                    if backup_run is None:
                        backup_root.mkdir(parents=True, exist_ok=True)
                        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
                        backup_run = Path(tempfile.mkdtemp(prefix=stamp, dir=backup_root))
                    backup = backup_run / target.name
                    target.rename(backup)
                applied.append((target, backup))
                (staging / target.name).rename(target)
        except (OSError, ValidationError):
            for target, backup in reversed(applied):
                if target.exists():
                    shutil.rmtree(target)
                if backup is not None:
                    backup.rename(target)
            raise

    for _, target, _, _, action in plans:
        print(f"{action}: {target}")
    for target, backup in applied:
        if backup is not None:
            print(f"Backup of {target.name}: {backup}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_dest = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    parser.add_argument("--dest", type=Path, default=default_dest, help="Skill directory (default: $CODEX_HOME/skills or ~/.codex/skills)")
    parser.add_argument("--with-legacy-alias", action="store_true", help=f"Also install the optional {ALIAS_NAME} entry point")
    parser.add_argument("--update", action="store_true", help="Back up and replace differing installed bundles")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Validate and show actions without writing")
    mode.add_argument("--check", action="store_true", help="Read-only content check; exit 1 if missing or different")
    args = parser.parse_args()
    if args.check and args.update:
        parser.error("--check cannot be combined with --update")
    try:
        return install(args.dest, with_alias=args.with_legacy_alias, dry_run=args.dry_run,
                       check=args.check, update=args.update)
    except (ValidationError, OSError, UnicodeError) as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
