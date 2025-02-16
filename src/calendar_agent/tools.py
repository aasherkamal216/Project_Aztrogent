"""This module provides tools for the Email Agent.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated
from composio_langgraph import Action, ComposioToolSet

import os
from calendar_agent.configuration import Configuration


composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

calendar_write_tools = composio_toolset.get_tools(
    actions=[
        Action.GOOGLECALENDAR_CREATE_EVENT,
        Action.GOOGLECALENDAR_UPDATE_EVENT,
        Action.GOOGLECALENDAR_DELETE_EVENT,
        Action.GOOGLECALENDAR_QUICK_ADD,
    ]
)

calendar_read_tools = composio_toolset.get_tools(
    actions=[
        Action.GOOGLECALENDAR_FIND_EVENT,
        Action.GOOGLECALENDAR_FIND_FREE_SLOTS,
        Action.GOOGLECALENDAR_GET_CURRENT_DATE_TIME,
    ]
)

write_tools_by_name = {tool.name: tool for tool in calendar_write_tools}