from google.adk.agents import LlmAgent
from . import prompt

MODEL = 'gemini-2.5-flash' 

merge_agent = LlmAgent(
    name="merge_agent",
    model=MODEL,
    instruction=prompt.MERGE_AGENT,
    description=(
       "Merge analysis from Market, News, and Sentiment agents into a final report."
    ),
    tools=[],
    output_key="final_trader_response"
)