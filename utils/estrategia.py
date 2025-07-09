import random

# Simulación simple de osciladores (esto será reemplazado por datos reales luego)
def evaluar_osciladores(activo):
    return {
        "rsi": "RSI > 50",
        "macd": "MACD+",
        "ema": "EMA 8/21",
        "volumen": "Volumen creciente",
        "atr": "ATR suficiente",
    }

def generar_estrategia_taxi(activo):
    # 🔢 Parámetros base
    precio_actual = obtener_precio_real_simulado(activo)
    importe_total = 250
    importe_tp = 125
    max_perdida_usd = 12.5  # SL monetario
    tipo_orden = random.choice(["LIMIT", "MARKET"])
    spread = round(random.uniform(0.05, 0.20), 2)

    # 🧮 Precio de entrada
    entrada = precio_actual + spread if tipo_orden == "LIMIT" else precio_actual

    # 📉 SL (en precio): pérdida de $12.5
    unidades = round(importe_tp / entrada, 2)
    sl_dinero = importe_tp - max_perdida_usd
    sl_precio = round(sl_dinero / unidades, 2)

    # 🎯 TP1 y TP2: definidos por RRR (ejemplo 1.2x y 1.6x)
    tp1_dinero = importe_tp + round(max_perdida_usd * 1.2, 2)
    tp2_dinero = importe_tp + round(max_perdida_usd * 1.6, 2)
    tp1_precio = round(tp1_dinero / unidades, 2)
    tp2_precio = round(tp2_dinero / unidades, 2)

    # 📊 Osciladores técnicos (mock)
    osciladores = evaluar_osciladores(activo)

    return {
        "activo": activo,
        "tipo_operacion": "LONG",  # Por ahora fijo
        "tipo_orden": tipo_orden,
        "importe": importe_tp,
        "entrada": round(entrada, 2),
        "sl_precio": sl_precio,
        "tp1_precio": tp1_precio,
        "tp2_precio": tp2_precio,
        "unidades": unidades,
        "osciladores": ", ".join(osciladores.values()),
        "spread": spread
    }

def tabla_taxi(estr):
    return f"""
🚕 TAXI (Demo) para {estr['activo']}
| 📈 Campo                | {estr['activo']} |
|------------------------|------------------|
| 📈 Tipo de operación    | {estr['tipo_operacion']} |
| ⚙️ Tipo de orden        | {estr['tipo_orden']} |
| 💵 Importe autorizado   | ${estr['importe']} |
| 🎯 Entrada (precio)     | ${estr['entrada']} |
| ⛔ SL (precio estimado) | ${estr['sl_precio']} |
| 🎯 TP1 (precio estimado)| ${estr['tp1_precio']} |
| 🎯 TP2 (precio estimado)| ${estr['tp2_precio']} |
| 📊 Unidades compradas   | {estr['unidades']} |
| 🧠 Osciladores          | {estr['osciladores']} |
| 🔍 Spread aplicado      | {estr['spread']} |
"""

def obtener_precio_real_simulado(activo):
    precios = {
        "TSLA": 298.00,
        "META": 320.10,
        "NVDA": 124.50,
        "AMD": 136.80,
        "AAPL": 195.40,
        "BA": 203.50,
        "MSFT": 445.20,
        "KO": 61.25,
        "EC": 11.50,
        "CRM": 220.90,
        "PYPL": 70.60
    }
    return precios.get(activo.upper(), round(random.uniform(100, 400), 2))
