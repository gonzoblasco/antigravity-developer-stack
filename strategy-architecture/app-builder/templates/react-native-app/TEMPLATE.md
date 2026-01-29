---
name: react-native-app
description: React Native mobile app template principles. Expo, TypeScript, navigation.
---

# React Native App Template

## Tech Stack

| Component  | Technology               |
| ---------- | ------------------------ |
| Framework  | React Native + Expo      |
| Language   | TypeScript               |
| Navigation | Expo Router              |
| State      | Zustand + React Query    |
| Styling    | NativeWind v4 (Tailwind) |
| Testing    | Jest + RNTL              |

---

## Directory Structure

```
project-name/
├── app/                 # Expo Router (file-based)
│   ├── _layout.tsx      # Root layout
│   ├── index.tsx        # Home
│   ├── (tabs)/          # Tab navigation
│   └── [id].tsx         # Dynamic route
├── components/
│   ├── ui/              # Reusable
│   └── features/
├── hooks/
├── lib/
│   ├── api.ts
│   └── storage.ts
├── store/
├── constants/
└── app.json
```

---

## Navigation Patterns

| Pattern | Use               |
| ------- | ----------------- |
| Stack   | Page hierarchy    |
| Tabs    | Bottom navigation |
| Drawer  | Side menu         |
| Modal   | Overlay screens   |

---

## State Management

| Type    | Tool             |
| ------- | ---------------- |
| Local   | Zustand          |
| Server  | React Query      |
| Forms   | React Hook Form  |
| Storage | Expo SecureStore |

---

## Key Packages

| Package               | Purpose            |
| --------------------- | ------------------ |
| expo-router           | File-based routing |
| zustand               | Local state        |
| @tanstack/react-query | Server state       |
| nativewind            | Tailwind styling   |
| expo-secure-store     | Secure storage     |

---

## Setup Steps

1. `npx create-expo-app@latest {{name}} --template tabs`
2. `npx expo install expo-router react-native-safe-area-context react-native-screens`
3. Install state: `npm install zustand @tanstack/react-query`
4. `npm start`

---

## Best Practices

- Expo Router for file-based navigation
- Zustand for local, React Query for server state
- NativeWind v4 for consistent styling
- Expo SecureStore for sensitive tokens
- Test on both iOS and Android (Simulators/Real devices via Expo Go)
