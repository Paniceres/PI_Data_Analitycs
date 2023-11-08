import streamlit as st
from funcs import (
    plot_criterio_provincia,
    plot_tasa_crecimiento_penetracion_criterio,
    plot_correlacion_ingresos_dolar,
    plot_dolares_ingresos_tasaIngresos,
    plot_dolares_ingresos_tasaPenetracion,
    calcular_provincias_criterio
)
from data_loader import DataLoader

# Crear una instancia de la clase DataLoader
data_load = DataLoader(data_directory='./data/readytogo')
data_load.load_data()
df_kpi = data_load.dataframes['kpi']

# Filtrar provincias con tasa de Penetracion > 60% en 2022
provincias_criterio = calcular_provincias_criterio(df_kpi)

def show(df_kpi, provincias_criterio):
    provincias_criterio = calcular_provincias_criterio(df_kpi)
    st.sidebar.title("Criterio")
    st.title("Comprender el Criterio de Análisis")
    st.write('''
             Con el propósito de conformar un criterio de análisis, discriminando para obtener una muestra en la cual priorizar esfuerzos, 
             hemos cuestionado la tasa de accesibilidad del servicio para el total de provincias en el año 2022.
             ''')
    
    st.header("Promedio de Accesos por cada 100 hogares por Provincia en 2022")
    plot_criterio_provincia(df_kpi)
    st.write("""
    En este gráfico, se muestra el promedio de accesos por cada 100 hogares por provincia en el año 2022. 
    Se identifican las provincias que tienen un promedio de acceso por debajo del 60%, marcadas por la línea roja.
    """)
    
    st.header("Tasa de Crecimiento Promedio de Penetración por Año para Provincias con Acceso < 60% en 2022")
    imagen = plot_tasa_crecimiento_penetracion_criterio(df_kpi, provincias_criterio)
    st.image(imagen, caption='Tasa de Crecimiento Promedio de Penetración', use_column_width=True)
    st.write("""
    En este gráfico, se muestra la tendencia de la tasa de crecimiento promedio de penetración por año 
    para las provincias con acceso por debajo del 60%. Se observa una tendencia alcista con cierta volatilidad en el corto plazo.
    """)
    
    # st.write("""
    # Surje la necesidad de contrastar los datos con alguna métrica de interés, como lo son los ingresos a la compañía, 
    # debido a la relevancia del valor del dólar en torno a la actividad económica en el país.
    # """)
    
    # st.header("3. Comparación entre Promedio de Ingresos y Valor del Dólar (Dólar Blue)")
    # imagen_correlacion_ingresos_dolar = plot_correlacion_ingresos_dolar(df_kpi)
    # st.image(imagen_correlacion_ingresos_dolar, caption='Comparación entre Promedio de Ingresos y Valor del Dólar (Dólar Blue)', use_column_width=True)
    # st.write("""
    # Este gráfico muestra la comparación entre el promedio de ingresos en miles de pesos y el valor del dólar 
    # valor del dólar en pesos argentinos. Se observa tanto una gran tendencia alcista en ambos, como una alta correlaciaón de datos.
    # """)
    
    # st.write("""
    # Se toma la decisión de convertir los ingresos a dólares, para analizar la relación entre los ingresos y el valor del dólar en pesos argentinos.
    # """)
    
    # st.header("4. Comparación entre Ingresos en Dólares y Tasa de Crecimiento de Ingresos")
    # img_bytes = plot_dolares_ingresos_tasaIngresos(df_kpi)
    # st.image(img_bytes, use_column_width=True)
    # st.write('''
    # Observamos una estabilidad a largo plazo en torno a una ingesta de 500.000usd. Corroboraremos la correlación entre la ingesta 
    # promedio en dólares contra la tasa de crecimiento de penetración, promedio nacional.
    # ''')
    
    # st.header("5. Comparación entre Ingresos en Dólares y Tasa de Crecimiento de Penetración")
    # img_bytes = plot_dolares_ingresos_tasaPenetracion(df_kpi)
    # st.image(img_bytes, use_column_width=True)
    # st.write("""
    # Este gráfico compara el promedio de ingresos en miles de dólares con la tasa de crecimiento promedio de ingresos. 
    # Se analiza la correlación entre estos factores para entender mejor la estabilidad de la ingesta neta en relación con la tasa de crecimiento.
    # """)