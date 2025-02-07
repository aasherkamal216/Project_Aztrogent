"""Define the state structures for the agent."""

from __future__ import annotations

from langgraph.graph import MessagesState
from typing import Literal

## Graph State
class LinkedInGraphState(MessagesState):
    post: str
    user_feedback: str
    refined_post: str
    status: Literal["refining", "uploading", "completed"]

