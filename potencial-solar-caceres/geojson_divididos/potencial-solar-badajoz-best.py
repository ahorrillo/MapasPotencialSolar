# -*- coding: utf-8 -*-
import json
import time
import sys
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Cargar GeoJSON con manejo de errores
try:
    with open('parte_002.geojson', 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    print("✓ GeoJSON cargado correctamente")
except FileNotFoundError:
    print("✗ ERROR: No se encuentra el archivo 'potencial-solar-badajoz.geojson'")
    print("Asegúrate de que está en la misma carpeta que este script")
    sys.exit(1)
except json.JSONDecodeError:
    print("✗ ERROR: El archivo GeoJSON tiene formato incorrecto")
    sys.exit(1)

# Inicializar geolocalizador
try:
    geolocator = Nominatim(user_agent="badajoz_solar_agent")
    print("✓ Geolocalizador inicializado")
except Exception as e:
    print(f"✗ ERROR al inicializar geolocalizador: {e}")
    sys.exit(1)

def centroid(coords):
    """Calcula el centroide del polígono de forma segura"""
    try:
        # Asegurarnos de que tenemos las coordenadas correctamente
        if not coords or not coords[0]:
            return None, None

        polygon_coords = coords[0]
        lat_sum = sum(lat for lng, lat in polygon_coords)
        lng_sum = sum(lng for lng, lat in polygon_coords)
        n = len(polygon_coords)

        if n == 0:
            return None, None

        return lat_sum / n, lng_sum / n
    except Exception as e:
        print(f"  ⚠ Error calculando centroide: {e}")
        return None, None

# Verificar que hay features
if 'features' not in geojson or not geojson['features']:
    print("✗ ERROR: El GeoJSON no tiene features o está vacío")
    sys.exit(1)

# Obtener número total de features
total_features = len(geojson['features'])
print(f"✓ Encontrados {total_features} polígonos para procesar\n")

# Contadores para estadísticas
exitos = 0
errores = 0
sin_direccion = 0

print("Iniciando geocodificación...")
print("=" * 60)

# Procesar cada feature
for i, feature in enumerate(geojson['features']):
    # Mostrar progreso
    porcentaje = (i + 1) / total_features * 100
    barra = '█' * int(porcentaje / 2.5) + '░' * (40 - int(porcentaje / 2.5))

    sys.stdout.write(f'\r[{barra}] {i+1}/{total_features} ({porcentaje:.1f}%)')
    sys.stdout.flush()

    # Obtener coordenadas
    try:
        coords = feature['geometry']['coordinates']
        lat, lng = centroid(coords)

        if lat is None or lng is None:
            feature['properties']['direccion'] = 'Coordenadas inválidas'
            errores += 1
            continue

    except Exception as e:
        feature['properties']['direccion'] = f'Error coordenadas: {str(e)[:30]}'
        errores += 1
        continue

    # Intentar geocodificación
    try:
        location = geolocator.reverse((lat, lng), exactly_one=True, timeout=15)

        if location and location.address:
            direccion_corta = location.address[:70] + "..." if len(location.address) > 70 else location.address
            feature['properties']['direccion'] = location.address
            exitos += 1

            # Mostrar cada 5 elementos
            if i % 5 == 0:
                print(f"\n  [{i+1}] ✓ {direccion_corta}")

        else:
            feature['properties']['direccion'] = 'Sin dirección encontrada'
            sin_direccion += 1
            if i % 10 == 0:
                print(f"\n  [{i+1}] ⚠ Sin dirección en ({lat:.4f}, {lng:.4f})")

    except (GeocoderTimedOut, GeocoderServiceError) as e:
        feature['properties']['direccion'] = f'Error API: {str(e)[:30]}'
        errores += 1
        if i % 5 == 0:
            print(f"\n  [{i+1}] ✗ Error de conexión")

    except Exception as e:
        feature['properties']['direccion'] = f'Error: {str(e)[:30]}'
        errores += 1

    # Pausa para no saturar el servidor
    time.sleep(1.2)

# Línea final
print(f"\r[{'█'*40}] {total_features}/{total_features} (100.0%)")
print("\n" + "=" * 60)

# Estadísticas
print("\n📊 ESTADÍSTICAS:")
print(f"  ✓ Correctos:     {exitos}/{total_features}")
print(f"  ⚠ Sin dirección: {sin_direccion}/{total_features}")
print(f"  ✗ Errores:       {errores}/{total_features}")

# Guardar nuevo GeoJSON
try:
    output_file = 'parte_002-direcciones.geojson'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Archivo guardado: '{output_file}'")
except Exception as e:
    print(f"\n✗ ERROR al guardar archivo: {e}")

# Tiempo estimado
tiempo_total = total_features * 1.2
print(f"⏱  Tiempo estimado: {tiempo_total:.0f} segundos (~{tiempo_total/60:.1f} minutos)")
print("\n✅ Proceso completado!")
