import streamlit as st
from utils.horario import es_dia_operativo, obtener_hora_colombia
from utils.activos import selector_activo
from utils.estrategia import generar_estrategia_taxi, tabla_taxi

# Configuracion de la app
st.set_page_config(layout="wide")
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Mostrar hora actual en Colombia
hora_col = obtener_hora_colombia().strftime("%H:%M:%S")
st.markdown(f"🕒 Hora Colombia actual: **{hora_col}**")

# Validar si es dia operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.warning("🧪 Hoy no es un día operativo. Eddie está en modo simulación.")

# Selección de dos activos
st.markdown("### 🌟 Selección de Activos")
col1, col2 = st.columns(2)

with col1:
    activo1 = selector_activo("activo_1")
with col2:
    activo2 = selector_activo("activo_2")

# Mostrar estrategia para ambos activos
def render_taxi_para_activo(nombre_activo, numero):
    st.subheader(f"🚕 TAXI oficial (Demo) para {nombre_activo}")
    estrategia = generar_estrategia_taxi(nombre_activo)
    tabla = tabla_taxi(estrategia)
    st.markdown(tabla, unsafe_allow_html=True)

st.divider()
st.markdown("### 💎 Estrategia TAXI Generada")

col1, col2 = st.columns(2)

with col1:
    render_taxi_para_activo(activo1, 1)

with col2:
    render_taxi_para_activo(activo2, 2)

