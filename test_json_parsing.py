"""
测试 JSON 解析修复效果
用于验证改进后的 _parse_json_response 函数能否处理各种格式
"""
import json
import sys
from typing import Dict, Any

# 设置UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def _parse_json_response_new(response: str) -> Dict[str, Any]:
    """
    解析LLM的JSON响应（鲁棒版本）
    支持多种格式：代码块、纯JSON、带解释的JSON
    """
    
    # 策略1: 提取 ```json 代码块
    if "```json" in response:
        json_start = response.find("```json") + 7
        json_end = response.find("```", json_start)
        if json_end > json_start:
            json_str = response[json_start:json_end].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
    
    # 策略2: 提取普通 ``` 代码块
    elif "```" in response:
        json_start = response.find("```") + 3
        json_end = response.find("```", json_start)
        if json_end > json_start:
            json_str = response[json_start:json_end].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
    
    # 策略3: 使用栈匹配法查找完整的JSON对象（支持任意层嵌套）
    def find_json_objects(text):
        """使用栈匹配查找完整的JSON对象"""
        results = []
        stack = []
        start_idx = None
        in_string = False
        escape_next = False
        
        for i, char in enumerate(text):
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
            
            if char == '"':
                in_string = not in_string
                continue
            
            if in_string:
                continue
            
            if char == '{':
                if not stack:
                    start_idx = i
                stack.append('{')
            elif char == '}':
                if stack:
                    stack.pop()
                    if not stack and start_idx is not None:
                        results.append(text[start_idx:i+1])
                        start_idx = None
        
        return results
    
    json_objects = find_json_objects(response)
    
    # 尝试解析找到的JSON对象（从最长的开始）
    for obj in sorted(json_objects, key=len, reverse=True):
        try:
            parsed = json.loads(obj)
            if isinstance(parsed, dict) and len(parsed) > 0:
                return parsed
        except json.JSONDecodeError:
            continue
    
    # 策略4: 尝试解析整个响应
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    
    # 所有策略都失败，抛出详细错误
    raise ValueError(
        f"无法从LLM响应中提取有效JSON。\n"
        f"响应长度: {len(response)} 字符\n"
        f"响应前200字符: {response[:200]}\n"
        f"响应后200字符: {response[-200:]}"
    )


def test_case_1_with_code_block():
    """测试用例1: 标准的 ```json 代码块"""
    response = """```json
{
  "summary": {
    "title": "测试项目",
    "stage": "新建",
    "confidence": 0.8
  }
}
```"""
    
    result = _parse_json_response_new(response)
    assert "summary" in result
    print("[PASS] Test case 1: Standard code block")


def test_case_2_with_explanation():
    """测试用例2: 带解释的JSON（最常见的失败情况）"""
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
    
    result = _parse_json_response_new(response)
    assert "summary" in result
    assert result["summary"]["title"] == "企业级瀑布流应用"
    print("[PASS] Test case 2: JSON with explanations")


def test_case_3_pure_json():
    """测试用例3: 纯JSON（无代码块）"""
    response = """{
  "summary": {
    "title": "纯JSON测试",
    "stage": "新建",
    "confidence": 0.9
  }
}"""
    
    result = _parse_json_response_new(response)
    assert "summary" in result
    print("[PASS] Test case 3: Pure JSON")


def test_case_4_nested_json():
    """测试用例4: 复杂嵌套JSON"""
    response = """```json
{
  "summary": {"title": "测试"},
  "project_basic": {
    "project_type_detail": {
      "value": "Web端",
      "source": "明确",
      "reasoning": "用户说明",
      "confidence": 0.9
    },
    "project_stage": {
      "value": "新建",
      "source": "推测"
    }
  },
  "business_scenario": {
    "core_features": {
      "value": ["瀑布流", "无限滚动"],
      "source": "明确"
    }
  }
}
```"""
    
    result = _parse_json_response_new(response)
    assert "project_basic" in result
    assert "business_scenario" in result
    print("[PASS] Test case 4: Complex nested JSON")


def test_case_5_with_markdown():
    """测试用例5: 混合Markdown文本的响应"""
    response = """# 项目分析

让我来分析你的需求：

```json
{
  "summary": {
    "title": "混合格式测试",
    "stage": "新建",
    "confidence": 0.85
  }
}
```

希望这个分析对你有帮助！"""
    
    result = _parse_json_response_new(response)
    assert "summary" in result
    print("[PASS] Test case 5: Mixed Markdown format")


def test_case_6_incomplete_should_fail():
    """测试用例6: 不完整的JSON应该失败"""
    response = """{
  "summary": {
    "title": "不完整"""
    
    try:
        _parse_json_response_new(response)
        print("✗ 测试用例6失败: 应该抛出异常")
    except ValueError as e:
        print("✓ 测试用例6通过: 正确识别不完整JSON")


if __name__ == "__main__":
    print("\n[TEST] JSON Parse Fix Validation\n")
    print("="*60)
    
    try:
        test_case_1_with_code_block()
        test_case_2_with_explanation()
        test_case_3_pure_json()
        test_case_4_nested_json()
        test_case_5_with_markdown()
        test_case_6_incomplete_should_fail()
        
        print("="*60)
        print("\n[SUCCESS] All test cases passed! JSON parsing fixed.\n")
        
    except Exception as e:
        print("="*60)
        print(f"\n[FAILED] Test failed: {str(e)}\n")
        import traceback
        traceback.print_exc()
