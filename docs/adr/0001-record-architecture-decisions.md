# 1. Record architecture decisions

Date: 2026-08-01

## Status

Accepted

## Context

This repository documents technical work intended for engineering review, employer assessment, and open-source contribution. Significant design choices should be recorded explicitly rather than implied only through code or README prose.

## Decision

We will use Architecture Decision Records (ADRs) in `docs/adr/` with sequential numbering and short, descriptive titles.

### Format

Each ADR is a markdown file:

```
docs/adr/NNNN-short-title.md
```

Use this structure:

1. **Title** — imperative phrase
2. **Status** — Proposed | Accepted | Deprecated | Superseded
3. **Context** — forces and constraints
4. **Decision** — what we chose
5. **Consequences** — positive, negative, and follow-ups

### When to write an ADR

- Choosing a framework, datastore, or deployment target
- Adopting a cross-cutting pattern (caching, auth, observability)
- Accepting a known trade-off (mock vs live integration, sync vs async)

Skip ADRs for trivial refactors or dependency patch bumps.

## Consequences

- Reviewers can trace rationale without archaeology in pull requests.
- Future contributors understand constraints before proposing alternatives.
- ADRs are immutable once accepted; supersede with a new numbered record.

---

**Maintained by:** [Dark Heart Labs](https://darkheartlabs.technology)  
**Author:** Jennifer ([@jv-darkheartlabs](https://github.com/jv-darkheartlabs))  
**Site:** https://darkheartlabs.technology
