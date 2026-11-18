#!/bin/sh
# Exercise project routing and the music tab on a private tmux server.
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
"$launcher" --detach --no-music-tab "$scratch/work #{test}"
session="$(tmux -L agent-setup list-sessions -F '#S')"
pane="$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')"
test "$(tmux -L agent-setup list-windows -t "$session" -F '#W' | LC_ALL=C sort | paste -sd , -)" = "git,pi,review"
"$launcher" --detach "$scratch/work #{test}/src"
music_pane="$(tmux -L agent-setup display-message -p -t "$session:music" '#{pane_id}')"
# The previous preset used the window name encore.
tmux -L agent-setup rename-window -t "$session:music" encore
# Reopening a project should also repair a Git tab closed since the last launch.
tmux -L agent-setup kill-window -t "$session:git"
"$launcher" --detach --encore "$scratch/work #{test}"
test "$(tmux -L agent-setup list-windows -t "$session" -F '#W' | LC_ALL=C sort | paste -sd , -)" = "git,music,pi,review"
test "$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')" = "$pane"
test "$(tmux -L agent-setup display-message -p -t "$session:music" '#{pane_id}')" = "$music_pane"
test "$(tmux -L agent-setup show-options -Av -t "$session" status-position)" = "top"
status=$(tmux -L agent-setup show-options -Av -t "$session" status-right)
case "$status" in
    *'AGENT_SETUP_MUSIC_STATUS'*'%H:%M'*) ;;
    *) exit 1 ;;
esac
helper=$(tmux -L agent-setup show-environment -g AGENT_SETUP_MUSIC_STATUS)
test -x "${helper#AGENT_SETUP_MUSIC_STATUS=}"
echo "Verified stable reattachment, top status with the Music reader, and default music tab."
