---
name: meli-n8n-crm-logger
description: Use cuando el usuario necesite integrar consultas de MercadoLibre con CRM usando n8n. Keywords: loguear consultas ML, registrar preguntas mercadolibre en CRM, n8n mercadolibre CRM, pilot solutions webhook.
---

# Integración MercadoLibre → n8n → Pilot Solutions CRM

## Overview

Configurar un pipeline automatizado que escuche preguntas de MercadoLibre y las registre como leads en Pilot Solutions CRM usando n8n.

## Quick Start

1.  **Configura el Webhook**: Registra tu endpoint de n8n en MercadoLibre.
    - [Guía de Setup y Payloads](references/setup-guide.md#1-configuración-de-webhook-mercadolibre)
2.  **Importa el Workflow**: Usa el JSON pre-configurado.
    - [`examples/webhook-to-crm-workflow.json`](examples/webhook-to-crm-workflow.json)
3.  **Configura Credenciales**: Añade tu AppKey de Pilot CRM y Token de ML en n8n.
4.  **Mapea Datos**: Ajusta el Function Node para tu vertical.
    - [Snippet de Mapeo JS](references/setup-guide.md#2-mapeo-de-datos-function-node)

## Core Components

### 1. Trigger (Entrada)

Usa un **Webhook Node** para recibir eventos `questions` de MercadoLibre.

- Alternativa simple: **Schedule Node** (Polling) si no tienes IP pública.
- [Ver comparación de estrategias](references/troubleshooting.md#estrategias-de-integración)

### 2. Processing (Lógica)

Un **Function Node** es vital para transformar el esquema JSON de ML al formato `form-url-encoded` de Pilot CRM.

- Requiere mapear `question.id` -> `pilot_tracking_id` para evitar duplicados.

### 3. Action (Salida)

**HTTP Request Node** hacia Pilot CRM.

- Endpoint: `https://api.pilotsolution.net/webhooks/welcome.php`
- Valida siempre la respuesta `success: true`.

## Troubleshooting

Si falla la integración (no llegan leads, errores de auth):

- [Ver Guía de Solución de Problemas](references/troubleshooting.md)

## References

- [Setup Guide & Code Snippets](references/setup-guide.md)
- [Troubleshooting & Variants](references/troubleshooting.md)
- [Official Pilot CRM API Docs](references/pilot-crm-api.md)
