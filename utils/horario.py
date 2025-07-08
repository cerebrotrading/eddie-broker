# utils/horario.py

from datetime import datetime
import pytz
import holidays

def obtener_hora_colombia():
    tz = pytz.timezone("America/Bogota")
    return datetime.now(tz)

def es_dia_operativo():
    tz = pytz.timezone("America/Bogota")
    hoy = datetime.now(tz).date()

    festivos_col = holidays.CountryHoliday('CO', years=hoy.year)
    festivos_usa = holidays.CountryHoliday('US', years=hoy.year)

    es_laborable = hoy.weekday() < 5  # Lunes a Viernes (0 a 4)
    no_es_festivo = hoy not in festivos_col and hoy not in festivos_usa

    return es_laborable and no_es_festivo
