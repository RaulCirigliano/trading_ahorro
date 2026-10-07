from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ccxt

app = FastAPI(title="Trading AI API", description="API para el agente de trading")

# Configurar CORS para permitir que el frontend HTML acceda a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite cualquier origen durante desarrollo
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializamos el exchange (usamos Kraken por defecto para evitar bloqueos geográficos de Binance)
exchange = ccxt.kraken()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Motor de Trading AI en línea"}

@app.get("/api/market/price")
def get_price(symbol: str = "BTC/USDT"):
    """
    Obtiene el precio actual y el volumen de un activo.
    """
    try:
        ticker = exchange.fetch_ticker(symbol)
        return {
            "symbol": symbol,
            "price": ticker['last'],
            "high": ticker['high'],
            "low": ticker['low'],
            "volume": ticker['quoteVolume']
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/market/history")
def get_history(symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 100):
    """
    Obtiene el histórico de velas (OHLCV) listo para graficar con su Media Móvil.
    """
    try:
        # fetch_ohlcv devuelve: [timestamp, open, high, low, close, volume]
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        import pandas as pd
        import ta
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['sma_20'] = ta.trend.SMAIndicator(close=df['close'], window=20).sma_indicator()
        
        # Lo formateamos para que Lightweight Charts lo entienda fácilmente
        formatted_data = []
        for index, row in df.iterrows():
            item = {
                "time": int(row['timestamp'] / 1000),
                "open": row['open'],
                "high": row['high'],
                "low": row['low'],
                "close": row['close'],
                "volume": row['volume']
            }
            if not pd.isna(row['sma_20']):
                item["sma_20"] = round(row['sma_20'], 2)
            formatted_data.append(item)
            
        return formatted_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/market/sentiment")
def get_sentiment(symbol: str = "BTC/USDT", source: str = "coindesk"):
    """
    Agente de Sentimiento con selección de fuente.
    """
    try:
        import feedparser
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        
        # Mapeo de monedas
        base_asset = symbol.split('/')[0].upper()
        nombres = {"BTC": "Bitcoin", "ETH": "Ethereum", "SOL": "Solana"}
        nombre_completo = nombres.get(base_asset, base_asset)
        
        if source == "twitter":
            return {
                "score": 0,
                "estado": "OFFLINE",
                "noticias": [
                    {
                        "title": "⚠️ La API de Twitter/X requiere configurar una Clave PRO en el archivo .env",
                        "score": 0
                    }
                ]
            }
        
        # Si es CoinDesk
        feed = feedparser.parse('https://www.coindesk.com/arc/outboundfeeds/rss/')
        analyzer = SentimentIntensityAnalyzer()
        
        total_score = 0
        news_list = []
        
        # Filtrar noticias que hablen de nuestro activo
        for entry in feed.entries:
            title = entry.title
            # Buscar menciones (ignorar mayúsculas)
            if base_asset.lower() in title.lower() or nombre_completo.lower() in title.lower():
                score = analyzer.polarity_scores(title)
                compound = score['compound']
                total_score += compound
                
                news_list.append({
                    "title": title,
                    "score": round(compound, 2)
                })
                
                if len(news_list) >= 5: # Quedarnos con máximo 5 noticias relevantes
                    break
                    
        # Si no hay noticias recientes sobre esta moneda, ser neutrales
        if len(news_list) == 0:
            return {"score": 0, "estado": "NEUTRAL", "noticias": [{"title": f"Sin noticias recientes de {nombre_completo}", "score": 0}]}
            
        avg_score = total_score / len(news_list)
        
        if avg_score > 0.15:
            estado = "BULLISH"
        elif avg_score < -0.15:
            estado = "BEARISH"
        else:
            estado = "NEUTRAL"
            
        return {
            "score": round(avg_score, 2),
            "estado": estado,
            "noticias": news_list
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/market/analysis")
def get_analysis(symbol: str = "BTC/USDT", timeframe: str = "1m", engine: str = "local"):
    """
    Realiza análisis técnico cuantitativo de las últimas velas.
    """
    try:
        import pandas as pd
        import ta
        
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Calcular RSI (14 periodos)
        df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
        
        # Calcular Medias Móviles (SMA 20 y SMA 50)
        df['sma_20'] = ta.trend.SMAIndicator(close=df['close'], window=20).sma_indicator()
        df['sma_50'] = ta.trend.SMAIndicator(close=df['close'], window=50).sma_indicator()
        
        latest = df.iloc[-1]
        previous = df.iloc[-2]
        
        # Lógica del Agente Orquestador (IA Gemini vs Matemático)
        signal = "MANTENER"
        reason = "El mercado está en zona neutral."
        
        rsi_val = round(latest['rsi'], 2)
        sma20_val = round(latest['sma_20'], 2)
        price_val = round(latest['close'], 2)

        if engine == "local":
            # Agente 100% Cuantitativo y Matemático (Gratis y ultra rápido)
            if rsi_val < 30 and price_val > sma20_val:
                signal = "COMPRAR"
                reason = "RSI en sobreventa (<30) y precio rompió la SMA 20 al alza."
            elif rsi_val > 70 and price_val < sma20_val:
                signal = "VENDER"
                reason = "RSI en sobrecompra (>70) y precio cayó bajo la SMA 20."
            elif rsi_val < 20:
                signal = "COMPRAR"
                reason = "Pánico extremo en el mercado (RSI <20). Posible rebote."
            elif rsi_val > 80:
                signal = "VENDER"
                reason = "Euforia extrema (RSI >80). Corrección inminente."
            else:
                signal = "MANTENER"
                reason = f"Esperando confirmación (RSI: {rsi_val}, Precio cerca de SMA 20)."
                
        elif engine == "ai":
            from dotenv import load_dotenv
            import os
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.prompts import PromptTemplate
            import json

            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key or api_key == "tu_clave_aqui_sin_comillas":
                reason = "[AVISO] Falta GEMINI_API_KEY en archivo .env. IA Desconectada."
                signal = "ERROR"
            else:
                try:
                    # Inicializar Gemini
                    llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", google_api_key=api_key, temperature=0.2)
                    
                    prompt = PromptTemplate.from_template(
                        "Eres el Agente Orquestador de un bot de trading cuantitativo. "
                        "Analiza los siguientes datos técnicos del par {symbol}:\n"
                        "- Precio Actual: ${precio}\n"
                        "- RSI (14): {rsi}\n"
                        "- SMA (20): {sma20}\n"
                        "- SMA (50): {sma50}\n\n"
                        "Emite una señal final. Tu respuesta debe ser EXCLUSIVAMENTE en formato JSON válido:\n"
                        '{{"signal": "COMPRAR", "reason": "Justificación de máximo 15 palabras"}} o VENDER o MANTENER.'
                    )
                    
                    chain = prompt | llm
                    respuesta = chain.invoke({
                        "symbol": symbol,
                        "precio": price_val,
                        "rsi": rsi_val,
                        "sma20": sma20_val,
                        "sma50": round(latest['sma_50'], 2)
                    })
                    
                    raw_json = respuesta.content.replace("```json", "").replace("```", "").strip()
                    ia_decision = json.loads(raw_json)
                    
                    signal = ia_decision.get("signal", "MANTENER").upper()
                    reason = "IA: " + ia_decision.get("reason", "Decisión generada.")
                    
                    if signal not in ["COMPRAR", "VENDER", "MANTENER"]:
                        signal = "MANTENER"
                except Exception as e:
                    reason = f"Error en el Agente IA: {str(e)}"
                    signal = "ERROR"
                    
        return {
            "symbol": symbol,
            "signal": signal,
            "reason": reason,
            "indicators": {
                "rsi": round(latest['rsi'], 2) if not pd.isna(latest['rsi']) else None,
                "sma_20": round(latest['sma_20'], 2) if not pd.isna(latest['sma_20']) else None,
                "sma_50": round(latest['sma_50'], 2) if not pd.isna(latest['sma_50']) else None,
                "current_price": latest['close']
            },
            "latest_candle": {
                "time": int(latest['timestamp'] / 1000),
                "open": latest['open'],
                "high": latest['high'],
                "low": latest['low'],
                "close": latest['close']
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8765, reload=True)
