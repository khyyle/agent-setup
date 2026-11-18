#!/bin/sh
set -eu
cd "$(dirname "$0")/.."

case "${1:-}" in
  '') install_encore=false ;;
  --encore) install_encore=true ;;
  *) echo "Usage: $0 [--encore]" >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
  echo "Usage: $0 [--encore]" >&2
  exit 2
fi

pi=./tools/node_modules/.bin/pi
if [ ! -x "$pi" ]; then
  echo 'Run ./scripts/install-tools.sh first.' >&2
  exit 1
fi

command -v chafa >/dev/null 2>&1 || brew install chafa
command -v ffmpeg >/dev/null 2>&1 || brew install ffmpeg
if "$install_encore" && ! command -v encore >/dev/null 2>&1; then
  brew install bogdankim/tap/encore
fi

# This revision discovers the symlinks in ~/.agents/skills.
"$pi" install git:github.com/Whamp/pi-skill-toggle@bfb4ff810e49cf42c43ea818c5676a2e74398f3f
packages=$("$pi" list --no-approve)
old_toggle=$(printf '%s\n' "$packages" | awk '/^  npm:pi-skill-toggle(@[^ ]+)?$/ {print $1; exit}')
if [ -n "$old_toggle" ]; then
  "$pi" remove "$old_toggle"
fi
"$pi" install npm:@earendil-works/pi-voice@0.2.0
"$pi" install npm:@tintinweb/pi-subagents@0.26.1
"$pi" install npm:@lordekeen/pi-chafa@0.2.1
"$pi" install npm:pi-md-export@0.4.2
