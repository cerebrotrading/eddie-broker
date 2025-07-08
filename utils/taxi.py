# utils/taxi.py

import streamlit as st
from datetime import datetime
import pytz

def mostrar_estrategia_taxi(activo):
    st.markdown("### 🚕 Estrategia TAXI C.O.D.E v1.7.6")

    # Validar horario de ejecución (10:59 a 11:05 AM)
    zona_col = pytz.timezone("America/Bogota")
    ahora = datetime.now(zona_col).time()

    hora_inicio = datetime.strptime("10:59", "%H:%M").time()
    hora_fin = datetime.strptime("11:05", "%H:%M").time()

    if ahora < hora_inicio or ahora > hora_fin:
        st.warning("🚫 Fuera del horario de entrada permitido (10:59 AM a 11:05 AM).")
        return

    st.success(f"✅ Dentro del horario permitido. Preparando orden para: **{activo}**")

    # Parámetros de entrada (pueden venir de una API más adelante)
    entrada = st.number_input("Precio de Entrada ($)", value=158.00)
    stop_loss = st.number_input("Stop Loss ($)", value=154.00)
    tp1 = st.number_input("Take Profit 1 ($)", value=160.50)
    tp2 = st.number_input("Take Profit 2 ($)", value=164.00)

    capital_total = st.number_input("Capital disponible ($)", value=500)
    capital_entrada = capital_total / 2

    rrr_tp1 = round((tp1 - entrada) / (entrada - stop_loss), 2)
    rrr_tp2 = round((tp2 - entrada) / (entrada - stop_loss), 2)

    st.markdown(f"**Capital por entrada:** ${capital_entrada:.2f} (TP1 / TP2)")
    st.markdown(f"**RRR TP1:** {rrr_tp1} | **RRR TP2:** {rrr_tp2}")

    if st.button("📅 Confirmar entrada oficial"):
        st.success("🎉 Estrategia TAXI confirmada. Orden generada y registrada (simulada).")

def modo_simulacion():
    st.markdown("### 🎮 Modo Simulación Activado")
    st.info("Hoy no es día operativo. Puedes usar este modo para practicar sin riesgo.")

    activo = st.selectbox("Selecciona un activo para simular:", [
        "TSLA", "META", "AAPL", "EC", "AMD", "BA", "MSFT", "NVDA",
        "GOOGL", "INTC", "PYPL", "XOM", "DIS", "CRM", "BABA"
    ])

    precio_demo = st.slider("Simula un precio de entrada:", 50.0, 500.0, 100.0)
    st.markdown(f"Actuando como si entraras a **{activo}** a ${precio_demo:.2f} (modo demo)")

    if st.button("🔄 Simular estrategia"):
        st.success(f"Simulación ejecutada para {activo} con entrada en ${precio_demo:.2f} (ficticio).")
