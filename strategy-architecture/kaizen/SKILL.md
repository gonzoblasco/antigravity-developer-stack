---
name: kaizen
description: Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discuss process improvements. Keywords: refactoring, improvements, quality, kaizen, code review, patterns, best practices.
---

# Kaizen: Continuous Improvement

## Overview

Small improvements, continuously. Error-proof by design. Follow what works. Build only what's needed.

**Core principle:** Many small improvements beat one big change. Prevent errors at design time, not with fixes.

## When to Use

**Always applied for:**

- Code implementation and refactoring
- Architecture and design decisions
- Process and workflow improvements
- Error handling and validation

**Philosophy:** Quality through incremental progress and prevention, not perfection through massive effort.

## The Four Pillars

[Detailed Guide: The Four Pillars](references/four-pillars.md)

### 1. Continuous Improvement (Kaizen)

**Goal:** Small, frequent improvements compound into major gains.

- **Incremental:** Make smallest viable change.
- **Refinement:** Make it work -> Make it clear -> Make it efficient.
- **Action:** Always leave code better than you found it.

[Examples: Iterative Refinement](examples/code-quality.md#1-continuous-improvement-iterative-refinement)

### 2. Poka-Yoke (Error Proofing)

**Goal:** Design systems that prevent errors at compile/design time.

- **Make errors impossible:** Use the type system (TS/Rust/etc) to represent only valid states.
- **Fail fast:** Validate inputs at boundaries, not deep in the code.
- **Defense in layers:** Types -> Verification -> Guards.

[Examples: Type System & Validation](examples/code-quality.md#2-poka-yoke-error-proofing)

### 3. Standardized Work

**Goal:** Follow established patterns. Consistency > Cleverness.

- **Consistency:** Follow existing codebase patterns ("Do as the locals do").
- **Documentation:** "Why" comments, not "What".
- **Automation:** Let linters and tests enforce the standard.

[Examples: Patterns & Consistency](examples/code-quality.md#3-standardized-work)

### 4. Just-In-Time (JIT)

**Goal:** Build what's needed now. Avoid premature optimization.

- **YAGNI:** Implement only current requirements.
- **Optimization:** Only after profiling/measurement.
- **Abstraction:** Rule of Three (Duplicate twice, Abstract the third time).

[Examples: YAGNI & Optimization](examples/code-quality.md#4-just-in-time-jit)

## Integration with Commands

Use these commands for structured problem-solving:

- **`/why`**: Root cause analysis (5 Whys)
- **`/cause-and-effect`**: Fishbone diagram analysis
- **`/plan-do-check-act`**: Iterative improvement cycles
- **`/analyse`**: Select best method (Gemba/VSM/Muda)

## Red Flags (Anti-Patterns)

**Violating Continuous Improvement:**

- "I'll refactor it later" (never happens)
- Big bang rewrites
- Leaving code worse than found

**Violating Poka-Yoke:**

- "Users should just be careful"
- Validation after use (e.g., calculating fee before checking if amount > 0)
- Optional config `apiKey?: string` instead of failing at startup.

**Violating Standardized Work:**

- "I prefer my way" vs project convention.
- Ignoring existing helper functions.

**Violating Just-In-Time:**

- "We might need this later" (Speculative Generality).
- Building generic Repositories for 1 table.

## Remember

- **Mindset:** Good enough today, better tomorrow. Repeat.
- **Action:** Check `examples/code-quality.md` for specific implementation patterns.
