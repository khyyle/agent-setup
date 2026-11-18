# Personal agent setup

Edit your shared rules in [rules](rules/) and personal skills in [skills](skills/). Codex, Cursor and Pi resolve the installed entries back to this checkout. The initial Git commit captures the original imports. The repository is local to this machine.

## Everyday use

Open a project in Cursor or VS Code. Use the editor for navigation, breakpoints and inspecting diffs. In its integrated terminal, run `agent-tmux` for the project workspace. Each Git worktree gets its own session. Running the command from a subdirectory reattaches to that worktree. Pi uses the configured OpenAI provider. Use `/model` in Pi to change the model.

| Tab | Use |
|---|---|
| `pi` | Implement one change. Click **+ → Pi chat** for a separate conversation. To name one from a shell, run `pi --name investigate`. Use `pi -r` to return to a saved chat. |
| `review` | A fresh Codex terminal starts with a read-only shell sandbox. Once the author pauses, give the reviewer the original requirement, target diff and evidence. Ask for a triggering input and observable consequence. Take confirmed findings back to the author. |
| `git` | Opens a shell with the worktree status. Use it for Git, tests or a development server. Outside a repository it opens a shell where you can change directory. The launcher restores a missing Git tab on reattach. Give two simultaneous writers separate Git worktrees. |

Click a tab or press **Ctrl-b**, then its number (`1`, `2`, `3`). The **+** beside the last tab opens a menu for a new Pi chat, a regular Codex chat or a shell. **Ctrl-b +** opens the same menu by keyboard. **Ctrl-b c** opens a shell directly and **Ctrl-b d** detaches. Run `agent-tmux` to return. The preset requires tmux 3.5+ and lives on the dedicated `agent-setup` socket. Its [configuration](terminal/tmux.conf) puts tabs across the top and enables modified keys for Pi.

**Three ways to review.** The `review` tab runs `codex -s read-only -a never` and waits for your brief. The built-in `codex review --uncommitted` command runs a one-shot review of working changes from the Git tab. The optional `no-mistakes` skill drives its own configured Git validation pipeline for committed feature branches. Its pinned Codex backend uses `codex exec` with pipeline-supplied prompts. The dedicated review tab starts independently of that gate. [Pinned no-mistakes backend](https://github.com/kunchenguid/no-mistakes/blob/5732d1ed88a1572fa6115d6ede5d69bfec097946/internal/agent/codex.go)

**Optional dictation.** The screenshot's Pi Transcribe extension is now Pi Voice. It transcribes locally and inserts the result in Pi's prompt. If dictating prompts is useful, the package is `@earendil-works/pi-voice`. Setup uses `/voice-settings` to select a local speech model and microphone. `/voice` starts and stops a recording. [Pi Voice](https://github.com/earendil-works/pi-voice)

**Apple Music on macOS.** Run `agent-tmux --music` to add a music tab to the current workspace and show the track and artist on the right. Open Music normally. Run `agent-music info`, `agent-music toggle`, `agent-music next` or `agent-music previous` in the tab. macOS may ask whether your terminal host can control Music. If the status is blank during playback, `agent-music info` shows the diagnostic. A closed Music app stays closed.

**When to use Herdr.** When several agents are running and you want to see which needs attention, open a fresh IDE terminal in the project and run `herdr --session project-name`. In Herdr, **Ctrl-b c** adds a tab, **Ctrl-b n/p** changes tabs, **Ctrl-b v** splits a pane and **Ctrl-b q** detaches. Launch Pi in one tab and your test runner or a reviewer in another. Reopen the same named Herdr session to return. Use a single multiplexer per terminal so its prefix keys go to the right host. [Herdr guide](https://herdr.dev/agent-guide.md)

The [workflow review](workflow-review.md) records the exercised skills, grades and known gaps.

- Ask for **proof of the fix**, or invoke `$verify-change` in Codex or `/skill:verify-change` in Pi. Choose a check that exercises the changed behavior. For UI work, inspect a screenshot or trace from a real interaction.
- For a fresh local reading of work in progress, run `codex review --uncommitted`. For a requirement-specific review, start `codex -s read-only` in a second terminal and give it the original request, working-tree scope and evidence. The review rubric lives in [ponytail-review](skills/ponytail-review/SKILL.md).
- Use `gh-axi` for GitHub, `playwright-axi` for browser interactions, `chrome-devtools-axi` for Chrome inspection, `lavish-axi` for local HTML review, `quota-axi` for provider quota, and `toon` to encode or decode TOON. Run a command with `--help` for its installed syntax.
- Use `exa-axi search "query" --limit 3` or `exa-axi read https://example.com` for public web sources. This locally maintained wrapper uses Exa's hosted MCP endpoint. Its public service limits apply.
- The `axi` skill is the design guide for building another wrapper. Each installed tool has its own usage skill. The upstream skill named `lavish` drives the `lavish-axi` executable.

- Use [ARIS](skills/aris/SKILL.md) for claim-driven planning or a study-local research wiki. Use [unslop](skills/unslop/SKILL.md) for an explicitly requested prose edit. [no-mistakes](skills/no-mistakes/SKILL.md) is an explicitly invoked Git gate with its own CLI and repository enrollment.

## Rules and examples

Edit [rules/AGENTS.md](rules/AGENTS.md) for everyday behavior, including naming, commenting, control flow, helper boundaries and testing. It points directly to the [cross-language examples](rules/code-quality.md) and [Python conventions](rules/python.md). Codex and Pi link to the shared file as `AGENTS.md`. Cursor's `~/.cursor/rules/agent-defaults.mdc` links to the same content.

Architecture, design tokens, release procedures and project-specific commands belong in the owning checkout. The original personal and project rule snapshots are available locally in Git at `208df5f`, for example with `git show 208df5f:rules/personal/general-code-quality.mdc`.

Use the testing guidance in the shared default for everyday changes. The [ECC TDD workflow](skills/tdd-workflow/SKILL.md) is the original import, including its examples and 80% coverage target. Invoke the full workflow for an explicit test-first assignment. The [coding standards skill](skills/coding-standards/SKILL.md) retains its ECC examples with local guidance on comments and extraction. [Python patterns](skills/python-patterns/SKILL.md) is the original ECC import.

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
