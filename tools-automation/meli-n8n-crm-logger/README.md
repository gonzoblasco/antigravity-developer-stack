# MercadoLibre → n8n → Pilot CRM Integration Skill

Este skill proporciona una guía completa para integrar consultas de MercadoLibre con Pilot Solutions CRM usando n8n como orquestador.

## Contenido

### 📄 SKILL.md

Guía principal con instrucciones paso a paso, ejemplos, y mejores prácticas.

### 📚 References

- **pilot-crm-api.md**: Documentación completa del API de Pilot Solutions CRM
  - Endpoints, autenticación, parámetros
  - Ejemplos de requests/responses
  - Códigos de error y troubleshooting

- **data-mapping.md**: Guía de mapeo entre MercadoLibre y Pilot CRM
  - Tabla completa de campos
  - Transformaciones necesarias
  - Ejemplos de código JavaScript

### 🔧 Examples

- **webhook-to-crm-workflow.json**: Workflow n8n con Webhook Trigger
  - Respuesta en tiempo real a preguntas de ML
  - Workflow completo listo para importar
- **polling-questions-workflow.json**: Workflow n8n con Schedule Trigger
  - Polling cada hora de preguntas nuevas
  - Filtrado de preguntas ya procesadas
  - Ideal para ambientes sin webhook público

## Quick Start

1. **Importa un workflow en n8n**:

   ```bash
   # Copiar contenido de examples/webhook-to-crm-workflow.json
   # En n8n UI: Import from File/URL → Pegar JSON
   ```

2. **Configurar credenciales**:
   - MercadoLibre OAuth2 (para acceder al API)
   - Pilot CRM (appkey, suborigin_id)

3. **Activar el workflow**

4. **Configurar webhook en MercadoLibre** (si usas webhook trigger)

## Estructura del Skill

```
meli-n8n-crm-logger/
├── SKILL.md                           # Guía principal
├── README.md                          # Este archivo
├── examples/
│   ├── webhook-to-crm-workflow.json   # Workflow con webhook
│   └── polling-questions-workflow.json # Workflow con polling
└── references/
    ├── pilot-crm-api.md               # API reference
    └── data-mapping.md                # Mapeo de datos
```

## Casos de Uso

### ✅ Caso 1: Webhook en Tiempo Real

**Cuando usar**: Necesitas respuesta inmediata a consultas de ML

**Workflow**: `webhook-to-crm-workflow.json`

**Ventajas**:

- Sin delay
- Menor carga en APIs
- Más eficiente

### ✅ Caso 2: Polling Programado

**Cuando usar**: No tienes endpoint público o prefieres procesamiento por lotes

**Workflow**: `polling-questions-workflow.json`

**Ventajas**:

- Más fácil de debuggear
- No requiere configuración de webhook
- Puedes agrupar operaciones

## Requisitos

- Cuenta de MercadoLibre con aplicación registrada
- Instancia de n8n (self-hosted o cloud)
- Cuenta de Pilot Solutions CRM con appkey
- Credenciales OAuth de MercadoLibre

## Configuración

### Variables de Entorno Recomendadas

```bash
# Pilot CRM
PILOT_CRM_APPKEY=9715fc4b-17a8-4e56-ac7a-6deb5fd46u71
PILOT_CONTACT_TYPE_ID=1
PILOT_BUSINESS_TYPE_ID=1
PILOT_SUBORIGIN_ML=7A2E4184

# MercadoLibre OAuth
MELI_CLIENT_ID=tu_client_id
MELI_CLIENT_SECRET=tu_client_secret
```

### Credenciales en n8n

Crear dos credenciales en n8n:

1. **MercadoLibre OAuth2**
   - Tipo: OAuth2
   - Authorization URL: `https://auth.mercadolibre.com.ar/authorization`
   - Token URL: `https://api.mercadolibre.com/oauth/token`

2. **Pilot CRM** (Generic Credentials)
   - `appkey`: Tu API key de Pilot
   - `suborigenML`: ID de suborigen para ML (consultar en Pilot)

## Testing

### Debug Mode

Usa `debug: 1` en Pilot CRM para testear sin crear leads:

```javascript
const crmPayload = {
  ...
  debug: 1, // No crea el lead, solo valida
  ...
};
```

### Logs de n8n

Monitorear ejecuciones en n8n UI:

- Workflow Executions → Ver logs detallados
- Revisar cada nodo individualmente

## Troubleshooting

Consulta la sección **Troubleshooting** en `SKILL.md` para:

- Webhook no se dispara
- Error "appkey no fue seteado"
- Leads duplicados
- Y más...

## Referencias

- [MercadoLibre API Docs](https://developers.mercadolibre.com/)
- [n8n Documentation](https://docs.n8n.io/)
- [Pilot Solutions CRM](https://www.pilotsolution.net/)

## Contribuir

Este skill es parte del sistema de skills de Antigravity. Para mejoras o sugerencias, abrir un issue o crear un PR.

## Licencia

Este skill se distribuye bajo la misma licencia del proyecto principal.
