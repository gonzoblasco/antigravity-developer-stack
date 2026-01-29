#!/bin/bash
# detect_redux_legacy.sh
# Detecta código Redux legacy en el proyecto y recomienda acciones
# Uso: ./detect_redux_legacy.sh [directorio]

set -e

DIR="${1:-.}"

echo "=== 🔍 Redux Migration Analysis ==="
echo "Directorio: $DIR"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
CLASSIC=0
RTK=0
ZUSTAND=0

echo "📦 REDUX CLÁSICO:"
count=$(grep -rl 'createStore' --include='*.ts' --include='*.js' --include='*.tsx' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   createStore: $count archivos"
CLASSIC=$((CLASSIC + count))

count=$(grep -rl 'combineReducers' --include='*.ts' --include='*.js' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   combineReducers: $count archivos"
CLASSIC=$((CLASSIC + count))

count=$(grep -rl 'switch.*action\.type' --include='*.ts' --include='*.js' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   switch(action.type): $count archivos"
CLASSIC=$((CLASSIC + count))

count=$(grep -rl 'applyMiddleware' --include='*.ts' --include='*.js' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   applyMiddleware: $count archivos"
CLASSIC=$((CLASSIC + count))

echo ""
echo "🔧 REDUX TOOLKIT:"
count=$(grep -rl 'createSlice' --include='*.ts' --include='*.tsx' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   createSlice: $count archivos"
RTK=$((RTK + count))

count=$(grep -rl 'createAsyncThunk' --include='*.ts' --include='*.tsx' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   createAsyncThunk: $count archivos"
RTK=$((RTK + count))

count=$(grep -rl 'configureStore' --include='*.ts' --include='*.tsx' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   configureStore: $count archivos"
RTK=$((RTK + count))

echo ""
echo "🐻 ZUSTAND:"
count=$(grep -rl "from 'zustand'" --include='*.ts' --include='*.tsx' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   Zustand stores: $count archivos"
ZUSTAND=$((ZUSTAND + count))

echo ""
echo "📊 COMPONENTES CON REDUX:"
count=$(grep -rl 'useSelector' --include='*.tsx' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   useSelector: $count componentes"

count=$(grep -rl 'useDispatch' --include='*.tsx' "$DIR" 2>/dev/null | wc -l | tr -d ' ')
echo "   useDispatch: $count componentes"

echo ""
echo "=== 📋 RECOMENDACIÓN ==="

if [ "$CLASSIC" -gt 0 ]; then
  echo -e "${RED}⚠️  ACCIÓN REQUERIDA:${NC}"
  echo "   Migrar Redux Clásico → Redux Toolkit primero"
  echo ""
  echo "   Archivos a migrar:"
  grep -rl 'createStore' --include='*.ts' --include='*.js' "$DIR" 2>/dev/null | head -5
  echo ""
  echo "   Siguiente paso: npm install @reduxjs/toolkit"
elif [ "$RTK" -gt 0 ] && [ "$ZUSTAND" -eq 0 ]; then
  echo -e "${YELLOW}✅ LISTO PARA SIGUIENTE FASE:${NC}"
  echo "   Puedes migrar RTK → Zustand"
  echo ""
  echo "   Slices a migrar (ordenados por complejidad):"
  for file in $(grep -rl "createSlice" --include="*.ts" "$DIR" 2>/dev/null); do
    lines=$(wc -l < "$file" | tr -d ' ')
    echo "   $lines líneas: $file"
  done | sort -n | head -5
  echo ""
  echo "   Siguiente paso: npm install zustand"
elif [ "$ZUSTAND" -gt 0 ] && [ "$RTK" -eq 0 ]; then
  echo -e "${GREEN}🎉 MIGRACIÓN COMPLETADA:${NC}"
  echo "   Ya usas Zustand exclusivamente"
  echo "   Puedes eliminar dependencias Redux"
elif [ "$ZUSTAND" -gt 0 ] && [ "$RTK" -gt 0 ]; then
  echo -e "${YELLOW}🔄 MIGRACIÓN EN PROGRESO:${NC}"
  echo "   Tienes ambos RTK y Zustand"
  echo "   Continúa migrando slices restantes"
else
  echo -e "${GREEN}ℹ️  NO SE DETECTÓ REDUX:${NC}"
  echo "   Este proyecto no usa Redux/RTK/Zustand"
fi

echo ""
echo "=== Fin del análisis ==="
