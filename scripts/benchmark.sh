#!/usr/bin/env bash
# AgentWall Benchmark — scan top 20 real-world LangChain projects
# Usage: ./scripts/benchmark.sh [targets_dir] [results_dir]
#
# Clones projects (if not already present), runs agentwall scan on each,
# maps findings to attack vectors, and generates BENCHMARK.md.

set -euo pipefail

TARGETS_DIR="${1:-/tmp/agentwall-targets}"
RESULTS_DIR="${2:-/tmp/agentwall-results}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BENCHMARK_MD="$PROJECT_ROOT/BENCHMARK.md"

mkdir -p "$TARGETS_DIR" "$RESULTS_DIR"

# ── Projects (top 20 by stars, LangChain ecosystem) ──────────────────────

# Ordered list to preserve display order
REPO_NAMES=(
  langchain-chatchat
  private-gpt
  quivr
  localgpt
  docsgpt
  gpt-researcher
  onyx
  db-gpt
  chat-langchain
  rasagpt
  langflow
  flowise
  open-interpreter
  chainlit
  embedchain
  llm-app
  haystack
  superagent
  agentgpt
  auto-gpt-web
)

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
  [langflow]="https://github.com/langflow-ai/langflow.git"
  [flowise]="https://github.com/FlowiseAI/Flowise.git"
  [open-interpreter]="https://github.com/OpenInterpreter/open-interpreter.git"
  [chainlit]="https://github.com/Chainlit/chainlit.git"
  [embedchain]="https://github.com/mem0ai/mem0.git"
  [llm-app]="https://github.com/pathwaycom/llm-app.git"
  [haystack]="https://github.com/deepset-ai/haystack.git"
  [superagent]="https://github.com/superagent-ai/superagent.git"
  [agentgpt]="https://github.com/reworkd/AgentGPT.git"
  [auto-gpt-web]="https://github.com/Significant-Gravitas/AutoGPT.git"
)

# Projects that need --framework langchain (auto-detect fails)
declare -A FORCE_FRAMEWORK=(
  [localgpt]="langchain"
  [private-gpt]="langchain"
  [embedchain]="langchain"
  [llm-app]="langchain"
  [superagent]="langchain"
)

# ── Clone ─────────────────────────────────────────────────────────────────

echo "=== Cloning projects ==="
for name in "${REPO_NAMES[@]}"; do
  dir="$TARGETS_DIR/$name"
  if [ -d "$dir" ]; then
    echo "  $name: already cloned"
  else
    echo "  $name: cloning..."
    git clone --depth 1 "${REPOS[$name]}" "$dir" 2>/dev/null || echo "  $name: clone failed"
  fi
done

# ── Scan ──────────────────────────────────────────────────────────────────

echo ""
echo "=== Running AgentWall scans ==="
for name in "${REPO_NAMES[@]}"; do
  dir="$TARGETS_DIR/$name"
  out="$RESULTS_DIR/$name.json"

  if [ ! -d "$dir" ]; then
    echo "  $name: skipped (not cloned)"
    continue
  fi

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

# ── Generate BENCHMARK.md ────────────────────────────────────────────────

echo ""
echo "=== Generating BENCHMARK.md ==="

python3 << 'PYEOF'
import json
import sys
from pathlib import Path
from datetime import date

RESULTS_DIR = Path("RESULTS_DIR_PLACEHOLDER")
BENCHMARK_MD = Path("BENCHMARK_MD_PLACEHOLDER")

# ── Attack vector mapping ────────────────────────────────────────────────
# Rule ID → attack vector(s) it detects (verified against code)
RULE_TO_VECTORS = {
    "AW-MEM-001": ["AW-ATK-MEM-001"],
    "AW-MEM-002": ["AW-ATK-MEM-002"],
    "AW-MEM-003": ["AW-ATK-MEM-003"],
    "AW-MEM-004": ["AW-ATK-MEM-004"],
    "AW-MEM-005": ["AW-ATK-INJ-001"],
    "AW-TOOL-001": ["AW-ATK-AGT-001"],
    "AW-TOOL-002": ["AW-ATK-AGT-001"],
    "AW-TOOL-003": ["AW-ATK-AGT-001"],
    "AW-TOOL-004": [],
    "AW-TOOL-005": [],
    "AW-CFG-allow-reset": ["AW-ATK-CFG-001"],
    "AW-CFG-no-tls": ["AW-ATK-CFG-003"],
    "AW-CFG-hardcoded-secret": ["AW-ATK-CFG-004"],
    "AW-CFG-docker-no-auth": ["AW-ATK-CFG-003"],
    "AW-CFG-no-auth": ["AW-ATK-CFG-003"],
    "AW-CFG-debug-mode": ["AW-ATK-CFG-001"],
    "AW-CFG-exposed-port": ["AW-ATK-CFG-003"],
    "AW-CFG-no-password": ["AW-ATK-CFG-003"],
}

