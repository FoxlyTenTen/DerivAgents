from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.5-flash"

news_agent = LlmAgent(
    name="news_agent",
    model=MODEL,
    instruction=prompt.NEWS_AGENT,
    description=(
        "Monitor economic events and news to identify market catalysts."
    ),
    tools=[google_search],
    output_key="news_agent_results"
)