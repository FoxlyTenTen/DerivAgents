

# Keep Market Data (Real)
import yfinance as yf
import pandas as pd
import numpy as np

def get_real_market_data(symbol: str, period: str = "1mo", interval: str = "1h") -> dict:
    """
    Fetches real-time market data from Yahoo Finance and calculates technical indicators.
    
    Args:
        symbol: Ticker symbol (e.g., 'BTC-USD', 'NVDA', 'EURUSD=X').
        period: Data period to download (default: '1mo').
        interval: Data interval (default: '1h'). Options: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo.
        
    Returns:
        Dictionary with latest price, changes, and technical indicators (RSI, MACD, BB, ATR).
    """
    try:
        # Fetch data
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return {"error": f"No data found for symbol '{symbol}'. Please check the ticker."}
        
        # --- Technical Analysis Calculations ---
        
        # RSI (14)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD (12, 26, 9)
        exp12 = df['Close'].ewm(span=12, adjust=False).mean()
        exp26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp12 - exp26
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['Signal_Line']
        
        # Bollinger Bands (20, 2)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['STD20'] = df['Close'].rolling(window=20).std()
        df['Upper_Band'] = df['MA20'] + (df['STD20'] * 2)
        df['Lower_Band'] = df['MA20'] - (df['STD20'] * 2)
        
        # ATR (14)
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['ATR'] = true_range.rolling(14).mean()
        
        # Output latest available data (drop NaNs from start)
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        trend = "Bullish" if latest['MACD'] > latest['Signal_Line'] else "Bearish"
        
        result = {
            "symbol": symbol,
            "interval": interval,
            "current_price": round(latest['Close'], 2),
            "change_percent": round(((latest['Close'] - prev['Close']) / prev['Close']) * 100, 2),
            "last_updated": str(latest.name),
            "indicators": {
                "RSI": round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else None,
                "MACD": {
                    "line": round(latest['MACD'], 2) if not pd.isna(latest['MACD']) else None,
                    "signal": round(latest['Signal_Line'], 2) if not pd.isna(latest['Signal_Line']) else None,
                    "histogram": round(latest['MACD_Hist'], 2) if not pd.isna(latest['MACD_Hist']) else None
                },
                "BollingerBands": {
                    "upper": round(latest['Upper_Band'], 2) if not pd.isna(latest['Upper_Band']) else None,
                    "middle": round(latest['MA20'], 2) if not pd.isna(latest['MA20']) else None,
                    "lower": round(latest['Lower_Band'], 2) if not pd.isna(latest['Lower_Band']) else None
                },
                "ATR": round(latest['ATR'], 2) if not pd.isna(latest['ATR']) else None
            },
            "market_summary": {
                "trend_momentum": trend
            }
        }
        return result

    except Exception as e:
        return {"error": f"Failed to fetch market data: {str(e)}"}

# Keep Social Sentiment as Mock for now (no free real-time social API easily available)
def get_social_sentiment(symbol: str) -> dict:
    """Fetches MOCK social sentiment (replace with real API later)."""
    return {
        "symbol": symbol,
        "sentiment_score": 0.45,  # Neutral-Bearish
        "fear_greed_index": 48,   # Neutral
        "social_volume": "Normal",
        "trending_topics": ["#inflation", "#trading"],
        "crowd_psychology": "Cautious optimism pending macro news."
    }
