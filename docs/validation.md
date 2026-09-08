# Validation evidence

## Package validation — 2026-09-08

- `python3 scripts/validate.py`: both bundles pass structure, metadata, and local
  link checks. The main skill's links remain inside its own bundle.
- `python3 -m unittest discover -s tests -v`: 27 tests pass, including install,
  exact backup preservation, two-bundle rollback, source/target overlap rejection,
  symlink rejection, unrelated-skill preservation, and read-only check/dry-run.
- Codex skill-creator `quick_validate.py`: main skill and compatibility alias pass.
- A main-only installation into an empty temporary skill directory passes content
  comparison and installed-bundle validation without any legacy skills present.
- The global main skill and repaired alias pass installed/source content checks;
  the previous alias is preserved in a recoverable backup outside skill discovery.
- CI configuration is supplied as an optional template, not an active workflow;
  local validation results are not presented as GitHub CI results.

An independent package review found a source/target overlap defect in the initial
installer. A regression reproduced the unsafe update, then verified rejection
before writes with the checkout and adjacent data unchanged. The issue was repaired
before global installation or publication. The independent reviewer confirmed the
final repair and reported no remaining material defect in that repair.

## Independent workflow smoke test — 2026-09-08

A fresh Astra Ultra coordinator received only this skill, its bundled references,
and a synthetic local Python catalog with a request for paginated library and CLI
access. It dispatched one actual fresh-context Terra xhigh implementation worker,
then inspected the resulting production code and test assertions.

- The existing single baseline test passed. Final verification passed 16 library
  and subprocess CLI tests using the standard library only.
- Proof covers filtering before paging, stable ordering, page metadata, boundaries,
  input/dictionary preservation, defaults, CLI success, and invalid input failures.
- One consolidated repair round fixed a reproduced nonstandard JSON output edge,
  added missing proof of the default 20-item page, and placed temporary test data
  inside the authorized workspace. The first run's outside-workspace temporary
  fixtures had been removed; this scope deviation was corrected before completion.
- Astra approved the actual final files after repair. There were no network,
  dependency-installation, GitHub, commit, push, or deployment actions in the test.
- The fixture had no Git repository, so source hashes and test receipts supplied
  revision evidence. The pre-dispatch-to-final-readback interval was about seven
  minutes; complete provider usage and agent timing were unavailable.

This proves one completed local workflow execution with the requested pairing.
It does not test every workflow mode, the two-failed-round takeover path, live
shipping, or comparative model quality/cost. Synthetic fixture code and private
agent logs are not part of the installed skill.

## Behavior and limits

Structural checks do not prove that models will make correct decisions. Live
workflow smoke-test evidence is recorded above separately from installer tests.
No comparison against Sol/Luna, account-charge measurement, or cost-saving claim is
established by this package validation.

The generic workflow retains project-specific requirements. This package does not
provide browser access, credentials, GitHub permissions, model availability, or
production environment access. Live shipping and high-risk migration behavior
require evidence in the actual target project.
