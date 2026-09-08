"""Exercise the actual CLI against disposable packages and destinations."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
MAIN_NAME = "i2e-astra-terra"
ALIAS_NAME = "i2e-hybrid"


class PackageToolsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "package"
        self.dest = self.base / "codex" / "skills"
        shutil.copytree(SCRIPTS, self.repo / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        self.main = self.repo / "skills" / MAIN_NAME
        self.write(self.main / "SKILL.md", """---
name: i2e-astra-terra
description: Coordinate issue implementation with explicit model roles.
---
# Workflow

Follow the [role instructions](references/roles.md) and [task form](templates/task.md).
""")
        self.write(self.main / "agents" / "openai.yaml", """interface:
  display_name: "I2E Astra / Terra"
  short_description: "Coordinate issue implementation with model roles"
  default_prompt: "Use $i2e-astra-terra to complete the requested work."
""")
        self.write(self.main / "references" / "roles.md", "# Roles\n\nCoordinate work using the approved role contract.\n")
        self.write(self.main / "templates" / "task.md", "# Task\n\nRecord the concrete goal and acceptance evidence.\n")
        self.alias = self.repo / "skills" / ALIAS_NAME
        self.write(self.alias / "SKILL.md", """---
name: i2e-hybrid
description: Invoke the canonical Astra and Terra issue workflow.
---
Follow [the canonical workflow](../i2e-astra-terra/SKILL.md).
""")
        self.environment = dict(os.environ, CODEX_HOME=str(self.base / "default-codex"))
        self.environment.pop("PYTHONDONTWRITEBYTECODE", None)

    @staticmethod
    def write(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def cli(self, script: str, *args: str, success: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run([sys.executable, str(self.repo / "scripts" / script), *args],
                                cwd=self.base, env=self.environment, text=True, capture_output=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def install(self, *args: str, success: bool = True) -> subprocess.CompletedProcess[str]:
        return self.cli("install.py", "--dest", str(self.dest), *args, success=success)

    @staticmethod
    def snapshot(root: Path) -> dict[str, tuple[bytes | None, int, int]]:
        """Capture bytes and mtimes, including directories, to detect writes."""
        return {str(path.relative_to(root)): (path.read_bytes() if path.is_file() else None,
                                             path.stat().st_mtime_ns, path.stat().st_mode)
                for path in root.rglob("*")}

    def test_valid_package_and_cwd_independent_install(self) -> None:
        self.cli("validate.py")
        self.install()
        self.assertEqual((self.dest / MAIN_NAME / "SKILL.md").read_bytes(),
                         (self.main / "SKILL.md").read_bytes())
        self.assertFalse((self.dest / ALIAS_NAME).exists())
        self.assertEqual(sorted(path.name for path in self.dest.iterdir()), [MAIN_NAME])

    def test_default_destination_respects_codex_home(self) -> None:
        self.cli("install.py")
        self.assertTrue((self.base / "default-codex" / "skills" / MAIN_NAME / "SKILL.md").is_file())
        self.assertFalse(self.dest.exists())

    def test_alias_opt_in_and_links_survive_install(self) -> None:
        self.install("--with-legacy-alias")
        alias_link = self.dest / ALIAS_NAME / ".." / MAIN_NAME / "SKILL.md"
        self.assertTrue(alias_link.resolve().is_file())
        self.install("--with-legacy-alias", "--check")

    def test_identical_install_is_noop(self) -> None:
        self.install()
        before = self.snapshot(self.base)
        result = self.install()
        self.assertIn("unchanged:", result.stdout)
        self.assertEqual(before, self.snapshot(self.base))

    def test_conflict_does_not_overwrite_or_install_alias(self) -> None:
        target = self.dest / MAIN_NAME / "private.txt"
        self.write(target, "Preserve this installed skill.\n")
        before = self.snapshot(self.base)
        result = self.install("--with-legacy-alias", success=False)
        self.assertIn("--update", result.stderr)
        self.assertEqual(before, self.snapshot(self.base))

    def test_update_backs_up_exact_tree_and_preserves_unrelated_skill(self) -> None:
        self.install("--with-legacy-alias")
        self.write(self.dest / MAIN_NAME / "private.txt", "Original local customization.\n")
        self.write(self.dest / ALIAS_NAME / "extra.txt", "Original alias customization.\n")
        unrelated = self.dest / "unrelated" / "SKILL.md"
        self.write(unrelated, "Unrelated skill.\n")
        previous_main = self.snapshot(self.dest / MAIN_NAME)
        previous_alias = self.snapshot(self.dest / ALIAS_NAME)
        previous_unrelated = self.snapshot(unrelated.parent)
        result = self.install("--update", "--with-legacy-alias")
        backup_root = self.dest.parent / ".skills-backups"
        backups = list(backup_root.iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(previous_main, self.snapshot(backups[0] / MAIN_NAME))
        self.assertEqual(previous_alias, self.snapshot(backups[0] / ALIAS_NAME))
        self.assertEqual(previous_unrelated, self.snapshot(unrelated.parent))
        self.assertIn(str(backups[0] / MAIN_NAME), result.stdout)
        self.assertFalse((self.dest / MAIN_NAME / "private.txt").exists())
        self.install("--check", "--with-legacy-alias")

    def test_failed_second_replacement_restores_both_previous_bundles(self) -> None:
        self.install("--with-legacy-alias")
        self.write(self.dest / MAIN_NAME / "private.txt", "Original main.\n")
        self.write(self.dest / ALIAS_NAME / "private.txt", "Original alias.\n")
        before_main = self.snapshot(self.dest / MAIN_NAME)
        before_alias = self.snapshot(self.dest / ALIAS_NAME)
        # Simulate a filesystem failure after the first replacement succeeded.
        runner = f"""
