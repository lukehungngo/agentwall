---
paths:
  - "scripts/benchmark3000.sh"
  - "BENCHMARK3000.md"
---

# Benchmark Testing Rules

## Running benchmarks

```bash
# Full benchmark run (486 projects)
bash scripts/benchmark3000.sh

# Clear cached results for fresh run
rm -f /tmp/agentwall-results3k-*/*.json
```

## Critical: binary staleness

The `agentwall` CLI at `~/.local/bin/agentwall` comes from UV tool install. After code changes, you MUST reinstall:

```bash
uv tool install --force -e .
```

Without this, benchmarks run against stale code and results are meaningless.

## Result caching

The script skips projects with existing JSON results. To force re-scan, delete the results directory:
```bash
rm -f /tmp/agentwall-results3k-*/*.json
```

## Current metrics (v1.0)

- 486 registered projects, 480 scanned, 380 with findings (79%)
- 3,679 total findings
- 6.4% path-based FP estimate, ~8-9% real FP estimate
- 100 zero-finding projects remain (legitimate AI projects needing better detection)
