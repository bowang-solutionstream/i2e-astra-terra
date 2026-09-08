# Engineering guidance by surface

Rewritten and consolidated for this standalone package; see [provenance](../NOTICE.md).

Use the relevant entries while implementing. These are complete workflow defaults;
specialist skills are optional when available and useful, not package dependencies.
Project-specific contracts, commands, and genuine operational restrictions prevail.

**Repository and source.** Inspect applicable ancestor and scoped guidance plus the
worktree before edits. Use focused searches and existing conventions. For unfamiliar
APIs or dependencies, verify the needed behavior against current primary
documentation. Separate an observed fact from an assumption. Preserve unrelated
changes, secrets, and client evidence outside the patch.

**Specification and planning.** Define the intended behavior before choosing an
abstraction. Prefer existing code. Split dependent work into coherent outcomes with
clear interfaces and one integration owner. Investigate the riskiest unresolved
assumption early. Use an ADR only for a lasting architectural choice that needs it.

**Implementation and simplification.** Implement a working slice, check its changed
behavior, and continue. Size slices by coherence and risk rather than file count.
Do not introduce flags, wrappers, new dependencies, or layers without a current
need. Remove obsolete code caused by an authorized refactor when references prove
it is within scope; distinguish that from deleting unrelated or uncertain assets.
Commit only within the authorized handoff, not automatically after every slice.

**Bugs and testing.** Reproduce the failure and identify its cause before guessing
a patch. Add a failing regression test when practical and useful; a runtime repro
or other direct evidence may be more appropriate. Assert outcomes and meaningful
boundaries. Do not write tests that merely repeat the implementation. Use fakes or
fixtures for external effects and shared/table-driven cases when they remain clear.

**API, schema, migration.** Identify callers and compatibility obligations. Use
explicit types and validate boundary inputs. Coordinate changes across contracts,
implementation, fixtures, and docs. For persisted state, examine versioning, retry,
idempotency, interrupted execution, rollback/restore, and data preservation as
applicable. Follow the project's migration policy; do not require down-migrations
when the actual system uses forward fixes or restore procedures.

**UI and browser.** Treat approved design and typed data as the contract. Preserve
loading, empty, error, keyboard, and responsive behavior where relevant. For a
visual defect, capture a measurable baseline and recheck the same dimensions after
the smallest fix. Exercise the actual user interaction; screenshots support rather
than replace runtime evidence. Use the available browser tools and test accounts;
do not invent rendered values or claim authenticated proof from static tests.

**Access and providers.** Check authorization at the actual resource/tenant boundary
and test relevant negative paths. Keep credentials out of prompts, logs, and Git.
For providers, identify the approved account/environment, spend/side-effect limits,
timeouts, retry behavior, and cleanup requirements. Use approved fixtures when live
access is unnecessary or unavailable. Project collection rules still apply.

**Performance and observability.** Measure the observed bottleneck before changing
architecture. Check relevant query counts, memory, latency, bundle/runtime costs,
or concurrency. Add useful signals for new critical paths without logging sensitive
data. Instrument enough to detect the actual failure mode, not every function.

**CI and release.** Use repository-native checks and record revision-specific
results. A successful build is not evidence of deployment. Verify authorized
release steps against the actual environment and observe the deployed revision,
health, and rollback conditions using the handoff reference.