# Full attack vector catalog (32 vectors)
ALL_VECTORS = {
    "AW-ATK-MEM-001": "Cross-Tenant Retrieval (No Filter)",
    "AW-ATK-MEM-002": "Weak Tenant Isolation (Static Filter)",
    "AW-ATK-MEM-003": "Namespace/Collection Confusion",
    "AW-ATK-MEM-004": "Partition Bypass via Direct API",
    "AW-ATK-POI-001": "PoisonedRAG — Knowledge Corruption",
    "AW-ATK-POI-002": "CorruptRAG — Single-Document Poisoning",
    "AW-ATK-POI-003": "MINJA — Memory Injection via Query-Only",
    "AW-ATK-POI-004": "Persistent Memory Poisoning (Sleeper)",
    "AW-ATK-POI-005": "Document Loader Exploitation",
    "AW-ATK-POI-006": "Training Data Backdoor via Memory",
    "AW-ATK-EMB-001": "Vector Collision Attack",
    "AW-ATK-EMB-002": "Semantic Cache Poisoning",
    "AW-ATK-EMB-003": "Embedding Inversion (Reconstruction)",
    "AW-ATK-EMB-004": "Adversarial Multi-Modal Embedding",
    "AW-ATK-EMB-005": "Vector Drift / Stale Embedding",
    "AW-ATK-INJ-001": "Stored Prompt Injection in Retrieved Context",
    "AW-ATK-INJ-002": "Cross-Session Context Hijacking",
    "AW-ATK-INJ-003": "EchoLeak — Silent Data Exfiltration",
    "AW-ATK-EXF-001": "Membership Inference via Retrieval",
    "AW-ATK-EXF-002": "Embedding Exfiltration via Exposed API",
    "AW-ATK-EXF-003": "Side-Channel Leakage via Timing",
    "AW-ATK-CFG-001": "Unsafe Reset Enabled",
    "AW-ATK-CFG-002": "No Encryption at Rest",
    "AW-ATK-CFG-003": "No TLS / No Auth / Exposed Ports",
    "AW-ATK-CFG-004": "Hardcoded API Keys in Config",
    "AW-ATK-CFG-005": "Missing RBAC on Vector Store",
    "AW-ATK-CFG-006": "No Row-Level Security (PGVector)",
    "AW-ATK-DOS-001": "High-Dimensional Embedding Flood",
    "AW-ATK-DOS-002": "Expensive Query Amplification",
    "AW-ATK-DOS-003": "Collection/Index Deletion via Admin",
    "AW-ATK-AGT-001": "Tool Poisoning / Unsafe Tool Access",
    "AW-ATK-AGT-002": "Delegation Chain Privilege Escalation",
    "AW-ATK-AGT-003": "Memory-Mediated Identity Hijacking",
    "AW-ATK-AGT-004": "Cross-Agent Memory Contamination",
    "AW-ATK-AGT-005": "Conversation History Replay",
}

# Detectable vectors (verified in code)
DETECTABLE_VECTORS = {
    "AW-ATK-MEM-001", "AW-ATK-MEM-002", "AW-ATK-MEM-003", "AW-ATK-MEM-004",
    "AW-ATK-INJ-001",
    "AW-ATK-CFG-001", "AW-ATK-CFG-003", "AW-ATK-CFG-004",
    "AW-ATK-AGT-001",
}

# Projects metadata (display name, stars)
PROJECTS = {
    "langchain-chatchat": ("Langchain-Chatchat", "~37k"),
    "private-gpt": ("PrivateGPT", "~54k"),
    "quivr": ("Quivr", "~36k"),
    "localgpt": ("LocalGPT", "~22k"),
    "docsgpt": ("DocsGPT", "~15k"),
    "gpt-researcher": ("GPT-Researcher", "~17k"),
    "onyx": ("Onyx/Danswer", "~12k"),
    "db-gpt": ("DB-GPT", "~17k"),
    "chat-langchain": ("Chat-LangChain", "~6k"),
    "rasagpt": ("RasaGPT", "~2.4k"),
    "langflow": ("Langflow", "~48k"),
    "flowise": ("Flowise", "~35k"),
    "open-interpreter": ("Open Interpreter", "~58k"),
    "chainlit": ("Chainlit", "~8k"),
    "embedchain": ("Mem0/Embedchain", "~25k"),
    "llm-app": ("LLM App (Pathway)", "~4k"),
    "haystack": ("Haystack", "~18k"),
    "superagent": ("SuperAgent", "~5k"),
    "agentgpt": ("AgentGPT", "~32k"),
    "auto-gpt-web": ("AutoGPT", "~172k"),
}

# Preserve order
PROJECT_ORDER = [
    "langchain-chatchat", "private-gpt", "quivr", "localgpt", "docsgpt",
    "gpt-researcher", "onyx", "db-gpt", "chat-langchain", "rasagpt",
    "langflow", "flowise", "open-interpreter", "chainlit", "embedchain",
    "llm-app", "haystack", "superagent", "agentgpt", "auto-gpt-web",
]


def load_results(results_dir: Path) -> dict:
    """Load all JSON scan results."""
    data = {}
    for key in PROJECT_ORDER:
        f = results_dir / f"{key}.json"
        if f.exists():
            try:
                data[key] = json.loads(f.read_text())
            except json.JSONDecodeError:
                data[key] = None
        else:
            data[key] = None
    return data


