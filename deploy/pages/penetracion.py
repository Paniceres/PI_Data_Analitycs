import streamlit as st

def show(df_kpi):
    st.sidebar.title("KPI Penetracion")
    st.title("")
    
    st.write('''
             Al analizar los datos, encontramos que la tecnología inalámbrica (como 4G o 5G) muestra una correlación positiva 
más fuerte con la tasa de penetración en comparación con tecnologías como ADSL.
La razón radica en su naturaleza inalámbrica, lo que permite llegar a áreas donde la instalación de cables sería difícil o costosa. 
En zonas remotas o densamente pobladas, donde instalar cables es complicado, las conexiones inalámbricas son altamente beneficiosas. 
Además, la tecnología inalámbrica ofrece flexibilidad y accesibilidad, facilitando que más personas se conecten a Internet sin complicaciones.
En contraste, tecnologías como ADSL, que dependen de conexiones por cable, pueden tener limitaciones de alcance y dificultades de instalación, especialmente en áreas geográficamente desafiantes.''')