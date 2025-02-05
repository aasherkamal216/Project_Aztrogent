from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.types import Command, interrupt

from pydantic import BaseModel, Field
from typing import Literal

from langchain_core.messages import SystemMessage, HumanMessage
from src.linkedin_agent.prompts import ANALYST_PROMPT
from src.linkedin_agent.models import llama_model
from src.linkedin_agent.state import LinkedInGraphState

tavily_tool = TavilySearchResults(max_results=5)

def web_search(state: LinkedInGraphState) -> Command[Literal["post_writer"]]:
    # results = tavily_tool.invoke(state['messages'])

    return Command(
        # state update
        update={"context": "results"},
        goto="post_writer"
    )

def post_writer(state: LinkedInGraphState)-> Command[Literal["post_analyzer"]]:
    
    return Command(
        update={"post": state['messages'][-1]},
        goto="post_analyzer"
    )


class PostAnalystSchema(BaseModel):
    next_node: Literal["post_writer", "upload_post"]
    feedback: str = Field(description="The feedback about the post.")

post_analyst_llm = llama_model.with_structured_output(PostAnalystSchema)

def post_analyzer(state: LinkedInGraphState) -> Command[Literal["upload_post", "post_writer"]]:
    
    post_analysis = post_analyst_llm.invoke([SystemMessage(content=ANALYST_PROMPT)] + [state["post"]])

    user_feedback = ""
    if post_analysis.next_node == "post_writer":
        goto = "post_writer"
        user_feedback = interrupt("Please provide feedback about the post:")

    elif post_analysis.next_node == "upload_post":
        goto = "upload_post"

    return Command(
        update={"llm_feedback": post_analysis.feedback, 
                "user_feedback": user_feedback
               },
        goto=goto
    )


def upload_post(state: LinkedInGraphState) -> Command[Literal["__end__"]]:
    
    return Command(
        update={"messages": [HumanMessage(content="The post has successfully been posted!")]},
        goto="__end__"
    )
    