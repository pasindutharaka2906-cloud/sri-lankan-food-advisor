import os
import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from utils.rag_setup import get_retriever
from agents.prompts import ROUTER_PROMPT, RESEARCHER_PROMPT, CRITIC_PROMPT

# State Definition
class AgentState(TypedDict):
    query: str
    intent: str
    context: str
    research_notes: str
    final_response: str

# Retrieve keys securely
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.environ.get("OPENROUTER_API_KEY"))

def router_node(state: AgentState):
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)
    prompt = ROUTER_PROMPT.format(query=state["query"])
    response = llm.invoke([SystemMessage(content=prompt)])
    intent = response.content.strip()
    return {"intent": intent}

def researcher_node(state: AgentState):
    retriever = get_retriever()
    # Execute RAG
    docs = retriever.invoke(state["intent"] + " " + state["query"])
    context = "\n\n".join([doc.page_content for doc in docs])
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
    prompt = RESEARCHER_PROMPT.format(intent=state["intent"], query=state["query"], context=context)
    response = llm.invoke([SystemMessage(content=prompt)])
    
    return {"context": context, "research_notes": response.content}

def critic_node(state: AgentState):
    # Use OpenRouter for the critic node (Gemini/Claude)
    llm = ChatOpenAI(
        model="google/gemini-2.5-flash", 
        api_key=OPENROUTER_API_KEY, 
        base_url="https://openrouter.ai/api/v1"
    )
    prompt = CRITIC_PROMPT.format(research=state["research_notes"], query=state["query"])
    response = llm.invoke([SystemMessage(content=prompt)])
    
    return {"final_response": response.content}

# Build LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("critic", critic_node)

workflow.set_entry_point("router")
workflow.add_edge("router", "researcher")
workflow.add_edge("researcher", "critic")
workflow.add_edge("critic", END)

app_graph = workflow.compile()

def run_food_advisor(query: str) -> str:
    initial_state = {"query": query, "intent": "", "context": "", "research_notes": "", "final_response": ""}
    result = app_graph.invoke(initial_state)
    return result["final_response"]
