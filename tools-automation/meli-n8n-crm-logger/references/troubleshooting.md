# Troubleshooting & Strategic Variants

## Estrategias de Integración

### Opción A: Webhook (Recomendado)

**Mejor para:** Respuesta inmediata, sistemas de alto volumen.

- **Pros:** Real-time, menos consumo de API (solo dispara cuando hay eventos).
- **Cons:** Requiere endpoint público y SSL válido.

### Opción B: Polling (Programado)

**Mejor para:** Desarrollo local, firewalls restrictivos.

- **Pros:** Fácil de testear, no requiere exponer puertos.
- **Cons:** Delay en registro (~1h), consume cuota de API constantemente.

---

## Solución de Problemas Comunes

### 1. Webhook no se dispara

- **Síntoma:** Haces una pregunta en ML pero n8n no muestra ejecución.
- **Solución:**
  1. Verifica en [ML Developer Portal](https://developers.mercadolibre.com/) que la URL sea correcta.
  2. Confirma que el servidor n8n devuelve `200 OK` rápidamente.
  3. Revisa si el topic `questions` está suscrito.

### 2. Error "appkey no fue seteado"

- **Síntoma:** Respuesta JSON `{ "success": false, "message": "El parametro requerido appkey..." }`
- **Solución:**
  - El nodo `Function` no está leyendo bien la credencial.
  - Verifica que `{{$credentials.pilotCRM.appkey}}` tenga valor.
  - Asegúrate de pasar el objeto dentro de `form-urlencoded` en el nodo HTTP.

### 3. Leads Duplicados

- **Síntoma:** El mismo cliente aparece múltiples veces.
- **Solución:**
  - Uso estricto de `pilot_tracking_id` mappeado a `question.id`.
  - Pilot CRM debería rechazar duplicados si el tracking ID ya existe.

### 4. Error de Conexión OAuth ("Lo sentimos...")

- **Síntoma:** Al intentar conectar n8n con ML, aparece un popup de error genérico.
- **Solución:**
  1. Ve a la configuración de tu App en ML.
  2. Activa el checkbox **"Authorization Code"** (está desactivado por defecto).
  3. Verifica que la **Redirect URI** coincida exactamente con la de n8n (`.../callback`).
  4. Borra cualquier parámetro extra en "Auth URI Query Params" en n8n.

### 5. Error 404 en GET /questions

- **Síntoma:** Recibes `404 Not Found` al probar el flujo.
- **Causa:** Probablemente estás usando un ID de prueba (ej: `123456`) que no existe en ML.
- **Confirmación:** Si el error dice "Resource not found", ¡la conexión es EXITOSA! ML recibió tu petición y respondió. Solo necesitas esperar una pregunta real.

---

## Restricciones y Seguridad

- **Rate Limits:** MercadoLibre permite ~10k requests/día en tier gratuito. Usa webhooks para ahorrar.
- **GDPR/Privacidad:** No guardes datos personales (email, nombre) en logs de texto plano. Confía en el almacenamiento seguro de Pilot CRM.
- **Hardcoding:** NUNCA escribas la `appkey` directo en el código JS. Usa el store de credenciales de n8n.
