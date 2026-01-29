---
name: {{NOMBRE}}
description: Use cuando trabajes con [TECNOLOGÍA/API/FORMATO]. Keywords: [comandos, librerías, extensiones].
---

# {{Título}}

## Overview

[Breve descripción de qué cubre esta referencia - 1-2 oraciones]

---

## Quick Reference

### Operaciones Comunes

| Operación   | Código                |
| ----------- | --------------------- |
| [Crear]     | `funcion_crear()`     |
| [Leer]      | `funcion_leer()`      |
| [Modificar] | `funcion_modificar()` |
| [Eliminar]  | `funcion_eliminar()`  |

### Comandos Rápidos

```bash
# [Operación 1]
comando --opcion

# [Operación 2]
otro-comando --flag
```

---

## Installation

```bash
# Python
pip install [libreria]

# Node
npm install [package]
```

---

## API Reference

### Función Principal

```python
def funcion_principal(param1: str, param2: int = 0) -> Result:
    """
    [Descripción breve]

    Args:
        param1: [Descripción]
        param2: [Descripción] (default: 0)

    Returns:
        Result: [Descripción del retorno]

    Raises:
        ValueError: [Cuándo se lanza]
    """
```

### Función Secundaria

```python
def funcion_secundaria(data: dict) -> bool:
    """
    [Descripción]
    """
```

---

## Examples

### Caso de Uso 1: [Nombre]

```python
# Ejemplo completo y funcional
from libreria import funcion

resultado = funcion(param="valor")
print(resultado)
```

### Caso de Uso 2: [Nombre]

```python
# Otro ejemplo
```

---

## Configuration

### Opciones Disponibles

| Opción    | Tipo | Default | Descripción   |
| --------- | ---- | ------- | ------------- |
| `opcion1` | str  | `""`    | [Descripción] |
| `opcion2` | bool | `True`  | [Descripción] |

### Ejemplo de Configuración

```python
config = {
    "opcion1": "valor",
    "opcion2": False
}
```

---

## Troubleshooting

### Errores Comunes

| Error        | Causa   | Solución   |
| ------------ | ------- | ---------- |
| `ErrorTipo1` | [Causa] | [Solución] |
| `ErrorTipo2` | [Causa] | [Solución] |

### Debug Tips

```python
# Habilitar logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## References

- [Documentación oficial](https://...)
- [advanced.md](references/advanced.md) - API completa
