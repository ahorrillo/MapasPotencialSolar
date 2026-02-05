import json
import math
import os

def dividir_geojson(archivo_entrada, elementos_por_archivo, prefijo_salida="parte"):
    """
    Divide un archivo GeoJSON grande en múltiples archivos más pequeños.
    
    dividir_geojson("potencial-solar-caceres.geojson", 10000, "parte")
    
    Args:
        archivo_entrada (str): Ruta al archivo GeoJSON de entrada
        elementos_por_archivo (int): Número de elementos por archivo de salida
        prefijo_salida (str): Prefijo para los archivos de salida
    """
    
    # Leer el archivo GeoJSON original
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    # Verificar que sea un FeatureCollection
    if geojson_data.get('type') != 'FeatureCollection':
        raise ValueError("El archivo GeoJSON debe ser de tipo FeatureCollection")
    
    features = geojson_data.get('features', [])
    total_elementos = len(features)
    
    if total_elementos == 0:
        print("No hay elementos en el archivo GeoJSON")
        return
    
    # Calcular número de archivos necesarios
    num_archivos = math.ceil(total_elementos / elementos_por_archivo)
    print(f"Total de elementos: {total_elementos}")
    print(f"Dividiendo en {num_archivos} archivos de {elementos_por_archivo} elementos cada uno")
    
    # Crear directorio para los archivos divididos si no existe
    os.makedirs("geojson_divididos", exist_ok=True)
    
    # Dividir y guardar los archivos
    for i in range(num_archivos):
        inicio = i * elementos_por_archivo
        fin = min((i + 1) * elementos_por_archivo, total_elementos)
        
        # Crear nuevo GeoJSON con las features correspondientes
        nuevo_geojson = {
            "type": "FeatureCollection",
            "features": features[inicio:fin]
        }
        
        # Mantener otras propiedades del GeoJSON original si existen
        for key, value in geojson_data.items():
            if key not in ['type', 'features']:
                nuevo_geojson[key] = value
        
        # Guardar el archivo
        nombre_archivo = f"geojson_divididos/{prefijo_salida}_{i+1:03d}.geojson"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(nuevo_geojson, f, ensure_ascii=False, indent=2)
        
        print(f"Creado: {nombre_archivo} (elementos {inicio+1} a {fin})")
    
    print(f"\nDivisión completada. Archivos guardados en: geojson_divididos/")

def main_dividir():
    """Función principal para dividir GeoJSON"""
    archivo_entrada = input("Ingrese la ruta del archivo GeoJSON a dividir: ").strip()
    
    try:
        elementos = int(input("Ingrese el número de elementos por archivo: "))
    except ValueError:
        print("Por favor ingrese un número válido")
        return
    
    prefijo = input("Ingrese el prefijo para los archivos (presione Enter para usar 'parte'): ").strip()
    if not prefijo:
        prefijo = "parte"
    
    try:
        dividir_geojson(archivo_entrada, elementos, prefijo)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main_dividir()