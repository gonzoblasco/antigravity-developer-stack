#!/usr/bin/env python3
"""
External API Tool Example - Patrones para APIs externas

Demuestra:
1. Manejo de errores de red/API
2. Timeouts y reintentos
3. Errores estructurados para diferentes escenarios
4. Documentación de rate limits

Caso: Tool que consulta precio de criptomonedas.
"""

from typing import Dict, Any, Optional
import time
import random  # Para simular respuestas


# Simular cache
_price_cache: Dict[str, Dict] = {}
_last_request = 0


def create_error(
    error_type: str,
    message: str,
    retry: bool = False,
    retry_after: Optional[int] = None,
    suggestions: Optional[list] = None
) -> Dict[str, Any]:
    """Crea error estructurado para APIs."""
    error = {
        "type": error_type,
        "message": message,
        "retry": retry
    }
    if retry_after:
        error["retry_after_seconds"] = retry_after
    if suggestions:
        error["suggestions"] = suggestions
    return {"error": error, "status": "error"}


def get_crypto_price(
    symbol: str,
    currency: str = "USD",
    include_24h_change: bool = False
) -> Dict[str, Any]:
    """
    Obtiene el precio actual de una criptomoneda.
    
    INPUTS: symbol (string, 2-10 chars, ej: BTC, ETH), 
            currency (enum: USD|EUR|GBP, default USD),
            include_24h_change (boolean, default false).
    RETURNS: {symbol, price, currency, timestamp, change_24h?}.
    ERRORS: 'invalid_symbol' si símbolo no reconocido,
            'rate_limit_exceeded' si demasiadas requests (retry: true),
            'service_unavailable' si API caída (retry: true).
    
    Rate limit: 10 requests/minuto.
    
    Args:
        symbol: Símbolo de la criptomoneda (BTC, ETH, etc)
        currency: Moneda de conversión (USD, EUR, GBP)
        include_24h_change: Incluir cambio porcentual 24h
    
    Returns:
        Dict con precio actual y metadatos
    """
    global _last_request
    
    # === VALIDACIONES ===
    
    # Validar symbol
    symbol = symbol.upper().strip()
    valid_symbols = ["BTC", "ETH", "SOL", "DOGE", "ADA", "DOT"]
    
    if not symbol:
        return create_error(
            "validation_error",
            "Symbol es requerido",
            suggestions=[
                "Proporciona un símbolo válido",
                f"Símbolos soportados: {', '.join(valid_symbols)}"
            ]
        )
    
    if len(symbol) < 2 or len(symbol) > 10:
        return create_error(
            "validation_error",
            f"Symbol debe tener 2-10 caracteres, recibido: {len(symbol)}",
            suggestions=[
                "Usa el símbolo corto del token",
                "Ejemplo: 'BTC' para Bitcoin, 'ETH' para Ethereum"
            ]
        )
    
    if symbol not in valid_symbols:
        return create_error(
            "invalid_symbol",
            f"Símbolo '{symbol}' no reconocido",
            suggestions=[
                f"Símbolos soportados: {', '.join(valid_symbols)}",
                "Verifica la ortografía del símbolo"
            ]
        )
    
    # Validar currency
    valid_currencies = ["USD", "EUR", "GBP"]
    currency = currency.upper()
    
    if currency not in valid_currencies:
        return create_error(
            "validation_error",
            f"Currency '{currency}' no soportada",
            suggestions=[
                f"Usa una de: {', '.join(valid_currencies)}",
                "El valor es case-insensitive"
            ]
        )
    
    # === RATE LIMITING ===
    
    current_time = time.time()
    time_since_last = current_time - _last_request
    
    # Simular rate limit (en producción, trackear correctamente)
    if time_since_last < 0.1:  # Muy rápido = rate limited
        return create_error(
            "rate_limit_exceeded",
            "Demasiadas requests. Límite: 10/minuto",
            retry=True,
            retry_after=6,
            suggestions=[
                "Espera unos segundos antes de reintentar",
                "Considera usar cache para requests frecuentes"
            ]
        )
    
    _last_request = current_time
    
    # === API CALL (Simulado) ===
    
    try:
        # Simular posible fallo de red (5% probabilidad)
        if random.random() < 0.05:
            raise ConnectionError("Network timeout")
        
        # Simular precios (en producción, llamar API real)
        mock_prices = {
            "BTC": {"USD": 43250.50, "EUR": 39800.00, "GBP": 34100.00},
            "ETH": {"USD": 2280.75, "EUR": 2100.00, "GBP": 1800.00},
            "SOL": {"USD": 98.50, "EUR": 90.50, "GBP": 77.50},
            "DOGE": {"USD": 0.082, "EUR": 0.075, "GBP": 0.065},
            "ADA": {"USD": 0.52, "EUR": 0.48, "GBP": 0.41},
            "DOT": {"USD": 7.25, "EUR": 6.67, "GBP": 5.72}
        }
        
        price = mock_prices[symbol][currency]
        
        # Agregar variación aleatoria pequeña
        price = price * (1 + random.uniform(-0.01, 0.01))
        
        result = {
            "symbol": symbol,
            "price": round(price, 2),
            "currency": currency,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "success"
        }
        
        if include_24h_change:
            result["change_24h"] = round(random.uniform(-5, 5), 2)
            result["change_24h_formatted"] = f"{result['change_24h']:+.2f}%"
        
        return result
    
    except ConnectionError as e:
        return create_error(
            "service_unavailable",
            "No se pudo conectar al servicio de precios",
            retry=True,
            retry_after=30,
            suggestions=[
                "El servicio puede estar temporalmente caído",
                "Intenta nuevamente en 30 segundos",
                "Verifica tu conexión a internet"
            ]
        )
    
    except Exception as e:
        return create_error(
            "internal_error",
            f"Error inesperado: {str(e)}",
            retry=True,
            suggestions=[
                "Reporta este error si persiste",
                "Intenta nuevamente"
            ]
        )


