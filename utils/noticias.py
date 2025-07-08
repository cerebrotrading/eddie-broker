# utils/noticias.py

import requests
import os
from datetime import datetime, timedelta

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def obtener_noticias(activo, limite=5):
    hoy = datetime.now().date()
    hace_3_dias = hoy - timedelta(days=3)

    url = f"https://finnhub.io/api/v1/company-news"
    params = {
        "symbol": activo.upper(),
        "from": hace_3_dias.isoformat(),
        "to": hoy.isoformat(),
        "token": FINNHUB_API_KEY
    }

    try:
        resp = requests.get(url, params=params)
        data = resp.json()

        noticias_filtradas = data[:limite]
        return noticias_filtradas

    except Exception as e:
        return [{"headline": "No se pudieron cargar noticias", "summary": str(e)}]
