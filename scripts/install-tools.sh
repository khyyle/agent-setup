#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ "$(uname -sm)" != 'Darwin arm64' ]; then
  echo 'The pinned Herdr and no-mistakes binaries target Apple Silicon macOS.' >&2
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
gate_digest=336d0df56988de1ce4e893217c32586fcea1b0ba4540744787e479e940145f49
if ! echo "$gate_digest  tools/bin/no-mistakes" | shasum -a 256 -c >/dev/null 2>&1; then
  gate_tmp="$(mktemp -d tools/bin/no-mistakes.XXXXXX)"
  trap 'rm -rf "$gate_tmp"' EXIT
  curl --fail --location --silent --show-error https://github.com/kunchenguid/no-mistakes/releases/download/v1.106.1/no-mistakes-v1.106.1-darwin-arm64.tar.gz -o "$gate_tmp/release.tgz"
  echo "3105ae3ffd9f5f6dc27674302dcd126a89ba9c23d43ecb8be5e266ac52f1472c  $gate_tmp/release.tgz" | shasum -a 256 -c
  tar -xOzf "$gate_tmp/release.tgz" no-mistakes > "$gate_tmp/no-mistakes"
  echo "$gate_digest  $gate_tmp/no-mistakes" | shasum -a 256 -c
  chmod 755 "$gate_tmp/no-mistakes"
  mv "$gate_tmp/no-mistakes" tools/bin/no-mistakes
fi
PLAYWRIGHT_SKIP_BROWSER_GC=1 tools/node_modules/.bin/playwright install chromium
