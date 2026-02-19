---
name: tech-stack-agent-quickstart
description: tech-stack-agent 项目快速启动、环境排障和常见问题解决。适用于项目启动、Python 环境问题、依赖安装、AI理解失败等场景。
---

# tech-stack-agent 快速启动与排障

## 一、快速启动（3 步）

```bash
# 1. 安装依赖
py -m pip install -r requirements.txt

# 2. 配置 .env（项目根目录）
# DEEPSEEK_API_KEY=你的密钥

# 3. 运行
py cli.py
```

可选：`py check_setup.py` 验证环境。

---

## 二、Python 环境问题

### 问题 A：py 报错 "Can't find a default Python"

**原因**：`python` 指向 Windows 应用执行别名（0 字节占位符），非真实 Python。

**诊断**：
```powershell
Get-Command python | Format-List
# 若 Path 为 WindowsApps\python.exe → 占位符
```

**解决**：
1. 从 [python.org/downloads](https://www.python.org/downloads/) 安装 Python，勾选 "Add python.exe to PATH"
2. 设置 → 应用 → 应用执行别名 → 关闭 `python.exe`、`python3.exe`
3. 重启终端

### 问题 B：ModuleNotFoundError: No module named 'rich'

**原因**：依赖未安装。

**解决**：
```bash
py -m pip install -r requirements.txt
```

### 问题 C：依赖包很多（70+ 个）正常吗？

正常。`requirements.txt` 仅 8 个直接依赖，但 LangChain/LangGraph 会拉取大量间接依赖。

### 问题 D：Scripts 不在 PATH 的 WARNING

可忽略，不影响 `py cli.py` 运行。若需使用 `dotenv` 等命令行工具，可将 `...\pythoncore-3.14-64\Scripts` 加入 PATH。

---

## 三、AI 理解失败

### 现象
```
AI理解失败: '\n  "summary"'
将使用简化流程...
没有AI理解结果可展示
```

**原因**：LLM 返回的 JSON 被截断或格式异常，解析失败。详见 `BUG_ANALYSIS.md`。

**当前行为**：自动降级，用 `raw_user_input` 继续生成文档，可正常完成流程。

**可选优化**（若需修复）：
- 在 `.env` 中提高 `DEEPSEEK_MAX_TOKENS`（如 8000）
- 降低 `DEEPSEEK_TEMPERATURE`（如 0.2）提高输出稳定性
- 参考 `BUG_ANALYSIS.md` 改进 `_parse_json_response` 的容错逻辑

---

## 四、快速诊断清单

| 检查项 | 命令 | 正常结果 |
|--------|------|----------|
| Python | `py --version` | 显示版本号 |
| 依赖 | `py -c "import rich"` | 无报错 |
| API Key | 检查 `.env` 中 `DEEPSEEK_API_KEY` | 已配置 |

---

## 五、相关文件

- `BUG_ANALYSIS.md` - AI 理解失败详细分析
- `TROUBLESHOOTING.md` - 故障排除
- `~/.cursor/skills/windows-python-troubleshooting/` - Windows Python 环境排障（个人技能）
