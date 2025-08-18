import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import sys
import os
import re
from datetime import datetime, timedelta
import threading
from pathlib import Path

VERDE_OSCURO = '#204529'
VERDE_CLARO = '#7ED957'
FONDO = VERDE_OSCURO
TEXTO = 'white'

class SedeAppSimple(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SEDEApp Carburantes')
        self.configure(bg=FONDO)
        self.geometry('800x700')
        self.resizable(False, False)
        self.carpeta_destino = tk.StringVar()
        self.descarga_en_progreso = False
    
        self.combustibles_disponibles = [
            'Gasolina 95 E5', 'Gasoleo A', 'Gasoleo B', 'Gasoleo Premium', 'Gasolina 95 E10',
            'Gasolina 98 E5', 'Gasolina 98 E10', 'Gasolina 95 E5 Premium',
            'Biodiesel', 'Gases licuados del petróleo', 'Gas Natural Comprimido', 'Adblue', 
            'Hidrogeno', 'Gas Natural Licuado', 'Diésel Renovable'
        ]
        self.combustibles_vars = {}


        if not Path('scrapy_carburantes_simple.py').exists():
            messagebox.showerror(
                "Error", 
                "No se encuentra 'py_carburantes_simplescra.py'\n"
                "Este archivo es necesario para el funcionamiento."
            )
            self.destroy()
            return

        self.crear_widgets()

    def crear_widgets(self):
        fuente = ('Segoe UI', 11)
        fuente_bold = ('Segoe UI', 11, 'bold')
        
        titulo = tk.Label(self, text='SEDEApp Carburantes', 
                         bg=FONDO, fg=VERDE_CLARO, font=('Segoe UI', 13, 'bold'))
        titulo.pack(pady=(15, 10))

        instrucciones = tk.Label(
            self, 
            text='Introduce un día (dd-mm-aaaa) o un rango (desde dd-mm-aaaa hasta dd-mm-aaaa):',
            bg=FONDO, fg=TEXTO, font=fuente, wraplength=570, justify='center'
        )
        instrucciones.pack(pady=(0, 8))

        self.entry = tk.Entry(self, font=('Segoe UI', 12), width=50, fg='grey')
        self.entry.insert(0, 'Ejemplo: 13-05-2024 o desde 01-01-2024 hasta 31-12-2024')
        self.entry.bind('<FocusIn>', self.clear_placeholder)
        self.entry.bind('<FocusOut>', self.add_placeholder)
        self.entry.pack(pady=(0, 15))

        btn_carpeta = tk.Button(
            self, text='📁 Seleccionar carpeta destino', 
            command=self.seleccionar_carpeta, bg=VERDE_CLARO, 
            font=fuente_bold, relief='flat', padx=20, pady=8
        )
        btn_carpeta.pack(pady=(0, 5))

        self.label_carpeta = tk.Label(
            self, text='Ninguna carpeta seleccionada', 
            bg=FONDO, fg=TEXTO, font=('Segoe UI', 9)
        )
        self.label_carpeta.pack(pady=(0, 10))

        combustibles_frame = tk.LabelFrame(
            self, text='⛽ Combustibles', 
            bg=FONDO, fg=VERDE_CLARO, font=fuente_bold,
            padx=10, pady=8
        )
        combustibles_frame.pack(pady=(0, 15), padx=20, fill='x')
        
        explicacion_comb = tk.Label(
            combustibles_frame,
            text='ℹ️ Solo se incluirán combustibles que tengan datos en la fecha seleccionada\n(Combustibles con columnas vacías se omiten automáticamente)',
            bg=FONDO, fg='lightgray', font=('Segoe UI', 8),
            justify='center'
        )
        explicacion_comb.pack(pady=(0, 8))
        
        checkboxes_frame = tk.Frame(combustibles_frame, bg=FONDO)
        checkboxes_frame.pack()
        
        for i, combustible in enumerate(self.combustibles_disponibles):
            var = tk.BooleanVar()
            self.combustibles_vars[combustible] = var
            
            columna = i % 2
            fila = i // 2
            
            checkbox = tk.Checkbutton(
                checkboxes_frame, text=combustible, variable=var,
                bg=FONDO, fg=TEXTO, selectcolor=VERDE_OSCURO,
                activebackground=FONDO, activeforeground=VERDE_CLARO,
                font=('Segoe UI', 10)
            )
            checkbox.grid(row=fila, column=columna, sticky='w', padx=(0, 20), pady=2)
        
        botones_comb_frame = tk.Frame(combustibles_frame, bg=FONDO)
        botones_comb_frame.pack(pady=(8, 0))
        
        btn_limpiar_comb = tk.Button(
            botones_comb_frame, text='🔄 Limpiar todo', 
            command=self.limpiar_combustibles,
            bg='#555', fg='white', font=('Segoe UI', 9),
            relief='flat', padx=10, pady=4
        )
        btn_limpiar_comb.pack(side='left', padx=(0, 10))
        
        btn_seleccionar_comunes = tk.Button(
            botones_comb_frame, text='⛽ Básicos (95, Gasóleo A, etc.)', 
            command=self.seleccionar_combustibles_comunes,
            bg='#777', fg='white', font=('Segoe UI', 9),
            relief='flat', padx=10, pady=4
        )
        btn_seleccionar_comunes.pack(side='left')

        self.btn_descargar = tk.Button(
            self, text='⚡ Descargar', command=self.descargar, 
            bg=VERDE_CLARO, font=fuente_bold, relief='flat', 
            padx=25, pady=10
        )
        self.btn_descargar.pack(pady=(0, 10))

        self.progreso = tk.Label(self, text='', bg=FONDO, fg=VERDE_CLARO, font=fuente)
        self.progreso.pack(pady=(0, 3))
        
        self.progreso_detalle = tk.Label(self, text='', bg=FONDO, fg='lightgray', font=('Segoe UI', 9))
        self.progreso_detalle.pack(pady=(0, 3))

    def clear_placeholder(self, event):
        if self.entry.get().startswith('Ejemplo:'):
            self.entry.delete(0, tk.END)
            self.entry.config(fg='black')

    def add_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, 'Ejemplo: 13-05-2024 o desde 01-01-2024 hasta 31-12-2024')
            self.entry.config(fg='grey')

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title='Selecciona la carpeta de destino')
        if carpeta:
            self.carpeta_destino.set(carpeta)
            display_path = carpeta
            if len(display_path) > 60:
                display_path = "..." + display_path[-57:]
            self.label_carpeta.config(text=display_path)
        else:
            self.label_carpeta.config(text='Ninguna carpeta seleccionada')

    def descargar(self):
        if self.descarga_en_progreso:
            self.progreso.config(text='⚠️ Ya hay una descarga en progreso', fg='orange')
            return

        entrada = self.entry.get().strip()
        if entrada == '' or entrada.startswith('Ejemplo:'):
            self.progreso.config(text='⚠️ Por favor, introduce una fecha o rango de fechas', fg='orange')
            return

        fechas_resultado = self.procesar_fechas(entrada)
        if not fechas_resultado:
            return

        fecha_inicio, fecha_fin, total_dias = fechas_resultado

        if total_dias > 31:
            resultado = messagebox.askyesno(
                "Confirmación", 
                f"Vas a descargar {total_dias} días de datos.\n"
                f"Tiempo estimado: {total_dias//2} minutos.\n"
                f"¿Continuar?"
            )
            if not resultado:
                return

        self.descarga_en_progreso = True
        self.btn_descargar.config(state='disabled', text='Descargando...')
        

        
        thread = threading.Thread(target=self.ejecutar_scrapy, args=(fecha_inicio, fecha_fin, total_dias))
        thread.daemon = True
        thread.start()

    def procesar_fechas(self, entrada):
        """Validar fechas de entrada"""
        regex_dia = r'^(\d{2}-\d{2}-\d{4})$'
        regex_rango = r'^desde (\d{2}-\d{2}-\d{4}) hasta (\d{2}-\d{2}-\d{4})$'

        match_dia = re.match(regex_dia, entrada)
        match_rango = re.match(regex_rango, entrada, re.IGNORECASE)

        if match_dia:
            fecha = match_dia.group(1)
            if not self.fecha_valida(fecha):
                self.progreso.config(text=f'❌ La fecha {fecha} no es válida', fg='red')
                return None
            return fecha, fecha, 1

        elif match_rango:
            fecha_inicio = match_rango.group(1)
            fecha_fin = match_rango.group(2)
            
            if not self.fecha_valida(fecha_inicio):
                self.progreso.config(text=f'❌ Fecha de inicio {fecha_inicio} no válida', fg='red')
                return None
            
            if not self.fecha_valida(fecha_fin):
                self.progreso.config(text=f'❌ Fecha de fin {fecha_fin} no válida', fg='red')
                return None
            
            d_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y')
            d_fin = datetime.strptime(fecha_fin, '%d-%m-%Y')
            
            if d_inicio > d_fin:
                self.progreso.config(text='❌ La fecha de inicio debe ser anterior a la de fin', fg='red')
                return None
            
            total_dias = (d_fin - d_inicio).days + 1
            return fecha_inicio, fecha_fin, total_dias

        else:
            self.progreso.config(text='❌ Formato no válido. Usa: dd-mm-aaaa o "desde dd-mm-aaaa hasta dd-mm-aaaa"', fg='red')
            return None

    def limpiar_combustibles(self):
        """Limpiar todas las selecciones de combustibles"""
        for var in self.combustibles_vars.values():
            var.set(False)
    
    def seleccionar_combustibles_comunes(self):
        """Seleccionar combustibles básicos/comunes"""
        combustibles_basicos = [
            'Gasolina 95 E5', 'Gasoleo A', 'Gasoleo B', 'Gasoleo Premium', 'Gasolina 95 E10',
            'Gasolina 98 E5', 'Gasolina 95 E5 Premium'
        ]
        for combustible, var in self.combustibles_vars.items():
            var.set(combustible in combustibles_basicos)

    def obtener_combustibles_seleccionados(self):
        """Obtener lista de combustibles adicionales seleccionados"""
        seleccionados = []
        for combustible, var in self.combustibles_vars.items():
            if var.get():
                seleccionados.append(combustible)
        return seleccionados

    def ejecutar_scrapy(self, fecha_inicio, fecha_fin, total_dias):
        """Ejecutar el script de Scrapy robusto que funciona"""
        try:
            combustibles_extra = self.obtener_combustibles_seleccionados()
            
            self.after(0, lambda: self.progreso.config(text=f'🚀 Iniciando descarga de {total_dias} archivo(s)...', fg='yellow'))
            self.after(0, lambda: self.progreso_detalle.config(text='', fg='lightgray'))
        
            cmd = [
                'python', '-m', 'scrapy', 'runspider', 'scrapy_carburantes_simple.py',
                '-a', f'fecha_inicio={fecha_inicio}',
                '-a', f'fecha_fin={fecha_fin}',
                '--loglevel=INFO'
            ]
            
            if combustibles_extra:
                combustibles_str = ','.join(combustibles_extra)
                cmd.extend(['-a', f'combustibles_extra={combustibles_str}'])

            self.after(0, lambda: self.progreso.config(text='', fg='yellow'))
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())

            if result.returncode == 0:
                fecha_str = f'{datetime.strptime(fecha_inicio, "%d-%m-%Y").strftime("%Y%m%d")}_{datetime.strptime(fecha_fin, "%d-%m-%Y").strftime("%Y%m%d")}'
                carpeta_scrapy = f'carburantes_scrapy_{fecha_str}'
                
                if os.path.exists(carpeta_scrapy):
                    archivos_excel = [f for f in os.listdir(carpeta_scrapy) if f.endswith('.xlsx')]
                    
                    if archivos_excel:
                        # Mover archivos si se seleccionó carpeta destino
                        carpeta_destino = self.carpeta_destino.get()
                        if carpeta_destino:
                            try:
                                # Formato correcto: dd-mm-aaaa_a_dd-mm-aaaa
                                if total_dias == 1:
                                    subcarpeta = f'SEDEApp_Carburantes_{fecha_inicio}'
                                else:
                                    subcarpeta = f'SEDEApp_Carburantes_{fecha_inicio}_a_{fecha_fin}'
                                
                                ruta_final = os.path.join(carpeta_destino, subcarpeta)
                                os.makedirs(ruta_final, exist_ok=True)
                                
                                # Progreso al empezar a mover archivos
                                self.after(0, lambda: self.progreso.config(text=f'📁 Organizando {len(archivos_excel)} archivos...', fg='yellow'))
                                # Mantener línea de detalle oculta durante organización
                                
                                archivos_movidos = 0
                                for i, archivo in enumerate(archivos_excel, 1):
                                    origen = os.path.join(carpeta_scrapy, archivo)
                                    destino = os.path.join(ruta_final, archivo)
                                    

                                    
                                    # Verificar que el archivo origen existe
                                    if os.path.exists(origen):
                                        # Si ya existe en destino, eliminarlo
                                        if os.path.exists(destino):
                                            os.remove(destino)
                                        # Mover archivo
                                        os.rename(origen, destino)
                                        archivos_movidos += 1
                                
                                # Limpiar carpeta temporal de Scrapy
                                try:
                                    if os.path.exists(carpeta_scrapy):
                                        import shutil
                                        shutil.rmtree(carpeta_scrapy)
                                except:
                                    pass
                                
                                self.after(0, lambda: self.progreso.config(text=f'🎉 ¡Completado! {archivos_movidos} archivos Excel', fg='green'))
                                self.after(0, lambda: self.progreso_detalle.config(text=f'📁 Archivos guardados en: {ruta_final}', fg='white'))
                            except Exception as e:
                                error_detalle = str(e)
                                self.after(0, lambda: self.progreso.config(text='⚠️ Error moviendo archivos', fg='orange'))
                                self.after(0, lambda: self.progreso_detalle.config(text=f'Error: {error_detalle[:50]}. Archivos en: {carpeta_scrapy}', fg='orange'))
                        else:
                            self.after(0, lambda: self.progreso.config(text=f'🎉 ¡Completado! {len(archivos_excel)} archivos Excel', fg='green'))
                            self.after(0, lambda: self.progreso_detalle.config(text=f'📁 Archivos en: {carpeta_scrapy}', fg='white'))
                    else:
                        self.after(0, lambda: self.progreso.config(text='⚠️ No se generaron archivos Excel', fg='orange'))
                        self.after(0, lambda: self.progreso_detalle.config(text='Verifica las fechas e intenta de nuevo', fg='orange'))
                else:
                    self.after(0, lambda: self.progreso.config(text='⚠️ No se encontró carpeta de resultados', fg='orange'))
                    self.after(0, lambda: self.progreso_detalle.config(text='Scrapy ejecutó pero no generó la carpeta esperada', fg='orange'))
            else:
                error_msg = result.stderr[:200] if result.stderr else 'Error desconocido'
                self.after(0, lambda: self.progreso.config(text='❌ Error en Scrapy', fg='red'))
                self.after(0, lambda: self.progreso_detalle.config(text=f'Error: {error_msg[:80]}... Verifica instalación de Scrapy', fg='red'))

        except Exception as e:
            self.after(0, lambda: self.progreso.config(text='❌ Error inesperado', fg='red'))
            self.after(0, lambda: self.progreso_detalle.config(text=str(e)[:100], fg='red'))
            
        finally:
            self.after(0, lambda: self.btn_descargar.config(state='normal', text='⚡ Descargar'))
            self.after(0, lambda: setattr(self, 'descarga_en_progreso', False))
            self.after(30000, lambda: self.progreso_detalle.config(text=''))

    def fecha_valida(self, fecha_str):
        try:
            datetime.strptime(fecha_str, '%d-%m-%Y')
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    app = SedeAppSimple()
    app.mainloop() 