import streamlit as st
import datetime
from utils.activos import obtener_lista_activos
from utils.horario import es_dia_operativo, obtener_hora_colombia, dentro_ventana_taxi
from utils.estrategia import generar_estrategia_taxi, tabla_taxi
from utils.noticias import obtener_noticias, generar_resumen_noticias
from utils.indicadores import obtener_datos_activo
from utils.taxi import selector_activo, mostrar_grafico_tradingview

st.set_page_config(page_title="🧠 Eddie Paper Broker", layout="wide")
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Mostrar hora y validación operativa
hora_col = obtener_hora_colombia()
es_operativo = es_dia_operativo()
es_ventana_taxi = dentro_ventana_taxi()

st.markdown(f"🕒 Hora Colombia actual: **{hora_col.strftime('%H:%M:%S')}**")
if es_operativo:
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.error("⛔ Hoy NO es un día operativo (festivo COL o NYSE)")

st.subheader("🎯 Selección de Activos")
col1, col2 = st.columns(2)

with col1:
    activo1 = selector_activo("activo_1")
with col2:
    activo2 = selector_activo("activo_2")

col1, col2 = st.columns(2)
with col1:
    mostrar_grafico_tradingview(activo1)
with col2:
    mostrar_grafico_tradingview(activo2)

st.subheader("🗞️ Noticias Relevantes")
col1, col2 = st.columns(2)
with col1:
    noticias1 = obtener_noticias(activo1)
    for n in noticias1:
        st.markdown(f"**🗞️ {n['headline']}**\n{n['summary'][:150]}...")
with col2:
    noticias2 = obtener_noticias(activo2)
    for n in noticias2:
        st.markdown(f"**🗞️ {n['headline']}**\n{n['summary'][:150]}...")

# --- BLOQUE ESTRATEGIA ---
st.subheader("🚕 Estrategia TAXI")

col1, col2 = st.columns(2)
for idx, activo in enumerate([activo1, activo2]):
    with [col1, col2][idx]:
        if es_ventana_taxi:
            estrategia = generar_estrategia_taxi(activo)
            st.markdown(tabla_taxi(estrategia), unsafe_allow_html=True)
        else:
            st.warning(f"⏰ Fuera de horario TAXI para {activo}")
            if st.button(f"🚕 Iniciar simulación para {activo}", key=f"sim_{idx}"):
                estrategia = generar_estrategia_taxi(activo)
                st.markdown(tabla_taxi(estrategia), unsafe_allow_html=True)
                st.button(f"🛑 Detener simulación {activo}", key=f"stop_{idx}")

