"""Define a graph for custom Email Agent.
"""

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START

from github_agent.configuration import Configuration
from github_agent.state import GitHubGraphState
from github_agent.nodes import github_agent, action_node


# Build graph
builder = StateGraph(GitHubGraphState, config_schema=Configuration)

builder.add_node("github_agent", github_agent)
builder.add_node("action_executor", action_node)

builder.add_edge(START, "github_agent")

# Compile the builder into an executable graph
graph = builder.compile()
graph.name = "GitHub Agent"
