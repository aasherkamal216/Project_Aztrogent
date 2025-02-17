"""This module provides tools for the Calendar Agent.
"""

from composio_langgraph import Action, ComposioToolSet
import os

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