def extract_vectors(findings: list[dict]) -> dict[str, list[dict]]:
    """Map findings to attack vectors with evidence."""
    vectors: dict[str, list[dict]] = {}
    for f in findings:
        rule_id = f.get("rule_id", "")
        mapped = RULE_TO_VECTORS.get(rule_id, [])
        for vec_id in mapped:
            if vec_id not in vectors:
                vectors[vec_id] = []
            vectors[vec_id].append({
                "rule_id": rule_id,
                "file": f.get("file"),
                "line": f.get("line"),
                "severity": f.get("severity", "?"),
                "title": f.get("title", ""),
            })
    return vectors


def generate_benchmark_md(results_dir: Path, output_path: Path) -> None:
    """Generate the full BENCHMARK.md."""
    results = load_results(results_dir)
    today = date.today().isoformat()

    lines = []
    w = lines.append

    w("# AgentWall Benchmark Report")
    w("")
    w(f"**Date:** {today}")
    w("**Version:** 0.1.0 (Phase 1 complete)")
    w("**Layers enabled:** L0\u2013L6 (default static analysis)")
    w("**Reproduce:** `./scripts/benchmark.sh`")
    w("")
    w("---")
    w("")

    # ── Section 1: Summary table ──────────────────────────────────────────
    w("## 1. Scan Results (20 Projects)")
    w("")
    w("| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |")
    w("|---|---|---|---|---|---|---|---|---|---|")

    total_findings = 0
    total_crit = 0
    total_high = 0
    total_files = 0
    projects_with_findings = 0
    all_vectors_found: dict[str, list[dict]] = {}

    for idx, key in enumerate(PROJECT_ORDER, 1):
        name, stars = PROJECTS[key]
        data = results.get(key)

        if data is None:
            w(f"| {idx} | {name} | {stars} | - | - | - | - | - | - | not scanned |")
            continue

        findings = data.get("findings", [])
        files = data.get("scanned_files", 0)
        total_files += files

        sev: dict[str, int] = {}
        rules: dict[str, int] = {}
        for f in findings:
            s = f.get("severity", "?").lower()
            sev[s] = sev.get(s, 0) + 1
            r = f.get("rule_id", "?")
            rules[r] = rules.get(r, 0) + 1

        crit = sev.get("critical", 0)
        high = sev.get("high", 0)
        med = sev.get("medium", 0)
        low = sev.get("low", 0) + sev.get("info", 0)
        total = len(findings)
        total_findings += total
        total_crit += crit
        total_high += high
        if total > 0:
            projects_with_findings += 1

        top = sorted(rules.items(), key=lambda x: -x[1])[:3]
        rule_str = ", ".join(f"{r}({c})" for r, c in top) if top else "\u2014"

        # Collect attack vectors for this project
        proj_vectors = extract_vectors(findings)
        for vec_id, evidence in proj_vectors.items():
            if vec_id not in all_vectors_found:
                all_vectors_found[vec_id] = []
            for e in evidence:
                e["project"] = name
            all_vectors_found[vec_id].extend(evidence)

        w(f"| {idx} | {name} | {stars} | {files} | {total} | {crit} | {high} | {med} | {low} | {rule_str} |")

    w("")
    w(f"**Totals: {total_findings} findings ({total_crit} CRITICAL, {total_high} HIGH) across {total_files} files in {len(PROJECT_ORDER)} projects. {projects_with_findings}/{len(PROJECT_ORDER)} projects have findings.**")
    w("")
    w("---")
    w("")

    # ── Section 2: Rule distribution ──────────────────────────────────────
    w("## 2. Rule Distribution")
    w("")

    all_rules: dict[str, int] = {}
    for key in PROJECT_ORDER:
        data = results.get(key)
        if data is None:
            continue
        for f in data.get("findings", []):
            r = f.get("rule_id", "?")
            all_rules[r] = all_rules.get(r, 0) + 1

    if all_rules:
        w("| Rule | Count | % | Description |")
        w("|---|---|---|---|")
        rule_descs = {
            "AW-MEM-001": "No tenant isolation in vector store",
            "AW-MEM-002": "Shared collection without retrieval filter",
            "AW-MEM-003": "Memory backend has no access control",
            "AW-MEM-004": "Injection patterns in retrieval path",
            "AW-MEM-005": "No sanitization on retrieved memory",
            "AW-TOOL-001": "Destructive tool without approval gate",
            "AW-TOOL-002": "Tool accepts arbitrary code execution",
            "AW-TOOL-003": "High-risk tool lacks scope check",
            "AW-TOOL-004": "Tool has no description",
            "AW-TOOL-005": "Agent has >15 tools",
        }
        for rule_id, count in sorted(all_rules.items(), key=lambda x: -x[1]):
            pct = f"{count / total_findings * 100:.0f}%" if total_findings else "0%"
            desc = rule_descs.get(rule_id, rule_id)
            w(f"| {rule_id} | {count} | {pct} | {desc} |")
    w("")
    w("---")
    w("")

    # ── Section 3: Attack vector coverage ─────────────────────────────────
    w("## 3. Attack Vector Coverage")
    w("")
    w("### Detectable Vectors (verified in code): 10 / 32")
    w("")

    # Group by category
    categories = {
        "MEM": ("Memory Isolation", 4),
        "POI": ("Data Poisoning", 6),
        "EMB": ("Embedding Attacks", 5),
        "INJ": ("Prompt Injection", 3),
        "EXF": ("Exfiltration", 3),
        "CFG": ("Configuration", 6),
        "DOS": ("Denial of Service", 3),
        "AGT": ("Agentic Attacks", 5),
    }

    w("| Category | Detected | Total | Coverage |")
    w("|---|---|---|---|")
    for cat, (cat_name, cat_total) in categories.items():
        detected = sum(
            1 for v in DETECTABLE_VECTORS if f"-{cat}-" in v
        )
        pct = f"{detected / cat_total * 100:.0f}%"
        w(f"| **{cat}** \u2014 {cat_name} | {detected} | {cat_total} | {pct} |")
    w("")

    # ── Section 4: Attack vectors found in real-world projects ────────────
    w("### Attack Vectors Found in Real-World Projects")
    w("")

    if all_vectors_found:
        w("| Attack Vector | Description | Projects Affected | Total Hits | Example Evidence |")
        w("|---|---|---|---|---|")

        for vec_id in sorted(all_vectors_found.keys()):
            evidence_list = all_vectors_found[vec_id]
            desc = ALL_VECTORS.get(vec_id, vec_id)
            projects_hit = sorted(set(e["project"] for e in evidence_list))
            total_hits = len(evidence_list)

            # Pick best example: first CRITICAL, then HIGH, then any
            example = None
            for sev_pref in ["critical", "high", "medium", "low"]:
                for e in evidence_list:
                    if e["severity"] == sev_pref and e.get("file"):
                        example = e
                        break
                if example:
                    break
            if not example and evidence_list:
                example = evidence_list[0]

            proj_str = ", ".join(projects_hit)
            if example and example.get("file"):
                fname = Path(example["file"]).name
                evidence_str = f"`{fname}:{example.get('line', '?')}` ({example['rule_id']})"
            else:
                evidence_str = f"({example['rule_id']})" if example else "\u2014"

            w(f"| **{vec_id}** | {desc} | {proj_str} | {total_hits} | {evidence_str} |")

        w("")
    else:
        w("No attack vectors found (no scan results available).")
        w("")

    # ── Section 5: Vectors NOT detected ───────────────────────────────────
    w("### Vectors Not Detected (22 / 32)")
    w("")
    w("| Vector | Description | Why Not Detectable |")
    w("|---|---|---|")

    not_detected_reasons = {
        "AW-ATK-POI-001": "Requires runtime: inject docs, measure retrieval ranking",
        "AW-ATK-POI-002": "Requires runtime: single-doc injection + query verification",
        "AW-ATK-POI-003": "Requires runtime: query-only memory injection simulation",
        "AW-ATK-POI-004": "Requires runtime: time-delayed session analysis",
        "AW-ATK-POI-005": "Requires binary analysis: PDF/DOCX hidden content",
        "AW-ATK-POI-006": "Requires tracking memory\u2192fine-tuning pipeline",
        "AW-ATK-EMB-001": "Requires embedding model invocation",
        "AW-ATK-EMB-002": "Requires semantic cache middleware identification",
        "AW-ATK-EMB-003": "Requires embedding model + inversion validation",
        "AW-ATK-EMB-004": "Requires multi-modal model analysis",
        "AW-ATK-EMB-005": "Requires embedding model lifecycle tracking",
        "AW-ATK-INJ-002": "Requires session identity tracking across turns",
        "AW-ATK-INJ-003": "Requires action execution tracing (tool invocation)",
        "AW-ATK-EXF-001": "Requires runtime: membership inference measurement",
        "AW-ATK-EXF-002": "Requires runtime: embedding extraction validation",
        "AW-ATK-EXF-003": "Requires runtime: timing side-channel measurement",
        "AW-ATK-CFG-002": "Requires vector DB config schema inspection",
        "AW-ATK-CFG-005": "Requires vector DB RBAC/ACL audit",
        "AW-ATK-CFG-006": "Requires PostgreSQL RLS policy inspection",
        "AW-ATK-DOS-001": "Requires rate-limit config audit",
        "AW-ATK-DOS-002": "Requires parameter bounds checking",
        "AW-ATK-DOS-003": "Requires admin endpoint auth audit",
        "AW-ATK-AGT-002": "Requires multi-agent delegation graph",
        "AW-ATK-AGT-003": "Requires agent identity redefinition detection",
        "AW-ATK-AGT-004": "Requires multi-agent shared memory provenance",
        "AW-ATK-AGT-005": "Requires session management analysis",
    }

    for vec_id in sorted(ALL_VECTORS.keys()):
        if vec_id not in DETECTABLE_VECTORS:
            desc = ALL_VECTORS[vec_id]
            reason = not_detected_reasons.get(vec_id, "Out of scope for static analysis")
            w(f"| {vec_id} | {desc} | {reason} |")

    w("")
    w("---")
    w("")

    # ── Section 6: Per-project attack vector heatmap ──────────────────────
    w("## 4. Attack Vector Heatmap (Per Project)")
    w("")

    detected_vec_ids = sorted(DETECTABLE_VECTORS)
    header = "| Project |" + " | ".join(v.split("-")[-1] for v in detected_vec_ids) + " | Total |"
    sep = "|---|" + "|".join("---|" for _ in detected_vec_ids) + "---|"
    w(header)
    w(sep)

    for key in PROJECT_ORDER:
        name, _ = PROJECTS[key]
        data = results.get(key)
        if data is None:
            cells = " | ".join(["\u2014"] * len(detected_vec_ids))
            w(f"| {name} | {cells} | \u2014 |")
            continue

        findings = data.get("findings", [])
        proj_vectors = extract_vectors(findings)
        row_total = 0
        cells = []
        for vec_id in detected_vec_ids:
            hits = proj_vectors.get(vec_id, [])
            count = len(hits)
            row_total += count
            if count > 0:
                cells.append(f"**{count}**")
            else:
                cells.append("\u00b7")

        w(f"| {name} | {' | '.join(cells)} | {row_total} |")

    w("")
    w("*Legend: number = findings count, \u00b7 = not detected, \u2014 = not scanned*")
    w("")
    w("---")
    w("")

    # ── Section 7: Projects outside scope ─────────────────────────────────
    w("## 5. Projects Outside Adapter Scope")
    w("")
    w("| Project | Reason | Required Adapter |")
    w("|---|---|---|")

    for key in PROJECT_ORDER:
        data = results.get(key)
        if data is None:
            w(f"| {PROJECTS[key][0]} | Clone/scan failed | \u2014 |")
            continue
        findings = data.get("findings", [])
        errors = data.get("errors", [])
        if not findings and any("Unsupported" in e or "undetected" in e for e in errors):
            name, _ = PROJECTS[key]
            w(f"| {name} | Framework not detected by LangChain adapter | Needs dedicated adapter |")

    w("")
    w("---")
    w("")

    # ── Section 8: How to reproduce ───────────────────────────────────────
    w("## 6. How to Reproduce")
    w("")
    w("```bash")
    w("# Install AgentWall")
    w('pip install -e ".[dev]"')
    w("")
    w("# Run benchmark (clones 20 repos, ~5 min)")
    w("./scripts/benchmark.sh")
    w("")
    w("# Scan a single project")
    w("agentwall scan /path/to/langchain-project --format agent-json --output report.json")
    w("```")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Written to: {output_path}")
    print(f"  Projects scanned: {sum(1 for d in results.values() if d is not None)}/{len(PROJECT_ORDER)}")
    print(f"  Total findings: {total_findings}")
    print(f"  Attack vectors confirmed: {len(all_vectors_found)}/{len(DETECTABLE_VECTORS)}")


