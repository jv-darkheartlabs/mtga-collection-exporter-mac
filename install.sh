#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This installer targets macOS. Use install.bat on Windows."
  exit 1
fi

PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "python3 not found. Install Python 3.10+ and retry."
  exit 1
fi

"$PYTHON" -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-mac.txt

cat <<EOF

Install complete.

Run the exporter:
  source .venv/bin/activate
  python mtg.py

If memory access fails, retry with sudo:
  sudo .venv/bin/python mtg.py

Before exporting:
  1. Launch MTG Arena
  2. Open Decks or Collection
  3. Scroll through cards for ~30 seconds so the collection loads into memory
EOF
