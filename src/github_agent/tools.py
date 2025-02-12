"""This module contains tools for the GitHub Agent.
"""
import os
from composio_langgraph import Action, ComposioToolSet

composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

github_tools = composio_toolset.get_tools(
    actions=[
        Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER,
        Action.GITHUB_SEARCH_REPOSITORIES,
        Action.GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER,
        Action.GITHUB_LIST_REPOSITORIES_FOR_A_USER,
        Action.GITHUB_GET_THE_AUTHENTICATED_USER,
        Action.GITHUB_LIST_REPOSITORIES_STARRED_BY_A_USER,
        Action.GITHUB_LIST_USER_PROJECTS,
        Action.GITHUB_LIST_FOLLOWERS_OF_A_USER
    ]
)

tools_by_name = {tool.name: tool for tool in github_tools}
