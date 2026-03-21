---
paths:
  - "action.yml"
  - ".github/workflows/**"
---

# GitHub Action & CI Security

## Shell injection prevention (P0)

NEVER use `${{ inputs.* }}` directly in shell commands. Use env vars:

```yaml
# WRONG — shell injection via crafted input
run: agentwall scan ${{ inputs.path }}

# CORRECT — env var + quoting
env:
  SCAN_PATH: ${{ inputs.path }}
run: agentwall scan "$SCAN_PATH"
```

## CI pipeline

- Test on Python 3.10, 3.11, 3.12 (matrix)
- `mypy src/ --strict` — always strict mode
- Publish workflow runs tests + lint before `hatch build`
- Trusted publishing via `pypa/gh-action-pypi-publish@release/v1`
