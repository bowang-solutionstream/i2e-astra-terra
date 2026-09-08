---
name: i2e-astra-terra
description: Run an Issue-to-Edit workstream with Astra Ultra decisions and review, and Terra xhigh implementation.
---

# I2E Astra Terra

Deliver the requested outcome with one continuing Issue-to-Edit contract. This
package contains the workflow, issue, engineering, verification, and handoff
guidance; no other workflow skill or issue-to-edit repository is required.
Repository-specific instructions and acceptance requirements still apply.

## Start with the requested outcome

Classify the request as learning, issue scoping, implementation, review, or shipping.
An implementation request authorizes the relevant local edits and verification;
do not turn it into a planning-only response. An audit or explanation stays read-only.
Use routine repository conventions to resolve ordinary details. Ask only for a
missing decision that materially changes the outcome or an action's authority.

Inspect the worktree and applicable repository guidance, then the relevant source,
issue, or PR. Read enough to establish the behavior and proof; do not tour every
document. Preserve unrelated changes. For substantial work, maintain one compact
record using [the run record](templates/run-record.md); reuse it across agents.
Tiny edits need only a clear outcome and proportionate evidence.

Carry forward applicable user authorization from this session and existing
workflow records. Invocation chooses the workflow; it does not grant unrelated
external actions. Do not seek the same permission again. Keep a material missing
approval confined to the affected action while completing independent authorized
work. See [issue and authority guidance](references/issue-contract.md) when
scoping, splitting, or working from an issue.

## Route work deliberately

For substantial implementation, use **gpt-6-astra / ultra** for the decision lead
and review, and **gpt-5.6-terra / xhigh** for bounded implementation. Verify actual
runtime support and use [model routing](references/model-routing.md) before
delegating. If the coordinator already is Astra Ultra, plan and review locally;
do not introduce another planner. Never silently substitute a model or report
routing that did not happen.

Keep tiny edits, explanation, scoping, and ordinary review in the current agent
when delegation offers no material benefit; disclose actual execution. Astra owns
unresolved architecture and consequential invariants, and can implement a critical
portion directly. Terra receives a cohesive write scope, the contract, relevant
evidence, and verification commands. Use parallel workers only for independent
write sets. The coordinator integrates and owns the final result.

## Implement, prove, and finish

Read [engineering guidance](references/engineering.md) when implementing and apply
the entries relevant to the touched surface. Use existing patterns and small reviewable changes. A
failed local test is evidence to diagnose and repair within scope, not an automatic
request for renewed permission. Follow [verification and review](references/verification.md)
to choose proof and review depth. Retain all required repository gates; repeated
checks need a changed input, new failure, or unresolved concern.

After two unsuccessful repair rounds, Astra reassesses the contract and takes over
or narrows the worker assignment. Escalation changes who solves the problem; it
does not declare the task finished or automatically end authorized work.

Complete only when the requested acceptance criteria and required proof are
satisfied and the appropriate reviewer approves the actual final state. Missing
required proof means incomplete, with the precise gap recorded. A model verdict
is judgment, not permission to release. Perform authorized issue/PR/ship actions
with readback under [handoff and shipping](references/handoff.md). Report the
outcome, evidence, actual routing, material repairs, and remaining limits without
empty checklist fields or invented cost savings.
