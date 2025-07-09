# app.py

import streamlit as st
import time
from utils.horario import es_dia_operativo, obtener_hora_colombia
from utils.activos import selector_activo
from utils.noticias import obtener_noticias, generar_resumen_noticias
from utils.estrategia import generar_estrategia_taxi, tabla_taxi

st.set_page_config(layout="wide")
st.title("🤖 Eddie Broker – Estrategia TAXI")

# Mostrar hora actual
placeholder_hora = st.empty()
placeholder_hora.markdown(f"🕒 Hora Colombia actual: {obtener_hora_colombia().strftime('%H:%M:%S')}")

# Validar si es día operativo
operativo = es_dia_operativo()
if operativo:
    st.success("📈 Hoy es un día operativo (COL + NYSE).")
else:
    st.warning("🧪 Hoy no es un día operativo. Eddie está en modo simulación.")

# Selección de activos
st.markdown("### 🎯 Selección de Activos")
col1, col2 = st.columns(2)
with col1:
    activo1 = selector_activo("activo_1")
with col2:
    activo2 = selector_activo("activo_2")

# Noticias y bloques independientes por activo
col1, col2 = st.columns(2)

# Estado de simulación por activo
if 'simulando_1' not in st.session_state:
    st.session_state.simulando_1 = False
if 'simulando_2' not in st.session_state:
    st.session_state.simulando_2 = False

def render_activo_block(activo, slot, col):
    noticias = obtener_noticias(activo)
    with col:
        st.subheader(f"📰 Noticias recientes – {activo}")
        if noticias:
            for n in noticias:
                st.markdown(f"""
                **🗞️ {n['headline']}**  
                {n['summary']}  
                [🔗 Ver más]({n['url']})
                """)
        else:
            st.info("No se encontraron noticias recientes para este activo.")

        st.subheader("🧠 Resumen contextual de las noticias")
        resumen = generar_resumen_noticias(noticias)
        st.success(resumen)

        st.markdown(f"### ⏰ Fuera de horario TAXI para {activo}")
        if st.session_state[f'simulando_{slot}']:
            if st.button(f"🔴 Detener simulación para {activo}", key=f"stop_sim_{slot}"):
                st.session_state[f'simulando_{slot}'] = False
        else:
            if st.button(f"🟢 Iniciar simulación para {activo}", key=f"start_sim_{slot}"):
                st.session_state[f'simulando_{slot}'] = True

        mostrar_taxi = False
        hora_actual = obtener_hora_colombia().strftime("%H:%M:%S")
        if "10:59:00" <= hora_actual <= "11:05:00":
            st.markdown(f"## 🚕 TAXI OFICIAL – {activo}")
            mostrar_taxi = True
        elif st.session_state[f'simulando_{slot}']:
            st.markdown(f"## 🚕 TAXI (Demo) para {activo}")
            mostrar_taxi = True

        if mostrar_taxi:
            estr = generar_estrategia_taxi(activo)
            st.markdown(tabla_taxi(estr), unsafe_allow_html=True)

# Renderizar bloques para ambos activos
render_activo_block(activo1, 1, col1)
render_activo_block(activo2, 2, col2)


