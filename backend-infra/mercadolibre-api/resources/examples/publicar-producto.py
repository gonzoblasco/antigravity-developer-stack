#!/usr/bin/env python3
"""
Ejemplo de publicación de producto en Mercado Libre usando Python

Requiere: pip install requests python-dotenv
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

ACCESS_TOKEN = os.getenv('MELI_ACCESS_TOKEN')
BASE_URL = 'https://api.mercadolibre.com'


def buscar_categoria(query: str, site_id: str = 'MLA') -> list:
    """
    Busca categorías que coincidan con el query
    
    Args:
        query: Término de búsqueda (ej: "zapatillas deportivas")
        site_id: ID del sitio (MLA=Argentina, MLB=Brasil, etc.)
    
    Returns:
        Lista de categorías sugeridas
    """
    url = f"{BASE_URL}/sites/{site_id}/domain_discovery/search"
    params = {'q': query, 'limit': 5}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    categories = []
    for item in response.json():
        categories.append({
            'category_id': item['category_id'],
            'category_name': item['category_name'],
            'domain_id': item.get('domain_id'),
            'domain_name': item.get('domain_name')
        })
    
    return categories


def obtener_atributos_categoria(category_id: str) -> list:
    """
    Obtiene los atributos requeridos y opcionales de una categoría
    
    Args:
        category_id: ID de la categoría
    
    Returns:
        Lista de atributos con sus valores permitidos
    """
    url = f"{BASE_URL}/categories/{category_id}/attributes"
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()


def crear_publicacion(
    titulo: str,
    category_id: str,
    precio: float,
    cantidad: int,
    condicion: str = 'new',
    descripcion: str = '',
    imagenes: Optional[list] = None,
    atributos: Optional[list] = None,
    listing_type: str = 'bronze'
) -> Dict:
    """
    Crea una nueva publicación en Mercado Libre
    
    Args:
        titulo: Título del producto (max 60 caracteres)
        category_id: ID de la categoría
        precio: Precio del producto
        cantidad: Cantidad disponible
        condicion: 'new' o 'used'
        descripcion: Descripción del producto
        imagenes: Lista de URLs de imágenes
        atributos: Lista de atributos específicos de la categoría
        listing_type: Tipo de publicación (free, bronze, silver, gold, premium)
    
    Returns:
        Respuesta del API con los datos de la publicación creada
    """
    if not ACCESS_TOKEN:
        raise ValueError("ACCESS_TOKEN no configurado. Configure MELI_ACCESS_TOKEN en .env")
    
    url = f"{BASE_URL}/items"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Preparar datos de la publicación
    data = {
        'title': titulo,
        'category_id': category_id,
        'price': precio,
        'currency_id': 'ARS',  # Cambiar según el país
        'available_quantity': cantidad,
        'buying_mode': 'buy_it_now',
        'listing_type_id': listing_type,
        'condition': condicion,
        'description': {
            'plain_text': descripcion
        }
    }
    
    # Agregar imágenes si se proporcionan
    if imagenes:
        data['pictures'] = [{'source': url} for url in imagenes]
    
    # Agregar atributos si se proporcionan
    if atributos:
        data['attributes'] = atributos
    
    # Realizar petición
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"✅ Publicación creada exitosamente")
        return response.json()
    else:
        print(f"❌ Error al crear publicación: {response.status_code}")
        print(response.json())
        response.raise_for_status()


def actualizar_precio(item_id: str, nuevo_precio: float) -> Dict:
    """
    Actualiza el precio de una publicación existente
    
    Args:
        item_id: ID de la publicación
        nuevo_precio: Nuevo precio
    
    Returns:
        Respuesta del API
    """
    url = f"{BASE_URL}/items/{item_id}"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {'price': nuevo_precio}
    
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    
    print(f"✅ Precio actualizado a ${nuevo_precio}")
    return response.json()


def pausar_publicacion(item_id: str) -> Dict:
    """
    Pausa una publicación activa
    
    Args:
        item_id: ID de la publicación
    
    Returns:
        Respuesta del API
    """
    url = f"{BASE_URL}/items/{item_id}"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {'status': 'paused'}
    
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    
    print(f"✅ Publicación {item_id} pausada")
    return response.json()


# Ejemplo de uso
if __name__ == '__main__':
    # 1. Buscar categoría apropiada
    print("🔍 Buscando categoría...")
    categorias = buscar_categoria("zapatillas deportivas")
    
    if categorias:
        categoria = categorias[0]
        print(f"📁 Categoría encontrada: {categoria['category_name']} (ID: {categoria['category_id']})")
    else:
        print("❌ No se encontraron categorías")
        exit(1)
    
    # 2. Crear publicación de ejemplo
    print("\n📝 Creando publicación...")
    
    try:
        resultado = crear_publicacion(
            titulo="Zapatillas Deportivas Running - Talle 42",
            category_id=categoria['category_id'],
            precio=15999.99,
            cantidad=5,
            condicion='new',
            descripcion="Zapatillas deportivas ideales para running. Excelente amortiguación y soporte.",
            imagenes=[
                "https://example.com/imagen1.jpg",
                "https://example.com/imagen2.jpg"
            ],
            listing_type='bronze'
        )
        
        print(f"\n✅ Publicación creada con éxito!")
        print(f"   ID: {resultado['id']}")
        print(f"   Permalink: {resultado['permalink']}")
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Error: {e}")
    except ValueError as e:
        print(f"\n❌ Error de configuración: {e}")
