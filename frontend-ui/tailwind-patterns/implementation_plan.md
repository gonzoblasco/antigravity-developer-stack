# Plan de Implementación: Refactorización de Tailwind Patterns a Antigravity

**Objetivo**: Elevar el skill `tailwind-patterns` al estándar `meta-skill-antigravity`, transformándolo de una "hoja de trucos" a un skill agentic robusto, estructurado y testeado.

## Estado Actual vs. Deseado

| Elemento        | Estado Actual                      | Estado Deseado (Antigravity)                          |
| --------------- | ---------------------------------- | ----------------------------------------------------- |
| **Estructura**  | Solo `SKILL.md` (Flat)             | Estructura completa (`references/`, `task.md`, etc.)  |
| **Frontmatter** | Descriptivo ("v4 principles")      | Trigger-based ("Use when designing UI...") + Keywords |
| **Contenido**   | Tablas de referencia (Cheat sheet) | Reglas de comportamiento + Referencias separadas      |
| **Validación**  | Ninguna explícita                  | Tests TDD (Baseline vs. Skill active)                 |

## User Review Required

> [!IMPORTANT]
> **Cambio de Enfoque**: El skill dejará de ser solo información pasiva para convertirse en instrucciones activas ("Preferir OKLCH sobre HEX", "Rechazar configs JS en v4").

## Proposed Changes

### 1. Reestructuración del Directorio

Se creará la estructura estándar de carpetas para separar "Instrucciones de Agente" de "Conocimiento de Referencia".

#### [NEW] Estructura de Carpetas

```text
tailwind-patterns/
├── SKILL.md                 # Core instructions (< 500 lines)
├── task.md                  # Progress tracking
├── implementation_plan.md   # This document
├── walkthrough.md           # Proof of work
└── references/              # Detailed knowledge
    ├── v4-architecture.md   # Diff v3 vs v4
    ├── modern-layout.md     # Flex/Grid patterns
    └── design-tokens.md     # Colors & Typography
```

### 2. Actualización de `SKILL.md`

El archivo principal se reescribirá para ser más **imperativo**.

**Frontmatter Nuevo:**

```yaml
name: tailwind-patterns
description: Use cuando estés diseñando interfaces, escribiendo CSS o configurando estilos. Keywords: [tailwind, css, styling, ui, design system].
```

**Nuevo Contenido Core (Ejemplo):**

- **Regla #1 (Architecture)**: Always use CSS-first configuration (`@theme`). Reject `tailwind.config.js` unless migrating legacy.
- **Regla #2 (Color)**: Enforce `oklch` for semantic tokens.
- **Regla #3 (Layout)**: Prefer `flex` compositions over fixed geometries.
- **Referencias**: Links a los archivos en `references/`.

### 3. Migración de Contenido (Refactoring)

- Mover las tablas de comparación v3/v4 a `references/v4-architecture.md`.
- Mover los patrones de Flex/Grid a `references/modern-layout.md`.
- **[NEW]** Añadir soporte explícito para v4.1 features:
  - `text-shadow-*` utilities.
  - `mask-*` utilities.
  - Colored `drop-shadow-*`.
  - `@source not` y `@source inline`.
- Mantener en `SKILL.md` solo las reglas de decisión críticas y los anti-patrones.

## Verification Plan (TDD)

### Scenario: The "Legacy Habit" Trap + v4.1 Features

**Prompt**: "Crea un botón primario rojo con sombra de texto azul y un efecto de máscara."

#### Baseline (FAIL Condition)

Sin el skill (o con el actual si es pasivo), el agente podría:

- Usar colores hex: `bg-[#ff0000]`
- Intentar usar plugins arbitrarios para `text-shadow`.
- Usar clases arbitrarias para máscara o `style="..."`.

#### Test (PASS Condition)

Con el nuevo skill, el agente debe:

1. Usar `oklch` o variables CSS semánticas (`bg-primary`).
2. Usar utilidad nativa v4.1: `text-shadow-blue-500`.
3. Usar utilidad nativa v4.1: `mask-linear` (o similar).
4. No crear archivo de config JS.

### Execution Steps

1. [ ] Crear estructura de directorios.
2. [ ] Extraer contenido de `SKILL.md` a `references/*.md`.
3. [ ] Reescribir `SKILL.md` con enfoque imperativo/guardrail.
4. [ ] Ejecutar Baseline y verificar mejora.
