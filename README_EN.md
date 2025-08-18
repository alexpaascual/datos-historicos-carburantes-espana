# 🚀 SEDEAPP - Gas Station Data System

**Automated system to download official gas station data from Spain**

## What does it do?

- 📊 **Downloads historical prices** from any date
- 📍 **Gets locations** of all gas stations  
- 📁 **Generates Excel files** ready to use
- 🖥️ **Simple interface** - just enter the date and go

## 🚀 How to use

### 1. Install (first time only)
```bash
pip3 install -r requirements_simple.txt
```

### 2. Run
```bash
python3 sedeapp_simple.py
```

### 3. Use the interface
- **Enter a date**: `13-05-2024`
- **Or a range**: `desde(from) 01-01-2024 (hasta)to 31-12-2024`  
- **Click "Download"**
- **Done!** A folder is generated in the selected destination with the Excel file(s)

## 📊 What you get

**Excel file** with information from all gas stations:
- **Prices** of fuels (selected ones)
- **Location** (address, GPS coordinates)
- **Station information** (brand, services)
- **Date** of the data

### ⛽ **Included fuels:**
- **Available**: 15+ fuels including Gasoline 95 E5, Diesel A, Biodiesel, LPG, CNG, Hydrogen, etc.

## 📁 Project files

- `sedeapp_simple.py` - Main interface (run this one)
- `scrapy_carburantes_simple.py` - Download engine 
- `requirements_simple.txt` - Required dependencies

## 💡 Use cases

- **Price analysis** - Compare gas stations in your area
- **Market studies** - Analyze price trends
- **Map apps** - Show gas stations on a map
- **Optimized routes** - Find the cheapest gas stations on your route

## ⚠️ Common issues

| Problem | Solution |
|---------|----------|
| `Connection error` | Check internet and retry |
| `ModuleNotFoundError` | Run `pip3 install -r requirements_simple.txt` or `pip install -r requirements_simple.txt` |
| `Window doesn't appear` | Verify Python installation with Tkinter |


## ℹ️ Technical information

- **Data source**: Official Ministry API (MITECO)
- **Available dates**: Any date with available historical data
- **Limits**: No specific limits, depends on official data availability
- **Output format**: Optimized Excel (.xlsx)

---
