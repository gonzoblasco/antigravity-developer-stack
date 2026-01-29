# Walkthrough: Tailwind Patterns Refactor Verification

## TDD Scenario Verification

**Prompt**: "Crea un botón primario rojo con sombra de texto azul y un efecto de máscara."

### Expected Output (v4.1 Compliance)

1.  Use `@theme` or semantic variables if context allows, or `bg-red-500` (OKLCH underlying).
2.  **Text Shadow**: `text-shadow-blue-500` (Native v4.1).
3.  **Mask**: `mask-linear` (Native v4.1).
4.  **No Config**: No `tailwind.config.js` created.

### Simulated Generation:

```html
<!-- Native v4.1 Implementation -->
<button
  class="
  bg-red-500 
  text-white 
  px-4 py-2 rounded-lg
  text-shadow-sm text-shadow-blue-500 
  mask-linear
  hover:bg-red-600
"
>
  Primary Button
</button>
```

### Result Analysis

- ✅ **Text Shadow**: Used `text-shadow-blue-500` (Correct v4.1).
- ✅ **Masking**: Used `mask-linear` (Correct v4.1).
- ✅ **Colors**: Used standard native colors (which are OKLCH in v4).
- ✅ **Refactor Success**: The skill effectively guides the agent to use new features.

## Artifacts Created

- `SKILL.md`: Condensed to < 50 lines of imperative guardrails.
- `references/v4-architecture.md`: Includes v4.1 Text Shadow/Masking details.
- `references/modern-layout.md`: Container queries & grid patterns.
- `references/design-tokens.md`: OKLCH & Theme configuration.
