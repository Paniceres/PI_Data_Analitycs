import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image

import sys
print(sys.executable)

from data_loader import DataLoader
from funcs import calcular_provincias_criterio, plot_correlacion_hogar_hab, plot_criterio_provincia, plot_tasa_crecimiento_penetracion_criterio, plot_correlacion_ingresos_dolar, plot_dolares_ingresos_tasaIngresos, plot_dolares_ingresos_tasaPenetracion, plot_correlacion_tasaIngresos_tasaPenetracion, plot_promedio_velocidad, matriz_correlacion_velocidad, plot_tendencia_tecnologia, plot_correlacion_tecnologia_velocidad

from pages.context import show as Contexto
from pages.criterio import show as Criterio
from pages.penetracion import show as Penetracion
from pages.tecnologia import show as Tecnologia
from pages.kpi_obligatorio import show as KPI_obligatorio

# Crear una instancia de la clase DataViz
data_load = DataLoader(data_directory='./data/readytogo')
data_load.load_data()

# Acceder a los DataFrames cargados
df_penetracion = data_load.dataframes['penetracion']
df_penetracion_ingresos = data_load.dataframes['penetracion_ingresos']
df_tecnologia_velocidad = data_load.dataframes['tecnologia_velocidad']
df_kpi = data_load.dataframes['kpi']

# Filtrar provincias con tasa de Penetracion > 60% en 2022
provincias_criterio = calcular_provincias_criterio(df_kpi)

# -------------- logo
# Obtener la ruta al directorio actual (donde se encuentra main.py)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta a la imagen usando os.path.join
static_directory = os.path.join(current_directory, 'static')
logo_path = os.path.join(static_directory, 'ENACOM_logo.png')

# Abrir la imagen
try:
    logo = Image.open(logo_path)
except FileNotFoundError:
    print(f"Error: No se pudo encontrar la imagen en la ruta: {logo_path}")
# -------------- logo

# Interactividad con Streamlit
st.title('Proyecto: Análisis de ENACOM: Calidad y Penetración de servicio en torno a tecnologías.')

pagina_seleccionada = st.sidebar.radio('Selecciona una página:',
                                       ['Contexto', 'Criterio', 'Penetración', 'Tecnología', 'KPI Obligatorio'])



if pagina_seleccionada == 'Contexto':
    Contexto(df_penetracion, df_kpi)
elif pagina_seleccionada == 'Criterio':
    Criterio(df_kpi, provincias_criterio)
elif pagina_seleccionada == 'Penetración':
    Penetracion(df_kpi, provincias_criterio)  
elif pagina_seleccionada == 'Tecnología':
    Tecnologia(df_kpi, provincias_criterio)  
elif pagina_seleccionada == 'KPI Obligatorio':
    KPI_obligatorio(df_kpi, provincias_criterio)


    