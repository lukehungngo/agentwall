#!/usr/bin/env bash
# AgentWall Benchmark 3000 — comprehensive scan of 150+ AI agent projects
# Usage: ./scripts/benchmark3000.sh [targets_dir] [results_dir]
#
# Massively expanded version of benchmark.sh. Clones projects (shallow),
# runs agentwall scan on each, maps findings to attack vectors, and
# generates BENCHMARK3000.md.

set -euo pipefail

TARGETS_DIR="${1:-/tmp/agentwall-bench3k}"
RESULTS_DIR="${2:-/tmp/agentwall-results3k}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BENCHMARK_MD="$PROJECT_ROOT/BENCHMARK3000.md"
LOG_DIR="$PROJECT_ROOT/logs"
RUN_TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
RUN_LOG="$LOG_DIR/benchmark3k_${RUN_TIMESTAMP}.log"
MAX_PARALLEL="${MAX_PARALLEL:-4}"       # parallel clone jobs
SCAN_TIMEOUT="${SCAN_TIMEOUT:-300}"     # per-project scan timeout (seconds)

mkdir -p "$TARGETS_DIR" "$RESULTS_DIR" "$LOG_DIR"

# Start run log
{
  echo "═══════════════════════════════════════════════════════"
  echo "AgentWall Benchmark 3000 — $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "═══════════════════════════════════════════════════════"
  echo "Targets: $TARGETS_DIR"
  echo "Results: $RESULTS_DIR"
  echo "Max parallel clones: $MAX_PARALLEL"
  echo "Scan timeout: ${SCAN_TIMEOUT}s"
  echo "AgentWall version: $(agentwall version 2>/dev/null || echo 'unknown')"
  echo ""
} > "$RUN_LOG"

# ══════════════════════════════════════════════════════════════════════════
# Repository Registry
# ══════════════════════════════════════════════════════════════════════════
# Format: REPO_NAMES[] for order, REPOS[] for URLs, REPO_META[] for display

REPO_NAMES=()

declare -A REPOS
declare -A REPO_META        # "display_name|stars|category"
declare -A FORCE_FRAMEWORK

# Helper: register a repo
reg() {
  local key="$1" url="$2" display="$3" stars="$4" category="$5"
  REPO_NAMES+=("$key")
  REPOS[$key]="$url"
  REPO_META[$key]="$display|$stars|$category"
}

# ── Tier 1: Established LangChain ecosystem (>2k stars) ─────────────────

reg langchain-chatchat "https://github.com/chatchat-space/Langchain-Chatchat.git" \
    "Langchain-Chatchat" "~37k" "tier1-langchain"
reg private-gpt "https://github.com/zylon-ai/private-gpt.git" \
    "PrivateGPT" "~54k" "tier1-langchain"
reg quivr "https://github.com/QuivrHQ/quivr.git" \
    "Quivr" "~36k" "tier1-langchain"
reg localgpt "https://github.com/PromtEngineer/localGPT.git" \
    "LocalGPT" "~22k" "tier1-langchain"
reg docsgpt "https://github.com/arc53/DocsGPT.git" \
    "DocsGPT" "~15k" "tier1-langchain"
reg gpt-researcher "https://github.com/assafelovic/gpt-researcher.git" \
    "GPT-Researcher" "~17k" "tier1-langchain"
reg onyx "https://github.com/onyx-dot-app/onyx.git" \
    "Onyx/Danswer" "~12k" "tier1-langchain"
reg db-gpt "https://github.com/eosphoros-ai/DB-GPT.git" \
    "DB-GPT" "~17k" "tier1-langchain"
reg chat-langchain "https://github.com/langchain-ai/chat-langchain.git" \
    "Chat-LangChain" "~6k" "tier1-langchain"
reg rasagpt "https://github.com/paulpierre/RasaGPT.git" \
    "RasaGPT" "~2.4k" "tier1-langchain"
reg langflow "https://github.com/langflow-ai/langflow.git" \
    "Langflow" "~48k" "tier1-langchain"
reg flowise "https://github.com/FlowiseAI/Flowise.git" \
    "Flowise" "~35k" "tier1-langchain"
reg open-interpreter "https://github.com/OpenInterpreter/open-interpreter.git" \
    "Open Interpreter" "~58k" "tier1-langchain"
reg chainlit "https://github.com/Chainlit/chainlit.git" \
    "Chainlit" "~8k" "tier1-langchain"
reg embedchain "https://github.com/mem0ai/mem0.git" \
    "Mem0/Embedchain" "~48k" "tier1-langchain"
reg llm-app "https://github.com/pathwaycom/llm-app.git" \
    "LLM App (Pathway)" "~4k" "tier1-langchain"
reg haystack "https://github.com/deepset-ai/haystack.git" \
    "Haystack" "~18k" "tier1-langchain"
