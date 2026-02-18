"""
Prompt templates for document generation
"""

GENERATOR_SYSTEM_PROMPT = """你是一位专业的技术文档撰写专家，擅长编写清晰、全面、结构化的技术选型文档。
你的文档能够帮助技术团队和管理层快速理解技术方案，做出明智的决策。
你的写作风格专业、客观，注重数据支撑和实际案例。"""


DOCUMENT_GENERATION_PROMPT_TEMPLATE = """请基于以下信息，生成一份完整的前端技术栈选型文档。

## 输入信息

### 项目背景
- **项目类型**: {project_type}
- **团队规模**: {team_size}
- **开发时间线**: {timeline}
- **特殊需求**: {special_requirements}

### 需求分析结果
**核心技术需求**:
{requirements}

**技术约束**:
{constraints}

### 技术调研数据
{search_summary}

## 文档要求

请生成一份包含以下章节的完整技术选型文档：

### 1. 项目背景（已提供）

### 2. 技术栈推荐
明确推荐的完整技术栈，包括：
- 前端框架（React/Vue/Angular/Svelte等）
- 状态管理（Redux/Zustand/Pinia等）
- 路由方案
- UI组件库
- 构建工具（Vite/Webpack等）
- 样式方案（CSS-in-JS/Tailwind/SCSS等）
- 测试框架

### 3. 技术选型详细分析
针对每个技术类别，详细说明：
- 为什么选择这个技术
- 技术的核心优势
- 潜在的局限性
- 如何应对局限性

### 4. 优缺点对比矩阵
使用表格形式对比2-3个备选方案的优缺点

### 5. 学习曲线评估
评估团队学习新技术栈所需的时间和资源

### 6. 生态系统对比
对比各技术栈的：
- 社区活跃度
- 第三方库丰富度
- 文档质量
- 企业支持

### 7. 案例研究

#### 7.1 知名公司案例
列举3-5个使用类似技术栈的知名公司案例，说明：
- 公司名称和产品
- 使用的技术栈
- 取得的成果

#### 7.2 优秀开源项目
列举3-5个优秀的开源项目，提供：
- 项目名称和GitHub链接
- 技术栈
- 项目特点

### 8. 成本分析
- 开发成本（学习时间、开发效率）
- 维护成本（技术更新、人员培训）
- 基础设施成本（托管、CI/CD等）

### 9. 风险评估与缓解措施
识别潜在风险并提供应对方案：
- 技术风险（如框架过时、社区衰退）
- 团队风险（如学习曲线过陡）
- 项目风险（如交付延期）

### 10. 实施建议
提供分阶段的实施计划和关键里程碑

## 输出要求
- 使用Markdown格式
- 使用清晰的标题层级（##、###）
- 适当使用表格和列表
- 保持专业、客观的语气
- 提供具体的数据和案例支撑
- 文档总长度控制在2000-3000字

现在请开始生成文档。"""


def get_generation_prompt(
    project_info: dict,
    analysis_result: dict,
    search_results: list,
) -> str:
    """
    Generate document generation prompt.
    
    Args:
        project_info: Project information
        analysis_result: Analysis results
        search_results: Search results summary
        
    Returns:
        Formatted prompt string
    """
    # Format requirements
    requirements_list = analysis_result.get('extracted_requirements', [])
    requirements_str = "\n".join([f"- {req}" for req in requirements_list])
    
    # Format constraints
    constraints_list = analysis_result.get('tech_constraints', [])
    constraints_str = "\n".join([f"- {const}" for const in constraints_list])
    
    # Format search results summary
    if search_results:
        search_summary = f"找到 {len(search_results)} 条相关技术信息，包括最新的技术趋势、最佳实践和案例研究。"
        
        # Add sample results
        sample_results = search_results[:5]
        search_summary += "\n\n**部分关键信息**:\n"
        for i, result in enumerate(sample_results, 1):
            title = result.get('title', 'No title')
            body = result.get('body', '')[:100]
            search_summary += f"{i}. {title}: {body}...\n"
    else:
        search_summary = "未进行在线搜索，将基于LLM已有知识生成推荐。"
    
    return DOCUMENT_GENERATION_PROMPT_TEMPLATE.format(
        project_type=project_info.get('project_type', '未指定'),
        team_size=project_info.get('team_size', '未指定'),
        timeline=project_info.get('timeline', '未指定'),
        special_requirements=project_info.get('special_requirements', '无'),
        requirements=requirements_str if requirements_str else "未提取到具体需求",
        constraints=constraints_str if constraints_str else "无明确约束",
        search_summary=search_summary,
    )
