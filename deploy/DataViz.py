import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

# Filtrar las provincias que tienen una tasa de acceso por debajo del 60%
provincias_criterio = datos_2022[datos_2022['Accesos por cada 100 hogares'] < 60]
provincias_criterio = provincias_criterio['Provincia'].unique()


def plot_penetracion_conectividad(df_penetracion):
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

