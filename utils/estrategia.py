# utils/estrategia.py

import random

# Simula una estrategia TAXI real o demo para un activo

def generar_estrategia_taxi(activo, modo_demo=False):
    precio_base = round(random.uniform(100, 500), 2)
    spread = round(random.uniform(0.02, 0.15), 2)
    entrada = round(precio_base + spread, 2)
    rrr_tp1 = 1.25
    rrr_tp2 = 1.5

    sl_precio = round(entrada - (125 / 1), 2)
    tp1_precio = round(entrada + (125 * rrr_tp1) / 125, 2)
    tp2_precio = round(entrada + (125 * rrr_tp2) / 125, 2)

    orden = random.choice(["LIMIT", "MARKET"])
    direccion = random.choice(["LONG", "SHORT"])

    estrategia = {
        "activo": activo,
        "modo_demo": modo_demo,
        "importe": 125,
        "tipo_orden": orden,
        "tipo_operacion": direccion,
        "entrada": entrada,
        "sl": sl_precio,
        "tp1": tp1_precio,
        "tp2": tp2_precio,
        "unidades": round(125 / entrada, 2),
        "spread": spread,
        "osciladores": "RSI > 50, MACD+, EMA 8/21",
    }
    return estrategia


def tabla_taxi(estr):
    return f"""
<table style="width:100%; font-size: 16px;">
<tr><th>📈 Campo</th><th>{estr['activo']}</th></tr>
<tr><td>📈 Tipo de operación</td><td>{estr['tipo_operacion']}</td></tr>
<tr><td>⚙️ Tipo de orden</td><td>{estr['tipo_orden']}</td></tr>
<tr><td>💵 Importe autorizado</td><td>${estr['importe']}</td></tr>
<tr><td>🎯 Entrada (precio activo)</td><td>${estr['entrada']}</td></tr>
<tr><td>⛔ SL (precio estimado)</td><td>${estr['sl']}</td></tr>
<tr><td>🎯 TP1 (precio estimado)</td><td>${estr['tp1']}</td></tr>
<tr><td>🎯 TP2 (precio estimado)</td><td>${estr['tp2']}</td></tr>
<tr><td>📊 Unidades compradas</td><td>{estr['unidades']}</td></tr>
<tr><td>🧠 Osciladores</td><td>{estr['osciladores']}</td></tr>
<tr><td>🔍 Spread aplicado</td><td>{estr['spread']}</td></tr>
</table>
"""
