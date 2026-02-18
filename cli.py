"""
Command Line Interface for Tech Stack Agent
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from src.agent.graph import get_workflow_app
from src.agent.state import TechStackState

# Install rich traceback handler
install(show_locals=True)

console = Console()


def initialize_state() -> dict:
    """
    Initialize the workflow state with empty values.
    
    Returns:
        Initial state dictionary
    """
    return {
        # User inputs
        "project_type": "",
        "team_size": "",
        "timeline": "",
        "special_requirements": "",
        
        # Analysis results
        "extracted_requirements": [],
        "tech_constraints": [],
        
        # Search results
        "search_results": [],
        
        # Document
        "recommended_stack": {},
        "final_document": "",
        
        # Control flow
        "current_step": "",
        "needs_search": False,
        
        # Messages
        "messages": [],
        
        # Output
        "output_path": "",
    }


def main():
    """
    Main entry point for the CLI application.
    """
    try:
        # Display banner
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]前端技术栈选型 Agent[/bold green]\n"
            "[dim]Powered by LangGraph & Deepseek[/dim]",
            border_style="green"
        ))
        
        # Get workflow app
        app = get_workflow_app()
        
        # Initialize state
        initial_state = initialize_state()
        
        # Run workflow
        final_state = app.invoke(initial_state)
        
        # Display completion message
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ 流程完成！[/bold green]\n\n"
            f"文档已保存到: [cyan]{final_state.get('output_path', 'unknown')}[/cyan]\n\n"
            "感谢使用技术栈选型 Agent！",
            border_style="green"
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
