# utils/noticias.py

import os
import requests
from datetime import datetime, timedelta

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def obtener_noticias(activo, limite=5):
    """
    Trae las últimas noticias de Finnhub para el símbolo dado.
    """
    hoy = datetime.now().date()
    hace_3_dias = hoy - timedelta(days=3)

    url = "https://finnhub.io/api/v1/company-news"
    params = {
        "symbol": activo.upper(),
        "from": hace_3_dias.isoformat(),
        "to": hoy.isoformat(),
        "token": FINNHUB_API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return []

    data = resp.json()
    # Los primeros `limite` artículos
    return data[:limite]

def generar_resumen_noticias(noticias):
    """
    Genera un resumen simple de las noticias (sin IA).
    """
    if not noticias:
        return "No hay noticias para mostrar."
    líneas = []
    for n in noticias:
        título = n.get("headline", "")
        resumen = n.get("summary", "")
        líneas.append(f"• {título} – {resumen}")
    return "\n".join(líneas)

