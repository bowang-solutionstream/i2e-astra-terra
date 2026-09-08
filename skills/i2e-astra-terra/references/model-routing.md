# Astra Ultra / Terra xhigh routing

## Runtime and roles

Use runtime-provided model and effort identifiers. This profile requests
`gpt-6-astra` with `ultra`, and `gpt-5.6-terra` with `xhigh`. Codex's Ultra label is
not an instruction to invent an API parameter. If the runtime cannot run the
requested pairing, explain the limitation; continue useful non-model-dependent
work and obtain a user-selected fallback before representing another profile as
the requested hybrid. A skill does not provide model access, subscriptions, or quota.

If the root is already Astra Ultra, it is the decision lead. Otherwise, create one
Astra Ultra lead with a focused contract/discovery task and reuse it for ordinary
review. The root relays tools and integrates work without duplicating the lead's
planning. Current-agent direct work remains appropriate for tiny tasks and
non-implementation requests; report that exception honestly.

Astra owns the contract, architecture, cross-module invariants, material scope
changes, and final judgment. Terra implements stable, bounded work, writes relevant
tests, and repairs local failures. For an uncertain migration, concurrency defect,
tenant boundary, or other consequential invariant, Astra investigates and can
implement the critical part; delegate only the separable settled portion.

## Delegation packet

Give each worker the objective, exact base/worktree, owned files or module, relevant
pattern, invariants and exclusions, acceptance-to-proof map, allowed commands and
actions, and unresolved questions. Include direct source pointers so it can inspect
necessary dependencies; an evidence capsule is not a ban on useful investigation.
Tell workers they share the codebase and must preserve others' changes. Do not fork
the whole conversation just to populate a task packet.

For a runtime exposing `collaboration.spawn_agent`, the relevant fields are:

```json
{
  "task_name": "implement_slice",
  "agent_type": "worker",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "xhigh",
  "fork_turns": "none",
  "message": "The task-specific contract, owned paths, evidence, and verification."
}
```

For a separate decision lead or fresh critical reviewer, select `gpt-6-astra`,
`ultra`, and a fresh bounded context. Follow the actual tool schema if different.
Use task subagents rather than creating user-visible tasks unless the user asks for
a new task. The root owns worker spawning, integration, and relay. Workers request
additional help through the root so overlapping work and repeated investigation
remain visible. Do not spend a slot on duplicate verification of unchanged inputs.

## Review and repair

Terra returns changed files, decisions, acceptance/proof mapping, commands and
outcomes, unresolved concerns, and usage metadata when available. Astra reads the
actual production diff and important test assertions, including omitted behavior.
For ordinary review, reuse the lead promptly. For consequential changes, use an
independent Astra reviewer with the requirements, raw diff, and evidence; avoid
feeding it the author's approval conclusion as its task.

Consolidate material findings into one repair packet and return ordinary fixes to
the same Terra worker. After two unsuccessful rounds, or earlier evidence of a
misunderstood invariant, Astra diagnoses the cause, corrects the contract, and
takes over or reassigns a smaller settled slice. Do not create an endless relay or
use the repair count as a completion condition. Parallel workers must have disjoint
write ownership; shared-contract changes happen before dependent implementation.

## Cost accounting

Optimize cost per accepted result. Record actual model/effort, input/cached/output
usage, reasoning usage if exposed, elapsed time, repair count, and proof quality.
Include root coordination, workers, reviews, retries, and evaluation in comparisons.
Do not count cached input twice, or add reasoning output twice when the provider
already includes it in output. State missing usage as unavailable. Estimated rate
card credits are not observed account charges or quota savings; date the rate card.
Matching an earlier Sol/Luna benchmark does not prove Astra/Terra quality or savings.
