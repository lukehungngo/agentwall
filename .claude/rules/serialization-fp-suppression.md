---
paths:
  - "src/agentwall/analyzers/serialization.py"
  - "tests/test_serialization_analyzer.py"
---

# SER-003 False Positive Suppression

SER-003 (dynamic import) is the highest-volume rule. Four heuristics suppress FPs:

1. **`_is_fstring_with_constant_prefix()`** — f-string with 2+ dots in prefix (e.g., `f"myapp.backends.{x}"`)
2. **`_is_config_attribute_import()`** — ALL_CAPS attribute access (e.g., `settings.BACKEND_CLASS`)
3. **`_is_try_except_guarded()`** — import wrapped in try/except (optional dependency pattern). Uses `_build_parent_map(tree)` for O(depth) ancestor traversal, NOT O(n^2) tree walk.
4. **`_is_constant_format_call()`** — `.format()` on string with 2+ dots (e.g., `"myapp.backends.{}".format(x)`)

## Critical: dot-count consistency

Both f-string and `.format()` suppressions require **2+ dots** in the constant prefix. A single dot (e.g., `"myapp.{}"`) is NOT enough — this was a P0 regression that suppressed true positives.