reg superagent "https://github.com/superagent-ai/superagent.git" \
    "SuperAgent" "~5k" "tier1-langchain"
reg agentgpt "https://github.com/reworkd/AgentGPT.git" \
    "AgentGPT" "~32k" "tier1-langchain"
reg auto-gpt-web "https://github.com/Significant-Gravitas/AutoGPT.git" \
    "AutoGPT" "~172k" "tier1-langchain"

# ── Tier 1 expanded: LangChain ecosystem ────────────────────────────────

reg langgraph "https://github.com/langchain-ai/langgraph.git" \
    "LangGraph" "~45k" "tier1-langchain"
reg langsmith-sdk "https://github.com/langchain-ai/langsmith-sdk.git" \
    "LangSmith SDK" "~1k" "tier1-langchain"
reg langchain-mono "https://github.com/langchain-ai/langchain.git" \
    "LangChain (mono)" "~100k" "tier1-langchain"
reg opengpts "https://github.com/langchain-ai/opengpts.git" \
    "OpenGPTs" "~6k" "tier1-langchain"
reg langserve "https://github.com/langchain-ai/langserve.git" \
    "LangServe" "~2k" "tier1-langchain"
reg langchain-extract "https://github.com/langchain-ai/langchain-extract.git" \
    "LangChain Extract" "~1k" "tier1-langchain"
reg awesome-llm-apps "https://github.com/Shubhamsaboo/awesome-llm-apps.git" \
    "Awesome LLM Apps" "~60k" "tier1-langchain"

# ── LlamaIndex ecosystem ────────────────────────────────────────────────

reg llama-index "https://github.com/run-llama/llama_index.git" \
    "LlamaIndex" "~47k" "llamaindex"
reg rags-llamaindex "https://github.com/run-llama/rags.git" \
    "RAGS (LlamaIndex)" "~6k" "llamaindex"
reg llama-parse "https://github.com/run-llama/llama_parse.git" \
    "LlamaParse" "~3k" "llamaindex"
reg create-llama "https://github.com/run-llama/create-llama.git" \
    "create-llama" "~2k" "llamaindex"
reg sec-insights "https://github.com/run-llama/sec-insights.git" \
    "SEC Insights" "~2k" "llamaindex"

# ── Multi-agent frameworks ──────────────────────────────────────────────

reg crewai "https://github.com/crewAIInc/crewAI.git" \
    "CrewAI" "~46k" "multi-agent"
reg autogen "https://github.com/microsoft/autogen.git" \
    "AutoGen" "~48k" "multi-agent"
reg metagpt "https://github.com/geekan/MetaGPT.git" \
    "MetaGPT" "~58k" "multi-agent"
reg chatdev "https://github.com/OpenBMB/ChatDev.git" \
    "ChatDev" "~25k" "multi-agent"
reg camel "https://github.com/camel-ai/camel.git" \
    "CAMEL" "~10k" "multi-agent"
reg babyagi "https://github.com/yoheinakajima/babyagi.git" \
    "BabyAGI" "~20k" "multi-agent"
reg openai-swarm "https://github.com/openai/swarm.git" \
    "OpenAI Swarm" "~18k" "multi-agent"
reg swarms "https://github.com/kyegomez/swarms.git" \
    "Swarms" "~4k" "multi-agent"
reg taskweaver "https://github.com/microsoft/TaskWeaver.git" \
    "TaskWeaver" "~5k" "multi-agent"

# ── RAG applications ────────────────────────────────────────────────────

reg ragflow "https://github.com/infiniflow/ragflow.git" \
    "RAGFlow" "~70k" "rag-app"
reg kotaemon "https://github.com/Cinnamon/kotaemon.git" \
    "Kotaemon" "~25k" "rag-app"
reg lightrag "https://github.com/HKUDS/LightRAG.git" \
    "LightRAG" "~30k" "rag-app"
reg fastgpt "https://github.com/labring/FastGPT.git" \
    "FastGPT" "~27k" "rag-app"
reg qanything "https://github.com/netease-youdao/QAnything.git" \
    "QAnything" "~12k" "rag-app"
reg r2r "https://github.com/SciPhi-AI/R2R.git" \
    "R2R" "~4k" "rag-app"
reg flashrag "https://github.com/RUC-NLPIR/FlashRAG.git" \
    "FlashRAG" "~2k" "rag-app"
reg autorag "https://github.com/Marker-Inc-Korea/AutoRAG.git" \
    "AutoRAG" "~3k" "rag-app"
reg canopy "https://github.com/pinecone-io/canopy.git" \
    "Canopy (Pinecone)" "~3k" "rag-app"
reg verba "https://github.com/weaviate/Verba.git" \
    "Verba (Weaviate)" "~6k" "rag-app"
reg vanna "https://github.com/vanna-ai/vanna.git" \
    "Vanna" "~13k" "rag-app"
