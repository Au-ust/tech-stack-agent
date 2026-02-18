"""
Document Generation Tools
"""
from typing import Dict, Any, List
from datetime import datetime


class DocumentGenerator:
    """
    Generates structured technical documents.
    """
    
    @staticmethod
    def format_tech_stack(stack: Dict[str, Any]) -> str:
        """
        Format technology stack as markdown table.
        
        Args:
            stack: Dictionary with categories and tech choices
            
        Returns:
            Markdown formatted table
        """
        if not stack:
            return "待生成技术栈推荐"
        
        lines = ["| 类别 | 推荐技术 | 说明 |", "|------|----------|------|"]
        
        for category, details in stack.items():
            if isinstance(details, dict):
                tech = details.get('name', '')
                reason = details.get('reason', '')
                lines.append(f"| {category} | {tech} | {reason} |")
            else:
                lines.append(f"| {category} | {details} | - |")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_comparison_matrix(comparisons: List[Dict[str, Any]]) -> str:
        """
        Format technology comparison as markdown table.
        
        Args:
            comparisons: List of technology comparisons
            
        Returns:
            Markdown formatted comparison table
        """
        if not comparisons:
            return "暂无对比数据"
        
        # Extract headers
        headers = ["技术", "优点", "缺点", "适用场景"]
        lines = [
            "| " + " | ".join(headers) + " |",
            "|" + "|".join(["------"] * len(headers)) + "|"
        ]
        
        for comp in comparisons:
            name = comp.get('name', '')
            pros = comp.get('pros', '')
            cons = comp.get('cons', '')
            use_case = comp.get('use_case', '')
            
            lines.append(f"| {name} | {pros} | {cons} | {use_case} |")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_search_results(results: List[Dict[str, Any]], max_items: int = 5) -> str:
        """
        Format search results as markdown list.
        
        Args:
            results: Search results
            max_items: Maximum number of items to include
            
        Returns:
            Markdown formatted list
        """
        if not results:
            return "无搜索结果"
        
        lines = []
        for i, result in enumerate(results[:max_items], 1):
            title = result.get('title', 'No title')
            href = result.get('href', '#')
            body = result.get('body', '')
            
            # Truncate body if too long
            if len(body) > 150:
                body = body[:150] + "..."
            
            lines.append(f"{i}. **[{title}]({href})**")
            if body:
                lines.append(f"   {body}")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def create_document_header(project_info: Dict[str, str]) -> str:
        """
        Create document header with project information.
        
        Args:
            project_info: Dictionary with project details
            
        Returns:
            Markdown formatted header
        """
        timestamp = datetime.now().strftime("%Y年%m月%d日")
        
        header = f"""# 技术栈选型文档

**生成时间**: {timestamp}

---

## 项目信息

- **项目类型**: {project_info.get('project_type', '未指定')}
- **团队规模**: {project_info.get('team_size', '未指定')}
- **开发时间线**: {project_info.get('timeline', '未指定')}
- **特殊需求**: {project_info.get('special_requirements', '无')}

---
"""
        return header
    
    @staticmethod
    def wrap_section(title: str, content: str, level: int = 2) -> str:
        """
        Wrap content in a markdown section.
        
        Args:
            title: Section title
            content: Section content
            level: Header level (2-6)
            
        Returns:
            Markdown formatted section
        """
        header = "#" * level
        return f"{header} {title}\n\n{content}\n\n"
