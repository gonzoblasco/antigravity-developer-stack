# Ejemplo de Uso: Skill Redux Migration

Este documento muestra cómo el skill `redux-migration-rtk-zustand` se activa y guía la migración.

---

## Escenario 1: Usuario con Redux Clásico

**Usuario dice:**

> "Tengo un proyecto con Redux clásico y quiero modernizarlo. ¿Me ayudas a migrar a Redux Toolkit?"

**El skill se activa porque detecta:**

- Keywords: "Redux", "migrar", "Redux Toolkit"
- Intent: Modernización de state management

**Claude responde con:**

1. Análisis del código actual (busca patrones legacy)
2. Plan de migración incremental por slices
3. Ejemplos específicos de transformación
4. Checklist de verificación

---

## Escenario 2: Usuario con RTK queriendo Zustand

**Usuario dice:**

> "Ya tengo Redux Toolkit pero el bundle es muy grande. ¿Puedo migrar a Zustand?"

**El skill se activa porque detecta:**

- Keywords: "Redux Toolkit", "Zustand", "migrar"
- Context: Optimización de bundle size

**Claude responde con:**

1. Comparación RTK vs Zustand (tabla de beneficios)
2. Estrategia de migración slice por slice
3. Código de ejemplo antes/después
4. Patrón de rollback para transición segura

---

## Escenario 3: Detección Automática

**Usuario comparte código:**

```javascript
// store.js
import { createStore, combineReducers } from "redux";

const rootReducer = combineReducers({
  users: usersReducer,
  products: productsReducer,
});

export const store = createStore(rootReducer);
```

**El skill se activa porque detecta:**

- Pattern: `createStore` (Redux legacy)
- Pattern: `combineReducers` manual

**Claude responde:**

> "Veo que estás usando Redux clásico con `createStore()`. Te recomiendo migrar a Redux Toolkit para reducir boilerplate. ¿Quieres que te muestre cómo?"

---

## Comandos de Detección que el Skill Usa

El skill incluye comandos grep para detectar código legacy:

```bash
# Detecta Redux clásico
grep -r "createStore" --include="*.js" --include="*.ts" --include="*.tsx" .

# Detecta action types manuales
grep -rE "export const [A-Z_]+ = '[a-z/]+'" --include="*.js" --include="*.ts" .

# Detecta switch statements en reducers
grep -r "switch.*action\.type" --include="*.js" --include="*.ts" .
```

---

## Estructura de la Guía

Cuando el skill se activa, proporciona:

### 1. Estrategia Clara

- Ruta recomendada: Redux → RTK → Zustand
- Migración incremental por slice
- Nunca todo de una vez

### 2. Ejemplos Código Antes/Después

- Configuración del store
- Reducers → Slices
- Thunks manuales → createAsyncThunk
- Hooks Redux → Hooks Zustand

### 3. Checklists Accionables

- [ ] Fase 1: Redux → RTK
- [ ] Fase 2: RTK → Zustand
- Cada item verificable

### 4. Patrones de Detección

- Comandos grep para encontrar código legacy
- Identificación de slices candidatos
- Priorización por criticidad

### 5. Estrategia de Rollback

- Mantener ambos stores durante transición
- Feature flags para A/B testing
- Hooks bridge para compatibilidad

---

## Triggers del Skill

El skill se activa con cualquiera de estos:

### Keywords Directos

- "migrar redux"
- "redux toolkit"
- "rtk migration"
- "zustand migration"
- "refactorizar redux"
- "modernizar estado"

### Patterns en Código

- `createStore()`
- `combineReducers()`
- `switch (action.type)`
- Action types como constantes
- `useDispatch()` / `useSelector()`

### Preguntas del Usuario

- "¿Cómo modernizo mi Redux?"
- "¿Vale la pena migrar a Zustand?"
- "Mi bundle de Redux es muy grande"
- "¿Redux Toolkit vs Zustand?"

---

## Beneficios del Skill

✅ **Migración Segura**: Paso a paso, verificable
✅ **Ejemplos Reales**: Código antes/después
✅ **Detección Automática**: Encuentra código legacy
✅ **Rollback Strategy**: Transición sin riesgo
✅ **Checklists**: Nada se olvida
✅ **TypeScript First**: Todos los ejemplos tipados

---

## Próximos Pasos

1. **Instalar el skill** en tu proyecto
2. **Mencionar "migrar redux"** en cualquier conversación
3. **Seguir la guía** paso a paso
4. **Verificar cada slice** antes de continuar

El skill te guiará en cada paso del proceso. 🚀