reg cognita "https://github.com/truefoundry/cognita.git" \
    "Cognita" "~8k" "rag-app"
reg chatgpt-retrieval-plugin "https://github.com/openai/chatgpt-retrieval-plugin.git" \
    "ChatGPT Retrieval Plugin" "~21k" "rag-app"
reg txtai "https://github.com/neuml/txtai.git" \
    "txtai" "~10k" "rag-app"

# ── Vector store ecosystems ─────────────────────────────────────────────

reg chromadb "https://github.com/chroma-core/chroma.git" \
    "ChromaDB" "~17k" "vector-store"
reg milvus-bootcamp "https://github.com/milvus-io/bootcamp.git" \
    "Milvus Bootcamp" "~2k" "vector-store"
reg qdrant-examples "https://github.com/qdrant/examples.git" \
    "Qdrant Examples" "~500" "vector-store"
reg lancedb "https://github.com/lancedb/lancedb.git" \
    "LanceDB" "~5k" "vector-store"

# ── Memory / knowledge graph systems ───────────────────────────────────

reg cognee "https://github.com/topoteretes/cognee.git" \
    "Cognee" "~12k" "memory-knowledge"
reg graphiti "https://github.com/getzep/graphiti.git" \
    "Graphiti (Zep)" "~14k" "memory-knowledge"
reg letta "https://github.com/letta-ai/letta.git" \
    "Letta (MemGPT)" "~22k" "memory-knowledge"
reg graphrag "https://github.com/microsoft/graphrag.git" \
    "GraphRAG (Microsoft)" "~22k" "memory-knowledge"
reg nano-graphrag "https://github.com/gusye1234/nano-graphrag.git" \
    "nano-graphrag" "~5k" "memory-knowledge"
reg zep "https://github.com/getzep/zep.git" \
    "Zep" "~3k" "memory-knowledge"

# ── Chatbot / assistant frameworks ──────────────────────────────────────

reg open-webui "https://github.com/open-webui/open-webui.git" \
    "Open WebUI" "~124k" "chatbot-assistant"
reg librechat "https://github.com/danny-avila/LibreChat.git" \
    "LibreChat" "~30k" "chatbot-assistant"
reg khoj "https://github.com/khoj-ai/khoj.git" \
    "Khoj" "~33k" "chatbot-assistant"
reg anything-llm "https://github.com/Mintplex-Labs/anything-llm.git" \
    "AnythingLLM" "~35k" "chatbot-assistant"
reg py-gpt "https://github.com/szczyglis-dev/py-gpt.git" \
    "PyGPT" "~3k" "chatbot-assistant"
reg jan "https://github.com/janhq/jan.git" \
    "Jan" "~25k" "chatbot-assistant"

# ── Code / dev agents ───────────────────────────────────────────────────

reg openhands "https://github.com/All-Hands-AI/OpenHands.git" \
    "OpenHands (OpenDevin)" "~65k" "code-dev-agent"
reg swe-agent "https://github.com/SWE-agent/SWE-agent.git" \
    "SWE-agent" "~15k" "code-dev-agent"
reg aider "https://github.com/Aider-AI/aider.git" \
    "Aider" "~36k" "code-dev-agent"
reg devika "https://github.com/stitionai/devika.git" \
    "Devika" "~18k" "code-dev-agent"
reg gpt-engineer "https://github.com/gpt-engineer-org/gpt-engineer.git" \
    "GPT-Engineer" "~52k" "code-dev-agent"
reg gpt-pilot "https://github.com/Pythagora-io/gpt-pilot.git" \
    "GPT-Pilot" "~32k" "code-dev-agent"

# ── Production agent platforms ──────────────────────────────────────────

reg dify "https://github.com/langgenius/dify.git" \
    "Dify" "~129k" "production-platform"
reg agno "https://github.com/agno-agi/agno.git" \
    "Agno (Phidata)" "~19k" "production-platform"
reg pydantic-ai "https://github.com/pydantic/pydantic-ai.git" \
    "Pydantic AI" "~15k" "production-platform"
reg smolagents "https://github.com/huggingface/smolagents.git" \
    "smolagents (HF)" "~26k" "production-platform"
reg semantic-kernel "https://github.com/microsoft/semantic-kernel.git" \
    "Semantic Kernel" "~22k" "production-platform"
reg openai-agents-sdk "https://github.com/openai/openai-agents-python.git" \
    "OpenAI Agents SDK" "~7k" "production-platform"
reg dspy "https://github.com/stanfordnlp/dspy.git" \
    "DSPy" "~20k" "production-platform"
reg google-adk "https://github.com/google/adk-python.git" \
    "Google Agent Dev Kit" "~18k" "production-platform"
reg ufo "https://github.com/microsoft/UFO.git" \
    "UFO (Microsoft)" "~5k" "production-platform"
