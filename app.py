# app.py

import streamlit as st
from utils.horario import es_dia_operativo, obtener_hora_colombia
from utils.activos import selector_activo
from utils.taxi import mostrar_estrategia_taxi, modo_simulacion
import time
import pytz
from datetime import datetime

# Configuración inicial
st.set_page_config(page_title="Eddie Broker – TAXI", layout="centered")

# Título principal
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Mostrar hora en tiempo real (al recargar o al interactuar)
zona_col = pytz.timezone("America/Bogota")
ahora = datetime.now(zona_col).strftime("%H:%M:%S")
st.markdown(f"🕒 Hora Colombia actual: **{ahora}**")

# Evaluar si es día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")

    # Selector de activo
    activo = selector_activo()

    # Mostrar estrategia TAXI
    mostrar_estrategia_taxi(activo)

else:
    st.warning("🚫 Hoy NO es un día operativo (ni COL ni NYSE).")
    modo_simulacion()
