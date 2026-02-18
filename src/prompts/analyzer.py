"""
Prompt templates for requirement analysis
"""

ANALYSIS_SYSTEM_PROMPT = """你是一位资深的前端技术架构师，拥有超过10年的大型项目开发经验。
你擅长根据项目需求分析最合适的技术栈，并能够平衡技术先进性、团队能力、项目时间线等多方面因素。
你的分析客观、全面，能够为技术选型提供有价值的洞见。"""


ANALYSIS_PROMPT_TEMPLATE = """基于用户提供的项目信息，请进行深入的技术需求分析。

## 项目信息
- **项目类型**: {project_type}
- **团队规模**: {team_size}
- **开发时间线**: {timeline}
- **特殊需求**: {special_requirements}

## 请完成以下分析任务

### 1. 提取核心技术需求
请列出5-8个关键技术需求点，例如：
- 性能要求（首屏加载时间、SEO优化等）
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
    Generate analysis prompt from project information.
    
    Args:
        project_info: Dictionary with project details
        
    Returns:
        Formatted prompt string
    """
    return ANALYSIS_PROMPT_TEMPLATE.format(
        project_type=project_info.get('project_type', '未指定'),
        team_size=project_info.get('team_size', '未指定'),
        timeline=project_info.get('timeline', '未指定'),
        special_requirements=project_info.get('special_requirements', '无特殊需求'),
    )
