"""
Environment Setup Checker

Run this script to verify your environment is correctly configured.
Usage: python check_setup.py
"""
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version >= (3, 9):
        return True, f"{version.major}.{version.minor}.{version.micro}"
    return False, f"{version.major}.{version.minor}.{version.micro} (需要 3.9+)"


def check_dependencies():
    """Check if all required packages are installed."""
    required = [
        "langgraph",
        "langchain",
        "langchain_openai",
        "duckduckgo_search",
        "dotenv",
        "rich",
    ]
    
    results = []
    all_installed = True
    
    for package in required:
        try:
            if package == "dotenv":
                __import__("dotenv")
            elif package == "duckduckgo_search":
                __import__("duckduckgo_search")
            elif package == "langchain_openai":
                __import__("langchain_openai")
            else:
                __import__(package)
            results.append((package, True, "已安装"))
        except ImportError:
            results.append((package, False, "未安装"))
            all_installed = False
    
    return all_installed, results


def check_env_file():
    """Check if .env file exists and has API key."""
    import os
    from pathlib import Path
    
    env_file = Path(".env")
    
    if not env_file.exists():
        return False, ".env 文件不存在"
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        if not api_key:
            return False, ".env 文件存在但未配置 DEEPSEEK_API_KEY"
        
        if api_key == "your_deepseek_api_key_here":
            return False, "请将 API Key 替换为真实的密钥"
        
        # Mask the API key for display
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        return True, f"已配置 ({masked_key})"
    
    except Exception as e:
        return False, f"读取失败: {str(e)}"


def check_project_structure():
    """Check if all required directories and files exist."""
    from pathlib import Path
    
    required_items = [
        ("src/agent/graph.py", "文件"),
        ("src/agent/nodes.py", "文件"),
        ("src/agent/state.py", "文件"),
        ("src/tools/search.py", "文件"),
        ("src/utils/llm_client.py", "文件"),
        ("src/prompts/analyzer.py", "文件"),
        ("src/templates/tech_doc_template.md", "文件"),
        ("outputs", "目录"),
        ("cli.py", "文件"),
    ]
    
    results = []
    all_exist = True
    
    for item, item_type in required_items:
        path = Path(item)
        exists = path.exists()
        if not exists:
            all_exist = False
        results.append((item, exists, item_type))
    
    return all_exist, results


def test_api_connection():
    """Test connection to Deepseek API."""
    try:
        from src.utils.llm_client import get_llm_client
        
        console.print("[yellow]测试 API 连接（这可能需要几秒钟）...[/yellow]")
        
        client = get_llm_client()
        response = client.invoke("Hello", system_message="Reply with just 'OK'")
        
        if response:
            return True, "连接成功"
        return False, "无响应"
    
    except Exception as e:
        return False, f"连接失败: {str(e)}"


def main():
    """Main checker function."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]环境配置检查工具[/bold green]\n"
        "[dim]检查您的开发环境是否正确配置[/dim]",
        border_style="green"
    ))
    
    all_checks_passed = True
    
    # 1. Python Version
    console.print("\n[bold cyan]1. Python 版本检查[/bold cyan]")
    passed, info = check_python_version()
    status = "[green]✓[/green]" if passed else "[red]✗[/red]"
    console.print(f"   {status} Python {info}")
    all_checks_passed = all_checks_passed and passed
    
    # 2. Dependencies
    console.print("\n[bold cyan]2. 依赖包检查[/bold cyan]")
    passed, results = check_dependencies()
    
    table = Table(show_header=True, header_style="bold")
    table.add_column("包名", style="cyan")
    table.add_column("状态", style="green")
    
    for package, installed, status in results:
        status_icon = "✓" if installed else "✗"
        status_color = "green" if installed else "red"
        table.add_row(package, f"[{status_color}]{status_icon}[/{status_color}] {status}")
    
    console.print(table)
    all_checks_passed = all_checks_passed and passed
    
    if not passed:
        console.print("\n[yellow]💡 提示: 运行 'pip install -r requirements.txt' 安装缺失的包[/yellow]")
    
    # 3. .env File
    console.print("\n[bold cyan]3. 配置文件检查[/bold cyan]")
    passed, info = check_env_file()
    status = "[green]✓[/green]" if passed else "[red]✗[/red]"
    console.print(f"   {status} {info}")
    all_checks_passed = all_checks_passed and passed
    
    if not passed:
        console.print("\n[yellow]💡 提示: 复制 .env.example 为 .env 并配置 DEEPSEEK_API_KEY[/yellow]")
    
    # 4. Project Structure
    console.print("\n[bold cyan]4. 项目结构检查[/bold cyan]")
    passed, results = check_project_structure()
    
    missing_items = [item for item, exists, _ in results if not exists]
    if missing_items:
        console.print("[red]缺少以下文件或目录：[/red]")
        for item in missing_items:
            console.print(f"   [red]✗[/red] {item}")
    else:
        console.print("   [green]✓[/green] 所有文件和目录都存在")
    
    all_checks_passed = all_checks_passed and passed
    
    # 5. API Connection Test (optional)
    console.print("\n[bold cyan]5. API 连接测试[/bold cyan]")
    
    if not all_checks_passed:
        console.print("   [yellow]⚠[/yellow] 跳过（请先解决上述问题）")
    else:
        from rich.prompt import Confirm
        if Confirm.ask("是否测试 API 连接？", default=True):
            passed, info = test_api_connection()
            status = "[green]✓[/green]" if passed else "[red]✗[/red]"
            console.print(f"   {status} {info}")
            all_checks_passed = all_checks_passed and passed
        else:
            console.print("   [dim]已跳过[/dim]")
    
    # Summary
    console.print("\n" + "="*60)
    if all_checks_passed:
        console.print(Panel.fit(
            "[bold green]✅ 环境配置完成！[/bold green]\n\n"
            "您可以开始使用了：\n"
            "  • 运行 CLI: [cyan]python cli.py[/cyan]\n"
            "  • 运行测试: [cyan]python test_scenarios.py[/cyan]\n"
            "  • 查看文档: [cyan]README.md[/cyan]",
            border_style="green"
        ))
        return 0
    else:
        console.print(Panel.fit(
            "[bold yellow]⚠️  配置未完成[/bold yellow]\n\n"
            "请解决上述问题后重新运行此脚本。\n\n"
            "需要帮助？查看：\n"
            "  • [cyan]TROUBLESHOOTING.md[/cyan] - 故障排除指南\n"
            "  • [cyan]USAGE.md[/cyan] - 详细使用说明",
            border_style="yellow"
        ))
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  检查被中断[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[red]❌ 检查过程出错: {str(e)}[/red]")
        import traceback
        console.print("[dim]" + traceback.format_exc() + "[/dim]")
        sys.exit(1)
