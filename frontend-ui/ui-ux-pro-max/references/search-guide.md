# UI/UX Search Guide

## Search Reference

### Available Domains

| Domain       | Use For                              | Example Keywords                                         |
| ------------ | ------------------------------------ | -------------------------------------------------------- |
| `product`    | Product type recommendations         | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style`      | UI styles, colors, effects           | glassmorphism, minimalism, dark mode, brutalism          |
| `typography` | Font pairings, Google Fonts          | elegant, playful, professional, modern                   |
| `color`      | Color palettes by product type       | saas, ecommerce, healthcare, beauty, fintech, service    |
| `landing`    | Page structure, CTA strategies       | hero, hero-centric, testimonial, pricing, social-proof   |
| `chart`      | Chart types, library recommendations | trend, comparison, timeline, funnel, pie                 |
| `ux`         | Best practices, anti-patterns        | animation, accessibility, z-index, loading               |
| `react`      | React/Next.js performance            | waterfall, bundle, suspense, memo, rerender, cache       |
| `web`        | Web interface guidelines             | aria, focus, keyboard, semantic, virtualize              |
| `prompt`     | AI prompts, CSS keywords             | (style name)                                             |

### Available Stacks

| Stack           | Focus                                          |
| --------------- | ---------------------------------------------- |
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react`         | State, hooks, performance, patterns            |
| `nextjs`        | SSR, routing, images, API routes               |
| `vue`           | Composition API, Pinia, Vue Router             |
| `svelte`        | Runes, stores, SvelteKit                       |
| `swiftui`       | Views, State, Navigation, Animation            |
| `react-native`  | Components, Navigation, Lists                  |
| `flutter`       | Widgets, State, Layout, Theming                |
| `shadcn`        | shadcn/ui components, theming, forms, patterns |

## Example Workflow

**User request:** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp"

### Step 1: Analyze Requirements

- Product type: Beauty/Spa service
- Style keywords: elegant, professional, soft
- Industry: Beauty/Wellness
- Stack: html-tailwind (default)

### Step 2: Generate Design System (REQUIRED)

```bash
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Output:** Complete design system with pattern, style, colors, typography, effects, and anti-patterns.

### Step 3: Supplement with Detailed Searches (as needed)

```bash
# Get UX guidelines for animation and accessibility
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Get alternative typography options if needed
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### Step 4: Stack Guidelines

```bash
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Then:** Synthesize design system + detailed searches and implement the design.

## Output Formats

The `--design-system` flag supports two output formats:

```bash
# ASCII box (default) - best for terminal display
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - best for documentation
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

## Tips for Better Results

1. **Be specific with keywords** - "healthcare SaaS dashboard" > "app"
2. **Search multiple times** - Different keywords reveal different insights
3. **Combine domains** - Style + Typography + Color = Complete design system
4. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues
5. **Use stack flag** - Get implementation-specific best practices
6. **Iterate** - If first search doesn't match, try different keywords
