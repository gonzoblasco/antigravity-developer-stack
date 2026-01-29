# Pilot Solutions CRM API Reference

## Base URL

```
https://api.pilotsolution.net/webhooks/welcome.php
```

**IMPORTANTE**: Cualquier respuesta que no sea HTTP 200 es un error.

---

## Autenticación

Pilot CRM usa autenticación vía **API Key** (`appkey`).

**Obtener tu appkey:**

1. Solicítalo a soporte de Pilot Solutions
2. O consíguelo desde la configuración de tu instancia de Pilot

**Formato del appkey:**

```
9715fc4b-17a8-4e56-ac7a-6deb5fd46u71
```

---

## Crear Lead (Webhook)

### Endpoint

```http
POST https://api.pilotsolution.net/webhooks/welcome.php
Content-Type: application/x-www-form-urlencoded
```

### Parámetros Requeridos

| Parámetro                                             | Tipo       | Descripción                                        | Ejemplo                       |
| ----------------------------------------------------- | ---------- | -------------------------------------------------- | ----------------------------- |
| `action`                                              | string     | **Obligatorio**. Valor fijo: "create"              | `create`                      |
| `appkey`                                              | string     | **Obligatorio**. API Key de tu instancia           | `9715fc4b-17a8-4e56-ac7a-...` |
| `pilot_contact_type_id` o `pilot_contact_type_code`   | int/string | **Obligatorio (uno de los dos)**. Tipo de contacto | `1` o `"electrónico"`         |
| `pilot_business_type_id` o `pilot_business_type_code` | int/string | **Obligatorio (uno de los dos)**. Tipo de negocio  | `1` o `"Nuevo"`               |

> **Nota**: Si envías tanto el `_id` como el `_code`, el sistema tomará el `_id` como mandante.

### Parámetros Opcionales (Recomendados)

| Parámetro                   | Tipo   | Descripción                            |
| --------------------------- | ------ | -------------------------------------- |
| `pilot_firstname`           | string | Nombre del lead                        |
| `pilot_lastname`            | string | Apellido del lead                      |
| `pilot_second_lastname`     | string | Segundo apellido                       |
| `pilot_email`               | string | Email del lead                         |
| `pilot_phone`               | string | Teléfono fijo                          |
| `pilot_cellphone`           | string | Teléfono móvil                         |
| `pilot_notes`               | string | Comentarios/observaciones del lead     |
| `pilot_suborigin_id`        | string | Código de origen primario del lead     |
| `pilot_provider_service`    | string | Nombre del servicio que provee el dato |
| `pilot_tracking_id`         | string | ID único para identificar el lead      |
| `pilot_product_of_interest` | string | Producto por el que consulta           |
| `pilot_car_brand`           | string | Marca del vehículo                     |
| `pilot_car_modelo`          | string | Modelo del vehículo                    |
| `pilot_assigned_user`       | string | Email del usuario Pilot asignado       |

### Parámetros de Control

| Parámetro            | Tipo   | Descripción                                      | Valores             |
| -------------------- | ------ | ------------------------------------------------ | ------------------- |
| `debug`              | int    | Flag de testing. 0 = normal, 1 = no crea el lead | `0` o `1`           |
| `notification_email` | string | Email para recibir copia del dato ingresado      | `admin@example.com` |

### Otros Parámetros Disponibles

- `pilot_city` - Ciudad
- `pilot_province` - Provincia
- `pilot_country` - País
- `pilot_vendor_name` - Nombre del proveedor
- `pilot_vendor_email` - Email del proveedor
- `pilot_vendor_phone` - Teléfono del proveedor
- `pilot_provider_url` - URL del servicio que recolectó el dato
- `pilot_client_company` - Nombre de la empresa
- `pilot_client_identity_document` - Documento de identidad
- `pilot_client_ip` - IP del lead
- `pilot_best_contact_time` - Horario preferido de contacto
- `pilot_product_code` - Código de producto (genera oferta automática)
- `pilot_notificacions_opt_in_consent_flag` - Acepta notificaciones (0/1)
- `pilot_publicity_opt_in_consent_flag` - Acepta publicidad (0/1)
- `pilot_address_street` - Calle
- `pilot_addresss_number` - Número (nota el typo en el parámetro original)
- `pilot_address_floor` - Piso
- `pilot_address_department` - Departamento
- `pilot_address_postal_code` - Código postal
- `pilot_birth_date` - Fecha de nacimiento (DD/MM/AA)
- `pilot_gender_code` - Código de género

---

