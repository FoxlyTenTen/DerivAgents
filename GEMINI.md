# DerivAgents

DerivAgents is a modular, multi-agent system designed for real-time market analysis and trading insights. It utilizes the `google.adk` (Agent Development Kit) and Google's Gemini models to orchestrate specialized agents that perform technical analysis, news monitoring, and sentiment analysis.

## Project Overview

The system is built to handle complex market queries by delegating tasks to specialized sub-agents and synthesizing their findings into a coherent report. It emphasizes a strict separation of concerns and follows a "coordinator-worker" pattern.

### Main Technologies
- **Agent Framework**: `google.adk`
- **LLM Models**: Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.0 Flash Experimental
- **Data & Analysis**: `yfinance`, `pandas`, `numpy`
- **Search**: `google_search` (via ADK tools)

## Architecture

The project is structured around a central coordinator that manages various workflows:

- **Root Coordinator (`trader_coordinator`)**: The entry point for all user requests. It classifies intent and routes to the appropriate specialist or workflow.
- **Real-Time Analysis Workflow**:
    - **Research Group (Parallel)**: Runs `MarketAnalysisAgent`, `NewsAgent`, and `SentimentAgent` simultaneously to gather diverse market data.
    - **Merge Agent (`merge_agent`)**: A sequential step that synthesizes the output from the Research Group into a final response.
- **Sub-Agents**:
    - `MarketAnalysis`: Fetches and analyzes technical indicators (RSI, MACD, Bollinger Bands).
    - `NewsAgent`: Uses Google Search to identify market-moving news and catalysts.
    - `SentimentAgent`: (Currently Mock) Evaluates social and market sentiment.
    - `CoachAgent` & `BehaviorAgent`: Provide additional trading guidance and behavioral analysis.

## Directory Structure

```text
/
├── trading/
│   ├── agent.py          # Workflow and Root Agent definitions
│   ├── prompt.py         # Global prompts and instructions
│   ├── tools.py          # Shared technical analysis and data tools
│   └── subAgents/        # Modular agent definitions
│       ├── MarketAnalysis/
│       ├── NewsAgent/
│       ├── SentimentAgent/
│       ├── MergeAgent/
│       ├── CoachAgent/
│       └── BehaviorAgent/
```

## Development Conventions

- **Modular Agents**: Every sub-agent resides in its own directory with an `agent.py` for logic and a `prompt.py` for its system instructions.
- **Prompt Management**: Keep agent instructions in `prompt.py` to maintain a clean `agent.py`.
- **Tooling**: Shared tools like `get_real_market_data` should be placed in `trading/tools.py`.
- **Safety & Compliance**: Agents are strictly instructed NOT to provide direct signals or predictions, focusing instead on objective analysis.

## Setup and Running

### Prerequisites
- Python 3.10+
- `google.adk` library access
- Google Gemini API credentials

### Installation
```bash
pip install yfinance pandas numpy
```

### Usage
The system is designed to be integrated into an application using the `root_agent` defined in `trading/agent.py`.

```python
from trading.agent import root_agent

# Example interaction
# response = root_agent.run("What is the current outlook for BTC?")
```

## TODO / Future Improvements
- [ ] Implement real-time social sentiment analysis in `SentimentAgent`.
- [ ] Integrate additional technical indicators.
- [ ] Add a CLI or Web entry point for direct interaction.