reg agentops "https://github.com/AgentOps-AI/agentops.git" \
    "AgentOps" "~3k" "production-platform"
reg modelscope-agent "https://github.com/modelscope/modelscope-agent.git" \
    "ModelScope Agent" "~3k" "production-platform"

# ── Tier 2: Small projects (<500 stars) — original ──────────────────────

reg memory-agent "https://github.com/langchain-ai/memory-agent.git" \
    "memory-agent" "416" "tier2-small"
reg rag-research-agent "https://github.com/langchain-ai/rag-research-agent-template.git" \
    "rag-research-agent-template" "295" "tier2-small"
reg langchain-chatbot "https://github.com/shashankdeshpande/langchain-chatbot.git" \
    "langchain-chatbot" "273" "tier2-small"
reg chat-with-websites "https://github.com/alejandro-ao/chat-with-websites.git" \
    "chat-with-websites" "260" "tier2-small"
reg cohere-qdrant-retrieval "https://github.com/menloparklab/langchain-cohere-qdrant-doc-retrieval.git" \
    "cohere-qdrant-doc-retrieval" "152" "tier2-small"
reg rag-chatbot-langchain "https://github.com/AlaGrine/RAG_chatabot_with_Langchain.git" \
    "RAG-chatbot-langchain" "133" "tier2-small"
reg langchain-rag-chroma "https://github.com/romilandc/langchain-RAG.git" \
    "langchain-RAG-chroma" "8" "tier2-small"
reg chat-with-pdf "https://github.com/ashutoshvct/chat-with-pdf.git" \
    "chat-with-pdf" "2" "tier2-small"
reg langchain-multi-agent "https://github.com/Hegazy360/langchain-multi-agent.git" \
    "langchain-multi-agent" "10" "tier2-small"
reg objectbox-rag "https://github.com/NebeyouMusie/End-to-End-RAG-Project-using-ObjectBox-and-LangChain.git" \
    "objectbox-rag" "10" "tier2-small"

# ── Tier 2 expanded: More small/niche projects ─────────────────────────

reg adalflow "https://github.com/SylphAI-Inc/AdalFlow.git" \
    "AdalFlow" "~3k" "tier2-small"
reg hindsight "https://github.com/palisaderesearch/hindsight.git" \
    "Hindsight" "~4k" "tier2-small"
reg vector-admin "https://github.com/Mintplex-Labs/vector-admin.git" \
    "Vector Admin" "~2k" "tier2-small"
reg agents-course "https://github.com/huggingface/agents-course.git" \
    "HF Agents Course" "~5k" "tier2-small"
reg libre-chat "https://github.com/vemonet/libre-chat.git" \
    "Libre Chat" "~500" "tier2-small"
reg langgraph-bigtool "https://github.com/langchain-ai/langgraph-bigtool.git" \
    "LangGraph BigTool" "~500" "tier2-small"
reg rag-anything "https://github.com/HKUDS/RAG-Anything.git" \
    "RAG-Anything" "~1k" "tier2-small"
reg camel-oasis "https://github.com/camel-ai/oasis.git" \
    "OASIS (CAMEL)" "~2k" "tier2-small"
reg swe-bench "https://github.com/SWE-bench/SWE-bench.git" \
    "SWE-bench" "~4k" "tier2-small"

# ── Force framework overrides ───────────────────────────────────────────

FORCE_FRAMEWORK=(
  [localgpt]="langchain"
  [private-gpt]="langchain"
  [embedchain]="langchain"
  [llm-app]="langchain"
  [superagent]="langchain"
  [chat-with-pdf]="langchain"
  [objectbox-rag]="langchain"
  [cohere-qdrant-retrieval]="langchain"
  [langchain-rag-chroma]="langchain"
  [rag-chatbot-langchain]="langchain"
  [canopy]="langchain"
  [libre-chat]="llamaindex"
)

