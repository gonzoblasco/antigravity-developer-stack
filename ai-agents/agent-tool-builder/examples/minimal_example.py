#!/usr/bin/env python3
"""
Minimal Tool Example - El patrón más simple posible

Demuestra los elementos MÍNIMOS que toda tool debe tener:
1. Descripción clara con INPUT/OUTPUT/ERRORS
2. Tipos con constraints básicos
3. Error estructurado con suggestions

Este es el ejemplo a seguir cuando quieras crear una tool rápidamente.
"""

from typing import Dict, Any


def calculate_percentage(value: float, total: float) -> Dict[str, Any]:
    """
    Calcula el porcentaje de un valor respecto a un total.
    
    INPUTS: value (number, >= 0), total (number, > 0).
    RETURNS: {percentage: number (0-100), formatted: string}.
    ERRORS: 'validation_error' si total es 0 o valores negativos.
    
    Args:
        value: Valor a calcular como porcentaje
        total: Total de referencia (debe ser > 0)
    
    Returns:
        Dict con percentage (número) y formatted (string con %)
    """
    # Validación mínima pero clara
    if total <= 0:
        return {
            "error": {
                "type": "validation_error",
                "message": "Total debe ser mayor a 0",
                "field": "total",
                "provided_value": total,
                "suggestions": [
                    "Proporciona un total positivo",
                    "Ejemplo: total=100"
                ]
            },
            "status": "error"
        }
    
    if value < 0:
        return {
            "error": {
                "type": "validation_error", 
                "message": "Value no puede ser negativo",
                "field": "value",
                "provided_value": value,
                "suggestions": [
                    "Proporciona un valor >= 0",
                    "Ejemplo: value=25"
                ]
            },
            "status": "error"
        }
    
    # Lógica simple
    percentage = (value / total) * 100
    
    return {
        "percentage": round(percentage, 2),
        "formatted": f"{round(percentage, 2)}%",
        "status": "success"
    }


# JSON Schema correspondiente
SCHEMA = {
    "name": "calculate_percentage",
    "description": "Calcula el porcentaje de un valor respecto a un total. INPUTS: value (number >= 0), total (number > 0). RETURNS: {percentage: number, formatted: string}. ERRORS: 'validation_error' si total <= 0 o value < 0.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "value": {
                "type": "number",
                "minimum": 0,
                "description": "Valor a calcular como porcentaje"
            },
            "total": {
                "type": "number",
                "exclusiveMinimum": 0,
                "description": "Total de referencia (debe ser > 0)"
            }
        },
        "required": ["value", "total"]
    }
}


def run_tests():
    """Tests mínimos."""
    print("🧪 Testing calculate_percentage\n")
    
    # Happy path
    result = calculate_percentage(25, 100)
    assert result["status"] == "success"
    assert result["percentage"] == 25.0
    print(f"✅ 25/100 = {result['formatted']}")
    
    # Edge case
    result = calculate_percentage(150, 100)
    assert result["percentage"] == 150.0
    print(f"✅ 150/100 = {result['formatted']} (over 100%)")
    
    # Error: total = 0
    result = calculate_percentage(50, 0)
    assert result["status"] == "error"
    assert "suggestions" in result["error"]
    print(f"✅ Error correctamente estructurado para total=0")
    
    # Error: value negativo
    result = calculate_percentage(-10, 100)
    assert result["status"] == "error"
    print(f"✅ Error correctamente estructurado para value=-10")
    
    print("\n🎉 Todos los tests pasaron!")
    print("\n📝 Este ejemplo muestra el MÍNIMO necesario:")
    print("   • Descripción con INPUTS/RETURNS/ERRORS")
    print("   • Tipos con constraints (minimum, exclusiveMinimum)")
    print("   • Errores con type, message, field, suggestions")


if __name__ == "__main__":
    run_tests()
