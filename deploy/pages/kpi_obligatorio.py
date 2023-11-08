import streamlit as st
from funcs import (calcular_provincias_criterio, kpi_obligatorio)
from data_loader import DataLoader

# Crear una instancia de la clase DataLoader
data_load = DataLoader(data_directory='./data/readytogo')
data_load.load_data()
df_kpi = data_load.dataframes['kpi']

# Filtrar provincias con tasa de Penetracion > 60% en 2022
provincias_criterio = calcular_provincias_criterio(df_kpi)


def show(df_kpi, provincias_criterio, filtro_activado=True, tasa_mejora=None):
    st.sidebar.title("KPI Obligatorio")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write("Cantidad de accesos en relación al objetivo de mejora desesado")

   # Agrega un botón para activar o desactivar el filtro de provincias_criterio
    filtro_activado = st.checkbox("Filtrar por provincias seleccionadas", value=True)

    # Agrega un botón para activar o desactivar el filtro de provincias_criterio
    if filtro_activado:
        # Obtener las opciones de provincias_criterio y permitir múltiple selección
        opciones_provincias = list(provincias_criterio)
        provincias_seleccionadas = st.multiselect("Selecciona provincias", opciones_provincias, default=opciones_provincias)

        # Si no se selecciona ninguna provincia y el filtro está activado, mostrar un mensaje de error
        if not provincias_seleccionadas:
            provincias_seleccionadas = opciones_provincias
    else:
        # Si el filtro no está activado, mostrar todas las provincias
        provincias_seleccionadas = list(provincias_criterio)

    # Filtrar el DataFrame según las provincias seleccionadas
    df_filtrado = df_kpi[df_kpi['Provincia'].isin(provincias_seleccionadas)]

    # Verificar si hay datos después de aplicar el filtro
    if df_filtrado.empty:
        st.error("No hay datos disponibles para las provincias seleccionadas.")
        return
    
    st.sidebar.slider("Tasa de mejora", 1, 100, 2)
    
    # Check if tasa_mejora is None, and assign a default value if necessary
    if tasa_mejora is None:
        tasa_mejora = 2.0 

    # Calcular el KPI
    kpi = kpi_obligatorio(df_kpi, provincias_criterio, filtro_activado=True, tasa_mejora=tasa_mejora)
    # Mostrar el KPI
    st.write(f"KPI: {kpi}")