TOTAL_REPOS=${#REPO_NAMES[@]}
echo "=== AgentWall Benchmark 3000 ==="
echo "    $TOTAL_REPOS repositories registered"
echo ""

# ── Clone (parallel) ────────────────────────────────────────────────────

echo "=== Phase 1: Cloning projects (max $MAX_PARALLEL parallel) ==="
clone_count=0
clone_skip=0
clone_fail=0
job_count=0

for name in "${REPO_NAMES[@]}"; do
  dir="$TARGETS_DIR/$name"
  if [ -d "$dir" ]; then
    ((clone_skip++)) || true
    continue
  fi

  # Run clone in background, limit parallelism
  (
    git clone --depth 1 --single-branch "${REPOS[$name]}" "$dir" 2>/dev/null \
      && echo "  ✓ $name" \
      || echo "  ✗ $name (clone failed)"
  ) &
  ((job_count++)) || true

  if (( job_count >= MAX_PARALLEL )); then
    wait -n 2>/dev/null || wait
    ((job_count--)) || true
  fi
done

# Wait for remaining clone jobs
wait
echo "  Cloned: new=$((TOTAL_REPOS - clone_skip)), cached=$clone_skip"
echo ""

# ── Scan ─────────────────────────────────────────────────────────────────

echo "=== Phase 2: Scanning $TOTAL_REPOS projects ==="
scan_done=0
scan_fail=0
scan_skip=0

for name in "${REPO_NAMES[@]}"; do
  dir="$TARGETS_DIR/$name"
  out="$RESULTS_DIR/$name.json"

  if [ ! -d "$dir" ]; then
    echo "  $name: skipped (not cloned)"
    ((scan_skip++)) || true
    continue
  fi

  # Skip if already scanned (idempotent reruns)
  if [ -f "$out" ] && [ -s "$out" ]; then
    echo "  $name: cached"
    ((scan_done++)) || true
    continue
  fi

  echo -n "  [$((scan_done + scan_fail + scan_skip + 1))/$TOTAL_REPOS] $name: scanning..."

  fw_flag=""
  if [[ -v "FORCE_FRAMEWORK[$name]" ]]; then
    fw_flag="--framework ${FORCE_FRAMEWORK[$name]}"
  fi

  scan_start="$(date +%s)"
  # shellcheck disable=SC2086
  if timeout "$SCAN_TIMEOUT" agentwall scan "$dir" $fw_flag --fail-on none --confidence medium --output "$out" >/dev/null 2>&1; then
    scan_exit=0
    echo " done"
  else
    scan_exit=$?
    if [ "$scan_exit" -eq 124 ]; then
      echo " TIMEOUT (${SCAN_TIMEOUT}s)"
    else
      echo " done (exit $scan_exit)"
    fi
  fi
  scan_end="$(date +%s)"
  scan_dur=$((scan_end - scan_start))
  ((scan_done++)) || true

  # Write per-project log entry
  {
    echo "───────────────────────────────────────────────────────"
    echo "Project: $name"
    echo "Path:    $dir"
    echo "Result:  $out"
    echo "Exit:    $scan_exit"
    echo "Duration: ${scan_dur}s"
    if [ -f "$out" ]; then
      python3 -c "
import json, sys
data = json.loads(open('$out').read())
findings = data.get('findings', [])
files = data.get('scanned_files', 0)
errors = data.get('errors', [])
framework = data.get('framework', '?')
print(f'Framework: {framework}')
print(f'Files scanned: {files}')
print(f'Findings: {len(findings)}')
if errors:
    print(f'Errors: {errors}')
sev = {}
for f in findings:
    s = f.get('severity', '?')
    sev[s] = sev.get(s, 0) + 1
if sev:
    print(f'  Severity: {dict(sorted(sev.items()))}')
" 2>/dev/null || echo "  (could not parse result)"
    else
      echo "No output file produced"
    fi
  } >> "$RUN_LOG"
done

echo ""
echo "  Scanned: $scan_done / Skipped: $scan_skip"
echo ""

# ── Generate BENCHMARK3000.md ───────────────────────────────────────────

echo "=== Phase 3: Generating BENCHMARK3000.md ==="

# Export metadata so Python can reconstruct project info
REPO_META_JSON="{"
first=true
for name in "${REPO_NAMES[@]}"; do
  if $first; then first=false; else REPO_META_JSON+=","; fi
  REPO_META_JSON+="\"$name\":\"${REPO_META[$name]}\""
done
REPO_META_JSON+="}"
export REPO_META_JSON

# Export ordered list
REPO_ORDER_CSV=""
for name in "${REPO_NAMES[@]}"; do
  if [ -n "$REPO_ORDER_CSV" ]; then REPO_ORDER_CSV+=","; fi
  REPO_ORDER_CSV+="$name"
done
export REPO_ORDER="$REPO_ORDER_CSV"
export RESULTS_DIR
export BENCHMARK_MD

python3 << 'PYEOF'
import json, sys, os
from pathlib import Path
from datetime import date
from collections import defaultdict

RESULTS_DIR = Path(os.environ.get("RESULTS_DIR", "/tmp/agentwall-results3k"))
BENCHMARK_MD = Path(os.environ.get("BENCHMARK_MD", "BENCHMARK3000.md"))

# ── Rule → Attack Vector mapping ─────────────────────────────────────

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

RULE_DESCS = {
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

NOT_DETECTED_REASONS = {
    'AW-ATK-POI-001': 'Requires runtime: inject docs, measure ranking',
    'AW-ATK-POI-002': 'Requires runtime: single-doc injection',
    'AW-ATK-POI-003': 'Requires runtime: query-only memory injection',
    'AW-ATK-POI-004': 'Requires runtime: time-delayed session analysis',
    'AW-ATK-POI-005': 'Requires binary analysis: PDF/DOCX hidden content',
    'AW-ATK-POI-006': 'Requires tracking memory→fine-tuning pipeline',
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

# ── Category definitions for report grouping ─────────────────────────

CATEGORIES = [
    ("tier1-langchain",    "Tier 1 — LangChain Ecosystem (>2k stars)"),
    ("llamaindex",         "Tier 2 — LlamaIndex Ecosystem"),
    ("multi-agent",        "Tier 3 — Multi-Agent Frameworks"),
    ("rag-app",            "Tier 4 — RAG Applications"),
    ("vector-store",       "Tier 5 — Vector Store Ecosystems"),
    ("memory-knowledge",   "Tier 6 — Memory & Knowledge Systems"),
    ("chatbot-assistant",  "Tier 7 — Chatbot / Assistant Frameworks"),
    ("code-dev-agent",     "Tier 8 — Code / Dev Agents"),
    ("production-platform","Tier 9 — Production Agent Platforms"),
    ("tier2-small",        "Tier 10 — Small / Niche Projects"),
]

# ── Load all results ─────────────────────────────────────────────────

# Read the REPO_META from environment (passed as JSON)
import subprocess
repo_meta_raw = os.environ.get("REPO_META_JSON", "{}")
try:
    REPO_META = json.loads(repo_meta_raw)
except Exception:
    REPO_META = {}

# Build project list from result files + metadata
projects = {}
for json_file in sorted(RESULTS_DIR.glob("*.json")):
    key = json_file.stem
    try:
        data = json.loads(json_file.read_text())
    except Exception:
        data = None
    meta = REPO_META.get(key, f"{key}|?|unknown")
    parts = meta.split("|")
    display = parts[0] if len(parts) > 0 else key
    stars = parts[1] if len(parts) > 1 else "?"
    category = parts[2] if len(parts) > 2 else "unknown"
    projects[key] = {
        "display": display,
        "stars": stars,
        "category": category,
        "data": data,
    }

# Also add entries for registered repos without results (not cloned / not scanned)
for key, meta_str in REPO_META.items():
    if key not in projects:
        parts = meta_str.split("|")
        projects[key] = {
            "display": parts[0] if len(parts) > 0 else key,
            "stars": parts[1] if len(parts) > 1 else "?",
            "category": parts[2] if len(parts) > 2 else "unknown",
            "data": None,
        }

# Respect registration order
repo_order_raw = os.environ.get("REPO_ORDER", "")
REPO_ORDER = [x for x in repo_order_raw.split(",") if x] if repo_order_raw else sorted(projects.keys())


def extract_vectors(findings):
    vectors = {}
    for f in findings:
        rule_id = f.get('rule_id', '')
        for vec_id in RULE_TO_VECTORS.get(rule_id, []):
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


# ── Build report ─────────────────────────────────────────────────────

lines = []
w = lines.append

w("# AgentWall Benchmark 3000")
w("")
w(f"**Date:** {date.today().isoformat()}")
w("**Version:** 0.1.0")
w("**Layers enabled:** L0–L6 (default static analysis)")
w(f"**Projects:** {len(REPO_ORDER)}")
w("**Reproduce:** `./scripts/benchmark3000.sh`")
w("")
w("---")
w("")

# ── Per-category tables ──────────────────────────────────────────────

grand_findings = 0
grand_crit = 0
grand_high = 0
grand_files = 0
grand_scanned = 0
grand_with_findings = 0
all_vectors_found = {}
all_rules = defaultdict(int)

category_stats = []  # (label, findings, crit, high, files, scanned, with_findings)

section_num = 1
for cat_key, cat_label in CATEGORIES:
    cat_projects = [k for k in REPO_ORDER if projects.get(k, {}).get("category") == cat_key]
    if not cat_projects:
        continue

    w(f"## {section_num}. {cat_label}")
    w("")
    w("| # | Project | Stars | Files | Findings | CRIT | HIGH | MED | LOW | Top Rules |")
    w("|---|---|---|---|---|---|---|---|---|---|")

    t_findings = 0; t_crit = 0; t_high = 0; t_files = 0; t_with = 0; t_scanned = 0

    for idx, key in enumerate(cat_projects, 1):
        proj = projects[key]
        display = proj["display"]
        stars = proj["stars"]
        data = proj["data"]

        if data is None:
            w(f"| {idx} | {display} | {stars} | - | - | - | - | - | - | not scanned |")
            continue

        t_scanned += 1
        findings = data.get("findings", [])
        files = data.get("scanned_files", 0)
        t_files += files

        sev = defaultdict(int)
        rules = defaultdict(int)
        for finding in findings:
            s = finding.get("severity", "?").lower()
            sev[s] += 1
            r = finding.get("rule_id", "?")
            rules[r] += 1
            all_rules[r] += 1

        crit = sev["critical"]; high = sev["high"]
        med = sev["medium"]; low = sev["low"] + sev["info"]
        total = len(findings)
        t_findings += total; t_crit += crit; t_high += high
        if total > 0:
            t_with += 1

        # Extract vectors
        proj_vectors = extract_vectors(findings)
        for vec_id, evidence in proj_vectors.items():
            if vec_id not in all_vectors_found:
                all_vectors_found[vec_id] = []
            for e in evidence:
                e["project"] = display
            all_vectors_found[vec_id].extend(evidence)

        top = sorted(rules.items(), key=lambda x: -x[1])[:3]
        rule_str = ", ".join(f"{r}({c})" for r, c in top) if top else "—"
        w(f"| {idx} | {display} | {stars} | {files} | {total} | {crit} | {high} | {med} | {low} | {rule_str} |")

    w("")
    w(f"**Totals: {t_findings} findings ({t_crit} CRITICAL, {t_high} HIGH) across {t_files} files. {t_with}/{len(cat_projects)} have findings.**")
    w("")
    w("---")
    w("")

    grand_findings += t_findings
    grand_crit += t_crit
    grand_high += t_high
    grand_files += t_files
    grand_scanned += t_scanned
    grand_with_findings += t_with
    category_stats.append((cat_label, t_findings, t_crit, t_high, t_files, t_scanned, t_with, len(cat_projects)))
    section_num += 1

# ── Grand summary ────────────────────────────────────────────────────

w(f"## {section_num}. Grand Summary")
w("")
w("| Metric | Value |")
w("|---|---|")
w(f"| Total projects | {len(REPO_ORDER)} |")
w(f"| Projects scanned | {grand_scanned} |")
w(f"| Projects with findings | {grand_with_findings} ({grand_with_findings*100//max(grand_scanned,1)}%) |")
w(f"| Total files scanned | {grand_files:,} |")
w(f"| Total findings | {grand_findings} |")
w(f"| CRITICAL | {grand_crit} |")
w(f"| HIGH | {grand_high} |")
fpf = f"{grand_findings / max(grand_files,1):.3f}" if grand_files else "0"
w(f"| Findings per file | {fpf} |")
w("")

w("### Category Comparison")
w("")
w("| Category | Projects | Scanned | With Findings | Findings | CRIT | HIGH | Files |")
w("|---|---|---|---|---|---|---|---|")
for label, f, c, h, fi, sc, wf, total in category_stats:
    short = label.split("—")[-1].strip() if "—" in label else label
    w(f"| {short} | {total} | {sc} | {wf} | {f} | {c} | {h} | {fi:,} |")
w("")
w("---")
w("")
section_num += 1

# ── Rule distribution ────────────────────────────────────────────────

w(f"## {section_num}. Rule Distribution")
w("")

if all_rules:
    w("| Rule | Count | % | Description |")
    w("|---|---|---|---|")
    for rule_id, count in sorted(all_rules.items(), key=lambda x: -x[1]):
        pct = f"{count / grand_findings * 100:.0f}%" if grand_findings else "0%"
        desc = RULE_DESCS.get(rule_id, rule_id)
        w(f"| {rule_id} | {count} | {pct} | {desc} |")
else:
    w("No findings to report.")

w("")
w("---")
w("")
section_num += 1

# ── Attack vector coverage ───────────────────────────────────────────

detected_count = len(DETECTABLE_VECTORS)
total_vectors = len(ALL_VECTORS)
w(f"## {section_num}. Attack Vector Coverage ({detected_count} / {total_vectors} Detectable)")
w("")

atk_categories = {
    'MEM': ('Memory Isolation', 4),
    'POI': ('Data Poisoning', 6),
    'EMB': ('Embedding Attacks', 5),
    'INJ': ('Prompt Injection', 3),
    'EXF': ('Exfiltration', 3),
    'CFG': ('Configuration', 6),
    'DOS': ('Denial of Service', 3),
    'AGT': ('Agentic Attacks', 5),
}

w("| Category | Detected | Total | Coverage |")
w("|---|---|---|---|")
for cat, (cat_name, cat_total) in atk_categories.items():
    detected = sum(1 for v in DETECTABLE_VECTORS if f"-{cat}-" in v)
    pct = f"{detected / cat_total * 100:.0f}%"
    w(f"| **{cat}** — {cat_name} | {detected} | {cat_total} | {pct} |")

w("")

# Vectors confirmed
w("### Attack Vectors Confirmed in Real-World Projects")
w("")

if all_vectors_found:
    w("| Attack Vector | Description | Projects Affected | Hits | Example Evidence |")
    w("|---|---|---|---|---|")

    for vec_id in sorted(all_vectors_found.keys()):
        evidence_list = all_vectors_found[vec_id]
        desc = ALL_VECTORS.get(vec_id, vec_id)
        projects_hit = sorted(set(e["project"] for e in evidence_list))
        total_hits = len(evidence_list)

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

        proj_str = ", ".join(projects_hit[:10])
        if len(projects_hit) > 10:
            proj_str += f" (+{len(projects_hit) - 10} more)"

        if example and example.get("file"):
            fname = Path(example["file"]).name
            evidence_str = f'`{fname}:{example.get("line", "?")}` ({example["rule_id"]})'
        else:
            evidence_str = f'({example["rule_id"]})' if example else "—"

        w(f"| **{vec_id}** | {desc} | {proj_str} | {total_hits} | {evidence_str} |")
    w("")
else:
    w("No scan results available yet. Run `./scripts/benchmark3000.sh` first.")
    w("")

# Vectors not detected
not_detected = [v for v in sorted(ALL_VECTORS.keys()) if v not in DETECTABLE_VECTORS]
w(f"### Vectors Not Detected ({len(not_detected)} / {total_vectors})")
w("")
w("| Vector | Description | Reason |")
w("|---|---|---|")
for vec_id in not_detected:
    desc = ALL_VECTORS[vec_id]
    reason = NOT_DETECTED_REASONS.get(vec_id, "Out of scope for static analysis")
    w(f"| {vec_id} | {desc} | {reason} |")

w("")
w("---")
w("")
section_num += 1

# ── Heatmap ──────────────────────────────────────────────────────────

w(f"## {section_num}. Attack Vector Heatmap (Per Project)")
w("")

detected_vec_ids = sorted(DETECTABLE_VECTORS)
short_labels = [v.replace("AW-ATK-", "") for v in detected_vec_ids]
header = "| Project | " + " | ".join(short_labels) + " | Total |"
sep = "| --- | " + " | ".join(["---"] * len(detected_vec_ids)) + " | --- |"
w(header)
w(sep)

for key in REPO_ORDER:
    proj = projects.get(key)
    if not proj:
        continue
    display = proj["display"]
    data = proj["data"]

    if data is None:
        cells = " | ".join(["—"] * len(detected_vec_ids))
        w(f"| {display} | {cells} | — |")
        continue

    findings = data.get("findings", [])
    proj_vectors = extract_vectors(findings)
    row_total = 0
    cells = []
    for vec_id in detected_vec_ids:
        hits = proj_vectors.get(vec_id, [])
        count = len(hits)
        row_total += count
        cells.append(f"**{count}**" if count > 0 else "·")

    w(f'| {display} | {" | ".join(cells)} | {row_total} |')

w("")
w("*Legend: number = findings count, · = not detected, — = not scanned*")
w("")
w("---")
w("")
section_num += 1

# ── How to reproduce ─────────────────────────────────────────────────

w(f"## {section_num}. How to Reproduce")
w("")
w("```bash")
w('pip install -e ".[dev]"')
w("./scripts/benchmark3000.sh")
w("```")
w("")
w("### Environment Variables")
w("")
w("| Variable | Default | Description |")
w("|---|---|---|")
w("| `MAX_PARALLEL` | 4 | Parallel git clone jobs |")
w("| `SCAN_TIMEOUT` | 300 | Per-project scan timeout (seconds) |")

BENCHMARK_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"  Written to: {BENCHMARK_MD}")
print(f"  Total projects: {len(REPO_ORDER)}")
print(f"  Total findings: {grand_findings}")
print(f"  Attack vectors confirmed: {len(all_vectors_found)}/{detected_count}")
PYEOF

# ── Write log summary ───────────────────────────────────────────────

{
  echo ""
  echo "═══════════════════════════════════════════════════════"
  echo "Run Summary — $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "═══════════════════════════════════════════════════════"
  echo "BENCHMARK.md: $BENCHMARK_MD"
  echo "JSON reports: $RESULTS_DIR/"
  echo "Log: $RUN_LOG"
  python3 -c "
import json
from pathlib import Path
results_dir = Path('$RESULTS_DIR')
total_f = 0; total_files = 0; scanned = 0; with_findings = 0
for p in sorted(results_dir.glob('*.json')):
    try:
        d = json.loads(p.read_text())
        findings = d.get('findings', [])
        total_f += len(findings)
        total_files += d.get('scanned_files', 0)
        scanned += 1
        if findings: with_findings += 1
    except Exception:
        pass
print(f'Projects scanned: {scanned}')
print(f'Projects with findings: {with_findings}')
print(f'Total files: {total_files}')
print(f'Total findings: {total_f}')
" 2>/dev/null
} >> "$RUN_LOG"

echo ""
echo "=== Benchmark 3000 complete ==="
echo "JSON reports: $RESULTS_DIR/"
echo "Report: $BENCHMARK_MD"
echo "Log: $RUN_LOG"
