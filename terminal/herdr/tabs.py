"""Create the session’s main tab group and keep project workspaces independent."""

import fcntl
import json
import os
from pathlib import Path
import shlex
import shutil
import socket

REVIEW = ["codex", "-s", "read-only", "-a", "never"]


def request(method: str, **params: object) -> dict:
    """Send one newline-delimited request to the server that invoked this plugin."""
    with socket.socket(socket.AF_UNIX) as connection:
        connection.settimeout(10)
        connection.connect(os.environ["HERDR_SOCKET_PATH"])
        message = {"id": method, "method": method, "params": params}
        connection.sendall(json.dumps(message).encode() + b"\n")
        with connection.makefile("rb") as reply:
            response = json.loads(reply.readline())
    if "error" in response:
        raise SystemExit(f"{method}: {response['error']['message']}")
    return response["result"]


def open_tab(workspace: str, cwd: str, label: str, command: list[str], focus: bool = False) -> str:
    # Supplying only workspace_id asks Herdr to create a tab. A tab_id would replace a live PTY.
    pane = {"type": "pane", "cwd": cwd}
    if command:
        pane["label"] = label
        pane["command"] = command
    layout = request("layout.apply", workspace_id=workspace, tab_label=label, root=pane, focus=focus)
    return layout["layout"]["tab_id"]


def restart_in_restored_shell(tab: dict, command: list[str]) -> None:
    """Restart a preset program when snapshot restore gave its pane a plain shell."""
    if tab["pane_count"] != 1:
        return
    root = request("layout.export", tab_id=tab["tab_id"])["layout"]["root"]
    if root.get("label") != tab["label"] or root.get("command"):
        return
    pane_id = root["pane_id"]
    pane = request("pane.get", pane_id=pane_id)["pane"]
    # Herdr resumes saved agent conversations after the client attaches.
    if pane.get("agent_session") or pane.get("agent") or pane.get("restore_error"):
        return
    process = request("pane.process_info", pane_id=pane_id)["process_info"]
    shell_pid = process.get("shell_pid")
    if not shell_pid or shell_pid != process.get("foreground_process_group_id"):
        return
    # A program started with shell exec can retain the shell's PID and foreground group.
    shells = {Path(line).name for line in Path("/etc/shells").read_text().splitlines() if line.startswith("/")}
    if any(p["pid"] == shell_pid and Path(p["name"]).name.lstrip("-") in shells
           for p in process["foreground_processes"]):
        request("pane.send_input", pane_id=pane_id, text=shlex.join(command), keys=["Enter"])


def main() -> None:
    action = os.environ.get("HERDR_PLUGIN_ACTION_ID")
    # Hooks and keybindings run in separate processes. Keep lookup and creation under one lock.
    with (Path(os.environ["HERDR_PLUGIN_STATE_DIR"]) / "tabs.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if action == "review":
            context = json.loads(os.environ["HERDR_PLUGIN_CONTEXT_JSON"])
            workspace = context["workspace_id"]
            tabs = request("tab.list", workspace_id=workspace)["tabs"]
            review = next((tab for tab in tabs if tab["label"] == "review"), None)
            if review:
                request("tab.focus", tab_id=review["tab_id"])
            else:
                worktree = context.get("worktree") or {}
                cwd = worktree.get("checkout_path") or context["workspace_cwd"]
                open_tab(workspace, cwd, "review", REVIEW, focus=True)
            return

        # A session can already contain projects or restored chats when this plugin first runs.
        # Only the dedicated group owns the preset. The launcher's cwd belongs to the project.
        spaces = request("workspace.list")["workspaces"]
        main_space = next((space for space in spaces if space["label"] == "main"), None)
        cwd = str(Path.home())
        if main_space:
            workspace = main_space["workspace_id"]
        else:
            group = request("workspace.create", label="main", cwd=cwd, focus=False)
            workspace = group["workspace"]["workspace_id"]
            request("tab.rename", tab_id=group["tab"]["tab_id"], label="git")
            request("workspace.move", workspace_id=workspace, insert_index=0)

        tabs = request("tab.list", workspace_id=workspace)["tabs"]
        by_label = {tab["label"]: tab for tab in tabs}
        commands = [("pi", ["pi", "--name", "implement"]), ("review", REVIEW), ("git", [])]
        if shutil.which("encore"):
            commands.append(("music", ["encore"]))
        for index, (label, command) in enumerate(commands):
            if label in by_label:
                if command and os.environ.get("HERDR_PLUGIN_EVENT") == "startup":
                    restart_in_restored_shell(by_label[label], command)
                continue
            tab = open_tab(workspace, cwd, label, command)
            # Position only new tabs. Reopening main preserves custom tabs and their ordering.
            if index < len(by_label):
                request("tab.move", tab_id=tab, insert_index=index)
            by_label[label] = {"tab_id": tab}

        if main_space is None:
            request("tab.focus", tab_id=by_label["pi"]["tab_id"])
        elif action == "open":
            request("workspace.focus", workspace_id=workspace)


if __name__ == "__main__":
    main()
