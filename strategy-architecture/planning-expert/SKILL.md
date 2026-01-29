---
name: planning-expert
description: Use cuando realices tareas complejas (>5 pasos), investigación, o construcción de proyectos. Keywords: plan, planificación, roadmap, task_plan, findings, workflow, state management.
---

# Planning Expert (Manus-Style)

## Overview

Esta skill implementa patrones de planificación avanzados basados en los principios de Manus (context engineering). El objetivo es utilizar el sistema de archivos como una "memoria de trabajo" persistente, evitando la pérdida de contexto en tareas complejas y habilitando una ejecución resiliente a errores.

**Role**: Task Planning & Execution Strategy Specialist.
I implement battle-tested planning patterns using persistent markdown files as "working memory on disk" to prevent context loss.

> [!IMPORTANT]
> **The Iron Law**: No complex task without a `task_plan.md` FIRST.
> **The 2-Action Rule**: After 2 view/search operations, save key findings to `findings.md` immediately.

---

## The 3 Planning Files

Create these in the **project directory** (never in the skill directory):

| File           | Purpose                    | Update Frequency    |
| :------------- | :------------------------- | :------------------ |
| `task_plan.md` | Roadmap, phases, decisions | After each phase    |
| `findings.md`  | Research, data, snapshots  | After ANY discovery |
| `progress.md`  | Log of actions and tests   | Throughout session  |

---

## Bulletproofing (Disciplina)

| Excusa del Agente                          | Realidad (La Ley)                                             |
| :----------------------------------------- | :------------------------------------------------------------ |
| "Es una tarea simple, no hace falta plan." | Si requiere >5 pasos, NO es simple. Crea el plan.             |
| "Ya sé qué hacer, escribirlo me retrasa."  | El plan no es para "saber", es para "recordar" tras 50 pasos. |
| "Guardaré los hallazgos al final."         | El contexto es volátil. Si no escribes pronto, se pierde.     |

---

## Core Protocols

### 1. Read Before Decide

Before major decisions or starting a new phase, re-read `task_plan.md`. This "recitation" forces the goal back into your short-term attention window.

### 2. The 3-Strike Rule (Failures)

1. **Strike 1**: Diagnose and fix.
2. **Strike 2**: Try alternative tool/approach.
3. **Strike 3**: Broader rethink (check docs).
   **After 3**: Escalate to user. **NEVER repeat the same failing action.**

---

## Workflow & Methodology

1. **Initialize**: Use `scripts/init-session.sh` or create the 3 files manually.
2. **Plan**: Define the Goal and Phases with TDD-like granularity (Step-by-step).
3. **Execute**: Update Status as you move through phases.
4. **Log**: Record ALL errors in the "Errors Encountered" table.

---

## Resources & Examples

### References

- [Manus Principles](references/manus-principles.md)
- [Context Engineering](references/context-engineering.md)
- [Error Protocols](references/error-protocols.md)

### Step-by-Step Examples

- [Research Task](examples/research-task.md)
- [Bug Fix Task](examples/bug-fix.md)
- [Feature Development](examples/feature-dev.md)
- [Error Recovery pattern](examples/error-recovery.md)

---

**Remember**: Context Window = RAM. Filesystem = Disk. Anything important gets written to disk. Update your plan as you learn.
