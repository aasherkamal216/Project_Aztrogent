"""Define the state structures for the agent."""

from __future__ import annotations

from langgraph.graph import MessagesState

from typing import Literal, Annotated
import operator

## Graph State
class LinkedInGraphState(MessagesState):
    posts: Annotated[list, operator.add]
    human_feedback: str
    writer_task: str
    status: Literal["writing", "rewriting", "completed"]