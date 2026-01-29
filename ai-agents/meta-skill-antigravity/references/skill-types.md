# Tipos de Skills

## Overview

Las skills se clasifican en 3 tipos según su propósito. Cada tipo requiere diferente enfoque de testing y estructura.

---

## 1. Guardrail Skills (Disciplina)

### Propósito

Prevenir errores críticos. Enfuerzan reglas que, si se violan, causan problemas serios.

### Características

| Aspecto     | Valor                                |
| ----------- | ------------------------------------ |
| Enforcement | Mental "DEBE"                        |
| Prioridad   | Critical/High                        |
| Testing     | Pressure scenarios                   |
| Contenido   | Reglas + tablas de racionalizaciones |

### Ejemplos

- `test-driven-development` - Enforce TDD cycle
- `verification-before-completion` - Verificar antes de claims
- `systematic-debugging` - Debug metódico
- `receiving-code-review` - Procesar feedback correctamente

### Estructura Típica

```markdown
---
name: mi-guardrail
description: Use cuando [situación que requiere disciplina]
---

# Nombre

## The Iron Law

[Regla principal, clara e inmutable]

## Process

[Pasos a seguir]

## Red Flags - STOP

[Lista de señales de violación]

## Rationalizations Table

| Excusa | Realidad |
| ------ | -------- |

## Sin Excepciones

[Lista de "no aplica porque..." comunes]
```

### Testing

**Pressure Scenarios con múltiples presiones:**

1. Tiempo ("deadline en 1 hora")
2. Sunk cost ("ya escribí 200 líneas")
3. Autoridad ("el lead dijo...")
4. Fatiga ("quinto bug del día")

**Proceso:**

1. Ejecutar SIN skill bajo presión
2. Documentar racionalizaciones verbatim
3. Escribir skill con counters explícitos
4. Re-ejecutar CON skill
5. Cerrar loopholes nuevos

---

## 2. Domain Skills (Técnica)

### Propósito

Guía comprehensiva para áreas específicas. Enseñan cómo hacer algo correctamente.

### Características

| Aspecto     | Valor                             |
| ----------- | --------------------------------- |
| Enforcement | Advisory                          |
| Prioridad   | Medium/High                       |
| Testing     | Application scenarios             |
| Contenido   | Patrones + ejemplos + referencias |

### Ejemplos

- `react-patterns` - Patrones modernos de React
- `api-security-best-practices` - Seguridad en APIs
- `database-design` - Diseño de schemas
- `redux-migration-rtk-zustand` - Guía de migración

### Estructura Típica

```markdown
---
name: mi-domain-skill
description: Use cuando [contexto técnico específico]. Keywords: [lista]
---

# Nombre

## Overview

[Qué es y principio core]

## When to Use

[Síntomas y contextos]

## Quick Start

[Ejemplo mínimo funcional]

## Patterns

[Patrones principales con código]

## Common Mistakes

[Errores frecuentes y fixes]

## References

[Links a documentación extendida]
```

### Testing

**Application Scenarios:**

1. **Básico** - ¿Puede aplicar correctamente?
2. **Edge cases** - ¿Maneja variaciones?
3. **Gaps** - ¿Faltan instrucciones?

**Proceso:**

1. Crear escenario de aplicación
2. Ejecutar SIN skill
3. Identificar gaps o errores
4. Escribir skill cubriendo gaps
5. Re-ejecutar CON skill
6. Verificar aplicación correcta

---

## 3. Reference Skills (Documentación)

### Propósito

Documentación de APIs, sintaxis, comandos. Referencia para consulta rápida.

### Características

| Aspecto     | Valor                      |
| ----------- | -------------------------- |
| Enforcement | Informational              |
| Prioridad   | Low/Medium                 |
| Testing     | Retrieval scenarios        |
| Contenido   | APIs + sintaxis + ejemplos |

### Ejemplos

- `pdf-official` - Manipulación de PDFs
- `docx-official` - Documentos Word
- `pptx-official` - Presentaciones
- `mcp-builder` - Crear MCP servers

### Estructura Típica

```markdown
---
name: mi-reference
description: Use cuando trabajes con [tecnología]. Keywords: [comandos, librerías]
---

# Nombre

## Overview

[Qué cubre esta referencia]

## Quick Reference

[Tabla de operaciones comunes]

## Detailed API

[Documentación por función/método]

## Examples

[Casos de uso comunes]

## Troubleshooting

[Problemas frecuentes]
```

### Testing

**Retrieval Scenarios:**

1. **Retrieval** - ¿Encuentra info correcta?
2. **Application** - ¿La aplica bien?
3. **Coverage** - ¿Casos comunes cubiertos?

**Proceso:**

1. Crear query típica de búsqueda
2. Ejecutar SIN skill
3. Verificar si encontró info
4. Ejecutar CON skill
5. Verificar mejora
6. Añadir casos faltantes

---

## Matriz de Decisión

| Pregunta                    | Guardrail | Domain | Reference |
| --------------------------- | --------- | ------ | --------- |
| ¿Previene errores críticos? | ✅        | ❌     | ❌        |
| ¿Enseña proceso/técnica?    | ❌        | ✅     | ❌        |
| ¿Es documentación/API?      | ❌        | ❌     | ✅        |
| ¿Requiere enforcement?      | ✅        | ⚠️     | ❌        |
| ¿Tiene rationalizations?    | ✅        | ❌     | ❌        |

---

## Templates Disponibles

- [basic-skill-template.md](../templates/basic-skill-template.md) - Domain skill genérico
- [discipline-skill-template.md](../templates/discipline-skill-template.md) - Guardrail skill
- [reference-skill-template.md](../templates/reference-skill-template.md) - Reference skill
