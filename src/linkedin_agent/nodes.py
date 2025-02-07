from typing import Literal

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command, interrupt

from src.linkedin_agent.state import LinkedInGraphState
from src.linkedin_agent.prompts import POST_REFINER_PROMPT

## Post Writer Node
def post_writer(
    state: LinkedInGraphState,
) -> Command[Literal["web_search", "style_refiner"]]:

    response = "invoking llm for post writing..."
    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage):
        if last_message.tool_calls:
            return Command(goto="web_search")
    return Command(update={"post": response}, goto="style_refiner")

## Post Style Refiner Node
def style_refiner(state: LinkedInGraphState) -> Command[Literal["human_feedback"]]:
    prompt = POST_REFINER_PROMPT.format(post=state["post"])
    # response = gemini_model.invoke(prompt)

    return Command(update={"refined_post": "the refined post..."}, goto="human_feedback")

## Human Feedback Node (Human-in-the-loop)
def human_feedback(
    state: LinkedInGraphState,
) -> Command[Literal["upload_post", "style_refiner", "__end__"]]:

    review = interrupt(
        {"post": state["post"], "is_approved": "Do you approve the post? [y/n]: "}
    )
    if review['is_approved'].lower().strip() == "y":
        decision = interrupt({"decision": "Should I upload the post? [y/n]: "})

        if decision["decision"].lower().strip() == "y":
            return Command(update={"status": "uploading"}, goto="upload_post")

        elif decision["decision"].lower().strip() == "n":
            return Command(
                update={
                    "messages": [HumanMessage(content="The post has been written!")],
                    "status": "completed",
                },
                goto="__end__",
            )
    elif review['is_approved'].lower().strip() == "n":
        feedback = interrupt("Please provide feedback about the post: ")
        return Command(
            update={"user_feedback": feedback[next(iter(feedback))], "status": "refining"},
            goto="style_refiner",
        )

## Post Uploading Node
def upload_post(state: LinkedInGraphState) -> Command[Literal["__end__"]]:

    return Command(
        update={
            "messages": [
                HumanMessage(content="The post has successfully been posted!", name="LinkedIn Agent")
            ],
            "status": "completed",
        },
        goto="__end__",
    )
