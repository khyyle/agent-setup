# Personal agent setup

Use Pi to make changes and Codex to review them. Run both in a tmux session for the current Git worktree, from your editor's terminal or a standalone terminal.

## Why this workflow

A separate review session gives the reviewer the original request and the diff without the implementation conversation. Pass along the command you ran and what it showed. For example, if a fix should make a preference survive a reload, save the preference, reload the page, and check its value. The reviewer can repeat that check and look for cases it misses.

## Principles and sources

- Keep everyday conventions in one set of shared rules. Put project-specific setup and test commands in the project. Turn repeated manual checks into commands an agent can run. [Mitchell Hashimoto on repeatable checks](https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness)
- Write skills for tasks with a distinct procedure. Keep imported instructions at a recorded revision and document local changes. [Matt Pocock's engineering skills](https://github.com/mattpocock/skills) · [Source pins](tools/skill-sources.tsv)
- Give command-line tools their own usage help. Prefer structured output when an agent needs to read a result. [Kun Chen's AXI](https://github.com/kunchenguid/axi)

## What you get

- `agent-tmux` opens Pi, a Codex review tab with a read-only shell, and a Git shell. Run it again to return to the same worktree session. The `+` menu opens another chat or shell.
- Pi, Codex, and Cursor use the same rules and skills. The linker installs them for your user account and can add selected skills to one project. [Rules](rules/) · [Skills](skills/)
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

Add `$HOME/.local/bin` to your shell's `PATH`. The linker sets Pi's default provider to OpenAI. Run `pi auth login openai` and `codex login` to sign in, then run `agent-tmux` from a project.

The linker stops at an existing personal rule or skill it does not manage. Use `python3 scripts/link.py --adopt` if you want it to back up those entries and replace them with links.

### Optional setup

- For Apple Music, install Encore with `brew install bogdankim/tap/encore`, then run `agent-tmux --encore`. [Encore](https://github.com/bogdankim/encore)
- To keep a skill off the global list, add its name to `skills/project-only.txt` and rerun `python3 scripts/link.py`. To enable it in one project, run `python3 scripts/link.py --project /path/to/project skill-name`. The command preserves existing project skills. [Project-only list](skills/project-only.txt)

Install the Pi skill toggle with the revision below. It scans the shared user skills directory.

```sh
pi install git:github.com/Whamp/pi-skill-toggle@bfb4ff810e49cf42c43ea818c5676a2e74398f3f
```

Restart Pi and open `/skills-toggle`. The manual-only setting edits `SKILL.md`. With this setup's symlinks, that edits the file in the checkout. [Pi Skill Toggle](https://github.com/Whamp/pi-skill-toggle)
