# utils/activos.py

import streamlit as st

# Lista de activos permitidos para estrategia TAXI
activos = [
    "TSLA", "META", "AAPL", "EC", "AMD", "BA", "MSFT", "NVDA",
    "GOOGL", "INTC", "PYPL", "XOM", "DIS", "CRM", "BABA"
]

def selector_activo():
    st.markdown("### 🎯 Selección de activo")
    activo = st.selectbox("Elige el activo para visualizar y aplicar la estrategia:", activos)
    mostrar_grafico_tradingview(activo)
    return activo

def mostrar_grafico_tradingview(activo):
    symbol = f"NASDAQ:{activo}" if activo != "EC" else "NYSE:EC"
    st.markdown(f"""
        <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_candles&symbol={symbol}&interval=15&theme=dark&style=1&locale=es&toolbar_bg=f1f3f6&hide_top_toolbar=true&hide_side_toolbar=false&allow_symbol_change=true&details=true"
            width="100%" height="450" frameborder="0" allowtransparency="true" scrolling="no">
        </iframe>
    """, unsafe_allow_html=True)
