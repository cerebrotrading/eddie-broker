# utils/noticias.py

import requests
import os
from datetime import datetime, timedelta
import openai

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

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
        return data[:limite]

    except Exception as e:
        return [{"headline": "No se pudieron cargar noticias", "summary": str(e)}]

def generar_resumen_noticias(noticias):
    if not noticias or not isinstance(noticias, list):
        return "No hay suficientes noticias para generar un resumen."

    contenido = "\n\n".join([
        f"Titular: {n.get('headline', '')}\nResumen: {n.get('summary', '')}" for n in noticias
    ])

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un analista financiero que resume noticias del mercado."},
                {"role": "user", "content": f"Resume brevemente el contexto general de estas noticias sobre el activo:\n\n{contenido}"}
            ],
            max_tokens=200
        )
        return respuesta.choices[0].message.content.strip()

    except Exception as e:
        return f"Error al generar resumen: {str(e)}"

