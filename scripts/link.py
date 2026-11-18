#!/usr/bin/env python3
"""Expose this repository to the local agent clients and verify the resulting paths."""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from collections.abc import Iterator

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
LEGACY_CODEX = {"humanizer", "ponytail", "ponytail-review"}
BINARIES = ("pi", "toon", "gh-axi", "chrome-devtools-axi", "lavish-axi", "quota-axi", "playwright-axi")
PI_DEFAULTS = {"defaultProvider": "openai", "defaultModel": "gpt-6.2-astra", "enabledModels": ["openai/*"]}


def destinations() -> Iterator[tuple[Path, Path]]:
    project_only = set((ROOT / "skills/project-only.txt").read_text().split())
    available = {guide.parent.name for guide in (ROOT / "skills").glob("*/SKILL.md")}
    if project_only - available:
        raise SystemExit(f"Unknown names in skills/project-only.txt: {sorted(project_only - available)}")
    for name in sorted(available - project_only):
        skill = ROOT / "skills" / name
        for client in (".agents", ".cursor"):
            yield HOME / client / "skills" / skill.name, skill
        if skill.name in LEGACY_CODEX:
            yield HOME / ".codex/skills" / skill.name, skill
    yield HOME / ".cursor/rules/agent-defaults.mdc", ROOT / "rules/AGENTS.md"
    for client in (".codex", ".pi/agent"):
        yield HOME / client / "AGENTS.md", ROOT / "rules/AGENTS.md"
    for name in BINARIES:
        yield HOME / ".local/bin" / name, ROOT / "tools/node_modules/.bin" / name
    yield HOME / ".local/bin/herdr", ROOT / "tools/bin/herdr"
    yield HOME / ".local/bin/no-mistakes", ROOT / "tools/bin/no-mistakes"
    yield HOME / ".local/bin/exa-axi", ROOT / "tools/exa-axi.mjs"
    yield HOME / ".local/bin/agent-tmux", ROOT / "terminal/agent-tmux"


def managed_entry(target: Path) -> bool:
    """Recognize only the same-name links this setup installed or adopted."""
    if not target.is_symlink():
        return False
    first = Path(os.path.abspath(target.parent / target.readlink()))
    if target.parent == HOME / ".cursor/rules":
        return first == ROOT / "rules" / target.name
    shared = HOME / ".agents/skills" / target.name
    if target.parent == HOME / ".cursor/skills" and first == shared:
        return managed_entry(shared)
    return first == ROOT / "skills" / target.name


def link_project_skills(project: Path, names: list[str], check: bool) -> None:
    """Add just the named skills to this project and preserve project-owned entries."""
    project = project.expanduser().resolve()
    if not project.is_dir() or project == HOME.resolve():
        raise SystemExit("Choose an existing project directory distinct from your home directory.")
    available = {guide.parent.name: guide.parent for guide in (ROOT / "skills").glob("*/SKILL.md")}
    unknown = set(names) - available.keys()
    if unknown:
        raise SystemExit(f"Unknown skill: {', '.join(sorted(unknown))}")

    names = list(dict.fromkeys(names))
    pending = []
    for client in (".agents", ".cursor"):
        directory = project / client / "skills"
        if not directory.resolve().is_relative_to(project):
            raise SystemExit(f"Project skill directory resolves outside this project: {directory}")
        for parent in (directory.parent, directory):
            if (parent.exists() or parent.is_symlink()) and not parent.is_dir():
                raise SystemExit(f"Expected a project skill directory at {parent}")
        for name in names:
            source = available[name]
            target = directory / name
            if target.is_symlink() and target.resolve() == source.resolve():
                continue
            if target.is_symlink() or target.exists():
                raise SystemExit(f"Project already supplies {target}. Inspect the existing skill before linking.")
            pending.append((target, source))

    if check and pending:
        raise SystemExit("\n".join(f"Missing project link: {target}" for target, _ in pending))
    for target, source in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            target.symlink_to(source, target_is_directory=True)
        except FileExistsError:
            if not target.is_symlink() or target.resolve() != source.resolve():
                raise
    print(f"Verified project skills in {project}: {', '.join(names)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report drift without writing")
    mode.add_argument("--adopt", action="store_true", help="back up conflicting personal rules or skills and replace them with links")
    parser.add_argument("--project", type=Path, metavar="DIR", help="link only the named skills into one project")
    parser.add_argument("skills", nargs="*", metavar="SKILL", help="skill names to enable with --project")
    args = parser.parse_args()
    if args.project is not None:
        if args.adopt or not args.skills:
            parser.error("--project needs one or more skill names and cannot be combined with --adopt")
        link_project_skills(args.project, args.skills, args.check)
        return
    if args.skills:
        parser.error("skill names require --project DIR")
    backups = HOME / ".local/state/agent-setup/backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    links = list(destinations())
    desired = {target for target, _ in links}
    retired = []
    # Inspect both ends before moving either part of a legacy Cursor -> shared link.
    for directory in (".agents/skills", ".codex/skills", ".cursor/skills", ".cursor/rules"):
        for entry in sorted((HOME / directory).glob("*")):
            if entry not in desired and managed_entry(entry):
                retired.append(entry)
    pending = []
    for target, source in links:
        if not source.exists():
            raise SystemExit(f"Missing source {source}. Install the locked tools first.")
        if target.is_symlink() and target.resolve() == source.resolve():
            continue
        exists = target.exists() or target.is_symlink()
        if exists and not args.check:
            if (not args.adopt and not managed_entry(target)) or target.parent == HOME / ".local/bin":
                raise SystemExit(f"Existing unmanaged path: {target}. Inspect it before linking.")
        pending.append((target, source, exists))

    settings = HOME / ".pi/agent/settings.json"
    config = json.loads(settings.read_text()) if settings.exists() else {}
    change_settings = any(config.get(key) != value for key, value in PI_DEFAULTS.items())
    if args.check:
        for target in retired:
            print(f"Retired managed link: {target}")
        for target, _, _ in pending:
            print(f"Link differs: {target}")
        if change_settings:
            print(f"OpenAI settings differ: {settings}")
        if pending or change_settings or retired:
            raise SystemExit(1)
        print(f"Verified {len(links)} links and Pi's OpenAI defaults.")
        return

    for target in retired:
        saved = backups / target.relative_to(HOME)
        saved.parent.mkdir(parents=True, exist_ok=True)
        target.rename(saved)
    for target, source, exists in pending:
        # An earlier change to a shared skills path can also repair a Cursor link.
        if target.is_symlink() and target.resolve() == source.resolve():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        old = backups / target.relative_to(HOME)
        if exists:
            old.parent.mkdir(parents=True, exist_ok=True)
            target.rename(old)
        try:
            target.symlink_to(source, target_is_directory=source.is_dir())
        except OSError:
            if exists:
                old.rename(target)
            raise
    if change_settings:
        settings.parent.mkdir(parents=True, exist_ok=True)
        if settings.exists():
            old = backups / settings.relative_to(HOME)
            old.parent.mkdir(parents=True, exist_ok=True)
            old.write_bytes(settings.read_bytes())
            old.chmod(0o600)
        config.update(PI_DEFAULTS)
        with NamedTemporaryFile(mode="w", dir=settings.parent, delete=False) as tmp:
            json.dump(config, tmp, indent=2)
            tmp.write("\n")
        os.replace(tmp.name, settings)
    if backups.exists():
        print(f"Original paths retained in {backups}")
    print(f"Installed links for {len(links)} paths. Run scripts/link.py --check to verify.")


if __name__ == "__main__":
    main()
