"""This module provides tools for the Aztrogent.
"""

from typing import Any, Callable, List, Optional, Annotated, cast, Literal
from pydantic import BaseModel, Field

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg, tool
from langmem import create_manage_memory_tool, create_search_memory_tool

from aztrogent_agent.configuration import Configuration
from src.settings import settings

## Tool to Search the web
async def search(
    query: str, *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Optional[list[dict[str, Any]]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_runnable_config(config)
    wrapped = TavilySearchResults(max_results=configuration.max_search_results)
    result = await wrapped.ainvoke({"query": query})
    return cast(list[dict[str, Any]], result)


OTHER_TOOLS: List[Callable[..., Any]] = [search]

## Tool to delegate a task to colleague agents team.
@tool
class COLLABORATE_WITH_TEAM(BaseModel):
    """
    Tool to delegate a task to colleague agents team.
    Args:
        team (Literal["LinkedIn", "Gmail", "GitHub", "Calendar"]): The team name of the colleague agents
        message (str): The message / description of the task to be completed by the agents team.
    """
    team: Literal["LinkedIn", "Gmail", "GitHub", "Calendar"]
    message: str

## Tools to create / search / manage memories
MEMORY_TOOLS : list = [
    create_manage_memory_tool(namespace=("memories", settings.USER_MEMORY_ID)),
    create_search_memory_tool(namespace=("memories", settings.USER_MEMORY_ID))
]