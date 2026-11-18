#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ "$(uname -sm)" != 'Darwin arm64' ]; then
  echo 'The pinned Herdr binary in this setup targets Apple Silicon macOS.' >&2
  exit 1
fi
node -e 'if (Number(process.versions.node.split(".")[0]) < 24) { console.error("Use Node 24 or newer"); process.exit(1) }'
npm ci --prefix tools --ignore-scripts --no-audit --no-fund
mkdir -p tools/bin
digest=fb77c2232a05a8035421382c894392f4174e4e38a18e48af3dd0290157c3a7e2
if ! echo "$digest  tools/bin/herdr" | shasum -a 256 -c >/dev/null 2>&1; then
  download="$(mktemp tools/bin/herdr.XXXXXX)"
  trap 'rm -f "$download"' EXIT
  curl --fail --location --silent --show-error https://github.com/herdrdev/herdr/releases/download/v0.9.5/herdr-macos-aarch64 -o "$download"
  echo "$digest  $download" | shasum -a 256 -c
  chmod 755 "$download"
  mv "$download" tools/bin/herdr
fi
PLAYWRIGHT_SKIP_BROWSER_GC=1 tools/node_modules/.bin/playwright install chromium
