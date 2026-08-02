# MTGA Collection Exporter (macOS)

Export your **Magic: The Gathering Arena** collection on macOS to text, JSON, and Moxfield-compatible CSV while the game is running.

Fork of [NthPhantom10/MTGA-collection-exporter](https://github.com/NthPhantom10/MTGA-collection-exporter) with macOS paths, memory backend, installer, and distribution tooling.

## Problem

MTG Arena on Mac stores card metadata locally, but there is no built-in export for deck builders like Moxfield. The upstream exporter targets Windows memory APIs; this fork adds a macOS memory scanner and Apple-native install paths.

## Solution

1. Load card names from local MTGA SQLite catalogs (Scryfall fallback)
2. Attach to the running `MTGA` process and scan memory using anchor cards you own
3. Write three export files next to the script

| File | Purpose |
|------|---------|
| `mtga_collection.txt` | Human-readable count + name (+ set) |
| `mtga_collection.json` | Structured export with set and collector number |
| `mtga_collection.csv` | Moxfield import format |

## Requirements

- macOS 12+ (Apple Silicon tested)
- Python 3.10+
- MTG Arena installed and running
- Network only needed if local card DB cache is missing (Scryfall fallback)

## Quick start

```bash
git clone https://github.com/jv-darkheartlabs/mtga-collection-exporter-mac.git
cd mtga-collection-exporter-mac
chmod +x install.sh
./install.sh
source .venv/bin/activate
python mtg.py
```

### Before you run

1. Launch **MTG Arena**
2. Open **Decks** or **Collection**
3. Scroll through cards for ~30 seconds so your collection loads into memory

### macOS permissions

Memory scanning uses Mach APIs. If connection fails:

```bash
sudo .venv/bin/python mtg.py
```

You may also need to grant **Full Disk Access** to Terminal (or your IDE) under System Settings → Privacy & Security.

## Homebrew (optional)

```bash
brew install jv-darkheartlabs/tap/mtga-collection-exporter-mac
mtga-export
```

See `Formula/mtga-collection-exporter-mac.rb` for the formula source.

## Build a standalone CLI binary

```bash
./scripts/build-macos.sh
./dist/mtga-export
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "MTG Arena not running" | Open the game and visit Collection/Decks first |
| "task_for_pid failed" | Run with `sudo` |
| Scanner finds no collection | Use rarer anchor cards (legendaries work well) |
| Wrong card names | Delete `arena_id_lookup.json` to rebuild cache |
| Duplicate entries | Should be fixed vs upstream; report if you see regressions |

## Project layout

| Path | Role |
|------|------|
| `mtg.py` | CLI entrypoint and export logic |
| `mtga_memory.py` | macOS/Windows memory backend |
| `install.sh` | macOS venv + dependency setup |
| `requirements-mac.txt` | macOS deps (`pymem-osx`, `requests`) |
| `docs/TECH_SPEC.md` | Architecture and evidence map |

## Upstream credit

Based on [MTGA-collection-exporter](https://github.com/NthPhantom10/MTGA-collection-exporter) by NthPhantom10 (MIT). Windows `.exe` workflow remains documented upstream.

## License

MIT — see [LICENSE](LICENSE).

---

**Maintained by:** [Dark Heart Labs](https://darkheartlabs.technology)  
**Author:** Jennifer ([@jv-darkheartlabs](https://github.com/jv-darkheartlabs))  
**Site:** https://darkheartlabs.technology
