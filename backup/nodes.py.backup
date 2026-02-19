"""
LangGraph Node Implementations
"""
import json
from typing import Dict, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from src.agent.state import TechStackState
from src.utils.llm_client import get_llm_client
from src.tools.search import get_search_tool
from src.utils.file_manager import get_file_manager
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


def welcome_node(state: TechStackState) -> Dict[str, Any]:
    """
    Welcome node - greet user and explain the process.
    """
    console.print(Panel.fit(
        "[bold cyan]🚀 前端技术栈选型 Agent[/bold cyan]\n\n"
        "我将通过引导式问答帮助您选择最合适的前端技术栈。\n\n"
        "流程包括：\n"
        "1. 收集项目信息\n"
        "2. 分析技术需求\n"
        "3. 在线调研（如需要）\n"
        "4. 生成技术选型文档\n"
        "5. 保存文档到本地\n",
        title="欢迎",
        border_style="cyan"
    ))
    
    return {
        "current_step": "welcome",
        "messages": ["用户开始使用技术栈选型Agent"]
    }


def ask_project_type_node(state: TechStackState) -> Dict[str, Any]:
    """
    Ask for project type.
    """
    console.print("\n[bold yellow]问题 1/4[/bold yellow]")
    
    project_type = Prompt.ask(
        "请描述您的项目类型",
        default="Web应用",
        choices=["Web应用", "移动应用", "桌面应用", "小程序", "混合应用", "其他"]
    )
    
    return {
        "project_type": project_type,
        "current_step": "ask_type",
        "messages": [f"项目类型: {project_type}"]
    }


def ask_team_size_node(state: TechStackState) -> Dict[str, Any]:
    """
    Ask for team size.
    """
    console.print("\n[bold yellow]问题 2/4[/bold yellow]")
    
    team_size = Prompt.ask(
        "请选择您的团队规模",
        choices=["1-3人（小型团队）", "4-10人（中型团队）", "10人以上（大型团队）"],
        default="1-3人（小型团队）"
    )
    
    return {
        "team_size": team_size,
        "current_step": "ask_team",
        "messages": [f"团队规模: {team_size}"]
    }


def ask_timeline_node(state: TechStackState) -> Dict[str, Any]:
    """
    Ask for development timeline.
    """
    console.print("\n[bold yellow]问题 3/4[/bold yellow]")
    
    timeline = Prompt.ask(
        "请选择预期的开发时间线",
        choices=["1个月内", "1-3个月", "3-6个月", "6个月以上"],
        default="1-3个月"
    )
    
    return {
        "timeline": timeline,
        "current_step": "ask_timeline",
        "messages": [f"开发时间线: {timeline}"]
    }


def ask_special_requirements_node(state: TechStackState) -> Dict[str, Any]:
    """
    Ask for special requirements.
    """
    console.print("\n[bold yellow]问题 4/4[/bold yellow]")
    
    special_requirements = Prompt.ask(
        "请描述任何特殊需求（如SEO、高性能、实时通信等，按回车跳过）",
        default="无特殊需求"
    )
    
    return {
        "special_requirements": special_requirements,
        "current_step": "ask_special",
        "messages": [f"特殊需求: {special_requirements}"]
    }


def analyze_node(state: TechStackState) -> Dict[str, Any]:
    """
    Analyze user requirements using LLM.
    """
    console.print("\n[bold green]🔍 正在分析项目需求...[/bold green]")
    
    # Prepare project info
    project_info = {
        'project_type': state.get('project_type', ''),
        'team_size': state.get('team_size', ''),
        'timeline': state.get('timeline', ''),
        'special_requirements': state.get('special_requirements', ''),
    }
    
    # Get LLM client
    llm_client = get_llm_client()
    
    # Generate analysis prompt
    prompt = get_analysis_prompt(project_info)
    
    try:
        # Call LLM
        response = llm_client.invoke(prompt, system_message=ANALYSIS_SYSTEM_PROMPT)
        
        # Parse JSON response
        # Extract JSON from markdown code blocks if present
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.find("```") + 3
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response.strip()
        
        analysis_result = json.loads(json_str)
        
        # Display results
        console.print("\n[bold cyan]分析结果：[/bold cyan]")
        console.print(f"✓ 提取了 {len(analysis_result.get('extracted_requirements', []))} 个核心需求")
        console.print(f"✓ 识别了 {len(analysis_result.get('tech_constraints', []))} 个技术约束")
        console.print(f"✓ 是否需要在线搜索: {'是' if analysis_result.get('needs_search', False) else '否'}")
        
        return {
            "extracted_requirements": analysis_result.get('extracted_requirements', []),
            "tech_constraints": analysis_result.get('tech_constraints', []),
            "needs_search": analysis_result.get('needs_search', False),
            "current_step": "analyze",
            "messages": [f"需求分析完成: {len(analysis_result.get('extracted_requirements', []))} 个需求"]
        }
    
    except Exception as e:
        console.print(f"[red]分析失败: {str(e)}[/red]")
        # Fallback: no search needed
        return {
            "extracted_requirements": ["基于项目类型的标准需求"],
            "tech_constraints": ["团队学习曲线"],
            "needs_search": False,
            "current_step": "analyze",
            "messages": ["分析遇到错误，使用默认配置"]
        }


