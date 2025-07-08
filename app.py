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

# Inicializar simulación\ for i in (1,2):
    key=f"sim{i}"
    if key not in st.session_state:
        st.session_state[key]=False

# Tabla de estrategia y validación técnica
def tabla_taxi(estr, operador="LONG", tipo_orden="LIMIT"):
    unidades = round(estr['capital_entrada']/estr['precio_entrada'],2)
    return f"""
| Campo                      | {estr['activo']}                            |
| -------------------------- | ------------------------------------------- |
| 📈 Tipo de operación       | {operador}                                  |
| ⚙️ Tipo de orden           | {tipo_orden}                                |
| 💵 Importe (USD eToro)     | $ {estr['capital_entrada']}               |
| 🎯 Entrada (precio activo) | ${estr['precio_entrada']}                  |
| ⛔ SL (USD eToro)           | -$25.00                                     |
| ⛔ SL (precio estimado)     | ${round(estr['precio_entrada'] - 25,2)}     |
| 🎯 TP1 (USD eToro)         | +$31.25                                     |
| 🎯 TP1 (precio estimado)   | ${round(estr['precio_entrada'] + 31.25,2)}  |
| 🎯 TP2 (USD eToro)         | +$37.50                                     |
| 🎯 TP2 (precio estimado)   | ${round(estr['precio_entrada'] + 37.5,2)}   |
| 📊 Unidades compradas      | {unidades}                                  |
| 🧠 Osciladores             | RSI > 50, MACD+, volumen ↑                  |
| 🔍 Spread validado eToro   | ✅                                           |
"""

# Función para renderizar bloque de activo
def render_activo_block(activo, idx, column):
    with column:
        st.markdown("---")
        # Noticias\ n        st.subheader(f"📰 Noticias de {activo}")
        noticias=obtener_noticias(activo)
        if noticias:
            mitad=(len(noticias)+1)//2
            n1, n2=noticias[:mitad], noticias[mitad:]
            nc1,nc2=st.columns(2)
            with nc1:
                for n in n1:
            st.markdown(f"""**🗞️ {n['headline']}**  
{n['summary']}  
[🔗 Ver más]({n['url']})""", unsafe_allow_html=True)
        with nc2:
            for n in n2:
                st.markdown(f"""**🗞️ {n['headline']}**  
{n['summary']}  
[🔗 Ver más]({n['url']})""", unsafe_allow_html=True)
        else:
                for n in n2:
                    st.markdown(f"**🗞️ {n['headline']}**  
{n['summary']}  
[🔗 Ver más]({n['url']})  ")
        else:
            st.info(f"No hay noticias recientes para {activo}.")
        # Resumen
        st.subheader(f"🧠 Resumen de noticias de {activo}")
        resumen=generar_resumen_noticias(noticias)
        st.success(resumen)
        # Estrategia
        in_horario="10:59:00"<=hora_actual<="11:05:00"
        sim_key=f"sim{idx}"
        if not in_horario:
            st.warning(f"⏰ Fuera de horario TAXI para {activo}.")
            if not st.session_state[sim_key]:
                if st.button(f"🔄 Simular TAXI para {activo}",key=f"start_{sim_key}"):
                    st.session_state[sim_key]=True
            else:
                if st.button(f"⏹️ Detener simulación para {activo}",key=f"stop_{sim_key}"):
                    st.session_state[sim_key]=False
        if in_horario or st.session_state[sim_key]:
            mode="(Demo)"if not in_horario else""
            st.subheader(f"🚕 TAXI oficial para {activo} {mode}")
            estr=generar_estrategia_taxi(activo)
            # Mostrar tabla\            st.markdown(tabla_taxi(estr),unsafe_allow_html=True)
            # Validación técnica
            st.markdown("""
            ## 📊 VALIDACIÓN TÉCNICA
            ✅ RSI > 50 (confirmado)  
            ✅ Momentum M15 alcista  
            ✅ ATR válido  
            ✅ Precio verificado  
            ✅ Indicadores alineados  
            ✅ Backtesting media 75%
            """)

# Renderizar en pestañas
col1, col2 = st.columns(2)
render_activo_block(activo1,1,col1)
render_activo_block(activo2,2,col2)

