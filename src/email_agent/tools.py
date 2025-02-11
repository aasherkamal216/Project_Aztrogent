"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated
from composio_langgraph import Action, ComposioToolSet

import os
from email_agent.configuration import Configuration


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


TOOLS: List[Callable[..., Any]] = [search]

composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
gmail_tools = composio_toolset.get_tools(
    actions=[
        Action.GMAIL_SEND_EMAIL,
        Action.GMAIL_FETCH_EMAILS,
        Action.GMAIL_GET_PROFILE,
        Action.GMAIL_CREATE_EMAIL_DRAFT,
        Action.GMAIL_LIST_THREADS,
        Action.GMAIL_REPLY_TO_THREAD,
        Action.GMAIL_ADD_LABEL_TO_EMAIL,
    ]
)

tools_by_name = {tool.name: tool for tool in gmail_tools}