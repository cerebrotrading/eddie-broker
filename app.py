# app.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
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

# 🔄 Auto-recarga cada 5 segundos para mantener la hora viva
st_autorefresh(interval=5000, limit=None, key="auto_refresh")

# 🧠 Encabezado principal
st.title("🤖 Eddie Broker – Estrategia TAXI")

# ⏰ Hora en tiempo real
zona_col = pytz.timezone("America/Bogota")
hora_actual = datetime.now(zona_col).strftime("%H:%M:%S")
st.markdown(f"🕒 Hora Colombia actual: **{hora_actual}**")

# 📅 Día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")

    # 🎯 Activo
  
    activo = selector_activo()

    # 📈 Gráfico (pantalla completa)
    st.components.v1.html(
        f"""
        <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=NASDAQ:{activo}&interval=15&locale=es&theme=dark&height=400"
                width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
        """,
        height=420,
    )

    # 🚕 Estrategia TAXI (debajo del gráfico)
    st.markdown("---")
    mostrar_estrategia_taxi(activo)

else:
    st.warning("🚫 Hoy NO es un día operativo (ni COL ni NYSE).")
    modo_simulacion()

