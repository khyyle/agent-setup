#!/bin/sh
# Exercise project routing and the Music status on a private tmux server.
set -eu
launcher="$(dirname "$0")/agent-tmux"
scratch="$(mktemp -d)"
export TMUX_TMPDIR="$scratch"
unset TMUX TMUX_PANE
cleanup() {
    tmux -L agent-setup kill-server 2>/dev/null || true
    rm -rf -- "$scratch"
}
trap cleanup EXIT
mkdir -p "$scratch/bin" "$scratch/work #{test}/src"
git init -q "$scratch/work #{test}"
# The preset needs real panes. The agents and the user's music library can stay idle.
for name in pi codex agent-music; do
    ln -s /usr/bin/true "$scratch/bin/$name"
done
export PATH="$scratch/bin:$PATH"
"$launcher" --detach "$scratch/work #{test}"
session="$(tmux -L agent-setup list-sessions -F '#S')"
pane="$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')"
"$launcher" --detach --music "$scratch/work #{test}/src"
# Reopening a project should also repair a Git tab closed since the last launch.
tmux -L agent-setup kill-window -t "$session:git"
"$launcher" --detach --music "$scratch/work #{test}"
test "$(tmux -L agent-setup list-windows -t "$session" -F '#W' | LC_ALL=C sort | paste -sd , -)" = "git,music,pi,review"
test "$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')" = "$pane"
test "$(tmux -L agent-setup show-options -Av -t "$session" status-position)" = "top"
tmux -L agent-setup show-options -v -t "$session" status-right | grep -Fq 'agent-music status'
echo "Verified four tabs, stable reattachment, top placement and the optional Music status."
