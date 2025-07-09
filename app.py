import streamlit as st
import streamlit.components.v1 as components

# 🔁 Función para mapear activo al símbolo de TradingView
def obtener_simbolo_tradingview(activo):
    nyse = ["BA", "XOM", "DIS", "CRM", "BABA", "KO", "EC"]  # Puedes ampliar esta lista si hay más
    if activo in nyse:
        return f"NYSE:{activo}"
    else:
        return f"NASDAQ:{activo}"

# 📊 Función para mostrar el gráfico del activo seleccionado
def mostrar_grafico_tradingview(activo):
    symbol = obtener_simbolo_tradingview(activo)
    
    # 🔍 HTML embebido del widget de TradingView
    iframe = f"""
    <iframe 
        src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval=15&symboledit=1&saveimage=1&toolbarbg=F1F3F6&studies=[]&theme=Dark&style=1&timezone=Etc/UTC&withdateranges=1&hideideas=1&studies_overrides={{}}"
        width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no">
    </iframe>
    """

    # 📍 Insertar en la app
    components.html(iframe, height=400)

# 🧪 Ejemplo de uso:
# activo = "BA"  # Puedes reemplazar esto con tu selector
# mostrar_grafico_tradingview(activo)

