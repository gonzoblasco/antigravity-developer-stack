# Claude Search Optimization (CSO)

## Filosofía

**CSO = SEO para skills de Claude/Antigravity**

Antigravity lee `description` para decidir qué skills cargar. Si tu description no matchea, tu skill no se usa.

---

## El Campo Description

### Regla de Oro

```
Description = CUÁNDO usar, NO QUÉ hace
```

### Por Qué Importa

Testing reveló que cuando description resume workflow, Claude/Antigravity sigue description en vez de leer skill completo.

**Ejemplo problemático:**

```yaml
description: Use para TDD - escribe test primero, falla, código mínimo, refactor
```

**Resultado:** Agente hace UN ciclo y para, aunque skill tiene flowchart con múltiples stages.

**Fix:**

```yaml
description: Use cuando implementes features o bugfixes, antes de escribir código
```

**Resultado:** Agente lee skill completo y sigue flowchart.

---

## Patrones Correctos

### ✅ Solo Triggering Conditions

```yaml
# ✅ BIEN
description: Use cuando tests tengan race conditions, timing dependencies, o fallen inconsistentemente

# ✅ BIEN
description: Use cuando implementes autenticación con React Router

# ✅ BIEN
description: Use cuando necesites migrar de Redux a Zustand sin romper la aplicación
```

### ❌ Evitar Workflow Summary

```yaml
# ❌ MAL - Resume proceso
description: Use para TDD - escribe test, falla, código, refactor

# ❌ MAL - Demasiado proceso
description: Guía de migración que detecta código legacy, genera codemods, y verifica

# ❌ MAL - Primera persona
description: Te ayudo a escribir tests cuando tengas código flaky
```

---

## Keywords Efectivos

### Categorías de Keywords

| Tipo             | Ejemplos                                     |
| ---------------- | -------------------------------------------- |
| **Errores**      | "ENOTEMPTY", "timeout", "race condition"     |
| **Síntomas**     | "flaky", "hanging", "lento", "inconsistente" |
| **Herramientas** | "React", "Prisma", "Redux", "Zustand"        |
| **Acciones**     | "migrar", "refactorizar", "convertir"        |
| **Contextos**    | "authentication", "database", "API"          |

### Ejemplos por Tipo de Skill

**Skill de Disciplina:**

```yaml
description: Use cuando implementes features o fixes, antes de escribir código de implementación. Keywords: TDD, test first, red green refactor
```

**Skill Técnica:**

```yaml
description: Use cuando necesites migrar Redux clásico a Zustand. Detecta connect(), mapStateToProps, reducers legacy. Keywords: redux migration, zustand, estado global
```

**Skill de Referencia:**

```yaml
description: Use cuando trabajes con documentos PDF - extracción, creación, formularios. Keywords: pdf, pdfplumber, pypdf, formularios pdf
```

---

## Estructura del Description

### Template

```yaml
description: Use cuando [situación/síntoma]. [Contexto adicional]. Keywords: [lista].
```

### Límites

- **Máximo:** 1024 caracteres
- **Recomendado:** < 500 caracteres
- **Formato:** Tercera persona

### Ejemplos Completos

```yaml
# Skill de Migración
description: Use cuando necesites migrar de React 16/17/18 a React 19 sin romper la aplicación. Cubre breaking changes, codemods, patrones incrementales. Keywords: react migration, react 19, breaking changes.

# Skill de Testing
description: Use cuando tests fallen inconsistentemente, tengan race conditions, o dependan de timing. Keywords: flaky tests, race condition, async testing, timeout.

# Skill de Arquitectura
description: Use cuando diseñes sistema nuevo o evalúes trade-offs arquitectónicos. Keywords: architecture, system design, ADR, decision record.
```

---

## Optimización por Ubicación

### En SKILL.md Body

Además del description, incluir keywords en:

1. **Overview** - Primera sección
2. **When to Use** - Lista de síntomas
3. **Common Mistakes** - Errores frecuentes
4. **Headers** - Títulos descriptivos

### Keywords Naturales

```markdown
## When to Use

- Tests que fallan **inconsistentemente**
- **Race conditions** en async code
- **Timeouts** inexplicables
- Comportamiento **flaky** en CI
```

---

## Cross-Referencing

### Cómo Referenciar Otras Skills

```markdown
# ✅ BIEN - Solo nombre

**REQUIRED:** Use test-driven-development skill primero

# ✅ BIEN - Con marcador

**REQUIRED BACKGROUND:** Entender systematic-debugging

# ❌ MAL - Path completo

Ver skills/testing/test-driven-development

# ❌ MAL - Force-load con @

@skills/testing/tdd/SKILL.md
```

**Por qué:** `@` force-loads archivos, consumiendo contexto innecesariamente.

---

## Token Efficiency

### Targets por Tipo

| Tipo            | Objetivo       |
| --------------- | -------------- |
| Getting-started | < 150 palabras |
| Frecuentes      | < 200 palabras |
| Normales        | < 500 palabras |

### Técnicas

1. **Cross-references** en vez de repetir
2. **Mover a references/** contenido > 100 líneas
3. **Un ejemplo excelente** > muchos mediocres
4. **--help de scripts** para detalles

---

## Checklist CSO

- [ ] Description empieza con "Use cuando..."
- [ ] Description NO resume workflow
- [ ] Description en tercera persona
- [ ] Keywords incluidos al final
- [ ] < 500 caracteres (recomendado)
- [ ] Síntomas específicos mencionados
- [ ] Herramientas relevantes listadas
- [ ] Cross-references sin @ links
