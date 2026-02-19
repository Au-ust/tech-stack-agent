"""
Command Line Interface for Tech Stack Agent - 表单式重构版
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from src.agent.graph import get_workflow_app

# Install rich traceback handler
install(show_locals=True)

console = Console()


def initialize_state() -> dict:
    """
    初始化工作流状态（表单式流程）
    """
    return {
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


def main():
    """Main entry point for the CLI application."""
    try:
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]前端技术栈选型 Agent[/bold green]\n"
            "[dim]表单式输入 · Powered by LangGraph & Deepseek[/dim]",
            border_style="green",
        ))

        app = get_workflow_app()
        initial_state = initialize_state()
        final_state = app.invoke(initial_state)

        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ 流程完成！[/bold green]\n\n"
            f"文档已保存到: [cyan]{final_state.get('output_path', 'unknown')}[/cyan]\n\n"
            "感谢使用技术栈选型 Agent！",
            border_style="green",
        ))

        return 0

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  用户取消操作[/yellow]")
        return 130

    except Exception as e:
        console.print(f"\n\n[red]❌ 发生错误: {str(e)}[/red]")
        console.print("[dim]请检查您的配置（特别是 .env 文件中的 API Key）[/dim]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
