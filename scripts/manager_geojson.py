import json
import math
import os
import glob

def dividir_geojson(archivo_entrada, elementos_por_archivo, prefijo_salida="parte"):
    """
    Divide un archivo GeoJSON grande en múltiples archivos más pequeños.
    
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

def unir_geojson(directorio_entrada, archivo_salida="geojson_completo.geojson", patron="*.geojson"):
    """
    Une múltiples archivos GeoJSON en uno solo.
    
    Args:
        directorio_entrada (str): Directorio que contiene los archivos GeoJSON a unir
        archivo_salida (str): Nombre del archivo de salida
        patron (str): Patrón para buscar archivos GeoJSON (ej: "*.geojson")
    """
    
    # Buscar todos los archivos GeoJSON en el directorio
    archivos = sorted(glob.glob(os.path.join(directorio_entrada, patron)))
    
    if not archivos:
        print(f"No se encontraron archivos {patron} en {directorio_entrada}")
        return
    
    print(f"Encontrados {len(archivos)} archivos GeoJSON para unir")
    
    all_features = []
    geojson_metadata = {}
    
    # Leer y combinar todos los archivos
    for i, archivo in enumerate(archivos, 1):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar que sea un FeatureCollection
            if data.get('type') == 'FeatureCollection':
                features = data.get('features', [])
                all_features.extend(features)
                
                # Guardar metadata del primer archivo (excluyendo type y features)
                if i == 1:
                    for key, value in data.items():
                        if key not in ['type', 'features']:
                            geojson_metadata[key] = value
                
                print(f"Procesado: {archivo} ({len(features)} elementos)")
            else:
                print(f"Advertencia: {archivo} no es un FeatureCollection, se omitirá")
        
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
    
    # Crear el GeoJSON completo
    geojson_completo = {
        "type": "FeatureCollection",
        "features": all_features
    }
    
    # Añadir metadata del primer archivo
    geojson_completo.update(geojson_metadata)
    
    # Guardar el archivo unido
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(geojson_completo, f, ensure_ascii=False, indent=2)
    
    print(f"\nUnión completada. Total de elementos: {len(all_features)}")
    print(f"Archivo guardado como: {archivo_salida}")

def main_dividir():
    """Función principal para dividir GeoJSON"""
    archivo_entrada = input("Ingrese la ruta del archivo GeoJSON a dividir: ").strip()
    
    if not os.path.isfile(archivo_entrada):
        print("El archivo especificado no existe")
        return
    
    try:
        elementos = int(input("Ingrese el número de elementos por archivo: "))
        if elementos <= 0:
            print("El número de elementos debe ser mayor a 0")
            return
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

def main_unir():
    """Función principal para unir GeoJSON"""
    directorio = input("Ingrese el directorio con los archivos GeoJSON a unir: ").strip()
    
    if not os.path.isdir(directorio):
        print("El directorio especificado no existe")
        return
    
    nombre_salida = input("Ingrese el nombre del archivo de salida (presione Enter para usar 'geojson_completo.geojson'): ").strip()
    if not nombre_salida:
        nombre_salida = "geojson_completo.geojson"
    
    patron = input("Ingrese el patrón de búsqueda (presione Enter para usar '*.geojson'): ").strip()
    if not patron:
        patron = "*.geojson"
    
    try:
        unir_geojson(directorio, nombre_salida, patron)
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Menú principal"""
    print("=" * 50)
    print("GESTOR DE GEOJSON")
    print("=" * 50)
    print("1. Dividir un GeoJSON grande en partes más pequeñas")
    print("2. Unir múltiples archivos GeoJSON en uno solo")
    print("=" * 50)
    
    opcion = input("Seleccione una opción (1 o 2): ").strip()
    
    if opcion == "1":
        main_dividir()
    elif opcion == "2":
        main_unir()
    else:
        print("Opción no válida. Por favor seleccione 1 o 2.")

if __name__ == "__main__":
    main()