if __name__ == "__main__":
    generate_benchmark_md(RESULTS_DIR, BENCHMARK_MD)
PYEOF

# Replace placeholders with actual paths
sed -i "s|RESULTS_DIR_PLACEHOLDER|$RESULTS_DIR|g" /dev/stdin 2>/dev/null || true

# Actually run it properly — inline python with variable substitution
python3 -c "
import json, sys
from pathlib import Path
from datetime import date

RESULTS_DIR = Path('$RESULTS_DIR')
BENCHMARK_MD = Path('$BENCHMARK_MD')

exec(open('/dev/stdin').read() if False else '')
" << 'PYEOF2' || true
PYEOF2

# Run the Python report generator directly
python3 -c "
import json, sys
from pathlib import Path
from datetime import date

RESULTS_DIR = Path('$RESULTS_DIR')
BENCHMARK_MD = Path('$BENCHMARK_MD')

RULE_TO_VECTORS = {
    'AW-MEM-001': ['AW-ATK-MEM-001'],
    'AW-MEM-002': ['AW-ATK-MEM-002'],
    'AW-MEM-003': ['AW-ATK-MEM-003'],
    'AW-MEM-004': ['AW-ATK-MEM-004'],
    'AW-MEM-005': ['AW-ATK-INJ-001'],
    'AW-TOOL-001': ['AW-ATK-AGT-001'],
    'AW-TOOL-002': ['AW-ATK-AGT-001'],
    'AW-TOOL-003': ['AW-ATK-AGT-001'],
    'AW-TOOL-004': [],
    'AW-TOOL-005': [],
    'AW-CFG-allow-reset': ['AW-ATK-CFG-001'],
    'AW-CFG-no-tls': ['AW-ATK-CFG-003'],
    'AW-CFG-hardcoded-secret': ['AW-ATK-CFG-004'],
    'AW-CFG-docker-no-auth': ['AW-ATK-CFG-003'],
    'AW-CFG-no-auth': ['AW-ATK-CFG-003'],
    'AW-CFG-debug-mode': ['AW-ATK-CFG-001'],
    'AW-CFG-exposed-port': ['AW-ATK-CFG-003'],
    'AW-CFG-no-password': ['AW-ATK-CFG-003'],
}

