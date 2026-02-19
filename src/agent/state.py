"""
LangGraph State Definition for Tech Stack Agent - 表单式重构版
仅保留 form_data、分析结果、文档，移除 AI 理解相关字段
"""
from typing import TypedDict, List, Dict, Any
from typing_extensions import Annotated
import operator


class TechStackState(TypedDict):
    """
    State object for the tech stack selection workflow.
    
    表单式流程：form_data -> analyze -> search? -> generate -> save
    """
    
    # ===== 表单数据 =====
    form_data: Dict[str, Any]  # 用户填写的结构化表单数据
    
    # ===== 分析结果 =====
    extracted_requirements: List[str]  # 提取的核心技术需求
    tech_constraints: List[str]  # 技术约束条件
    needs_search: bool  # 是否需要进行在线搜索
    
    # ===== 搜索结果 =====
    search_results: Annotated[List[Dict[str, Any]], operator.add]  # 搜索引擎返回的结果
    
    # ===== 文档生成 =====
    final_document: str  # 最终生成的完整 Markdown 文档
    
    # ===== 控制流程 =====
    current_step: str  # 当前执行的步骤
    
    # ===== 消息和历史 =====
    messages: Annotated[List[str], operator.add]  # 对话历史和日志
    
    # ===== 输出 =====
    output_path: str  # 保存的文档路径
    
    # ===== 兼容性字段（供 analyzer/generator 使用） =====
    project_type: str
    team_size: str
    timeline: str
    special_requirements: str
