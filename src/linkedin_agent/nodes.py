from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.types import Command, interrupt
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import RunnableConfig

from linkedin_agent.configuration import Configuration
from linkedin_agent.state import LinkedInGraphState
from linkedin_agent.prompts import LINKEDIN_AGENT_PROMPT, POST_WRITER_PROMPT
from linkedin_agent.models import llama_model
from linkedin_agent.tools import tools_by_name, linkedin_tools, POST_WRITER, search

## Bind tools to the main agent
main_linkedin_agent = llama_model.bind_tools([POST_WRITER] + linkedin_tools)

## Main LinkedIn Agent
def linkedin_agent(
    state: LinkedInGraphState,
    config: RunnableConfig,
) -> Command[Literal["writer_agent", "__end__", "action_executor"]]:
    configuration = Configuration.from_runnable_config(config)
    # Calling the main LinkedIn Agent
    response = main_linkedin_agent.invoke(
        [
            SystemMessage(
                content=LINKEDIN_AGENT_PROMPT.format(author_id=configuration.author_id)
            )
        ]
        + state["messages"]
    )
    # Check for tool calls
    if hasattr(response, "tool_calls") and response.tool_calls:
        for call in response.tool_calls:
            tool_name = call.get("name")
            args = call.get("args")
            if tool_name == "POST_WRITER":
                # Route to Post Writer Agent
                return Command(
                    update={"writer_task": args["task"], "messages": [response], "status": "writing"}, 
                    goto="writer_agent"
                )
        # Route to Action Executor to Upload/Delete a post
        return Command(
            goto="action_executor",
            update={"messages": [response]}
        )
    # End of Conversation
    return Command(
        update={"messages": [response]},
        goto="__end__"
    )

## Post Writer Agent
def post_writer(
    state: LinkedInGraphState
) -> Command[Literal["human_feedback_node"]]:

    human_feedback = state.get("human_feedback", None)
    task = state['writer_task']

    post_writer_agent = create_react_agent(
        llama_model,
        tools=[search],
        prompt=POST_WRITER_PROMPT
        )
    # Check if human feedback is available
    if human_feedback:
        prompt = (
            "## Post \n\n{post}\n\n"
            "## Feedback \n\n{human_feedback}"
        )
        message = HumanMessage(content=prompt.format(post=state["posts"][-1], human_feedback=human_feedback))
    else:
        message = HumanMessage(content=task)  # task to write post

    # Invoke the writer agent
    response = post_writer_agent.invoke({"messages": [message]})
    post = response["messages"][-1].content
    # Go to Human Node to get feedback
    return Command(
        update={"posts": [post]},
        goto="human_feedback_node"
    )

## Human Feedback Node
def human_feedback(
    state: LinkedInGraphState,
) -> Command[Literal["linkedin_agent", "writer_agent"]]:

    post = state["posts"][-1]  # Most recent version of the post
    action = interrupt(
        {"post": post, "is_approved": "Do you approve the post? [y/n]: "}
    )

    # If user approves the post
    if action["is_approved"].lower().strip() == "y":
        last_message = state["messages"][-1]  # LinkedIn Agent tool call
        tool_messages = []

        for call in last_message.tool_calls:
            tool_name = call.get("name")
            tool_id = call.get("id")

            if tool_name == "POST_WRITER":
                tool_msg = ToolMessage(
                    name=tool_name,
                    tool_call_id=tool_id,
                    content="Task completed! Here is the post: \n\n" + state["posts"][-1],
                )
                tool_messages.append(tool_msg)

        # Route to Main LinkedIn Agent with tool message
        return Command(
                update={"messages": tool_messages},
                goto="linkedin_agent"
            )
    # If user doesn't approve the post
    elif action["is_approved"].lower().strip() == "n":
        feedback = interrupt("Please provide feedback about the post: ")
        # Route back to writer agent with feedback
        return Command(
            update={"human_feedback": feedback, "status": "rewriting"},
            goto="writer_agent",
        )

## Action Node for uploading and deleting posts
def action_node(state: LinkedInGraphState) -> Command[Literal["linkedin_agent"]]:

    def execute_tool(tool_call):
        """Executes the given tool call and returns a ToolMessage."""
        tool = tools_by_name[tool_call["name"]]
        output = tool.invoke(tool_call["args"])
        return ToolMessage(content=output, name=tool_call["name"], tool_call_id=tool_call["id"])

    result = []
    ## Confirmation messages for tools
    confirmation_messages = {
        "LINKEDIN_CREATE_LINKED_IN_POST": {
            "post": lambda args: args["commentary"],
            "confirmation": "Should I upload the post? [y/n]: "
        },
        "LINKEDIN_DELETE_LINKED_IN_POST": {
            "confirmation": "Do you confirm the action of deleting the post? [y/n]: "
        }
    }

    for tool_call in state["messages"][-1].tool_calls:
        tool_name = tool_call["name"]

        if tool_name in confirmation_messages:
            confirmation_data = confirmation_messages[tool_name]
            prompt_data = {"confirmation": confirmation_data["confirmation"]}
            if "post" in confirmation_data:
                prompt_data["post"] = confirmation_data["post"](tool_call["args"])

            action = interrupt(prompt_data)

            if action["confirmation"].lower().strip() == "y":
                result.append(execute_tool(tool_call))
            elif action["confirmation"].lower().strip() == "n":
                result.append(
                    ToolMessage(
                        content="User declined to upload the post.",
                        name=tool_name,
                        tool_call_id=tool_call["id"],
                    )
                )
        else:
            result.append(execute_tool(tool_call))
    # Go to Main LinkedIn Agent
    return Command(
        update={"messages": result, "status": "completed"}, goto="linkedin_agent"
    )
