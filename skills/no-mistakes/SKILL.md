---
name: no-mistakes
description: Run or resume the no-mistakes gate when the user asks to put a feature branch through pre-push validation or to ship it through the repository's configured gate.
---

If the request includes implementation and gated delivery, read the [upstream workflow](references/upstream.md) at the start so you can carry the original requirements into review. Verify the change locally, commit the task on a feature branch, then start the gate against that committed work. For an already committed branch, go directly to the upstream validation workflow.

A request to verify, review or commit a change by itself stays local. The full gate can rebase, modify code, push, open a PR and monitor CI. Start a publishing run only when its destination and publication steps are within the requested scope.

Check the repository, branch, configured pipeline agent and state. This setup uses OpenAI via Codex. When setting up a repository at the user's request, use `no-mistakes init --skip-user-skill` to preserve the centrally maintained skill. An installation of the CLI alone does not enroll a repository. Use `no-mistakes doctor` to diagnose missing configuration.

Follow the pinned upstream instructions for intent, findings, gates and reattachment. Pass the user's requirements through stdin or a file. For a publishing run, review the intended public text as well as the code. A reviewer already inside an active gate handles its assigned phase and returns to the outer executor.