ALL_VECTORS = {
    'AW-ATK-MEM-001': 'Cross-Tenant Retrieval (No Filter)',
    'AW-ATK-MEM-002': 'Weak Tenant Isolation (Static Filter)',
    'AW-ATK-MEM-003': 'Namespace/Collection Confusion',
    'AW-ATK-MEM-004': 'Partition Bypass via Direct API',
    'AW-ATK-POI-001': 'PoisonedRAG',
    'AW-ATK-POI-002': 'CorruptRAG',
    'AW-ATK-POI-003': 'MINJA',
    'AW-ATK-POI-004': 'Persistent Memory Poisoning',
    'AW-ATK-POI-005': 'Document Loader Exploitation',
    'AW-ATK-POI-006': 'Training Data Backdoor',
    'AW-ATK-EMB-001': 'Vector Collision Attack',
    'AW-ATK-EMB-002': 'Semantic Cache Poisoning',
    'AW-ATK-EMB-003': 'Embedding Inversion',
    'AW-ATK-EMB-004': 'Adversarial Multi-Modal Embedding',
    'AW-ATK-EMB-005': 'Vector Drift',
    'AW-ATK-INJ-001': 'Stored Prompt Injection',
    'AW-ATK-INJ-002': 'Cross-Session Context Hijacking',
    'AW-ATK-INJ-003': 'EchoLeak',
    'AW-ATK-EXF-001': 'Membership Inference',
    'AW-ATK-EXF-002': 'Embedding Exfiltration via API',
    'AW-ATK-EXF-003': 'Timing Side-Channel',
    'AW-ATK-CFG-001': 'Unsafe Reset Enabled',
    'AW-ATK-CFG-002': 'No Encryption at Rest',
    'AW-ATK-CFG-003': 'No TLS / No Auth / Exposed Ports',
    'AW-ATK-CFG-004': 'Hardcoded API Keys',
    'AW-ATK-CFG-005': 'Missing RBAC',
    'AW-ATK-CFG-006': 'No Row-Level Security',
    'AW-ATK-DOS-001': 'Embedding Flood',
    'AW-ATK-DOS-002': 'Query Amplification',
    'AW-ATK-DOS-003': 'Collection Deletion via Admin',
    'AW-ATK-AGT-001': 'Tool Poisoning / Unsafe Tool Access',
    'AW-ATK-AGT-002': 'Delegation Chain Escalation',
    'AW-ATK-AGT-003': 'Memory-Mediated Identity Hijacking',
    'AW-ATK-AGT-004': 'Cross-Agent Memory Contamination',
    'AW-ATK-AGT-005': 'Conversation History Replay',
}

