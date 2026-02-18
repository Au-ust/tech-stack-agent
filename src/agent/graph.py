"""
LangGraph Workflow Definition
"""
from langgraph.graph import StateGraph, END
from src.agent.state import TechStackState
from src.agent.nodes import (
    welcome_node,
    ask_project_type_node,
    ask_team_size_node,
    ask_timeline_node,
    ask_special_requirements_node,
    analyze_node,
    search_node,
    generate_node,
    save_node,
)


def should_search(state: TechStackState) -> str:
    """
    Conditional edge function to determine if search is needed.
    
    Args:
        state: Current workflow state
        
    Returns:
        Next node name ("search" or "generate")
    """
    needs_search = state.get("needs_search", False)
    return "search" if needs_search else "generate"


def create_workflow() -> StateGraph:
    """
    Create and compile the LangGraph workflow.
    
    Returns:
        Compiled workflow graph
    """
    # Initialize workflow
    workflow = StateGraph(TechStackState)
    
    # Add all nodes
    workflow.add_node("welcome", welcome_node)
    workflow.add_node("ask_type", ask_project_type_node)
    workflow.add_node("ask_team", ask_team_size_node)
    workflow.add_node("ask_timeline", ask_timeline_node)
    workflow.add_node("ask_special", ask_special_requirements_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("search", search_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("save", save_node)
    
    # Set entry point
    workflow.set_entry_point("welcome")
    
    # Define linear flow for questions
    workflow.add_edge("welcome", "ask_type")
    workflow.add_edge("ask_type", "ask_team")
    workflow.add_edge("ask_team", "ask_timeline")
    workflow.add_edge("ask_timeline", "ask_special")
    workflow.add_edge("ask_special", "analyze")
    
    # Conditional edge: search or skip to generation
    workflow.add_conditional_edges(
        "analyze",
        should_search,
        {
            "search": "search",
            "generate": "generate"
        }
    )
    
    # Continue from search to generation
    workflow.add_edge("search", "generate")
    
    # Final steps
    workflow.add_edge("generate", "save")
    workflow.add_edge("save", END)
    
    # Compile workflow
    return workflow.compile()


# Global workflow instance
_workflow_app = None


def get_workflow_app():
    """
    Get or create the compiled workflow application.
    
    Returns:
        Compiled LangGraph application
    """
    global _workflow_app
    if _workflow_app is None:
        _workflow_app = create_workflow()
    return _workflow_app
