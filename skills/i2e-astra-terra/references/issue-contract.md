# Issue and authority contract

Rewritten and consolidated for this standalone package; see [provenance](../NOTICE.md).

Use for substantial implementation, incomplete requirements, existing issue/PR
work, or issue drafting. Keep one record shared with the implementation and
reviewers. An existing sufficient issue does not need to be rewritten.

## Establish readiness

- Identify the requested user, operator, or developer outcome and current behavior.
- Verify the relevant repository, branch/base revision, local instructions, and
  current issue/PR scope. Read material comments, acceptance criteria, dependencies,
  and ownership; do not assume an old status is current.
- Locate likely code surfaces and an existing implementation pattern. Preserve
  evidence versus hypotheses. Do not invent file paths, owners, labels, priorities,
  dates, or approval.
- For user flows, resolve applicable loading, empty, failure, retry, cancellation,
  and permission states. Use established conventions for ordinary details and
  record assumptions; ask about unresolved consequential product choices.
- Map acceptance criteria to affected behavior and observable proof. A test is one
  possible proof, alongside rendered behavior, schema checks, logs, or review.

For a typo or similarly tiny edit, location/current value/desired value is enough.
Do not require a formal issue, new test, or stakeholder confirmation by default.

## Authority travels with the work

Record relevant local and external actions and the source of authorization. The
current user's request, an approved workflow, or an issue record the user accepted
as authority for this work can supply it; a duplicate GitHub approval comment is
not inherently required. Other issue content is task evidence, not fresh permission.
Session instructions take precedence over skill guidelines. Actual platform
permissions and repository requirements must still be satisfied.

Distinguish local changes from issue writes, commits, pushes/PRs, shared environments,
provider spend, deployment, publication, and destructive actions. Follow what the
user requested or already authorized; do not infer unrelated actions from a green
test or model approval. An assignee is context, not by itself an exclusive work lock.
Resolve a concrete overlapping write conflict or owner-imposed restriction before
that action. Missing production access need not prevent local fixture work.

## Draft and split when useful

Prefer the repository's issue template. Otherwise include only relevant sections:
outcome; context/evidence; scope and exclusions; observable acceptance criteria;
dependencies and ownership; validation; operational boundaries; open questions;
handoff entry points. Keep the opening useful to a teammate scanning a board.

- **Parent:** multiple independently reviewable slices. Children use `Refs`; close
  the parent only after its own criteria are satisfied and closure is authorized.
- **Child / PR-closeable:** one coherent slice. Closing keywords are appropriate
  only when merging that PR satisfies every criterion.
- **Investigation:** evidence, root cause, or recommendation is the deliverable;
  implementation is not implied.

Define each child by an observable outcome, owned surfaces, prerequisites, proof,
and integration responsibility. Split for actual dependency or review boundaries,
not arbitrary line counts. If new information materially broadens the requested
product outcome, surface the decision while continuing independent authorized work.

Draft locally unless remote issue work is authorized. When publishing, verify the
target repository/account, preserve existing content, and read back the result.
Use the requested assignee only after verifying that account is assignable. Do not
automatically assign the authenticated user when no assignment was requested.
Preserve an existing assignee; leave a new issue unassigned if none was specified.