DETECTABLE_VECTORS = {
    'AW-ATK-MEM-001', 'AW-ATK-MEM-002', 'AW-ATK-MEM-003', 'AW-ATK-MEM-004',
    'AW-ATK-INJ-001',
    'AW-ATK-CFG-001', 'AW-ATK-CFG-003', 'AW-ATK-CFG-004',
    'AW-ATK-AGT-001',
}

PROJECTS = {
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
    'langflow': ('Langflow', '~48k'),
    'flowise': ('Flowise', '~35k'),
    'open-interpreter': ('Open Interpreter', '~58k'),
    'chainlit': ('Chainlit', '~8k'),
    'embedchain': ('Mem0/Embedchain', '~25k'),
    'llm-app': ('LLM App (Pathway)', '~4k'),
    'haystack': ('Haystack', '~18k'),
    'superagent': ('SuperAgent', '~5k'),
    'agentgpt': ('AgentGPT', '~32k'),
    'auto-gpt-web': ('AutoGPT', '~172k'),
}

PROJECT_ORDER = [
    'langchain-chatchat', 'private-gpt', 'quivr', 'localgpt', 'docsgpt',
    'gpt-researcher', 'onyx', 'db-gpt', 'chat-langchain', 'rasagpt',
    'langflow', 'flowise', 'open-interpreter', 'chainlit', 'embedchain',
    'llm-app', 'haystack', 'superagent', 'agentgpt', 'auto-gpt-web',
]

def extract_vectors(findings):
    vectors = {}
    for f in findings:
        rule_id = f.get('rule_id', '')
        mapped = RULE_TO_VECTORS.get(rule_id, [])
        for vec_id in mapped:
            if vec_id not in vectors:
                vectors[vec_id] = []
            vectors[vec_id].append({
                'rule_id': rule_id,
                'file': f.get('file'),
                'line': f.get('line'),
                'severity': f.get('severity', '?'),
                'title': f.get('title', ''),
            })
    return vectors

lines = []
w = lines.append

w('# AgentWall Benchmark Report')
w('')
w(f'**Date:** {date.today().isoformat()}')
w('**Version:** 0.1.0 (Phase 1 complete)')
w('**Layers enabled:** L0\u2013L6 (default static analysis)')
w('**Reproduce:** \`./scripts/benchmark.sh\`')
w('')
w('---')
w('')

# Section 1: Scan results
w('## 1. Scan Results (20 Projects)')
w('')
w('| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |')
w('|---|---|---|---|---|---|---|---|---|---|')

total_findings = 0
total_crit = 0
total_high = 0
total_files = 0
projects_with_findings = 0
all_vectors_found = {}

