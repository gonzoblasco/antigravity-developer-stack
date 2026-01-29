# Design Tokens & Theming

> Configuration using CSS variables, OKLCH colors, and typography.

## 1. CSS Configuration (`@theme`)

In Tailwind v4, use standard CSS variables in your main CSS file.

```css
@theme {
  /* Colors - OKLCH preferred */
  --color-primary: oklch(0.6 0.18 250); /* Blue-ish */
  --color-surface: oklch(0.98 0 0); /* White */

  /* Typography */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-display: "Outfit", sans-serif;

  /* Spacing */
  --spacing-4_5: 1.125rem;
}
```

## 2. Color System (OKLCH)

**Always prefer OKLCH** over HEX/RGB for new projects.

- **Perceptual Uniformity**: Changing Lightness (L) works as expected.
- **Gamut**: Access to vibrant colors P3 monitors display.

### Layer Architecture

1. **Primitives**: `--blue-500` (The raw palette)
2. **Semantic**: `--color-primary`, `--color-destructive` (The usage)
3. **Component**: `--btn-bg` (Specific context)

## 3. Typography

| Role         | Font Family Examples      |
| ------------ | ------------------------- |
| **Body/UI**  | Inter, SF Pro, Roboto     |
| **Headings** | Outfit, Poppins, Syne     |
| **Code**     | JetBrains Mono, Fira Code |

### Scale

- `text-xs`, `text-sm`: Utility/Labels
- `text-base`: Standard body
- `text-lg`: Lead paragraphs
- `text-xl` to `text-4xl`: Headings

## 4. Dark Mode

### Strategy

Use the `dark:` variant.

```html
<div class="bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100">
  <!-- Content -->
</div>
```

### Config

- **v4 Default**: Uses `@media (prefers-color-scheme: dark)`.
- **Manual Toggle**: Add `dark` class to HTML and configure if needed (or just use CSS selector strategy).

## 5. Animation

| Utility          | Effect                     |
| ---------------- | -------------------------- |
| `animate-spin`   | Loading spinners           |
| `animate-pulse`  | Skeletons / Loading states |
| `transition-all` | Smooth state changes       |
| `duration-200`   | Standard UI speed          |
| `ease-out`       | Best for entering elements |
