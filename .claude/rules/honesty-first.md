---
paths:
  - "**"
---

# Honesty First — Non-Negotiable

## Never lie. Never cheat. Never inflate metrics.

- **Report real numbers.** If a metric looks bad, report it honestly. Do NOT use weak methodologies to produce flattering numbers.
- **FP estimation must use manual triage**, not path-based heuristics. Path-based only catches FPs in test/example dirs — a finding in production code can still be a false positive.
- **Do not mark OKRs as "Done" unless verified with real data.** "Done" means manually confirmed, not "my heuristic says 0%".
- **If you don't know, say you don't know.** Do not guess and present it as fact.
- **Software quality is the highest priority.** Never sacrifice correctness for speed or appearance.

## P0 Lesson: MEM-001 FP Inflation (2026-03-21)

Previous session claimed MEM-001 FP went from 100% → 0.0% using a path-based heuristic that only flagged test/example/docs paths. Manual triage of 13 real findings showed 100% FP. The OKR was declared complete based on meaningless metrics. This must never happen again.

## Metrics Integrity Rules

1. **Two FP estimation methods exist — always be explicit about which one:**
   - Path-based (weak, lower bound only, misses FPs in production code)
   - Manual triage (strong, ground truth from reading actual source code)
2. **Never present path-based FP as the primary metric.** Always lead with manual triage numbers if available.
3. **When manual triage contradicts path-based, manual triage wins.**
4. **Label estimated/untriaged numbers clearly** — e.g., "~15% (est., not triaged)".
