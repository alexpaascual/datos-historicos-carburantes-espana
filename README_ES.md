# 🚀 SEDEAPP - Sistema de Datos de Gasolineras

**Sistema automatizado para descargar datos oficiales de gasolineras de España**

## ¿Qué hace?

- 📊 **Descarga precios históricos** de cualquier fecha
- 📍 **Obtiene ubicaciones** de todas las gasolineras  
- 📁 **Genera archivos Excel** listos para usar
- 🖥️ **Interfaz simple** - solo introduce la fecha y listo

## 🚀 Cómo usarlo

### 1. Instalar (solo la primera vez)
```bash
pip3 install -r requirements_simple.txt
```

### 2. Ejecutar
```bash
python3 sedeapp_simple.py
```

### 3. Usar la interfaz
- **Introduce una fecha**: `13-05-2024`
- **O un rango**: `desde 01-01-2024 hasta 31-12-2024`  
- **Clic en "Descargar"**
- **¡Listo!** Se genera una carpeta en el destino selecionado con el/los Excels 

## 📊 Qué obtienes

**Archivo Excel** con información de todas las gasolineras:
- **Precios** de combustibles (los seleccionados)
- **Ubicación** (dirección, coordenadas GPS)
- **Información** de la estación (marca, servicios)
- **Fecha** de los datos

### ⛽ **Combustibles incluidos:**
- **Disponibles**: 15+ combustibles incluyendo Gasolina 95 E5, Gasóleo A, Biodiesel, GLP, GNC, Hidrógeno, etc.

## 📁 Archivos del proyecto

- `sedeapp_simple.py` - Interfaz principal (ejecutar este)
- `scrapy_carburantes_simple.py` - Motor de descarga 
- `requirements_simple.txt` - Dependencias necesarias

## 💡 Ejemplos de uso

- **Análisis de precios** - Comparar gasolineras de tu zona
- **Estudios de mercado** - Analizar tendencias de precios
- **Apps de mapas** - Mostrar gasolineras en un mapa
- **Rutas optimizadas** - Encontrar las gasolineras más baratas en tu ruta


## ⚠️ Problemas comunes

| Problema | Solución |
|----------|----------|
| `Error de conexión` | Revisar internet y reintentar |
| `ModuleNotFoundError` | Ejecutar `pip3 install -r requirements_simple.txt` 
o `pip install -r requirements_simple.txt`  |
| `No aparece la ventana` | Verificar instalación de Python con Tkinter |
| `Aparecen combustibles no seleccionados` | Ejecutar `python3 test_rapido.py` 
o `python test_rapido.py` para verificar |

## ℹ️ Información técnica

- **Fuente de datos**: API oficial del Ministerio (MITECO)
- **Fechas disponibles**: Cualquier fecha con datos históricos disponibles
- **Límites**: Sin límites específicos, depende de disponibilidad de datos oficiales
- **Formato de salida**: Excel (.xlsx) optimizado

---
