# 🚀 SEDEAPP - Sistema de Datos de Gasolineras España

**Descarga automática de precios de gasolineras de España | Automated system to download official gas station data from Spain**

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Data Source](https://img.shields.io/badge/data-MITECO%20Official-orange.svg)](https://sedeaplicaciones.minetur.gob.es/)

## ¿Qué es SEDEAPP? | What is SEDEAPP?

**🇪🇸 ESPAÑOL:** SEDEAPP es una **aplicación gratuita** para descargar **precios históricos de combustibles** de todas las **gasolineras de España**. Obtén datos oficiales del **Ministerio MITECO** en formato Excel para análisis de precios de gasolina, gasóleo, y otros combustibles.

**🇬🇧 ENGLISH:** SEDEAPP is a **simple GUI application** that downloads official fuel price data from all gas stations in Spain using the Ministry's official API (MITECO). Get historical prices from any date and generate Excel files ready for analysis.

### ✨ Características Principales | Key Features

- 📊 **Datos históricos** - Precios de combustibles de cualquier fecha disponible
- 📍 **Todas las gasolineras** - Cobertura completa de España (Repsol, Cepsa, BP, etc.)
- 📁 **Archivos Excel** - Datos listos para análisis y estudios de mercado
- 🖥️ **Interfaz simple** - Solo introduce fechas y descarga automáticamente
- ⛽ **15+ combustibles** - Gasolina 95, Gasóleo A, GLP, GNC, Hidrógeno y más

### 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements_simple.txt

# Run the application
python sedeapp_simple.py
```

Enter a date (e.g., `13-05-2024`) or date range (e.g., `desde 01-01-2024 hasta 31-12-2024`) and click download!

## 📖 Documentation

- **🇪🇸 [Español - Guía Completa](README_ES.md)** - Instrucciones detalladas en español
- **🇬🇧 [English - Full Guide](README_EN.md)** - Detailed instructions in English

## 💡 Casos de Uso | Use Cases

- **Análisis de mercado** - Comparar precios de gasolina por regiones de España
- **Optimización de rutas** - Encontrar gasolineras más baratas para viajes
- **Estudios económicos** - Análisis de tendencias históricas de precios de combustibles
- **Aplicaciones móviles** - Integrar datos oficiales de gasolineras españolas
- **Investigación académica** - Datos del sector energético español

## 🔧 What's Included

- `sedeapp_simple.py` - Main GUI application
- `scrapy_carburantes_simple.py` - Data scraping engine  
- `requirements_simple.txt` - Python dependencies

## 📊 Fuente de Datos Oficial | Data Source

**Datos oficiales del MITECO** (Ministerio para la Transición Ecológica) - la misma fuente que usan las aplicaciones oficiales del gobierno español para precios de combustibles. Datos 100% oficiales y actualizados.

**Official data from MITECO** (Ministry for Ecological Transition) - the same source used by government and official fuel price apps in Spain.

## 📄 License / Licencia

This project is open source and available under the MIT License.
Este proyecto es código abierto y está disponible bajo la Licencia MIT.

---

*Created with AI assistance; [Cursor](https://cursor.sh/) running Claude-4-Sonnet*