import runpy
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, {str(self.repo / 'scripts')!r})
original_rename = Path.rename
def fail_alias(source, target):
    if source.parent.name.startswith('.i2e-install-') and source.name == {ALIAS_NAME!r}:
        raise OSError('Simulated second replacement failure')
    return original_rename(source, target)
with patch.object(Path, 'rename', fail_alias):
    runpy.run_path({str(self.repo / 'scripts' / 'install.py')!r}, run_name='__main__')
"""
        result = subprocess.run([sys.executable, "-c", runner, "--dest", str(self.dest),
                                 "--update", "--with-legacy-alias"], cwd=self.base,
                                env=self.environment, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Simulated second replacement failure", result.stderr)
        self.assertEqual(before_main, self.snapshot(self.dest / MAIN_NAME))
        self.assertEqual(before_alias, self.snapshot(self.dest / ALIAS_NAME))
        self.assertEqual(sorted(path.name for path in self.dest.iterdir()), [MAIN_NAME, ALIAS_NAME])

    def test_dry_run_never_creates_destination(self) -> None:
        before = self.snapshot(self.base)
        result = self.install("--dry-run", "--with-legacy-alias")
        self.assertIn("Would install:", result.stdout)
        self.assertEqual(before, self.snapshot(self.base))

    def test_update_dry_run_never_creates_backups_or_changes_target(self) -> None:
        self.write(self.dest / MAIN_NAME / "local.txt", "Keep me.\n")
        before = self.snapshot(self.base)
        result = self.install("--update", "--dry-run")
        self.assertIn("Would update:", result.stdout)
        self.assertIn("Would preserve exact previous tree", result.stdout)
        self.assertEqual(before, self.snapshot(self.base))

    def test_check_missing_is_read_only(self) -> None:
        before = self.snapshot(self.base)
        result = self.install("--check", success=False)
        self.assertIn("MISSING:", result.stdout)
        self.assertEqual(before, self.snapshot(self.base))

    def test_check_identical_and_different_are_read_only(self) -> None:
        self.install()
        before = self.snapshot(self.base)
        self.install("--check")
        self.assertEqual(before, self.snapshot(self.base))
        self.write(self.dest / MAIN_NAME / "templates" / "task.md", "Local change.\n")
        before = self.snapshot(self.base)
        result = self.install("--check", success=False)
        self.assertIn("DIFFERS:", result.stdout)
        self.assertEqual(before, self.snapshot(self.base))

    def test_symlink_source_entry_is_rejected(self) -> None:
        external = self.base / "external.txt"
        self.write(external, "External content.\n")
        (self.main / "references" / "external.md").symlink_to(external)
        self.install(success=False)
        self.assertFalse(self.dest.exists())

    def test_symlink_source_directory_is_rejected(self) -> None:
        original = self.repo / "original-main"
        self.main.rename(original)
        self.main.symlink_to(original, target_is_directory=True)
        self.install(success=False)
        self.assertFalse(self.dest.exists())

    def test_symlink_target_and_nested_entry_are_rejected(self) -> None:
        outside = self.base / "outside"
        self.write(outside / "keep.txt", "Original.\n")
        self.dest.mkdir(parents=True)
        (self.dest / MAIN_NAME).symlink_to(outside, target_is_directory=True)
        self.install("--update", success=False)
        self.assertEqual((outside / "keep.txt").read_text(), "Original.\n")
        (self.dest / MAIN_NAME).unlink()
        (self.dest / MAIN_NAME).mkdir()
        (self.dest / MAIN_NAME / "linked.txt").symlink_to(outside / "keep.txt")
        self.install("--update", success=False)
        self.assertTrue((self.dest / MAIN_NAME / "linked.txt").is_symlink())

    def test_symlink_destination_is_rejected(self) -> None:
        outside = self.base / "outside"
        outside.mkdir()
        self.dest.parent.mkdir()
        self.dest.symlink_to(outside, target_is_directory=True)
        self.install(success=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_invalid_source_does_not_touch_existing_install(self) -> None:
        self.install()
        (self.main / "agents" / "openai.yaml").unlink()
        before = self.snapshot(self.base)
        self.install("--update", success=False)
        self.assertEqual(before, self.snapshot(self.base))

    def test_missing_source_directory_is_rejected(self) -> None:
        self.main.rename(self.repo / "hidden-main")
        self.install(success=False)
        self.assertFalse(self.dest.exists())

    def test_missing_alias_only_required_when_requested(self) -> None:
        self.alias.rename(self.repo / "hidden-alias")
        self.install()
        self.install("--with-legacy-alias", success=False)
        self.assertFalse((self.dest / ALIAS_NAME).exists())

    def test_main_links_cannot_escape_bundle(self) -> None:
        self.write(self.repo / "README.md", "Outside bundle.\n")
        self.write(self.main / "references" / "roles.md", "[Outside](../../../README.md)\n")
        result = self.cli("validate.py", success=False)
        self.assertIn("escapes the bundle", result.stderr)

    def test_broken_relative_link_is_rejected(self) -> None:
        self.write(self.main / "references" / "roles.md", "[Missing](missing.md)\n")
        self.cli("validate.py", success=False)

    def test_absolute_and_file_links_are_rejected(self) -> None:
        for target in (str(self.main / "SKILL.md"), (self.main / "SKILL.md").as_uri()):
            with self.subTest(target=target):
                self.write(self.main / "references" / "roles.md", f"[Machine path]({target})\n")
                self.cli("validate.py", success=False)

    def test_reference_style_links_and_encoded_paths_are_checked(self) -> None:
        self.write(self.main / "references" / "extra notes.md", "Useful notes.\n")
        self.write(self.main / "references" / "roles.md", "[Notes][notes]\n\n[notes]: extra%20notes.md\n")
        self.cli("validate.py")
        self.write(self.main / "references" / "roles.md", "[Bad][bad]\n\n[bad]: %2e%2e/%2e%2e/elsewhere.md\n")
        self.cli("validate.py", success=False)

    def test_frontmatter_and_prompt_are_required(self) -> None:
        self.write(self.main / "agents" / "openai.yaml", "interface:\n  display_name: Package\n  short_description: Useful workflow\n  default_prompt: Placeholder text\n")
        self.cli("validate.py", success=False)
        self.write(self.main / "SKILL.md", "# No frontmatter\n")
        self.cli("validate.py", success=False)

    def test_block_strings_are_supported(self) -> None:
        self.write(self.main / "agents" / "openai.yaml", """interface:
  display_name: 'I2E Astra / Terra'
  short_description: >-
    Coordinate issue implementation
    with explicit model roles.
  default_prompt: |-
    Use $i2e-astra-terra to complete this work.
