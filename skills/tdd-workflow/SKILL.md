---
name: tdd-workflow
description: Implement a requested feature or regression fix test-first through one observable behavior at a time.
---

Choose the interface that can expose the defect. Write a check for one behavior, observe it fail for the expected reason, change the implementation, and rerun the check. Then take the next behavior or refactor with the checks passing.

Use unit cases for pure rules and boundary values, integration tests for contracts across components or storage, and E2E tests for critical user journeys. Prefer real local collaborators where practical and mock an external boundary explicitly. Test outcomes that should survive a refactor. Follow the repository's own coverage requirements. When an existing check already proves the changed behavior, reuse it.

Use the verify-change skill for browser evidence, interaction traces or a repeatable hands-on reproduction.
