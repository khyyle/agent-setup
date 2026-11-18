---
name: no-mistakes
description: Drive Kun Chen's no-mistakes Git validation gate when the user explicitly requests that pipeline.
disable-model-invocation: true
---

Use this skill for an explicitly requested no-mistakes run. For ordinary working-tree review use `ponytail-review`. The full gate works on a committed feature branch and can rebase, modify code, push, open a PR and monitor CI. Confirm that the requested scope covers the configured destination and publication before starting a publishing run.

Check the repository, branch, configured pipeline agent and state. This setup uses OpenAI via Codex. When setting up a repository at the user's request, use `no-mistakes init --skip-user-skill` to preserve the centrally maintained skill. An installation of the CLI alone does not enroll a repository. Use `no-mistakes doctor` to diagnose missing configuration.

Follow the pinned [upstream operating instructions](references/upstream.md) for intent, review findings, gates and reattachment. Pass the user's requirements through stdin or a file. For a publishing run, review the intended public text as well as the code. A reviewer already inside an active gate handles its assigned phase and returns to the outer executor.
