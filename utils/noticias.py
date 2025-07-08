# app.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from utils.horario import es_dia_operativo, obtener_hora_colombia
from utils.activos import selector_activo
from utils.taxi import generar_estrategia_taxi
from utils.noticias import obtener_noticias, generar_resumen_noticias

# Configuración de página
st.set_page_config(layout="wide")
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Auto-refresco para hora en tiempo real
st_autorefresh(interval=5000, key="hora_refresh")

# Mostrar hora Colombia
hora_actual_dt = obtener_hora_colombia()
hora_actual = hora_actual_dt.strftime('%H:%M:%S')
st.markdown(f"🕒 Hora Colombia actual: **{hora_actual}**")

# Verificación día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.warning("🧪 Hoy no es un día operativo. Eddie está en modo simulación.")

# Selección de dos activos
st.subheader("🎯 Selección de activos")
col1, col2 = st.columns(2)
with col1:
    activo1 = selector_activo(label="Activo 1")
with col2:
    activo2 = selector_activo(label="Activo 2")

# Función para procesar cada activo
def procesar_activo(activo):
    st.markdown(f"---\n## 📈 {activo} - Gráfico")
    # El selector ya mostró el gráfico; si no, llamar de nuevo
    # Noticias
    st.markdown(f"## 📰 Noticias de {activo}")
    noticias = obtener_noticias(activo)
    if noticias:
        for n in noticias:
            st.markdown(f"**🗞️ {n.get('headline','')}**\n\n{n.get('summary','')}\n\n[🔗 Ver más]({n.get('url','#')})\n")
    else:
        st.info(f"No hay noticias recientes para {activo}.")
    # Resumen
    st.markdown(f"## 🧠 Resumen contextual de {activo}")
    resumen = generar_resumen_noticias(noticias)
    st.success(resumen)
    # Estrategia TAXI si está en horario
    if "10:59:00" <= hora_actual <= "11:05:00":
        st.markdown(f"## 🚕 Estrategia TAXI para {activo}")
        estr = generar_estrategia_taxi(activo)
        st.markdown(f"**Precio de entrada:** ${estr['precio_entrada']}  |  **SL:** ${estr['stop_loss']}  |  **TP1:** ${estr['take_profit_1']}  |  **TP2:** ${estr['take_profit_2']}")
    else:
        st.warning(f"⏰ Fuera de horario TAXI para {activo}.")

# Procesar ambos activos
procesar_activo(activo1)
procesar_activo(activo2)

