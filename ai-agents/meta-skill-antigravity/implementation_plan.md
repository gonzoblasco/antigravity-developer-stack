# Plan de Refactorización: meta-skill-antigravity

## Objetivo

Refactorizar el skill `meta-skill-antigravity` para que:

1. **Practique lo que predica** (incluya sus propios artifacts TDD)
2. **Funcione en Antigravity** (rutas actualizadas)
3. **Sea increíble** (ejemplo práctico paso a paso)

---

## Estado Actual

| Archivo                                                                                                                    | Líneas  | Estado                      |
| -------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------------- |
| [SKILL.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/meta-skill-antigravity/SKILL.md)                           | 403     | ⚠️ Rutas incorrectas        |
| [init_skill.py](file:///Users/gonzoblasco/.gemini/antigravity/skills/meta-skill-antigravity/scripts/init_skill.py)         | 307     | ⚠️ Default `.agent/skills/` |
| [validate_skill.py](file:///Users/gonzoblasco/.gemini/antigravity/skills/meta-skill-antigravity/scripts/validate_skill.py) | 297     | ⚠️ Default `.agent/skills/` |
| references/                                                                                                                | 3 files | ✅ OK                       |
| templates/                                                                                                                 | 3 files | ✅ OK                       |

---

## User Review Required

> [!IMPORTANT]
> **Rutas Antigravity**: Cambiaremos el default de `.agent/skills/` a `~/.gemini/antigravity/skills/`. Esto afecta solo los defaults, los scripts seguirán aceptando `--path` para cualquier ubicación.

> [!CAUTION]
> **Breaking Change en Scripts**: Si usas los scripts actuales con los defaults, fallarán en Antigravity. El refactor corrige esto.

---

## Proposed Changes

### 1. Estructura de Directorios

```
meta-skill-antigravity/
├── SKILL.md                    # [MODIFY] Simplificar + rutas correctas
├── task.md                     # [COPY] Desde brain/
├── implementation_plan.md      # [COPY] Desde brain/
├── walkthrough.md              # [NEW] Documentar proceso
├── references/
│   ├── testing-methodology.md  # [OK]
│   ├── cso-optimization.md     # [OK]
│   ├── skill-types.md          # [OK]
│   └── antigravity-paths.md    # [NEW] Guía de rutas
├── scripts/
│   ├── init_skill.py           # [MODIFY] Autodetección rutas
│   └── validate_skill.py       # [MODIFY] Autodetección rutas
├── templates/                  # [OK]
└── examples/                   # [NEW]
    └── creating-hello-world-skill.md  # [NEW] Walkthrough completo
```

---

### 2. Modificaciones en SKILL.md

#### [MODIFY] [SKILL.md](file:///Users/gonzoblasco/.gemini/antigravity/skills/meta-skill-antigravity/SKILL.md)

**Cambios:**

1. **Description simplificada** (CSO optimizado):

```yaml
# Antes (193 chars):
description: Use cuando necesites crear, editar o validar skills para Google Antigravity. Combina metodología oficial de Anthropic con TDD para documentación. Incluye progressive disclosure, CSO, testing con subagentes. 100% compatible con Antigravity.

# Después (~120 chars):
description: Use cuando necesites crear, editar o validar skills para Antigravity. Keywords: crear skill, validar skill, TDD documentación, nueva skill, meta-skill.
```

2. **Rutas actualizadas**:

```bash
# Antes:
python scripts/init_skill.py <skill-name> --path .agent/skills/

# Después:
python scripts/init_skill.py <skill-name>  # Auto-detecta ~/.gemini/antigravity/skills/
```

3. **Sección nueva: Quick Example** inline con link a ejemplo completo

4. **Reducir a ~350 líneas** moviendo detalles a references/

---

### 3. Modificaciones en Scripts

#### [MODIFY] [init_skill.py](file:///Users/gonzoblasco/.gemini/antigravity/skills/meta-skill-antigravity/scripts/init_skill.py)

**Cambios principales:**

```python
# Nueva función para autodetección de ruta
def get_default_skills_path() -> Path:
    """Detecta ruta de skills según entorno."""
    # 1. Antigravity: ~/.gemini/antigravity/skills/
    antigravity_path = Path.home() / ".gemini" / "antigravity" / "skills"
    if antigravity_path.exists():
        return antigravity_path

    # 2. Claude Code: .agent/skills/ (legacy)
    agent_path = Path.cwd() / ".agent" / "skills"
    if agent_path.exists():
        return agent_path

    # 3. Default: Antigravity
    return antigravity_path

# Actualizar default en argparser
parser.add_argument(
    "--path", "-p",
    default=None,  # None triggers autodetection
    help="Directorio donde crear la skill (default: auto-detecta)"
)
```

#### [MODIFY] [validate_skill.py](file:///Users/gonzoblasco/.gemini/antigravity/skills/meta-skill-antigravity/scripts/validate_skill.py)

**Mismos cambios de autodetección de ruta.**

---

### 4. Nuevos Archivos

#### [NEW] examples/creating-hello-world-skill.md

Walkthrough completo de crear un skill desde cero:

```markdown
# Ejemplo: Creando "hello-world" Skill

## Paso 1: Planificación

[5 preguntas respondidas]

## Paso 2: Inicialización

[Comando + output esperado]

## Paso 3: RED Phase

[Baseline documentado]

## Paso 4: GREEN Phase

[SKILL.md editado]

## Paso 5: REFACTOR Phase

[Loopholes cerrados]

## Paso 6: Deploy

[Validación + commit]
```

#### [NEW] references/antigravity-paths.md

Documentación de rutas y diferencias Antigravity vs Claude Code.

---

## Verification Plan

### Automated Tests

```bash
# 1. Validar estructura del skill refactorizado
cd ~/.gemini/antigravity/skills/meta-skill-antigravity
python scripts/validate_skill.py meta-skill-antigravity --validate --path ~/.gemini/antigravity/skills/

# 2. Probar autodetección de rutas
python scripts/init_skill.py test-skill-temp --path /tmp/test-skills/
# Verificar que se crea correctamente

# 3. Contar líneas de SKILL.md
wc -l SKILL.md
# Debe ser < 500 (objetivo: ~350)
```

### Manual Verification

1. **Crear skill de prueba con script actualizado:**
   - Ejecutar `init_skill.py` sin `--path`
   - Verificar que usa `~/.gemini/antigravity/skills/`

2. **Validar que el ejemplo funciona:**
   - Seguir paso a paso `examples/creating-hello-world-skill.md`
   - Verificar que cada paso es claro y reproducible

3. **Verificar artifacts TDD copiados:**
   - Confirmar que `task.md`, `implementation_plan.md`, `walkthrough.md` están en el directorio del skill

---

## Estimación de Trabajo

| Fase                    | Archivos       | Tiempo Est. |
| ----------------------- | -------------- | ----------- |
| GREEN: SKILL.md         | 1              | 15 min      |
| GREEN: Scripts          | 2              | 20 min      |
| GREEN: Nuevo ejemplo    | 1              | 15 min      |
| GREEN: Nueva referencia | 1              | 10 min      |
| REFACTOR: Pulido        | All            | 15 min      |
| VERIFY: Tests           | -              | 15 min      |
| **Total**               | **6 archivos** | **~90 min** |

---

## Checklist Final

- [ ] SKILL.md < 500 líneas (objetivo ~350)
- [ ] Description concisa con keywords
- [ ] Scripts con autodetección de rutas
- [ ] Ejemplo práctico completo
- [ ] Artifacts TDD propios incluidos
- [ ] Todos los tests pasan
