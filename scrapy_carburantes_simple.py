import scrapy
from datetime import datetime, timedelta
import json
import pandas as pd
import os
import re
import numpy as np

class CarburantesSpider(scrapy.Spider):
    name = 'carburantes_historicos'
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 4,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 2,
        'AUTOTHROTTLE_MAX_DELAY': 8,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.5,
        'AUTOTHROTTLE_DEBUG': True,
        
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429, 403],
        
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'User-Agent': 'CarburantesBot 1.0 (Legal API Access)',
            'Connection': 'keep-alive',
        },
        
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'TELNETCONSOLE_ENABLED': False,
    }
    
    def __init__(self, fecha_inicio=None, fecha_fin=None, combustibles_extra=None, *args, **kwargs):
        super(CarburantesSpider, self).__init__(*args, **kwargs)
        
        if fecha_inicio:
            self.fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y')
        else:
            self.fecha_inicio = datetime.now() - timedelta(days=30)
            
        if fecha_fin:
            self.fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y')
        else:
            self.fecha_fin = datetime.now()
            
        self.combustibles_extra = []
        if combustibles_extra:
            self.combustibles_extra = combustibles_extra.split(',')
            self.logger.info(f'🔥 Combustibles extra a conservar: {self.combustibles_extra}')
            
        self.fechas = []
        fecha_actual = self.fecha_inicio
        while fecha_actual <= self.fecha_fin:
            self.fechas.append(fecha_actual.strftime('%d-%m-%Y'))
            fecha_actual += timedelta(days=1)
            
        self.logger.info(f'🎯 Preparado para procesar {len(self.fechas)} fechas')
        self.logger.info(f'📅 Desde: {self.fecha_inicio.strftime("%d-%m-%Y")}')
        self.logger.info(f'📅 Hasta: {self.fecha_fin.strftime("%d-%m-%Y")}')
        
        fecha_str = f'{self.fecha_inicio.strftime("%Y%m%d")}_{self.fecha_fin.strftime("%Y%m%d")}'
        self.output_dir = f'carburantes_scrapy_{fecha_str}'
        os.makedirs(self.output_dir, exist_ok=True)
        self.logger.info(f'📁 Archivos se guardarán en: {self.output_dir}')
        
    def start_requests(self):
        """Generar todas las peticiones iniciales"""
        base_url = 'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestresHist'
        
        for fecha in self.fechas:
            url = f'{base_url}/{fecha}'
            yield scrapy.Request(
                url=url,
                callback=self.parse_datos,
                meta={'fecha': fecha},
                dont_filter=True,
            )
    
    def parse_datos(self, response):
        """Procesar la respuesta JSON de cada fecha"""
        fecha = response.meta['fecha']
        
        if response.status == 200:
            try:
                data = json.loads(response.text)
                
                if 'ListaEESSPrecio' in data and data['ListaEESSPrecio']:
                    df = pd.DataFrame(data['ListaEESSPrecio'])
                    
                    df['FechaConsulta'] = fecha
                    df['FechaDescarga'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    df = self.limpiar_datos(df)
                    
                    nombre_archivo = f'precios_{fecha.replace("-", "_")}.xlsx'
                    ruta_archivo = os.path.join(self.output_dir, nombre_archivo)
                    df.to_excel(ruta_archivo, index=False, engine='openpyxl')
                    
                    self.logger.info(f'✅ {fecha}: {len(df)} estaciones → {nombre_archivo}')

                    yield {
                        'fecha': fecha,
                        'estaciones': len(df),
                        'status': 'success',
                        'archivo': nombre_archivo,
                        'tamaño_kb': round(os.path.getsize(ruta_archivo) / 1024, 1)
                    }
                else:
                    self.logger.warning(f'⚠️  {fecha}: Sin datos en la respuesta')
                    yield {
                        'fecha': fecha,
                        'estaciones': 0,
                        'status': 'no_data',
                        'archivo': None
                    }
                    
            except json.JSONDecodeError as e:
                self.logger.error(f'❌ {fecha}: Error JSON - {str(e)[:100]}')
                yield {
                    'fecha': fecha,
                    'status': 'json_error',
                    'error': str(e)[:200]
                }
                
            except Exception as e:
                self.logger.error(f'💥 {fecha}: Error inesperado - {str(e)[:100]}')
                yield {
                    'fecha': fecha,
                    'status': 'error',
                    'error': str(e)[:200]
                }
        else:
            self.logger.error(f'🚨 {fecha}: HTTP {response.status}')
            yield {
                'fecha': fecha,
                'status': f'http_{response.status}',
                'error': response.text[:200] if response.text else 'Sin contenido'
            }
    
    def limpiar_datos(self, df):
        """Limpieza de datos optimizada con preservación de combustibles seleccionados"""
        if df.empty:
            return df
            
        regex_lat = re.compile(r'latitud', re.IGNORECASE)
        regex_lon = re.compile(r'longitud', re.IGNORECASE)
        lat_cols = [col for col in df.columns if regex_lat.search(col)]
        lon_cols = [col for col in df.columns if regex_lon.search(col)]
        
        for col in lat_cols + lon_cols:
            if col in df.columns:
                serie = df[col].replace(['#####', ''], np.nan)
                serie = serie.astype(str).str.strip().str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(serie, errors='coerce')
        
        columnas_combustibles = [col for col in df.columns if col.startswith('Precio ')]
        
        combustibles_usuario = []
        if self.combustibles_extra:
            for combustible_usuario in self.combustibles_extra:
                matches = []
                for col in columnas_combustibles:
                    nombre_combustible = col.replace('Precio ', '')
                    if combustible_usuario.strip().lower() == nombre_combustible.strip().lower():
                        matches.append(col)
                combustibles_usuario.extend(matches)
        
        cols_fundamentales = ['IDEESS', 'Rótulo', 'Dirección', 'C.P.', 'Localidad', 'Municipio', 'Provincia']
        cols_importantes = (lat_cols + lon_cols + cols_fundamentales + combustibles_usuario)
        
        combustibles_no_seleccionados = [col for col in columnas_combustibles if col not in combustibles_usuario]
        columnas_eliminadas = []
        
        for col in combustibles_no_seleccionados:
            df = df.drop(columns=[col])
            columnas_eliminadas.append(f"{col} (combustible no seleccionado)")
        
        def es_vacio(x):
            return pd.isna(x) or x == '' or x == '#####'
        
        for col in list(df.columns):
            if col not in cols_importantes:
                vacios = df[col].apply(es_vacio).sum()
                if vacios / len(df) > 0.8:
                    df = df.drop(columns=[col])
                    columnas_eliminadas.append(f"{col} (>80% vacíos)")
                    continue
                    
                valores = df[col].astype(str).str.replace(',', '.').str.strip()
                if len(valores.mode()) > 0:
                    valor_frecuente = valores.mode()[0]
                    frecuencia = (valores == valor_frecuente).sum() / len(df)
                    if frecuencia > 0.9:
                        df = df.drop(columns=[col])
                        columnas_eliminadas.append(f"{col} (>90% mismo valor)")
        
        self.logger.info(f'🔥 Total combustibles disponibles: {len(columnas_combustibles)}')
        self.logger.info(f'❌ Combustibles eliminados: {len(combustibles_no_seleccionados)}')
        if combustibles_usuario:
            self.logger.info(f'⭐ Combustibles preservados: {combustibles_usuario}')
        else:
            self.logger.info(f'⚠️ NINGÚN combustible seleccionado - Excel sin precios')
        self.logger.info(f'🗑️ Total columnas eliminadas: {len(columnas_eliminadas)}')
        
        if 'C.P.' in df.columns:
            df['C.P.'] = df['C.P.'].astype(str).apply(
                lambda x: f"'{x.zfill(5)}" if x.isdigit() else f"'{x}"
            )
        
        if 'Localidad' in df.columns:
            df = df.sort_values('Localidad', na_position='last')
        
        return df

