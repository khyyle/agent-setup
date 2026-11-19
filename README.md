A collection of skills, coding rules, and terminal workflows for coding agents. Use the skills and rules independently. On macOS, the terminal presets keep Pi and Codex sessions available alongside your editor.

## What you get

- **Skills for recurring tasks.** Pick a procedure for work such as test-first development, browser checks, or code review. The catalog records upstream revisions for imported skills. [Skills](skills/) · [Source pins](skills/sources.tsv)
- **Coding rules with worked examples.** See how to document an invariant, decide where to extract a helper, and test the behavior a caller can observe. The rules include Python conventions. [Rules](rules/)

Inspired by [Mitchell Hashimoto on repeatable checks](https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness), [Matt Pocock's engineering skills](https://github.com/mattpocock/skills), and [Kun Chen's AXI conventions](https://github.com/kunchenguid/axi).

## Installation

Clone the repository and run the install commands below from its root.

```sh
git clone https://github.com/khyyle/agent-setup.git
cd agent-setup
```

### Use the skills and rules

On macOS or Linux with Python 3.9 or newer, you can copy selected skills into your user profile. The second command installs the shared coding rules. You can run either on its own.

```sh
python3 scripts/install-config.py --skills ponytail ponytail-review
python3 scripts/install-config.py --rules
```

For project installs, custom destinations, and updating installed copies, see the [skills and rules installation guide](skills/README.md).

### Set up the macOS workspace

Choose one preset to run in your IDE terminal or terminal app. Both open Pi, a read-only Codex review session, and a Git shell, with an optional Apple Music player.

- **Herdr** gives you a shared workspace for those tabs and a sidebar for project chats and worktrees. Use it to see which agent needs attention while you work in another checkout.
- **tmux** keeps a session per checkout. Run `agent-tmux` from a project to open its tabs or return to the session you left there.

The presets target Apple Silicon Macs. The [terminal setup guide](terminal/README.md) covers prerequisites, installation, and starting either workspace.
