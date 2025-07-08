# app.py

import streamlit as st
from utils.horario import mostrar_hora_colombia, es_dia_operativo

# Configuración general
st.set_page_config(page_title="Eddie Broker", layout="centered")
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Paso 1: Mostrar hora
mostrar_hora_colombia()

# Paso 2: Validar día operativo
if es_dia_operativo():
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
    st.markdown("> Aún no se ha cargado el selector de activos ni estrategia.")
else:
    st.warning("⛔ Hoy no es día operativo (COL o NYSE cerrado).")
    st.markdown("> Activado modo simulación (aún no implementado).")
