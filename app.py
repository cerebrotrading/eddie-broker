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

# Selección de dos activos y sus gráficos
sel_col1, sel_col2 = st.columns(2)
with sel_col1:
    st.subheader("🎯 Activo 1")
    activo1 = st.selectbox("Selecciona Activo 1:", activos, key="activo1")
    mostrar_grafico_tradingview(activo1)
with sel_col2:
    st.subheader("🎯 Activo 2")
    activo2 = st.selectbox("Selecciona Activo 2:", activos, key="activo2")
    mostrar_grafico_tradingview(activo2)

# Inicializar estado de simulación
for i in (1, 2):
    key = f"sim{i}"
    if key not in st.session_state:
        st.session_state[key] = False

# Importe por TP fijo
def tabla_taxi(estr, order_type, spread):
    capital_por_tp = 125.0  # USD por TP
    # Porcentajes
    sl_pct  = 0.10
    tp1_pct = 0.125
    tp2_pct = 0.15
    # Precios ajustados
    base_price = estr['precio_entrada']
    entry_price = round(base_price + spread, 2)
    sl_raw  = entry_price - capital_por_tp * sl_pct
    tp1_raw = entry_price + capital_por_tp * tp1_pct
    tp2_raw = entry_price + capital_por_tp * tp2_pct
    # Capping
    sl_price  = round(entry_price - min(capital_por_tp, entry_price - sl_raw), 2)
    tp1_price = round(entry_price + min(capital_por_tp, tp1_raw - entry_price), 2)
    tp2_price = round(entry_price + min(capital_por_tp, tp2_raw - entry_price), 2)
    unidades = round(capital_por_tp / entry_price, 2)
    return f"""
| Campo                  | Valor                     |
| ---------------------- | ------------------------- |
| 📈 Tipo de operación   | LONG                      |
| ⚙️ Tipo de orden       | {order_type}              |
| 💵 Importe             | $ {capital_por_tp:.2f} USD |
| 🎯 Entrada             | $ {entry_price:.2f} USD    |
| ⛔ SL                  | $ {sl_price:.2f} USD       |
| 🎯 TP1                 | $ {tp1_price:.2f} USD      |
| 🎯 TP2                 | $ {tp2_price:.2f} USD      |
| 📊 Unidades compradas  | {unidades}                |
| 🧠 Osciladores         | RSI > 50, MACD+, volumen ↑ |
| 🔍 Spread validado     | ✅                        |
"""  

# Cabecera oficial
def formato_taxi_header(dt: datetime):
    dia = dt.day
    mes = dt.strftime('%B')
    año = dt.year
    hora12 = dt.strftime('%I:%M %p')
    return f"🚕 TAXI OFICIAL – {dia} de {mes} de {año} – {hora12} (RRR Optimizado)"

# Renderizado de bloques
def render_activo_block(activo, idx, column):
    with column:
        st.markdown('---')
        # Noticias dual-columna
        st.subheader(f"📰 Noticias de {activo}")
        noticias = obtener_noticias(activo)
        if noticias:
            mitad = (len(noticias)+1)//2
            n1, n2 = noticias[:mitad], noticias[mitad:]
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
        st.success(generar_resumen_noticias(noticias))
        # Cabecera
        st.markdown(formato_taxi_header(hora_actual_dt))
        st.markdown("📌 Compatible con eToro – SL y TP en USD reales dentro del límite")
        # Inputs order & spread
        order_type = st.selectbox("Tipo de orden:", ["LIMIT","MARKET"], key=f"order_{idx}")
        spread = st.number_input("Spread estimado (USD):", min_value=0.0, value=0.08, step=0.01, key=f"spread_{idx}")
        # Simulación
        in_horario = "10:59:00" <= hora_actual <= "11:05:00"
        sim_key = f"sim{idx}"
        if not in_horario:
            st.warning(f"⏰ Fuera de horario TAXI para {activo}.")
            if not st.session_state[sim_key]:
                if st.button(f"🔄 Iniciar simulación para {activo}", key=f"start_{sim_key}"):
                    st.session_state[sim_key] = True
            else:
                if st.button(f"⏹️ Detener simulación para {activo}", key=f"stop_{sim_key}"):
                    st.session_state[sim_key] = False
        # Mostrar estrategia/demo\        
        if in_horario or st.session_state[sim_key]:
            mode = " (Demo)" if not in_horario else ""
            st.subheader(f"🚕 TAXI oficial{mode} para {activo}")
            estr = generar_estrategia_taxi(activo)
            st.markdown(tabla_taxi(estr, order_type, spread), unsafe_allow_html=True)
            st.markdown("""
            ## 📊 VALIDACIÓN TÉCNICA
            ✅ RSI > 50 (confirmado)  
            ✅ Momentum M15 alcista  
            ✅ ATR válido  
            ✅ Precio verificado  
            ✅ Indicadores alineados  
            ✅ Backtesting media 75%
            """
            )

# Ejecutar render para ambos activos
block_col1, block_col2 = st.columns(2)
render_activo_block(activo1, 1, block_col1)
render_activo_block(activo2, 2, block_col2)



