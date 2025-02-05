from typing import Literal

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END

from src.linkedin_agent.configuration import Configuration
from src.linkedin_agent.state import LinkedInGraphState
from src.linkedin_agent.nodes import web_search, post_writer, post_analyzer, upload_post


def task_router(state: LinkedInGraphState) -> Literal["post_writer", "web_search"]:
    """Determine the next node based on the model's output.

    This function checks if the model's last message contains tool calls.

    Args:
        state (State): The current state of the conversation.

    Returns:
        str: The name of the next node to call ("post_writer" or "web_search").
    """
    if state.get("feedback"):
        return "post_writer"
    return "web_search"


# Build graph
builder = StateGraph(LinkedInGraphState, config_schema=Configuration)

builder.add_node("post_writer", post_writer)
builder.add_node("web_search", web_search)
builder.add_node("post_analyzer", post_analyzer)
builder.add_node("upload_post", upload_post)

builder.add_conditional_edges(START, task_router)

# Compile the builder into an executable graph
graph = builder.compile(interrupt_before=["upload_post"])

graph.name = "LinkedIn Agent"  # This customizes the name in LangSmith
