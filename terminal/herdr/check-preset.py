#!/usr/bin/env python3
"""Exercise a plain Herdr launch, installation into a live session, and snapshot restore."""

from contextlib import contextmanager
from collections.abc import Callable, Iterator
import fcntl
import json
import os
from pathlib import Path
import pty
import struct
import subprocess
import tempfile
import termios
import threading
import time
from typing import TypeVar

PLUGIN = Path(__file__).resolve().parent
EXPECTED = ["pi", "review", "git", "music"]
T = TypeVar("T")


def wait_for(read: Callable[[], T], accepts: Callable[[T], bool]) -> T:
    deadline = time.monotonic() + 12
    while True:
        value = read()
        if accepts(value):
            return value
        if time.monotonic() >= deadline:
            raise AssertionError(f"Timed out waiting for Herdr. Last value: {value!r}")
        time.sleep(0.1)


def check(directory: Path) -> None:
    # Give the default session a private socket, config, and snapshots. Nested invocations
    # must never inherit the developer's live Herdr socket or pane identifiers.
    env = {k: v for k, v in os.environ.items() if not k.startswith("HERDR_")}
    env.update(XDG_CONFIG_HOME=str(directory), XDG_STATE_HOME=str(directory / "state"),
               PATH=str(directory) + os.pathsep + env["PATH"], TERM="xterm-256color")
    config = directory / "herdr"
    config.mkdir()
    (config / "config.toml").write_text('onboarding = false\n[terminal]\ndefault_shell = "/bin/sh"\nshell_mode = "non_login"\n')

    # Record actual process launches without accounts, network access, or audio playback.
    trace = directory / "launches"
    env["PRESET_LAUNCHES"] = str(trace)
    for name in ("pi", "codex", "encore"):
        tool = directory / name
        tool.write_text('#!/bin/sh\nprintf "%s\\n" "${0##*/}" >> "$PRESET_LAUNCHES"\nexec /bin/cat\n')
        tool.chmod(0o755)

    def cli(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["herdr", *args], env=env, cwd=directory, text=True,
                              capture_output=True, check=check, timeout=12)

    def result(*args: str) -> dict:
        return json.loads(cli(*args).stdout)["result"]

    @contextmanager
    def attached() -> Iterator[None]:
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 32, 120, 0, 0))
        client = subprocess.Popen(["herdr"], stdin=slave, stdout=slave, stderr=slave,
                                  cwd=directory, env=env, start_new_session=True)
        os.close(slave)

        screen = bytearray()

        def drain() -> None:
            try:
                while chunk := os.read(master, 8192):
                    screen.extend(chunk)
                    del screen[:-500]
            except OSError:
                pass  # The client has released its pseudo-terminal.

        thread = threading.Thread(target=drain, daemon=True)
        thread.start()
        try:
            wait_for(lambda: cli("status", "server", "--json", check=False),
                     lambda p: p.returncode == 0 and json.loads(p.stdout)["running"])
            yield
        except Exception:
            print("Terminal output:", repr(bytes(screen[-500:])))
            print("Plugin log:", cli("plugin", "log", "list", "--limit", "4", check=False).stdout[-1800:])
            raise
        finally:
            cli("server", "stop", check=False)
            try:
                client.wait(timeout=5)
            except subprocess.TimeoutExpired:
                client.terminate()
                client.wait(timeout=5)
            os.close(master)
            thread.join(timeout=1)

    def main_tabs() -> list[dict]:
        spaces = result("workspace", "list")["workspaces"]
        groups = [s for s in spaces if s["label"] == "main"]
        assert len(groups) <= 1, groups
        return result("tab", "list", "--workspace", groups[0]["workspace_id"])["tabs"] if groups else []

    def verify_main() -> list[str]:
        tabs = wait_for(main_tabs, lambda rows: [tab["label"] for tab in rows] == EXPECTED)
        wait_for(lambda: trace.read_text().splitlines() if trace.exists() else [],
                 lambda runs: all(tool in runs for tool in ("pi", "codex", "encore")))
        return [tab["tab_id"] for tab in tabs]

    # Installing into a session with an open chat must create a separate, named group.
    with attached():
        original = result("tab", "list")["tabs"][0]
        cli("plugin", "link", str(PLUGIN))
        cli("plugin", "action", "invoke", "open", "--plugin", "agent-setup.tabs")
        tab_ids = verify_main()
        assert result("tab", "get", original["tab_id"])["tab"]["label"] == original["label"]
        cli("plugin", "action", "invoke", "open", "--plugin", "agent-setup.tabs")
        assert verify_main() == tab_ids

    # A stopped server has no live processes. Starting plain herdr must restore real programs.
    trace.write_text("")
    with attached():
        assert verify_main() == tab_ids


if __name__ == "__main__":
    # Short socket paths fit macOS's sockaddr_un limit.
    with tempfile.TemporaryDirectory(prefix="herdr-check-", dir="/tmp") as scratch:
        check(Path(scratch))
    print("Verified main tabs, preserved project tabs, and program startup after restart.")
