from google.adk.agents import LlmAgent
from trading.tools import get_social_sentiment
from . import prompt

MODEL = "gemini-2.5-flash"

sentiment_agent = LlmAgent(
    name="sentiment_agent",
    model=MODEL,
    instruction=prompt.SENTIMENT_AGENT,
    description=(
        "Analyze crowd psychology, sentiment trends, and fear/greed metrics."
    ),
    tools=[get_social_sentiment],
    output_key="sentiment_agent_results"
)