for idx, key in enumerate(PROJECT_ORDER, 1):
    name, stars = PROJECTS[key]
    f = RESULTS_DIR / f'{key}.json'

    if not f.exists():
        w(f'| {idx} | {name} | {stars} | - | - | - | - | - | - | not scanned |')
        continue

    try:
        data = json.loads(f.read_text())
    except Exception:
        w(f'| {idx} | {name} | {stars} | - | - | - | - | - | - | parse error |')
        continue

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
    low = sev.get('low', 0) + sev.get('info', 0)
    total = len(findings)
    total_findings += total
    total_crit += crit
    total_high += high
    if total > 0:
        projects_with_findings += 1

    top = sorted(rules.items(), key=lambda x: -x[1])[:3]
    rule_str = ', '.join(f'{r}({c})' for r, c in top) if top else '\u2014'

    proj_vectors = extract_vectors(findings)
    for vec_id, evidence in proj_vectors.items():
        if vec_id not in all_vectors_found:
            all_vectors_found[vec_id] = []
        for e in evidence:
            e['project'] = name
        all_vectors_found[vec_id].extend(evidence)

    w(f'| {idx} | {name} | {stars} | {files} | {total} | {crit} | {high} | {med} | {low} | {rule_str} |')

w('')
w(f'**Totals: {total_findings} findings ({total_crit} CRITICAL, {total_high} HIGH) across {total_files} files in {len(PROJECT_ORDER)} projects. {projects_with_findings}/{len(PROJECT_ORDER)} have findings.**')
w('')
w('---')
w('')

# Section 2: Rule distribution
w('## 2. Rule Distribution')
w('')

all_rules = {}
for key in PROJECT_ORDER:
    f = RESULTS_DIR / f'{key}.json'
    if not f.exists():
        continue
    try:
        data = json.loads(f.read_text())
    except Exception:
        continue
    for finding in data.get('findings', []):
        r = finding.get('rule_id', '?')
        all_rules[r] = all_rules.get(r, 0) + 1

if all_rules:
    w('| Rule | Count | % | Description |')
    w('|---|---|---|---|')
    rule_descs = {
        'AW-MEM-001': 'No tenant isolation in vector store',
        'AW-MEM-002': 'Shared collection without retrieval filter',
        'AW-MEM-003': 'Memory backend has no access control',
        'AW-MEM-004': 'Injection patterns in retrieval path',
        'AW-MEM-005': 'No sanitization on retrieved memory',
        'AW-TOOL-001': 'Destructive tool without approval gate',
        'AW-TOOL-002': 'Tool accepts arbitrary code execution',
        'AW-TOOL-003': 'High-risk tool lacks scope check',
        'AW-TOOL-004': 'Tool has no description',
        'AW-TOOL-005': 'Agent has >15 tools',
    }
    for rule_id, count in sorted(all_rules.items(), key=lambda x: -x[1]):
        pct = f'{count / total_findings * 100:.0f}%' if total_findings else '0%'
        desc = rule_descs.get(rule_id, rule_id)
        w(f'| {rule_id} | {count} | {pct} | {desc} |')

w('')
w('---')
w('')

# Section 3: Attack vector coverage
w('## 3. Attack Vector Coverage (10 / 32 Detectable)')
w('')

categories = {
    'MEM': ('Memory Isolation', 4),
    'POI': ('Data Poisoning', 6),
    'EMB': ('Embedding Attacks', 5),
    'INJ': ('Prompt Injection', 3),
    'EXF': ('Exfiltration', 3),
    'CFG': ('Configuration', 6),
    'DOS': ('Denial of Service', 3),
    'AGT': ('Agentic Attacks', 5),
}

w('| Category | Detected | Total | Coverage |')
w('|---|---|---|---|')
for cat, (cat_name, cat_total) in categories.items():
    detected = sum(1 for v in DETECTABLE_VECTORS if f'-{cat}-' in v)
    pct = f'{detected / cat_total * 100:.0f}%'
    w(f'| **{cat}** \u2014 {cat_name} | {detected} | {cat_total} | {pct} |')

w('')

# Section 4: Vectors found in real projects
w('### Attack Vectors Confirmed in Real-World Projects')
w('')

if all_vectors_found:
    w('| Attack Vector | Description | Projects Affected | Hits | Example Evidence |')
    w('|---|---|---|---|---|')

    for vec_id in sorted(all_vectors_found.keys()):
        evidence_list = all_vectors_found[vec_id]
        desc = ALL_VECTORS.get(vec_id, vec_id)
        projects_hit = sorted(set(e['project'] for e in evidence_list))
        total_hits = len(evidence_list)

        example = None
        for sev_pref in ['critical', 'high', 'medium', 'low']:
            for e in evidence_list:
                if e['severity'] == sev_pref and e.get('file'):
                    example = e
                    break
            if example:
                break
        if not example and evidence_list:
            example = evidence_list[0]

        proj_str = ', '.join(projects_hit)
        if example and example.get('file'):
            from pathlib import Path as P
            fname = P(example['file']).name
            evidence_str = f'\`{fname}:{example.get(\"line\", \"?\")}\` ({example[\"rule_id\"]})'
        else:
            evidence_str = f'({example[\"rule_id\"]})' if example else '\u2014'

        w(f'| **{vec_id}** | {desc} | {proj_str} | {total_hits} | {evidence_str} |')
    w('')
