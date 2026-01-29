# Ejemplo Práctico: Creando una Tool MCP para Gestión de Notas

> [!TIP]
> Este ejemplo demuestra el workflow completo de `agent-tool-builder` para crear una herramienta MCP profesional.

## Objetivo

Crear una tool MCP llamada `note_manager` que permita a un agente AI:

- Crear, leer, actualizar y eliminar notas
- Buscar notas por contenido
- Etiquetar notas

---

## Paso 1: Definir Propósito (Quick Start del Skill)

Antes de escribir código, respondemos las preguntas clave:

| Pregunta                        | Respuesta                                                         |
| ------------------------------- | ----------------------------------------------------------------- |
| **¿Qué hace?**                  | Gestiona notas persistentes con operaciones CRUD + búsqueda       |
| **¿Qué INPUT requiere?**        | Acción (create/read/update/delete/search), datos de nota, filtros |
| **¿Qué OUTPUT retorna?**        | Nota(s) con id, titulo, contenido, tags, timestamps               |
| **¿Qué ERRORS pueden ocurrir?** | note_not_found, validation_error, storage_error                   |

---

## Paso 2: Generar Template Inicial

Usamos el script del skill:

```bash
python scripts/generate_tool_template.py \
  --name manage_notes \
  --type mcp \
  --params "action:string,note_id:string,title:string,content:string,tags:array"
```

---

## Paso 3: Diseñar el Schema (Aplicando Principios del Skill)

```json
{
  "name": "manage_notes",
  "description": "Gestiona notas persistentes con operaciones CRUD y búsqueda. Acepta action (enum: create|read|update|delete|search|list), note_id (string, requerido para read/update/delete), title (string 1-100 chars, requerido para create/update), content (string 1-5000 chars), tags (array de strings, max 10). Retorna {note: {id, title, content, tags, created_at, updated_at}, status: string}. Lanza 'note_not_found' si note_id no existe, 'validation_error' si faltan campos requeridos.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["create", "read", "update", "delete", "search", "list"],
        "description": "Operación a realizar sobre las notas"
      },
      "note_id": {
        "type": "string",
        "description": "ID único de la nota (requerido para read/update/delete)",
        "pattern": "^[a-zA-Z0-9_-]+$"
      },
      "title": {
        "type": "string",
        "description": "Título de la nota (1-100 caracteres)",
        "minLength": 1,
        "maxLength": 100
      },
      "content": {
        "type": "string",
        "description": "Contenido de la nota (1-5000 caracteres)",
        "minLength": 1,
        "maxLength": 5000
      },
      "tags": {
        "type": "array",
        "items": {
          "type": "string",
          "maxLength": 30
        },
        "maxItems": 10,
        "description": "Etiquetas para categorizar la nota"
      },
      "query": {
        "type": "string",
        "description": "Término de búsqueda para action=search",
        "maxLength": 100
      }
    },
    "required": ["action"]
  }
}
```

### Principios Aplicados ✅

- **Tipos específicos con constraints** (minLength, maxLength, enum, pattern)
- **Descripción clara** para cada campo
- **Solo `action` es required** - otros dependen de la operación
- **`enum` para opciones finitas** en action

---

## Paso 4: Implementar la Tool MCP

