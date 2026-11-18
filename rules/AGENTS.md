# Personal development conventions

Use these defaults for coding in this checkout. The user's task and explicit repository requirements govern the change. Project-specific architecture, release policies, supported versions and test commands belong in the project.

- Start from the behavior the user wants. Read its normal entry point and the affected callers before editing. For a consequential ambiguity, surface the tradeoff. Make reversible implementation choices and verify them.
- Prefer the smallest readable change that completes the task for existing callers and persisted data. Reuse a nearby pattern when it satisfies the contract. When it violates a written convention or causes a concrete defect, use the sound pattern within the touched scope and explain the reason.
- Keep feature-specific code, fixtures and explanation with their owning feature. Follow a mirrored test tree where the repo uses one. Keep cross-feature journeys in integration or E2E suites. Promote shared logic when consumers genuinely share semantics or one owner must define a wire format, stored value or policy.
- Make invariants obvious through names and structure. Use domain names, explicit dependencies and specific errors. Comments explain a decision, invariant or surprising constraint. For detailed naming and Python style, read the applicable personal rules at `~/.cursor/rules/general-code-quality.mdc` and `~/.cursor/rules/python-code-quality.mdc`.
- Verify at the cheapest boundary that can actually expose the failure. Use a public function for a calculation, a real persistence boundary for a write, and a browser journey for UI wiring. Preserve independent expected values for external contracts. Respect existing project test gates.
- For user-visible fixes, exercise the actual behavior and inspect the result. The `verify-change` skill covers reproduction, visual evidence and local review. When finishing, give the exact check and result and link useful local artifacts. A chat request is sufficient input.
- Use the research-loop skill for empirical studies. Keep hypotheses, data versions, experiments and scientific verification with their study. Use humanizer for prose when appropriate.
