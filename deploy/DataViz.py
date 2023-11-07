import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class DataViz:
    def __init__(self):
        # Ruta al directorio donde se encuentran los archivos
        self.data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'readytogo')


    def load_data(self):
        # Lista de archivos en el directorio
        files = os.listdir(self.data_directory)

        # Diccionario para almacenar los DataFrames cargados
        self.dataframes = {}

        # Leer los DataFrames desde los archivos CSV
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(self.data_directory, file)
                dataframe_name = os.path.splitext(file)[0]  # Nombre del DataFrame sin extensión
                self.dataframes[dataframe_name] = pd.read_csv(file_path)

# Crear una instancia de la clase DataViz
data_viz = DataViz()

# Cargar los datos
data_viz.load_data()

# Acceder a los DataFrames cargados
df_penetracion = data_viz.dataframes['penetracion']
df_penetracion_ingresos = data_viz.dataframes['penetracion_ingresos']
df_tecnologia_velocidad = data_viz.dataframes['tecnologia_velocidad']
df_kpi = data_viz.dataframes['kpi']

# Filtrar los datos para el año 2022 usando la variable de instancia self.df_kpi
datos_2022 = df_kpi[df_kpi['Año'] == 2022]

# Lista provincias_criterio
provincias_criterio = datos_2022[datos_2022['Accesos por cada 100 hogares'] < 60]
provincias_criterio = provincias_criterio['Provincia'].unique()


def plot_correlacion_hogar_hab(df_penetracion):
    plt.figure(figsize=(10, 6))

    sns.lineplot(data=df_penetracion, x='Año', y='Accesos por cada 100 hogares', label='Accesos por cada 100 hogares')
    sns.lineplot(data=df_penetracion, x='Año', y='Accesos por cada 100 hab', label='Accesos por cada 100 hab')

    df_penetracion['Accesos por cada 3.24 hab'] = df_penetracion['Accesos por cada 100 hab'] * 3.24
    sns.lineplot(data=df_penetracion, x='Año', y='Accesos por cada 3.24 hab', label='Accesos por cada 3.24 hab')

    plt.xlabel('Año')
    plt.ylabel('Accesos')
    plt.title('Penetración de conectividad por año')
    plt.grid()
    plt.legend()
    plt.show()
    
    text = '''
    Notamos un aumento proporcionalmente correlacionado entre los accesos por cada 100 habitantes y 100 hogares.     
    Hay una significativa diferencia entre la cantidad neta de accesos, por lo que el volumen de datos es distinto.     
        Contemplando los datos del censo de 2010 de Argentina, extraemos el promedio general de habitantes que residen en un mismo hogar (3.24), 
    multiplindo los accesos por cada 100 habitantes y observando así una completa correlación de los datos. 
    El promedio de habitantes por hogar fue realizado por la Dirección General de Estadísticas y Censos (DGEC) de Argentina.
    '''
    return text

def plot_criterio_provincia(df_kpi):
    # Calcula el promedio de Accesos por cada 100 hogares para cada provincia en 2022
    promedio_por_provincia_2022 = datos_2022.groupby('Provincia')['Accesos por cada 100 hogares'].mean().reset_index()

    # Crea un gráfico de barras para mostrar el promedio de Accesos por cada 100 hogares por provincia en 2022
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Provincia', y='Accesos por cada 100 hogares', data=promedio_por_provincia_2022, palette='viridis')
    plt.xlabel('Provincia')
    plt.ylabel('Promedio de Accesos por cada 100 hogares')
    plt.title('Promedio de Accesos por cada 100 hogares por Provincia en 2022')
    plt.xticks(rotation=90)  
    plt.grid(axis='y')

    # Agrega una línea punteada en el valor 60
    plt.axhline(y=60, color='red', linestyle='--', linewidth=2, label='Línea en 60')

    # Muestra el gráfico
    plt.legend() 
    plt.show()
    
    text = '''
    Vemos el promedio de penetración de internet por cada 100 hogares por provincia,
    son 10 las provincias que se encuentran por debajo al 60%. Serán objeto de análisis.
    '''
    return text

