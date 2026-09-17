# SEDEAPP — Spanish Fuel Price Data

Download official historical fuel prices for every gas station in Spain as ready-to-use Excel files.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Data Source](https://img.shields.io/badge/data-MITECO%20Official-orange.svg)](https://sedeaplicaciones.minetur.gob.es/)

*Léeme en [español](docs/README.es.md).*

SEDEAPP is a small desktop app that pulls fuel price data from the official API of Spain's Ministry for Ecological Transition (MITECO) — the same source behind the government's own fuel price apps. Pick a date or a date range, choose which fuels you care about, and it writes one Excel file per day with prices, station details, and GPS coordinates.

## Quick start

```bash
pip install -r requirements.txt
python sedeapp_simple.py
```

In the window that opens, enter a single date as `13-05-2024`, or a range as `desde 01-01-2024 hasta 31-12-2024`. Tick the fuels you want, optionally pick a destination folder, and click **Descargar**.

## What you get

One `.xlsx` per day, containing:

- **Prices** for the fuels you selected
- **Location** — address, municipality, province, postal code, GPS coordinates
- **Station details** — brand, services
- **Date** the data refers to

Columns that are more than 80% empty, or that hold the same value in more than 90% of rows, are dropped automatically to keep the files readable.

### Available fuels

Gasolina 95 E5, Gasolina 95 E10, Gasolina 95 E5 Premium, Gasolina 98 E5, Gasolina 98 E10, Gasóleo A, Gasóleo B, Gasóleo Premium, Diésel Renovable, Biodiesel, Gases licuados del petróleo (GLP), Gas Natural Comprimido (GNC), Gas Natural Licuado (GNL), Hidrógeno, and AdBlue.

Only fuels that actually have data on the chosen date end up in the file.

## Use cases

- Compare prices across regions or between brands
- Find the cheapest stations along a route
- Study historical price trends for economics or academic research
- Feed official station data into a map or mobile app

## Project files

| File | Purpose |
|---|---|
| `sedeapp_simple.py` | Main GUI application — run this one |
| `scrapy_carburantes_simple.py` | Scrapy spider that fetches and cleans the data |
| `requirements.txt` | Python dependencies |

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Window doesn't appear | Your Python build is missing Tkinter. On Debian/Ubuntu: `sudo apt install python3-tk` |
| `Connection error` | Check your internet connection and retry — the ministry's API is occasionally down |
| No Excel files generated | The ministry has no data for that date. Try a more recent one |

## Technical notes

- **Data source**: MITECO public REST API (`EstacionesTerrestresHist`)
- **Output format**: Excel `.xlsx`
- **Rate limiting**: requests are throttled and retried automatically to stay well within polite use of a public API. Expect roughly half a minute per day of data.
- **Date coverage**: any date for which the ministry publishes historical data

## License

MIT — see [LICENSE](LICENSE).

---

*Built with AI assistance using [Cursor](https://cursor.sh/).*
