# 🚀 前端技术栈选型 Agent

基于 **LangGraph** 和 **Deepseek API** 的智能前端技术栈选型助手，通过 AI 驱动的需求分析、在线技术调研和文档生成，帮助团队做出最佳的技术选型决策。

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特性

- 🤖 **AI 驱动分析**: 使用 Deepseek API 智能分析项目需求和技术约束
- 🔍 **在线技术调研**: 自动搜索最新的技术趋势和最佳实践
- 📝 **完整文档生成**: 生成包含优缺点对比、案例研究、风险评估的专业文档
- 💰 **超低成本**: 使用 Deepseek API（¥0.001/1K tokens），100次对话约¥1.7
- 🎯 **引导式交互**: 友好的问答式信息收集流程
- 📊 **结构化输出**: 生成符合企业评审标准的 Markdown 技术文档

## 📋 生成文档包含

1. **项目背景分析** - 需求提取和约束识别
2. **技术栈推荐** - 框架、工具链、最佳实践
3. **详细分析** - 每个技术选择的深入说明
4. **优缺点对比** - 多方案对比矩阵
5. **学习曲线评估** - 团队学习成本分析
6. **生态系统对比** - 社区、文档、企业支持
7. **案例研究** - 知名公司和优秀开源项目案例
8. **成本分析** - 开发、维护、基础设施成本
9. **风险评估** - 技术风险和缓解措施
10. **实施建议** - 分阶段实施计划

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                   用户输入项目信息                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           LangGraph 工作流引擎                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ 问答节点  │→ │ 分析节点  │→ │ 搜索节点  │→ │ 生成节点  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Deepseek │  │ DuckDuck │  │  本地文件 │
│   API    │  │    Go    │  │  存储     │
└──────────┘  └──────────┘  └──────────┘
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- pip 或 conda

### 2. 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd tech-stack-agent

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置 API Key

创建 `.env` 文件并配置 Deepseek API Key：

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件
# DEEPSEEK_API_KEY=your_api_key_here
```

**获取 Deepseek API Key**:
1. 访问 [Deepseek 官网](https://platform.deepseek.com/)
2. 注册并获取 API Key
3. 新用户有免费额度可供测试

### 4. 运行 CLI 版本

```bash
python cli.py
```

按照提示回答问题，Agent 将自动生成技术选型文档。

### 5. 运行 Streamlit Web 界面（可选）

```bash
streamlit run app.py
```

> 注意：Streamlit 版本当前为演示版，推荐使用 CLI 版本获得完整功能。

## 📖 使用示例

### 命令行交互示例

```
🚀 前端技术栈选型 Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

问题 1/4
请描述您的项目类型: Web应用

问题 2/4
请选择您的团队规模: 1-3人（小型团队）

问题 3/4
请选择预期的开发时间线: 1-3个月

问题 4/4
请描述任何特殊需求: 需要SEO优化和高性能

🔍 正在分析项目需求...
✓ 提取了 5 个核心需求
✓ 识别了 3 个技术约束
✓ 是否需要在线搜索: 是

🌐 正在进行技术调研...
✓ 找到 15 条相关信息

📝 正在生成技术选型文档...
✓ 文档生成完成

💾 正在保存文档...
✓ 文档已保存到: outputs/tech_stack_Web应用_20260217_143022.md

✅ 流程完成！
```

## 💰 成本说明

使用 **Deepseek API** 实现超低成本运行：

| 项目 | 成本 |
|------|------|
| 单次完整对话 | ≈ ¥0.017 (约2分钱) |
| 100次对话 | ≈ ¥1.7 |
| 500次对话 | ≈ ¥8.5 |

**对比其他方案**:
- GPT-4: 约 30倍 成本
- GPT-3.5: 约 10倍 成本
- 智谱 GLM-4: 约 50倍 成本

## 📁 项目结构

```
tech-stack-agent/
├── src/
│   ├── agent/
│   │   ├── graph.py          # LangGraph 工作流编排
│   │   ├── nodes.py          # 节点实现
│   │   └── state.py          # 状态定义
│   ├── tools/
│   │   ├── search.py         # DuckDuckGo 搜索
│   │   └── document.py       # 文档生成工具
│   ├── prompts/
│   │   ├── analyzer.py       # 分析提示词
│   │   ├── searcher.py       # 搜索提示词
│   │   └── generator.py      # 生成提示词
│   ├── templates/
│   │   └── tech_doc_template.md  # 文档模板
│   └── utils/
│       ├── llm_client.py     # Deepseek 客户端
│       └── file_manager.py   # 文件管理
├── outputs/                   # 生成的文档
├── cli.py                     # CLI 入口
├── app.py                     # Streamlit UI
├── requirements.txt           # 依赖列表
├── .env.example              # 配置示例
└── README.md                 # 本文件
```

## 🔧 配置说明

`.env` 文件支持的配置项：

```bash
# 必需配置
DEEPSEEK_API_KEY=your_api_key_here

# 可选配置
DEEPSEEK_MODEL=deepseek-chat          # 模型名称
DEEPSEEK_TEMPERATURE=0.7              # 温度参数 (0.0-1.0)
DEEPSEEK_MAX_TOKENS=4000              # 最大token数
```

## 🛠️ 高级用法

### 作为 Python 模块使用

```python
from src.agent.graph import get_workflow_app

# 创建工作流
app = get_workflow_app()

# 准备初始状态
initial_state = {
    "project_type": "Web应用",
    "team_size": "1-3人（小型团队）",
    "timeline": "1-3个月",
    "special_requirements": "需要SEO优化",
    # ... 其他字段
}

# 执行工作流
final_state = app.invoke(initial_state)

# 获取生成的文档
document = final_state["final_document"]
output_path = final_state["output_path"]
```

### 自定义节点

可以在 `src/agent/nodes.py` 中添加自定义节点：

```python
def custom_node(state: TechStackState) -> Dict[str, Any]:
    # 自定义逻辑
    return {
        "custom_field": "value",
        "messages": ["自定义节点执行完成"]
    }
```

### 修改提示词

提示词位于 `src/prompts/` 目录，可以根据需求修改：

- `analyzer.py` - 需求分析提示词
- `searcher.py` - 搜索策略提示词
- `generator.py` - 文档生成提示词

## 🧪 测试

创建测试脚本：

```python
# test_agent.py
from src.agent.graph import get_workflow_app

def test_blog_project():
    """测试博客项目"""
    app = get_workflow_app()
    state = {
        "project_type": "Web应用",
        "team_size": "1-3人（小型团队）",
        "timeline": "1个月内",
        "special_requirements": "需要SEO和Markdown支持",
        # ...
    }
    result = app.invoke(state)
    assert result["output_path"] != ""
    print("✓ 博客项目测试通过")

if __name__ == "__main__":
    test_blog_project()
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

## 📄 许可证

MIT License

## 🙏 致谢

- [LangGraph](https://github.com/langchain-ai/langgraph) - 强大的 AI 工作流框架
- [Deepseek](https://www.deepseek.com/) - 高性价比的 LLM API
- [DuckDuckGo](https://duckduckgo.com/) - 免费的搜索服务

## 📞 联系方式

- 问题反馈: GitHub Issues
- 功能建议: GitHub Discussions

---

**Made with ❤️ using LangGraph & Deepseek**
