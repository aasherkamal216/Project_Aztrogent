"""Define a graph for custom Email Agent.
"""

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START

from email_agent.configuration import Configuration
from email_agent.state import GmailGraphState
from email_agent.nodes import gmail_agent, action_node


builder = StateGraph(GmailGraphState, config_schema=Configuration)
# Build graph
builder = StateGraph(GmailGraphState)

builder.add_node("gmail_agent", gmail_agent)
builder.add_node("action_executor", action_node)


builder.add_edge(START, "gmail_agent")

# Compile the builder into an executable graph
graph = builder.compile()
graph.name = "Email Agent"
