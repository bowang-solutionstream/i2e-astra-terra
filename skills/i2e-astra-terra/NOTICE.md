# Provenance and upstream notices

## Primary upstream credit: Addy Osmani

Credit to Addy Osmani's [agent-skills](https://github.com/addyosmani/agent-skills)
for the foundational engineering skillset behind this workflow's adapted planning,
incremental implementation, testing, source-driven development, and review guidance.
This package consolidates those practices with the locally authored Issue-to-Edit
orchestration and Astra/Terra routing. It is an independent adaptation, not an
official release of the upstream skillset or a claim of upstream endorsement.

## Package provenance and retained licenses

This standalone package was assembled on 2026-09-08 from the locally authored
Issue-to-Edit workflow and hybrid-routing requirements. The prior package was
`h3ro-dev/issue-to-edit-workflow-skills`. That repository is provenance, not an
installation or runtime dependency.

The standalone instructions consolidate and rewrite the former multi-skill
workflow. Changes include Astra Ultra / Terra xhigh routing, a shared authority and
acceptance contract, proportional proof, final-state review, and repair escalation.
No credentials, client artifacts, or project-specific deployment configuration are
included.

The engineering and issue-writing guidance draws on practices packaged previously
from the following sources. Attribution and license copies are retained with the
installed skill. Upstream source files are not installed as separate skills.

- Addy Osmani, [agent-skills](https://github.com/addyosmani/agent-skills), source
  revision `70b7506ce90e200cb47645ddb3f6b8e84fecc047`.
  Copyright (c) 2025 Addy Osmani. [MIT license](notices/ADDY_AGENT_SKILLS_LICENSE).
- Pattern, Inc., [code-mint](https://github.com/patterninc/code-mint), source
  revision `ee3817c78f85b98701db618337837801cdfc8da6`; former
  `interface-ticket-writer` guidance. Copyright 2025-2026 Pattern, Inc.
  [Apache 2.0 license](notices/CODE_MINT_LICENSE).

The original locally authored wrapper names were `i2e-mode`, `issue-workflow-gate`,
`writeissue-guidance`, and `project-coding-guidance`. The new package does not load
them or the legacy hybrid delivery skill. This notice does not imply endorsement
by the upstream authors or change their license terms.
