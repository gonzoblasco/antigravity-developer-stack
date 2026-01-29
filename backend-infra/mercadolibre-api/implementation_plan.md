# Refactorización del Skill `mercadolibre-api`

Aplicar metodología TDD del `meta-skill-antigravity` para optimizar el skill existente.

---

## Diagnóstico Actual

| Criterio                   | Estado Actual         | Objetivo                       |
| -------------------------- | --------------------- | ------------------------------ |
| **Description**            | "Ayuda a trabajar..." | "Use cuando..." (CSO)          |
| **Keywords**               | Genéricos             | Síntomas + errores específicos |
| **Líneas SKILL.md**        | 256                   | < 200 (condensar)              |
| **Progressive Disclosure** | ❌ Todo inline        | ✅ Quick Start + references    |
| **Artifacts TDD**          | ❌ No existen         | ✅ task/plan/walkthrough       |

---

## Proposed Changes

### Core Skill File

#### [MODIFY] [SKILL.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/mercadolibre-api/SKILL.md)

**Cambios en Frontmatter:**

```diff
---
name: mercadolibre-api
-description: Ayuda a trabajar con el API de Mercado Libre. Actívala cuando el usuario quiera integrar Mercado Libre, consultar productos ML, publicar en Mercado Libre, gestionar órdenes ML, usar API de MercadoLibre, o necesite ayuda con autenticación OAuth de ML.
+description: Use cuando necesite integrar MercadoLibre API, autenticar OAuth ML, resolver error 401/403/429 MELI, configurar webhooks ML, publicar productos, gestionar órdenes/preguntas, o debuggear tokens expirados. Keywords: oauth mercadolibre, token expirado ML, rate limit MELI, webhook notificaciones.
---
```

**Cambios en Estructura:**

1. Condensar sección "Instructions" a Quick Start (~50 líneas)
2. Mover ejemplos de código extensos a `references/code-examples.md`
3. Crear tabla de errores compacta con links a soluciones
4. Añadir flowchart de decisión OAuth

---

#### [NEW] [oauth-guide.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/mercadolibre-api/references/oauth-guide.md)

Guía detallada de flujo OAuth 2.0 extraída de SKILL.md actual (líneas 25-43).

---

#### [NEW] [code-examples.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/mercadolibre-api/references/code-examples.md)

Ejemplos de código completos para:

- Búsqueda de productos
- Publicación de items
- Gestión de órdenes
- Respuesta a preguntas
- Configuración webhooks

---

#### [NEW] [error-handling.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/mercadolibre-api/references/error-handling.md)

Tabla expandida de errores HTTP con:

- Código de error
- Causa común
- Solución paso a paso
- Ejemplo de retry/backoff

---

## Verification Plan

### Test de Activación CSO

**Escenario 1: Trigger por síntoma**

```
Prompt: "tengo un error 401 con mercadolibre y no sé por qué"
Expected: Skill se activa y ofrece solución de token expirado
```

**Escenario 2: Trigger por tarea**

```
Prompt: "necesito configurar webhooks para recibir notificaciones de ML"
Expected: Skill se activa y guía configuración
```

**Escenario 3: Trigger por keyword**

```
Prompt: "el token de mercadolibre expiró, cómo lo renuevo?"
Expected: Skill se activa y explica refresh token
```

### Validación Manual

1. **Verificar estructura de archivos** después de refactorización
2. **Contar líneas** de SKILL.md (debe ser < 200)
3. **Revisar links** a referencias (deben funcionar)
4. **Leer description** y confirmar formato CSO

---

## Archivos Resultantes

```
mercadolibre-api/
├── SKILL.md                    # < 200 líneas (condensado)
├── task.md                     # Tracking TDD
├── implementation_plan.md      # Este documento
├── walkthrough.md              # Post-implementación
└── references/
    ├── oauth-guide.md          # [NEW] Flujo OAuth detallado
    ├── code-examples.md        # [NEW] Ejemplos completos
    ├── error-handling.md       # [NEW] Tabla de errores
    ├── examples/               # Existente
    │   └── ...
    └── templates/              # Existente
        └── ...
```

---

## Riesgos y Mitigaciones

| Riesgo                          | Mitigación                                |
| ------------------------------- | ----------------------------------------- |
| Perder información al condensar | Mover TODO a references antes de eliminar |
| Links rotos a referencias       | Validar cada link manualmente             |
| Regresión en activación         | Probar escenarios antes/después           |

---

## Estimación

| Fase           | Duración | Acciones                          |
| -------------- | -------- | --------------------------------- |
| GREEN Phase    | 15 min   | Editar SKILL.md, crear references |
| REFACTOR Phase | 10 min   | Optimización final                |
| Validación     | 5 min    | Tests de activación               |
| **Total**      | ~30 min  |                                   |

---

> [!IMPORTANT]
> **Esperar aprobación antes de proceder a EXECUTION**
