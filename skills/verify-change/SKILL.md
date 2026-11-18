---
name: verify-change
description: Verify a behavior change through its normal entry point and capture reproducible local evidence, especially for UI fixes or cross-component regressions.
---

Recover the expected behavior from the user's request. For a regression, demonstrate the failure on the original code when practical. Preserve unrelated working changes. Compare a separate checkout or a saved observation if switching revisions would disturb the user's work.

Use the smallest existing command that exercises the failure. For a layout change, inspect comparable screenshots with the same viewport, record, and state. For interactions, drive the real flow and assert the resulting state. For persistence, check a new read after writing. For numerical work, use a known case or a study-appropriate comparison. Name simulated boundaries. Reuse the project's fixture and local runner. When the same setup repeatedly needs manual intervention, put that setup behind one project command.

Keep evidence in the project's ignored artifact location or a local temporary directory. Use synthetic or redacted inputs. Inspect the artifact. Return the original claim, command and fixture, observed outcome, and local artifact path. Identify the tested revision or working changes and any important limitation.

For a requested fresh reading of the requirements and change, pass the evidence to `ponytail-review`.