def search_node(state: TechStackState) -> Dict[str, Any]:
    """
    Perform online search for technology information.
    """
    console.print("\n[bold green]🌐 正在进行技术调研...[/bold green]")
    
    # Prepare project info and analysis result
    project_info = {
        'project_type': state.get('project_type', ''),
        'team_size': state.get('team_size', ''),
        'timeline': state.get('timeline', ''),
        'special_requirements': state.get('special_requirements', ''),
    }
    
    analysis_result = {
        'extracted_requirements': state.get('extracted_requirements', []),
        'tech_constraints': state.get('tech_constraints', []),
    }
    
    # Get LLM client and search tool
    llm_client = get_llm_client()
    search_tool = get_search_tool()
    
    try:
        # Generate search keywords using LLM
        prompt = get_search_keywords_prompt(project_info, analysis_result)
        response = llm_client.invoke(prompt, system_message=SEARCH_SYSTEM_PROMPT)
        
        # Parse JSON response
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.find("```") + 3
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response.strip()
        
        search_data = json.loads(json_str)
        keywords = search_data.get('search_keywords', [])
        
        console.print(f"生成了 {len(keywords)} 个搜索关键词")
        
        # Perform searches (limit to first 5 keywords to save time)
        all_results = []
        for keyword in keywords[:5]:
            console.print(f"  搜索: {keyword}")
            results = search_tool.search(keyword, max_results=3)
            all_results.extend(results)
        
        console.print(f"✓ 找到 {len(all_results)} 条相关信息")
        
        return {
            "search_results": all_results,
            "current_step": "search",
            "messages": [f"完成技术调研，收集了 {len(all_results)} 条信息"]
        }
    
    except Exception as e:
        console.print(f"[yellow]搜索遇到问题: {str(e)}，将继续使用已有知识生成文档[/yellow]")
        return {
            "search_results": [],
            "current_step": "search",
            "messages": ["搜索失败，使用LLM已有知识"]
        }


def generate_node(state: TechStackState) -> Dict[str, Any]:
    """
    Generate the complete technical document.
    """
    console.print("\n[bold green]📝 正在生成技术选型文档...[/bold green]")
    
    # Prepare all input data
    project_info = {
        'project_type': state.get('project_type', ''),
        'team_size': state.get('team_size', ''),
        'timeline': state.get('timeline', ''),
        'special_requirements': state.get('special_requirements', ''),
    }
    
    analysis_result = {
        'extracted_requirements': state.get('extracted_requirements', []),
        'tech_constraints': state.get('tech_constraints', []),
    }
    
    search_results = state.get('search_results', [])
    
    # Get LLM client
    llm_client = get_llm_client()
    
    try:
        # Generate document prompt
        prompt = get_generation_prompt(project_info, analysis_result, search_results)
        
        # Call LLM with streaming for better UX
        console.print("\n[dim]生成中...[/dim]")
        document_parts = []
        
        for chunk in llm_client.stream(prompt, system_message=GENERATOR_SYSTEM_PROMPT):
            document_parts.append(chunk)
        
        final_document = "".join(document_parts)
        
        console.print("✓ 文档生成完成")
        
        return {
            "final_document": final_document,
            "current_step": "generate",
            "messages": ["技术文档生成完成"]
        }
    
    except Exception as e:
        console.print(f"[red]文档生成失败: {str(e)}[/red]")
        # Generate a minimal fallback document
        fallback_doc = f"""# 技术栈选型文档

## 项目信息
- 项目类型: {project_info.get('project_type', '未知')}
- 团队规模: {project_info.get('team_size', '未知')}
- 时间线: {project_info.get('timeline', '未知')}

## 推荐技术栈
（文档生成遇到错误，请检查API配置后重试）
"""
        return {
            "final_document": fallback_doc,
            "current_step": "generate",
            "messages": ["文档生成失败，生成了简化版本"]
        }


def save_node(state: TechStackState) -> Dict[str, Any]:
    """
    Save the generated document to local file.
    """
    console.print("\n[bold green]💾 正在保存文档...[/bold green]")
    
    final_document = state.get('final_document', '')
    project_type = state.get('project_type', 'unknown')
    
    # Get file manager
    file_manager = get_file_manager()
    
    try:
        # Save document
        output_path = file_manager.save_document(
            content=final_document,
            project_name=project_type
        )
        
        console.print(f"✓ 文档已保存到: [cyan]{output_path}[/cyan]")
        
        # Show preview option
        if Confirm.ask("\n是否显示文档预览？", default=False):
            console.print("\n" + "="*80)
            console.print(final_document[:500] + "...\n（仅显示前500字符）")
            console.print("="*80)
        
        return {
            "output_path": output_path,
            "current_step": "save",
            "messages": [f"文档已保存: {output_path}"]
        }
    
    except Exception as e:
        console.print(f"[red]保存失败: {str(e)}[/red]")
        return {
            "output_path": "",
            "current_step": "save",
            "messages": ["保存失败"]
        }
