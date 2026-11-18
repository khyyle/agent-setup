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
LEGACY_CODEX = {"humanizer", "ponytail", "ponytail-review", "research-loop"}
BINARIES = ("pi", "toon", "gh-axi", "chrome-devtools-axi", "lavish-axi", "quota-axi", "playwright-axi")
PI_DEFAULTS = {"defaultProvider": "openai", "defaultModel": "gpt-6.2-astra", "enabledModels": ["openai/*"]}


def destinations() -> Iterator[tuple[Path, Path]]:
    for guide in sorted((ROOT / "skills").glob("*/SKILL.md")):
        skill = guide.parent
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
    for name in ("agent-tmux", "agent-music"):
        yield HOME / ".local/bin" / name, ROOT / "terminal" / name


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report drift without writing")
    mode.add_argument("--adopt", action="store_true", help="back up conflicting personal rules or skills and replace them with links")
    args = parser.parse_args()
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
