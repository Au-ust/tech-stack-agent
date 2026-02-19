"""
LangGraph Workflow Definition - 表单式重构版
流程：表单收集 -> 需求分析 -> 搜索(可选) -> 生成文档 -> 保存
"""
from langgraph.graph import StateGraph, END
from src.agent.state import TechStackState
from src.agent.nodes import (
    form_collect_node,
    analyze_node,
    search_node,
    generate_node,
    save_node,
)


def should_search(state: TechStackState) -> str:
    """判断是否需要在线搜索"""
    needs_search = state.get("needs_search", False)
    return "search" if needs_search else "generate"


def create_workflow() -> StateGraph:
    """
    创建并编译 LangGraph 工作流
    
    流程：form_collect -> analyze -> (search | generate) -> save -> END
    """
    workflow = StateGraph(TechStackState)
    
    workflow.add_node("form_collect", form_collect_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("search", search_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("save", save_node)
    
    workflow.set_entry_point("form_collect")
    
    workflow.add_edge("form_collect", "analyze")
    
    workflow.add_conditional_edges(
        "analyze",
        should_search,
        {
            "search": "search",
            "generate": "generate",
        },
    )
    
    workflow.add_edge("search", "generate")
    workflow.add_edge("generate", "save")
    workflow.add_edge("save", END)
    
    return workflow.compile()


_workflow_app = None


def get_workflow_app():
    """获取或创建编译后的工作流应用"""
    global _workflow_app
    if _workflow_app is None:
        _workflow_app = create_workflow()
    return _workflow_app
