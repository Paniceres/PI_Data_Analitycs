import streamlit as st
from funcs import (plot_promedio_penetracion_interactivo, calcular_provincias_criterio,
            plot_correlacion_tecnologia_penetracion, calcular_alteracion_penetracion   )
from data_loader import DataLoader

# Crear una instancia de la clase DataLoader
data_load = DataLoader(data_directory='./data/readytogo')
data_load.load_data()
df_kpi = data_load.dataframes['kpi']

# Filtrar provincias con tasa de Penetracion > 60% en 2022
provincias_criterio = calcular_provincias_criterio(df_kpi)



def show(df_kpi, provincias_criterio, filtro_activado=True):
    st.sidebar.title("KPI Penetracion")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write("Relación: Tecnología y Penetración.")
    st.write('''En torno a un KPI deseado del 10% de aumento en la penetración del servicio, 
             determinamos la distribución de tecnologías en pos del objetivo''')
    
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
    
    # Llama a la función para mostrar el gráfico interactivo de promedio de penetracion
    plot_promedio_penetracion_interactivo(df_filtrado, provincias_criterio, filtro_activado)

    # Llama a la función para mostrar el gráfico de correlación entre tecnologías y penetracion
    plot_correlacion_tecnologia_penetracion(df_filtrado, provincias_criterio, filtro_activado)

    try:
        # Obtener los valores de los KPIs
        disminucion_adsl_necesaria, aumento_fibra_necesaria, aumento_wireless_necesario, total_accesos_nuevos_adsl, total_accesos_nuevos_fibra, total_accesos_nuevos_wireless = calcular_alteracion_penetracion(df_kpi, provincias_seleccionadas, filtro_activado)
    except ValueError as e:
        st.error(str(e))
        return

    # Mostrar los KPIs como tarjetas
    st.write("### Para conseguir un aumento de Penetración de un 10% Trimestral")
    tarjeta_adsl_html = f"""
        <div style="background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; border-radius: .25rem; padding: .75rem 1.25rem; cursor: pointer;" onclick="adslClicked()">
            Disminuir ADSL en {disminucion_adsl_necesaria:.2f}%, equivalente a: {total_accesos_nuevos_adsl:.0f} accesos
        </div>
    """
    tarjeta_fibra_html = f"""
        <div style="background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; border-radius: .25rem; padding: .75rem 1.25rem; cursor: pointer;" onclick="fibraClicked()">
            Aumentar Fibra Óptica en {aumento_fibra_necesaria:.2f}%, equivalente a: {total_accesos_nuevos_fibra:.0f} accesos
        </div>
    """
    tarjeta_wireless_html = f"""
        <div style="background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; border-radius: .25rem; padding: .75rem 1.25rem; cursor: pointer;" onclick="wirelessClicked()">
            Aumentar Wireless en {aumento_wireless_necesario:.2f}%, equivalente a: {total_accesos_nuevos_wireless:.0f} accesos
        </div>
    """

    # Muestra las tarjetas en Streamlit
    st.markdown(tarjeta_adsl_html, unsafe_allow_html=True)
    st.markdown(tarjeta_fibra_html, unsafe_allow_html=True)
    st.markdown(tarjeta_wireless_html, unsafe_allow_html=True)
