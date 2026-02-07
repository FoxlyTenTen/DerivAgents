from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from . import prompt

# Import Sub-Agents
from .subAgents.MarketAnalysis.agent import market_analysis_agent
from .subAgents.NewsAgent.agent import news_agent
from .subAgents.SentimentAgent.agent import sentiment_agent
from .subAgents.MergeAgent.agent import merge_agent
from .subAgents.BehaviorAgent.agent import behavior_agent

# 1. Define the Sequential Research Step
# Using SequentialAgent to prevent race conditions during file saves (stale session error).
research_group = ParallelAgent(
    name="research_group",
    sub_agents=[market_analysis_agent, news_agent, sentiment_agent, behavior_agent],
    description="Runs Market Analysis, News, Sentiment, and Behavior agents in parallel."
)

# 2. Define the Full Real-Time Analysis Workflow
# This workflow runs the research group first, then passes the results to the Merge Agent.
real_time_workflow = SequentialAgent(
    name="real_time_market_workflow",
    sub_agents=[research_group, merge_agent],
    description="Orchestrates the full real-time market analysis flow: Research -> Merge."
)

# 3. Create Tools for the Coordinator
# This allows the LlmAgent (Coordinator) to choose which workflow or agent to call.
real_time_analysis_tool = AgentTool(real_time_workflow)

# 4. The Root Coordinator Agent
trader_coordinator = LlmAgent(
    name="trader_coordinator",
    model="gemini-2.5-pro",
    instruction=prompt.TRADER_COORDINATOR,
    tools=[
        real_time_analysis_tool,
        # Future: You can add tools for individual agents here if you want the coordinator to call them directly
        AgentTool(market_analysis_agent),
        AgentTool(news_agent),
        AgentTool(sentiment_agent),
        AgentTool(merge_agent),
    ] 
)

root_agent = trader_coordinator