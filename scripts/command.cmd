# Dividir los json:
dividir_geojson("datos_grandes.geojson", 2000, "parte")

# Unir los json:
unir_geojson("geojson_divididos/", "datos_completos.geojson")

# Obtener la dirección:
python potencial-solar-badajoz-best.py parte_001.geojson

# Limpiar la dirección:
python limpiar_direcciones.py

# Minimizar el Json
jq.exe -c . potencial-solar-caceres_completo_opt.geojson > potencial-solar-caceres_completo_opt_min.json
