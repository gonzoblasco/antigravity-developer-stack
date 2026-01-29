# n8n Workflow Builder - Recursos

Esta carpeta contiene templates y ejemplos para facilitar la creación de workflows de n8n.

## Templates de Nodos (`/templates`)

Templates individuales de nodos comunes, listos para copiar y personalizar:

- **`webhook.json`**: Webhook trigger para recibir datos HTTP
- **`http-request.json`**: HTTP Request para llamadas a APIs externas
- **`function.json`**: Code node para JavaScript personalizado
- **`set.json`**: Set node para transformar datos
- **`if.json`**: IF node para lógica condicional
- **`schedule-trigger.json`**: Schedule Trigger con expresión cron
- **`respond-to-webhook.json`**: Responder a webhooks

### Uso de Templates

1. Copia el contenido del template
2. Reemplaza los IDs únicos con nuevos UUIDs
3. Personaliza los parámetros según tu caso de uso
4. Integra en tu workflow

## Ejemplos de Workflows (`/examples`)

Workflows completos funcionales que puedes importar directamente en n8n:

### `simple-webhook-to-response.json`

**Descripción**: Workflow básico que recibe un webhook y devuelve una respuesta JSON.

**Flujo**:

- Webhook → Set Response → Respond to Webhook

**Caso de uso**: Endpoints simples de API, health checks, webhooks de confirmación

---

### `api-integration-workflow.json`

**Descripción**: Integración completa con API externa incluyendo manejo de errores.

**Flujo**:

- Webhook → Extract Parameters → Call API → Check Response → Format Response → Respond

**Caso de uso**: Consultas a APIs externas, enriquecimiento de datos, validación de respuestas

**Características**:

- Extracción de parámetros desde el webhook
- Llamada a API externa (JSONPlaceholder como ejemplo)
- Validación condicional de respuestas
- Manejo de casos de éxito y error
- Respuesta final al webhook

---

### `scheduled-polling.json`

**Descripción**: Workflow programado que consulta una API periódicamente.

**Flujo**:

- Schedule Trigger (cada 6 horas) → Fetch API → Filter Data → Split Items → Check Conditions → Notify

**Caso de uso**: Monitoreo de APIs, sincronización periódica, alertas automáticas

**Características**:

- Ejecución programada con cron
- Procesamiento con JavaScript personalizado
- División de arrays en items individuales
- Filtrado condicional de resultados
- Preparación de notificaciones

## Cómo Importar Workflows

1. Copia el contenido del archivo JSON
2. En n8n, haz click en el menú principal (☰)
3. Selecciona "Import from File" o "Import from URL"
4. Pega el JSON y confirma
5. Personaliza los parámetros según tus necesidades
6. Configura las credenciales necesarias
7. Activa el workflow

## Personalización

Todos los ejemplos usan IDs únicos y datos de prueba. Antes de usar en producción:

- ✅ Reemplaza URLs de APIs con tus endpoints reales
- ✅ Configura credenciales apropiadas
- ✅ Ajusta expresiones cron según tus necesidades
- ✅ Implementa validación de datos robusta
- ✅ Agrega manejo de errores específico
- ✅ Prueba exhaustivamente antes de activar

## Notas Importantes

- **IDs únicos**: Al combinar nodos de diferentes templates, asegúrate de que cada nodo tenga un ID único
- **Conexiones**: Verifica que todas las conexiones entre nodos estén correctamente definidas
- **Versiones**: Los templates usan versiones actuales de nodos. Si usas una versión antigua de n8n, puede requerir ajustes
- **Credenciales**: Los workflows no incluyen credenciales. Debes configurarlas manualmente en n8n

## Recursos Adicionales

- [Documentación oficial de n8n](https://docs.n8n.io)
- [Core Nodes Library](https://docs.n8n.io/integrations/builtin/core-nodes/)
- [Workflow Components](https://docs.n8n.io/workflows/components/)
- [n8n Community](https://community.n8n.io)
