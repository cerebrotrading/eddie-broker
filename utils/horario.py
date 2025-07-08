# utils/horario.py

from datetime import datetime
from workalendar.america import Colombia
from pandas.tseries.holiday import USFederalHolidayCalendar
import pytz
import pandas as pd
import streamlit as st

def mostrar_hora_colombia():
    zona_col = pytz.timezone("America/Bogota")
    ahora = datetime.now(zona_col).strftime("%H:%M:%S")
    st.markdown(f"🕒 **Hora Colombia actual:** `{ahora}`")

def es_dia_operativo():
    cal_col = Colombia()
    zona_col = pytz.timezone("America/Bogota")
    hoy = datetime.now(zona_col).date()

    cal_usa = USFederalHolidayCalendar()
    feriados_usa = cal_usa.holidays(start=hoy, end=hoy + pd.Timedelta(days=1))

    es_col = cal_col.is_working_day(hoy)
    es_usa = hoy.weekday() < 5 and hoy not in feriados_usa

    return es_col and es_usa
