import asyncio
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent


load_dotenv()


SYSTEM_PROMPT = """
You are an expert travel planner for heritage and photography-focused trips.

When the user asks for a trip plan, always:
1) Check weather first using weather tools for each day/time window.
2) Build a practical day-wise route using maps tools (minimize backtracking).
3) Prioritize must-visit heritage spots from the heritage DB tool.
4) Include 1 short description + sample photo links for every recommended spot.
5) Suggest affordable hotels with price range, distance to core spots, and why they fit budget travelers.
6) If weather is poor for outdoor photography, propose fallback timings/indoor alternatives.

Output format:
- Trip summary
- Weather suitability check
- Day 1 plan
- Day 2 plan (or adapt to requested duration)
- Must-visit heritage spots (with sample photos)
- Affordable stay options
- Budget tips + transport notes
""".strip()


def build_mcp_connections() -> dict:
    """Build MCP server connection config from environment variables."""
    connections = {}

    weather_url = os.getenv("WEATHER_MCP_URL")
    maps_url = os.getenv("MAPS_MCP_URL")
    hotels_url = os.getenv("HOTELS_MCP_URL")

    if weather_url:
        connections["weather"] = {
            "url": weather_url,
            "transport": "streamable_http",
        }

    if maps_url:
        connections["maps"] = {
            "url": maps_url,
            "transport": "streamable_http",
        }

    if hotels_url:
        connections["hotels"] = {
            "url": hotels_url,
            "transport": "streamable_http",
        }

    connections["heritage-db"] = {
        "command": sys.executable,
        "args": [str(Path(__file__).with_name("heritage_mcp_server.py"))],
        "transport": "stdio",
    }

    return connections


def build_model() -> ChatOpenAI:
    """Create the chat model from environment configuration."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Set it in your shell or in a local .env file before running the assistant."
        )

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model_name, api_key=api_key)

async def main() -> None:
    client = MultiServerMCPClient(build_mcp_connections())
    tools = await client.get_tools()

    model = build_model()
    checkpointer = InMemorySaver()
    config = {"configurable": {"thread_id": "travel_conversation"}}

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=checkpointer,
    )

    print("\nTravel Assistant is ready.")
    print("Example: Plan a 2-day heritage photography trip in Hampi\n")

    while True:
        choice = input("""
Menu:
1. Plan a trip
2. Quit
Enter your choice (1 or 2): """)

        if choice == "1":
            query = input("\nDescribe your trip requirement:\n> ")
            response = await agent.ainvoke(
                {
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": query},
                    ]
                },
                config=config,
            )

            print("\n" + response["messages"][-1].content + "\n")
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Please choose 1 or 2.")


if __name__ == "__main__":
    asyncio.run(main())
