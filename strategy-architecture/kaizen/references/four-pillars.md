# The Four Pillars of Kaizen

## 1. Continuous Improvement (Kaizen)

Small, frequent improvements compound into major gains.

### Principles

**Incremental over revolutionary:**

- Make smallest viable change that improves quality
- One improvement at a time
- Verify each change before next
- Build momentum through small wins

**Always leave code better:**

- Fix small issues as you encounter them
- Refactor while you work (within scope)
- Update outdated comments
- Remove dead code when you see it

**Iterative refinement:**

- First version: make it work
- Second pass: make it clear
- Third pass: make it efficient
- Don't try all three at once

### In Practice

**When implementing features:**

1. Start with simplest version that works
2. Add one improvement (error handling, validation, etc.)
3. Test and verify
4. Repeat if time permits
5. Don't try to make it perfect immediately

**When refactoring:**

- Fix one smell at a time
- Commit after each improvement
- Keep tests passing throughout
- Stop when "good enough" (diminishing returns)

**When reviewing code:**

- Suggest incremental improvements (not rewrites)
- Prioritize: critical → important → nice-to-have
- Focus on highest-impact changes first
- Accept "better than before" even if not perfect

## 2. Poka-Yoke (Error Proofing)

Design systems that prevent errors at compile/design time, not runtime.

### Principles

**Make errors impossible:**

- Type system catches mistakes
- Compiler enforces contracts
- Invalid states unrepresentable
- Errors caught early (left of production)

**Design for safety:**

- Fail fast and loudly
- Provide helpful error messages
- Make correct path obvious
- Make incorrect path difficult

**Defense in layers:**

1. Type system (compile time)
2. Validation (runtime, early)
3. Guards (preconditions)
4. Error boundaries (graceful degradation)

### In Practice

**When designing APIs:**

- Use types to constrain inputs
- Make invalid states unrepresentable
- Return Result<T, E> instead of throwing
- Document preconditions in types

**When handling errors:**

- Validate at system boundaries
- Use guards for preconditions
- Fail fast with clear messages
- Log context for debugging

**When configuring:**

- Required over optional with defaults
- Validate all config at startup
- Fail deployment if config invalid
- Don't allow partial configurations

## 3. Standardized Work

Follow established patterns. Document what works. Make good practices easy to follow.

### Principles

**Consistency over cleverness:**

- Follow existing codebase patterns
- Don't reinvent solved problems
- New pattern only if significantly better
- Team agreement on new patterns

**Documentation lives with code:**

- README for setup and architecture
- CLAUDE.md for AI coding conventions
- Comments for "why", not "what"
- Examples for complex patterns

**Automate standards:**

- Linters enforce style
- Type checks enforce contracts
- Tests verify behavior
- CI/CD enforces quality gates

### In Practice

**Before adding new patterns:**

- Search codebase for similar problems solved
- Check CLAUDE.md for project conventions
- Discuss with team if breaking from pattern
- Update docs when introducing new pattern

**When writing code:**

- Match existing file structure
- Use same naming conventions
- Follow same error handling approach
- Import from same locations

**When reviewing:**

- Check consistency with existing code
- Point to examples in codebase
- Suggest aligning with standards
- Update CLAUDE.md if new standard emerges

## 4. Just-In-Time (JIT)

Build what's needed now. No more, no less. Avoid premature optimization and over-engineering.

### Principles

**YAGNI (You Aren't Gonna Need It):**

- Implement only current requirements
- No "just in case" features
- No "we might need this later" code
- Delete speculation

**Simplest thing that works:**

- Start with straightforward solution
- Add complexity only when needed
- Refactor when requirements change
- Don't anticipate future needs

**Optimize when measured:**

- No premature optimization
- Profile before optimizing
- Measure impact of changes
- Accept "good enough" performance

### In Practice

**When implementing:**

- Solve the immediate problem
- Use straightforward approach
- Resist "what if" thinking
- Delete speculative code

**When optimizing:**

- Profile first, optimize second
- Measure before and after
- Document why optimization needed
- Keep simple version in tests

**When abstracting:**

- Wait for 3+ similar cases (Rule of Three)
- Make abstraction as simple as possible
- Prefer duplication over wrong abstraction
- Refactor when pattern clear
