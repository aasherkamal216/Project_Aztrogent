from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END

from linkedin_agent.configuration import Configuration
from linkedin_agent.state import LinkedInGraphState
from langgraph.checkpoint.memory import MemorySaver
from linkedin_agent.nodes import (
    linkedin_agent,
    action_node,
    post_writer,
    human_feedback,
)

# Build graph
builder = StateGraph(LinkedInGraphState, config_schema=Configuration)

builder.add_node("linkedin_agent", linkedin_agent)
builder.add_node("action_executor", action_node)
builder.add_node("writer_agent", post_writer)
builder.add_node("human_feedback_node", human_feedback)

builder.add_edge(START, "linkedin_agent")

# Compile the builder into an executable graph
graph = builder.compile()

graph.name = "LinkedIn Agent"
