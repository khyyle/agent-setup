#!/bin/sh
# Exercise workspace creation and reattachment with real tmux panes.
# This test uses a temporary Git checkout and stand-ins for services like 
# Pi, Codex, and Encore.
set -eu
launcher="$(dirname "$0")/agent-tmux"
scratch="$(mktemp -d)"

# Keep test sessions and cleanup confined to a private tmux socket.
export TMUX_TMPDIR="$scratch"
unset TMUX TMUX_PANE
cleanup() {
    tmux -L agent-setup kill-server 2>/dev/null || true
    rm -rf -- "$scratch"
}
trap cleanup EXIT

# Include a space and a tmux format marker to exercise path handling.
mkdir -p "$scratch/bin" "$scratch/work #{test}/src"
git init -q "$scratch/work #{test}"

# Make the launcher find local stand-ins. The Encore pane stays open for reattachment.
for name in pi codex; do
    ln -s /usr/bin/true "$scratch/bin/$name"
done

printf '#!/bin/sh\nexec sleep 60\n' > "$scratch/bin/encore"
chmod +x "$scratch/bin/encore"
export PATH="$scratch/bin:$PATH"

# Start without the player, even though Encore is available on PATH.
"$launcher" --detach --no-music-tab "$scratch/work #{test}"
session="$(tmux -L agent-setup list-sessions -F '#S')"
pane="$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')"
# Check the exact set of starter tabs, including the effect of --no-music-tab.
test "$(tmux -L agent-setup list-windows -t "$session" -F '#W' | LC_ALL=C sort | paste -sd , -)" = "git,pi,review"

# Launch from a subdirectory. The default music tab must appear in the original session.
"$launcher" --detach "$scratch/work #{test}/src"
music_pane="$(tmux -L agent-setup display-message -p -t "$session:music" '#{pane_id}')"

# Close Git to exercise the launcher's repair path on reattach.
tmux -L agent-setup kill-window -t "$session:git"
"$launcher" --detach --encore "$scratch/work #{test}"

# Check that Git returns and the session has exactly one tab of each kind.
test "$(tmux -L agent-setup list-windows -t "$session" -F '#W' | LC_ALL=C sort | paste -sd , -)" = "git,music,pi,review"

# Check that the original Pi pane survives both relaunches.
test "$(tmux -L agent-setup display-message -p -t "$session:pi" '#{pane_id}')" = "$pane"

# Check that reattaching keeps the existing player pane.
test "$(tmux -L agent-setup display-message -p -t "$session:music" '#{pane_id}')" = "$music_pane"

# Check that the session inherits the preset's top status bar.
test "$(tmux -L agent-setup show-options -Av -t "$session" status-position)" = "top"

# Check the status format for the helper reference and clock. This checks configuration only.
status=$(tmux -L agent-setup show-options -Av -t "$session" status-right)
case "$status" in
    *'AGENT_SETUP_MUSIC_STATUS'*'%H:%M'*) ;;
    *) exit 1 ;;
esac

# Check that the helper path exported to tmux points to an executable file.
helper=$(tmux -L agent-setup show-environment -g AGENT_SETUP_MUSIC_STATUS)
test -x "${helper#AGENT_SETUP_MUSIC_STATUS=}"
echo "Verified stable reattachment, top status with the Music reader, and default music tab."
