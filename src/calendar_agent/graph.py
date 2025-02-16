"""Define a graph for custom Email Agent.
"""

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode

from calendar_agent.configuration import Configuration
from calendar_agent.state import GoogleCalendarGraphState
from calendar_agent.nodes import calendar_agent, action_node
from calendar_agent.tools import calendar_read_tools


# Build graph
builder = StateGraph(GoogleCalendarGraphState, config_schema=Configuration)

builder.add_node("calendar_agent", calendar_agent)
builder.add_node("retrieve_data", ToolNode(calendar_read_tools))
builder.add_node("action_executor", action_node)


builder.add_edge(START, "calendar_agent")
builder.add_edge("retrieve_data", "calendar_agent")

# Compile the builder into an executable graph
graph = builder.compile()
graph.name = "Google Calendar Agent"
