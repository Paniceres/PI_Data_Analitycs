import streamlit as st
from funcs import calcular_provincias_criterio, plot_correlacion_hogar_hab, plot_correlacion_ingresos_dolar

from data_loader import DataLoader

# Crear una instancia de la clase DataLoader
data_load = DataLoader(data_directory='../../data/readytogo')
data_load.load_data()
df_kpi = data_load.dataframes['kpi']
df_penetracion = data_load.dataframes['penetracion']

# Filtrar provincias con tasa de Penetracion > 60% en 2022
provincias_criterio = calcular_provincias_criterio(df_kpi)

def show(df_penetracion, df_kpi):
    st.sidebar.title("Contexto")  
    st.title("Entendiendo y agregando valor a los datos.")
    st.write(
        """
        En esta sección, intentamos comprender que relación hay entre la proporción de habitantes y hogares con acceso al servicio. 
        Con la pregunta en mente 'Cuantos habitantes viven en promedio por hogar?', buscamos en la base de datos de la Dirección General de Estadísticas y Censos (DGEC) de Argentina.
        """
    )
    plot_correlacion_hogar_hab(df_penetracion)

    
    st.write("""
    Surje la necesidad de contrastar los datos con alguna métrica de interés, como lo son los ingresos a la compañía, 
    debido a la relevancia del valor del dólar en torno a la actividad económica en el país.
    """)
    
    st.header("Comparación entre Promedio de Ingresos y Valor del Dólar (Dólar Blue)")
    imagen_correlacion_ingresos_dolar = plot_correlacion_ingresos_dolar(df_kpi)
    st.image(imagen_correlacion_ingresos_dolar, caption='Comparación entre Promedio de Ingresos y Valor del Dólar (Dólar Blue)', use_column_width=True)
    st.write("""
    Este gráfico muestra el promedio de ingresos en miles de pesos argentinos y en relación del valor del dólar.
    Se observa una alta correlaciaón de datos.
    """)
    
    st.write("""
    Se toma la decisión de convertir los ingresos a dólares.
    """)
