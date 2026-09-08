# I2E Astra Terra

A self-contained Codex Issue-to-Edit workflow: **Astra Ultra** owns
decisions and review; **Terra xhigh** performs bounded implementation.

Built on engineering workflow practices from
[Addy Osmani's agent-skills](https://github.com/addyosmani/agent-skills).
Credit to Addy Osmani for the foundational engineering skillset; this repository
consolidates and adapts those practices into a standalone Issue-to-Edit workflow
with Astra/Terra routing. It is an independent adaptation, not an official upstream
release or endorsement.

This public repository includes the complete workflow, supporting references,
run-record template, installer, and tests. It does **not** require cloning the old
`issue-to-edit-workflow-skills` repository or installing its skill stack.

## Install

You need Git, Python 3.10+, and Codex with
subagent support and access to `gpt-6-astra` / `ultra` and `gpt-5.6-terra` / `xhigh`.
Model access and project-specific tools or credentials are not supplied by a skill.

```sh
git clone https://github.com/bowang-solutionstream/i2e-astra-terra.git
cd i2e-astra-terra
python3 scripts/install.py
python3 scripts/install.py --check
```

The repository can be cloned without a GitHub invitation or authenticated account.
If you prefer GitHub CLI, use `gh repo clone bowang-solutionstream/i2e-astra-terra`.

The installer copies the complete skill to `$CODEX_HOME/skills`, or
`~/.codex/skills` when `CODEX_HOME` is unset. It has no third-party Python dependency,
does not contact the network, and does not alter project `AGENTS.md` files or Codex
model configuration. Open a new Codex task after installation to load the skill.

To also repair/retain the old `$i2e-hybrid` command as an entry point to this workflow:

```sh
python3 scripts/install.py --with-legacy-alias --update
python3 scripts/install.py --with-legacy-alias --check
```

The optional alias depends only on the sibling `i2e-astra-terra` bundle installed by
the same command. The main skill is independently usable without the alias.
Neither command modifies `i2e-mode` or the separately named Sol/Luna preset.

## Use

```text
Use $i2e-astra-terra to implement issue #123 in this repository.
```

State the desired deliverable and any operational boundary, for example local
changes only or an authorized PR. The skill carries existing authorization forward
without treating a model's approval as release permission.

For substantial implementation, the runtime uses Astra Ultra as decision lead and
reviewer and Terra xhigh as implementer. An existing Astra Ultra coordinator is
reused; otherwise the coordinator creates one Astra lead. Tiny edits and
non-implementation requests can stay in the current agent when delegation adds no
material value. Actual routing must be reported; unavailable models are not silently
substituted. This is an instruction workflow, not a runtime setting switch.

The bundled guidance covers repository/issue intake, scope and acceptance criteria,
issue splitting, architecture and implementation, relevant engineering surfaces,
proportional verification, final-diff review and repairs, and authorized handoff or
shipping. Required failed or missing proof means incomplete. Two unsuccessful
repair rounds trigger Astra reassessment/takeover, not permission to abandon the
requested outcome.

Repository-specific rules and native checks still apply. Specialized tools and
skills can be used when available and relevant; none of the former I2E workflow
skills are dependencies of this package.

### Working on a teammate's issue

Issue creators and assignees do not hold an exclusive I2E work lock. A teammate
with the required repository permissions can take over authorized work on the
same issue without the original person's approval or prior reassignment. This also
applies to older issues containing owner-only I2E process notes. Inspect current
progress and coordinate actual conflicting writes; preserve repository protections,
required reviews, and the user's action boundary. Taking over does not automatically
change the assignee, rewrite old issues, or authorize deployment.

## Update or inspect

```sh
git pull --ff-only
python3 scripts/install.py --update
python3 scripts/install.py --check
```

Keep `--with-legacy-alias` on update/check commands if you installed the alias.
Identical installs are no-ops. Different existing bundles are refused unless
`--update` is given. Every replaced bundle is preserved under a timestamped run in
the destination's sibling `.skills-backups` directory (for a destination named
`skills`), outside skill discovery; the installer prints the exact backup path.
Restore by moving the unwanted installed bundle aside and copying its preserved
backup to the original location. Other installed skills are left untouched.

Use `--dest /path/to/skills` for an alternate installation. Add `--dry-run` to
preview without writes; previewing replacement also needs `--update`. `--check` is
read-only and returns nonzero if a selected bundle is absent or differs.

## Maintain and validate

Edit the source under `skills/`, not an installed copy.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
git diff --check
```

The validation script checks package structure, metadata, and bundled links. Tests
exercise installation, updates, backups, conflicts, and failure behavior. These
checks do not establish model quality or cost savings; see
[validation evidence](docs/validation.md) for the scope of behavioral testing.

An optional [GitHub Actions template](docs/github-actions-validate.yml) runs the
same checks. Copy it to `.github/workflows/validate.yml` when enabling CI with an
account/token authorized to edit workflow files. CI is not enabled by this package's
initial publication; the install and local checks do not require it.

## Credits and license notices

- [Addy Osmani's agent-skills](https://github.com/addyosmani/agent-skills) provides
  the foundational engineering practices adapted here, including planning,
  incremental implementation, testing, source-driven development, and review.
  The original [MIT license and copyright notice](skills/i2e-astra-terra/notices/ADDY_AGENT_SKILLS_LICENSE)
  are retained with the installed skill.
- [Pattern, Inc.'s code-mint](https://github.com/patterninc/code-mint) contributed
  the issue-refinement guidance adapted from `interface-ticket-writer`.
  Its [Apache 2.0 license](skills/i2e-astra-terra/notices/CODE_MINT_LICENSE) is retained.

See [the main skill](skills/i2e-astra-terra/SKILL.md) for workflow instructions and
[provenance and upstream notices](skills/i2e-astra-terra/NOTICE.md) for the source
revisions and adaptation details. No repository-wide license is declared for the
original orchestration and tooling; this visibility change does not relicense them.
Upstream material retains its respective license terms.
