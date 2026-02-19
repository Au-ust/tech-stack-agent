import re
import json

response = """好的，我来分析这个项目：

{
  "summary": {
    "title": "企业级瀑布流应用",
    "stage": "改造",
    "confidence": 0.75
  },
  "project_basic": {
    "project_type_detail": {
      "value": "Web端-C端页面",
      "source": "推测"
    }
  }
}

以上是我的理解。"""

print("=== 测试响应 ===")
print(response)
print("\n" + "="*60)

# 测试当前的正则表达式
json_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
matches = re.findall(json_pattern, response, re.DOTALL)

print(f"\n找到 {len(matches)} 个匹配")
for i, match in enumerate(matches):
    print(f"\n匹配 {i+1} (长度 {len(match)} 字符):")
    print(match[:200])
    print("\n尝试解析...")
    try:
        parsed = json.loads(match)
        print(f"✓ 解析成功！键: {list(parsed.keys())}")
    except Exception as e:
        print(f"✗ 解析失败: {e}")

# 尝试更好的方法：查找花括号对
print("\n" + "="*60)
print("\n尝试改进的方法：栈匹配法")

def find_json_objects(text):
    """使用栈匹配查找完整的JSON对象"""
    results = []
    stack = []
    start_idx = None
    
    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start_idx = i
            stack.append('{')
        elif char == '}':
            if stack:
                stack.pop()
                if not stack and start_idx is not None:
                    # 找到一个完整的对象
                    results.append(text[start_idx:i+1])
                    start_idx = None
    
    return results

json_objects = find_json_objects(response)
print(f"\n找到 {len(json_objects)} 个 JSON 对象")

for i, obj in enumerate(json_objects):
    print(f"\n对象 {i+1} (长度 {len(obj)} 字符):")
    print(obj[:200])
    print("\n尝试解析...")
    try:
        parsed = json.loads(obj)
        print(f"✓ 解析成功！键: {list(parsed.keys())}")
        print(f"summary.title = {parsed.get('summary', {}).get('title')}")
    except Exception as e:
        print(f"✗ 解析失败: {e}")
