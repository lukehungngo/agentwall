#!/usr/bin/env bash
# Hook: pre-stop-gate
# Trigger: Stop
# Purpose: Full quality gate before session ends.
# Runs ruff + mypy --strict + pytest. Prints summary.

set -euo pipefail

cd /home/soh/working/agent-wall

echo "==============================="
echo "  AgentWall — pre-stop gate"
echo "==============================="

echo ""
echo "→ ruff check"
ruff check src/ tests/ --quiet

echo "→ mypy"
mypy src/ --strict --no-error-summary 2>&1 | tail -20

echo "→ pytest"
pytest --tb=short -q 2>&1 | tail -30

echo ""
echo "✓ gate passed"
