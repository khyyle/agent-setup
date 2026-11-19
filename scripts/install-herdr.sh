#!/bin/sh
# Install the tab preset and the hook for repository-defined worktree setup.
set -eu
cd "$(dirname "$0")/.."
herdr=./tools/bin/herdr
config=${HERDR_CONFIG_PATH:-${XDG_CONFIG_HOME:-$HOME/.config}/herdr/config.toml}

"$herdr" plugin link "$PWD/terminal/herdr" >/dev/null
"$herdr" integration install pi

# An exact upstream revision keeps the worktree hook reproducible across machines.
revision=bdd6b4783b8ad673890ba74bdceb8480b12c3572
plugin=toyamarinyon.worktree-setup
installed=$("$herdr" plugin list --plugin "$plugin" --json)
if ! printf '%s' "$installed" | python3 -c '
import json, sys
plugins = json.load(sys.stdin)["result"]["plugins"]
sys.exit(0 if any(p["source"].get("resolved_commit") == sys.argv[1] and p["enabled"] for p in plugins) else 1)
' "$revision"; then
    "$herdr" plugin install toyamarinyon/herdr-worktree-setup --ref "$revision" --yes
fi

# The tab bar belongs to the user's Herdr profile. Seed fresh profiles and keep existing UI choices.
mkdir -p "$(dirname "$config")"
if [ -e "$config" ]; then
    echo "For the Music and clock display, merge terminal/herdr/ui.toml into $config."
else
    (set -C; cat terminal/herdr/ui.toml > "$config")
fi
"$herdr" config check

# Linking a plugin does not replay startup hooks on an already-running server.
server=$("$herdr" status server --json)
if [ "$(printf '%s' "$server" | python3 -c 'import json, sys; print(json.load(sys.stdin)["running"])')" = True ]; then
    "$herdr" plugin action invoke open --plugin agent-setup.tabs >/dev/null
fi
