# 故障排除指南

本文档列出常见问题及解决方案。

## 安装问题

### 问题: pip install 失败

**症状**:
```
ERROR: Could not find a version that satisfies the requirement langgraph
```

**解决方案**:
1. 升级 pip：
```bash
python -m pip install --upgrade pip
```

2. 使用国内镜像（中国用户）：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 检查 Python 版本（需要 3.9+）：
```bash
python --version
```

### 问题: 缺少某个包

**症状**:
```
ModuleNotFoundError: No module named 'rich'
```

**解决方案**:
```bash
pip install rich
# 或重新安装所有依赖
pip install -r requirements.txt
```

## API 配置问题

### 问题: API Key 错误

**症状**:
```
ValueError: DEEPSEEK_API_KEY not found
```

**解决方案**:
1. 确保 `.env` 文件存在于项目根目录
2. 检查文件内容格式：
```bash
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx
```
注意：**没有空格**，**没有引号**

3. 验证 API Key 是否有效：
```python
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("DEEPSEEK_API_KEY"))  # 应该输出你的API Key
```

### 问题: API 调用失败

**症状**:
```
RuntimeError: Deepseek API call failed: 401 Unauthorized
```

**解决方案**:
1. 检查 API Key 是否正确
2. 检查 API Key 是否已过期
3. 访问 Deepseek 控制台确认账户状态
4. 确认是否有足够的余额

### 问题: 网络连接错误

**症状**:
```
requests.exceptions.ConnectionError
```

**解决方案**:
1. 检查网络连接
2. 如果在公司网络，检查代理设置
3. 尝试使用代理：
```python
# 在 src/utils/llm_client.py 中添加
import os
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.example.com:8080'
```

## 运行时问题

### 问题: 中文显示乱码

**症状**: 终端输出的中文显示为 `???` 或方块

**解决方案**:

Windows PowerShell:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

Windows CMD:
```bash
chcp 65001
```

### 问题: Rich 格式显示问题

**症状**: 终端输出的颜色和格式混乱

**解决方案**:
1. 使用现代终端（Windows Terminal、iTerm2）
2. 在代码中禁用 Rich 格式：
```python
# 在 cli.py 顶部添加
import os
os.environ['TERM'] = 'dumb'
```

### 问题: 程序卡住不动

**症状**: 运行到某个步骤后无响应

**可能原因**:
1. 等待用户输入（检查终端是否有提示）
2. API 调用超时
3. 搜索请求被限流

**解决方案**:
1. 查看终端是否有输入提示
2. 按 `Ctrl+C` 中断，检查网络
3. 增加超时设置：
```python
# 在 llm_client.py 中
self.llm = ChatOpenAI(
    # ...
    timeout=60,  # 增加超时时间
)
```

### 问题: 搜索返回空结果

**症状**:
```
✓ 找到 0 条相关信息
```

**解决方案**:
1. DuckDuckGo 可能限流，等待几分钟后重试
2. 修改搜索延迟：
```python
# 在 src/tools/search.py 中
search_tool = TechSearchTool(delay=2.0)  # 增加延迟
```
3. 使用其他搜索引擎（需修改代码）

### 问题: 生成的文档质量差

**症状**: 文档内容不完整、格式混乱或信息不准确

**解决方案**:
1. 优化提示词（编辑 `src/prompts/*.py`）
2. 增加 token 限制：
```bash
# .env
DEEPSEEK_MAX_TOKENS=6000
```
3. 提供更详细的项目需求
4. 调整温度参数：
```bash
# .env
DEEPSEEK_TEMPERATURE=0.5  # 降低温度以获得更稳定的输出
```

## 文件系统问题

### 问题: 无法保存文档

**症状**:
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**:
1. 检查 `outputs/` 目录权限：
```bash
# Linux/macOS
chmod 755 outputs/

# Windows: 右键 outputs 文件夹 → 属性 → 安全 → 编辑权限
```

2. 手动创建 outputs 目录：
```bash
mkdir outputs
```

### 问题: 找不到模板文件

**症状**:
```
FileNotFoundError: Template not found
```

**解决方案**:
1. 确保从项目根目录运行：
```bash
cd /path/to/tech-stack-agent
python cli.py
```

2. 检查文件结构是否完整：
```bash
ls src/templates/tech_doc_template.md
```

## LangGraph 问题

### 问题: 状态类型错误

**症状**:
```
TypeError: unhashable type: 'list'
```

**解决方案**:
1. 检查 `state.py` 中的 Annotated 类型
2. 确保使用 `operator.add` 处理列表：
```python
from typing_extensions import Annotated
import operator

search_results: Annotated[List[Dict[str, Any]], operator.add]
```

### 问题: 条件边不工作

**症状**: 工作流总是执行某个分支

**解决方案**:
1. 检查条件函数返回值：
```python
def should_search(state: TechStackState) -> str:
    print(f"needs_search: {state.get('needs_search')}")  # 调试
    return "search" if state.get("needs_search") else "generate"
```

2. 确保状态更新正确

## 性能问题

### 问题: 运行速度慢

**症状**: 完整流程超过 5 分钟

**优化方案**:
1. 禁用搜索（如果不需要最新信息）
2. 减少搜索关键词数量：
```python
# 在 search_node 中
for keyword in keywords[:3]:  # 只搜索前3个
```
3. 减少每个查询的结果数：
```python
results = search_tool.search(keyword, max_results=2)
```
4. 降低 max_tokens：
```bash
DEEPSEEK_MAX_TOKENS=3000
```

### 问题: 内存占用高

**解决方案**:
1. 清理搜索结果：
```python
# 只保留重要字段
formatted_results.append({
    'title': result.get('title', '')[:100],  # 截断
    'body': result.get('body', '')[:200],
})
```

2. 定期清理 outputs 目录

## 调试技巧

### 启用详细日志

```python
# 在 cli.py 开头添加
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 检查中间状态

```python
# 在任意节点中添加
def analyze_node(state: TechStackState) -> Dict[str, Any]:
    print(f"DEBUG - Current state: {state}")  # 打印状态
    # ... 其他代码
```

### 单步测试节点

```python
# test_node.py
from src.agent.nodes import analyze_node
from src.agent.state import TechStackState

state = {
    "project_type": "Web应用",
    # ... 其他字段
}

result = analyze_node(state)
print(result)
```

## 获取更多帮助

如果以上方案都无法解决问题：

1. **查看日志**: 运行时添加 `--verbose` 标志（如果支持）
2. **搜索 Issues**: 在 GitHub 仓库搜索类似问题
3. **提交 Issue**: 提供以下信息：
   - 操作系统版本
   - Python 版本
   - 完整错误信息
   - 复现步骤
   - 相关配置文件（去除敏感信息）

4. **社区讨论**: 在 GitHub Discussions 发起讨论

## 常用命令速查

```bash
# 检查 Python 版本
python --version

# 检查已安装的包
pip list | grep langgraph

# 重新安装依赖
pip install -r requirements.txt --force-reinstall

# 清理 Python 缓存
find . -type d -name __pycache__ -exec rm -rf {} +

# 验证 .env 文件
cat .env  # Linux/macOS
type .env  # Windows

# 测试 API 连接
python -c "from src.utils.llm_client import get_llm_client; print(get_llm_client().invoke('test'))"
```

---

**最后更新**: 2026-02-17
