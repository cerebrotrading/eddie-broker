# utils/noticias.py

import os
import requests
from openai import OpenAI

# API Key de OpenAI (asegúrate de haberla definido en Render como variable de entorno)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cliente OpenAI actualizado
client = OpenAI(api_key=OPENAI_API_KEY)

# API de noticias (puedes cambiarla si tienes otra fuente preferida)
def obtener_noticias(activo):
    try:
        # Puedes usar una API como Finnhub o una ficticia de prueba aquí
        # Este ejemplo usa datos mock por simplicidad
        noticias_mock = {
            "TSLA": [
                {
                    "headline": "Tesla Stock Bull Says 'Tesla Board Needs To Act Now'",
                    "summary": "Tesla cayó en la bolsa y analistas piden intervención de la junta directiva.",
                    "url": "https://example.com/tesla1"
                },
                {
                    "headline": "Tesla robotaxi stumble is a win for Lyft",
                    "summary": "El tropiezo de Tesla con su robotaxi impulsa a su competidor Lyft.",
                    "url": "https://example.com/tesla2"
                }
            ],
            "NVDA": [
                {
                    "headline": "Micron gana mercado tras retrasos de Nvidia",
                    "summary": "Micron captura participación tras problemas de suministro de Nvidia.",
                    "url": "https://example.com/nvda1"
                }
            ]
        }
        return noticias_mock.get(activo.upper(), [])
    except Exception as e:
        return []

# Generar resumen con OpenAI (usando SDK 1.x)
def generar_resumen_noticias(noticias):
    if not noticias:
        return "No hay n


