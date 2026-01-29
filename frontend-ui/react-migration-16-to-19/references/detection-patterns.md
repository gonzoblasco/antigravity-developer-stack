# Detection Patterns

Use these commands to find legacy patterns that need migration.

### Buscar código legacy con grep

```bash
# PropTypes usage
grep -r "\.propTypes\s*=" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" .

# DefaultProps en funciones
grep -r "\.defaultProps\s*=" --include="*.js" --include="*.jsx" --include="*.tsx" .

# String refs
grep -rE "ref=['\"]" --include="*.js" --include="*.jsx" --include="*.tsx" .

# Legacy context
grep -r "getChildContext\|childContextTypes\|contextTypes" --include="*.js" --include="*.jsx" .

# ReactDOM.render legacy
grep -r "ReactDOM\.render\|ReactDOM\.hydrate" --include="*.js" --include="*.jsx" --include="*.tsx" .

# findDOMNode (eliminado)
grep -r "findDOMNode" --include="*.js" --include="*.jsx" --include="*.tsx" .
```
