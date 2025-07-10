import pandas as pd
import pandas_ta as ta
import numpy as np
import yfinance as yf

# 📊 Función principal para obtener indicadores técnicos del activo
def obtener_datos_tecnicos(simbolo):
    df = yf.download(simbolo, period="2d", interval="5m")

    if df.empty:
        return None

    # Eliminar filas con valores faltantes
    df.dropna(inplace=True)

    # 📈 Cálculo de indicadores técnicos
    df["RSI"] = ta.rsi(df["Close"], length=14)
    df["EMA_8"] = ta.ema(df["Close"], length=8)
    df["EMA_21"] = ta.ema(df["Close"], length=21)
    df["MACD"] = ta.macd(df["Close"]).iloc[:, 0]  # Línea MACD
    df["MACD_signal"] = ta.macd(df["Close"]).iloc[:, 1]  # Línea de señal
    df["ATR"] = ta.atr(df["High"], df["Low"], df["Close"], length=14)

    # Solo devolvemos las últimas dos filas (la actual y la anterior)
    return df.tail(2)
