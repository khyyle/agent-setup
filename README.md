# Personal agent setup

Edit your shared rules in [rules](rules/) and personal skills in [skills](skills/). Codex, Cursor and Pi resolve the installed entries back to this checkout. The initial Git commit captures the original imports. The repository is local to this machine.

## Everyday use

Open a project in Cursor or VS Code and work as usual. In the IDE terminal, run `pi` for the OpenAI-backed agent, or run `herdr` and start `pi` inside a Herdr pane when you want persistent terminals. Pi starts with the same OpenAI model selected in the local Codex config at setup time. Use `/model` inside Pi to select another available OpenAI model.

- Ask for **proof of the fix**, or invoke `$verify-change` in Codex or `/skill:verify-change` in Pi. Choose a check that exercises the changed behavior. For UI work, inspect a screenshot or trace from a real interaction.
- For a fresh local reading of work in progress, run `codex review --uncommitted`. For a requirement-specific review, start `codex -s read-only` in a second terminal and give it the original request, working-tree scope and evidence. The review rubric lives in [ponytail-review](skills/ponytail-review/SKILL.md).
- Use `gh-axi` for GitHub, `playwright-axi` for browser interactions, `chrome-devtools-axi` for Chrome inspection, `lavish-axi` for local HTML review, `quota-axi` for provider quota, and `toon` to encode or decode TOON. Run a command with `--help` for its installed syntax.
- Use `exa-axi search "query" --limit 3` or `exa-axi read https://example.com` for public web sources. This locally maintained wrapper uses Exa's hosted MCP endpoint. Its public service limits apply.
- The `axi` skill is the design guide for building another wrapper. Each installed tool has its own usage skill. The upstream skill named `lavish` drives the `lavish-axi` executable.

- For independent chats, run `pi --name implement` and `pi --name investigate` in separate IDE terminals, or in two Herdr tabs. `pi -r` reopens the session picker. Use separate Git worktrees if both chats will edit independently.
- Use [ARIS](skills/aris/SKILL.md) for claim-driven planning or a study-local research wiki. Use [unslop](skills/unslop/SKILL.md) for an explicitly requested prose edit. [no-mistakes](skills/no-mistakes/SKILL.md) is an explicitly invoked Git gate with its own CLI and repository enrollment.

## Rules and original examples

The shared default lives in [rules/AGENTS.md](rules/AGENTS.md). Codex and Pi link to it as `AGENTS.md`. Cursor's `~/.cursor/rules/agent-defaults.mdc` points to the same file. The [original personal rules](rules/personal/) retain the detailed [Python examples](rules/personal/python-code-quality.mdc) and [general coding examples](rules/personal/general-code-quality.mdc). The [project rule copies](rules/imported/) retain their original contents for comparison, including their project-specific settings. The global installer reads only the shared default when exposing a Cursor rule.

Use the testing guidance in the shared default for everyday changes. The [ECC TDD workflow](skills/tdd-workflow/SKILL.md) is the original import, including its examples and 80% coverage target. Invoke the full workflow for an explicit test-first assignment. [Coding standards](skills/coding-standards/SKILL.md) and [Python patterns](skills/python-patterns/SKILL.md) are the original ECC imports as well.

## Maintain the collection

Edit an existing skill in place. For a new one, add `skills/<name>/SKILL.md` with a matching name and a task-specific description. Run `python3 scripts/link.py` for new paths and `python3 scripts/link.py --check` to verify discovery paths and the configured Pi defaults. Reopen a client session to refresh its skill list. Pi and Codex use the shared `~/.agents/skills` directory. Cursor also has links under `~/.cursor/skills`. The original four Codex paths still resolve.

Locally authored for this setup: `verify-change`, `exa-axi` and its CLI. `research-loop` was developed in an earlier session and imported. `ponytail`, `ponytail-review` and `context7-mcp` have local edits. The ARIS skill adapts the two previously installed stages and ships the pinned upstream wiki helpers. The Django skill condenses the previously project-local Django patterns, security and test references. Upstream revisions for the tool skills are in [tools/skill-sources.tsv](tools/skill-sources.tsv).

The active collection includes [web-perf](skills/web-perf/SKILL.md) for browser performance audits and [search-first](skills/search-first/SKILL.md) for checking existing solutions before adding code or dependencies. The other 13 Cloudflare-distributed skills (including the three Sandbox skills) and seven GitNexus skills are available in the earlier local commit `eb1cebd`. To reactivate one globally, run `git restore --source=eb1cebd -- skills/<name>` with its real name, then run the linker. App-managed plugin skills live outside this collection.

## Install on Apple Silicon macOS

Requires Node 24 or later, npm, Python 3.9 or later, Git and curl. Add `~/.local/bin` to the shell's PATH. The upstream GitHub wrapper also needs an authenticated `gh` for GitHub operations.

```sh
./scripts/install-tools.sh
python3 scripts/link.py
python3 scripts/link.py --check
pi auth login openai
pi auth check --provider openai --no-refresh
```

The tool installer restores pinned dependencies from [tools/package-lock.json](tools/package-lock.json), verifies the Herdr and no-mistakes release checksums, and installs the matching Chromium with cache cleanup disabled. Pi stores its credentials outside this repo. Select the ChatGPT sign-in option to use eligible plan usage. Browser and review session hooks are optional.

The linker refuses to overwrite an existing unmanaged path by default. For a migration of existing personal rules and skills, `python3 scripts/link.py --adopt` retains the old entries under `~/.local/state/agent-setup/backups/<timestamp>/` at their original relative paths before linking. It preserves unrelated Pi settings and refuses conflicting executables. To restore a migrated file, inspect its backup and replace only its managed symlink with that saved file or directory.

To update tool versions, change the exact dependency in [tools/package.json](tools/package.json), refresh its lockfile, and retest the CLI and its matching skill. The imported authoring and wrapper skill revisions are in [tools/skill-sources.tsv](tools/skill-sources.tsv). Their instructions prefer the locally pinned executables. The original Cloudflare source manifest is available with `git show eb1cebd:skills-sources.json`.
