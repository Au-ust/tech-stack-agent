"""
Prompt templates for requirement analysis - 表单式适配
输入为结构化 form_data，注入选型指南
"""
from pathlib import Path

_ANALYZER_DIR = Path(__file__).parent
_SELECTION_GUIDE_PATH = _ANALYZER_DIR / "selection_guide.md"


def _load_selection_guide() -> str:
    """加载选型指南内容"""
    if _SELECTION_GUIDE_PATH.exists():
        return _SELECTION_GUIDE_PATH.read_text(encoding="utf-8")
    return ""


SELECTION_GUIDE = _load_selection_guide()

ANALYSIS_SYSTEM_PROMPT = f"""你是一位资深的前端技术架构师，拥有超过10年的大型项目开发经验。
你擅长根据项目需求分析最合适的技术栈，并能够平衡技术先进性、团队能力、项目时间线等多方面因素。
你的分析客观、全面，能够为技术选型提供有价值的洞见。

## 选型参考（必读）

以下《前端技术栈选型指南》作为你分析的重要参考，请结合用户表单输入与指南给出最佳分析：

---
{SELECTION_GUIDE}
---

## 隐式默认（用户未填时按此补全）

- 性能：在保证基础功能与约束的前提下，给出性能最优的组合（分包、虚拟化、监控等）
- 工程约束：TypeScript + ESLint、适度测试、可维护性优先
- 决策偏好：以业务目标与团队约束为锚（交付速度、SEO、长期维护、多人协作、成本、性能）
"""


ANALYSIS_PROMPT_TEMPLATE = """基于用户通过表单提供的项目信息，请进行深入的技术需求分析。

## 项目信息（结构化输入）

- **项目类型**: {project_type}
- **项目阶段**: {project_stage}
- **本次前端人数**: {frontend_count}
- **现有技术栈**: {existing_stack}
- **package.json**: {package_json}
- **业务核心功能**: {core_features}
- **关键特性**: {key_features}
- **开发偏好**: {dev_preference}
- **禁忌与不接受项**: {forbidden_items}

## 请完成以下分析任务

### 1. 提取核心技术需求
请列出5-8个关键技术需求点，例如：
- 性能要求（首屏加载时间、SEO优化、虚拟滚动等）
- 用户体验要求（实时更新、离线支持等）
- 开发效率要求（快速迭代、代码复用等）
- 可维护性要求（代码规范、测试覆盖等）

### 2. 识别技术约束
请列出3-5个主要的技术约束条件，例如：
- 团队技术栈熟悉度
- 学习曲线限制
- 生态系统成熟度要求
- 浏览器兼容性需求

### 3. 判断是否需要在线搜索
基于以下标准，判断是否需要进行在线技术调研：
- 项目涉及较新的技术栈或框架（近2年内发布）
- 需要了解最新的技术趋势和最佳实践
- 需要对比多个技术方案的实际应用案例
- 用户明确提到需要"最新"、"流行"的技术

### 输出格式
请严格按照以下JSON格式输出（不要包含任何其他文字）：

```json
{{
  "extracted_requirements": [
    "需求1描述",
    "需求2描述",
    "需求3描述"
  ],
  "tech_constraints": [
    "约束1描述",
    "约束2描述",
    "约束3描述"
  ],
  "needs_search": true,
  "search_reason": "需要搜索的原因说明"
}}
```

现在请开始分析。"""


def get_analysis_prompt(project_info: dict) -> str:
    """
    生成分析提示词
    
    Args:
        project_info: 来自 form_data 的结构化项目信息
        
    Returns:
        格式化后的提示词
    """
    return ANALYSIS_PROMPT_TEMPLATE.format(
        project_type=project_info.get("project_type", "未指定"),
        project_stage=project_info.get("project_stage", "全新开发"),
        frontend_count=project_info.get("frontend_count", 1),
        existing_stack=project_info.get("existing_stack", "无") or "无",
        package_json=(project_info.get("package_json", "") or "未提供")[:500],
        core_features=project_info.get("core_features", "未指定") or "未指定",
        key_features=project_info.get("key_features", "未指定") or "未指定",
        dev_preference=project_info.get("dev_preference", "无偏好") or "无偏好",
        forbidden_items=project_info.get("forbidden_items", "无") or "无",
    )
