---
name: meta-skill-antigravity
description: Use cuando necesites crear, editar o validar skills para Antigravity. Keywords: crear skill, validar skill, TDD documentación, nueva skill, meta-skill.
---

# Meta Skill Creator - Antigravity Edition

## Overview

**Crear skills ES Test-Driven Development aplicado a documentación.**

Este skill sintetiza el enfoque oficial para crear skills robustos y mantenibles en Antigravity.

> [!IMPORTANT]
> **Rutas Antigravity**: Los scripts de este skill detectan automáticamente tu entorno. Por defecto usan `~/.gemini/antigravity/skills/`.

---

## Quick Example (30 seg)

```bash
# 1. Crear estructura básica
python scripts/init_skill.py hello-world

# 2. Ejecutar baseline (ver cómo falla sin el skill)
python scripts/validate_skill.py hello-world --baseline

# 3. Iterar editando SKILL.md hasta pasar el test
python scripts/validate_skill.py hello-world --test
```

[Ver ejemplo completo paso a paso](examples/creating-hello-world-skill.md)

---

## 5 Pasos para un Skill Increíble

### 1. Entender el Problema

Antes de escribir, define claramente:

- **Trigger**: ¿Cuándo EXACTAMENTE debe activarse?
- **Keywords**: ¿Qué palabras usa el usuario cuando tiene este problema?
- **Tipo**: ¿Es guía técnica (Domain) o regla de disciplina (Guardrail)?

### 2. Inicializar

```bash
python scripts/init_skill.py <nombre-kebab-case>
```

Esto crea `SKILL.md`, directorios y templates necesarios.

### 3. RED: Baseline (Critical)

**LA LEY DE HIERRO**: No skill without failing test first.

1. Desactiva el skill (o no lo crees aún en `.agent/skills` o repo oficial).
2. Presenta al agente el problema que el skill debe resolver (Pressure Scenario).
3. Documenta: ¿Qué hizo mal? ¿Qué excusas (racionalizaciones) dio?
4. Guarda esto en `task.md` o `implementation_plan.md` del skill.

### 4. GREEN: Implementar Mínimo

Edita `SKILL.md` para contrarrestar _específicamente_ las fallas del baseline.

- Si el agente dijo "es muy simple para testear", añade una regla explícita: "Nunca es demasiado simple".
- Si inventó una librería, añade documentación de referencia correcta.

### 5. REFACTOR & Verify

Vuelve a ejecutar el escenario (Test).

- ¿Siguió las instrucciones? -> ✅ Deploy.
- ¿Encontró una nueva excusa? -> Añade contra-medida y repite.

---

## Estructura de una Skill

```
skill-name/
├── SKILL.md              # Core (requerido, < 500 líneas)
├── task.md               # Tracking de creación (copiar del brain)
├── implementation_plan.md # Plan TDD (copiar del brain)
├── walkthrough.md        # Registro final (copiar del brain)
├── references/           # Documentación extendida
├── scripts/              # Código ejecutable
├── templates/            # Plantillas reutilizables
└── examples/             # Ejemplos prácticos paso a paso
```

### SKILL.md Frontmatter Ideal

```yaml
---
name: mi-skill
description: Use cuando [SITUACIÓN ESPECÍFICA]. Keywords: [palabra1, palabra2].
---
```

> [!TIP]
> **Description = Trigger, NO Resumen**.
> ❌ "Use para crear APIs con FastAPI siguiendo patrones..."
> ✅ "Use cuando crees APIs con FastAPI. Keywords: api, rest, endpoint."

---

## Core Principles

### 1. Progressive Disclosure

No abrumes al contexto.

- **Nivel 1 (Always on)**: `description` y keywords.
- **Nivel 2 (Activated)**: `SKILL.md` (< 500 líneas).
- **Nivel 3 (On demand)**: Archivos en `references/` (ilimitado).

### 2. Claude Search Optimization (CSO)

Antigravity decide qué skill cargar basándose EXCLUSIVAMENTE en la `description`.

- Sé específico sobre el CUÁNDO.
- Incluye nombres de errores, tecnologías y acciones clave.

### 3. Bulletproofing (Disciplina)

Si el skill es para evitar errores humanos (ej. TDD, Debugging):

- Anticipa las excusas ("racionalizaciones").
- Usa tablas de "Excusa vs Realidad".
- Sé imperativo y absoluto ("Borrar significa borrar").

---

## Scripts y Herramientas

Todos los scripts soportan autodetección de rutas (`~/.gemini/antigravity/skills` o `.agent/skills`).

```bash
# Inicializar
python scripts/init_skill.py <nombre>

# Validar estructura y reglas
python scripts/validate_skill.py <nombre> --validate

# Guías de Testing
python scripts/validate_skill.py <nombre> --baseline
python scripts/validate_skill.py <nombre> --test
```

---

## Referencias

- [Testing Methodology TDD](references/testing-methodology.md)
- [Rutas y Entornos](references/antigravity-paths.md)
- [Tipos de Skill (Guardrail vs Domain)](references/skill-types.md)
- [CSO Optimization](references/cso-optimization.md)

---

## The Iron Law

```
NO SKILL WITHOUT FAILING TEST FIRST
```

Aplica a skills NUEVAS y EDICIONES importantes.
Si no puedes probar que falla sin el skill, tal vez no necesitas el skill.
