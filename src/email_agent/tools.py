"""This module provides tools for the Email Agent.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated
from composio_langgraph import Action, ComposioToolSet

import os
from email_agent.configuration import Configuration

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