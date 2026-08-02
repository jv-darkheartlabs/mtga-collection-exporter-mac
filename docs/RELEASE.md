# Releasing MTGA Collection Exporter (macOS)

How to publish a version everyone can install **without** committing personal export data.

## What never goes in the repo

These are gitignored and generated on each user's machine:

| File | Why |
|------|-----|
| `last_anchors.json` | User's calibration cards |
| `arena_id_lookup.json` | Cached card DB from local MTGA install |
| `mtga_collection.*` | User's collection export |
| `export.log` | Debug log from a run |
| `.venv/`, `dist/`, `build/` | Local build artifacts |

Verify before every release:

```bash
git status
git ls-files | rg 'collection|anchor|lookup|export\.log'
```

## Distribution channels

### 1. Source install (always available)

Users clone and run `./install.sh` — no release required.

### 2. GitHub Releases (recommended for non-developers)

1. Merge fixes to `main`
2. Tag a version:

```bash
git tag -a v1.0.0-mac -m "First macOS release"
git push origin v1.0.0-mac
```

3. GitHub Actions (`.github/workflows/release-macos.yml`) builds `mtga-export` and uploads:
   - `mtga-export` (standalone binary)
   - `mtga-collection-exporter-mac-macos-arm64.zip` (binary + README + LICENSE)

4. Users download from [Releases](https://github.com/jv-darkheartlabs/mtga-collection-exporter-mac/releases):

```bash
# Example after v1.0.0-mac is published
curl -LO https://github.com/jv-darkheartlabs/mtga-collection-exporter-mac/releases/download/v1.0.0-mac/mtga-export
chmod +x mtga-export
sudo ./mtga-export
```

First run on macOS may require **Right-click → Open** (unsigned binary).

### 3. Homebrew tap (optional)

1. Create `jv-darkheartlabs/homebrew-tap` if it does not exist
2. Copy `Formula/mtga-collection-exporter-mac.rb` into the tap
3. Update `url` and `sha256` to the release tarball:

```bash
shasum -a 256 mtga-collection-exporter-mac-1.0.0-mac.tar.gz
```

4. Users install with:

```bash
brew tap jv-darkheartlabs/tap
brew install mtga-collection-exporter-mac
```

## Pre-release checklist

- [ ] `./install.sh` works on a clean Mac
- [ ] Export succeeds with sudo against a running MTGA client
- [ ] No personal files staged in git
- [ ] README install paths match release asset names
- [ ] Tag pushed → CI green → assets on Releases page

## Notarization (future)

For friction-free installs on other people's Macs, add Apple notarization to the release workflow. Not required for open-source / technical users who can use source install or Right-click → Open.

---

**Maintained by:** [Dark Heart Labs](https://darkheartlabs.technology)  
**Author:** Jennifer ([@jv-darkheartlabs](https://github.com/jv-darkheartlabs))  
**Site:** https://darkheartlabs.technology
