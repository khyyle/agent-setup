# Personal agent setup

Use Pi to make changes and Codex to review them. Run both in a tmux session for the current Git worktree, from your editor's terminal or a standalone terminal.

## Why this workflow

A separate review session gives the reviewer the original request and the diff without the implementation conversation. Pass along the command you ran and what it showed. For example, if a fix should make a preference survive a reload, save the preference, reload the page, and check its value. The reviewer can repeat that check and look for cases it misses.

## Principles and sources

- Keep everyday conventions in one set of shared rules. Put project-specific setup and test commands in the project. Turn repeated manual checks into commands an agent can run. [Mitchell Hashimoto on repeatable checks](https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness)
- Write skills for tasks with a distinct procedure. Keep imported instructions at a recorded revision and document local changes. [Matt Pocock's engineering skills](https://github.com/mattpocock/skills) · [Source pins](skills/sources.tsv)
- Give command-line tools their own usage help. Prefer structured output when an agent needs to read a result. [Kun Chen's AXI](https://github.com/kunchenguid/axi)

## What you get

- `agent-tmux` opens Pi, a Codex review tab with a read-only shell, and a Git shell. Run it again to return to the same worktree session. The `+` menu opens another chat or shell.
- A catalog of pinned skills and example rules. Install the ones you want to use. [Rules](rules/) · [Skills](skills/)
- The installer pins Pi and the browser tools used to reproduce web issues. It also installs Herdr for use in a separate terminal. [Tool lockfile](tools/package-lock.json)

## Install

The bundled tool installer targets Apple Silicon macOS. You need Node.js 24 or newer with npm, Python 3.9 or newer, Git, curl, tmux 3.5 or newer, and the Codex CLI. [Install Codex](https://developers.openai.com/codex/cli/)

```sh
git clone https://github.com/khyyle/agent-setup.git
cd agent-setup
./scripts/install-tools.sh
python3 scripts/link.py
python3 scripts/link.py --check
```

Add `$HOME/.local/bin` to your shell's `PATH`. Use `python3 scripts/link.py --bin-dir DIR` if you keep executables elsewhere. Run `pi auth login openai` and `codex login` to sign in, then run `agent-tmux` from a project.

### Install skills and rules

```sh
python3 scripts/install-config.py --skills ponytail ponytail-review
python3 scripts/install-config.py --rules
python3 scripts/install-config.py --project /path/to/project --skills search-first
```

Pi, Codex, and Cursor discover user skills from `~/.agents/skills` and project skills from `.agents/skills` in the project. The installer copies files to those directories. `--all-skills` copies the suggested user collection. [Project-only list](skills/project-only.txt)

For a custom profile, pass `--skills-dir DIR` with your skill selection or use `--rules-file FILE` to install the rule template at an exact path. Choose a location your client already reads. `--rules` copies the rules into the default Pi, Codex, and Cursor locations. Either rules option installs the worked examples under `~/.local/share/agent-setup/rules`.

A repeat install keeps existing copies. Use `--refresh` to replace selected copies from the checkout. The installer backs up anything it replaces.

The skills also work with standard catalog installers. To copy one from this checkout into a Codex user profile, run the command below from the repo root. [Vercel skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add)

```sh
npx skills add . --copy --global --agent codex --skill ponytail
```

### Optional setup

- Install Encore with `./scripts/install-extras.sh --encore` to add a `music` tab on launch. Use `agent-tmux --no-music-tab` to skip opening the tab. The status bar reads the playing track from Music.app when macOS grants Automation access. [Encore](https://github.com/bogdankim/encore)

Install pinned Pi extensions:

```sh
./scripts/install-extras.sh
```

Restart Pi or run `/reload`. Use `/voice-settings` to select a local transcription model, `/agents` to manage subagents, `/images status` to check screenshot support, and `/md` to export a conversation. Ask Pi to show a screenshot by path.

Use `/skills-toggle` to choose which skills Pi can load. The manual-only setting edits the installed `SKILL.md`. [Pi Skill Toggle](https://github.com/Whamp/pi-skill-toggle)
