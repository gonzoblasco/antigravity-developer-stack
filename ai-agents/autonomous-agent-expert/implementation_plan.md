# Implementation Plan: autonomous-agent-expert Refactor

## Objetivo

Refactorizar el skill `autonomous-agent-expert` para cumplir con la metodología `meta-skill-antigravity`, aplicando progressive disclosure y optimización de descripción.

---

## Problemas Identificados

### 1. Description Incorrecta

```yaml
# ❌ ACTUAL: Resume el workflow
description: "Design patterns for building autonomous agents. Covers agent loops, tool integration..."

# ✅ CORRECTO: Solo condiciones de activación
description: "Use when building AI agents, designing tool APIs, implementing permission systems, or working with ReAct/Plan-Execute patterns. Keywords: agent loop, tool design, permission system, sandbox, human-in-the-loop."
```

### 2. Sin Progressive Disclosure

Todo el contenido está en un solo archivo de 379 líneas. Los ejemplos de código extensos deberían estar en `references/`.

### 3. Frontmatter con Campo Extra

Tiene `source: consolidated from...` que no es parte del estándar.

---

## Proposed Changes

### Nueva Estructura

```
autonomous-agent-expert/
├── SKILL.md                    # Core reducido (~200-250 líneas)
├── task.md                     # Este archivo
├── implementation_plan.md      # Este plan
├── walkthrough.md              # Registro del proceso
└── references/
    ├── react-pattern.md        # ReAct Agent Loop (líneas 27-67)
    ├── plan-execute-pattern.md # Plan-Execute (líneas 69-87)
    ├── reflection-pattern.md   # Reflection (líneas 89-107)
    ├── tool-design.md          # Tools (líneas 109-166)
    ├── permission-patterns.md  # Permissions + Sandbox (líneas 168-237)
    ├── context-management.md   # Context injection (líneas 239-275)
    └── anti-patterns.md        # Anti-patterns + Sharp edges (líneas 300-332)
```

---

### [NEW] references/react-pattern.md

Contendrá el ReAct Agent Loop completo con ejemplo de código Python.

---

### [NEW] references/plan-execute-pattern.md

Contendrá el Plan-Execute pattern con ejemplo.

---

### [NEW] references/reflection-pattern.md

Contendrá el Reflection pattern con ejemplo.

---

### [NEW] references/tool-design.md

Contendrá:

- Essential Coding Agent Tools
- Tool Schema Design

---

### [NEW] references/permission-patterns.md

Contendrá:

- Permission Levels (enum + config)
- Sandboxed Execution

---

### [NEW] references/context-management.md

Contendrá:

- Context Injection patterns (@-mention)

---

### [NEW] references/anti-patterns.md

Contendrá:

- Anti-patterns detallados
- Sharp Edges table

---

### [MODIFY] SKILL.md

**Cambios:**

1. Frontmatter: remover `source`, corregir `description`
2. Quick Start: 1 ejemplo mínimo inline (ReAct simplificado)
3. Core Principles: mantener lista concisa
4. Patterns Overview: tabla resumen con links a references
5. Tool Design: resumen con link a reference
6. Permission & Safety: resumen con link a reference
7. Best Practices Checklist: mantener
8. Key Insights: mantener
9. Resources: mantener

**Meta:** < 250 líneas

---

## Verification Plan

### Automated

- Contar líneas de SKILL.md (debe ser < 250)
- Verificar que todos los links a references existen

### Manual

- Confirmar que progressive disclosure funciona
- Verificar que keywords en description son relevantes
