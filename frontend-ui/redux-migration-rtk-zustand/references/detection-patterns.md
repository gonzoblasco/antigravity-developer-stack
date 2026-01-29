# Patrones de Detección de Código Redux

> Comandos para identificar código legacy y estado de migración

---

## Detectar Redux Clásico

```bash
# createStore legacy
grep -r "createStore" --include="*.js" --include="*.ts" --include="*.tsx" .

# Action types como constantes
grep -rE "export const [A-Z_]+ = '[a-z/]+'" --include="*.js" --include="*.ts" .

# Switch statements en reducers
grep -r "switch.*action\.type" --include="*.js" --include="*.ts" .

# Spread operator inmutabilidad manual
grep -rE "\.\.\.state,.*\.\.\.action" --include="*.js" --include="*.ts" .

# combineReducers manual
grep -r "combineReducers" --include="*.js" --include="*.ts" .

# applyMiddleware
grep -r "applyMiddleware" --include="*.js" --include="*.ts" .

# Redux DevTools extension manual
grep -r "__REDUX_DEVTOOLS_EXTENSION__" --include="*.js" --include="*.ts" .
```

---

## Detectar RTK (listo para Zustand)

```bash
# createSlice usage
grep -r "createSlice" --include="*.ts" --include="*.tsx" .

# configureStore
grep -r "configureStore" --include="*.ts" --include="*.tsx" .

# createAsyncThunk
grep -r "createAsyncThunk" --include="*.ts" --include="*.tsx" .

# useDispatch/useSelector hooks
grep -rE "useDispatch|useSelector" --include="*.tsx" .

# Provider component
grep -r "<Provider store=" --include="*.tsx" .

# RTK Query
grep -r "createApi" --include="*.ts" --include="*.tsx" .
```

---

## Detectar Zustand (migración completada)

```bash
# Zustand create
grep -r "from 'zustand'" --include="*.ts" --include="*.tsx" .

# Store hooks pattern
grep -rE "use[A-Z][a-zA-Z]+Store" --include="*.tsx" .

# Zustand middleware
grep -r "zustand/middleware" --include="*.ts" .
```

---

## Análisis de Complejidad

```bash
# Contar slices RTK
grep -rl "createSlice" --include="*.ts" . | wc -l

# Contar thunks async
grep -rl "createAsyncThunk" --include="*.ts" . | wc -l

# Contar componentes que usan Redux
grep -rl "useSelector\|useDispatch" --include="*.tsx" . | wc -l

# Estimar líneas de código Redux
find . -name "*.ts" -o -name "*.tsx" | xargs grep -l "redux\|@reduxjs" | xargs wc -l
```

---

## Script de Diagnóstico Completo

```bash
#!/bin/bash
echo "=== Redux Migration Analysis ==="

echo -e "\n📦 REDUX CLÁSICO:"
echo "createStore: $(grep -rl 'createStore' --include='*.ts' --include='*.js' . 2>/dev/null | wc -l) archivos"
echo "combineReducers: $(grep -rl 'combineReducers' --include='*.ts' --include='*.js' . 2>/dev/null | wc -l) archivos"
echo "switch(action.type): $(grep -rl 'switch.*action\.type' --include='*.ts' --include='*.js' . 2>/dev/null | wc -l) archivos"

echo -e "\n🔧 REDUX TOOLKIT:"
echo "createSlice: $(grep -rl 'createSlice' --include='*.ts' . 2>/dev/null | wc -l) archivos"
echo "createAsyncThunk: $(grep -rl 'createAsyncThunk' --include='*.ts' . 2>/dev/null | wc -l) archivos"
echo "configureStore: $(grep -rl 'configureStore' --include='*.ts' . 2>/dev/null | wc -l) archivos"

echo -e "\n🐻 ZUSTAND:"
echo "Zustand stores: $(grep -rl "from 'zustand'" --include='*.ts' . 2>/dev/null | wc -l) archivos"

echo -e "\n📊 COMPONENTES:"
echo "useSelector: $(grep -rl 'useSelector' --include='*.tsx' . 2>/dev/null | wc -l) componentes"
echo "useDispatch: $(grep -rl 'useDispatch' --include='*.tsx' . 2>/dev/null | wc -l) componentes"

echo -e "\n=== RECOMENDACIÓN ==="
CLASSIC=$(grep -rl 'createStore' --include='*.ts' --include='*.js' . 2>/dev/null | wc -l)
RTK=$(grep -rl 'createSlice' --include='*.ts' . 2>/dev/null | wc -l)
ZUSTAND=$(grep -rl "from 'zustand'" --include='*.ts' . 2>/dev/null | wc -l)

if [ "$CLASSIC" -gt 0 ]; then
  echo "⚠️  ACCIÓN: Migrar Redux Clásico → RTK primero"
elif [ "$RTK" -gt 0 ] && [ "$ZUSTAND" -eq 0 ]; then
  echo "✅ LISTO: Puedes migrar RTK → Zustand"
elif [ "$ZUSTAND" -gt 0 ]; then
  echo "🎉 COMPLETADO: Ya usas Zustand"
fi
```

---

## Priorización de Slices

Para decidir orden de migración:

```bash
# Ordenar slices por complejidad (líneas de código)
for file in $(grep -rl "createSlice" --include="*.ts" .); do
  lines=$(wc -l < "$file")
  echo "$lines $file"
done | sort -n

# Ordenar por uso en componentes
for slice in $(grep -roh "use[A-Z][a-zA-Z]*Slice" --include="*.tsx" . | sort -u); do
  count=$(grep -rl "$slice" --include="*.tsx" . | wc -l)
  echo "$count $slice"
done | sort -n
```

**Regla**: Empezar por slices con menos líneas y menos uso → menor riesgo.
