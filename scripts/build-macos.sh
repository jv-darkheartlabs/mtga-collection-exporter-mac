#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This build script targets macOS."
  exit 1
fi

PYTHON="${PYTHON:-python3}"

if [[ ! -d .venv ]]; then
  ./install.sh
fi

source .venv/bin/activate
python -m pip install --upgrade pip pyinstaller

pyinstaller \
  --onefile \
  --name mtga-export \
  --clean \
  --collect-all pymem \
  mtg.py

echo
echo "Built: $ROOT/dist/mtga-export"
echo "Run: ./dist/mtga-export"
echo "If memory access fails: sudo ./dist/mtga-export"
