# utils/noticias.py

# Simulador simple de noticias por activo sin necesidad de API

def obtener_noticias(activo):
    noticias_mock = {
        "TSLA": [
            {
                "headline": "Tesla cae tras decisiones políticas de Elon Musk",
                "summary": "Analistas piden intervención de la junta directiva de Tesla tras recientes movimientos políticos del CEO.",
                "url": "https://example.com/tsla1"
            },
            {
                "headline": "Tesla retrasa su robotaxi, oportunidad para Lyft",
                "summary": "El retraso en el lanzamiento del robotaxi de Tesla genera oportunidades de mercado para su competidor Lyft.",
                "url": "https://example.com/tsla2"
            }
        ],
        "NVDA": [
            {
                "headline": "Micron gana participación tras retrasos en Nvidia",
                "summary": "Micron se posiciona mejor en el mercado de chips frente a Nvidia, según analistas.",
                "url": "https://example.com/nvda1"
            }
        ]
    }

    return noticias_mock.get(activo.upper(), [])

def generar_resumen_noticias(noticias):
    if not noticias:
        return "No hay noticias para mostrar."
    
    resumen = "Resumen automático:\n\n"
    for n in noticias:
        resumen += f"• {n['headline']} – {n['summary']}\n"
    return resumen

