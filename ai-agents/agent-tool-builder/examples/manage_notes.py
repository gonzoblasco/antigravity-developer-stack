#!/usr/bin/env python3
"""
Note Manager MCP Tool - Ejemplo Práctico

Gestiona notas persistentes con operaciones CRUD y búsqueda.
Demuestra mejores prácticas de agent-tool-builder.

Uso:
    # Como servidor MCP
    python manage_notes.py
    
    # Testing directo
    python manage_notes.py --test
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import os
import uuid
import argparse

# Almacenamiento simple en JSON (producción usaría DB)
NOTES_FILE = os.path.expanduser("~/.notes_demo_data.json")


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


def run_tests():
    """Ejecuta tests demostrativos."""
    print("\n" + "="*60)
    print("🧪 Testing manage_notes - Ejemplo agent-tool-builder")
    print("="*60 + "\n")
    
    # Limpiar datos previos para tests limpios
    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)
    
    tests_passed = 0
    tests_failed = 0
    
    def test(name: str, condition: bool, result: Dict):
        nonlocal tests_passed, tests_failed
        if condition:
            print(f"✅ {name}")
            tests_passed += 1
        else:
            print(f"❌ {name}")
            print(f"   Resultado: {json.dumps(result, indent=2)}")
            tests_failed += 1
    
    # Test 1: Crear nota
    print("📝 Test CREATE:")
    result = manage_notes(
        action="create",
        title="Reunión de Sprint",
        content="Discutir avances del proyecto",
        tags=["trabajo", "sprint"]
    )
    test("Crear nota exitosamente", 
         result["status"] == "success" and "id" in result["note"],
         result)
    created_id = result.get("note", {}).get("id", "")
    
    # Test 2: Leer nota
    print("\n📖 Test READ:")
    result = manage_notes(action="read", note_id=created_id)
    test("Leer nota existente",
         result["status"] == "success" and result["note"]["title"] == "Reunión de Sprint",
         result)
    
    # Test 3: Actualizar nota
    print("\n✏️ Test UPDATE:")
    result = manage_notes(
        action="update",
        note_id=created_id,
        title="Reunión de Sprint Actualizada",
        tags=["trabajo", "sprint", "urgente"]
    )
    test("Actualizar nota",
         result["status"] == "success" and "urgente" in result["note"]["tags"],
         result)
    
    # Test 4: Buscar nota
    print("\n🔍 Test SEARCH:")
    result = manage_notes(action="search", query="sprint")
    test("Buscar por término",
         result["status"] == "success" and result["total"] >= 1,
         result)
    
    # Test 5: Listar notas
    print("\n📋 Test LIST:")
    result = manage_notes(action="list")
    test("Listar todas las notas",
         result["status"] == "success" and result["total"] >= 1,
         result)
    
    # Test 6: Error - nota no encontrada
    print("\n⚠️ Test ERROR - Nota no encontrada:")
    result = manage_notes(action="read", note_id="inexistente123")
    test("Error estructurado con suggestions",
         result["status"] == "error" 
         and result["error"]["type"] == "note_not_found"
         and "suggestions" in result["error"],
         result)
    
    # Test 7: Error - validación
    print("\n⚠️ Test ERROR - Validación:")
    result = manage_notes(action="create")  # Sin title
    test("Validación de campo requerido",
         result["status"] == "error"
         and result["error"]["field"] == "title"
         and "suggestions" in result["error"],
         result)
    
    # Test 8: Eliminar nota
    print("\n🗑️ Test DELETE:")
    result = manage_notes(action="delete", note_id=created_id)
    test("Eliminar nota",
         result["status"] == "success",
         result)
    
    # Resumen
    print("\n" + "="*60)
    print(f"📊 Resultados: {tests_passed} pasados, {tests_failed} fallados")
    print("="*60)
    
    if tests_failed == 0:
        print("\n🎉 ¡Todos los tests pasaron!")
        print("\n💡 Este ejemplo demuestra:")
        print("   • Descripción clara siguiendo template del skill")
        print("   • Tipos específicos con constraints")
        print("   • Errores estructurados con suggestions")
        print("   • Sin fallos silenciosos")
    
    # Cleanup
    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)


def run_interactive():
    """Modo interactivo para probar la tool."""
    print("\n" + "="*60)
    print("🎯 Note Manager - Modo Interactivo")
    print("="*60)
    print("\nComandos disponibles:")
    print("  create <titulo> [contenido] [tags separados por coma]")
    print("  read <id>")
    print("  update <id> <nuevo_titulo>")
    print("  delete <id>")
    print("  search <query>")
    print("  list")
    print("  quit")
    print()
    
    while True:
        try:
            cmd = input("📝 > ").strip()
            if not cmd:
                continue
            if cmd == "quit":
                break
            
            parts = cmd.split(maxsplit=3)
            action = parts[0]
            
            result = None
            if action == "create" and len(parts) >= 2:
                tags = parts[3].split(",") if len(parts) > 3 else []
                result = manage_notes(
                    action="create",
                    title=parts[1],
                    content=parts[2] if len(parts) > 2 else "",
                    tags=tags
                )
            elif action == "read" and len(parts) >= 2:
                result = manage_notes(action="read", note_id=parts[1])
            elif action == "update" and len(parts) >= 3:
                result = manage_notes(action="update", note_id=parts[1], title=parts[2])
            elif action == "delete" and len(parts) >= 2:
                result = manage_notes(action="delete", note_id=parts[1])
            elif action == "search" and len(parts) >= 2:
                result = manage_notes(action="search", query=parts[1])
            elif action == "list":
                result = manage_notes(action="list")
            else:
                print("Comando no reconocido. Usa: create, read, update, delete, search, list, quit")
                continue
            
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Note Manager - Ejemplo de agent-tool-builder"
    )
    parser.add_argument("--test", action="store_true", help="Ejecutar tests")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interactivo")
    parser.add_argument("--mcp", action="store_true", help="Iniciar como servidor MCP")
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
    elif args.interactive:
        run_interactive()
    elif args.mcp:
        # Solo importar FastMCP si se necesita
        try:
            from fastmcp import FastMCP
            mcp = FastMCP("note-manager")
            mcp.tool()(manage_notes)
            mcp.run()
        except ImportError:
            print("❌ FastMCP no instalado. Instala con: pip install fastmcp")
            print("   O usa --test o --interactive para probar sin MCP")
    else:
        # Por defecto, mostrar ayuda y correr tests
        parser.print_help()
        print("\n" + "-"*60)
        run_tests()


if __name__ == "__main__":
    main()
