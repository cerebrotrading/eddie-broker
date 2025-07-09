import streamlit as st

# Lista de activos permitidos para estrategia TAXI
activos = [
    "TSLA", "META", "AAPL", "EC", "AMD", "BA", "MSFT", "NVDA",
    "GOOGL", "INTC", "PYPL", "XOM", "DIS", "CRM", "BABA"
]

def selector_activo(key_suffix=""):
    st.markdown("### 🎯 Selección de activo")
    activo = st.selectbox(
        "Elige el activo para visualizar y aplicar la estrategia:",
        activos,
        key=f"activo_selector_{key_suffix}"
    )
    mostrar_grafico_tradingview(activo, key_suffix)
    return activo

def mostrar_grafico_tradingview(activo, key_suffix=""):
    symbol = f"NASDAQ:{activo}" if activo != "EC" else "NYSE:EC"
    st.markdown(f"""
        <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{key_suffix}&symbol={symbol}&interval=15&theme=dark&style=1&locale=es&toolbar_bg=f1f3f6&hide_top_toolbar=true&hide_side_toolbar=false&allow_symbol_change=true&details=true"
            width="100%" height="450" frameborder="0" allowtransparency="true" scrolling="no">
        </iframe>
    """, unsafe_allow_html=True)
