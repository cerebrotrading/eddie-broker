# app.py

import streamlit as st
import time
from datetime import datetime
from utils.horario import es_dia_operativo, obtener_hora_colombia
from utils.taxi import mostrar_estrategia_taxi, modo_simulacion
from utils.noticias import obtener_noticias

st.set_page_config(page_title="Eddie Broker", layout="wide")
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Mostrar hora Colombia en tiempo real
hora_placeholder = st.empty()

hora_actual = obtener_hora_colombia().strftime("%H:%M:%S")
hora_placeholder.markdown(f"🕒 **Hora Colombia actual:** `{hora_actual}`")

# Día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.warning("📉 Hoy NO es un día operativo. Modo simulación activo.")

# Selector de activos
st.markdown("## 🎯 Selección de activo")
lista_activos = ["TSLA", "META", "AAPL", "EC", "AMD", "BA", "MSFT", "NVDA", "GOOGL", "INTC", "PYPL", "XOM", "DIS", "CRM", "BABA"]
activo_seleccionado = st.selectbox("Elige el activo para visualizar y aplicar la estrategia:", lista_activos)

# Gráfico de TradingView
st.markdown("---")
st.markdown("## 📈 Gráfico del activo seleccionado")
st.components.v1.html(f'''
    <div style="height:500px">
    <iframe
      src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{activo_seleccionado}&symbol=NASDAQ%3A{activo_seleccionado}&interval=15&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=America%2FBogota&withdateranges=1&hideideas=1&hidelegend=0&enable_publishing=false"
      width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no">
    </iframe>
    </div>
''', height=500)

# Noticias recientes
st.markdown("## 📰 Noticias recientes")
noticias = obtener_noticias(activo_seleccionado)

if noticias:
    for noticia in noticias:
        st.markdown(f"**🗞️ {noticia.get('headline', 'Sin título')}**")
        st.markdown(f"{noticia.get('summary', '')}")
        if 'url' in noticia:
            st.markdown(f"[🔗 Ver más]({noticia['url']})")
        st.markdown("---")
else:
    st.info("No hay noticias recientes disponibles para este activo.")

# Estrategia
hora_actual_obj = obtener_hora_colombia()
if es_dia_operativo():
    if hora_actual_obj.strftime("%H:%M") >= "10:59" and hora_actual_obj.strftime("%H:%M") <= "11:05":
        mostrar_estrategia_taxi(activo_seleccionado)
    else:
        st.warning("🚫 Fuera del horario de entrada permitido (10:59 AM a 11:05 AM).")
else:
    modo_simulacion()


