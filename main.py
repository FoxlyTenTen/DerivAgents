import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the package is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trading.agent import root_agent

async def run_chat():
    print("Welcome to DerivAgents CLI")
    print("Type 'exit', 'quit', or 'q' to stop.")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting...")
                break
            
            if not user_input.strip():
                continue

            # Run the agent using the correct async method
            response = await root_agent.run_async(user_input)
            print(f"Agent: {response}")

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_chat())