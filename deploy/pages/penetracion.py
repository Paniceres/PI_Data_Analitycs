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



def show(df_kpi, provincias_criterio):
    st.sidebar.title("KPI Penetracion")
    st.write('''
             Al analizar los datos, encontramos que la tecnología inalámbrica (como 4G o 5G) muestra una correlación positiva 
más fuerte con la tasa de penetración en comparación con tecnologías como ADSL.
La razón radica en su naturaleza inalámbrica, lo que permite llegar a áreas donde la instalación de cables sería difícil o costosa. 
En zonas remotas o densamente pobladas, donde instalar cables es complicado, las conexiones inalámbricas son altamente beneficiosas. 
Además, la tecnología inalámbrica ofrece flexibilidad y accesibilidad, facilitando que más personas se conecten a Internet sin complicaciones.
En contraste, tecnologías como ADSL, que dependen de conexiones por cable, pueden tener limitaciones de alcance y dificultades de instalación, especialmente en áreas geográficamente desafiantes.''')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write("Título")
    st.write("Subtítulo")

    # Agrega un botón para activar o desactivar el filtro de provincias_criterio
    filtro_activado = st.checkbox("Filtrar por provincias seleccionadas", value=True)

    if filtro_activado:
        # Obtener las opciones de provincias_criterio y permitir múltiple selección
        opciones_provincias = list(provincias_criterio)
        provincias_seleccionadas = st.multiselect("Selecciona provincias", opciones_provincias, default=opciones_provincias)

        # Si no se selecciona ninguna provincia, considerar todas las provincias seleccionadas
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

    # Obtener los valores de los KPIs
    disminucion_adsl_necesaria, aumento_fibra_necesaria, aumento_wireless_necesario, total_accesos_nuevos_adsl, total_accesos_nuevos_fibra, total_accesos_nuevos_wireless = calcular_alteracion_penetracion(df_kpi, provincias_seleccionadas)

    # Mostrar los KPIs como tarjetas
    st.write("### Aumento de Velocidad en un 10% Trimestral")
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
