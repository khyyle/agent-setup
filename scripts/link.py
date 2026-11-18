#!/usr/bin/env python3
"""Link the checkout's executables into a user bin directory."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NPM_TOOLS = (
    "pi",
    "toon",
    "gh-axi",
    "chrome-devtools-axi",
    "lavish-axi",
    "quota-axi",
    "playwright-axi",
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument(
        "--check", action="store_true", help="verify links without writing"
    )
    parser.add_argument(
        "--bin-dir",
        type=Path,
        metavar="DIR",
        default=Path.home() / ".local/bin",
        help="override ~/.local/bin",
    )
    args = parser.parse_args()
    bin_dir = args.bin_dir.expanduser().resolve()

    # npm provides launchers for its packages. The release binaries and
    # repository scripts have their own entry points.
    sources = {name: ROOT / "tools/node_modules/.bin" / name for name in NPM_TOOLS}
    sources.update(
        {
            "herdr": ROOT / "tools/bin/herdr",
            "no-mistakes": ROOT / "tools/bin/no-mistakes",
            "exa-axi": ROOT / "tools/exa-axi.mjs",
            "agent-tmux": ROOT / "terminal/agent-tmux",
        }
    )

    # Check the full set before writing links, so a name conflict leaves the bin directory alone.
    missing = []
    for name, source in sources.items():
        path = bin_dir / name
        if not source.exists():
            raise SystemExit(f"Missing {source}. Run ./scripts/install-tools.sh first.")
        if path.is_symlink() and path.resolve() == source.resolve():
            continue
        if path.exists() or path.is_symlink():
            raise SystemExit(f"Existing unmanaged executable: {path}")
        missing.append((path, source))

    if args.check and missing:
        raise SystemExit("\n".join(f"Missing tool link: {path}" for path, _ in missing))
    for path, source in missing:
        bin_dir.mkdir(parents=True, exist_ok=True)
        try:
            path.symlink_to(source)
        except FileExistsError:
            # A parallel install may have already created the same link.
            if not path.is_symlink() or path.resolve() != source.resolve():
                raise
    print(f"Verified {len(sources)} tool links in {bin_dir}.")


if __name__ == "__main__":
    main()
