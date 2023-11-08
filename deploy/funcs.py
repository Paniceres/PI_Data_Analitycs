import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image
import io



# Contexto

def plot_correlacion_hogar_hab(df_penetracion):
    st.subheader('Penetración de conectividad por año')

    # Crear una figura para el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar los datos
    sns.lineplot(data=df_penetracion, x='Año', y='Accesos por cada 100 hogares', label='Accesos por cada 100 hogares', ax=ax)
    sns.lineplot(data=df_penetracion, x='Año', y='Accesos por cada 100 hab', label='Accesos por cada 100 hab', ax=ax)

    df_penetracion['Accesos por cada 3.24 hab'] = df_penetracion['Accesos por cada 100 hab'] * 3.24
    sns.lineplot(data=df_penetracion, x='Año', y='Accesos por cada 3.24 hab', label='Accesos por cada 3.24 hab', ax=ax)

    # Configurar el gráfico
    plt.xlabel('Año')
    plt.ylabel('Accesos')
    plt.grid(True)
    plt.legend()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Texto explicativo
    st.write(
        """
        Notamos una completa correlación de datos y tendencias entre los accesos cada 100 hogares y 100 habitantes.
        El promedio de habitantes por hogar fue realizado por la Dirección General de Estadísticas y Censos (DGEC) de Argentina.
        Decidimos quedarnos solo con el dato de accesos cada 100 hogares para evitar redundancias.
        """
    )

def plot_correlacion_ingresos_dolar(df_kpi):
    # Calcula los promedios de ingresos por año
    promedios_por_año = df_kpi.groupby('Año')['Ingresos (miles de pesos)'].mean()

    # Diccionario con tasas de cambio de pesos a dólares (dólar blue)
    tasas_de_cambio = {
        2022: 0.007846,
        2021: 0.01054,
        2020: 0.01445,
        2019: 0.02144,
        2018: 0.03759,
        2017: 0.06058,
        2016: 0.06787,
        2015: 0.1090,
        2014: 0.1235
    }

    # Crea un DataFrame a partir del diccionario de tasas de cambio
    df_tasas_de_cambio = pd.DataFrame(list(tasas_de_cambio.items()), columns=['Año', 'Tasa de Cambio Dólar Blue'])

    # Calcula el valor del dólar en pesos argentinos
    df_tasas_de_cambio['Valor del Dólar en Pesos'] = 1 / df_tasas_de_cambio['Tasa de Cambio Dólar Blue']

    # Crea un gráfico de doble eje y para mostrar los promedios por año y el valor del dólar en pesos argentinos
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Gráfico de promedios de ingresos por año
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Promedio de Ingresos (miles de pesos)', color='tab:blue')
    ax1.plot(promedios_por_año.index, promedios_por_año.values, marker='o', color='tab:blue', linestyle='-', linewidth=2, markersize=8)
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Gráfico del valor del dólar en pesos argentinos en el segundo eje y
    ax2 = ax1.twinx()
    ax2.set_ylabel('Valor del Dólar en Pesos Argentinos', color='tab:red')
    ax2.plot(df_tasas_de_cambio['Año'], df_tasas_de_cambio['Valor del Dólar en Pesos'], marker='o', color='tab:red', linestyle='-', linewidth=2, markersize=8)
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title('Comparación entre Promedio de Ingresos y Valor del Dólar (Dólar Blue)')
    plt.grid(True)
    
    # Guarda el gráfico como un archivo de imagen temporal
    plt.savefig('temp_correlacion_ingresos_dolar.png')
    plt.close()

    # Lee el archivo de imagen con Pillow
    image = Image.open('temp_correlacion_ingresos_dolar.png')

    # Convierte la imagen a bytes para mostrarla en Streamlit
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes

def calcular_provincias_criterio(df_kpi):
    datos_2022 = df_kpi[df_kpi['Año'] == 2022]
    provincias_criterio = datos_2022[datos_2022['Accesos por cada 100 hogares'] < 60]
    return provincias_criterio['Provincia'].unique()

# Criterio