""")
        self.cli("validate.py")

    def test_scaffolds_and_unsupported_argument_are_rejected(self) -> None:
        for content in ("TODO: fill this in.\n", "spawn_agent(fork_context=True)\n"):
            with self.subTest(content=content):
                self.write(self.main / "references" / "roles.md", content)
                self.cli("validate.py", success=False)

    def test_source_cannot_be_installation_target(self) -> None:
        before = self.snapshot(self.base)
        self.cli("install.py", "--dest", str(self.repo / "skills"), "--update", success=False)
        self.assertEqual(before, self.snapshot(self.base))

    def test_checkout_and_ancestor_cannot_be_installation_targets(self) -> None:
        for nested_checkout in (False, True):
            with self.subTest(nested_checkout=nested_checkout):
                destination = self.base / ("ancestor-case" if nested_checkout else "checkout-case")
                target = destination / MAIN_NAME
                checkout = target / "checkout" if nested_checkout else target
                shutil.copytree(self.repo, checkout)
                self.write(checkout / ".git" / "HEAD", "ref: refs/heads/main\n")
                self.write(destination / "sibling-data" / "keep.txt", "Preserve sibling data.\n")
                if nested_checkout:
                    self.write(target / "other-project" / "keep.txt", "Preserve adjacent project.\n")
                before = self.snapshot(self.base)
                result = subprocess.run(
                    [sys.executable, str(checkout / "scripts" / "install.py"),
                     "--dest", str(destination), "--update"],
                    cwd=self.base, env=self.environment, text=True, capture_output=True)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("overlaps package source", result.stderr)
                self.assertEqual(before, self.snapshot(self.base))
                self.assertTrue((checkout / "scripts" / "install.py").is_file())
                self.assertTrue((checkout / "skills" / MAIN_NAME / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
