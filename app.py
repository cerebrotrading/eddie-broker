# app.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils.horario import es_dia_operativo
from utils.activos import selector_activo
from utils.taxi import mostrar_estrategia_taxi, modo_simulacion
from datetime import datetime
import pytz

# 🧩 Configuración
st.set_page_config(
    page_title="Eddie Broker – TAXI",
    layout="wide",
    page_icon="💀",
)

# ⏱️ Auto recarga cada 5 segundos
st_autorefresh(interval=5000, limit=None, key="refresh")

# 🧠 Encabezado
st.title("🤖 Eddie Broker – Estrategia TAXI")

# 🕒 Hora Colombia actual
zona_col = pytz.timezone("America/Bogota")
ahora = datetime.now(zona_col).strftime("%H:%M:%S")
st.markdown(f"🕒 Hora Colombia actual: **{ahora}**")

# 📅 Día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")

    col1, col2 = st.columns([1, 2])
    with col1:
        activo = selector_activo()
    with col2:
        mostrar_estrategia_taxi(activo)
else:
    st.warning("🚫 Hoy NO es un día operativo (ni COL ni NYSE).")
    modo_simulacion()
