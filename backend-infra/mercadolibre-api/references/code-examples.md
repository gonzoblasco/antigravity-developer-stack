# Ejemplos de Código - MercadoLibre API

## Búsqueda de Productos

### Búsqueda Simple

```bash
curl -X GET 'https://api.mercadolibre.com/sites/MLA/search?q=notebook&limit=10'
```

### Búsqueda con Filtros

```bash
curl -X GET 'https://api.mercadolibre.com/sites/MLA/search
  ?q=notebook
  &category=MLA1055
  &price=50000-100000
  &condition=new
  &limit=20
  &offset=0'
```

### Respuesta Ejemplo

```json
{
  "results": [
    {
      "id": "MLA123456789",
      "title": "Notebook Lenovo 15.6 Intel Core i5",
      "price": 85000,
      "currency_id": "ARS",
      "condition": "new",
      "permalink": "https://articulo.mercadolibre.com.ar/MLA-123456789",
      "thumbnail": "https://http2.mlstatic.com/...",
      "seller": {
        "id": 987654321,
        "nickname": "TIENDA_OFICIAL"
      }
    }
  ],
  "paging": {
    "total": 150,
    "offset": 0,
    "limit": 10
  }
}
```

---

## Obtener Detalles de Item

```bash
curl -X GET 'https://api.mercadolibre.com/items/MLA123456789'
```

### Con Descripción

```bash
curl -X GET 'https://api.mercadolibre.com/items/MLA123456789/description'
```

---

## Publicar un Producto

```bash
curl -X POST 'https://api.mercadolibre.com/items' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Producto de prueba - No ofertar",
    "category_id": "MLA1055",
    "price": 35000,
    "currency_id": "ARS",
    "available_quantity": 10,
    "buying_mode": "buy_it_now",
    "listing_type_id": "bronze",
    "condition": "new",
    "description": {"plain_text": "Descripción detallada del producto"},
    "pictures": [
      {"source": "https://example.com/image1.jpg"},
      {"source": "https://example.com/image2.jpg"}
    ],
    "attributes": [
      {"id": "BRAND", "value_name": "Marca Ejemplo"},
      {"id": "MODEL", "value_name": "Modelo 2024"}
    ]
  }'
```

### Listing Types Disponibles

| Tipo           | Descripción | Comisión |
| -------------- | ----------- | -------- |
| `free`         | Gratuita    | 0%       |
| `bronze`       | Clásica     | ~10%     |
| `silver`       | Premium     | ~15%     |
| `gold_special` | Oro Premium | ~20%     |

---

## Gestionar Órdenes

### Listar Órdenes del Vendedor

```bash
curl -X GET 'https://api.mercadolibre.com/orders/search?seller={SELLER_ID}&sort=date_desc' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}'
```

### Obtener Orden Específica

```bash
curl -X GET 'https://api.mercadolibre.com/orders/{ORDER_ID}' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}'
```

---

## Gestionar Preguntas

### Ver Preguntas de un Item

```bash
curl -X GET 'https://api.mercadolibre.com/questions/search?item={ITEM_ID}&status=UNANSWERED' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}'
```

### Responder Pregunta

```bash
curl -X POST 'https://api.mercadolibre.com/answers' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}' \
  -H 'Content-Type: application/json' \
  -d '{
    "question_id": 123456789,
    "text": "Hola! Sí, tenemos stock. Gracias por tu consulta."
  }'
```

---

## Configurar Webhooks

### Registrar URL de Notificaciones

```bash
curl -X PUT 'https://api.mercadolibre.com/applications/{APP_ID}' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}' \
  -H 'Content-Type: application/json' \
  -d '{
    "notifications": {
      "webhook_url": "https://tu-servidor.com/webhook/ml"
    }
  }'
```

### Suscribirse a Topics

```bash
curl -X POST 'https://api.mercadolibre.com/applications/{APP_ID}/subscriptions' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}' \
  -H 'Content-Type: application/json' \
  -d '{
    "topic": "orders_v2"
  }'
```

**Topics disponibles:**

- `orders_v2` - Cambios en órdenes
- `items` - Cambios en publicaciones
- `questions` - Nuevas preguntas
- `messages` - Mensajes de compradores
- `claims` - Reclamos

### Payload de Notificación

```json
{
  "resource": "/orders/123456789",
  "user_id": 987654321,
  "topic": "orders_v2",
  "application_id": 1234567890123456,
  "attempts": 1,
  "sent": "2024-01-15T10:30:00.000-04:00",
  "received": "2024-01-15T10:30:01.000-04:00"
}
```

---

## Ejemplos en Node.js

```javascript
const axios = require("axios");

const ML_API = "https://api.mercadolibre.com";

// Buscar productos
async function searchProducts(query, siteId = "MLA") {
  const response = await axios.get(`${ML_API}/sites/${siteId}/search`, {
    params: { q: query, limit: 10 },
  });
  return response.data.results;
}

// Publicar producto
async function createItem(accessToken, itemData) {
  const response = await axios.post(`${ML_API}/items`, itemData, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return response.data;
}

// Responder pregunta
async function answerQuestion(accessToken, questionId, text) {
  const response = await axios.post(
    `${ML_API}/answers`,
    { question_id: questionId, text },
    { headers: { Authorization: `Bearer ${accessToken}` } },
  );
  return response.data;
}
```

---

## Ejemplos en Python

```python
import requests

ML_API = 'https://api.mercadolibre.com'

def search_products(query, site_id='MLA'):
    """Buscar productos en MercadoLibre"""
    response = requests.get(
        f'{ML_API}/sites/{site_id}/search',
        params={'q': query, 'limit': 10}
    )
    return response.json()['results']

def create_item(access_token, item_data):
    """Publicar un producto"""
    response = requests.post(
        f'{ML_API}/items',
        json=item_data,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return response.json()

def answer_question(access_token, question_id, text):
    """Responder una pregunta"""
    response = requests.post(
        f'{ML_API}/answers',
        json={'question_id': question_id, 'text': text},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return response.json()
```
