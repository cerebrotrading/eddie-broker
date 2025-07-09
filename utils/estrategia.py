# utils/estrategia.py

import yfinance as yf
import pandas as pd
import ta

def generar_estrategia_taxi(activo: str, capital_total: float = 250.0):
    # 1. Descargar datos M15
    df = yf.download(tickers=activo, interval="15m", period="2d")
    if df.empty:
        raise ValueError(f"No se pudo descargar datos para {activo}")

    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["EMA8"] = ta.trend.EMAIndicator(df["Close"], window=8).ema_indicator()
    df["EMA21"] = ta.trend.EMAIndicator(df["Close"], window=21).ema_indicator()
    df["MACD"] = ta.trend.MACD(df["Close"]).macd()
    df["ATR"] = ta.volatility.AverageTrueRange(high=df["High"], low=df["Low"], close=df["Close"]).average_true_range()

    # 2. Último valor técnico
    rsi = df["RSI"].iloc[-1]
    ema8 = df["EMA8"].iloc[-1]
    ema21 = df["EMA21"].iloc[-1]
    macd = df["MACD"].iloc[-1]
    atr = df["ATR"].iloc[-1]
    precio = df["Close"].iloc[-1]

    # 3. Lógica de validación real
    es_entrada_larga = rsi > 50 and ema8 > ema21 and macd > 0 and atr > 1.0  # umbral simple

    if not es_entrada_larga:
        raise ValueError(f"{activo} no cumple condiciones técnicas reales.")

    # 4. Parámetros de estrategia
    tipo_orden = "LIMIT"
    spread = round(precio * 0.0005, 2)
    entrada = round(precio + spread, 2)
    importe = capital_total / 2  # 125 por TP
    unidades = round(importe / entrada, 2)

    # SL y TP con RRR reales
    sl_dinero = -importe
    sl_precio = round(entrada - (importe / unidades), 2)
    tp1_dinero = round(importe * 1.25, 2)
    tp1_precio = round(entrada + (tp1_dinero / unidades), 2)
    tp2_dinero = round(importe * 1.5, 2)
    tp2_precio = round(entrada + (tp2_dinero / unidades), 2)

    osciladores = f"RSI: {rsi:.1f}, MACD: {macd:.2f}, EMA8/21: {ema8:.2f} / {ema21:.2f}, ATR: {atr:.2f}"

    return {
        "activo": activo,
        "tipo_operacion": "LONG",
        "tipo_orden": tipo_orden,
        "spread": spread,
        "importe": importe,
        "entrada": entrada,
        "sl": sl_precio,
        "tp1": tp1_precio,
        "tp2": tp2_precio,
        "unidades": unidades,
        "osciladores": osciladores
    }
