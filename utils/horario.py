# utils/horario.py

from datetime import datetime
import pytz
from workalendar.america import Colombia
from workalendar.usa import UnitedStates

def obtener_hora_colombia():
    zona_col = pytz.timezone("America/Bogota")
    ahora = datetime.now(zona_col)
    return ahora.strftime("%H:%M:%S")

def es_dia_operativo():
    hoy = datetime.now().date()
    cal_col = Colombia()
    cal_usa = UnitedStates()
    es_laboral_col = cal_col.is_working_day(hoy)
    es_laboral_usa = cal_usa.is_working_day(hoy)
    return es_laboral_col and es_laboral_usa