```python
#!/usr/bin/env python3
"""
Note Manager MCP Tool

Gestiona notas persistentes con operaciones CRUD y búsqueda.
Demuestra mejores prácticas de agent-tool-builder.
"""

from fastmcp import FastMCP
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import os
import uuid

mcp = FastMCP("note-manager")

# Almacenamiento simple en JSON (producción usaría DB)
NOTES_FILE = os.path.expanduser("~/.notes_data.json")


def load_notes() -> Dict[str, Any]:
    """Carga notas desde almacenamiento."""
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE) as f:
            return json.load(f)
    return {}


def save_notes(notes: Dict[str, Any]) -> None:
    """Persiste notas a almacenamiento."""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2, default=str)


def create_error(
    error_type: str,
    message: str,
    field: Optional[str] = None,
    suggestions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Crea respuesta de error estructurada (patrón del skill).

    Incluye:
    - type: Categoría del error
    - message: Descripción clara
    - field: Campo afectado (si aplica)
    - suggestions: Cómo resolver el error
    """
    error = {
        "type": error_type,
        "message": message
    }
    if field:
        error["field"] = field
    if suggestions:
        error["suggestions"] = suggestions
    return {"error": error, "status": "error"}


@mcp.tool()
def manage_notes(
    action: str,
    note_id: str = "",
    title: str = "",
    content: str = "",
    tags: list = None,
    query: str = ""
) -> Dict[str, Any]:
    """
    Gestiona notas persistentes con operaciones CRUD y búsqueda.

    Acepta action (enum: create|read|update|delete|search|list),
    note_id (string, requerido para read/update/delete),
    title (string 1-100 chars, requerido para create/update),
    content (string 1-5000 chars),
    tags (array de strings, max 10),
    query (string, para búsqueda).

    Retorna {note: {id, title, content, tags, created_at, updated_at}, status}.
    Lanza 'note_not_found' si note_id no existe.
    Lanza 'validation_error' si faltan campos requeridos para la acción.

    Args:
        action: Operación a realizar (create|read|update|delete|search|list)
        note_id: ID único de la nota (requerido para read/update/delete)
        title: Título de la nota (requerido para create/update)
        content: Contenido de la nota
        tags: Lista de etiquetas para categorizar
        query: Término de búsqueda (para action=search)

    Returns:
        Dict con:
            - note/notes: Datos de la nota(s)
            - status: "success" o "error"
            - (error): Objeto de error si status="error"
    """
    if tags is None:
        tags = []

    notes = load_notes()

    # === VALIDACIONES ===

    # Validar action
    valid_actions = ["create", "read", "update", "delete", "search", "list"]
    if action not in valid_actions:
        return create_error(
            "validation_error",
            f"Action '{action}' no válida",
            field="action",
            suggestions=[
                f"Usa una de las acciones válidas: {', '.join(valid_actions)}",
                "Ejemplo: action='create' para crear una nota nueva"
            ]
        )

    # Validar requerimientos por acción
    if action in ["read", "update", "delete"] and not note_id:
        return create_error(
            "validation_error",
            f"note_id es requerido para action='{action}'",
            field="note_id",
            suggestions=[
                "Proporciona el ID de la nota a operar",
                "Usa action='list' para ver todas las notas y sus IDs"
            ]
        )

    if action in ["create"] and not title:
        return create_error(
            "validation_error",
            "title es requerido para crear una nota",
            field="title",
            suggestions=[
                "Proporciona un título (1-100 caracteres)",
                "Ejemplo: title='Mi nueva nota'"
            ]
        )

    # Validar que nota existe para operaciones que la requieren
    if action in ["read", "update", "delete"] and note_id not in notes:
        return create_error(
            "note_not_found",
            f"No se encontró nota con ID '{note_id}'",
            field="note_id",
            suggestions=[
                "Verifica que el ID sea correcto",
                "Usa action='list' para ver notas existentes"
            ]
        )

    # === OPERACIONES ===

    try:
        if action == "create":
            new_id = str(uuid.uuid4())[:8]
            now = datetime.now().isoformat()

            note = {
                "id": new_id,
                "title": title[:100],  # Truncar si excede
                "content": content[:5000] if content else "",
                "tags": tags[:10] if tags else [],
                "created_at": now,
                "updated_at": now
            }

            notes[new_id] = note
            save_notes(notes)

            return {
                "note": note,
                "status": "success",
                "message": f"Nota creada con ID: {new_id}"
            }

        elif action == "read":
            return {
                "note": notes[note_id],
                "status": "success"
            }

        elif action == "update":
            note = notes[note_id]

            if title:
                note["title"] = title[:100]
            if content:
                note["content"] = content[:5000]
            if tags is not None:
                note["tags"] = tags[:10]

            note["updated_at"] = datetime.now().isoformat()
            save_notes(notes)

            return {
                "note": note,
                "status": "success",
                "message": f"Nota {note_id} actualizada"
            }

        elif action == "delete":
            deleted_note = notes.pop(note_id)
            save_notes(notes)

            return {
                "note": deleted_note,
                "status": "success",
                "message": f"Nota {note_id} eliminada"
            }

        elif action == "search":
            if not query:
                return create_error(
                    "validation_error",
                    "query es requerido para búsqueda",
                    field="query",
                    suggestions=[
                        "Proporciona un término de búsqueda",
                        "Ejemplo: query='reunión proyecto'"
                    ]
                )

            query_lower = query.lower()
            results = [
                note for note in notes.values()
                if query_lower in note["title"].lower()
                or query_lower in note.get("content", "").lower()
                or any(query_lower in tag.lower() for tag in note.get("tags", []))
            ]

            return {
                "notes": results,
                "total": len(results),
                "query": query,
                "status": "success"
            }

        elif action == "list":
            return {
                "notes": list(notes.values()),
                "total": len(notes),
                "status": "success"
            }

    except Exception as e:
        return create_error(
            "storage_error",
            f"Error al procesar la operación: {str(e)}",
            suggestions=[
                "Intenta nuevamente",
                "Verifica permisos del sistema de archivos"
            ]
        )


if __name__ == "__main__":
    mcp.run()
```

