#!/bin/sh
# Exercise project routing and the optional Encore tab on a private tmux server.
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
for name in pi codex; do
    ln -s /usr/bin/true "$scratch/bin/$name"
done
printf '#!/bin/sh\nexec sleep 60\n' > "$scratch/bin/encore"
chmod +x "$scratch/bin/encore"
export PATH="$scratch/bin:$PATH"
"$launcher" --detach "$scratch/work #{test}"
session="$(tmux -L agent-setup list-sessions -F '#S')"
pane="$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')"
test "$(tmux -L agent-setup list-windows -t "$session" -F '#W' | LC_ALL=C sort | paste -sd , -)" = "git,pi,review"
"$launcher" --detach --encore "$scratch/work #{test}/src"
encore_pane="$(tmux -L agent-setup display-message -p -t "$session:encore" '#{pane_id}')"
# Reopening a project should also repair a Git tab closed since the last launch.
tmux -L agent-setup kill-window -t "$session:git"
"$launcher" --detach --encore "$scratch/work #{test}"
test "$(tmux -L agent-setup list-windows -t "$session" -F '#W' | LC_ALL=C sort | paste -sd , -)" = "encore,git,pi,review"
test "$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')" = "$pane"
test "$(tmux -L agent-setup display-message -p -t "$session:encore" '#{pane_id}')" = "$encore_pane"
test "$(tmux -L agent-setup show-options -Av -t "$session" status-position)" = "top"
test "$(tmux -L agent-setup show-options -Av -t "$session" status-right)" = "$(tmux -L agent-setup show-options -gv status-right)"
echo "Verified stable reattachment, top placement, inherited status, and opt-in Encore tab."
