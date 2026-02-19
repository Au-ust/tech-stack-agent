"""
表单收集逻辑 - 使用 InquirerPy 驱动 CLI 交互
"""
from typing import Dict, Any, Optional
from pathlib import Path

from src.forms.schema import FIELD_DEFINITIONS, GROUP_ORDER, GROUP_LABELS


def _get_default(field_id: str) -> Any:
    """获取字段默认值"""
    defn = FIELD_DEFINITIONS.get(field_id, {})
    return defn.get("default")


def collect_form(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    收集用户填写的表单数据
    
    Args:
        config_path: 可选，指定 defaults.yaml 路径
        
    Returns:
        表单数据字典，未填项为空字符串或默认值
    """
    try:
        from InquirerPy import inquirer
    except ImportError:
        return _collect_form_fallback()
    
    result: Dict[str, Any] = {}
    
    for group in GROUP_ORDER:
        fields = [
            (fid, defn)
            for fid, defn in FIELD_DEFINITIONS.items()
            if defn.get("group") == group
        ]
        if not fields:
            continue
        
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        console.print(Panel.fit(f"[bold cyan]{GROUP_LABELS.get(group, group)}[/bold cyan]", border_style="cyan"))
        
        for field_id, defn in fields:
            msg = defn.get("message", field_id)
            field_type = defn.get("type", "text")
            default = defn.get("default")
            
            if field_type == "list":
                choices = defn.get("choices", [])
                val = inquirer.select(
                    message=msg,
                    choices=choices,
                    default=default or choices[0] if choices else None,
                ).execute()
            elif field_type == "number":
                try:
                    raw = inquirer.text(
                        message=f"{msg}（回车使用默认值 {default}）",
                        default=str(default) if default is not None else "1",
                    ).execute()
                    val = int(raw) if raw else (default or 1)
                except (ValueError, TypeError):
                    val = default or 1
            elif field_type == "textarea":
                val = inquirer.text(
                    message=f"{msg}（可回车跳过）",
                    default="",
                ).execute()
                val = (val or "").strip()
            else:
                val = inquirer.text(
                    message=f"{msg}（可回车跳过）",
                    default=default or "",
                ).execute()
                val = (val or "").strip()
            
            result[field_id] = val
    
    return result


def _collect_form_fallback() -> Dict[str, Any]:
    """
    当 InquirerPy 未安装时的降级方案，使用 Rich Prompt
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    
    console = Console()
    result: Dict[str, Any] = {}
    
    for group in GROUP_ORDER:
        fields = [
            (fid, defn)
            for fid, defn in FIELD_DEFINITIONS.items()
            if defn.get("group") == group
        ]
        if not fields:
            continue
        
        console.print(Panel.fit(f"[bold cyan]{GROUP_LABELS.get(group, group)}[/bold cyan]", border_style="cyan"))
        
        for field_id, defn in fields:
            msg = defn.get("message", field_id)
            field_type = defn.get("type", "text")
            default = defn.get("default")
            choices = defn.get("choices", [])
            
            if field_type == "list":
                choices_str = " / ".join(choices)
                hint = f"（{choices_str}）"
                while True:
                    raw = Prompt.ask(f"{msg} {hint}", default=default or choices[0] if choices else "")
                    if raw in choices:
                        result[field_id] = raw
                        break
                    if not raw and default:
                        result[field_id] = default
                        break
                    console.print("[yellow]请从选项中选择[/yellow]")
            elif field_type == "number":
                try:
                    raw = Prompt.ask(f"{msg}", default=str(default or 1))
                    result[field_id] = int(raw) if raw else (default or 1)
                except (ValueError, TypeError):
                    result[field_id] = default or 1
            else:
                val = Prompt.ask(f"{msg}（可回车跳过）", default="")
                result[field_id] = (val or "").strip()
    
    return result


def form_data_to_project_info(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    将 form_data 转换为 analyzer/generator 所需的 project_info 格式
    """
    return {
        "project_type": form_data.get("project_type", "Web-C端"),
        "project_stage": form_data.get("project_stage", "全新开发"),
        "frontend_count": form_data.get("frontend_count", 1),
        "existing_stack": form_data.get("existing_stack", ""),
        "package_json": form_data.get("package_json", ""),
        "core_features": form_data.get("core_features", ""),
        "key_features": form_data.get("key_features", ""),
        "dev_preference": form_data.get("dev_preference", ""),
        "forbidden_items": form_data.get("forbidden_items", ""),
        # 兼容旧字段
        "team_size": str(form_data.get("frontend_count", 1)) + "人",
        "timeline": "未指定",
        "special_requirements": form_data.get("key_features", "") or form_data.get("core_features", ""),
    }
