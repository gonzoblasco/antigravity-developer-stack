# Data Mapping: MercadoLibre → Pilot Solutions CRM

Esta tabla muestra el mapeo completo entre los datos que proporciona MercadoLibre y los parámetros que acepta Pilot Solutions CRM.

---

## Webhook de Preguntas MercadoLibre

Cuando se recibe un webhook de tipo `questions`, MercadoLibre envía:

```json
{
  "resource": "/questions/123456789",
  "user_id": 987654321,
  "topic": "questions",
  "received": "2024-01-26T10:30:00.000Z",
  "sent": "2024-01-26T10:30:00.000Z",
  "attempts": 1
}
```

Luego necesitas hacer `GET https://api.mercadolibre.com/questions/{question_id}` para obtener:

```json
{
  "id": 123456789,
  "text": "¿Tiene stock disponible?",
  "status": "UNANSWERED",
  "date_created": "2024-01-26T10:30:00.000Z",
  "item_id": "MLA123456",
  "from": {
    "id": 98765432,
    "nickname": "JUANPEREZ",
    "email": "juan@example.com"
  },
  "answer": null
}
```

Y también `GET https://api.mercadolibre.com/items/{item_id}`:

```json
{
  "id": "MLA123456",
  "title": "Ford Fiesta Kinetic 2024 - 0km",
  "price": 25000000,
  "currency_id": "ARS",
  "available_quantity": 5,
  "condition": "new",
  "permalink": "https://articulo.mercadolibre.com.ar/...",
  "seller": {
    "id": 11111111,
    "nickname": "CONCESIONARIA_FORD"
  }
}
```

---

## Mapeo Principal

| Dato MercadoLibre        | Parámetro Pilot CRM         | Transformación                   | Notas                      |
| ------------------------ | --------------------------- | -------------------------------- | -------------------------- |
| **Datos Fijos**          |                             |                                  |                            |
| -                        | `action`                    | `"create"`                       | Siempre                    |
| -                        | `appkey`                    | Credencial configurada           | Obtener de env vars        |
| -                        | `pilot_contact_type_id`     | `1`                              | 1 = Electrónico            |
| -                        | `pilot_business_type_id`    | Configurar según negocio         | Ej: 1 = 0km, 2 = Usados    |
| -                        | `pilot_provider_service`    | `"MercadoLibre"`                 | Identificador del origen   |
| **Datos del Comprador**  |                             |                                  |                            |
| `question.from.nickname` | `pilot_firstname`           | Directo                          | Nombre de usuario ML       |
| `question.from.email`    | `pilot_email`               | Directo si disponible            | No siempre está presente   |
| -                        | `pilot_lastname`            | Extraer de `nickname` si posible | Opcional                   |
| -                        | `pilot_phone`               | No disponible                    | Dejar vacío                |
| -                        | `pilot_cellphone`           | No disponible                    | Dejar vacío                |
| **Datos de la Consulta** |                             |                                  |                            |
| `question.text`          | `pilot_notes`               | Formatear con contexto           | Ver ejemplo abajo          |
| `question.id`            | `pilot_tracking_id`         | String                           | Para evitar duplicados     |
| `question.date_created`  | Metadato interno            | No enviar                        | Usar para filtros          |
| **Datos del Producto**   |                             |                                  |                            |
| `item.title`             | `pilot_product_of_interest` | Directo                          | Producto consultado        |
| `item.title`             | `pilot_car_brand`           | Extraer marca                    | Si es vehículo             |
| `item.title`             | `pilot_car_modelo`          | Extraer modelo                   | Si es vehículo             |
| `item.id`                | `pilot_provider_url`        | URL del producto                 | Ver formato                |
| `item.permalink`         | `pilot_provider_url`        | Alternativa                      | Enlace directo             |
| **Metadatos**            |                             |                                  |                            |
| -                        | `pilot_suborigin_id`        | Configurar en Pilot              | Ej: "ML_QUESTIONS"         |
| `item.seller.id`         | Metadato interno            | No enviar                        | Para identificar tu cuenta |
| -                        | `debug`                     | `0` o `1`                        | 0 = prod, 1 = test         |

---

## Formateo de `pilot_notes`

**Recomendado:**

```javascript
const pilot_notes = `
CONSULTA MERCADOLIBRE

Pregunta: ${question.text}
Producto: ${item.title}
Precio: ${item.currency_id} ${item.price.toLocaleString()}
Stock: ${item.available_quantity} unidades
Condición: ${item.condition === "new" ? "Nuevo" : "Usado"}
Fecha: ${question.date_created}

Link: ${item.permalink}
`.trim();
```

**Ejemplo de salida:**

```
CONSULTA MERCADOLIBRE

Pregunta: ¿Tiene stock disponible?
Producto: Ford Fiesta Kinetic 2024 - 0km
Precio: ARS 25.000.000
Stock: 5 unidades
Condición: Nuevo
Fecha: 2024-01-26T10:30:00.000Z

Link: https://articulo.mercadolibre.com.ar/MLA-123456...
```

