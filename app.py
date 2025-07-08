# app.py

import streamlit as st
from utils.horario import es_dia_operativo
from utils.activos import selector_activo
from utils.taxi import mostrar_estrategia_taxi, modo_simulacion
from datetime import datetime
import pytz

# 🧩 Configuración visual
st.set_page_config(
    page_title="Eddie Broker – TAXI",
    layout="wide",
    page_icon="💀",
)

# 🧠 Encabezado principal
st.title("🤖 Eddie Broker – Estrategia TAXI")

# 🕒 Hora actual en Colombia (refresca en cada render)
zona_col = pytz.timezone("America/Bogota")
ahora = datetime.now(zona_col).strftime("%H:%M:%S")
st.markdown(f"🕒 Hora Colombia actual: **{ahora}**")

# 📅 Validación de día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")

    # 🎯 Selector de activo y visualización en columnas
    col1, col2 = st.columns([1, 2])

    with col1:
        activo = selector_activo()

    with col2:
        mostrar_estrategia_taxi(activo)

else:
    st.warning("🚫 Hoy NO es un día operativo (ni COL ni NYSE).")
    modo_simulacion()
