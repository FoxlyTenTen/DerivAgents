from google.adk.agents import LlmAgent
from .tools import get_behavior_metrics
from . import prompt

MODEL = "gemini-2.5-flash"

behavior_agent = LlmAgent(
    name="behavior_agent",
    model=MODEL,
    instruction=prompt.BEHAVIOR_AGENT,
    description=(
        "Analyzes trader psychology and history to detect 'Tilt', revenge trading, and toxic asset patterns."
    ),
    tools=[get_behavior_metrics],
    output_key="behavior_agent_results"
)
