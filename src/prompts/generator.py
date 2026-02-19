"""
Prompt templates for document generation - 表单式适配
输出采用《前端技术方案模版》结构，注入选型指南和模版
"""
from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent
_SELECTION_GUIDE_PATH = _PROMPTS_DIR / "selection_guide.md"
_TECH_TEMPLATE_PATH = _PROMPTS_DIR / "tech_solution_template.md"


def _load_file(path: Path) -> str:
    """加载文件内容"""
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


SELECTION_GUIDE = _load_file(_SELECTION_GUIDE_PATH)
TECH_SOLUTION_TEMPLATE = _load_file(_TECH_TEMPLATE_PATH)

GENERATOR_SYSTEM_PROMPT = f"""你是一位专业的技术文档撰写专家，擅长编写清晰、全面、结构化的企业级技术方案文档。
你的文档能够帮助技术团队和管理层快速理解技术方案，做出明智的决策。
你的写作风格专业、客观，注重数据支撑和实际案例。

## 选型参考（必读）

以下《前端技术栈选型指南》作为你选型推荐的重要参考：

---
{SELECTION_GUIDE[:8000]}
---

## 输出模版（必须遵循）

请按照以下《前端技术方案模版》结构生成文档。**非每项必填**，按方案相关性选择填写；用户未指出、本次未涉及的部分注明「用户未指出但可能需要保留」。

---
{TECH_SOLUTION_TEMPLATE[:6000]}
---

## 核心要求

1. **3.1 技术调研和选型** 必须包含 2+ 套方案对比，每套写明：投放场景、容器类型、开发模式、模块方案
2. 最后给出**明确建议**
3. 在保证基础功能与约束的前提下，给出**性能最优**的组合建议（分包、虚拟化、监控等）
"""


DOCUMENT_GENERATION_PROMPT_TEMPLATE = """请基于以下信息，生成一份符合《前端技术方案模版》结构的企业级技术方案文档。

## 输入信息

### 项目背景（来自用户表单）
- **项目类型**: {project_type}
- **项目阶段**: {project_stage}
- **本次前端人数**: {team_size}
- **现有技术栈**: {existing_stack}
- **业务核心功能**: {core_features}
- **关键特性**: {key_features}
- **开发偏好**: {dev_preference}
- **禁忌与不接受项**: {forbidden_items}

### 需求分析结果
**核心技术需求**:
{requirements}

**技术约束**:
{constraints}

### 技术调研数据
{search_summary}

## 文档要求

1. 按照《前端技术方案模版》结构输出，非每项必填，按相关性选择
2. 用户未指出、本次未涉及的部分注明「用户未指出但可能需要保留」
3. **3.1 技术调研和选型** 必须包含 2+ 套方案对比，每套写明：投放场景、容器类型、开发模式、模块方案
4. 最后给出明确建议
5. 使用 Markdown 格式，清晰的标题层级
6. 文档总长度控制在 2000-4000 字

现在请开始生成文档。"""


def get_generation_prompt(
    project_info: dict,
    analysis_result: dict,
    search_results: list,
) -> str:
    """
    生成文档生成提示词
    
    Args:
        project_info: 来自 form_data 的项目信息（含 form_data）
        analysis_result: 分析结果
        search_results: 搜索结果列表
        
    Returns:
        格式化后的提示词
    """
    form_data = project_info.get("form_data", project_info)
    
    requirements_list = analysis_result.get("extracted_requirements", [])
    requirements_str = "\n".join([f"- {req}" for req in requirements_list])
    
    constraints_list = analysis_result.get("tech_constraints", [])
    constraints_str = "\n".join([f"- {c}" for c in constraints_list])
    
    if search_results:
        search_summary = f"找到 {len(search_results)} 条相关技术信息。\n\n**部分关键信息**:\n"
        for i, result in enumerate(search_results[:5], 1):
            title = result.get("title", "No title")
            body = (result.get("body", "") or "")[:100]
            search_summary += f"{i}. {title}: {body}...\n"
    else:
        search_summary = "未进行在线搜索，将基于选型指南和LLM已有知识生成推荐。"
    
    return DOCUMENT_GENERATION_PROMPT_TEMPLATE.format(
        project_type=project_info.get("project_type", "未指定"),
        project_stage=project_info.get("project_stage", "全新开发"),
        team_size=str(project_info.get("frontend_count", 1)) + "人",
        existing_stack=form_data.get("existing_stack", "") or "无",
        core_features=form_data.get("core_features", "") or "未指定",
        key_features=form_data.get("key_features", "") or "未指定",
        dev_preference=form_data.get("dev_preference", "") or "无偏好",
        forbidden_items=form_data.get("forbidden_items", "") or "无",
        requirements=requirements_str if requirements_str else "未提取到具体需求",
        constraints=constraints_str if constraints_str else "无明确约束",
        search_summary=search_summary,
    )
