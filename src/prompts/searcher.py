"""
Prompt templates for search strategy generation
"""

SEARCH_SYSTEM_PROMPT = """你是一位技术信息检索专家，擅长为技术调研生成精准的搜索关键词。
你了解各种前端框架、工具链的特点，能够快速定位到最有价值的技术信息来源。"""


SEARCH_KEYWORDS_PROMPT_TEMPLATE = """基于以下项目需求分析结果，请生成用于技术调研的搜索关键词列表。

## 项目背景
- **项目类型**: {project_type}
- **核心需求**: {requirements}
- **技术约束**: {constraints}

## 搜索目标
我们需要调研以下方面的信息：
1. 当前主流的前端技术栈选项
2. 各技术栈的优缺点对比
3. 2026年的技术趋势和最佳实践
4. 实际应用案例（知名公司和优秀开源项目）

## 任务要求
请生成8-12个搜索关键词，涵盖：
- 框架对比（如："React vs Vue 2026"）
- 最佳实践（如："Next.js best practices 2026"）
- 性能优化（如："frontend performance optimization"）
- 案例研究（如："React production case study"）

### 输出格式
请严格按照以下JSON格式输出（不要包含任何其他文字）：

```json
{{
  "search_keywords": [
    "关键词1",
    "关键词2",
    "关键词3"
  ],
  "priority_frameworks": [
    "框架名称1",
    "框架名称2"
  ]
}}
```

现在请生成搜索关键词。"""


def get_search_keywords_prompt(project_info: dict, analysis_result: dict) -> str:
    """
    Generate search keywords prompt.
    
    Args:
        project_info: Project information
        analysis_result: Analysis results from analyzer
        
    Returns:
        Formatted prompt string
    """
    requirements = ", ".join(analysis_result.get('extracted_requirements', []))
    constraints = ", ".join(analysis_result.get('tech_constraints', []))
    
    return SEARCH_KEYWORDS_PROMPT_TEMPLATE.format(
        project_type=project_info.get('project_type', '未指定'),
        requirements=requirements if requirements else '未指定',
        constraints=constraints if constraints else '无约束',
    )
