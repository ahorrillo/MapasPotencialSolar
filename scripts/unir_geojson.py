import json
import os
import glob

def unir_geojson(directorio=os.getcwd(), archivo_salida="geojson_completo.geojson", patron="*.geojson"):
    """
    Une múltiples archivos GeoJSON en uno solo.
    
    unir_geojson("geojson_divididos/", "datos_completos.geojson")
    
    Args:
        directorio_entrada (str): Directorio que contiene los archivos GeoJSON a unir
        archivo_salida (str): Nombre del archivo de salida
        patron (str): Patrón para buscar archivos GeoJSON (ej: "*.geojson")
    """
    
    # Buscar todos los archivos GeoJSON en el directorio
    archivos = sorted(glob.glob(os.path.join(directorio, patron)))
    
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

def main_unir():
    """Función principal para unir GeoJSON"""
    directorio = input(f"Ingrese el directorio con los archivos GeoJSON (presione Enter para usar '{os.getcwd()}'): ").strip()
    
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

    """
    está hecho el menú para las dos funciones, pero solo unir está implementada.
    """
if __name__ == "__main__":
    print("¿Qué desea hacer?")
    print("1. Dividir un GeoJSON grande")
    print("2. Unir GeoJSON divididos")
    
    opcion = input("Seleccione una opción (1 o 2): ").strip()
    
    if opcion == "1":
        main_dividir()
    elif opcion == "2":
        main_unir()
    else:
        print("Opción no válida")