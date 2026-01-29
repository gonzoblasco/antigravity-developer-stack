# Rutas y Entornos en Antigravity

Antigravity utiliza una estructura de directorios estandarizada para skills, diferente a la de Claude Code. Este skill está diseñado para funcionar en ambos entornos mediante autodetección.

## Rutas Estándar

| Entorno                  | Ruta de Skills                  | Descripción                                              |
| ------------------------ | ------------------------------- | -------------------------------------------------------- |
| **Antigravity** (Modern) | `~/.gemini/antigravity/skills/` | Ruta global persistente recomendada por Google Deepmind. |
| **Claude Code** (Legacy) | `.agent/skills/`                | Ruta local relativa al proyecto.                         |

## Autodetección

Los scripts `init_skill.py` y `validate_skill.py` utilizan la siguiente lógica de precedencia para determinar dónde buscar o crear skills:

1. **Argumento explícito**: Si pasas `--path /ruta/custom`, siempre gana.
2. **Antigravity Global**: Si existe `~/.gemini/antigravity/skills/`, se usa por defecto.
3. **Legacy Local**: Si no existe la global pero existe `.agent/skills/` en el directorio actual, se usa esa.
4. **Fallback**: Si ninguna existe, intenta crear en `.agent/skills/` (comportamiento legacy default).

## Cómo migrar skills

Si tienes skills en `.agent/skills/` y quieres moverlos a Antigravity:

```bash
# Crear directorio global si no existe
mkdir -p ~/.gemini/antigravity/skills

# Mover skill
mv .agent/skills/mi-skill ~/.gemini/antigravity/skills/
```

Antigravity descubrirá automáticamente los skills en la ruta global gracias a su sistema de indexación.
