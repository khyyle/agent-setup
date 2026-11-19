# Terminal presets

Both presets open a Pi chat, a read-only Codex session (`review`), and a Git shell. Herdr keeps these starter tabs in a shared workspace and groups project chats by checkout. The tmux launcher gives each checkout its own set of tabs. Either runs in an IDE terminal or a standalone terminal app.

## Install the tools

Use an Apple Silicon Mac with Node.js 24 or newer, npm, Python 3.9 or newer, Git, curl, and the [Codex CLI](https://developers.openai.com/codex/cli/). For the tmux preset, also install tmux 3.5 or newer.

Run these commands from the repository root. The installer downloads the pinned tools, including Pi, Herdr, and Chromium. The second command links executables from this checkout into `~/.local/bin`, so keep the checkout where you installed it.

```sh
./scripts/install-tools.sh
python3 scripts/link.py
export PATH="$HOME/.local/bin:$PATH"
```

Add the PATH line to your shell configuration for future terminals. For first-time sign-in with OpenAI, run `pi auth login openai` and `codex login`.

## Herdr

Register the preset once, then use `herdr` to open or reattach to the workspace.

```sh
./scripts/install-herdr.sh
herdr
```

The preset creates a shared workspace named **main**. Its starter tabs open in your home directory, including the shell labeled `git`. Open a project in its own workspace when you want chats and shells to start in that checkout. For another chat there, open a tab and run `pi`. The sidebar shows agent status across workspaces.

The preset binds `Ctrl-b`, then `a` to return to **main** and restore missing starter tabs. On a fresh profile the installer applies the binding and tab bar automatically. If you already have a Herdr user profile, the installer prints its config path so you can merge the settings you want. [Preset settings](herdr/ui.toml)

## tmux

Run `agent-tmux` inside a checkout, or pass its path from another directory.

```sh
agent-tmux /path/to/project
```

Run it again from anywhere in the same checkout to reattach. A linked worktree gets its own session. Click **+** in the tab bar to add a Pi chat, a Codex chat, or a shell. The launcher uses a dedicated tmux server, so the preset's tab bar and bindings apply only to sessions it manages. [tmux preset](tmux/tmux.conf)

## Optional project setup for Herdr worktrees

If a project needs dependencies installed in each new checkout, add `.herdr/config.toml` to its main checkout. Set `script` under `[setup]` to the project's setup command and commit the file. When Herdr creates a worktree for that project, the hook runs the command once in the new checkout. [Worktree setup example](https://github.com/toyamarinyon/herdr-worktree-setup#configure)

## Optional Pi extensions

Run `./scripts/install-extras.sh` from the repository root, then restart Pi or run `/reload`. The installer uses Homebrew for missing media utilities. In Pi, use `/skills-toggle` to control which installed skills the model can invoke, `/voice-settings` for dictation, `/agents` for subagents, `/images status` to check screenshot support, and `/md` to export a chat.

## Apple Music

Run `./scripts/install-extras.sh --encore` from the repository root to install the Apple Music player alongside the Pi extensions. Reopen **main** in Herdr or rerun `agent-tmux` to add the `music` tab. Both preset tab bars can show the current track while Music.app is playing, including when the player tab is closed. macOS may request Automation access to read the track. [Encore](https://github.com/bogdankim/encore)
