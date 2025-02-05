"""Define the state structures for the agent."""

from __future__ import annotations

from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages

## Graph State
class LinkedInGraphState(MessagesState):
    task: str
    critique: str
    post: str
    user_feedback: str
    llm_feedback: str
    context: list

