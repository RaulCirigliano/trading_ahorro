from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Wealth Management API", description="API para el agente de ahorro a largo plazo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

TRADES_FILE = "trades_history.json"

class Trade(BaseModel):
    hora: str
    activo: str
    tipo: str
    precio: float
    estado: str
    modo: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Motor de Ahorro AI en línea"}

@app.get("/api/trades")
def get_trades():
    if not os.path.exists(TRADES_FILE):
        return []
    try:
        with open(TRADES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

@app.post("/api/trades")
def save_trade(trade: Trade):
    trades = []
    if os.path.exists(TRADES_FILE):
        try:
            with open(TRADES_FILE, "r") as f:
                trades = json.load(f)
        except:
            pass
    trades.append(trade.model_dump())
    with open(TRADES_FILE, "w") as f:
        json.dump(trades, f, indent=4)
    return {"status": "success", "trade": trade.model_dump()}

@app.get("/api/market/price")
def get_price(symbol: str = "SPY"):
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d")
        if df.empty:
            return {"error": "No data"}
        return {
            "symbol": symbol,
            "price": round(df['Close'].iloc[-1], 2)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/market/history")
def get_history(symbol: str = "SPY", timeframe: str = "1d", limit: int = 365):
    try:
        import yfinance as yf
        import pandas as pd
        import ta
        
        ticker = yf.Ticker(symbol)
        interval_map = {"1d": "1d", "1w": "1wk", "1m": "1m"}
        yf_interval = interval_map.get(timeframe, "1d")
        
        period = "2y" if yf_interval in ["1d", "1wk"] else "7d"
        df = ticker.history(period=period, interval=yf_interval)
        
        if df.empty:
            return {"error": "No data found for symbol"}
            
        df['sma_20'] = ta.trend.SMAIndicator(close=df['Close'], window=20).sma_indicator()
        df['sma_50'] = ta.trend.SMAIndicator(close=df['Close'], window=50).sma_indicator()
        
        formatted_data = []
        for index, row in df.iterrows():
            item = {
                "time": int(index.timestamp()),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2),
                "volume": int(row['Volume'])
            }
            if not pd.isna(row['sma_20']):
                item["sma_20"] = round(row['sma_20'], 2)
            if not pd.isna(row['sma_50']):
                item["sma_50"] = round(row['sma_50'], 2)
            formatted_data.append(item)
            
        return formatted_data[-limit:]
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/market/sentiment")
def get_sentiment(symbol: str = "SPY", source: str = "coindesk"):
    import random
    return {
        "score": round(random.uniform(-0.1, 0.4), 2),
        "estado": "NEUTRAL" if random.random() > 0.5 else "BULLISH",
        "noticias": [
            {"title": f"Resumen macroeconómico y tendencias de {symbol}", "score": 0.2},
            {"title": f"Análisis a largo plazo de fondos vinculados a {symbol}", "score": 0.1}
        ]
    }

@app.get("/api/market/analysis")
def get_analysis(symbol: str = "SPY", timeframe: str = "1d", engine: str = "local"):
    try:
        import yfinance as yf
        import pandas as pd
        import ta
        
        ticker = yf.Ticker(symbol)
        interval_map = {"1d": "1d", "1w": "1wk", "1m": "1m"}
        yf_interval = interval_map.get(timeframe, "1d")
        df = ticker.history(period="1y", interval=yf_interval)
        
        if df.empty:
            return {"error": "Empty data"}
            
        df['rsi'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
        df['sma_20'] = ta.trend.SMAIndicator(close=df['Close'], window=20).sma_indicator()
        df['sma_50'] = ta.trend.SMAIndicator(close=df['Close'], window=50).sma_indicator()
        
        latest = df.iloc[-1]
        
        rsi_val = round(latest['rsi'], 2) if not pd.isna(latest['rsi']) else 50
        sma20_val = round(latest['sma_20'], 2) if not pd.isna(latest['sma_20']) else latest['Close']
        price_val = round(latest['Close'], 2)

        signal = "MANTENER"
        reason = "Mercado estable."

        if engine == "local":
            if rsi_val < 30:
                signal = "COMPRAR"
                reason = "Caída histórica detectada (RSI < 30)."
            elif price_val > sma20_val:
                signal = "COMPRAR"
                reason = "Tendencia alcista confirmada. Buen momento para DCA."
            else:
                signal = "MANTENER"
                reason = "Esperando mejor punto de entrada para DCA."
                
        return {
            "symbol": symbol,
            "signal": signal,
            "reason": reason,
            "indicators": {
                "rsi": rsi_val,
                "sma_20": sma20_val,
                "current_price": price_val
            },
            "latest_candle": {
                "time": int(latest.name.timestamp()),
                "open": latest['Open'],
                "high": latest['High'],
                "low": latest['Low'],
                "close": latest['Close']
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8766, reload=True)
