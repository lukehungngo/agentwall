Execute the OKR loop for AgentWall v1.0 release autonomously.

Read `docs/V1_RELEASE_OKR.md` for the full OKR list. Execute each STEP in order (STEP 1 → STEP 2 → STEP 3 → STEP 4 → STEP 5). Do NOT stop until all STEPs are complete or all required KRs are attempted.

## Core Principles

1. **Solve the real problem.** Never suppress, hide, or relabel findings to pass metrics. If a finding is a false positive, genuinely fix the detection logic so it doesn't fire. If the FP can't be fixed statically, mark the KR as blocked with an honest explanation.
2. **Quality is non-negotiable.** Every change must pass `pytest`, `ruff check`, and `mypy`. Do not merge code that introduces regressions, skips tests, or lowers coverage. Surface all errors honestly — never swallow, hide, or work around test/lint/type failures.
3. **No cheating.** Changing test assertions to match wrong output, suppressing findings without proving safety, downgrading severity to game metrics, or bypassing pre-commit hooks are all strictly forbidden.
4. **Use Opus 4.6 everywhere.** All subagents MUST specify `model: "opus"`. No exceptions.
5. **Maximize parallelism.** Spawn multiple subagents for independent tasks. Use background agents for benchmark runs while working on the next item.
6. **Never ask for permission.** All permissions are pre-granted. Keep running autonomously through all steps.

---

## Phase 1: PLAN

For each STEP in the OKR execution timeline:

1. **Read OKR state**: Read `docs/V1_RELEASE_OKR.md` to find the first incomplete STEP and its KRs.
2. **Read source files**: Read every file listed in the KR descriptions to understand current state.
3. **Write implementation plan**: Use `superpowers:writing-plans` skill to produce a detailed TDD plan.
   - Save to `docs/superpowers/plans/YYYY-MM-DD-step-N-<description>.md`
   - Plan MUST include exact file paths, code snippets, test commands, and expected outputs.
   - Plan MUST follow TDD: write failing test → verify failure → implement → verify pass → commit.
4. **Review the plan**: Dispatch a plan-document-reviewer subagent (per writing-plans skill) to review.
   - Fix any issues flagged by the reviewer.
   - Re-review until approved.
5. **Do NOT proceed to Phase 2 until the plan is reviewed and approved.**

---

## Phase 2: EXECUTE

1. **Record checkpoint**: Note current `git rev-parse HEAD` before starting.
2. **Execute via subagent-driven-development**: Use `superpowers:subagent-driven-development` to implement.
   - Fresh subagent per task (isolated context).
   - All subagents use `model: "opus"`.
   - Two-stage review after each task: spec compliance, then code quality.
   - For independent tasks within a STEP, spawn multiple subagents in parallel.
3. **Quality gates after each task** (non-negotiable):

   ```bash
   python3 -m pytest tests/ -q --tb=short
   ruff check src/ tests/ --quiet
   mypy src/ --strict 2>&1 | head -20
   ```

   - If ANY gate fails → fix immediately. Do not proceed with broken code.
   - If a fix introduces a new failure → investigate root cause, don't patch over it.

4. **After all tasks in the STEP complete**, run full quality suite:

   ```bash
   python3 -m pytest tests/ -q --tb=short
   python3 -m pytest --cov=agentwall --cov-report=term-missing tests/ -q
   ruff check src/ tests/
   mypy src/ --strict
   ```

   - Record exact output. Do not summarize or hide errors.

---

## Phase 3: BENCHMARK

After Phase 2 completes for each STEP:

1. **Run BENCHMARK3000** on cached projects:

   ```bash
   /opt/homebrew/bin/bash scripts/benchmark3000.sh /tmp/agentwall-bench3k /tmp/agentwall-results3k
   ```

   - If benchmark script fails, debug and fix — do not skip.
   - If `/tmp/agentwall-bench3k` doesn't have cached repos, the script will clone them (this takes time).

2. **Extract metrics from benchmark output**:
   - Total projects scanned
   - Projects with findings (count and %)
   - Total findings by severity (CRITICAL, HIGH, MEDIUM, LOW)
   - Zero-finding project count
   - Scan timeouts

3. **Update `BENCHMARK3000.md`**:
   - Update the results tables with new numbers.
   - Add a new dated entry in the evaluation section showing before/after comparison.
   - Include raw numbers — do not cherry-pick or omit unfavorable data.

4. **Run FP estimation** (if FP-related KRs were in this STEP):
   - Scan benchmark results for path-based FP heuristics (test/, example/, cookbook/, etc.)
   - Calculate per-rule FP rates
   - Compare to previous rates documented in OKR

