#!/usr/bin/env python3
"""Copy skills and rules from this checkout to a user or project install.

Pi, Codex, and Cursor share the default skills directory. Explicit destinations
support agents with a different layout. Refreshing a copy saves the old version.
"""

import argparse
import fcntl
import os
import shutil
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
USER_DIR = Path.home()
SHARED_SKILLS = Path(".agents/skills")
DEFAULT_RULE_FILES = (
    ".codex/AGENTS.md",
    ".pi/agent/AGENTS.md",
    ".cursor/rules/agent-defaults.mdc",
)


def plan_install(args: argparse.Namespace) -> tuple[dict[Path, Path], list[Path]]:
    """Plan the source-to-destination copies and any legacy aliases to retire."""
    project = args.project.expanduser().resolve() if args.project else None
    if project is not None and (not project.is_dir() or project == USER_DIR.resolve()):
        raise SystemExit(
            "Choose an existing project directory distinct from your home directory."
        )

    # A directory qualifies through its SKILL.md. Resolve requested names here
    # before using them in any destination path.
    catalog = {
        guide.parent.name: guide.parent
        for guide in (ROOT / "skills").glob("*/SKILL.md")
    }
    names = set(args.skills or ())
    if args.all_skills:
        project_only = set((ROOT / "skills/project-only.txt").read_text().split())
        if project_only - catalog.keys():
            raise SystemExit(
                f"Unknown project-only skill: {', '.join(sorted(project_only - catalog.keys()))}"
            )
        names = catalog.keys() - project_only
    if names - catalog.keys():
        raise SystemExit(f"Unknown skill: {', '.join(sorted(names - catalog.keys()))}")

    scope = (project or USER_DIR).resolve()
    shared_dir = scope / SHARED_SKILLS
    skills_dir = (
        args.skills_dir.expanduser().resolve() if args.skills_dir else shared_dir
    )
    assets = {skills_dir / name: catalog[name] for name in sorted(names)}
    explicit_targets = set(assets) if args.skills_dir else set()

    # Older installs put aliases in client directories. Retire them only when
    # the shared directory will contain the replacements those clients can find.
    legacy_dirs = []
    if skills_dir == shared_dir:
        legacy_dirs.append(scope / ".cursor/skills")
        if project is None:
            legacy_dirs.append(scope / ".codex/skills")

    legacy_links = []
    for directory in legacy_dirs:
        for name in sorted(names):
            entry = directory / name
            if entry.is_symlink():
                first_hop = Path(os.path.abspath(entry.parent / entry.readlink()))
                # The alias may already point to a physical copy after a partial migration.
                if (
                    entry.resolve() == catalog[name].resolve()
                    or first_hop == shared_dir / name
                ):
                    legacy_links.append(entry)

    if args.rules or args.rules_file:
        rule_files = [scope / path for path in DEFAULT_RULE_FILES] if args.rules else []
        if args.rules_file:
            rule_file = args.rules_file.expanduser()
            # Resolve the parent so the existing file itself remains available for link checks.
            target = rule_file.parent.resolve() / rule_file.name
            rule_files.append(target)
            explicit_targets.add(target)
        for name in ("code-quality.md", "python.md"):
            assets[scope / ".local/share/agent-setup/rules" / name] = (
                ROOT / "rules" / name
            )
        for path in rule_files:
            if path in assets:
                raise SystemExit(
                    f"Rules and another asset have the same destination: {path}"
                )
            assets[path] = ROOT / "rules/AGENTS.md"

    # A default destination stays in its scope. An explicit path can live
    # elsewhere, but every install must stay separate from the reference checkout.
    for path in [*assets, *legacy_links]:
        parent = path.parent.resolve()
        if parent.is_relative_to(ROOT):
            raise SystemExit(
                f"Choose an install directory outside the reference checkout: {path.parent}"
            )
        if path not in explicit_targets and not parent.is_relative_to(scope):
            raise SystemExit(
                f"Configuration directory resolves outside the installation area: {path.parent}"
            )
        if any(ancestor in assets for ancestor in path.parents):
            raise SystemExit(
                f"Install destinations overlap at {path}. Choose separate paths."
            )
    return assets, legacy_links


