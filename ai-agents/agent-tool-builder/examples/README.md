# Ejemplos de agent-tool-builder

Esta carpeta contiene ejemplos prácticos que demuestran cómo usar el skill `agent-tool-builder`.

## Contenido

| Archivo                    | Descripción                          | Complejidad      |
| -------------------------- | ------------------------------------ | ---------------- |
| `minimal_example.py`       | Patrón mínimo viable                 | ⭐ Básico        |
| `external_api_example.py`  | Manejo de APIs externas, rate limits | ⭐⭐ Intermedio  |
| `manage_notes.py`          | CRUD completo con MCP                | ⭐⭐⭐ Avanzado  |
| `practical_example.md`     | Guía paso a paso                     | 📚 Documentación |
| `manage_notes_schema.json` | JSON Schema validado                 | 📄 Referencia    |

## Quick Start

```bash
# Empezar con el ejemplo mínimo
python3 minimal_example.py

# Luego ver patrones de API externa
python3 external_api_example.py

# Finalmente, el ejemplo completo
python3 manage_notes.py --test
```

- ✅ Descripción clara con INPUTS/RETURNS/ERRORS
- ✅ Tipos específicos con constraints (enum, minLength, maxLength, pattern)
- ✅ Errores estructurados con `suggestions` para ayudar al LLM
- ✅ Validaciones según la acción requerida
- ✅ Sin fallos silenciosos

## Uso Rápido

```bash
# Ejecutar tests (8 escenarios)
python3 manage_notes.py --test

# Modo interactivo
python3 manage_notes.py --interactive

# Como servidor MCP (requiere: pip install fastmcp)
python3 manage_notes.py --mcp
```

## Validar el Schema

```bash
# Desde la raíz del skill
python3 scripts/validate_tool_schema.py examples/manage_notes_schema.json

# Salida esperada:
# ✅ Schema is valid and follows all best practices!
```

## Workflow Demostrado

1. **Definir propósito** → ¿Qué hace? ¿Inputs? ¿Outputs? ¿Errores?
2. **Generar template** → Usar `scripts/generate_tool_template.py`
3. **Diseñar schema** → Tipos específicos, constraints, enums
4. **Escribir descripción** → Template: `[ACTION] [WHAT]. INPUTS: [...]. RETURNS: [...]. ERRORS: [...]`
5. **Implementar errores** → Estructurados con `type`, `message`, `suggestions`
6. **Validar** → `scripts/validate_tool_schema.py`
7. **Testing** → Happy path + edge cases + error recovery

## Principios Clave

> **El LLM nunca ve tu código, solo ve el schema y la descripción.**
>
> Una herramienta con código perfecto pero descripción vaga **fallará**.
> Una herramienta simple con documentación clara **funcionará**.

## Ver También

- [SKILL.md](../SKILL.md) - Documentación completa del skill
- [references/](../references/) - Guías detalladas de JSON Schema, MCP, errores
- [assets/templates/](../assets/templates/) - Templates reutilizables
