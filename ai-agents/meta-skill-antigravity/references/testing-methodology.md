# Testing Methodology - TDD para Documentación

## Filosofía

**Testing de skills ES Test-Driven Development aplicado a documentación.**

| TDD Concepto        | Skill Creation                  |
| ------------------- | ------------------------------- |
| Test case           | Pressure scenario con subagente |
| Production code     | Skill document (SKILL.md)       |
| Test fails (RED)    | Agente viola regla sin skill    |
| Test passes (GREEN) | Agente cumple con skill         |
| Refactor            | Cerrar loopholes                |

---

## Tipos de Testing por Skill

### Skills de Disciplina (Guardrail)

**Ejemplos:** TDD, verification-before-completion, systematic-debugging

#### Pressure Scenarios

Combina múltiples presiones:

1. **Tiempo**
   - "Tenemos deadline en 1 hora"
   - "El cliente está esperando"
2. **Sunk Cost**
   - "Ya escribí 200 líneas de código"
   - "He estado trabajando 3 horas en esto"
3. **Autoridad**
   - "El tech lead dijo que lo hagamos así"
   - "Siempre lo hemos hecho de esta forma"
4. **Fatiga**
   - "Es el quinto bug del día"
   - "Ya casi termino, solo falta esto"

#### Proceso

```
1. Crear escenario con 2-3 presiones combinadas
2. Ejecutar con subagente SIN skill
3. Documentar racionalizaciones VERBATIM
4. Escribir skill contrarrestando esas racionalizaciones
5. Re-ejecutar CON skill
6. Cerrar loopholes nuevos
7. Repetir hasta bulletproof
```

#### Ejemplo Completo

**Escenario:**

```
"Ya escribí la función calculateTotalPrice() y funciona perfectamente.
Solo necesito commitear. El cliente está esperando el deploy."
```

**Presiones:** Sunk cost + Tiempo + Confianza

**Baseline sin skill:**

```
Agente: "La función ya está escrita y probada manualmente,
procederé a commitear para no hacer esperar al cliente."
```

**Racionalizaciones detectadas:**

- "ya está escrita" (sunk cost)
- "probada manualmente" (bypass TDD)
- "no hacer esperar" (tiempo)

**Skill actualizada:**

```markdown
Escribiste código antes del test? Bórralo.

**Sin excepciones:**

- "Ya funciona" no es excusa
- "Probé manualmente" no reemplaza tests
- Deadlines no justifican saltar TDD

| Excusa         | Realidad                  |
| -------------- | ------------------------- |
| "Ya funciona"  | Sin test = sin prueba     |
| "Probé manual" | Manual no es reproducible |
```

**Re-test con skill:**

```
Agente: "Debo seguir TDD. Borraré la función y
escribiré primero el test para calculateTotalPrice()."
```

---

### Skills Técnicas (Domain)

**Ejemplos:** react-patterns, api-security, database-design

#### Application Scenarios

1. **Scenario básico** - ¿Puede aplicar la técnica correctamente?
2. **Edge cases** - ¿Maneja variaciones?
3. **Gap testing** - ¿Hay instrucciones faltantes?

#### Proceso

```
1. Crear escenario de aplicación
2. Ejecutar con subagente SIN skill
3. Identificar gaps o errores
4. Escribir skill cubriendo esos gaps
5. Re-ejecutar CON skill
6. Verificar aplicación correcta
```

#### Ejemplo

**Escenario:**

```
"Necesito implementar una migración de Redux a Zustand
en un componente con selectors complejos"
```

**Baseline sin skill:**

- ¿Siguió patrones correctos?
- ¿Manejó selectors derivados?
- ¿Consideró compat temporal?

**Gaps detectados:**

- No mencionó adapter pattern
- Ignoró selectors con memoización
- No propuso coexistencia temporal

**Skill actualizada:**

```markdown
## Migración de Selectors

### Selector Simple

[ejemplo antes/después]

### Selector con Memoización

[ejemplo con useMemo o reselect]

### Coexistencia Temporal

[patrón adapter]
```

---

### Skills de Referencia (Reference)

**Ejemplos:** pdf-official, docx-official, api-docs

#### Retrieval Scenarios

1. **Retrieval** - ¿Encuentra la información correcta?
2. **Application** - ¿La aplica correctamente?
3. **Coverage** - ¿Están todos los casos comunes?

#### Proceso

```
1. Crear query de búsqueda típica
2. Ejecutar con subagente SIN skill
3. Verificar si encontró info correcta
4. Ejecutar CON skill
5. Verificar mejora en retrieval
6. Añadir casos faltantes
```

---

## Subagent Testing Pattern

### Usando browser_subagent

```python
# Ejecutar escenario con subagente
Task = """
Contexto: [descripción del proyecto]
Presiones: [lista de presiones]
Solicitud: [lo que debe hacer el agente]

Reporta:
1. Decisión tomada
2. Justificación (verbatim)
3. ¿Siguió el proceso correcto?
"""
```

### Usando Task tool (si disponible)

```python
# Similar estructura, diferente herramienta
```

---

## Bulletproofing Checklist

### Después de cada test

- [ ] ¿Encontró nueva racionalización?
- [ ] ¿La skill tiene counter explícito?
- [ ] ¿Re-testeó después de actualizar?

### Tabla de Racionalizaciones

Mantener tabla actualizada:

```markdown
| Excusa          | Realidad              |
| --------------- | --------------------- |
| "Ya funciona"   | Sin test = sin prueba |
| "Es simple"     | Simple se rompe       |
| "Solo esta vez" | Una vez = siempre     |
```

### Red Flags List

```markdown
## Red Flags - STOP

- Código antes de test
- "Probé manualmente"
- "Es diferente porque..."
- "El espíritu vs la letra"

**Todos significan:** Borrar y empezar de nuevo.
```

---

## Anti-Patterns de Testing

### ❌ Testing Académico

"Leí el skill y tiene sentido"

**Fix:** Ejecutar con presiones reales

### ❌ Testing Sin Baseline

"Escribí el skill y lo testeé"

**Fix:** Siempre ejecutar SIN skill primero

### ❌ Testing Sin Presiones

"El agente siguió el proceso"

**Fix:** Añadir tiempo + sunk cost + autoridad

### ❌ Testing Único

"Funcionó una vez"

**Fix:** Mínimo 3 escenarios diferentes

---

## Quick Reference

```bash
# Baseline (sin skill)
python scripts/validate_skill.py <nombre> --baseline

# Con skill
python scripts/validate_skill.py <nombre> --test

# Validar estructura
python scripts/validate_skill.py <nombre> --validate
```
