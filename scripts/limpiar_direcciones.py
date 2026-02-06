#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar direcciones en un archivo GeoJSON.
Mantiene solo calle + número y elimina todo lo demás.
"""

import json
import re
import sys

def limpiar_direccion(direccion):
    """
    Limpia una dirección manteniendo solo calle + número.

    Ejemplos:
    - "81, Calle José María Giles Ontiveros, Pardaleras, Badajoz..."
      -> "Calle José María Giles Ontiveros 81"
    - "Calle Dolores Marabe, Urbanización Guadiana, Badajoz..."
      -> "Calle Dolores Marabe"
    - "Carretera de Talavera la Real a La Albuera, Alvarado..."
      -> "Carretera de Talavera la Real a La Albuera"
    """
    if not direccion:
        return ""

    # Dividir por comas
    partes = [p.strip() for p in direccion.split(",")]

    # Patrones para detectar calles
    patrones_calle = [
        r'^Calle\s+',
        r'^Avenida\s+',
        r'^Av\.?\s+',
        r'^Carretera\s+',
        r'^Ctra\.?\s+',
        r'^Plaza\s+',
        r'^Paseo\s+',
        r'^Ronda\s+',
        r'^Travesía\s+',
        r'^Camino\s+',
        r'^C\/\s+',  # C/ para Calle
    ]

    # Buscar número en la dirección completa
    numeros = re.findall(r'\b(\d+)\b', direccion)
    numero = numeros[0] if numeros else None

    # Caso 1: Primera parte es solo un número (ej: "81, Calle ...")
    if len(partes) > 1 and re.match(r'^\d+$', partes[0]):
        # La segunda parte probablemente sea la calle
        for patron in patrones_calle:
            if re.match(patron, partes[1], re.IGNORECASE):
                return f"{partes[1]} {partes[0]}"
        return f"{partes[1]} {partes[0]}" if partes[1] else partes[0]

    # Caso 2: Buscar calle en las primeras partes
    for i, parte in enumerate(partes[:2]):  # Mirar solo las primeras 2 partes
        for patron in patrones_calle:
            if re.match(patron, parte, re.IGNORECASE):
                calle = parte
                # Buscar número en las partes siguientes
                if i + 1 < len(partes) and re.match(r'^\d+$', partes[i + 1]):
                    return f"{calle} {partes[i + 1]}"
                elif numero and str(numero) not in calle:
                    return f"{calle} {numero}"
                else:
                    return calle

    # Caso 3: Si no encontramos patrón de calle, tomar primera parte
    # pero buscar si tiene número incluido (ej: "Calle 123")
    primera_parte = partes[0]
    if numero and str(numero) not in primera_parte:
        # Verificar si la primera parte parece una dirección (no solo un número)
        if not re.match(r'^\d+$', primera_parte):
            return f"{primera_parte} {numero}"

    return primera_parte

def procesar_geojson(archivo_entrada, archivo_salida):
    """Procesa un archivo GeoJSON completo."""
    try:
        # Leer el archivo GeoJSON
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        # Contadores para estadísticas
        total = 0
        modificadas = 0

        # Procesar cada feature
        if 'features' in datos:
            for feature in datos['features']:
                if 'properties' in feature and 'direccion' in feature['properties']:
                    total += 1
                    original = feature['properties']['direccion']
                    limpia = limpiar_direccion(original)

                    if original != limpia:
                        feature['properties']['direccion'] = limpia
                        modificadas += 1
                        print(f"✓ {original[:50]}... -> {limpia}")

        # Guardar el resultado
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        # Mostrar resumen
        print(f"\n{'='*50}")
        print(f"RESUMEN:")
        print(f"  Total de direcciones: {total}")
        print(f"  Direcciones modificadas: {modificadas}")
        print(f"  Archivo guardado: {archivo_salida}")
        print(f"{'='*50}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: El archivo '{archivo_entrada}' no es un JSON válido")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

def main():
    """Función principal del script."""
    print("=" * 60)
    print("LIMPIADOR DE DIRECCIONES GEOJSON")
    print("=" * 60)

    # Configurar archivos (puedes cambiar estos valores)
    archivo_entrada = "potencial-solar-caceres_completo.geojson"  # Cambia esto por tu archivo
    archivo_salida = "potencial-solar-caceres_completo_opt.geojson"  # Archivo de salida

    # Preguntar si se quieren usar nombres diferentes
    respuesta = input(f"\n¿Procesar '{archivo_entrada}'? (s/n): ").strip().lower()
    if respuesta not in ['s', 'si', 'yes', 'y']:
        archivo_entrada = input("Nombre del archivo de entrada: ").strip()
        archivo_salida = input("Nombre del archivo de salida: ").strip()

    print(f"\nProcesando {archivo_entrada}...")
    procesar_geojson(archivo_entrada, archivo_salida)

if __name__ == "__main__":
    main()
