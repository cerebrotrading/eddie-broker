# utils/estrategia.py
import random

def calcular_tp_sl(precio_entrada, direccion, spread=0.1):
    importe = 125  # USD fijos por TP
    perdida_maxima = 12.5  # 10% de 125

    if direccion == "LONG":
        sl = precio_entrada - (perdida_maxima / (importe / precio_entrada))
        tp1 = precio_entrada + (20 / (importe / precio_entrada))
        tp2 = precio_entrada + (30 / (importe / precio_entrada))
    else:
        sl = precio_entrada + (perdida_maxima / (importe / precio_entrada))
        tp1 = precio_entrada - (20 / (importe / precio_entrada))
        tp2 = precio_entrada - (30 / (importe / precio_entrada))

    unidades = round(importe / precio_entrada, 2)
    return round(sl, 2), round(tp1, 2), round(tp2, 2), unidades

def generar_estrategia_taxi(activo, precio_actual, direccion, tipo_orden, spread):
    precio_entrada = precio_actual + spread if tipo_orden == "LIMIT" else precio_actual
    sl, tp1, tp2, unidades = calcular_tp_sl(precio_entrada, direccion, spread)

    osciladores = "RSI > 50, MACD+, EMA 8/21"
    estrategia = {
        "activo": activo,
        "direccion": direccion,
        "tipo_orden": tipo_orden,
        "importe": 125,
        "entrada": round(precio_entrada, 2),
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "unidades": unidades,
        "osciladores": osciladores,
        "spread": spread,
    }
    return estrategia

def tabla_taxi(estr):
    return f"""
    <div style='border:1px solid #444;padding:10px;border-radius:8px;'>
    <h4>🚕 TAXI (Demo) para {estr['activo']}</h4>
    <b>📈 Tipo de operación:</b> {estr['direccion']}<br>
    <b>⚙️ Tipo de orden:</b> {estr['tipo_orden']}<br>
    <b>💵 Importe autorizado:</b> ${estr['importe']}<br>
    <b>🎯 Entrada (precio activo):</b> ${estr['entrada']}<br>
    <b>⛔ SL (precio estimado):</b> ${estr['sl']}<br>
    <b>🎯 TP1 (precio estimado):</b> ${estr['tp1']}<br>
    <b>🎯 TP2 (precio estimado):</b> ${estr['tp2']}<br>
    <b>📊 Unidades compradas:</b> {estr['unidades']}<br>
    <b>🧠 Osciladores:</b> {estr['osciladores']}<br>
    <b>🔍 Spread aplicado:</b> {estr['spread']}<br>
    </div>
    """

