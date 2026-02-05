# Potencial Solar – Geocodificación de GeoJSON

[![PYTHON](https://img.shields.io/badge/Python-3-%23777bb3)](https://winpython.github.io/)
[![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen)](https://github.com/ahorrillo)
[![License](https://img.shields.io/badge/License-Vocento-informational)](LICENSE)

Este repositorio contiene varios **scripts en Python** para procesar grandes archivos **GeoJSON de potencial solar**, dividirlos en partes manejables, **obtener direcciones postales mediante geocodificación inversa** y finalmente **unirlos de nuevo**.

El flujo está pensado para trabajar con archivos muy grandes (decenas o cientos de miles de polígonos) sin saturar memoria ni servicios de geocodificación.

Actualmente se ha usado con:
- `potencial-solar-badajoz.geojson`
- `potencial-solar-caceres.geojson`

---

## 📂 Estructura del repositorio

```text
.
├── potencial-solar-badajoz/
│   ├── fuentes/
│   │   ├── potencial-solar-badajoz.geojson           # GeoJSON original
│   │   └── ...
│   ├── geojson_divididos/                            # Carpeta con partes divididas
│   │   ├── parte_001.geojson
│   │   ├── parte_002.geojson
│   │   └── ...
│   ├── geojson_final/
│   │   ├── parte_001-direcciones.geojson             # GeoJSON con partes y direcciones
│   │   ├── potencial-solar-badajoz_completo.geojson
│   │   └── ...
├── potencial-solar-caceres/
│   ├── fuentes/
│   │   ├── potencial-solar-caceres.geojson           # GeoJSON original
│   │   └── ...
│   ├── geojson_divididos/                            # Carpeta con partes divididas
│   │   ├── parte_001.geojson
│   │   ├── parte_002.geojson
│   │   └── ...
│   ├── geojson_final/
│   │   ├── parte_001-direcciones.geojson             # GeoJSON con partes y direcciones
│   │   ├── potencial-solar-caceres_completo.geojson  # GeoJSON final unido
│   │   └── ...
├── scripts/
│   ├── dividir_geojson.py                            # Divide un GeoJSON grande en partes pequeñas
│   ├── unir_geojson.py                               # Une múltiples GeoJSON procesados en uno solo
│   ├── potencial-solar-badajoz-best.py               # Obtiene direcciones a partir de GeoJSON
│   └── ...
├── LICENSE
└── README.md
```

---

## 🔁 Flujo de trabajo recomendado

### 1️⃣ Dividir el GeoJSON original

Se utiliza cuando el archivo es demasiado grande para procesarlo de una sola vez.

```python
# dividir_geojson.py
dividir_geojson("datos_grandes.geojson", 10000, "parte")
```

Esto generará archivos como:

```text
parte_001.geojson
parte_002.geojson
parte_003.geojson
...
```

Cada archivo contiene un máximo de **10.000 features**.

---

### 2️⃣ Obtener direcciones (geocodificación inversa)

Para cada parte generada, se ejecuta el script de geocodificación:

```bash
python potencial-solar-badajoz-best.py parte_001.geojson
```

Este script:
- Calcula el centroide de cada polígono
- Obtiene la dirección usando **Nominatim (OpenStreetMap)**
- Añade la propiedad `direccion`
- Genera:
  - Un **GeoJSON con direcciones**
  - Un **CSV** con las columnas:

```text
geojson | Potencial | Direccion
```

⚠️ El script introduce pausas (`sleep`) para no saturar la API.

---

### 3️⃣ Repetir el proceso para todas las partes

```bash
python potencial-solar-badajoz-best.py parte_002.geojson
python potencial-solar-badajoz-best.py parte_003.geojson
...
```

Se recomienda automatizar este paso con un script o bash loop.

---

### 4️⃣ Unir todos los GeoJSON procesados

Una vez todas las partes han sido procesadas:

```python
# unir_geojson.py
unir_geojson("geojson_divididos/", "datos_completos.geojson")
```

El resultado es un **GeoJSON final completo**, con todas las direcciones incorporadas.

---

### 5️⃣ Limpiar Direcciones GeoJSON

Una vez todas las partes han sido procesadas:

```python
# limpiar_direcciones.py
python limpiar_direcciones.py
```

El resultado es un **GeoJSON final completo**, con todas las direcciones limpias.

**Ejemplos:**

```python
"81, Calle José María Giles Ontiveros, Pardaleras, Badajoz..."
"Calle José María Giles Ontiveros 81"

"Calle Dolores Marabe, Urbanización Guadiana, Badajoz..."
"Calle Dolores Marabe"

"Carretera de Talavera la Real a La Albuera, Alvarado..."
"Carretera de Talavera la Real a La Albuera"

"Calle San Marcial, El Gurugú, Badajoz..."
"Calle San Marcial"
```

### 6️⃣ Minimizar el GeoJSON

Una vez todas las partes han sido procesadas, minimizamos el josn para producción con JQ:

```python
jq.exe -c . potencial-solar-badajoz_completo_opt.geojson > potencial-solar-badajoz_completo_opt_min.json
```

## 🗺️ Compatibilidad

- Python 3.x (probado)
- Compatible con Python 2.7 (sin f-strings ni librerías modernas)
- Funciona con:
  - QGIS
  - PostGIS
  - Pandas
  - Excel (CSV)

---

## 📦 Dependencias

```bash
pip install geopy
```

Se utiliza:
- **Nominatim / OpenStreetMap** para geocodificación inversa

---

## 📊 Salida CSV

Cada CSV generado contiene exactamente:

```text
geojson, Potencial, Direccion
```

Ejemplo:

```csv
{"type":"Polygon","coordinates":[[[-6.7794,38.8142],...]]},2060.13,"Calle Mayor, Badajoz, España"
```

---

## ⚠️ Notas importantes

- Nominatim tiene **límites de uso** → no reducir el `sleep`
- Para grandes volúmenes se recomienda:
  - Cachear resultados
  - Usar un servicio propio de geocodificación
- Los scripts están pensados para **procesamiento batch**, no en tiempo real

---

## 🚀 Posibles mejoras futuras

- Exportación directa a **PostGIS**
- Cache de direcciones
- Paralelización controlada
- Normalización por calles / barrios
- Generación automática de estadísticas

---

## 👤 Autor

Desarrollado por **Antonio Horrillo Horrillo**.
<ahorrillo@hoy.es> | <tuanhorrillo@gmail.com> [GitHub](https://github.com/ahorrillo) | [LinkedIn](https://www.linkedin.com/in/antoniohh)

Proyecto creado y mantenido por Antonio Horrillo Horrillo, responsable de la arquitectura, desarrollo y diseño de Mapas.

---

## 📜 Licencia

- **Propiedad:** Grupo Vocento.
- **Licencia:** Privativa (uso interno).

Este proyecto es **software privativo** y propiedad del **Grupo Vocento**.
No está permitido su uso, copia, modificación o distribución sin autorización expresa de Vocento.

---
