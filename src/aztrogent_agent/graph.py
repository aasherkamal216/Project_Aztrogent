"""This module defines the main Aztrogent Graph.
"""
from datetime import datetime, timezone
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.pregel import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.prebuilt import ToolNode

from aztrogent_agent.configuration import Configuration
from aztrogent_agent.state import InputState, State
from aztrogent_agent.nodes import (
    linkedin_subgraph,
    gmail_subgraph,
    github_subgraph,
    calendar_subgraph
)
from aztrogent_agent.tools import OTHER_TOOLS, COLLABORATE_WITH_TEAM, MEMORY_TOOLS
from aztrogent_agent.utils import load_chat_model
from src.settings import settings

# Map team names to subgraph names
team_graph_name_map = {
    "LinkedIn": "linkedin_subgraph",
    "Gmail": "gmail_subgraph",
    "GitHub": "github_subgraph",
    "Calendar": "calendar_subgraph"
}


## Conditional Edge
async def tools_condition(
    state: MessagesState,
) -> Literal[
    "linkedin_subgraph",
    "memory_node",
    "web_search",
    "gmail_subgraph",
    "github_subgraph",
    "calendar_subgraph",
    END,
]:
    """
    Determine if the conversation should continue to tools/subgaphs or end
    """
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        for call in last_message.tool_calls:
            tool_name = call.get("name")
            if tool_name == "COLLABORATE_WITH_TEAM":
                return team_graph_name_map[call["args"]["team"]]

            elif tool_name == "search":
                return "web_search"

            else:
                return "memory_node"

    return END


## Main Agent Calling Node
async def call_model(
    state: State, 
    config: RunnableConfig,
    store: BaseStore
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our "agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)
    user_id = config["configurable"]["user_id"]

    model = load_chat_model(configuration.model).bind_tools(
        [COLLABORATE_WITH_TEAM, *MEMORY_TOOLS, *OTHER_TOOLS]
    )

    # Format the system prompt
    system_message = configuration.system_prompt.format(
        system_time=datetime.now(tz=timezone.utc).isoformat(),
        user_name=configuration.user_name,
        user_email=configuration.user_email,
        user_role=configuration.user_role
    )

    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state["messages"]], config
        ),
    )

    # Handle the case when it's the last step and the model still wants to use a tool
    if state["is_last_step"] and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not find an answer to your question in the specified number of steps.",
                )
            ]
        }

    # Return the model's response as a list to be added to existing messages
    return {"messages": [response]}


# Define a graph
workflow = StateGraph(State, input=InputState, config_schema=Configuration)

workflow.add_node("AZTROGENT", call_model)
workflow.add_node("linkedin_subgraph", linkedin_subgraph)
workflow.add_node("gmail_subgraph", gmail_subgraph)
workflow.add_node("github_subgraph", github_subgraph)
workflow.add_node("calendar_subgraph", calendar_subgraph)
workflow.add_node("memory_node", ToolNode(MEMORY_TOOLS))
workflow.add_node("web_search", ToolNode(OTHER_TOOLS))

workflow.add_edge(START, "AZTROGENT")
workflow.add_conditional_edges(
    "AZTROGENT",
    tools_condition,
    [
        "linkedin_subgraph",
        "memory_node",
        "web_search",
        "gmail_subgraph",
        "github_subgraph",
        "calendar_subgraph",
        END,
    ],
)
workflow.add_edge("linkedin_subgraph", "AZTROGENT")
workflow.add_edge("gmail_subgraph", "AZTROGENT")
workflow.add_edge("github_subgraph", "AZTROGENT")
workflow.add_edge("calendar_subgraph", "AZTROGENT")
workflow.add_edge("memory_node", "AZTROGENT")
workflow.add_edge("web_search", "AZTROGENT")

# Set up store and memory saver
store = InMemoryStore(
    index={
        "dims": settings.EMBED_MODEL_DIMENSIONS,
        "embed": settings.EMBEDDING_MODEL
    }
)
# Compile the workflow into an executable graph
graph = workflow.compile(store=store)
graph.name = "Aztrogent" 
