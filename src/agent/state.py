"""
LangGraph State Definition for Tech Stack Agent
"""
from typing import TypedDict, List, Optional, Dict, Any
from typing_extensions import Annotated
import operator


class TechStackState(TypedDict):
    """
    State object for the tech stack selection workflow.
    
    This state is passed between nodes in the LangGraph workflow.
    """
    
    # User Input Fields
    project_type: str  # e.g., "Web应用", "移动应用", "桌面应用"
    team_size: str  # e.g., "1-3人", "4-10人", "10人以上"
    timeline: str  # e.g., "1个月内", "3个月", "6个月以上"
    special_requirements: str  # 用户的特殊需求描述
    
    # Analysis Results
    extracted_requirements: List[str]  # 提取的核心技术需求
    tech_constraints: List[str]  # 技术约束条件
    
    # Search Results
    search_results: Annotated[List[Dict[str, Any]], operator.add]  # 搜索引擎返回的结果
    
    # Document Generation
    recommended_stack: Dict[str, Any]  # 推荐的技术栈（结构化数据）
    final_document: str  # 最终生成的完整Markdown文档
    
    # Control Flow
    current_step: str  # 当前执行的步骤
    needs_search: bool  # 是否需要进行在线搜索
    
    # Messages and History
    messages: Annotated[List[str], operator.add]  # 对话历史和日志
    
    # Output
    output_path: str  # 保存的文档路径
