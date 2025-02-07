from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from src.linkedin_agent.configuration import Configuration
from src.linkedin_agent.tools import search
from src.linkedin_agent.state import LinkedInGraphState
from src.linkedin_agent.nodes import post_writer, style_refiner, human_feedback, upload_post

# Build graph
builder = StateGraph(LinkedInGraphState)

builder.add_node("post_writer", post_writer)
builder.add_node("web_search", ToolNode([search]))
builder.add_node("style_refiner", style_refiner)
builder.add_node("human_feedback", human_feedback)
builder.add_node("upload_post", upload_post)

builder.add_edge(START, "post_writer")
builder.add_edge("web_search", "post_writer")

# Compile the builder into an executable graph
graph = builder.compile()

graph.name = "LinkedIn Agent"  # This customizes the name in LangSmith
