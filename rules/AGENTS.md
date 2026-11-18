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
- Name values for the distinctions a reader needs. A name can distinguish requested from committed state, standard deviation from variance, or bytes from samples. Use verbs for operations and predicates for yes/no questions. Familiar mathematical symbols are useful near the formula that defines them. Use the language's types, primitives and idioms to make valid states and operations clear.
- Keep the main path readable in execution order. Make the conditions for stopping, falling back or committing a change visible beside their consequences. Use guard clauses, pattern matching, a pipeline or an ordinary loop where it makes that path easier to follow.
- Extract a helper for a coherent operation with a clear contract. A private helper can earn its place with one caller when its name lets the reader follow the larger operation. Keep steps together when they share evolving state and the reader must jump between functions to reconstruct their order. Keep helpers private to their owner until a real cross-module contract justifies sharing them.
- Validate at trust boundaries. Catch errors where the caller can recover or add actionable context. Log once where the failure is handled. For writes that can fail partway or repeat, preserve consistency across retries and concurrent callers.
- Orient readers at module boundaries. Use the language's native module docstring or file comment when purpose, scope or assumptions need an introduction. Above a section, explain what that phase accomplishes and why it sits there. Beside a surprising operation, explain the offset, unit conversion or invariant that makes it correct. A block comment can take the space needed for a derivation, example or tradeoff, including inside a private function. Omit narration that merely translates the next line and keep edit history in Git.
- In UI work, reuse the project's components and tokens. Handle the loading, empty, error and keyboard interaction states relevant to the change. For unattended scripts, scope file operations and staging explicitly, preserve failure exit codes and keep credentials out of output.

For worked examples of naming, comments and helper boundaries, see `~/projects/agent-setup/rules/code-quality.md`.

## Python

Type function signatures and use NumPy-style docstrings for nontrivial interfaces. When writing Python, see `~/projects/agent-setup/rules/python.md` for conventions and a worked example.

## Verify the behavior

Start with what the user or caller should observe. Use focused unit tests for calculations, boundary values and error cases that can fail independently. Use a real integration for a storage or service contract. Exercise a critical journey end to end when the failure could be in how its parts connect. Choose the fastest check that can catch that failure. Add another test when it catches a distinct regression. Skip assertions that merely repeat an existing check or pin private helper calls.

For example, if a saved preference disappears on reload, change it through the UI, reload, and assert the displayed value. One browser journey covers the save request, storage and reload together when it uses the real local backend. Test a preference's complex validation cases through the validator's public interface. Use repeatable fixtures and independent expected values. When a critical journey repeatedly needs manual setup, give the project one command that sets up its fixture and runs it. Respect project test gates. Use the full `tdd-workflow` when the user or project asks for test-first development.

For a user-visible fix, exercise the changed path and inspect the outcome. Report the exact check and what it showed. Use `verify-change` for reproducible evidence, `ponytail-review` for a requested local code review and `research-loop` for empirical studies.
