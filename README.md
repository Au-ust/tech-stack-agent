# 前端技术栈选型 Agent

基于 **LangGraph** 和 **Deepseek API** 的智能前端技术栈选型助手，通过**结构化表单**收集需求、AI 分析、在线技术调研，生成符合企业级《前端技术方案模版》的技术选型文档。

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 特性

- **表单式输入**：结构化表单收集，仅保留影响选型的硬核字段，可回车跳过使用默认值
- **选型指南驱动**：内置《前端技术栈选型指南》，模型结合表单 + 指南 + 自身知识给出最佳方案
- **企业级输出**：按《前端技术方案模版》生成文档，2+ 套方案对比，明确建议
- **在线技术调研**：自动搜索最新技术趋势和最佳实践
- **超低成本**：使用 Deepseek API（¥0.001/1K tokens），100 次对话约 ¥1.7
- **CLI 专注**：纯命令行交互，高效流畅

## 表单字段（极简 9 项）

| 分组 | 字段 | 说明 |
|------|------|------|
| 项目基础 | 项目类型 | Web-C端、Web-B端、小程序、移动端开发 |
| | 项目阶段 | 全新开发、项目新增、局部模块替换 |
| | 本次前端人数 | 数字，默认 1 |
| | 现有技术栈 | 新项目可不填 |
| | package.json | 项目新增/局部替换时强烈建议粘贴 |
| 业务与需求 | 业务核心功能 | 如：后台管理、商品列表、表单、图表等 |
| | 关键特性 | 如：SEO、虚拟滚动、弱网兼容等 |
| 开发偏好与约束 | 开发偏好 | 新项目填：React/Vue/TS 优先等 |
| | 禁忌与不接受项 | 明确拒绝的方案 |

## 生成文档结构（《前端技术方案模版》）

- 模版声明、ChangeLog
- 1. 业务背景和目标
- 2. 相关人员
- 3. 整体技术方案（含 3.1 技术调研和选型：2+ 套方案对比）
- 4. 详细设计（可选）
- 5. 技术风险分析
- 6. 测试范围分析
- 7. 发布计划流程
- 8. 评估意见
- 9. 技术方案申请变更

非每项必填，按方案相关性选择；用户未指出部分注明「用户未指出但可能需要保留」。

## 快速开始

### 1. 环境要求

- Python 3.9+
- pip 或 conda

### 2. 安装依赖

```bash
git clone <repository-url>
cd tech-stack-agent
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

### 4. 运行 CLI

```bash
python cli.py
```

按提示填写表单，可回车跳过使用默认值。流程：表单 → 分析 → 搜索（可选）→ 生成文档 → 保存。

## 项目结构

```
tech-stack-agent/
├── src/
│   ├── agent/
│   │   ├── graph.py          # LangGraph 工作流（表单式流程）
│   │   ├── nodes.py          # 节点：form_collect、analyze、search、generate、save
│   │   └── state.py          # 状态定义
│   ├── forms/
│   │   ├── schema.py         # 表单字段定义
│   │   ├── defaults.yaml    # 默认值配置
│   │   └── collector.py     # 表单收集逻辑
│   ├── prompts/
│   │   ├── selection_guide.md       # 选型指南知识库
│   │   ├── tech_solution_template.md # 技术方案模版
│   │   ├── analyzer.py      # 分析提示词
│   │   ├── searcher.py      # 搜索提示词
│   │   └── generator.py     # 生成提示词
│   ├── tools/
│   │   ├── search.py        # DuckDuckGo 搜索
│   │   └── document.py      # 文档工具
│   └── utils/
│       ├── llm_client.py    # Deepseek 客户端
│       └── file_manager.py  # 文件管理
├── outputs/                  # 生成的文档
├── cli.py                    # CLI 入口
├── requirements.txt
└── README.md
```

## 配置说明

`.env` 支持：

```bash
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TEMPERATURE=0.7
DEEPSEEK_MAX_TOKENS=4000
```

## 作为 Python 模块使用

```python
from src.agent.graph import get_workflow_app

app = get_workflow_app()
initial_state = {
    "form_data": {},
    "extracted_requirements": [],
    "tech_constraints": [],
    "needs_search": False,
    "search_results": [],
    "final_document": "",
    "current_step": "",
    "messages": [],
    "output_path": "",
    "project_type": "",
    "team_size": "",
    "timeline": "",
    "special_requirements": "",
}
final_state = app.invoke(initial_state)
# form_data 由 form_collect_node 交互式填充
```

## 致谢

- [LangGraph](https://github.com/langchain-ai/langgraph) - AI 工作流框架
- [Deepseek](https://www.deepseek.com/) - 高性价比 LLM API
- [DuckDuckGo](https://duckduckgo.com/) - 免费搜索服务
- [InquirerPy](https://github.com/kazhala/InquirerPy) - CLI 表单交互

---

**Made with ❤️ using LangGraph & Deepseek**
