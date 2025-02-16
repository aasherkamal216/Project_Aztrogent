from typing import Literal
from datetime import datetime

from calendar_agent.prompts import EMAIL_AGENT_PROMPT
from calendar_agent.state import GmailGraphState
from calendar_agent.models import gemini_model
from calendar_agent.tools import calendar_read_tools, calendar_write_tools, write_tools_by_name
from calendar_agent.configuration import Configuration

from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.types import Command, interrupt
from langchain_core.runnables import RunnableConfig


# Bind tools to the model
agent_with_tools = gemini_model.bind_tools(calendar_read_tools + calendar_write_tools)

## Main Calendar Agent
def calendar_agent(
    state: GoogleCalendarGraphState,
    config: RunnableConfig
) -> Command[Literal["retrieve_data", "action_executor" , "__end__"]]:

    configuration = Configuration.from_runnable_config(config)
    response = agent_with_tools.invoke(
        [
            SystemMessage(
                content=CALENDAR_AGENT_PROMPT.format(
                    user_name=configuration.user_name,
                    user_email=configuration.user_email,
                    timezone_offset=configuration.timezone_offset,
                )
            )
        ] + state["messages"]
    )

    # Check for tool calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        for call in response.tool_calls:
            tool_name = call.get("name")

            if tool_name in write_tools_by_name:
                # Route to Post Writer Agent
                return Command(
                    update={"messages": [response]}, 
                    goto="action_executor"
                )
        # Go to Read-operations Node
        return Command(
            goto="retrieve_data",
            update={"messages": [response]}
        )
    # End 
    return Command(update={"messages": [response]}, goto="__end__")

## Action Node to execute tool calls
def action_node(
    state: GoogleCalendarGraphState,
    config: RunnableConfig
) -> Command[Literal["calendar_agent"]]:

    tool_calls = state["messages"][-1].tool_calls
    result = []

    for call in tool_calls:
        tool_name = call["name"]
        args = call.get("args")
        
        while True:
            ## Confirm action by user
            action = interrupt({
                "tool_name": tool_name.replace("_", " ").title(),
                "confirmation": "Do you confirm the action? [y/n]: "
            })
            decision = list(action.values())[0].lower().strip()
            
            if decision == "y":
                output = write_tools_by_name[tool_name].invoke(args)
                break
            elif decision == "n":
                output = "User declined to perform this action."
                break
            else:
                print("Please enter 'y' or 'n'")
                continue
            
        result.append(ToolMessage(content=output, tool_call_id=call["id"], name=tool_name))
    
    return Command(
        goto="calendar_agent",
        update={"messages": result}
    )
