# App Builder Skill - Implementation Plan

## Problema

El skill `app-builder` tiene buena estructura pero no cumple completamente con `meta-skill-antigravity`:

1. **Description** resume funcionalidad en vez de triggering conditions
2. **Sin artifacts TDD** que documenten el proceso de creación
3. **Sin validación** de los 13 templates incluidos

---

## Propuestas de Cambio

### 1. Corregir Description (CSO Optimization)

**Actual:**

```yaml
description: Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, coordinates agents.
```

**Propuesto:**

```yaml
description: Use cuando el usuario quiera crear una nueva aplicación, necesite scaffolding de proyecto, determinar tech stack, o construir algo desde cero. Keywords: nueva app, crear proyecto, scaffolding, full-stack, tech stack, boilerplate.
```

> [!IMPORTANT]
> El cambio de description es crítico. Antigravity usa esto para decidir cuándo activar el skill.

---

### 2. Verificar Templates

Los 13 templates deben verificarse:

| Template           | Verificación                              |
| ------------------ | ----------------------------------------- |
| nextjs-fullstack   | Pendiente                                 |
| nextjs-saas        | Pendiente                                 |
| nextjs-static      | Pendiente                                 |
| nuxt-app           | Pendiente                                 |
| express-api        | Pendiente                                 |
| python-fastapi     | Pendiente                                 |
| react-native-app   | Pendiente                                 |
| flutter-app        | Pendiente                                 |
| electron-desktop   | Pendiente                                 |
| chrome-extension   | Pendiente                                 |
| cli-tool           | Pendiente                                 |
| monorepo-turborepo | Pendiente                                 |
| astro-static       | Pendiente (nuevo, no listado en SKILL.md) |

> [!WARNING]
> El template `astro-static` existe pero no está documentado en SKILL.md.

---

### 3. Añadir Sección Common Mistakes (opcional)

Basado en problemas comunes al crear apps:

| Error                                      | Fix                                  |
| ------------------------------------------ | ------------------------------------ |
| Elegir tech stack sin preguntar requisitos | Hacer preguntas Socráticas primero   |
| Crear sin plan                             | Crear {task-slug}.md antes de código |

---

## Archivos a Modificar

### [MODIFY] [SKILL.md](file:///Users/gonzoblasco/habilidades_de_agentes/.agent/skills/app-builder/SKILL.md)

- Cambiar description en frontmatter
- Añadir `astro-static` a la tabla de templates
- Opcional: añadir sección Common Mistakes

---

## Verificación

1. Validar que description activa el skill correctamente
2. Confirmar SKILL.md < 500 líneas
3. Verificar que todos los templates están documentados

---

## Decisión Requerida

¿Proceder con los 3 cambios, o solo el cambio de description?
