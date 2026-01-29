# Component Design Patterns

## Design Principles

### Component Types

| Type               | Use                   | State             |
| ------------------ | --------------------- | ----------------- |
| **Server**         | Data fetching, static | None              |
| **Client**         | Interactivity         | useState, effects |
| **Presentational** | UI display            | Props only        |
| **Container**      | Logic/state           | Heavy state       |

### Rules of Thumb

- **One responsibility per component**: If it does two things, split it.
- **Props down, events up**: Data flows down, actions flow up.
- **Composition over inheritance**: Use `children` prop to compose UI.
- **Prefer small, focused components**: Easier to test and reuse.

---

## Advanced Composition

### Compound Components

Use this pattern when you have a parent component that implicitly shares state with its children.

**Example**: `<Tabs>`, `<Select>`, `<Menu>`.

See implementation in `examples/advanced-composition.tsx`.

### Render Props

Use this pattern to share logic between components using a prop whose value is a function. React 19/Hooks have largely replaced this with custom hooks, but it's still useful for specific cases like virtualization or animation libraries.

See implementation in `examples/advanced-composition.tsx`.

---

## TypeScript Patterns

### Props Typing

| Pattern   | Use                 |
| --------- | ------------------- |
| Interface | Component props     |
| Type      | Unions, complex     |
| Generic   | Reusable components |

### Common Types

| Need          | Type                 |
| ------------- | -------------------- |
| Children      | `ReactNode`          |
| Event handler | `MouseEventHandler`  |
| Ref           | `RefObject<Element>` |
