from typing import Literal
from datetime import datetime

from email_agent.prompts import EMAIL_AGENT_PROMPT
from email_agent.state import GmailGraphState
from email_agent.models import gemini_model
from email_agent.tools import tools_by_name, gmail_tools
from email_agent.configuration import Configuration

from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.types import Command, interrupt
from langchain_core.runnables import RunnableConfig


## Bind tools to the model
agent_with_tools = gemini_model.bind_tools(gmail_tools)

## Main Gmail Agent
def gmail_agent(
    state: GmailGraphState,
    config: RunnableConfig,
) -> Command[Literal["action_executor", "__end__"]]:

    configuration = Configuration.from_runnable_config(config)
    response = agent_with_tools.invoke(
        [
            SystemMessage(
                content=EMAIL_AGENT_PROMPT.format(
                    user_name=configuration.user_name,
                    user_email=configuration.user_email,
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


## Action Node to execute tool calls
def action_node(
    state: GmailGraphState, config: RunnableConfig
) -> Command[Literal["gmail_agent"]]:

    tool_calls = state["messages"][-1].tool_calls
    result = []

    for call in tool_calls:
        tool_name = call["name"]
        args = call.get("args")
        ## Confirm action by user
        action = interrupt({
            "tool_name": tool_name.replace("_", " ").title() ,
            "confirmation": "Do you confirm the action? [y/n]: "
            })
        decision = next(iter(action))
        if decision.lower().strip() == "y":
            output = tools_by_name[tool_name].invoke(args)
            result.append(ToolMessage(content=output, tool_call_id=call["id"], name=tool_name))
        elif decision.lower().strip() == "n":
            output = "User declined to perform this action."

            result.append(ToolMessage(content=output, tool_call_id=call["id"], name=tool_name))
    return Command(
        goto="gmail_agent",
        update={"messages": result}
    )