def plot_criterio_provincia(df_kpi):
   # Calcula el promedio de Accesos por cada 100 hogares para cada provincia en 2022
   promedio_por_provincia_2022 = df_kpi[df_kpi['Año'] == 2022].groupby('Provincia')['Accesos por cada 100 hogares'].mean().reset_index()

   # Crea un gráfico de barras para mostrar el promedio de Accesos por cada 100 hogares por provincia en 2022
   fig, ax = plt.subplots(figsize=(12, 6))
   sns.barplot(x='Provincia', y='Accesos por cada 100 hogares', data=promedio_por_provincia_2022, palette='viridis', ax=ax)
   ax.set_xlabel('Provincia')
   ax.set_ylabel('Promedio de Accesos por cada 100 hogares')
   ax.set_title('Promedio de Accesos por cada 100 hogares por Provincia en 2022')
   ax.set_xticklabels(ax.get_xticklabels(), rotation=90) 
   ax.grid(axis='y')

   # Agrega una línea punteada en el valor 60
   ax.axhline(y=60, color='red', linestyle='--', linewidth=2, label='Línea en 60')

   # Muestra el gráfico con Streamlit
   st.pyplot(fig)
   
   text = '''
   Vemos el promedio de penetración de internet por cada 100 hogares por provincia,
   son 10 las provincias que se encuentran por debajo al 60%. Serán objeto de análisis.
   '''
   st.write(text)

def plot_tasa_crecimiento_penetracion_criterio(df_kpi, provincias_criterio):
    # Filtra los datos para las provincias con tasa de acceso por debajo del 60% en 2022
    provincias_filtradas = df_kpi[df_kpi['Provincia'].isin(provincias_criterio)]

    # Calcula el promedio de tasa de crecimiento por año para las provincias filtradas en 2022
    promedio_tasa_crecimiento = provincias_filtradas.groupby('Año')['Tasa de Crecimiento Penetracion'].mean()

    # Crea un gráfico de líneas para mostrar el promedio de tasa de crecimiento por año
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=promedio_tasa_crecimiento.index, y=promedio_tasa_crecimiento.values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)

    # Agrega una línea de tendencia roja punteada
    sns.regplot(x=promedio_tasa_crecimiento.index, y=promedio_tasa_crecimiento.values, ci=None, scatter=False, color='red', line_kws={'linestyle':'dashed'})

    plt.xlabel('Año')
    plt.ylabel('Tasa de Crecimiento Promedio (%)')
    plt.title('Tasa de Crecimiento Promedio de Penetración por Año para Provincias con Acceso < 60% en 2022')
    plt.grid(True)

    # Guarda el gráfico como un archivo de imagen temporal
    plt.savefig('temp_plot.png')
    plt.close()

    # Lee el archivo de imagen con Pillow
    image = Image.open('temp_plot.png')

    # Convierte la imagen a bytes para mostrarla en Streamlit
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes
    
