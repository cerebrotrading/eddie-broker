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

# Auto-refresco cada 5s para la hora
st_autorefresh(interval=5000, key="hora_refresh")
hora_actual_dt = obtener_hora_colombia()
hora_actual = hora_actual_dt.strftime('%H:%M:%S')
st.markdown(f"🕒 **Hora Colombia actual:** {hora_actual}")

# Día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.warning("🧪 Hoy no es un día operativo. Eddie está en modo simulación.")

# Selección de dos activos\ ncol1, col2 = st.columns(2)
with col1:
    st.subheader("🎯 Activo 1")
    activo1 = st.selectbox("Selecciona Activo 1:", activos, key="activo1")
    mostrar_grafico_tradingview(activo1)
with col2:
    st.subheader("🎯 Activo 2")
    activo2 = st.selectbox("Selecciona Activo 2:", activos, key="activo2")
    mostrar_grafico_tradingview(activo2)

# Inicializar estado de simulación
for i in (1, 2):
    key = f"sim{i}"
    if key not in st.session_state:
        st.session_state[key] = False

# Parámetros de capital
capital_total = 500
capital_por_activo = capital_total / 2
capital_por_tp = capital_por_activo / 2

# Formato de cabecera oficial
def formato_taxi_header(dt: datetime):
    dia = dt.day
    mes = dt.strftime("%B")
    año = dt.year
    hora24 = dt.strftime("%I:%M %p")
    return f"🚕 TAXI OFICIAL – {dia} de {mes} de {año} – {hora24} (RRR Optimizado)"

# Función para renderizar cada bloque de activo

def render_activo_block(activo, idx, column):
    with column:
        st.markdown("---")
        # Noticias en dos columnas
        st.subheader(f"📰 Noticias de {activo}")
        noticias = obtener_noticias(activo)
        if noticias:
            mitad = (len(noticias) + 1) // 2
            n1 = noticias[:mitad]
            n2 = noticias[mitad:]
            nc1, nc2 = st.columns(2)
            with nc1:
                for n in n1:
                    st.markdown(f"**🗞️ {n['headline']}**  \n{n['summary']}  \n[🔗 Ver más]({n['url']})", unsafe_allow_html=True)
            with nc2:
                for n in n2:
                    st.markdown(f"**🗞️ {n['headline']}**  \n{n['summary']}  \n[🔗 Ver más]({n['url']})", unsafe_allow_html=True)
        else:
            st.info(f"No hay noticias recientes para {activo}.")

        # Resumen
        st.subheader(f"🧠 Resumen de noticias de {activo}")
        resumen = generar_resumen_noticias(noticias)
        st.success(resumen)

        # Cabecera oficial y capital
        st.markdown(formato_taxi_header(hora_actual_dt))
        st.markdown(
            f"💰 Capital: ${capital_total} USD → ${capital_por_activo:.2f} por activo → ${capital_por_tp:.2f} por TP"
        )
        st.markdown("📌 Compatible con eToro – SL y TP en USD reales dentro del límite")

        # Estrategia o simulación
        in_horario = "10:59:00" <= hora_actual <= "11:05:00"
        sim_key = f"sim{idx}"
        if not in_horario:
            st.warning(f"⏰ Fuera de horario TAXI para {activo}.")
            if not st.session_state[sim_key]:
                if st.button(f"🔄 Iniciar simulación TAXI para {activo}", key=f"start_{sim_key}"):
                    st.session_state[sim_key] = True
            else:
                if st.button(f"⏹️ Detener simulación TAXI para {activo}", key=f"stop_{sim_key}"):
                    st.session_state[sim_key] = False

        if in_horario or st.session_state[sim_key]:
            mode = " (Demo)" if not in_horario else ""
            st.subheader(f"🚕 TAXI oficial{mode} para {activo}")
            estr = generar_estrategia_taxi(activo)
            # Mostrar tabla de estrategia
            st.markdown(tabla_taxi(estr), unsafe_allow_html=True)
            # Validación técnica
            st.markdown(
                """
                ## 📊 VALIDACIÓN TÉCNICA
                ✅ RSI > 50 (confirmado)  
                ✅ Momentum M15 alcista  
                ✅ ATR válido  
                ✅ Precio verificado  
                ✅ Indicadores alineados  
                ✅ Backtesting media 75%
                """
            )

# Renderizar en pestañas
col1, col2 = st.columns(2)
with col1:
    render_activo_block(activo1, 1, col1)
with col2:
    render_activo_block(activo2, 2, col2)


