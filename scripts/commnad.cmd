# Para dividir:
dividir_geojson("datos_grandes.geojson", 2000, "parte")

# Para unir:
unir_geojson("geojson_divididos/", "datos_completos.geojson")

# Para Obtener la dirección:
python potencial-solar-badajoz-best.py parte_001.geojson

# Minimizar el Json
jq.exe -c . potencial-solar-badajoz_completo.geojson > potencial-solar-badajoz_completo_min.json
