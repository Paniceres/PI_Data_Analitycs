import sys
import os
import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from notebooks import main  # No parece que necesites importar main aquí
import pandas as pd
import plotly.express as px

# Tu DataFrame original
df_accesos_velocidad = pd.read_csv('../data/processed/accesos_velocidad.csv')

# Lista de columnas de velocidad
columnas_velocidad = ['HASTA 512 kbps', '+ 512 Kbps - 1 Mbps', '+ 1 Mbps - 6 Mbps', '+ 6 Mbps - 10 Mbps',
                      '+ 10 Mbps - 20 Mbps', '+ 20 Mbps - 30 Mbps', '+ 30 Mbps', 'OTROS']

# Sidebar para seleccionar año
st.sidebar.header('Filtros')
selected_year = st.sidebar.selectbox('Selecciona un año:', sorted(df_accesos_velocidad['Año'].unique()))

# Filtrar datos según la selección del usuario
filtered_data = df_accesos_velocidad[df_accesos_velocidad['Año'] == selected_year]

# Reformatear los datos para tener solo dos columnas: categorías de velocidad y valores
melted_data = filtered_data.melt(id_vars=['Provincia'], value_vars=columnas_velocidad, 
                                 var_name='Categoría de Velocidad', value_name='Velocidad de Internet')

# Crear el gráfico interactivo
fig = px.line(melted_data, x='Categoría de Velocidad', y='Velocidad de Internet', color='Provincia',
              labels={'variable': 'Categorías de Velocidad', 'value': 'Velocidades de Internet'},
              title=f'Velocidades de Internet para el año {selected_year}',
              template='plotly')

# Mostrar el gráfico interactivo
st.plotly_chart(fig)
