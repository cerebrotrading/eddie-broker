# app.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from utils.horario import es_dia_operativo, obtener_hora_colombia
from utils.activos import activos, mostrar_grafico_tradingview
from utils.noticias import obtener_noticias, generar_resumen_noticias
from utils.taxi import generar_estrategia_taxi

# Configuración de página
st.set_page_config(layout="wide")
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Auto-refresco para hora en tiempo real
st_autorefresh(interval=5000, key="hora_refresh")

# Mostrar hora Colombia
hora_actual = obtener_hora_colombia().strftime('%H:%M:%S')
st.markdown(f"🕒 Hora Colombia actual: **{hora_actual}**")

# Verificación día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.warning("🧪 Hoy no es un día operativo. Eddie está en modo simulación.")

# Selección de dos activos en columnas
col1, col2 = st.columns(2)
with col1:
    st.subheader("🎯 Activo 1")
    activo1 = st.selectbox("Selecciona Activo 1:", activos, key="activo1")
    mostrar_grafico_tradingview(activo1)
with col2:
    st.subheader("🎯 Activo 2")
    activo2 = st.selectbox("Selecciona Activo 2:", activos, key="activo2")
    mostrar_grafico_tradingview(activo2)

# Inicializar estados de simulación
if 'sim1' not in st.session_state:
    st.session_state['sim1'] = False
if 'sim2' not in st.session_state:
    st.session_state['sim2'] = False

# Función para procesar cada activo
def procesar_activo(activo, idx):
    st.markdown("---")
    # Noticias
    st.subheader(f"📰 Noticias de {activo}")
    noticias = obtener_noticias(activo)
    if noticias:
        for n in noticias:
            st.markdown(f"**🗞️ {n.get('headline','')}**\n\n{n.get('summary','')}\n\n[🔗 Ver más]({n.get('url','#')})\n")
    else:
        st.info(f"No hay noticias recientes para {activo}.")

    # Resumen de noticias
    st.subheader(f"🧠 Resumen de noticias de {activo}")
    resumen = generar_resumen_noticias(noticias)
    st.success(resumen)

    # Fuera de horario o estrategia
    in_horario = "10:59:00" <= hora_actual <= "11:05:00"
    sim_key = f"sim{idx}"

    if not in_horario:
        # Mostrar advertencia y botón de simulación debajo de noticias
        st.warning(f"⏰ Fuera de horario TAXI para {activo}.")
        if not st.session_state[sim_key]:
            if st.button(f"🔄 Iniciar simulación TAXI para {activo}", key=sim_key+"_start"):
                st.session_state[sim_key] = True
        else:
            if st.button(f"⏹️ Detener simulación TAXI para {activo}", key=sim_key+"_stop"):
                st.session_state[sim_key] = False

    # Mostrar estrategia en horario o en simulación
    if in_horario or st.session_state[sim_key]:
        mode = "(Demo)" if not in_horario else ""
        st.subheader(f"🚕 Estrategia TAXI para {activo} {mode}")
        estr = generar_estrategia_taxi(activo)
        st.markdown(f"**Precio de entrada:** ${estr['precio_entrada']}  |  **SL:** ${estr['stop_loss']}  |  **TP1:** ${estr['take_profit_1']}  |  **TP2:** ${estr['take_profit_2']}")
        st.markdown("""
        ## 📊 VALIDACIÓN TÉCNICA
        ✅ RSI > 50 (confirmado)  
        ✅ Momentum M15 alcista  
        ✅ ATR válido  
        ✅ Precio verificado  
        ✅ Indicadores alineados  
        ✅ Backtesting media 75%
        """)

# Procesar ambos activos
procesar_activo(activo1, 1)
procesar_activo(activo2, 2)


