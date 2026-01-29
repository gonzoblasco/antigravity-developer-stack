/**
 * Ejemplo de autenticación OAuth 2.0 con Mercado Libre
 *
 * Requiere: npm install express axios dotenv
 */

const express = require("express");
const axios = require("axios");
require("dotenv").config();

const app = express();

// Configuración desde variables de entorno
const CLIENT_ID = process.env.MELI_CLIENT_ID;
const CLIENT_SECRET = process.env.MELI_CLIENT_SECRET;
const REDIRECT_URI =
  process.env.MELI_REDIRECT_URI || "http://localhost:3000/callback";

// Almacenamiento simple de tokens (en producción usar base de datos)
let tokens = {
  access_token: null,
  refresh_token: null,
  expires_at: null,
};

// Paso 1: Iniciar flujo OAuth - redirigir usuario a Mercado Libre
app.get("/auth", (req, res) => {
  const authUrl =
    `https://auth.mercadolibre.com.ar/authorization?` +
    `response_type=code&` +
    `client_id=${CLIENT_ID}&` +
    `redirect_uri=${encodeURIComponent(REDIRECT_URI)}`;

  res.redirect(authUrl);
});

// Paso 2: Callback - intercambiar código por access token
app.get("/callback", async (req, res) => {
  const { code } = req.query;

  if (!code) {
    return res.status(400).send("No se recibió código de autorización");
  }

  try {
    const response = await axios.post(
      "https://api.mercadolibre.com/oauth/token",
      {
        grant_type: "authorization_code",
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
        code: code,
        redirect_uri: REDIRECT_URI,
      },
    );

    // Guardar tokens
    tokens.access_token = response.data.access_token;
    tokens.refresh_token = response.data.refresh_token;
    tokens.expires_at = Date.now() + response.data.expires_in * 1000;

    console.log("✅ Autenticación exitosa");
    res.send(`
      <h1>Autenticación Exitosa</h1>
      <p>Access Token: ${tokens.access_token.substring(0, 20)}...</p>
      <p>Expira en: ${response.data.expires_in} segundos</p>
      <a href="/test">Probar API</a>
    `);
  } catch (error) {
    console.error(
      "Error en autenticación:",
      error.response?.data || error.message,
    );
    res.status(500).send("Error al obtener token");
  }
});

// Paso 3: Renovar access token usando refresh token
async function refreshAccessToken() {
  if (!tokens.refresh_token) {
    throw new Error("No hay refresh token disponible");
  }

  try {
    const response = await axios.post(
      "https://api.mercadolibre.com/oauth/token",
      {
        grant_type: "refresh_token",
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
        refresh_token: tokens.refresh_token,
      },
    );

    tokens.access_token = response.data.access_token;
    tokens.refresh_token = response.data.refresh_token;
    tokens.expires_at = Date.now() + response.data.expires_in * 1000;

    console.log("✅ Token renovado exitosamente");
    return tokens.access_token;
  } catch (error) {
    console.error(
      "Error al renovar token:",
      error.response?.data || error.message,
    );
    throw error;
  }
}

// Función helper para obtener token válido
async function getValidToken() {
  if (!tokens.access_token) {
    throw new Error("No hay token. Debe autenticarse primero en /auth");
  }

  // Si el token expira en menos de 5 minutos, renovarlo
  if (tokens.expires_at && Date.now() > tokens.expires_at - 5 * 60 * 1000) {
    return await refreshAccessToken();
  }

  return tokens.access_token;
}

// Ejemplo de uso del API - obtener datos del usuario
app.get("/test", async (req, res) => {
  try {
    const accessToken = await getValidToken();

    const response = await axios.get("https://api.mercadolibre.com/users/me", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    res.json({
      success: true,
      user: {
        id: response.data.id,
        nickname: response.data.nickname,
        email: response.data.email,
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.response?.data || error.message,
    });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
  console.log(`Iniciar autenticación: http://localhost:${PORT}/auth`);
});
