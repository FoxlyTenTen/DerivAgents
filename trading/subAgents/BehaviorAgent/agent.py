from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt

model = "gemini-2.0-flash-exp"

root_agent = LlmAgent(
    name="trader_coordinator",
    model=model,
    instruction=prompt.TRADER_COORDINATOR,
    description=(
        "Understand user intent and route tasks to specialist agents,"
        "Route tasks to specialist agents"
        "Combine agent outputs into one explanation"
        "Enforce no-signal and no-prediction rules"
        "Structure final response for UI and chatbot"
    ),
    tools=[]
)