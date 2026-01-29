#!/usr/bin/env python3
"""
init_skill.py - Inicializa estructura de nueva skill para Antigravity

Uso:
    python init_skill.py <nombre-skill> --path <directorio>
    python init_skill.py --interactive
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def get_default_skills_path() -> Path:
    """Detecta ruta de skills según entorno."""
    # 1. Antigravity Global (Priority)
    antigravity_path = Path.home() / ".gemini" / "antigravity" / "skills"
    if antigravity_path.exists():
        return antigravity_path
    
    # 2. Legacy Local
    agent_path = Path.cwd() / ".agent" / "skills"
    if agent_path.exists():
        return agent_path
    
    # 3. Default fallback (for creation) -> Antigravity if we can create it, else local
    # We encourage Antigravity structure
    return antigravity_path


def create_skill_structure(name: str, path: str, skill_type: str = "domain"):
    """Crea la estructura de directorios y archivos para una nueva skill."""
    
    # Resolve path: if path is None, use autodetection
    if path is None:
        target_path = get_default_skills_path()
    else:
        target_path = Path(path)

    # Ensure target path exists
    if not target_path.exists():
        try:
            target_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"⚠️  No se pudo crear el directorio base {target_path}: {e}")
            print("   Intentando usar .agent/skills local...")
            target_path = Path.cwd() / ".agent" / "skills"
            target_path.mkdir(parents=True, exist_ok=True)

    skill_dir = target_path / name
    
    if skill_dir.exists():
        print(f"❌ Error: El directorio {skill_dir} ya existe")
        sys.exit(1)
    
    # Crear directorios
    skill_dir.mkdir(parents=True)
    (skill_dir / "references").mkdir()
    (skill_dir / "scripts").mkdir()
    (skill_dir / "templates").mkdir()
    (skill_dir / "examples").mkdir()
    
    # Seleccionar template según tipo
    templates = {
        "guardrail": get_guardrail_template(name),
        "domain": get_domain_template(name),
        "reference": get_reference_template(name)
    }
    
    skill_content = templates.get(skill_type, templates["domain"])
    
    # Crear SKILL.md
    (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
    
    # Crear README de referencias
    (skill_dir / "references" / ".gitkeep").write_text(
        "# Referencias\n\nAñadir documentación extendida aquí.\n"
    )

    # Crear artifacts placeholders
    (skill_dir / "task.md").write_text("# Task: " + name + "\n\n- [ ] Initial Analysis\n", encoding="utf-8")
    (skill_dir / "implementation_plan.md").write_text("# Plan: " + name + "\n", encoding="utf-8")
    
    print(f"""
✅ Skill '{name}' creada exitosamente en {skill_dir}

Estructura:
{name}/
├── SKILL.md          ← Editar con contenido
├── references/       ← Documentación extendida
├── scripts/          ← Código ejecutable
├── templates/        ← Plantillas reutilizables
└── examples/         ← Ejemplos prácticos

Próximos pasos:
1. Editar SKILL.md con tu contenido
2. Ejecutar baseline: python validate_skill.py {name} --baseline
3. Iterar hasta pasar tests

