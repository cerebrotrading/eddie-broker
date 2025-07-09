# utils/estrategia.py

import random

def generar_estrategia_taxi(activo):
    """
    Simula una estrategia TAXI para un activo dado.
    Devuelve un diccionario con campos clave para construir la tabla.
    """

    # Simulaciones de precios base
    precio_base = round(random.uniform(100, 500), 2)
    spread = round(random.uniform(0.03, 0.07), 2)
    entrada = round(precio_base + spread, 2)
    tipo_operacion = random.choice(["LONG", "SHORT"])
    orden = random.choice(["LIMIT", "MARKET"])

    # TP y SL con base en RRR típicos (1.5, 2)
    capital_parcial = 125  # usd por TP
    sl_dinero = -capital_parcial
    rrr_tp1 = 1.25
    rrr_tp2 = 1.5

    sl_precio = round(entrada - (abs(sl_dinero) / (1 * 1)), 2) if tipo_operacion == "LONG" else round(entrada + (abs(sl_dinero) / (1 * 1)), 2)
    tp1_precio = round(entrada + (capital_parcial * rrr_tp1 / capital_parcial), 2) if tipo_operacion == "LONG" else round(entrada - (capital_parcial * rrr_tp1 / capital_parcial), 2)
    tp2_precio = round(entrada + (capital_parcial * rrr_tp2 / capital_parcial), 2) if tipo_operacion == "LONG" else round(entrada - (capital_parcial * rrr_tp2 / capital_parcial), 2)

    unidades = round(125 / entrada, 2)

    # Simulación de osciladores
    osciladores = "RSI > 50, MACD+, EMA 8/21 cruce"
    spread_valido = "✅"

    return {
        "activo": activo,
        "tipo_operacion": tipo_operacion,
        "tipo_orden": orden,
        "importe": "$125",
        "entrada": f"${entrada}",
        "sl": f"${sl_precio}",
        "tp1": f"${tp1_precio}",
        "tp2": f"${tp2_precio}",
        "unidades": unidades,
        "osciladores": osciladores,
        "spread": spread,
        "spread_valido": spread_valido
    }


def tabla_taxi(estr):
    """
    Construye una tabla en Markdown con los datos de una estrategia.
    """
    return f"""
<table>
    <thead>
        <tr><th>Campo</th><th>{estr['activo']}</th></tr>
    </thead>
    <tbody>
        <tr><td>📈 Tipo de operación</td><td>{estr['tipo_operacion']}</td></tr>
        <tr><td>⚙️ Tipo de orden</td><td>{estr['tipo_orden']}</td></tr>
        <tr><td>💵 Importe autorizado</td><td>{estr['importe']}</td></tr>
        <tr><td>🎯 Entrada (precio activo)</td><td>{estr['entrada']}</td></tr>
        <tr><td>⛔ SL (precio estimado)</td><td>{estr['sl']}</td></tr>
        <tr><td>🎯 TP1 (precio estimado)</td><td>{estr['tp1']}</td></tr>
        <tr><td>🎯 TP2 (precio estimado)</td><td>{estr['tp2']}</td></tr>
        <tr><td>📊 Unidades compradas</td><td>{estr['unidades']}</td></tr>
        <tr><td>🧠 Osciladores</td><td>{estr['osciladores']}</td></tr>
        <tr><td>🔍 Spread</td><td>{estr['spread']}</td></tr>
        <tr><td>🔍 Spread validado eToro</td><td>{estr['spread_valido']}</td></tr>
    </tbody>
</table>
"""
