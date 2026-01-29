# Setup Guide: MercadoLibre → n8n → Pilot CRM

## 1. Configuración de Webhook MercadoLibre

Para recibir notificaciones en tiempo real cuando alguien hace una pregunta.

**Endpoint:** `POST https://api.mercadolibre.com/applications/{APP_ID}`

**Payload:**

```json
{
  "notifications_url": "https://tu-instancia-n8n.com/webhook/meli-questions"
}
```

**Topics Importantes:**

- `questions`: Nuevas preguntas (El que usamos aquí)
- `items`: Cambios en publicaciones (precios, pausas)
- `orders_v2`: Nuevas ventas

> [!TIP]
> Asegúrate de que `notifications_url` sea pública y tenga certificado SSL válido. Usa `cloudflared` o `ngrok` para pruebas locales.

---

## 2. Mapeo de Datos (Function Node)

Este código JavaScript transforma el JSON de MercadoLibre al formato que espera Pilot Solutions.

**Entrada:** Objeto `question` de ML.
**Salida:** Objeto `lead` para Pilot CRM.

```javascript
// Extraer datos del webhook de MercadoLibre
const mlData = $input.item.json;

// Mapear a formato Pilot CRM
const crmData = {
  action: "create",
  appkey: "{{$credentials.pilotCRM.appkey}}", // Usar credenciales seguras
  debug: 0, // Poner en 1 para pruebas seguras
  pilot_contact_type_id: 1, // 1 = Electrónico
  pilot_business_type_id: 1, // Ajustar según tu vertical de negocio
  pilot_firstname: mlData.question?.from?.nickname || "Consulta ML",
  pilot_email: mlData.question?.from?.email || "",

  // Notas enriquecidas
  pilot_notes: `Pregunta ML: ${mlData.question?.text}\n\nProducto: ${mlData.item?.title}`,

  pilot_provider_service: "MercadoLibre",
  pilot_tracking_id: mlData.question?.id, // ID único para evitar duplicados
  pilot_product_of_interest: mlData.item?.title,
  pilot_suborigin_id: "{{$credentials.pilotCRM.suborigenML}}",
  pilot_car_brand: "",
  pilot_car_modelo: "",
};

return { json: crmData };
```

---

## 3. Configuración HTTP Request (Pilot CRM)

**Endpoint:** `https://api.pilotsolution.net/webhooks/welcome.php`
**Method:** `POST`
**Body Type:** Form URL-Encoded

**Parámetros Críticos:**

| Parámetro         | Valor     | Descripción         |
| ----------------- | --------- | ------------------- |
| `action`          | `create`  | Acción a realizar   |
| `appkey`          | (Secreto) | Tu llave de API     |
| `pilot_firstname` | String    | Nombre del contacto |

**Respuesta Exitosa Esperada:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "message": "El servicio de carga de datos se ejecuto correctamente.",
    "assigned_user_id": 80,
    "success": true,
    "id": 8855
  }
}
```
