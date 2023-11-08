import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image

from data_loader import DataLoader
from funcs import calcular_provincias_criterio, plot_correlacion_hogar_hab, plot_criterio_provincia, plot_tasa_crecimiento_penetracion_criterio, plot_correlacion_ingresos_dolar, plot_dolares_ingresos_tasaIngresos, plot_dolares_ingresos_tasaPenetracion, plot_correlacion_tasaIngresos_tasaPenetracion, plot_promedio_velocidad, matriz_correlacion_velocidad, plot_tendencia_tecnologia, plot_correlacion_tecnologia_velocidad

from pages.context import show as Contexto
from pages.criterio import show as Criterio
from pages.penetracion import show as Penetracion
from pages.tecnologia import show as Tecnologia

# Crear una instancia de la clase DataViz
data_load = DataLoader(data_directory='../data/readytogo')
data_load.load_data()

# Acceder a los DataFrames cargados
df_penetracion = data_load.dataframes['penetracion']
df_penetracion_ingresos = data_load.dataframes['penetracion_ingresos']
df_tecnologia_velocidad = data_load.dataframes['tecnologia_velocidad']
df_kpi = data_load.dataframes['kpi']

# Filtrar provincias con tasa de Penetracion > 60% en 2022
provincias_criterio = calcular_provincias_criterio(df_kpi)

# Cargar el logo desde el archivo
logo_path = '/home/p/Code/Henry/PI_DA/deploy/static/ENACOM_logo.png'
logo = Image.open(logo_path)

# Mostrar el logo en Streamlit
st.sidebar.image(logo, width=300)


# Interactividad con Streamlit
st.title('Proyecto: Análisis de ENACOM y su calidad y penetración de servicio')

pagina_seleccionada = st.sidebar.radio('Selecciona una página:',
                                       ['Contexto', 'Criterio', 'Penetración', 'Tecnología'])



if pagina_seleccionada == 'Contexto':
    Contexto(df_penetracion, df_kpi)
elif pagina_seleccionada == 'Criterio':
    Criterio(df_kpi, provincias_criterio)
elif pagina_seleccionada == 'Penetración':
    Penetracion(df_kpi)  
elif pagina_seleccionada == 'Tecnología':
    Tecnologia(df_kpi, provincias_criterio)  


    