A collection of skills, coding rules, and terminal workflows for coding agents. Use the skills and rules independently, or install the macOS workspace to run Pi and Codex in tmux.

## What you get

- **Skills for recurring tasks.** Pick a procedure for work such as test-first development, browser checks, or code review. The catalog records upstream revisions for imported skills. [Skills](skills/) · [Source pins](skills/sources.tsv)
- **Coding rules with worked examples.** See how to document an invariant, decide where to extract a helper, and test the behavior a caller can observe. The rules include Python conventions. [Rules](rules/)
- **A workspace you can reopen.** Each Git worktree gets a tmux session with Pi, Codex, and a Git shell. The installer includes browser tools for running and inspecting checks.

Inspired by [Mitchell Hashimoto on repeatable checks](https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness), [Matt Pocock's engineering skills](https://github.com/mattpocock/skills), and [Kun Chen's AXI conventions](https://github.com/kunchenguid/axi).

## Installation

Clone the repository and run the install commands below from its root.

```sh
git clone https://github.com/khyyle/agent-setup.git
cd agent-setup
```

### Use the skills and rules

The copy installer requires Python 3.9 or newer on macOS or Linux. Pick skills by name and install the rules separately if you want them.

```sh
python3 scripts/install-config.py --skills ponytail ponytail-review
python3 scripts/install-config.py --rules
```

To install a skill for one project, pass its path. For example, add `search-first` to a project where you regularly evaluate dependencies.

```sh
python3 scripts/install-config.py --project /path/to/project --skills search-first
```

Use `--all-skills` for the suggested user collection. It skips the entries in `skills/project-only.txt`, which are intended for named installs in individual projects. A repeat install keeps existing copies. Add `--refresh` to replace selected copies with the checkout version and save a backup. Run `python3 scripts/install-config.py --help` for custom destinations.

You can also install individual skills from this checkout using the standard skills CLI. [Vercel skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add)

```sh
npx skills add . --copy --global --agent codex --skill ponytail
```

### Set up the macOS workspace

#### Prerequisites

- An Apple Silicon Mac.
- Node.js 24 or newer with npm, and Python 3.9 or newer.
- Git, curl, and tmux 3.5 or newer.
- The Codex CLI. [Install Codex](https://developers.openai.com/codex/cli/)

#### Install the tools

```sh
./scripts/install-tools.sh
python3 scripts/link.py
export PATH="$HOME/.local/bin:$PATH"
```

The tool installer downloads the pinned Pi and browser tools, including Chromium for Playwright. The linker makes the commands available in `~/.local/bin`. Add that directory to your shell configuration to keep it on your PATH in new terminals.

## Usage

Sign in to Pi and Codex on first use.

```sh
pi auth login openai
codex login
```

```text
agent-tmux [directory] [--detach] [--encore | --no-music-tab]
```

Run `agent-tmux` from a fresh terminal to open or reattach the workspace for the current directory. Pass a directory to open another project. Use `--detach` to prepare the session without attaching.

| Tab | Use |
| --- | --- |
| `pi` | Pi session. |
| `review` | Codex session with read-only shell access. |
| `git` | Shell that opens at the worktree root and shows Git status. |

Use the `+` menu to open another agent or shell. Press `Ctrl-b d` to detach. Run `agent-tmux` from the project again to return to the same session.

## Optional tools

### Pi extensions

Run the extras script after installing the tools. It installs the Pi extensions below into your user profile. Have Homebrew available if the script needs to install Chafa or FFmpeg.

```sh
./scripts/install-extras.sh
```

Restart Pi or run `/reload`.

| What you want | Where to start |
| --- | --- |
| Dictate a prompt locally | Open `/voice-settings` and select a speech model. Then press `Ctrl+Space` to dictate. macOS may ask for microphone access. |
| Delegate a task | Open `/agents` to see the available subagents. |
| Preview a screenshot | Ask Pi to show the image by path. Use `/images status` to check the terminal renderer. |
| Save a conversation as Markdown | Run `/md`. |
| Choose when skills are available | Open `/skills-toggle`. Manual-only mode updates the installed skill copy. |

### Apple Music in tmux

Run `./scripts/install-extras.sh --encore` to include Encore in the extras install. The workspace opens a `music` tab when Encore is installed. The tmux status bar can show the track playing in Music.app when macOS grants Automation access. Use `agent-tmux --no-music-tab` when you want to skip opening the player. [Encore](https://github.com/bogdankim/encore)
