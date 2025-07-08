import requests
import pandas as pd
import pandas_ta as ta
import os
from datetime import datetime, timedelta

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def obtener_precios_historicos(activo, intervalo="15"):
    url = f"https://finnhub.io/api/v1/stock/candle"
    ahora = int(datetime.now().timestamp())
    desde = ahora - (60 * 60 * 24)  # Últimas 24 horas

    params = {
        "symbol": activo,
        "resolution": intervalo,
        "from": desde,
        "to": ahora,
        "token": FINNHUB_API_KEY,
    }

    resp = requests.get(url, params=params)
    data = resp.json()

    if data.get("s") != "ok":
        return None

    df = pd.DataFrame({
        "timestamp": pd.to_datetime(data["t"], unit="s"),
        "open": data["o"],
        "high": data["h"],
        "low": data["l"],
        "close": data["c"],
        "volume": data["v"]
    })

    df.set_index("timestamp", inplace=True)
    return df


def validar_indicadores(activo):
    df = obtener_precios_historicos(activo, intervalo="15")
    if df is None or len(df) < 20:
        return {}

    resultados = {}

    # RSI
    df["rsi"] = ta.rsi(df["close"], length=14)
    rsi_actual = df["rsi"].iloc[-1]
    resultados["RSI > 50"] = rsi_actual > 50

    # Momentum (velas alcistas consecutivas)
    ultimos = df["close"].tail(3)
    resultados["Momentum alcista"] = all(ultimos.diff().dropna() > 0)

    # ATR
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    atr_actual = df["atr"].iloc[-1]
    resultados["ATR > 1.0"] = atr_actual > 1.0

    # EMA
    df["ema20"] = ta.ema(df["close"], length=20)
    df["ema50"] = ta.ema(df["close"], length=50)
    resultados["EMA20 > EMA50"] = df["ema20"].iloc[-1] > df["ema50"].iloc[-1]

    # MACD
    macd = ta.macd(df["close"])
    resultados["MACD hist > 0"] = macd["MACDh_12_26_9"].iloc[-1] > 0

    return resultados
