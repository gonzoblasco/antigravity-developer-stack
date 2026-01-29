# Manejo de Errores - MercadoLibre API

## Tabla Rápida de Errores

| Código | Nombre            | Causa Común             | Solución                               |
| ------ | ----------------- | ----------------------- | -------------------------------------- |
| 400    | Bad Request       | Payload malformado      | Validar JSON y campos requeridos       |
| 401    | Unauthorized      | Token expirado/inválido | [Renovar token](#401-unauthorized)     |
| 403    | Forbidden         | Sin permisos            | Verificar scopes de la app             |
| 404    | Not Found         | Recurso no existe       | Verificar IDs                          |
| 429    | Too Many Requests | Rate limit excedido     | [Implementar backoff](#429-rate-limit) |
| 500    | Server Error      | Error interno ML        | Reintentar con backoff                 |

---

## 401 Unauthorized

### Síntomas

```json
{
  "message": "invalid_token",
  "error": "not_found",
  "status": 401
}
```

### Causas

1. **Token expirado** - El `access_token` expira cada 6 horas
2. **Token revocado** - Usuario desautorizó la app
3. **Token malformado** - Error de copia/pegado

### Solución

```javascript
async function makeRequest(url, accessToken, refreshToken) {
  try {
    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    return response.data;
  } catch (error) {
    if (error.response?.status === 401) {
      // Renovar token
      const newTokens = await refreshAccessToken(refreshToken);
      // Reintentar con nuevo token
      return makeRequest(url, newTokens.access_token, newTokens.refresh_token);
    }
    throw error;
  }
}

async function refreshAccessToken(refreshToken) {
  const response = await axios.post(
    "https://api.mercadolibre.com/oauth/token",
    new URLSearchParams({
      grant_type: "refresh_token",
      client_id: process.env.ML_APP_ID,
      client_secret: process.env.ML_SECRET,
      refresh_token: refreshToken,
    }),
  );
  return response.data;
}
```

---

## 403 Forbidden

### Síntomas

```json
{
  "message": "The caller is not authorized to access this resource",
  "error": "forbidden",
  "status": 403
}
```

### Causas

1. **Scopes insuficientes** - La app no tiene permisos para esa operación
2. **Recurso de otro usuario** - Intentando acceder a datos de otro vendedor
3. **App no verificada** - Algunas APIs requieren verificación

### Solución

- Verificar permisos de la aplicación en Developer Portal
- Confirmar que el usuario autorizó todos los scopes necesarios
- Para APIs restringidas, solicitar acceso especial

---

## 429 Rate Limit

### Síntomas

```json
{
  "message": "Too many requests",
  "error": "too_many_requests",
  "status": 429
}
```

### Límites Conocidos

| Tipo de Request    | Límite Aproximado  |
| ------------------ | ------------------ |
| Consultas públicas | 10,000/día         |
| Con autenticación  | Varía por endpoint |
| Bulk operations    | 1,000/hora         |

### Solución: Exponential Backoff

```javascript
async function requestWithBackoff(fn, maxRetries = 5) {
  let retries = 0;

  while (retries < maxRetries) {
    try {
      return await fn();
    } catch (error) {
      if (error.response?.status !== 429) throw error;

      retries++;
      const delay = Math.pow(2, retries) * 1000; // 2s, 4s, 8s, 16s, 32s
      console.log(`Rate limited. Waiting ${delay}ms...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error("Max retries exceeded");
}

// Uso
const items = await requestWithBackoff(() =>
  axios.get("https://api.mercadolibre.com/items/MLA123"),
);
```

### Mejores Prácticas

1. **Cachear respuestas** estáticas (categorías, atributos)
2. **Usar webhooks** en vez de polling
3. **Batch requests** cuando sea posible
4. **Implementar queue** para operaciones masivas

---

## 400 Bad Request

### Síntomas Comunes

```json
{
  "message": "body.title is required",
  "error": "bad_request",
  "status": 400,
  "cause": [{ "code": "required", "field": "title" }]
}
```

### Campos Requeridos para Publicar

| Campo                | Tipo   | Obligatorio   |
| -------------------- | ------ | ------------- |
| `title`              | string | ✅            |
| `category_id`        | string | ✅            |
| `price`              | number | ✅            |
| `currency_id`        | string | ✅            |
| `available_quantity` | number | ✅            |
| `buying_mode`        | string | ✅            |
| `listing_type_id`    | string | ✅            |
| `condition`          | string | ✅            |
| `pictures`           | array  | ✅ (mínimo 1) |

### Validación Previa

```javascript
function validateItem(item) {
  const required = [
    "title",
    "category_id",
    "price",
    "currency_id",
    "available_quantity",
    "buying_mode",
    "listing_type_id",
    "condition",
  ];

  const missing = required.filter((field) => !item[field]);

  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(", ")}`);
  }

  if (!item.pictures || item.pictures.length === 0) {
    throw new Error("At least one picture is required");
  }

  return true;
}
```

---

## Debugging Tips

### 1. Verificar Token

```bash
curl -X GET 'https://api.mercadolibre.com/users/me' \
  -H 'Authorization: Bearer {TOKEN}'
```

### 2. Inspeccionar Headers de Respuesta

```
X-Content-Created: 2024-01-15T10:30:00.000-04:00
X-Request-Id: abc123-def456
```

### 3. Usar Sandbox para Pruebas

- Crear usuarios de prueba en Developer Portal
- No usar producción para tests de integración
