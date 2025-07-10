import streamlit as st
from utils.estrategia import generar_estrategia_taxi, tabla_taxi
from utils.activos import lista_activos
from utils.indicadores import obtener_datos_tecnicos
from utils.horario import es_horario_operativo

st.set_page_config(page_title="Eddie Broker - TAXI", layout="wide")

st.title("🤖 Eddie Broker – Estrategia TAXI")

# Hora actual y validación operativa
from datetime import datetime
import pytz
hora_colombia = datetime.now(pytz.timezone("America/Bogota")).strftime("%H:%M:%S")
st.markdown(f"🕒 **Hora Colombia actual:** `{hora_colombia}`")

if es_horario_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.warning("⛔ Hoy no es un día operativo.")

# Selección de activos
col1, col2 = st.columns(2)
with col1:
    activo1 = st.selectbox("🎯 Selecciona activo 1:", lista_activos(), key="activo1")
with col2:
    activo2 = st.selectbox("🎯 Selecciona activo 2:", lista_activos(), key="activo2")

# Mostrar estrategia TAXI para cada activo
st.subheader("🚕 Estrategia TAXI (automática)")
col1, col2 = st.columns(2)

for col, activo in zip([col1, col2], [activo1, activo2]):
    with col:
        st.markdown(f"### 🚕 TAXI (Demo) para {activo}")

        datos = obtener_datos_tecnicos(activo)  # RSI, MACD, ATR, Precio, Spread, etc.

        # Simulamos tipo de orden automático (puede ser 'LIMIT' o 'MARKET')
        tipo_orden = "LIMIT" if datos['rsi'] > 50 else "MARKET"
        direccion = "LONG" if datos['rsi'] > 50 else "SHORT"

        estrategia = generar_estrategia_taxi(
            activo=activo,
            direccion=direccion,
            order_type=tipo_orden,
            precio=datos['precio'],
            spread=datos['spread'],
            capital_total=250
        )

        st.markdown(tabla_taxi(estrategia), unsafe_allow_html=True)

