# 2. Use pymem-osx for macOS memory scanning

Date: 2026-08-01

## Status

Accepted

## Context

The upstream exporter uses the Windows-only `pymem` library (`MTGA.exe`, `CreateToolhelp32Snapshot`, `VirtualQueryEx`). Standard `pymem` on macOS provides mock Windows APIs and cannot attach to processes.

MTG Arena on Mac runs as process name `MTGA` with card catalogs under `~/Library/Application Support/com.wizards.mtga/Downloads/Raw`.

Alternatives considered:

- **mtga-reader (Rust/Node)** — robust Unity/Mono traversal but adds native bindings and a Node runtime
- **Log parsing** — no reliable collection payload in `Player.log` on this install
- **pymem-osx** — pure Python Mach VM read API, closest to upstream anchor-scan algorithm

## Decision

Use `pymem-osx` on macOS with a thin adapter (`mtga_memory.py`) that implements `pattern_scan_all` by walking readable Mach VM regions.

Document that users may need `sudo` when `task_for_pid` is denied.

Keep Windows code path available via standard `pymem` for upstream parity, but prioritize macOS in README and packaging.

## Consequences

**Positive**

- Reuses upstream anchor + block parsing logic with minimal changes
- No compiled Rust/Node dependency for v1
- Apple Silicon friendly (Mach 64-bit APIs)

**Negative**

- Memory scans can be slow (full region walk)
- Requires elevated privileges on many Macs
- `pymem-osx` package name conflicts with `pymem`; macOS installs must use `requirements-mac.txt` only

**Follow-ups**

- Evaluate mtga-reader if pymem-osx proves unstable across macOS versions
- Add release binaries via PyInstaller once manual testing passes

---

**Maintained by:** [Dark Heart Labs](https://darkheartlabs.technology)  
**Author:** Jennifer ([@jv-darkheartlabs](https://github.com/jv-darkheartlabs))  
**Site:** https://darkheartlabs.technology