def install_copy(source: Path, target: Path, backup: Path) -> None:
    """Prepare the copy before replacing anything at its destination."""
    target.parent.mkdir(parents=True, exist_ok=True)
    # Stage beside the destination so the final rename stays on the same filesystem.
    with TemporaryDirectory(prefix=".agent-setup-", dir=target.parent) as workspace:
        fresh = Path(workspace) / "copy"
        if source.is_dir():
            # ARIS has a relative helper alias. Materialize it inside the installed copy.
            for entry in source.rglob("*"):
                if entry.is_symlink() and not entry.resolve().is_relative_to(
                    source.resolve()
                ):
                    raise SystemExit(
                        f"Skill link points outside its source directory: {entry}"
                    )
            shutil.copytree(source, fresh)
        else:
            shutil.copy2(source, fresh)

        if not target.exists() and not target.is_symlink():
            fresh.rename(target)
            return

        backup.parent.mkdir(parents=True, exist_ok=True)
        previous = Path(workspace) / "previous"
        target.rename(previous)
        try:
            shutil.move(str(previous), str(backup))
            fresh.rename(target)
        except OSError:
            # Use the staging copy if the move failed, or the backup if publishing failed.
            saved = previous if previous.exists() or previous.is_symlink() else backup
            shutil.move(str(saved), str(target))
            raise


def install(args: argparse.Namespace, backups: Path) -> None:
    assets, legacy_links = plan_install(args)
    # Check every destination before changing the first one. Local copies stay
    # in place during repeat installs, including files edited by skill toggles.
    pending = []
    for target, source in assets.items():
        if target.is_symlink() and target.resolve() != source.resolve():
            raise SystemExit(f"Existing unmanaged link: {target}")
        if target.is_symlink() or not target.exists():
            pending.append((target, source))
        elif source.is_dir() and not (target / "SKILL.md").is_file():
            raise SystemExit(f"Existing path is not an installed skill: {target}")
        elif source.is_file() and not target.is_file():
            raise SystemExit(f"Existing path is not a rule file: {target}")
        elif args.refresh:
            pending.append((target, source))

    if args.check:
        if pending or legacy_links:
            raise SystemExit(
                "\n".join(
                    [
                        *(f"Needs a local copy: {target}" for target, _ in pending),
                        *(
                            f"Legacy duplicate link: {target}"
                            for target in legacy_links
                        ),
                    ]
                )
            )
        print(f"Verified {len(assets)} configuration copies.")
        return

    for target, source in pending:
        backup = (
            backups / target.relative_to(USER_DIR)
            if target.is_relative_to(USER_DIR)
            else (backups / "_external" / target.relative_to(target.anchor))
        )
        install_copy(source, target, backup)
    for entry in legacy_links:
        # A duplicate can point through the primary link that was just migrated.
        backup = backups / "legacy" / entry.relative_to(entry.anchor)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(entry), str(backup))

    print(
        f"Installed {len(pending)} copies. Kept {len(assets) - len(pending)} existing copies."
    )
    if backups.exists():
        print(f"Backups: {backups}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0], allow_abbrev=False
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--skills", nargs="+", metavar="SKILL", help="copy named skills"
    )
    selection.add_argument(
        "--all-skills", action="store_true", help="copy the suggested collection"
    )
    rules = parser.add_mutually_exclusive_group()
    rules.add_argument(
        "--rules",
        action="store_true",
        help="copy rules to the default client locations",
    )
    rules.add_argument(
        "--rules-file", type=Path, metavar="FILE", help="copy rules to this file"
    )
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument(
        "--project",
        type=Path,
        metavar="DIR",
        help="copy named skills to DIR/.agents/skills",
    )
    destination.add_argument(
        "--skills-dir", type=Path, metavar="DIR", help="override ~/.agents/skills"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check", action="store_true", help="check for local copies without writing"
    )
    mode.add_argument(
        "--refresh",
        action="store_true",
        help="back up and replace selected existing copies",
    )
    args = parser.parse_args()
    if not (args.skills or args.all_skills or args.rules or args.rules_file):
        parser.error("select --skills, --all-skills, --rules, or --rules-file")
    if args.project is not None and (not args.skills or args.rules or args.rules_file):
        parser.error("--project takes named --skills")
    if args.skills_dir is not None and not (args.skills or args.all_skills):
        parser.error("--skills-dir requires --skills or --all-skills")
    state = USER_DIR / ".local/state/agent-setup"
    backups = state / "backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    if args.check:
        install(args, backups)
        return
    state.mkdir(parents=True, exist_ok=True)

    # Hold the lock across planning and copying so two installs cannot both
    # decide to replace the same file.
    with (state / "config-install.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        install(args, backups)


if __name__ == "__main__":
    main()