---

## Paso 5: Validar Schema

Usamos el script de validación del skill:

```bash
python scripts/validate_tool_schema.py schema.json
```

**Salida esperada:**

```
✅ Schema Validation Results
============================
✅ Tool name 'manage_notes' follows snake_case convention
✅ Description includes input format
✅ Description includes output format
✅ Description includes error conditions
✅ All string properties have maxLength
✅ Enum used for 'action' field
⚠️  Suggestion: Consider adding examples to description

Score: 9/10 - Excellent
```

---

## Paso 6: Testing (Escenarios del Skill)

### 6.1 Casos de Éxito

```python
# Test: Crear nota
result = manage_notes(
    action="create",
    title="Reunión de Sprint",
    content="Discutir avances del proyecto",
    tags=["trabajo", "sprint"]
)
assert result["status"] == "success"
assert "id" in result["note"]
```

```python
# Test: Buscar notas
result = manage_notes(
    action="search",
    query="sprint"
)
assert result["status"] == "success"
assert result["total"] >= 1
```

### 6.2 Casos de Error (Verificar Recuperación)

```python
# Test: Nota no encontrada
result = manage_notes(
    action="read",
    note_id="inexistente123"
)
assert result["status"] == "error"
assert result["error"]["type"] == "note_not_found"
assert "suggestions" in result["error"]  # ✅ Ayuda al LLM a recuperarse
```

```python
# Test: Validación faltante
result = manage_notes(
    action="create"
    # Sin title - debería fallar con sugerencia
)
assert result["error"]["field"] == "title"
assert "Proporciona un título" in result["error"]["suggestions"][0]
```

---

## Checklist de Calidad (del Skill)

| Criterio                                 | Estado |
| ---------------------------------------- | ------ |
| ✅ Descripción sigue template del skill  | ✅     |
| ✅ Tipos específicos con constraints     | ✅     |
| ✅ Enum para opciones finitas            | ✅     |
| ✅ Errores estructurados con suggestions | ✅     |
| ✅ No hay fallos silenciosos             | ✅     |
| ✅ Documentación en docstring            | ✅     |
| ✅ Testing de happy path + errores       | ✅     |

---

## Configurar en MCP

Para usar esta tool con un agente, agregar a `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "note-manager": {
      "command": "python",
      "args": ["/path/to/manage_notes.py"]
    }
  }
}
```

---

## Resumen

Este ejemplo demostró el workflow completo del skill `agent-tool-builder`:

1. **Definir propósito** antes de codificar
2. **Generar template** con el script
3. **Diseñar schema** con tipos específicos y constraints
4. **Escribir descripción** siguiendo el template del skill
5. **Implementar errores estructurados** que ayuden al LLM a recuperarse
6. **Validar** con el script del skill
7. **Testing** de casos de éxito y error

> [!IMPORTANT]
> **Recuerda:** El LLM nunca ve tu código, solo ve el schema y la descripción.
> Una herramienta con código perfecto pero descripción vaga **fallará**.
> Una herramienta simple con documentación clara **funcionará**.