## Response Format

Todas las respuestas son JSON con la siguiente estructura:

### Respuesta Exitosa

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "message": "(3.2) El servicio de carga de datos se ejecuto correctamente.",
    "assigned_user_id": 80,
    "success": true,
    "id": 8855
  }
}
```

**Campos de `data`:**

- `message`: Mensaje descriptivo del resultado
- `assigned_user_id`: ID del usuario Pilot asignado (opcional)
- `success`: Boolean indicando inserción exitosa
- `id`: ID numérico del lead creado en Pilot

### Respuesta de Error

```json
{
  "success": false,
  "message": "Error",
  "data": "El parametro requerido appkey no fue seteado"
}
```

---

## Maestros (Master Data)

### Obtener Tipo de Contacto

**Endpoint:** `masters/read.php` (consultar documentación de Pilot)

Valores comunes:

- `1` - Electrónico
- `2` - Telefónico
- `3` - Entrevista

_(Pueden variar según configuración de cada instancia)_

### Obtener Tipo de Negocio

**Endpoint:** `masters/read.php`

Valores comunes:

- `1` - Convencional / 0km
- `2` - Usados
- `3` - Plan de Ahorro

_(Pueden variar según configuración de cada instancia)_

### Obtener Suborígenes

Consultar en Pilot CRM:

- Panel de Administración → Informe "Origen de los datos"

---

## Códigos de Error Comunes

| Error                                          | Causa                        | Solución                                                     |
| ---------------------------------------------- | ---------------------------- | ------------------------------------------------------------ |
| "El parametro requerido appkey no fue seteado" | Falta `appkey`               | Verificar credenciales                                       |
| "Parameter pilot_contact_type_id not set"      | Falta tipo de contacto       | Enviar `pilot_contact_type_id` o `pilot_contact_type_code`   |
| "Parameter pilot_business_type_id not set"     | Falta tipo de negocio        | Enviar `pilot_business_type_id` o `pilot_business_type_code` |
| HTTP != 200                                    | Error de conexión o servidor | Verificar URL, conectividad                                  |

---

## Rate Limits

**No documentado oficialmente**, pero se recomienda:

- No más de 10 requests por segundo
- Implementar backoff si se reciben errores 5xx
- Usar `debug: 1` para testing sin impactar producción

---

## Ejemplo cURL

```bash
curl -X POST https://api.pilotsolution.net/webhooks/welcome.php \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "action=create" \
  -d "appkey=9715fc4b-17a8-4e56-ac7a-6deb5fd46u71" \
  -d "pilot_firstname=Juan" \
  -d "pilot_lastname=Pérez" \
  -d "pilot_email=juan@example.com" \
  -d "pilot_phone=1147899000" \
  -d "pilot_cellphone=1160403456" \
  -d "pilot_contact_type_id=1" \
  -d "pilot_business_type_id=1" \
  -d "pilot_notes=Consulta desde MercadoLibre sobre Ford Fiesta" \
  -d "pilot_provider_service=MercadoLibre" \
  -d "pilot_tracking_id=ML123456789" \
  -d "pilot_product_of_interest=Ford Fiesta 2024" \
  -d "debug=0"
```

---

## Ejemplo JavaScript (Node.js)

```javascript
const axios = require("axios");
const qs = require("querystring");

async function createLeadInPilotCRM(leadData) {
  const data = {
    action: "create",
    appkey: process.env.PILOT_CRM_APPKEY,
    debug: 0,
    pilot_contact_type_id: 1,
    pilot_business_type_id: 1,
    ...leadData,
  };

  try {
    const response = await axios.post(
      "https://api.pilotsolution.net/webhooks/welcome.php",
      qs.stringify(data),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      },
    );

    if (response.data.success) {
      console.log("Lead created:", response.data.data.id);
      return response.data.data.id;
    } else {
      throw new Error(response.data.data);
    }
  } catch (error) {
    console.error("Error creating lead:", error.message);
    throw error;
  }
}

// Uso
createLeadInPilotCRM({
  pilot_firstname: "María",
  pilot_email: "maria@example.com",
  pilot_notes: "Interesada en Volkswagen Gol",
  pilot_provider_service: "MercadoLibre",
  pilot_tracking_id: "ML987654321",
});
```

---

## Integración vía Email (ADF)

Pilot CRM también soporta integración vía email con formato ADF XML.

**Endpoint:** Enviar email a dirección configurada en Pilot

**Formato:** XML con estructura ADF

**Ver más:** Documentación oficial de Pilot Solutions
