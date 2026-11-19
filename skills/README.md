# Installing skills and rules

Each skill has its own directory and `SKILL.md`. The installer copies the directories you select, so edits to an installed skill stay local to that installation. Run the examples from the repository root with Python 3.9 or newer on macOS or Linux.

## Choose where a skill applies

For skills you use across projects, install by name. This puts each skill under `~/.agents/skills/`.

```sh
python3 scripts/install-config.py --skills ponytail ponytail-review
```

To share a skill with one project, give the installer the project's path. This example creates `.agents/skills/search-first/` inside the project.

```sh
python3 scripts/install-config.py --project /path/to/project --skills search-first
```

Use `--all-skills` to install the suggested user collection. It skips the [project-only list](project-only.txt), whose entries you can still install by name. For a client with a different skills directory, pass `--skills-dir DIR` with your selection.

## Install coding rules

```sh
python3 scripts/install-config.py --rules
```

This copies the [shared conventions](../rules/AGENTS.md) to `~/.codex/AGENTS.md`, `~/.pi/agent/AGENTS.md`, and `~/.cursor/rules/agent-defaults.mdc`. To install the rules at a single path, use `--rules-file FILE`. Either option also installs the worked examples under `~/.local/share/agent-setup/rules/`.

## Verify or update an installation

Repeating an install keeps existing copies, including local edits. Add `--check` to your original selection to verify the copies are present. To update them from this checkout, add `--refresh`. The installer backs up each copy it replaces and prints the backup location.

## Use the skills CLI

You can also copy a skill from this checkout with the [Vercel skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add). For example, to install Ponytail for your Codex user profile, run the following command from the repository root.

```sh
npx skills add . --copy --global --agent codex --skill ponytail
```
