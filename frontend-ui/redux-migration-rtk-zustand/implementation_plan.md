# Implementation Plan: Reescritura redux-migration-rtk-zustand

> Aplicando meta-skill-antigravity + TDD para documentación

---

## Problema

El skill actual viola múltiples estándares del meta-skill:

| Criterio               | Requerido               | Actual              | Gap              |
| ---------------------- | ----------------------- | ------------------- | ---------------- |
| Líneas SKILL.md        | < 500                   | 618                 | -118 líneas      |
| Progressive Disclosure | ✅                      | ❌                  | Todo inline      |
| Estructura carpetas    | references/, scripts/   | Solo EJEMPLO_USO.md | Falta estructura |
| Artifacts TDD          | task.md, walkthrough.md | Ninguno             | Sin registro     |

---

## User Review Required

> [!IMPORTANT]
> **Decisión de Contenido**
>
> El skill actual tiene ejemplos muy extensos (código antes/después). Propongo:
>
> - Mantener **1 ejemplo compacto** por fase en SKILL.md
> - Mover ejemplos completos a `references/`
>
> ¿Estás de acuerdo con este enfoque?

---

## Proposed Changes

### Component 1: Estructura de Carpetas

Crear nueva jerarquía:

```
redux-migration-rtk-zustand/
├── SKILL.md                    # Condensado ~300 líneas
├── task.md                     # ✅ Creado
├── implementation_plan.md      # ✅ Este archivo
├── walkthrough.md              # Al finalizar
├── references/
│   ├── rtk-migration.md        # Secciones 2.1-2.4 actuales
│   ├── zustand-migration.md    # Secciones 3.1-3.4 actuales
│   └── detection-patterns.md   # Sección 5 actual
├── scripts/
│   └── detect_redux_legacy.sh  # Automatizar detección
└── examples/
    └── EJEMPLO_USO.md          # Mover archivo existente
```

---

### Component 2: references/rtk-migration.md

#### [NEW] [rtk-migration.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/redux-migration-rtk-zustand/references/rtk-migration.md)

Contenido a mover desde SKILL.md (líneas 39-251):

- 2.1 Configuración del Store
- 2.2 Migración de Reducers a Slices
- 2.3 Migración de Async Actions (Thunks)
- 2.4 Migración de Selectors

---

### Component 3: references/zustand-migration.md

#### [NEW] [zustand-migration.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/redux-migration-rtk-zustand/references/zustand-migration.md)

Contenido a mover desde SKILL.md (líneas 254-480):

- 3.1 ¿Por qué migrar de RTK a Zustand?
- 3.2 Migración de Store
- 3.3 Migración de Hooks
- 3.4 Patrón de Slices en Zustand

---

### Component 4: references/detection-patterns.md

#### [NEW] [detection-patterns.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/redux-migration-rtk-zustand/references/detection-patterns.md)

Contenido a mover desde SKILL.md (líneas 514-546):

- Detectar Redux Clásico (comandos grep)
- Detectar RTK listo para Zustand

---

### Component 5: scripts/detect_redux_legacy.sh

#### [NEW] [detect_redux_legacy.sh](file:///Users/gonzoblasco/.gemini/antigravity/skills/redux-migration-rtk-zustand/scripts/detect_redux_legacy.sh)

Script ejecutable que automatiza la detección:

```bash
#!/bin/bash
# Detecta código Redux legacy en el proyecto
# Uso: ./detect_redux_legacy.sh [directorio]
```

---

### Component 6: SKILL.md Condensado

#### [MODIFY] [SKILL.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/redux-migration-rtk-zustand/SKILL.md)

**Estructura nueva (~300 líneas):**

1. **Frontmatter** (sin cambios)
2. **Estrategia Overview** (tabla ruta - mantener)
3. **Quick Start**
   - 1 ejemplo Redux → RTK (compacto)
   - 1 ejemplo RTK → Zustand (compacto)
   - Links a referencias para detalles
4. **Checklist de Migración** (condensado)
5. **Constraints** (mantener)
6. **References** (links a archivos)

**Contenido a eliminar del SKILL.md:**

- Ejemplos extensos de código (mover)
- Sección detección patterns (mover)
- Consideraciones Server Components (mover)

---

## Verification Plan

### Automated Tests

```bash
# Verificar líneas < 500
wc -l SKILL.md

# Verificar estructura
ls -la references/ scripts/ examples/

# Verificar links funcionan
grep -r "references/" SKILL.md
```

### Manual Verification

1. Leer SKILL.md completo - ¿es suficiente para empezar?
2. Navegar a reference - ¿encuentro lo que necesito?
3. Ejecutar script - ¿detecta código legacy?

---

## Estimación

| Tarea                          | Tiempo      |
| ------------------------------ | ----------- |
| Crear estructura carpetas      | 2 min       |
| Crear references/ (3 archivos) | 15 min      |
| Crear script detección         | 5 min       |
| Condensar SKILL.md             | 20 min      |
| Verificación                   | 5 min       |
| **Total**                      | **~47 min** |
