---
paths:
  - "src/agentwall/rules.py"
  - "src/agentwall/analyzers/taint.py"
  - "src/agentwall/runtime/patcher.py"
  - "src/agentwall/analyzers/memory.py"
---

# Severity Discipline

**CRITICAL is reserved for confirmed cross-tenant data access.** This is an architecture invariant (CLAUDE.md #6). Inflated severity kills user trust.

## What qualifies as CRITICAL

Only AW-MEM-001: vector store queries executed without any user/tenant filter, where similarity search returns globally closest vectors including other users' data.

## What does NOT qualify as CRITICAL

- **Runtime detection (L7)**: detects patterns at runtime but doesn't confirm multi-tenancy → HIGH
- **Taint analysis (L3)**: traces data flow but doesn't prove cross-user access → HIGH
- **Missing sanitization**: dangerous but not confirmed cross-user → HIGH or MEDIUM
- **Tool permissions**: privilege escalation risk but not data leakage → HIGH or MEDIUM

## P0 lessons

Both `runtime/patcher.py` (line 78) and `analyzers/taint.py` (lines 264, 289) were shipping CRITICAL severity without evidence-based classification. Fixed to HIGH in v1.0 audit.