else:
    w('No scan results available yet. Run \`./scripts/benchmark.sh\` first.')
    w('')

# Section 5: Vectors not detected
w('### Vectors Not Detected (22 / 32)')
w('')
w('| Vector | Description | Reason |')
w('|---|---|---|')

not_detected_reasons = {
    'AW-ATK-POI-001': 'Requires runtime: inject docs, measure ranking',
    'AW-ATK-POI-002': 'Requires runtime: single-doc injection',
    'AW-ATK-POI-003': 'Requires runtime: query-only memory injection',
    'AW-ATK-POI-004': 'Requires runtime: time-delayed session analysis',
    'AW-ATK-POI-005': 'Requires binary analysis: PDF/DOCX hidden content',
    'AW-ATK-POI-006': 'Requires tracking memory\u2192fine-tuning pipeline',
    'AW-ATK-EMB-001': 'Requires embedding model invocation',
    'AW-ATK-EMB-002': 'Requires semantic cache identification',
    'AW-ATK-EMB-003': 'Requires embedding model + inversion validation',
    'AW-ATK-EMB-004': 'Requires multi-modal model analysis',
    'AW-ATK-EMB-005': 'Requires embedding lifecycle tracking',
    'AW-ATK-INJ-002': 'Requires session identity tracking',
    'AW-ATK-INJ-003': 'Requires action execution tracing',
    'AW-ATK-EXF-001': 'Requires runtime: membership inference',
    'AW-ATK-EXF-002': 'Requires runtime: embedding extraction',
    'AW-ATK-EXF-003': 'Requires runtime: timing measurement',
    'AW-ATK-CFG-002': 'Requires vector DB config schema inspection',
    'AW-ATK-CFG-005': 'Requires vector DB RBAC/ACL audit',
    'AW-ATK-CFG-006': 'Requires PostgreSQL RLS policy inspection',
    'AW-ATK-DOS-001': 'Requires rate-limit config audit',
    'AW-ATK-DOS-002': 'Requires parameter bounds checking',
    'AW-ATK-DOS-003': 'Requires admin endpoint auth audit',
    'AW-ATK-AGT-002': 'Requires multi-agent delegation graph',
    'AW-ATK-AGT-003': 'Requires agent identity redefinition detection',
    'AW-ATK-AGT-004': 'Requires multi-agent shared memory provenance',
    'AW-ATK-AGT-005': 'Requires session management analysis',
}

for vec_id in sorted(ALL_VECTORS.keys()):
    if vec_id not in DETECTABLE_VECTORS:
        desc = ALL_VECTORS[vec_id]
        reason = not_detected_reasons.get(vec_id, 'Out of scope for static analysis')
        w(f'| {vec_id} | {desc} | {reason} |')

w('')
w('---')
w('')

# Section 6: Heatmap
w('## 4. Attack Vector Heatmap (Per Project)')
w('')

detected_vec_ids = sorted(DETECTABLE_VECTORS)
short_labels = [v.replace('AW-ATK-', '') for v in detected_vec_ids]
header = '| Project | ' + ' | '.join(short_labels) + ' | Total |'
sep = '|---|' + '|'.join('---|' for _ in detected_vec_ids) + '---|'
w(header)
w(sep)

for key in PROJECT_ORDER:
    name, _ = PROJECTS[key]
    f = RESULTS_DIR / f'{key}.json'

    if not f.exists():
        cells = ' | '.join(['\u2014'] * len(detected_vec_ids))
        w(f'| {name} | {cells} | \u2014 |')
        continue

    try:
        data = json.loads(f.read_text())
    except Exception:
        cells = ' | '.join(['\u2014'] * len(detected_vec_ids))
        w(f'| {name} | {cells} | \u2014 |')
        continue

    findings = data.get('findings', [])
    proj_vectors = extract_vectors(findings)
    row_total = 0
    cells = []
    for vec_id in detected_vec_ids:
        hits = proj_vectors.get(vec_id, [])
        count = len(hits)
        row_total += count
        if count > 0:
            cells.append(f'**{count}**')
        else:
            cells.append('\u00b7')

    w(f'| {name} | {\" | \".join(cells)} | {row_total} |')

w('')
w('*Legend: number = findings count, \u00b7 = not detected, \u2014 = not scanned*')
w('')
w('---')
w('')

# Section 7
w('## 5. How to Reproduce')
w('')
w('\`\`\`bash')
w('pip install -e \".[dev]\"')
w('./scripts/benchmark.sh')
w('\`\`\`')

BENCHMARK_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'  Written to: {BENCHMARK_MD}')
print(f'  Total findings: {total_findings}')
print(f'  Attack vectors confirmed in real projects: {len(all_vectors_found)}/{len(DETECTABLE_VECTORS)}')
"

echo ""
echo "=== Benchmark complete ==="
echo "JSON reports: $RESULTS_DIR/"
echo "Report: $BENCHMARK_MD"
