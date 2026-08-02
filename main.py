from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage, ToolMessage

from chains import first_responder, revisor
from tool_executor import execute_tools

MAX_ITERATIONS = 2

def draft_node(state: MessagesState) -> MessagesState:
    """Generate a draft answer."""
    response = first_responder.invoke({"messages": state["messages"]})
    return {"messages": [response]}

def revise_node(state: MessagesState) -> MessagesState:
    """Revise the answer."""
    response = revisor.invoke({"messages": state["messages"]})
    return {"messages": [response]}

def event_loop(state: MessagesState) -> MessagesState:
    count_tool_visits = sum(
        isinstance(msg, ToolMessage) for msg in state["messages"]
    )
    if count_tool_visits >= MAX_ITERATIONS:
        return END
    return "execute_tools"

builder = StateGraph(MessagesState)
builder.add_node("draft", draft_node)
builder.add_node("revise", revise_node)
builder.add_node("execute_tools", execute_tools)
builder.add_edge(START, "draft")
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")
builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])
graph = builder.compile()

res = graph.invoke({"messages": [
   {
    "role": "user",
    "content": "Write about AI-Powered SOC / autonomous soc problem domain, list startups that do that and raised funding."
   } 
]})

last_message = res["messages"][-1]

if isinstance(last_message, AIMessage) and last_message.tool_calls:
    print(last_message.tool_calls[0]["args"]["answer"])
print(res)