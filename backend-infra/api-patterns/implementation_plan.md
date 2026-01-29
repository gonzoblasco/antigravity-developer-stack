# Plan de Refactorización: api-patterns

> Siguiendo metodología TDD de `meta-skill-antigravity`

---

## Diagnóstico Actual

| Criterio            | Estado       | Acción                    |
| ------------------- | ------------ | ------------------------- |
| Estructura SKILL.md | ✅ 82 líneas | Mantener                  |
| Description YAML    | ❌ No CSO    | **Reescribir**            |
| Keywords            | ❌ Faltan    | **Agregar**               |
| Archivos referencia | ⚠️ Sueltos   | **Mover a `references/`** |
| TDD Artifacts       | ❌ Faltan    | **Crear**                 |
| Pressure Testing    | ❌ Nunca     | **Ejecutar**              |

---

## Cambios Propuestos

### 1. YAML Frontmatter (CSO)

**Antes:**

```yaml
description: API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination.
```

**Después:**

```yaml
description: Use cuando diseñes APIs, elijas entre REST/GraphQL/tRPC, definas formatos de respuesta, o planifiques versionado. Keywords: API design, REST, GraphQL, tRPC, OpenAPI, versioning, pagination, rate limiting, authentication.
```

> [!IMPORTANT]
> La description actual describe QUÉ hace el skill, no CUÁNDO usarla. CSO requiere triggering conditions.

---

### 2. Reorganización de Archivos

**Estructura actual:**

```
api-patterns/
├── SKILL.md
├── api-style.md      # ← suelto
├── auth.md           # ← suelto
├── rest.md           # ← suelto
├── ...
└── scripts/
```

**Estructura propuesta:**

```
api-patterns/
├── SKILL.md
├── task.md
├── implementation_plan.md
├── walkthrough.md
├── references/
│   ├── api-style.md
│   ├── auth.md
│   ├── rest.md
│   ├── response.md
│   ├── graphql.md
│   ├── trpc.md
│   ├── versioning.md
│   ├── rate-limiting.md
│   ├── documentation.md
│   └── security-testing.md
└── scripts/
    └── api_validator.py
```

---

### 3. Mejoras a SKILL.md

#### 3.1 Content Map actualizado

Actualizar rutas en la tabla para reflejar `references/`:

```markdown
| File                      | Description                           | When to Read      |
| ------------------------- | ------------------------------------- | ----------------- |
| `references/api-style.md` | REST vs GraphQL vs tRPC decision tree | Choosing API type |
```

#### 3.2 Agregar Quick Decision Flowchart

Mover el decision tree de `api-style.md` a SKILL.md para visibilidad inmediata:

```markdown
## Quick Decision

┌─ Public API? ─────────────→ REST + OpenAPI
├─ Complex data + Multiple FE? → GraphQL  
├─ TS Monorepo? ────────────→ tRPC
└─ Real-time? ──────────────→ WebSocket
```

#### 3.3 Tabla de Racionalizaciones

Agregar sección específica de "trampas mentales":

```markdown
## Racionalizaciones Comunes

| Excusa                      | Realidad                           |
| --------------------------- | ---------------------------------- |
| "Siempre usamos REST"       | Evalúa consumidores primero        |
| "GraphQL es overkill"       | Para apps complejas, ahorra tiempo |
| "No necesitamos versionado" | Clients romperán sin aviso         |
```

---

### 4. Eliminación de `allowed-tools`

```yaml
# Antes
allowed-tools: Read, Write, Edit, Glob, Grep

# Después
# (eliminar - no es necesario para Antigravity)
```

> [!NOTE]
> `allowed-tools` es específico de Claude Code. En Antigravity no tiene efecto.

---

## Verificación

### Automated

- [ ] `SKILL.md` < 500 líneas
- [ ] Todos los archivos movidos a `references/`
- [ ] Links en Content Map actualizados

### Manual

- [ ] Activar skill con "diseñar API REST"
- [ ] Verificar que carga solo archivos necesarios
- [ ] Probar decision checklist en proyecto real

---

## Riesgos

| Riesgo               | Mitigación                               |
| -------------------- | ---------------------------------------- |
| Links rotos          | Actualizar Content Map al mover archivos |
| Pérdida de contenido | Git backup antes de cambios              |

---

## Estimación

| Fase              | Tiempo       |
| ----------------- | ------------ |
| Quick Wins        | 15 min       |
| Mejoras Contenido | 30 min       |
| TDD Validation    | 45 min       |
| Calidad Final     | 15 min       |
| **Total**         | **~2 horas** |