---

## Extracción de Marca y Modelo

Para vehículos, extraer del título:

```javascript
function extractCarData(title) {
  // Ejemplo: "Ford Fiesta Kinetic 2024 - 0km"
  const parts = title.split(" ");

  return {
    brand: parts[0] || "", // "Ford"
    model: parts.slice(1, 3).join(" ") || "", // "Fiesta Kinetic"
  };
}
```

**Limitación:** ML no tiene estructura consistente en títulos, esto es best-effort.

---

## Datos No Disponibles en ML

Estos campos de Pilot CRM **no están disponibles** en webhooks de ML:

- `pilot_lastname` - Solo hay `nickname`
- `pilot_phone` / `pilot_cellphone` - ML no comparte por privacidad
- `pilot_city` / `pilot_province` / `pilot_country` - No en webhook de preguntas
- `pilot_address_*` - Datos de dirección no disponibles
- `pilot_birth_date` - No disponible
- `pilot_gender_code` - No disponible
- `pilot_client_identity_document` - No disponible

**Estrategia:** Dejar vacíos o usar valores por defecto.

---

## Ejemplo Completo de Mapeo (JavaScript)

```javascript
// Input: datos de ML
const questionData = {
  id: 123456789,
  text: "¿Acepta permuta?",
  from: {
    nickname: "COMPRADOR123",
    email: "comprador@example.com",
  },
  date_created: "2024-01-26T10:30:00.000Z",
};

const itemData = {
  id: "MLA123456",
  title: "Ford Fiesta Kinetic 2024 - 0km",
  price: 25000000,
  currency_id: "ARS",
  available_quantity: 5,
  condition: "new",
  permalink: "https://articulo.mercadolibre.com.ar/MLA-123456",
};

// Output: parámetros Pilot CRM
const crmPayload = {
  action: "create",
  appkey: process.env.PILOT_CRM_APPKEY,
  debug: 0,

  // Tipo de contacto y negocio
  pilot_contact_type_id: 1, // Electrónico
  pilot_business_type_id: 1, // Ajustar según configuración

  // Datos del comprador
  pilot_firstname: questionData.from.nickname,
  pilot_email: questionData.from.email || "",

  // Datos de la consulta
  pilot_notes: `
CONSULTA MERCADOLIBRE

Pregunta: ${questionData.text}
Producto: ${itemData.title}
Precio: ${itemData.currency_id} ${itemData.price.toLocaleString()}
Stock: ${itemData.available_quantity} unidades
Condición: ${itemData.condition === "new" ? "Nuevo" : "Usado"}

Link: ${itemData.permalink}
  `.trim(),

  pilot_tracking_id: `ML_Q_${questionData.id}`,

  // Datos del producto
  pilot_product_of_interest: itemData.title,
  pilot_car_brand: extractCarData(itemData.title).brand,
  pilot_car_modelo: extractCarData(itemData.title).model,

  // Metadatos
  pilot_provider_service: "MercadoLibre",
  pilot_provider_url: itemData.permalink,
  pilot_suborigin_id: process.env.PILOT_SUBORIGIN_ML || "1",

  // Opt-ins (si están disponibles, sino 0)
  pilot_notificacions_opt_in_consent_flag: 0,
  pilot_publicity_opt_in_consent_flag: 0,
};

function extractCarData(title) {
  const parts = title.split(" ");
  return {
    brand: parts[0] || "",
    model: parts.slice(1, 3).join(" ") || "",
  };
}
```

---

## Configuraciones Recomendadas

### Variables de Entorno

```bash
# n8n .env o Credenciales
PILOT_CRM_APPKEY=9715fc4b-17a8-4e56-ac7a-6deb5fd46u71
PILOT_CONTACT_TYPE_ID=1
PILOT_BUSINESS_TYPE_ID=1
PILOT_SUBORIGIN_ML=7A2E4184
```

### Valores de `pilot_suborigin_id`

Configurar en Pilot CRM panel de administración:

- `7A2E4184` - Landing ML (ejemplo)
- `ML_PREGUNTAS` - Consultas ML
- Consultar "Origen de los datos" en Pilot

---

## Validaciones Recomendadas

Antes de enviar a Pilot CRM:

```javascript
// Validar campos obligatorios
if (!crmPayload.appkey) {
  throw new Error("Missing appkey");
}

if (!crmPayload.pilot_contact_type_id) {
  throw new Error("Missing contact_type_id");
}

if (!crmPayload.pilot_business_type_id) {
  throw new Error("Missing business_type_id");
}

// Validar email (si presente)
if (crmPayload.pilot_email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(crmPayload.pilot_email)) {
    delete crmPayload.pilot_email; // Remover si inválido
  }
}

// Truncar notas si es muy largo (máximo recomendado: 5000 chars)
if (crmPayload.pilot_notes && crmPayload.pilot_notes.length > 5000) {
  crmPayload.pilot_notes = crmPayload.pilot_notes.substring(0, 4997) + "...";
}
```