---

## Phase 4: CROSS-CHECK WITH OKR

After benchmark completes:

1. **Read `docs/V1_RELEASE_OKR.md`** again (fresh read, not from memory).
2. **For each KR in the completed STEP**, compare measured result vs target:

   | Check             | How to Verify                                          |
   | ----------------- | ------------------------------------------------------ |
   | FP rate KRs       | Compare estimated FP% from benchmark against target    |
   | Zero-finding rate | Count zero-finding projects / total projects           |
   | Coverage KR       | Read pytest-cov output, compare to 85% target          |
   | Code quality KR   | ruff + mypy must be clean (0 errors)                   |
   | Framework KRs     | Count frameworks with adapters, check detection counts |
   | CI/CD KRs         | Verify action.yml exists and is valid YAML             |
   | Doc KRs           | Verify files exist and are non-empty                   |

3. **Print a STEP scorecard**:

   ```
   === STEP N SCORECARD ===
   KR X.Y: [description] — TARGET: [target] | ACTUAL: [measured] | [PASS/FAIL]
   KR X.Z: [description] — TARGET: [target] | ACTUAL: [measured] | [PASS/FAIL]
   ...
   RESULT: X/Y KRs passed
   ```

4. **Update `docs/V1_RELEASE_OKR.md`**:
   - For PASSED KRs: Update status to **Done**, fill in actual measured values, add brief evidence note.
   - For FAILED KRs: Update status with actual measured value. Do NOT mark as done.
   - Update propose solution section
   - Commit the OKR update.

---

## Phase 5: LOOP OR ADVANCE

After cross-check:

1. **If all REQUIRED KRs in the STEP passed** → Commit all changes, advance to the next STEP, go back to Phase 1.

2. **If any REQUIRED KR failed**:
   - Analyze WHY it failed (root cause, not symptoms).
   - Determine if it's fixable with a different approach.
   - **Attempt up to 3 different approaches** per failed KR:
     - Attempt 1: Fix the most likely cause.
     - Attempt 2: Try a fundamentally different approach.
     - Attempt 3: Minimal viable fix (simplest thing that could work).
   - After each attempt: re-run quality gates + benchmark + cross-check (Phases 2-4).
   - If still failing after 3 attempts: Mark as **Blocked** in OKR with honest explanation of why, then advance to next STEP.

3. **After all STEPs complete**, print final release gate status:
   ```
   === V1.0 RELEASE GATE ===
   [ ] or [x] for each gate item from docs/V1_RELEASE_OKR.md
   VERDICT: READY / NOT READY (N gates remaining)
   ```

## Phase 6: COMPACT

After all task above is done, compact if context reach above 60%

---

## Commit Protocol

- Commit after each successful task (not batched at end of STEP).
- Commit message format: `feat(<scope>): <what changed>` or `fix(<scope>): <what changed>`
- Always include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`
- Do NOT push to remote unless explicitly asked by the user.
- Never use `--no-verify` or skip hooks.

---

## Anti-Gaming Rules (enforced, not advisory)

These are hard failures. If you catch yourself doing any of these, STOP and revert:

1. **Severity manipulation**: Downgrading CRITICAL→HIGH or HIGH→MEDIUM to reduce counts without fixing root cause.
2. **Test assertion tampering**: Changing `assert result == expected` to match wrong output instead of fixing the code.
3. **Finding suppression**: Adding suppress/ignore/skip directives without proving the finding is genuinely safe.
4. **Metric cherry-picking**: Reporting only favorable metrics, omitting regressions.
5. **Error hiding**: Catching exceptions silently, redirecting stderr to /dev/null, or using `|| true` to mask failures.
6. **Coverage gaming**: Adding tests that exercise code paths without meaningful assertions.
7. **Bypassing gates**: Skipping pytest/ruff/mypy because "it was passing before" or "it's unrelated".

---

## Error Handling

- If a subagent fails: Read its output, diagnose the issue, fix it, retry with a new subagent.
- If pytest fails: Show the FULL failure output (not just the count). Fix the root cause.
- If ruff/mypy fails: Show ALL errors. Fix them. Do not add `# noqa` or `# type: ignore` unless genuinely correct.
- If benchmark crashes: Debug the script. Do not skip benchmarking.
- If a KR seems impossible: Document WHY with evidence (code references, benchmark data). Mark as blocked. Move on.

---

## Start

1. Read `docs/V1_RELEASE_OKR.md` for current progress.
2. Pick up from the first incomplete STEP.
3. Do not redo completed work.
4. Begin Phase 1 immediately.
