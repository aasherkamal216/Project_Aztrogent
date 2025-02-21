from typing import Literal
from datetime import datetime

from github_agent.prompts import GITHUB_AGENT_PROMPT
from github_agent.state import GitHubGraphState
from github_agent.models import model
from github_agent.tools import github_tools, tools_by_name
from github_agent.configuration import Configuration

from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.types import Command, interrupt
from langchain_core.runnables import RunnableConfig


## Bind tools to the model
agent_with_tools = model.bind_tools(github_tools)

def execute_tool(tool, args):
    MAX_RETRIES = 3
    retry_count = 0

    while retry_count < MAX_RETRIES:
        try:
            output = tool.invoke(args)
            return output
        except Exception as e:
            retry_count += 1
            continue
    return "Error: Tool Couldn't be called"

###### GitHub Agent ######
def github_agent(
    state: GitHubGraphState,
    config: RunnableConfig,
) -> Command[Literal["action_executor", "__end__"]]:

    configuration = Configuration.from_runnable_config(config)
    response = agent_with_tools.invoke(
        [
            SystemMessage(
                content=GITHUB_AGENT_PROMPT.format(
                    user_name=configuration.user_name,
                    github_username=configuration.github_username,
                    system_time=datetime.now().isoformat(),
                )
            )
        ] + state["messages"]
    )
    if hasattr(response, "tool_calls") and response.tool_calls:
        # Route to Action Executor
        return Command(goto="action_executor", update={"messages": [response]})
    # End of Conversation
    return Command(update={"messages": [response]}, goto="__end__")


###### Action Node to execute tool calls ######
def action_node(
    state: GitHubGraphState
) -> Command[Literal["github_agent"]]:

    tool_calls = state["messages"][-1].tool_calls
    result = []

    # Iterate through each tool call that needs to be executed
    for call in tool_calls:
        # Extract the tool name and arguments from the call
        tool_name = call["name"]
        args = call.get("args")
        
        while True:
            # Prompt user to confirm the action
            action = interrupt({
                "tool_name": tool_name.replace("_", " ").title(),  # Format tool name for display
                "confirmation": "Do you confirm the action? [y/n]: "
            })

            if action.lower().strip() == "y":
                # Retry logic in case of failures
                for attempt in range(3):
                    try:
                        output = tools_by_name[tool_name].invoke(args)
                        break
                    except Exception as e:

                        if attempt == 2:  # Last attempt
                            output = f"Tool call failed after 3 attempts. Last error: {str(e)}"
                
                break  # Break while loop after attempts complete

            elif action.lower().strip() == "n":
                # User declined the action
                output = "User declined to perform this action."
                break
            else:
                # Invalid input - prompt again
                print("Please enter 'y' or 'n'")
                continue
            
        # Add the tool execution result to the list
        result.append(ToolMessage(content=output, tool_call_id=call["id"], name=tool_name))
    return Command(
        goto="github_agent",
        update={"messages": result}
    )