"""
LangGraph Node Implementations - 表单式重构版
实现 表单填充 -> 需求分析 -> 搜索(可选) -> 生成文档 -> 保存
"""
import json
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from src.agent.state import TechStackState
from src.utils.llm_client import get_llm_client
from src.tools.search import get_search_tool
from src.utils.file_manager import get_file_manager
from src.forms.collector import collect_form, form_data_to_project_info
from src.prompts.analyzer import (
    ANALYSIS_SYSTEM_PROMPT,
    get_analysis_prompt,
)
from src.prompts.searcher import (
    SEARCH_SYSTEM_PROMPT,
    get_search_keywords_prompt,
)
from src.prompts.generator import (
    GENERATOR_SYSTEM_PROMPT,
    get_generation_prompt,
)

console = Console()


# ===== 表单收集节点 =====

def form_collect_node(state: TechStackState) -> Dict[str, Any]:
    """
    表单收集节点 - 用户通过结构化表单填写需求
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]前端技术栈选型 Agent[/bold green]\n"
        "[dim]请按提示填写，可回车跳过使用默认值[/dim]",
        border_style="green"
    ))
    
    form_data = collect_form()
    project_info = form_data_to_project_info(form_data)
    
    return {
        "form_data": form_data,
        "project_type": project_info.get("project_type", "Web-C端"),
        "team_size": project_info.get("team_size", "1人"),
        "timeline": project_info.get("timeline", "未指定"),
        "special_requirements": project_info.get("special_requirements", ""),
        "current_step": "form_collect",
        "messages": ["表单收集完成"],
    }


# ===== 分析节点 =====

def analyze_node(state: TechStackState) -> Dict[str, Any]:
    """
    分析节点 - 基于 form_data 进行技术需求分析
    """
    console.print("\n[bold green]🔍 正在分析技术需求...[/bold green]")
    
    form_data = state.get("form_data", {})
    project_info = form_data_to_project_info(form_data)
    
    llm_client = get_llm_client()
    
    try:
        prompt = get_analysis_prompt(project_info)
        response = llm_client.invoke(prompt, system_message=ANALYSIS_SYSTEM_PROMPT)
        analysis_result = _parse_json_response(response)
        
        console.print("✓ 分析完成")
        
        return {
            "extracted_requirements": analysis_result.get("extracted_requirements", []),
            "tech_constraints": analysis_result.get("tech_constraints", []),
            "needs_search": analysis_result.get("needs_search", False),
            "current_step": "analyze",
            "messages": ["需求分析完成"],
        }
    
    except Exception as e:
        console.print(f"[yellow]分析遇到错误: {str(e)}[/yellow]")
        return {
            "extracted_requirements": ["基于项目类型的标准需求"],
            "tech_constraints": ["团队学习曲线"],
            "needs_search": False,
            "current_step": "analyze",
            "messages": ["使用默认分析"],
        }


# ===== 搜索节点 =====

def search_node(state: TechStackState) -> Dict[str, Any]:
    """搜索节点 - 在线技术调研"""
    console.print("\n[bold green]🌐 正在进行技术调研...[/bold green]")
    
    form_data = state.get("form_data", {})
    project_info = form_data_to_project_info(form_data)
    
    analysis_result = {
        "extracted_requirements": state.get("extracted_requirements", []),
        "tech_constraints": state.get("tech_constraints", []),
    }
    
    llm_client = get_llm_client()
    search_tool = get_search_tool()
    
    try:
        prompt = get_search_keywords_prompt(project_info, analysis_result)
        response = llm_client.invoke(prompt, system_message=SEARCH_SYSTEM_PROMPT)
        search_data = _parse_json_response(response)
        keywords = search_data.get("search_keywords", [])
        
        console.print(f"生成了 {len(keywords)} 个搜索关键词")
        
        all_results = []
        for keyword in keywords[:8]:
            console.print(f"  搜索: {keyword}")
            results = search_tool.search(keyword, max_results=3)
            all_results.extend(results)
        
        console.print(f"✓ 找到 {len(all_results)} 条相关信息")
        
        return {
            "search_results": all_results,
            "current_step": "search",
            "messages": ["技术调研完成"],
        }
    
    except Exception as e:
        console.print(f"[yellow]搜索失败: {str(e)}[/yellow]")
        return {
            "search_results": [],
            "current_step": "search",
            "messages": ["搜索失败"],
        }


# ===== 生成节点 =====

def generate_node(state: TechStackState) -> Dict[str, Any]:
    """
    文档生成节点 - 基于 form_data + 分析结果生成技术方案文档
    """
    console.print("\n[bold green]📝 正在生成技术方案文档...[/bold green]")
    
    form_data = state.get("form_data", {})
    project_info = form_data_to_project_info(form_data)
    project_info["form_data"] = form_data
    
    analysis_result = {
        "extracted_requirements": state.get("extracted_requirements", []),
        "tech_constraints": state.get("tech_constraints", []),
    }
    
    search_results = state.get("search_results", [])
    
    llm_client = get_llm_client()
    
    try:
        prompt = get_generation_prompt(project_info, analysis_result, search_results)
        
        console.print("\n[dim]生成中...[/dim]")
        document_parts = []
        
        for chunk in llm_client.stream(prompt, system_message=GENERATOR_SYSTEM_PROMPT):
            document_parts.append(chunk)
        
        final_document = "".join(document_parts)
        
        console.print("✓ 文档生成完成")
        
        return {
            "final_document": final_document,
            "current_step": "generate",
            "messages": ["技术文档生成完成"],
        }
    
    except Exception as e:
        console.print(f"[red]文档生成失败: {str(e)}[/red]")
        
        fallback_doc = _generate_fallback_document(state)
        
        return {
            "final_document": fallback_doc,
            "current_step": "generate",
            "messages": ["使用降级文档"],
        }


# ===== 保存节点 =====

def save_node(state: TechStackState) -> Dict[str, Any]:
    """保存节点"""
    console.print("\n[bold green]💾 正在保存文档...[/bold green]")
    
    final_document = state.get("final_document", "")
    project_type = state.get("project_type", "unknown")
    
    file_manager = get_file_manager()
    
    try:
        output_path = file_manager.save_document(
            content=final_document,
            project_name=project_type,
        )
        
        console.print(f"✓ 文档已保存到: [cyan]{output_path}[/cyan]")
        
        if Confirm.ask("\n是否显示文档预览？", default=False):
            console.print("\n" + "=" * 80)
            console.print(final_document[:500] + "...\n（仅显示前500字符）")
            console.print("=" * 80)
        
        return {
            "output_path": output_path,
            "current_step": "save",
            "messages": [f"文档已保存: {output_path}"],
        }
    
    except Exception as e:
        console.print(f"[red]保存失败: {str(e)}[/red]")
        return {
            "output_path": "",
            "current_step": "save",
            "messages": ["保存失败"],
        }


# ===== 辅助函数 =====

def _parse_json_response(response: str) -> Dict[str, Any]:
    """
    解析 LLM 的 JSON 响应（鲁棒版本）
    """
    if "```json" in response:
        json_start = response.find("```json") + 7
        json_end = response.find("```", json_start)
        if json_end > json_start:
            json_str = response[json_start:json_end].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
    
    if "```" in response:
        json_start = response.find("```") + 3
        json_end = response.find("```", json_start)
        if json_end > json_start:
            json_str = response[json_start:json_end].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
    
    def find_json_objects(text):
        results = []
        stack = []
        start_idx = None
        in_string = False
        escape_next = False
        
        for i, char in enumerate(text):
            if escape_next:
                escape_next = False
                continue
            if char == "\\":
                escape_next = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if char == "{":
                if not stack:
                    start_idx = i
                stack.append("{")
            elif char == "}":
                if stack:
                    stack.pop()
                    if not stack and start_idx is not None:
                        results.append(text[start_idx : i + 1])
                        start_idx = None
        
        return results
    
    json_objects = find_json_objects(response)
    
    for obj in sorted(json_objects, key=len, reverse=True):
        try:
            parsed = json.loads(obj)
            if isinstance(parsed, dict) and len(parsed) > 0:
                return parsed
        except json.JSONDecodeError:
            continue
    
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    
    raise ValueError(
        f"无法从LLM响应中提取有效JSON。\n"
        f"响应长度: {len(response)} 字符\n"
        f"响应前200字符: {response[:200]}\n"
        f"响应后200字符: {response[-200:]}"
    )


def _generate_fallback_document(state: Dict[str, Any]) -> str:
    """生成降级文档"""
    form_data = state.get("form_data", {})
    project_type = state.get("project_type", "未知")
    team_size = state.get("team_size", "未知")
    core_features = form_data.get("core_features", "")
    key_features = form_data.get("key_features", "")
    
    return f"""# 技术方案文档

## 模版声明

本方案因生成过程遇到错误，采用简化版本。请检查 API 配置后重试。

## ChangeLog

| 版本号 | 变更人 | 变更时间 | 变更备注 |
|--------|--------|----------|----------|
| V 1.0 | Agent | {__import__('datetime').datetime.now().strftime('%Y-%m-%d')} | 降级文档 |

## 1. 业务背景和目标

### 1.1 需求背景

- 项目类型: {project_type}
- 团队规模: {team_size}
- 核心功能: {core_features or '未填写'}
- 关键特性: {key_features or '未填写'}

## 3. 整体技术方案

### 3.1 技术调研和选型

（文档生成遇到错误，请重试获取完整方案）

---
生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