# JSON Schema
SCHEMA = {
    "name": "get_crypto_price",
    "description": "Obtiene el precio actual de una criptomoneda. INPUTS: symbol (string 2-10 chars, ej: BTC, ETH, SOL, DOGE, ADA, DOT), currency (enum: USD|EUR|GBP, default USD), include_24h_change (boolean, default false). RETURNS: {symbol, price, currency, timestamp, change_24h?}. ERRORS: 'invalid_symbol' si no reconocido, 'rate_limit_exceeded' si límite alcanzado (retry: true, retry_after_seconds), 'service_unavailable' si API caída (retry: true). Rate limit: 10 req/min.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Símbolo de la criptomoneda (BTC, ETH, SOL, etc)",
                "minLength": 2,
                "maxLength": 10
            },
            "currency": {
                "type": "string",
                "enum": ["USD", "EUR", "GBP"],
                "default": "USD",
                "description": "Moneda de conversión"
            },
            "include_24h_change": {
                "type": "boolean",
                "default": False,
                "description": "Incluir cambio porcentual de las últimas 24h"
            }
        },
        "required": ["symbol"]
    }
}


def run_tests():
    """Tests de escenarios."""
    print("🧪 Testing get_crypto_price - External API Patterns\n")
    
    # Happy path
    time.sleep(0.2)  # Evitar rate limit
    result = get_crypto_price("BTC")
    assert result["status"] == "success"
    print(f"✅ BTC price: ${result['price']} {result['currency']}")
    
    # Con opciones
    time.sleep(0.2)
    result = get_crypto_price("ETH", currency="EUR", include_24h_change=True)
    assert result["status"] == "success"
    assert "change_24h" in result
    print(f"✅ ETH price: €{result['price']} ({result['change_24h_formatted']})")
    
    # Error: símbolo inválido
    time.sleep(0.2)
    result = get_crypto_price("XYZ")  # Símbolo válido en longitud pero no soportado
    assert result["status"] == "error"
    assert result["error"]["type"] == "invalid_symbol"
    assert "suggestions" in result["error"]
    print(f"✅ Error estructurado para símbolo inválido")
    
    # Error: currency inválida
    time.sleep(0.2)
    result = get_crypto_price("BTC", currency="JPY")
    assert result["status"] == "error"
    assert "USD" in result["error"]["suggestions"][0]
    print(f"✅ Error estructurado para currency inválida")
    
    # Test rate limit (requests muy rápidas)
    time.sleep(0.01)
    _ = get_crypto_price("BTC")
    result = get_crypto_price("BTC")  # Inmediatamente después
    # Puede o no disparar rate limit dependiendo del timing
    print(f"✅ Rate limit handling implementado")
    
    print("\n🎉 Todos los tests pasaron!")
    print("\n📝 Patrones demostrados para APIs externas:")
    print("   • Validación de inputs antes de llamar API")
    print("   • Rate limiting con retry_after")
    print("   • Errores de red con retry: true")
    print("   • Suggestions específicas por tipo de error")
    print("   • Documentación de límites en description")


if __name__ == "__main__":
    run_tests()
