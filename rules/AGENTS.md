---
description: Personal development conventions
alwaysApply: true
---

# Personal development conventions

## Understand the change

Start with the observable behavior the user wants. Read the normal entry point, relevant callers and existing checks. When a dependency's behavior matters, check the installed version and its matching documentation. Ask about ambiguity when the answer changes a user-facing contract. Make reversible implementation decisions and verify them.

The user's request and explicit repository requirements govern the work. Reuse surrounding conventions when they support correctness and readability. If a nearby example conflicts with a written rule or has a concrete defect, use the sound pattern in the touched code. Explain the choice if it affects maintenance. Keep unrelated cleanup out of the change.

## Ownership and colocation

Keep a feature's implementation, fixtures, examples and explanation with its owner. Put a test beside the feature, or in its corresponding directory when the project mirrors source under a separate test tree. Cross-feature journeys belong in the integration or E2E suite. Keep study-specific controls and evidence with the study.

Start with a local definition. Extract shared logic when consumers implement the same rule and must change together. Similar-looking features can evolve independently. Give wire formats, stored values and policy decisions one authoritative owner even when they have a single caller. For example, the module that writes a persisted status owns its encoding. A compatibility test can use a literal from a previous release to detect accidental changes to that encoding.

## Code quality

- Choose the smallest readable implementation that covers supported inputs, callers and existing data. Follow a change through its public entry points. Remove code the change makes obsolete.
- Name values for their meaning. Use verbs for operations, predicates for yes/no questions and units when a number could be misread. Name thresholds and policy choices where readers need their meaning.
- Keep dependencies explicit, state close to its owner and module dependencies acyclic. Extract a function when it gives a decision or operation a useful name. Split modules when their responsibilities change independently.
- Validate at trust boundaries. Catch errors where the caller can recover or add actionable context. Log once where the failure is handled. For writes that can fail partway or repeat, preserve consistency across retries and concurrent callers.
- Comments explain invariants, units, decisions and external constraints a reader cannot infer. Document public contracts. Let version control hold edit history.
- In UI work, reuse the project's components and tokens. Handle the loading, empty, error and keyboard interaction states relevant to the change. For unattended scripts, scope file operations and staging explicitly, preserve failure exit codes and keep credentials out of output.

For the original naming and comment examples, see `~/projects/agent-setup/rules/personal/general-code-quality.mdc`.

## Python

Type function signatures using the project's supported Python version. Prefer built-in generics where supported and familiar domain terms over type-suffixed names. Use specific exceptions and the project logger for diagnostics. A command can write its result to stdout.

Use NumPy-style docstrings for nontrivial functions, methods and classes. Use underlined sections such as `Parameters`, `Returns` and `Raises` when they help the caller. Describe units, shapes, missingness, timezone assumptions and side effects where they matter. A self-explanatory private helper can rely on its name and signature.

Use the detailed Python conventions and worked docstring and error-handling examples in `~/projects/agent-setup/rules/personal/python-code-quality.mdc` when writing Python.

## Verify the behavior

Start with what the user or caller should observe. Use focused unit tests for calculations, boundary values and error cases that can fail independently. Use a real integration for a storage or service contract. Exercise a critical journey end to end when the failure could be in how its parts connect. Choose the fastest check that can catch that failure. Add another test when it catches a distinct regression. Skip assertions that merely repeat an existing check or pin private helper calls.

For example, if a saved preference disappears on reload, change it through the UI, reload, and assert the displayed value. One browser journey covers the save request, storage and reload together when it uses the real local backend. Test a preference's complex validation cases through the validator's public interface. Use repeatable fixtures and independent expected values. When a critical journey repeatedly needs manual setup, give the project one command that sets up its fixture and runs it. Respect project test gates. Use the full `tdd-workflow` when the user or project asks for test-first development.

For a user-visible fix, exercise the changed path and inspect the outcome. Report the exact check and what it showed. Use `verify-change` for reproducible evidence, `ponytail-review` for a requested local code review and `research-loop` for empirical studies.
