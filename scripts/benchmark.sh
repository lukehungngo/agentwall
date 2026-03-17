#!/usr/bin/env bash
# AgentWall Benchmark — scan 10 real-world LangChain projects
# Usage: ./scripts/benchmark.sh [targets_dir] [results_dir]
#
# Clones projects (if not already present) and runs agentwall scan on each.
# Produces JSON reports + a summary table.

set -euo pipefail

TARGETS_DIR="${1:-/tmp/agentwall-targets}"
RESULTS_DIR="${2:-/tmp/agentwall-results}"

mkdir -p "$TARGETS_DIR" "$RESULTS_DIR"

# ── Projects ──────────────────────────────────────────────────────────────

declare -A REPOS=(
  [langchain-chatchat]="https://github.com/chatchat-space/Langchain-Chatchat.git"
  [private-gpt]="https://github.com/zylon-ai/private-gpt.git"
  [quivr]="https://github.com/QuivrHQ/quivr.git"
  [localgpt]="https://github.com/PromtEngineer/localGPT.git"
  [docsgpt]="https://github.com/arc53/DocsGPT.git"
  [gpt-researcher]="https://github.com/assafelovic/gpt-researcher.git"
  [onyx]="https://github.com/onyx-dot-app/onyx.git"
  [db-gpt]="https://github.com/eosphoros-ai/DB-GPT.git"
  [chat-langchain]="https://github.com/langchain-ai/chat-langchain.git"
  [rasagpt]="https://github.com/paulpierre/RasaGPT.git"
)

# Projects that need --framework langchain (auto-detect fails)
declare -A FORCE_FRAMEWORK=(
  [localgpt]="langchain"
  [private-gpt]="langchain"
)

# ── Clone ─────────────────────────────────────────────────────────────────

echo "=== Cloning projects ==="
for name in "${!REPOS[@]}"; do
  dir="$TARGETS_DIR/$name"
  if [ -d "$dir" ]; then
    echo "  $name: already cloned"
  else
    echo "  $name: cloning..."
    git clone --depth 1 "${REPOS[$name]}" "$dir" 2>/dev/null
  fi
done

# ── Scan ──────────────────────────────────────────────────────────────────

echo ""
echo "=== Running AgentWall scans ==="
for name in "${!REPOS[@]}"; do
  dir="$TARGETS_DIR/$name"
  out="$RESULTS_DIR/$name.json"
  echo -n "  $name: scanning..."

  fw_flag=""
  if [[ -v "FORCE_FRAMEWORK[$name]" ]]; then
    fw_flag="--framework ${FORCE_FRAMEWORK[$name]}"
  fi

  # shellcheck disable=SC2086
  if agentwall scan "$dir" $fw_flag --fail-on none --output "$out" >/dev/null 2>&1; then
    echo " done"
  else
    echo " done (exit $?)"
  fi
done

# ── Summary ───────────────────────────────────────────────────────────────

echo ""
echo "=== Generating summary ==="

python3 -c "
import json, sys
from pathlib import Path

results = Path('$RESULTS_DIR')

projects = {
    'langchain-chatchat': ('Langchain-Chatchat', '~37k'),
    'private-gpt': ('PrivateGPT', '~54k'),
    'quivr': ('Quivr', '~36k'),
    'localgpt': ('LocalGPT', '~22k'),
    'docsgpt': ('DocsGPT', '~15k'),
    'gpt-researcher': ('GPT-Researcher', '~17k'),
    'onyx': ('Onyx/Danswer', '~12k'),
    'db-gpt': ('DB-GPT', '~17k'),
    'chat-langchain': ('Chat-LangChain', '~6k'),
    'rasagpt': ('RasaGPT', '~2.4k'),
}

total_findings = 0
total_crit = 0
total_high = 0
total_files = 0

print()
print('| Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |')
print('|---|---|---|---|---|---|---|---|---|')

for key, (name, stars) in projects.items():
    f = results / f'{key}.json'
    if not f.exists():
        print(f'| {name} | {stars} | - | - | - | - | - | - | not scanned |')
        continue
    data = json.loads(f.read_text())
    findings = data.get('findings', [])
    files = data.get('scanned_files', 0)
    total_files += files

    sev = {}
    rules = {}
    for finding in findings:
        s = finding.get('severity', '?').lower()
        sev[s] = sev.get(s, 0) + 1
        r = finding.get('rule_id', '?')
        rules[r] = rules.get(r, 0) + 1

    crit = sev.get('critical', 0)
    high = sev.get('high', 0)
    med = sev.get('medium', 0)
    low = sev.get('low', 0)
    total = len(findings)
    total_findings += total
    total_crit += crit
    total_high += high

    top = sorted(rules.items(), key=lambda x: -x[1])[:3]
    rule_str = ', '.join(f'{r}({c})' for r, c in top) if top else '-'

    print(f'| {name} | {stars} | {files} | {total} | {crit} | {high} | {med} | {low} | {rule_str} |')

print()
print(f'**Totals: {total_findings} findings ({total_crit} CRITICAL, {total_high} HIGH) across {total_files} files in {len(projects)} projects**')
"

echo ""
echo "JSON reports saved to: $RESULTS_DIR/"
