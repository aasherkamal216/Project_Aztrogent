import os
from composio_langgraph import Action, ComposioToolSet
import logging

def init_composio_toolset():
    
    # Configure logging to write to a file
    logging.basicConfig(
        level=logging.INFO,
        filename='github_agent.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
        logger.info("ComposioToolSet initialized successfully.")
        return composio_toolset.get_tools(
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
    
    except Exception as e:
        logger.error(f"Error initializing ComposioToolSet: {e}")