Tipo seleccionado: {skill_type}
""")


def get_domain_template(name: str) -> str:
    """Template para skill de tipo Domain (técnica)."""
    return f'''---
name: {name}
description: Use cuando [SITUACIÓN ESPECÍFICA]. Keywords: [lista de keywords].
---

# {name.replace("-", " ").title()}

## Overview

[Qué es y principio core en 1-2 oraciones]

## When to Use

- [Síntoma 1]
- [Síntoma 2]
- [Contexto específico]

**Cuándo NO usar:**
- [Caso que no aplica]

## Quick Start

```python
# Ejemplo mínimo funcional
```

## Patterns

### Patrón Principal

**Antes:**
```python
# Código problemático
```

**Después:**
```python
# Código mejorado
```

## Common Mistakes

| Error | Fix |
|-------|-----|
| [Error común 1] | [Solución] |
| [Error común 2] | [Solución] |

## References

- [reference-name.md](references/reference-name.md) - Documentación extendida
'''


def get_guardrail_template(name: str) -> str:
    """Template para skill de tipo Guardrail (disciplina)."""
    return f'''---
name: {name}
description: Use cuando [SITUACIÓN QUE REQUIERE DISCIPLINA]. Keywords: [lista].
---

# {name.replace("-", " ").title()}

## The Iron Law

```
[REGLA PRINCIPAL EN MAYÚSCULAS]
```

Aplica a [contextos]. Sin excepciones.

## Process

1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

## Red Flags - STOP

- [Señal de violación 1]
- [Señal de violación 2]
- "Es diferente porque..."

**Todos significan:** [Acción correctiva]

## Rationalizations Table

| Excusa | Realidad |
|--------|----------|
| "[Excusa común 1]" | [Por qué es incorrecta] |
| "[Excusa común 2]" | [Por qué es incorrecta] |

## Sin Excepciones

- No para "casos simples"
- No para "urgencias"
- No para "esta vez"

**[Regla] significa [regla]. Siempre.**
'''


def get_reference_template(name: str) -> str:
    """Template para skill de tipo Reference (documentación)."""
    return f'''---
name: {name}
description: Use cuando trabajes con [TECNOLOGÍA/API]. Keywords: [comandos, librerías].
---

# {name.replace("-", " ").title()}

## Overview

[Qué cubre esta referencia]

## Quick Reference

| Operación | Código |
|-----------|--------|
| [Operación 1] | `código` |
| [Operación 2] | `código` |

## API Reference

### Función Principal

```python
def funcion(param1, param2):
    """
    Descripción.
    
    Args:
        param1: Descripción
        param2: Descripción
    
    Returns:
        Resultado
    """
```

## Examples

### Caso de Uso Común

```python
# Ejemplo completo
```

## Troubleshooting

| Problema | Solución |
|----------|----------|
| [Error común] | [Fix] |
'''


def interactive_mode():
    """Modo interactivo para crear skill."""
    print("\\n🚀 Creador de Skills - Modo Interactivo\\n")
    
    # Nombre
    name = input("1. Nombre de la skill (kebab-case, ej: mi-skill): ").strip()
    if not name:
        print("❌ Nombre requerido")
        sys.exit(1)
    
    # Validar nombre
    if not all(c.isalnum() or c == '-' for c in name):
        print("❌ Nombre debe ser kebab-case (letras, números, guiones)")
        sys.exit(1)
    
    # Tipo
    print("\\n2. Tipo de skill:")
    print("   1) domain    - Guía técnica (patrones, how-to)")
    print("   2) guardrail - Reglas de disciplina (TDD, verification)")
    print("   3) reference - Documentación/API")
    
    type_input = input("Selecciona (1/2/3) [1]: ").strip() or "1"
    type_map = {"1": "domain", "2": "guardrail", "3": "reference"}
    skill_type = type_map.get(type_input, "domain")
    
    # Path
    default_path = get_default_skills_path()
    path_input = input(f"\\n3. Directorio [{default_path}]: ").strip()
    
    path = path_input if path_input else str(default_path)
    
    # Confirmar
    print(f"\\n📋 Resumen:")
    print(f"   Nombre: {name}")
    print(f"   Tipo: {skill_type}")
    print(f"   Path: {Path(path) / name}/")
    
    confirm = input("\\n¿Crear? (s/n) [s]: ").strip().lower() or "s"
    
    if confirm == "s":
        create_skill_structure(name, path, skill_type)
    else:
        print("Cancelado.")


def main():
    parser = argparse.ArgumentParser(
        description="Inicializa estructura de nueva skill para Antigravity"
    )
    parser.add_argument(
        "name", 
        nargs="?",
        help="Nombre de la skill (kebab-case)"
    )
    parser.add_argument(
        "--path", "-p",
        default=None,
        help="Directorio donde crear la skill (default: auto-detect)"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["domain", "guardrail", "reference"],
        default="domain",
        help="Tipo de skill"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Modo interactivo"
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.name:
        create_skill_structure(args.name, args.path, args.type)
    else:
        parser.print_help()
        print("\\n💡 Tip: Usa --interactive para modo guiado")


if __name__ == "__main__":
    main()
