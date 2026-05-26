import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AquaLimpia S.A. - Dashboard Exploratorio", layout="wide")

st.title("💧 AquaLimpia S.A. - Control de Plantas Residuales")
st.markdown("### Dashboard Exploratorio de Desempeño y Cumplimiento Normativo")

# Cargar datos procesados
@st.cache_data
def load_data():
    ruta_datos = r"C:\Users\vllhcontrol19\Desktop\dataset.xlsx"
    df = pd.read_excel(ruta_datos)
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
    df['eficiencia_remocion_DBO'] = ((df['DBO_entrada_mg_L'] - df['DBO_salida_mg_L']) / df['DBO_entrada_mg_L']) * 100
    return df

df = load_data()

# Filtros laterales
st.sidebar.header("Filtros de Análisis")
plantas = st.sidebar.multiselect("Selecciona la(s) Planta(s):", options=df['planta'].unique(), default=df['planta'].unique())
df_filtered = df[df['planta'].isin(plantas)]

# KPIs Principales
tasa_cumplimiento = (df_filtered['cumplimiento_norma'].mean()) * 100
eficiencia_med = df_filtered['eficiencia_remocion_DBO'].mean()

col1, col2, col3 = st.columns(3)
col1.metric(label="Tasa Global de Cumplimiento", value=f"{tasa_cumplimiento:.1f}%")
col2.metric(label="Eficiencia Media DBO", value=f"{eficiencia_med:.1f}%")
col3.metric(label="Total Registros Analizados", value=len(df_filtered))

st.markdown("---")

# Gráficos de análisis
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Relación entre Caudal de Entrada y DBO de Salida")
    fig1 = px.scatter(df_filtered, x="caudal_entrada_m3_d", y="DBO_salida_mg_L", 
                      color="planta", symbol="cumplimiento_norma",
                      labels={"caudal_entrada_m3_d": "Caudal Entrada (m³/d)", "DBO_salida_mg_L": "DBO Salida (mg/L)"},
                      title="Análisis de Desviaciones de DBO por Volumen de Caudal")
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.subheader("Consumo de Energía en Aireación vs Lodos Generados")
    fig2 = px.scatter(df_filtered, x="energia_aeracion_kWh", y="lodos_generados_kg_d", 
                      color="planta", size="DBO_entrada_mg_L",
                      labels={"energia_aeracion_kWh": "Energía Aireación (kWh)", "lodos_generados_kg_d": "Lodos Generados (kg/d)"},
                      title="Comportamiento y Eficiencia Operativa Interna")
    st.plotly_chart(fig2, use_container_width=True)