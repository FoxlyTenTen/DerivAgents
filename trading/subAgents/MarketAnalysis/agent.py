from google.adk.agents import LlmAgent
from trading.tools import get_real_market_data
from . import prompt

MODEL = 'gemini-2.5-flash' 

market_analysis_agent = LlmAgent(
    name="market_analysis_agent",
    model=MODEL,
    instruction=prompt.MARKET_ANALYSIS,
    description=(
       "Fetch real-time market data (OHLC) AND analyze price movement using technical indicators (RSI, MACD, BB)."
    ),
    tools=[get_real_market_data],
    output_key="market_analysis_results"
)