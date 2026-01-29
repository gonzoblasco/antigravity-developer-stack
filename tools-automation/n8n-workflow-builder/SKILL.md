---
name: n8n-workflow-builder
description: Use cuando el usuario quiera crear, planificar o depurar workflows de n8n. Keywords: n8n, workflow, automatización, json, webhook.
---

# n8n Workflow Builder

## Goal

Guiar la creación de workflows n8n eficientes y mantenibles, generando JSON válido y listo para importar.

## The Process

Sigue este algoritmo EXACTO para garantizar calidad:

1.  **Requirements**: Define Trigger, Datos de Entrada y Resultado Esperado.
2.  **Logic**: Diseña el flujo en abstracto (Ver `references/common-patterns.md`).
3.  **Nodes**: Selecciona los nodos correctos.
4.  **JSON**: Genera el archivo usando los esquemas oficiales (Ver `references/n8n-json-schemas.md`).

## Core Instructions

### 1. Planificación

ANTES de generar cualquier código JSON, confirma explícitamente:

- **Trigger**: ¿Qué inicia el proceso? (Webhook, Cron, Manual)
- **Inputs**: ¿Qué datos llegan?
- **Outputs**: ¿Qué debe pasar al final? (Respuesta HTTP, DB Insertion)

### 2. Generación

> [!IMPORTANT]
> **Progressive Disclosure**: No adivines estructuras. LEE `references/n8n-json-schemas.md` antes de escribir JSON.

- Usa la estructura base `nodes` y `connections`.
- Para nodos desconocidos, usa un `HTTPRequest` genérico o el nodo `Function`.
- **Valida IDs**: Asegura que cada nodo tenga un UUID único.

### 3. Entrega

- Entrega el JSON en un bloque de código `json`.
- Explica cómo importarlo (Copiar texto -> Clic en canvas n8n -> Ctrl+V).

## Reference Library

- **Mental Models & Patterns**: `references/common-patterns.md`
- **Technical Schemas**: `references/n8n-json-schemas.md`