def plot_dolares_ingresos_tasaIngresos(df_kpi):
    # Cálculo del promedio de ingresos por año en miles de dólares
    promedios_por_año_dolares = df_kpi.groupby('Año')['Ingresos (miles USD)'].mean()

    # Cálculo de la tasa de crecimiento de ingresos por año y trimestre
    # Combina 'Año' y 'Trimestre' en un índice temporal temporalmente
    df_kpi['Año-Trimestre'] = df_kpi['Año'].astype(str) + '-' + df_kpi['Trimestre'].astype(str)
    tasa_crecimiento_ingresos = df_kpi.groupby('Año-Trimestre')['Tasa de Crecimiento Ingresos'].mean()
    
    # Restaura el dataframe original eliminando el índice temporal temporal
    del df_kpi['Año-Trimestre']
    
    # Crear subplots
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Primer subplot: Ingresos por año en miles de dólares
    axes[0].plot(promedios_por_año_dolares.index, promedios_por_año_dolares.values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
    axes[0].set_xlabel('Año')
    axes[0].set_ylabel('Ingresos (en miles de dólares)')
    axes[0].set_title('Ingresos por Año (en miles de dólares)')
    axes[0].grid(True)
    axes[0].set_ylim(0)

    # Añade una línea de tendencia
    coefficients = np.polyfit(promedios_por_año_dolares.index.astype(int), promedios_por_año_dolares.values, 1)
    polynomial = np.poly1d(coefficients)
    axes[0].plot(promedios_por_año_dolares.index, polynomial(promedios_por_año_dolares.index.astype(int)), color='red', linestyle='--', label='Línea de Tendencia')
    axes[0].legend()

    # Segundo subplot: Tasa de crecimiento de ingresos por año
    axes[1].plot(tasa_crecimiento_ingresos.index, tasa_crecimiento_ingresos.values, marker='o', color='g', linestyle='-', linewidth=2, markersize=8)
    axes[1].set_xlabel('Año')
    axes[1].set_ylabel('Tasa de Crecimiento de Ingresos (%)')
    axes[1].set_title('Tasa de Crecimiento de Ingresos por Año')
    axes[1].grid(True)
    axes[1].tick_params(axis='x', rotation=90) 


    # Ajusta el espaciado entre subplots
    plt.tight_layout()
    
    # Guarda el gráfico como un archivo de imagen temporal
    plt.savefig('temp_dolares_ingresos_tasaIngresos.png')
    plt.close()

    # Lee el archivo de imagen con Pillow
    image = Image.open('temp_dolares_ingresos_tasaIngresos.png')

    # Convierte la imagen a bytes para mostrarla en Streamlit
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes

def plot_dolares_ingresos_tasaPenetracion(df_kpi):
    # Cálculo del promedio de ingresos por año en miles de dólares
    promedios_por_año_dolares = df_kpi.groupby('Año')['Ingresos (miles USD)'].mean()
    
    # Combina 'Año' y 'Trimestre' en un índice temporal temporalmente
    df_kpi['Año-Trimestre'] = df_kpi['Año'].astype(str) + '-' + df_kpi['Trimestre'].astype(str)
    tasa_crecimiento_penetracion = df_kpi.groupby('Año-Trimestre')['Tasa de Crecimiento Penetracion'].mean()

    # Restaura el dataframe original eliminando el índice temporal temporal
    del df_kpi['Año-Trimestre']

    # Crear subplots
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Primer subplot: Ingresos por año en miles de dólares
    axes[0].plot(promedios_por_año_dolares.index, promedios_por_año_dolares.values, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
    axes[0].set_xlabel('Año')
    axes[0].set_ylabel('Ingresos (en miles de dólares)')
    axes[0].set_title('Ingresos por Año (en miles de dólares)')
    axes[0].grid(True)
    axes[0].set_ylim(0)

    # Añade una línea de tendencia
    coefficients = np.polyfit(promedios_por_año_dolares.index.astype(int), promedios_por_año_dolares.values, 1)
    polynomial = np.poly1d(coefficients)
    axes[0].plot(promedios_por_año_dolares.index, polynomial(promedios_por_año_dolares.index.astype(int)), color='red', linestyle='--', label='Línea de Tendencia')
    axes[0].legend()

    # Segundo subplot: Tasa de crecimiento de ingresos por año
    axes[1].plot(tasa_crecimiento_penetracion.index, tasa_crecimiento_penetracion.values, marker='o', color='g', linestyle='-', linewidth=2, markersize=8)
    axes[1].set_xlabel('Año')
    axes[1].set_ylabel('Tasa de Crecimiento de Penetración (%)')
    axes[1].set_title('Tasa de Crecimiento de Penetración por Año')
    axes[1].grid(True)
    axes[1].tick_params(axis='x', rotation=90) 


    # Ajusta el espaciado entre subplots
    plt.tight_layout()

    # Guarda el gráfico como un archivo de imagen temporal
    plt.savefig('temp_dolares_ingresos_tasaPenetracion.png')
    plt.close()

    # Lee el archivo de imagen con Pillow
    image = Image.open('temp_dolares_ingresos_tasaPenetracion.png')

    # Convierte la imagen a bytes para mostrarla en Streamlit
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes
    
def plot_correlacion_tasaIngresos_tasaPenetracion(df_kpi):
    # Combina 'Año' y 'Trimestre' en un índice temporal temporalmente
    df_kpi['Año-Trimestre'] = df_kpi['Año'].astype(str) + '-' + df_kpi['Trimestre'].astype(str)
    media_tasa_crecimiento_penetracion = df_kpi.groupby('Año-Trimestre')['Tasa de Crecimiento Penetracion'].mean()

    # Crea un gráfico de líneas para la relación entre la tasa de crecimiento de ingresos y la tasa de penetración
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Año-Trimestre', y='Tasa de Crecimiento Ingresos', data=df_kpi, marker='o', label='Tasa de Crecimiento Ingresos', color='blue')
    sns.lineplot(x=media_tasa_crecimiento_penetracion.index, y=media_tasa_crecimiento_penetracion.values, marker='o', label='Tasa de Crecimiento Penetración', color='green')
    plt.xlabel('Año-Trimestre')
    plt.ylabel('Tasa de Crecimiento')
    plt.title('Relación entre la Tasa de Crecimiento de Ingresos y Tasa de Crecimiento de Penetración del Servicio')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Restaura el dataframe original eliminando el índice temporal temporal
    del df_kpi['Año-Trimestre']
    text = '''
    Observando al detalle, notamos la volatilidad de los datos, no se nota una correlación directa.'''  
    return text

# accesibilidad, penetracion kpi

def plot_matriz_correlacion_penetracion(df_kpi):
    # Selecciona las columnas relevantes para la matriz de correlación
    columnas_correlacion = ['ADSL', 'Cablemodem', 'Fibra optica', 'Wireless', 'Tasa de Crecimiento Penetracion']

    # Calcula la matriz de correlación
    matriz_correlacion = df_kpi[columnas_correlacion].corr()

    # Muestra la matriz de correlación
    st.header("Matriz de Correlación entre Tecnologías y Tasa de Crecimiento de Penetración")
    st.write(matriz_correlacion)
     
def plot_matriz_correlacion_penetracion_interactiva(df_kpi, provincias_criterio):
    # Lista desplegable para seleccionar la provincia
    provincia_seleccionada = st.selectbox("Selecciona una provincia:", provincias_criterio)

    # Filtra el DataFrame por la provincia seleccionada
    df_provincia = df_kpi[df_kpi['Provincia'] == provincia_seleccionada]

    # Selecciona las columnas relevantes para la matriz de correlación
    columnas_correlacion = ['ADSL', 'Cablemodem', 'Fibra optica', 'Wireless', 'Tasa de Crecimiento Penetracion']

    # Calcula la matriz de correlación para la provincia seleccionada
    matriz_correlacion_provincia = df_provincia[columnas_correlacion].corr()

    # Estilo para la matriz de correlación
    sns.set(font_scale=1.2)
    plt.figure(figsize=(8, 6))
    st.header(f"Matriz de Correlación para {provincia_seleccionada}")
    sns.heatmap(matriz_correlacion_provincia, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, annot_kws={"size": 14})
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot()
    
def plot_promedio_penetracion(df_kpi):
    # Calcula el promedio de Accesos por cada 100 hogares por provincia en 2022 para todas las provincias
    promedio_accesos_por_provincia_total = df_kpi[df_kpi['Año'] == 2022].groupby('Provincia')['Accesos por cada 100 hogares'].mean()

    # Filtra las provincias en provincias_menores_al_60_list
    df_provincias_menores_al_60 = df_kpi[df_kpi['Provincia'].isin(provincias_criterio)]

    # Calcula el promedio de Accesos por cada 100 hogares por provincia en 2022 para las provincias en provincias_menores_al_60_list
    promedio_accesos_por_provincia_menores_al_60 = df_provincias_menores_al_60[df_provincias_menores_al_60['Año'] == 2022].groupby('Provincia')['Accesos por cada 100 hogares'].mean()

    # Crea el gráfico de barras para las provincias en provincias_menores_al_60_list en 2022
    plt.figure(figsize=(12, 6))
    sns.barplot(x=promedio_accesos_por_provincia_menores_al_60.index, y=promedio_accesos_por_provincia_menores_al_60.values, palette='viridis')
    plt.axhline(y=60, color='red', linestyle='--', label='60 Accesos por cada 100 hogares')
    plt.xlabel('Provincia')
    plt.ylabel('Promedio de Accesos por cada 100 hogares')
    plt.title('Promedio de Accesos por cada 100 hogares por Provincia en 2022 (Provincias Menores al 60% de penetración)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()    

def plot_promedio_penetracion_interactivo(df_kpi, provincias_criterio, filtro_activado=True):
    if filtro_activado:
        df_filtrado = df_kpi[df_kpi['Provincia'].isin(provincias_criterio)]
    else:
        df_filtrado = df_kpi

    # Calcula el promedio de Accesos por cada 100 hogares por provincia en 2022 para las provincias en provincias_criterio
    promedio_accesos_por_provincia = df_filtrado[df_filtrado['Año'] == 2022].groupby('Provincia')['Accesos por cada 100 hogares'].mean()

    # Crea el gráfico de barras para las provincias en provincias_criterio en 2022
    plt.figure(figsize=(12, 6))
    sns.barplot(x=promedio_accesos_por_provincia.index, y=promedio_accesos_por_provincia.values, palette='viridis')
    plt.axhline(y=60, color='red', linestyle='--', label='60 Accesos por cada 100 hogares')
    plt.xlabel('Provincia')
    plt.ylabel('Promedio de Accesos por cada 100 hogares')
    plt.title('Promedio de Accesos por cada 100 hogares por Provincia en 2022')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Muestra el gráfico usando st.pyplot() con la figura de Matplotlib
    st.pyplot()

def plot_correlacion_tecnologia_penetracion(df_kpi, provincias_criterio, filtro_activado=True):
    st.header("Correlación entre Tecnologías y Accesos por cada 100 hogares")

    # Filtrar el dataframe según las provincias_criterio seleccionadas
    df_filtrado = df_kpi[df_kpi['Provincia'].isin(provincias_criterio)]

    # Verificar si hay datos después de aplicar el filtro
    if df_filtrado.empty:
        st.error("No hay datos disponibles para las provincias seleccionadas.")
        return

    # Crear un gráfico de líneas para cada tecnología
    fig, axes = plt.subplots(figsize=(12, 6))

    # Graficar tecnologías
    for tecnologia in ['ADSL', 'Cablemodem', 'Fibra optica', 'Wireless']:
        sns.lineplot(data=df_filtrado, x='Año', y=tecnologia, label=f'{tecnologia}')

    # Graficar la velocidad media con una línea roja de referencia en 60 Accesos por cada 100 hogares
    sns.lineplot(data=df_filtrado.groupby('Año')['Accesos por cada 100 hogares'].mean().reset_index(), x='Año', y='Accesos por cada 100 hogares', color='red', label='Accesos por cada 100 hogares Media (Promedio)')
    plt.axhline(y=60, color='red', linestyle='--', label='60 Accesos por cada 100 hogares (Referencia)')

    # Configurar el gráfico
    plt.xlabel('Año')
    plt.ylabel('Accesos por cada 100 hogares')
    plt.title('Correlación entre Tecnologías y Accesos por cada 100 hogares')
    plt.legend()
    plt.grid(True)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

def calcular_alteracion_penetracion(df_kpi, provincias_seleccionadas):
    # Filtrar el dataframe según las provincias seleccionadas
    df_filtrado = df_kpi[df_kpi['Provincia'].isin(provincias_seleccionadas)]

    # Obtener los porcentajes de tecnología respecto al total de tecnología
    df_filtrado['ADSL'] = df_filtrado['ADSL'] / df_filtrado['Total Tecnologia']
    df_filtrado['Fibra optica'] = df_filtrado['Fibra optica'] / df_filtrado['Total Tecnologia']

    # Calcular los porcentajes de disminución/adición de ADSL y Fibra Óptica para alcanzar el 20% de mejora
    correlacion_tecnologia_penetracion = df_filtrado[['ADSL', 'Fibra optica', 'Accesos por cada 100 hogares', 'Total Tecnologia']].corr()['Accesos por cada 100 hogares']
    correlacion_fibra_penetracion = correlacion_tecnologia_penetracion['Fibra optica']
    correlacion_adsl_penetracion = -correlacion_tecnologia_penetracion['ADSL']

    porcentaje_aumento_penetracion = 20  # Aumento del 20%
    disminucion_adsl_necesaria = (porcentaje_aumento_penetracion / 100) * correlacion_adsl_penetracion 
    aumento_fibra_necesaria = (porcentaje_aumento_penetracion / 100) * correlacion_fibra_penetracion

    # Calcular el total de accesos nuevos para ADSL y Fibra Óptica
    total_accesos_nuevos_adsl = disminucion_adsl_necesaria * df_filtrado['Total Tecnologia'].sum()
    total_accesos_nuevos_fibra = aumento_fibra_necesaria * df_filtrado['Total Tecnologia'].sum()

    return disminucion_adsl_necesaria, aumento_fibra_necesaria, total_accesos_nuevos_adsl, total_accesos_nuevos_fibra


    
# calidad, tecnologia kpi

def plot_promedio_velocidad(df_kpi):
    # Calcula el promedio de Mbps por provincia en 2022 para todas las provincias
    promedio_mbps_por_provincia_total = df_kpi[df_kpi['Año'] == 2022].groupby('Provincia')['Mbps (Media de bajada)'].mean()

    # Filtra las provincias en provincias_menores_al_60_list
    df_provincias_menores_al_60 = df_kpi[df_kpi['Provincia'].isin(provincias_criterio)]

    # Calcula el promedio de Mbps por provincia en 2022 para las provincias en provincias_menores_al_60_list
    promedio_mbps_por_provincia_menores_al_60 = df_provincias_menores_al_60[df_provincias_menores_al_60['Año'] == 2022].groupby('Provincia')['Mbps (Media de bajada)'].mean()

    # Crea el gráfico de barras para las provincias en provincias_menores_al_60_list en 2022
    plt.figure(figsize=(12, 6))
    sns.barplot(x=promedio_mbps_por_provincia_menores_al_60.index, y=promedio_mbps_por_provincia_menores_al_60.values, palette='viridis')
    plt.axhline(y=50, color='red', linestyle='--', label='50 Mbps')
    plt.xlabel('Provincia')
    plt.ylabel('Promedio de Mbps')
    plt.title('Promedio de Mbps por Provincia en 2022 (Provincias Menores al 60% de penetración)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_promedio_velocidad_interactivo(df_kpi, provincias_criterio, filtro_activado=True):
    if filtro_activado:
        df_filtrado = df_kpi[df_kpi['Provincia'].isin(provincias_criterio)]
    else:
        df_filtrado = df_kpi

    # Calcula el promedio de Mbps por provincia en 2022 para las provincias en provincias_criterio
    promedio_mbps_por_provincia = df_filtrado[df_filtrado['Año'] == 2022].groupby('Provincia')['Mbps (Media de bajada)'].mean()

    # Crea el gráfico de barras para las provincias en provincias_criterio en 2022
    plt.figure(figsize=(12, 6))
    sns.barplot(x=promedio_mbps_por_provincia.index, y=promedio_mbps_por_provincia.values, palette='viridis')
    plt.axhline(y=50, color='red', linestyle='--', label='50 Mbps')
    plt.xlabel('Provincia')
    plt.ylabel('Promedio de Mbps')
    plt.title('Promedio de Mbps por Provincia en 2022')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Muestra el gráfico usando st.pyplot() con la figura de Matplotlib
    st.pyplot()

def matriz_correlacion_velocidad(df_kpi):
    correlacion = df_kpi[['ADSL', 'Cablemodem', 'Fibra optica', 'Wireless', 'Mbps (Media de bajada)']].corr()
    sns.heatmap(correlacion, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de Correlación')
    plt.show()
    
    text = '''
    Con esta matriz de correlación podemos observar que 'Fibra óptica' tiene una mayor correlación con la velocidad media de internet.'''
    return text

def plot_tendencia_tecnologia(df_kpi):
    # Calcular el promedio de cada tecnología a lo largo de los años para todas las provincias
    promedio_tecnologias = df_kpi.groupby('Año')[['ADSL', 'Cablemodem', 'Fibra optica', 'Wireless']].mean()

    # Crear el gráfico de tendencia general
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=promedio_tecnologias, dashes=False, markers=True)
    plt.xlabel('Año')
    plt.ylabel('Promedio de Porcentaje')
    plt.title('Tendencia General de Tecnologías a lo largo de los Años')
    plt.legend(title='Tecnología', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_correlacion_tecnologia_velocidad(df_kpi, provincias_criterio, filtro_activado=True):
    st.header("Correlación entre Tecnologías y Velocidad de Internet")

    # Filtrar el dataframe según las provincias_criterio seleccionadas
    df_filtrado = df_kpi[df_kpi['Provincia'].isin(provincias_criterio)]

    # Verificar si hay datos después de aplicar el filtro
    if df_filtrado.empty:
        st.error("No hay datos disponibles para las provincias seleccionadas.")
        return

    # Crear un gráfico de líneas para cada tecnología
    fig, axes = plt.subplots(figsize=(12, 6))

    # Graficar tecnologías
    for tecnologia in ['ADSL', 'Cablemodem', 'Fibra optica', 'Wireless']:
        sns.lineplot(data=df_filtrado, x='Año', y=tecnologia, label=f'{tecnologia}')

    # Graficar la velocidad media con una línea roja de referencia en 50 Mbps
    sns.lineplot(data=df_filtrado.groupby('Año')['Mbps (Media de bajada)'].mean().reset_index(), x='Año', y='Mbps (Media de bajada)', color='red', label='Velocidad Media (Promedio)')
    plt.axhline(y=50, color='red', linestyle='--', label='50 Mbps (Referencia)')

    # Configurar el gráfico
    plt.xlabel('Año')
    plt.ylabel('Mbps')
    plt.title('Correlación entre Tecnologías y Velocidad de Internet')
    plt.legend()
    plt.grid(True)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    
def calcular_alteracion_tecnologia(df_kpi, provincias_seleccionadas):
    # Filtrar el dataframe según las provincias seleccionadas
    df_filtrado = df_kpi[df_kpi['Provincia'].isin(provincias_seleccionadas)]

    # Obtener los porcentajes de tecnología respecto al total de tecnología
    df_filtrado['ADSL'] = df_filtrado['ADSL'] / df_filtrado['Total Tecnologia']
    df_filtrado['Fibra optica'] = df_filtrado['Fibra optica'] / df_filtrado['Total Tecnologia']

    # Calcular los porcentajes de disminución/adición de ADSL y Fibra Óptica para alcanzar el 20% de mejora
    correlacion_tecnologia_velocidad = df_filtrado[['ADSL', 'Fibra optica', 'Mbps (Media de bajada)', 'Total Tecnologia']].corr()['Mbps (Media de bajada)']
    correlacion_fibra_velocidad = correlacion_tecnologia_velocidad['Fibra optica']
    correlacion_adsl_velocidad = -correlacion_tecnologia_velocidad['ADSL']

    porcentaje_aumento_velocidad = 20  # Aumento del 20%
    disminucion_adsl_necesaria = (porcentaje_aumento_velocidad / 100) * correlacion_adsl_velocidad 
    aumento_fibra_necesaria = (porcentaje_aumento_velocidad / 100) * correlacion_fibra_velocidad

    # Calcular el total de accesos nuevos para ADSL y Fibra Óptica
    total_accesos_nuevos_adsl = disminucion_adsl_necesaria * df_filtrado['Total Tecnologia'].sum()
    total_accesos_nuevos_fibra = aumento_fibra_necesaria * df_filtrado['Total Tecnologia'].sum()
    
    return disminucion_adsl_necesaria, aumento_fibra_necesaria, total_accesos_nuevos_adsl, total_accesos_nuevos_fibra