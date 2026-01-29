# Tailwind CSS v4 Architecture & Features

> Detailed reference for Tailwind v4.0 and v4.1 architecture.

## 1. Architecture: v3 vs v4

| v3 (Legacy)          | v4 (Current)                 |
| -------------------- | ---------------------------- |
| `tailwind.config.js` | CSS-based `@theme` directive |
| PostCSS plugin       | Oxide engine (10x faster)    |
| JIT mode             | Native, always-on            |
| Plugin system        | CSS-native features          |
| `@apply` directive   | Still works, discouraged     |

### Core Concepts

| Concept            | Description                          |
| ------------------ | ------------------------------------ |
| **CSS-first**      | Configuration in CSS, not JavaScript |
| **Oxide Engine**   | Rust-based compiler, much faster     |
| **Native Nesting** | CSS nesting without PostCSS          |
| **CSS Variables**  | All tokens exposed as `--*` vars     |

## 2. Performance Principles

| Principle          | Implementation             |
| ------------------ | -------------------------- |
| **Purge unused**   | Automatic in v4            |
| **Avoid dynamism** | No template string classes |
| **Use Oxide**      | Default in v4, 10x faster  |
| **Cache builds**   | CI/CD caching              |

## 3. Tailwind v4.1 New Features

### Text Effects

- **Text Shadows**: Native utilities like `text-shadow-sm`, `text-shadow-lg`.
  - Customizable color: `text-shadow-blue-500`.
  - Opacity support: `text-shadow-black/50`.
- **Colored Drop Shadows**: `drop-shadow-indigo-500` (previously only black/alpha).

### Masking (Native)

- **Mask Utilities**: `mask-*` classes for CSS masking.
  - `mask-linear`: Standard linear gradient mask.
  - `mask-radial`: Radial gradient mask.
  - Custom masks supported via utilities.

### Build Configuration

- **`@source` Directive**: Fine-grained control over scanning.
  - `@source not ./vendor/**`: Exclude directories.
  - `@source inline(.my-class { ... })`: Force include classes.

### Typography

- **`overflow-wrap`**: Better control for long words.
