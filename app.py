# app.py

import streamlit as st
from utils.horario import es_dia_operativo, obtener_hora_colombia
from utils.activos import selector_activo
from utils.taxi import mostrar_estrategia_taxi, modo_simulacion

# Configuración inicial
st.set_page_config(page_title="Eddie Broker – TAXI", layout="centered")

# Título principal
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Hora actual en Colombia
hora_actual = obtener_hora_colombia()
st.markdown(f"🕒 Hora Colombia actual: **{hora_actual}**")

# Evaluación del día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
    
    # Selección de activo y ejecución de estrategia
    activo = selector_activo()
    mostrar_estrategia_taxi(activo)
else:
    st.warning("🚫 Hoy NO es un día operativo (ni COL ni NYSE).")
    modo_simulacion()
