import asyncio
import uuid

import streamlit as st

from main import SYSTEM_PROMPT, build_mcp_connections, build_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent


async def _build_agent(connections: dict):
    client = MultiServerMCPClient(connections)
    tools = await client.get_tools()

    model = build_model()
    checkpointer = InMemorySaver()

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=checkpointer,
    )
    return agent


def _run_async(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@st.cache_resource
def get_agent(model_override: str | None):
    if model_override:
        import os

        os.environ["OPENAI_MODEL"] = model_override

    connections = build_mcp_connections()
    try:
        agent = _run_async(_build_agent(connections))
        st.session_state.mcp_warning = ""
        return agent
    except BaseException as exc:
        local_only = {"heritage-db": connections["heritage-db"]}
        st.session_state.mcp_warning = (
            "Some MCP servers could not be reached. Running with local heritage-db tools only. "
            f"Details: {type(exc).__name__}: {exc}"
        )
        return _run_async(_build_agent(local_only))


def main() -> None:
    st.set_page_config(page_title="Heritage Travel Assistant", layout="wide")

    st.title("Heritage Travel Assistant")
    st.caption("Plan heritage + photography-friendly trips using MCP tools.")

    import os

    if not os.getenv("OPENAI_API_KEY"):
        st.error(
            "OPENAI_API_KEY is missing. Add it to your shell environment or create a .env file (you can copy .env.example to .env)."
        )
        st.stop()

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"travel_{uuid.uuid4().hex}" 

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    with st.sidebar:
        st.subheader("Settings")
        st.text_input(
            "OpenAI model",
            key="openai_model",
            value="",
            placeholder="Defaults to OPENAI_MODEL env var",
        )
        if st.button("New conversation"):
            st.session_state.thread_id = f"travel_{uuid.uuid4().hex}" 
            st.session_state.chat_messages = []
            st.rerun()

        st.markdown("---")
        st.write("Required env var: `OPENAI_API_KEY`")
        st.write("Optional: `WEATHER_MCP_URL`, `MAPS_MCP_URL`, `HOTELS_MCP_URL`")

        warning = st.session_state.get("mcp_warning")
        if warning:
            st.warning(warning)

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Describe your trip requirement...")
    if not prompt:
        return

    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    model_override = st.session_state.openai_model.strip() or None
    agent = get_agent(model_override)

    with st.chat_message("assistant"):
        with st.spinner("Planning..."):
            response = _run_async(
                agent.ainvoke(
                    {
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ]
                    },
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                )
            )

            content = response["messages"][-1].content
            st.markdown(content)

    st.session_state.chat_messages.append({"role": "assistant", "content": content})


if __name__ == "__main__":
    main()
