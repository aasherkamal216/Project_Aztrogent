from typing import Literal

from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import MessagesState

from linkedin_agent.graph import graph as linkedin_graph
from email_agent.graph import graph as gmail_graph
from github_agent.graph import graph as github_graph

######## LINKEDIN SUBGRAPH #########
def linkedin_subgraph(state: MessagesState):
    tool_calls = state["messages"][-1].tool_calls
    result = []
    for call in tool_calls:
        args = call.get("args")
        
        if args["team"] == "LinkedIn":
            
            response = linkedin_graph.invoke(
                {"messages": [HumanMessage(content=args["message"])]}
            )
            result.append(ToolMessage(content=response["messages"][-1].content,
            name=call["name"],
            tool_call_id=call["id"]))
    return {"messages": result}

######## GMAIL SUBGRAPH #########
def gmail_subgraph(state: MessagesState):
    tool_calls = state["messages"][-1].tool_calls
    result = []
    for call in tool_calls:
        args = call.get("args")
        
        if args["team"] == "Gmail":
            
            response = gmail_graph.invoke(
                {"messages": [HumanMessage(content=args["message"])]}
            )
            result.append(ToolMessage(content=response["messages"][-1].content,
            name=call["name"],
            tool_call_id=call["id"]))
    return {"messages": result}

######## GITHUB SUBGRAPH #########
def github_subgraph(state: MessagesState):
    tool_calls = state["messages"][-1].tool_calls
    result = []
    for call in tool_calls:
        args = call.get("args")
        
        if args["team"] == "GitHub":
            
            response = github_graph.invoke(
                {"messages": [HumanMessage(content=args["message"])]}
            )
            result.append(ToolMessage(content=response["messages"][-1].content,
            name=call["name"],
            tool_call_id=call["id"]))
    return {"messages": result}


def memory_node(state: MessagesState):
    pass