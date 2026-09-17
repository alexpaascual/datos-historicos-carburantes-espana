# SEDEAPP — Datos de precios de carburantes en España

Descarga precios históricos oficiales de todas las gasolineras de España en archivos Excel listos para usar.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)
[![Data Source](https://img.shields.io/badge/data-MITECO%20Oficial-orange.svg)](https://sedeaplicaciones.minetur.gob.es/)

*Read this in [English](../README.md).*

SEDEAPP es una pequeña aplicación de escritorio que obtiene los precios de carburantes de la API oficial del MITECO (Ministerio para la Transición Ecológica) — la misma fuente que usan las aplicaciones oficiales del Gobierno. Elige una fecha o un rango, selecciona los combustibles que te interesan y genera un Excel por día con precios, datos de la estación y coordenadas GPS.

## Inicio rápido

```bash
pip install -r requirements.txt
python sedeapp_simple.py
```

En la ventana que se abre, introduce una fecha suelta como `13-05-2024`, o un rango como `desde 01-01-2024 hasta 31-12-2024`. Marca los combustibles que quieras, elige opcionalmente una carpeta de destino y pulsa **Descargar**.

## Qué obtienes

Un `.xlsx` por día, con:

- **Precios** de los combustibles seleccionados
- **Ubicación** — dirección, municipio, provincia, código postal, coordenadas GPS
- **Datos de la estación** — rótulo, servicios
- **Fecha** a la que corresponden los datos

Las columnas con más de un 80% de valores vacíos, o que repiten el mismo valor en más del 90% de las filas, se eliminan automáticamente para que los archivos sean manejables.

### Combustibles disponibles

Gasolina 95 E5, Gasolina 95 E10, Gasolina 95 E5 Premium, Gasolina 98 E5, Gasolina 98 E10, Gasóleo A, Gasóleo B, Gasóleo Premium, Diésel Renovable, Biodiésel, Gases licuados del petróleo (GLP), Gas Natural Comprimido (GNC), Gas Natural Licuado (GNL), Hidrógeno y AdBlue.

Solo aparecen en el archivo los combustibles que tienen datos en la fecha elegida.

## Ejemplos de uso

- Comparar precios entre regiones o entre marcas
- Encontrar las gasolineras más baratas de una ruta
- Analizar tendencias históricas de precios para estudios económicos o académicos
- Alimentar un mapa o una app móvil con datos oficiales de estaciones

## Archivos del proyecto

| Archivo | Función |
|---|---|
| `sedeapp_simple.py` | Aplicación principal con interfaz — ejecuta este |
| `scrapy_carburantes_simple.py` | Spider de Scrapy que descarga y limpia los datos |
| `requirements.txt` | Dependencias de Python |

## Problemas comunes

| Problema | Solución |
|---|---|
| `ModuleNotFoundError` | Ejecuta `pip install -r requirements.txt` |
| No aparece la ventana | Tu instalación de Python no incluye Tkinter. En Debian/Ubuntu: `sudo apt install python3-tk` |
| `Error de conexión` | Revisa tu conexión y reintenta — la API del ministerio se cae de vez en cuando |
| No se generan Excels | El ministerio no tiene datos para esa fecha. Prueba con una más reciente |

## Información técnica

- **Fuente de datos**: API REST pública del MITECO (`EstacionesTerrestresHist`)
- **Formato de salida**: Excel `.xlsx`
- **Límite de peticiones**: las peticiones se limitan y reintentan automáticamente para hacer un uso responsable de una API pública. Cuenta con alrededor de medio minuto por cada día de datos.
- **Fechas disponibles**: cualquier fecha para la que el ministerio publique histórico

## Licencia

MIT — consulta [LICENSE](../LICENSE).

---

*Creado con asistencia de IA usando [Cursor](https://cursor.sh/).*
