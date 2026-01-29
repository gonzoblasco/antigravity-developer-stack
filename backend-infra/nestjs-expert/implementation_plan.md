# Implementation Plan - NestJS Skill Upgrade

Refactor the `nestjs-expert` skill to align with `meta-skill-antigravity` standards (Progressive Disclosure, CSO, TDD) and optimize performance.

## User Review Required

> [!IMPORTANT]
> This upgrade will significantly restructure the `nestjs-expert` skill folder. The single `SKILL.md` will be split into a core file and multiple reference files. This is a non-destructive change to the logic but a major change to the file structure.

## Proposed Changes

### Structure Refactor (Progressive Disclosure)

Refactor `nestjs-expert/SKILL.md` (currently ~552 lines) to be under 500 lines by moving detailed sections to `references/`.

#### [MODIFY] [SKILL.md](file:///Users/gonzoblasco/habilidades_de_agentes/.agent/skills/nestjs-expert/SKILL.md)

- **Goal**: Reduce size, focus on "Trigger" and "Process".
- Keep: Detection, High-level strategies, Key commands.
- Move out: Detailed troubleshooting specific errors, list of decision trees, verbose patterns.
- Update Frontmatter: Ensure `description` is trigger-focused (CSO).

#### [NEW] `references/troubleshooting.md`

- Content: "Problem-Specific Approaches" section (The 17 specific error cases).

#### [NEW] `references/architecture-decisions.md`

- Content: "Decision Trees for Architecture" section.

#### [NEW] `references/patterns.md`

- Content: "Common Patterns & Solutions" and "Quick Reference Patterns".

### Content Enhancement

- **Performance**: Add a dedicated `references/performance.md` or expand the performance section if it was weak (it was brief).
- **Modern NestJS**: Verify and update for NestJS 10/11 (e.g., SWC support, standalone applications mentions if missing).

### Skill Metadata & hygiene

- Create `task.md` in the skill folder.
- Create `implementation_plan.md` in the skill folder (this current plan, copied over).
- Ensure `description` keywords are optimized.

## Verification Plan

### Automated Validation

- Use `meta-skill-antigravity` scripts if available/applicable to validate structure.
- `python scripts/validate_skill.py nestjs-expert --validate` (if script runs in this env).

### Manual Verification

- **Baseline Test**: Simulate a user asking "My NestJS app has a circular dependency" and ensure the agent can still find the solution (now in `references/troubleshooting.md`) by reading the reference or if the core instructions guide it there.
- **Performance Test**: Check token count of `SKILL.md` (lines reduction).
