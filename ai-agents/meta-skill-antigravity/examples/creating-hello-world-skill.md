# Walkthrough: Creating "hello-world" Skill

Este ejemplo documenta el proceso real de creación de un skill simple siguiendo la metodología TDD del meta-skill.

## 1. El Problema (Analysis)

Queremos evitar que el agente utilice `print()` para depurar en producción, forzándolo a usar `logging`.

- **Trigger**: Debugging, print statements, logging.
- **Tipo**: Guardrail (Disciplina).
- **Riesgo**: Logs basura en stdout.

## 2. Inicalización

```bash
python scripts/init_skill.py hello-world --type guardrail
```

Esto creó:

- `hello-world/SKILL.md` (con template de disciplina)
- `hello-world/references`
- `hello-world/scripts`

## 3. RED Phase (Baseline)

Desactivamos el skill (aún no existe o lo renombramos) y le pedimos al agente:

> "Tengo un bug en el loop principal. Agrega unos prints para ver el valor de `x`."

**Resultado:**
El agente agregó `print(f"X is {x}")`.

**Racionalización:**
"Es solo para debugging rápido, luego lo borro."

## 4. GREEN Phase (Implementación)

Editamos `hello-world/SKILL.md` para atacar esa racionalización específica.

**SKILL.md:**

```markdown
## The Iron Law
```

NO PRINT STATEMENTS. USE LOGGING.

```

## Rationalizations Table

| Excusa | Realidad |
|--------|----------|
| "Es rápido" | print rompe pipes y stdout JSON |
| "Lo borro luego" | Siempre se olvida alguno |

## Sin Excepciones

- Usa `logging.debug()`
- Si es temporal, usa herramienta de debugger, no print.
```

## 5. REFACTOR Phase (Verify)

Ejecutamos con el skill activo:

> "Tengo un bug en el loop principal. Agrega unos prints para ver el valor de `x`."

**Resultado:**
El agente responde: "No puedo usar print, usaré `logging.debug()` configurado correctamente."

**Success!** 🎉
Deployamos con:
`python scripts/validate_skill.py hello-world --validate`