def plot_tasa_crecimiento_penetracion_criterio(df_kpi):
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

    # Muestra el gráfico
    plt.show()
    
    text = '''
    Se observa una tendencia alcista en la tasa de penetración por cada 100 hogares, 
    con una alta volatilidad en el corto plazo, esperamos estabilidad a largo plazo. 
    Indagaremos en torno a los factores que volatilizan la tendencia.
    
    El factor económico siempre es el gran factor a considerar, encontramos un dataset donde detallan los ingresos en miles de pesos por trimestre. 
    Ante el condicional de devaluación de la moneda pivote, consideramos convertir los datos a dolares, 
    gracias a web scrapping https://www.exchange-rates.org/, 
    obtuvimos los valores promedio de conversión del dolar por año y comparamos contra la sumatoria de la ingesta en miles de pesos por año.
    '''
    return text

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
    plt.show()
    
    text = '''
    Se observa una tendencia alcista en la inversión año tras año, observamos una correlación entre los datos, 
    ha de haber una estabilidad en la ingesta neta.
    '''
    return text

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

    # Muestra los subplots
    plt.show()

    text = '''
    Observamos una estabilidad a largo plazo en torno a una ingesta de 500.000usd. Corroboraremos la correlación entre la ingesta 
    promedio en dolares contra la tasa de crecimiento promedio de los países en los que hacemos foco, los que tienen una tasa menor al 60%.'''
    return text

def plot_dolares_ingresos_tasaPenetracion(df_kpi):
    # Cálculo del promedio de ingresos por año en miles de dólares
    promedios_por_año_dolares = df_kpi.groupby('Año')['Ingresos (miles USD)'].mean()
    
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

    # Muestra los subplots
    plt.show()
    
    text = '''
    Encontramos correlacionados los años desde 2014 hasta 2020, si bien los patrones de comportamiento son similares, 
    correlacionandose anomalías y picos entre ambos, no hay una correlación en torno a la tendencia, refiero a que si bien aumenta 
    la penetración del servicio a un mayor porcentaje de la población, no se traduce necesariamente en una mayor retribución económica para la empresa.             

    No obstante, el año 2018 parece ser una anomalía no explicada aún, indagaremos este año por separado luego.
    '''
    return text

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

def plot_correlacion_tecnologia_velocidad(df_kpi):
    # Filtrar las provincias con un promedio de menos de 50 Mbps de bajada para el año 2022
    provincias_filtradas = df_kpi[df_kpi['Año'] == 2022].groupby('Provincia')['Mbps (Media de bajada)'].mean()
    provincias_criterio = provincias_filtradas[provincias_filtradas < 50].index.tolist()

    # Si hay provincias que cumplen el criterio, mostrar el gráfico; de lo contrario, mostrar un mensaje de error
    if not provincias_criterio:
        st.error("No hay provincias disponibles que cumplan el criterio de menos de 50 Mbps de bajada para el año 2022.")
        return
    
    # Seleccionar una provincia de las que cumplen el criterio
    provincia_seleccionada = st.selectbox("Selecciona una provincia", provincias_criterio)

    # Obtener el promedio de velocidad de bajada para la provincia seleccionada
    promedio_provincia = df_kpi[(df_kpi['Provincia'] == provincia_seleccionada)]
    
    # Crear un gráfico de líneas para cada tecnología en la provincia seleccionada
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    
    # Graficar tecnologías en la primera columna
    for tecnologia in ['ADSL', 'Cablemodem', 'Fibra optica', 'Wireless']:
        df_temp = df_kpi[(df_kpi['Provincia'] == provincia_seleccionada)]
        sns.lineplot(data=df_temp, x='Año', y=tecnologia, label=f'{tecnologia}', ax=axes[0])
    axes[0].set_xlabel('Año')
    axes[0].set_ylabel('Cantidad')
    axes[0].set_title(f'Tecnologías en {provincia_seleccionada}')
    axes[0].legend(title='Tecnología', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Graficar velocidad media en la segunda columna
    sns.lineplot(data=promedio_provincia, x='Año', y='Mbps (Media de bajada)', color='green', label='Velocidad Media', ax=axes[1])
    axes[1].axhline(y=50, color='red', linestyle='--', label='50 Mbps')
    axes[1].set_xlabel('Año')
    axes[1].set_ylabel('Mbps')
    axes[1].set_title(f'Promedio de Velocidad en {provincia_seleccionada}')
    axes[1].legend(title='Línea', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Ajustar el espacio entre subgráficos
    plt.tight_layout()
    st.pyplot(fig)

plot_correlacion_tecnologia_velocidad(df_kpi)