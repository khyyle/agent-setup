# Personal agent setup

Edit your shared rules in [rules](rules/) and personal skills in [skills](skills/). Codex, Cursor and Pi resolve the installed entries back to this checkout. The initial Git commit captures the original imports. The repository is local to this machine.

## Everyday use

Open a project in Cursor or VS Code and work as usual. In the IDE terminal, run `pi` for the OpenAI-backed agent, or run `herdr` and start `pi` inside a Herdr pane when you want persistent terminals. Pi starts with the same OpenAI model selected in the local Codex config at setup time. Use `/model` inside Pi to select another available OpenAI model.

- Ask for **proof of the fix**, or invoke `$verify-change` in Codex or `/skill:verify-change` in Pi. Choose a check that exercises the changed behavior. For UI work, inspect a screenshot or trace from a real interaction.
- For a fresh local reading of work in progress, run `codex review --uncommitted`. The verification skill also describes how to give a new read-only session the original request and relevant evidence.
- Use `gh-axi` for GitHub, `playwright-axi` for browser interactions, `chrome-devtools-axi` for Chrome inspection, `lavish-axi` for local HTML review, `quota-axi` for provider quota, and `toon` to encode or decode TOON. Run a command with `--help` for its installed syntax.
- Use `exa-axi search "query" --limit 3` or `exa-axi read https://example.com` for public web sources. This locally maintained wrapper uses Exa's hosted MCP endpoint. Its public service limits apply.
- The `axi` skill is the design guide for building another wrapper. Each installed tool has its own usage skill. The upstream skill named `lavish` drives the `lavish-axi` executable.

## Maintain the collection

Edit an existing skill in place. For a new one, add `skills/<name>/SKILL.md` with a matching name and a task-specific description. Run `python3 scripts/link.py` for new paths and `python3 scripts/link.py --check` to verify discovery paths and the configured Pi defaults. Reopen a client session to refresh its skill list. Pi and Codex use the shared `~/.agents/skills` directory. Cursor also has links under `~/.cursor/skills`. The original four Codex paths still resolve.

The personal behavioral guide is [rules/AGENTS.md](rules/AGENTS.md). Python conventions live in [rules/python-code-quality.mdc](rules/python-code-quality.mdc). The [scoped](scoped/) directory links directly to the project-owned Nexa and video-annotation guidance, including the classifier's ARIS installation. Edit a scoped file in its owning repository. Host-supplied plugin skills, application-managed sync directories, execution permissions and credentials remain managed by their respective applications.

## Install on Apple Silicon macOS

Requires Node 24 or later, npm, Python 3.9 or later, Git and curl. Add `~/.local/bin` to the shell's PATH. The upstream GitHub wrapper also needs an authenticated `gh` for GitHub operations.

```sh
./scripts/install-tools.sh
python3 scripts/link.py
python3 scripts/link.py --check
pi auth login openai
pi auth check --provider openai --no-refresh
```

The tool installer restores pinned dependencies from [tools/package-lock.json](tools/package-lock.json), verifies the Herdr release checksum, and installs the matching Chromium with cache cleanup disabled. Pi stores its credentials outside this repo. Select the ChatGPT sign-in option to use eligible plan usage. Browser and review session hooks are optional.

The linker refuses to overwrite an existing unmanaged path by default. For a migration of existing personal rules and skills, `python3 scripts/link.py --adopt` retains the old entries under `~/.local/state/agent-setup/backups/<timestamp>/` at their original relative paths before linking. It preserves unrelated Pi settings and refuses conflicting executables. To restore a migrated file, inspect its backup and replace only its managed symlink with that saved file or directory.

To update tool versions, change the exact dependency in [tools/package.json](tools/package.json), refresh its lockfile, and retest the CLI and its matching skill. The imported authoring and wrapper skill revisions are in [tools/skill-sources.tsv](tools/skill-sources.tsv). Their instructions prefer the locally pinned executables. The earlier Cloudflare installation provenance is in [skills-sources.json](skills-sources.json).
