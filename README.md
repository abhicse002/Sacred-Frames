# Agentic Travel Assistant (MCP)

An MCP-powered travel planner that can create heritage-focused itineraries like:

> Plan a 2-day heritage photography trip in Hampi

The assistant is designed to:
- check weather suitability first,
- route the day plan using maps,
- prioritize must-visit heritage spots,
- include sample photo links + short descriptions,
- and suggest affordable hotels.

## Architecture

- **Client Agent:** `main.py`
  - Uses `langgraph` + `MultiServerMCPClient`
  - Connects to multiple MCP servers as tools
- **Custom MCP Server:** `heritage_mcp_server.py`
  - Local DB of heritage destinations and photography-friendly spots
  - Exposes MCP tools over `stdio`

## MCP servers used

Configure these as environment variables (HTTP MCP endpoints):

- `WEATHER_MCP_URL`
- `MAPS_MCP_URL`
- `HOTELS_MCP_URL`

Local tool server is auto-wired:
- `heritage-db` via `python heritage_mcp_server.py`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create local environment config:

```bash
cp .env.example .env
```

Edit `.env` and set at least:

- `OPENAI_API_KEY`
- `WEATHER_MCP_URL`
- `MAPS_MCP_URL`
- `HOTELS_MCP_URL`

`OPENAI_MODEL` is optional and defaults to `gpt-4o-mini`.

> `.env` is gitignored to avoid committing API keys.
> If one of the remote MCP URLs is missing, the assistant will still start, but tool coverage will be limited.

## Run

```bash
python main.py
```

Then choose **1. Plan a trip** and enter:

```text
Plan a 2-day heritage photography trip in Hampi
```

## Current custom heritage DB coverage

Use this local MCP tool data:
- Hampi (Karnataka, India)

Tools exposed by `heritage_mcp_server.py`:
- `list_supported_destinations()`
- `search_heritage_spots(destination, limit=8)`
- `get_spot_by_id(destination, spot_id)`

## Recommended next upgrades

1. Add more destinations (e.g., Jaipur, Varanasi, Khajuraho, Mahabalipuram).
2. Add scoring logic in MCP tool outputs for weather + crowd level + photo opportunity.
3. Cache hotel/maps/weather tool calls for faster repeated itinerary planning.
4. Add a web UI (Streamlit/Next.js) on top of this CLI agent.
