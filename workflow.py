from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from agents import (
    analyze_fabric,
    generate_fashion_design,
    generate_collection_plan
)


# Shared state
class FashionWorkflowState(TypedDict):
    fabric_image: Any
    occasion: str
    audience: str
    budget: int
    fabric_analysis: Any
    fashion_design: Any
    collection_plan: Any


# Agent 1: Fabric Analysis
def fabric_analysis_node(state: FashionWorkflowState):

    result = analyze_fabric(state["fabric_image"])

    return {
        "fabric_analysis": result
    }


# Agent 2: Fashion Design
def fashion_design_node(state: FashionWorkflowState):

    result = generate_fashion_design(
        state["fabric_analysis"],
        state["occasion"],
        state["audience"],
        state["budget"]
    )

    return {
        "fashion_design": result
    }


# Agent 3: Collection Planning
def collection_planning_node(state: FashionWorkflowState):

    result = generate_collection_plan(
        state["fabric_analysis"],
        state["fashion_design"],
        state["occasion"],
        state["audience"],
        state["budget"]
    )

    return {
        "collection_plan": result
    }


# Create LangGraph workflow
builder = StateGraph(FashionWorkflowState)

# Register all three agents
builder.add_node("fabric_analysis", fabric_analysis_node)
builder.add_node("fashion_design", fashion_design_node)
builder.add_node("collection_planning", collection_planning_node)

# Define execution order
builder.add_edge(START, "fabric_analysis")
builder.add_edge("fabric_analysis", "fashion_design")
builder.add_edge("fashion_design", "collection_planning")
builder.add_edge("collection_planning", END)

# Compile workflow
fashion_workflow = builder.compile()